from datetime import datetime, timezone

import pytest

from vetting.models import Disposition, Identity, Kind, Observation, Recommendation, Review
from vetting.store import Store, migrate

T = datetime(2026, 9, 14, 12, tzinfo=timezone.utc)


def ident(tenant="acme", i="greenhouse:1"):
    return Identity(i, tenant, "greenhouse", "1", "A B", T)


def obs(tenant="acme", i="greenhouse:1", kind=Kind.PHONE, value="+14155550143", ref="r1"):
    return Observation(i, tenant, kind, value, "greenhouse", T, ref)


def test_migrations_apply_once(store):
    assert migrate(store.conn) == []


def test_identity_upsert_is_idempotent_and_tenant_scoped(store):
    store.identities.upsert(ident())
    store.identities.upsert(ident())
    assert len(store.identities.list("acme")) == 1
    assert store.identities.get("globex", "greenhouse:1") is None


def test_observations_ignore_redelivery_and_stay_in_tenant(store):
    assert store.observations.add_many([obs(), obs()]) == 1
    assert store.observations.add_many([obs()]) == 0
    store.observations.add_many([obs(tenant="globex")])
    assert len(store.observations.find("acme", Kind.PHONE, "+14155550143")) == 1
    assert store.observations.find("acme", Kind.PHONE, "(415) 555-0143") == []
    assert len(store.observations.list_by_kind("globex", Kind.PHONE)) == 1


def test_review_roundtrip_and_dispositions_survive_resave(store):
    review = Review("acme", "greenhouse:1", Recommendation.RECOMMENDED, 30, [], T)
    store.reviews.save(review)
    store.reviews.add_disposition("acme", Disposition("greenhouse:1", "cleared", "ok", T))
    store.reviews.save(review)
    assert store.reviews.get("acme", "greenhouse:1").score == 30
    assert [d.decision for d in store.reviews.dispositions("acme", "greenhouse:1")] == ["cleared"]
    assert store.reviews.dispositions("globex", "greenhouse:1") == []


def test_disposition_check_constraint(store):
    with pytest.raises(Exception):
        store.conn.execute(
            "INSERT INTO dispositions (tenant_id, identity_id, decision, decided_at) VALUES ('a', 'b', 'maybe', 'c')"
        )
