"""ingest -> store -> signals -> score -> review."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from vetting import scoring
from vetting.lookups import Lookups, build_lookups
from vetting.metrics import metrics
from vetting.models import Identity, Review
from vetting.settings import DEFAULT_CONFIG_DIR, DEFAULT_INTEL_DIR, Settings, load_settings
from vetting.signals import SIGNALS, SignalContext, all_signals
from vetting.sources import SOURCES, Ingested, Source
from vetting.store import Store
from vetting.timeutil import utcnow

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class IngestResult:
    identities: int
    observations: int
    reviews: int


class Pipeline:
    """One tenant's pipeline. Build with ``Pipeline.for_tenant`` unless a test injects pieces."""

    def __init__(
        self, store: Store, settings: Settings, lookups: Lookups, sources: list[Source] | None = None
    ) -> None:
        self.store = store
        self.settings = settings
        self.lookups = lookups
        self.sources = sources if sources is not None else [cls() for cls in SOURCES.values()]
        self.signals = all_signals()
        settings.require_weights(SIGNALS)

    @classmethod
    def for_tenant(
        cls,
        tenant_id: str,
        store: Store,
        config_dir: Path = DEFAULT_CONFIG_DIR,
        intel_dir: Path = DEFAULT_INTEL_DIR,
    ) -> "Pipeline":
        settings = load_settings(tenant_id, config_dir)
        return cls(store, settings, build_lookups(intel_dir, settings.cache_ttl_seconds))

    def ingest(self, root: Path) -> IngestResult:
        """Load every source under ``root`` for this tenant, then re-evaluate the whole tenant.

        Re-evaluating everything (not just the new identities) is deliberate: findings can depend
        on what else is in the store, and ingest is re-runnable.
        """
        tenant = self.settings.tenant_id
        batches: list[Ingested] = [b for source in self.sources for b in source.load(root, tenant)]
        for batch in batches:
            if batch.identity is not None:
                self.store.identities.upsert(batch.identity)
        added = 0
        for batch in batches:
            if not batch.observations:
                continue
            if self.store.identities.get(tenant, batch.observations[0].identity_id) is None:
                metrics.incr("pipeline.orphan_observations", len(batch.observations))
                continue
            added += self.store.observations.add_many(batch.observations)
        reviews = self.evaluate_all()
        self.store.conn.commit()
        return IngestResult(
            identities=len(self.store.identities.list(tenant)), observations=added, reviews=len(reviews)
        )

    def evaluate_all(self) -> list[Review]:
        return [self.evaluate(identity) for identity in self.store.identities.list(self.settings.tenant_id)]

    def evaluate(self, identity: Identity) -> Review:
        observations = self.store.observations.for_identity(identity.tenant_id, identity.id)
        ctx = SignalContext(identity, observations, self.lookups, self.settings, self.store)
        findings = [f for f in (signal.evaluate(ctx) for signal in self.signals) if f is not None]
        total, recommendation = scoring.score(findings, self.settings)
        review = Review(identity.tenant_id, identity.id, recommendation, total, findings, utcnow())
        self.store.reviews.save(review)
        return review
