from __future__ import annotations

import json
import sqlite3

from vetting.models import (
    Disposition,
    Finding,
    Identity,
    Kind,
    Observation,
    Recommendation,
    Review,
)
from vetting.timeutil import parse_ts, to_iso


class IdentityRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def upsert(self, identity: Identity) -> None:
        self._conn.execute(
            "INSERT INTO identities (tenant_id, id, source, external_id, display_name, applied_at) "
            "VALUES (?, ?, ?, ?, ?, ?) "
            "ON CONFLICT (tenant_id, id) DO UPDATE SET display_name = excluded.display_name, "
            "applied_at = excluded.applied_at",
            (
                identity.tenant_id,
                identity.id,
                identity.source,
                identity.external_id,
                identity.display_name,
                to_iso(identity.applied_at),
            ),
        )

    def get(self, tenant_id: str, identity_id: str) -> Identity | None:
        row = self._conn.execute(
            "SELECT * FROM identities WHERE tenant_id = ? AND id = ?", (tenant_id, identity_id)
        ).fetchone()
        return self._row(row) if row else None

    def list(self, tenant_id: str) -> list[Identity]:
        rows = self._conn.execute(
            "SELECT * FROM identities WHERE tenant_id = ? ORDER BY applied_at, id", (tenant_id,)
        ).fetchall()
        return [self._row(row) for row in rows]

    @staticmethod
    def _row(row: sqlite3.Row) -> Identity:
        return Identity(
            id=row["id"],
            tenant_id=row["tenant_id"],
            source=row["source"],
            external_id=row["external_id"],
            display_name=row["display_name"],
            applied_at=parse_ts(row["applied_at"]),
        )


class ObservationRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def add_many(self, observations: list[Observation]) -> int:
        """Insert observations; re-delivered ones (same identity, kind, value, ref) are ignored."""
        before = self._conn.total_changes
        self._conn.executemany(
            "INSERT OR IGNORE INTO observations (tenant_id, identity_id, kind, value, source, ts, raw_ref) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (o.tenant_id, o.identity_id, o.kind.value, o.value, o.source, to_iso(o.ts), o.raw_ref)
                for o in observations
            ],
        )
        return self._conn.total_changes - before

    def for_identity(self, tenant_id: str, identity_id: str) -> list[Observation]:
        return self._query(
            "WHERE tenant_id = ? AND identity_id = ? ORDER BY ts, id", (tenant_id, identity_id)
        )

    def find(self, tenant_id: str, kind: Kind, value: str) -> list[Observation]:
        """Observations of ``kind`` whose stored value equals ``value`` exactly (indexed)."""
        return self._query("WHERE tenant_id = ? AND kind = ? AND value = ? ORDER BY id", (tenant_id, kind.value, value))

    def list_by_kind(self, tenant_id: str, kind: Kind) -> list[Observation]:
        return self._query("WHERE tenant_id = ? AND kind = ? ORDER BY id", (tenant_id, kind.value))

    def _query(self, where: str, params: tuple) -> list[Observation]:
        rows = self._conn.execute(f"SELECT * FROM observations {where}", params).fetchall()
        return [
            Observation(
                identity_id=r["identity_id"],
                tenant_id=r["tenant_id"],
                kind=Kind(r["kind"]),
                value=r["value"],
                source=r["source"],
                ts=parse_ts(r["ts"]),
                raw_ref=r["raw_ref"],
            )
            for r in rows
        ]


class ReviewRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def save(self, review: Review) -> None:
        """Insert or replace the computed review. Dispositions are separate and never touched."""
        self._conn.execute(
            "INSERT OR REPLACE INTO reviews "
            "(tenant_id, identity_id, recommendation, score, findings_json, evaluated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                review.tenant_id,
                review.identity_id,
                review.recommendation.value,
                review.score,
                json.dumps([f.to_dict() for f in review.findings]),
                to_iso(review.evaluated_at) if review.evaluated_at else "",
            ),
        )

    def get(self, tenant_id: str, identity_id: str) -> Review | None:
        row = self._conn.execute(
            "SELECT * FROM reviews WHERE tenant_id = ? AND identity_id = ?", (tenant_id, identity_id)
        ).fetchone()
        return self._row(row) if row else None

    def list(self, tenant_id: str, recommendation: Recommendation | None = None) -> list[Review]:
        sql, params = "SELECT * FROM reviews WHERE tenant_id = ?", [tenant_id]
        if recommendation is not None:
            sql += " AND recommendation = ?"
            params.append(recommendation.value)
        rows = self._conn.execute(sql + " ORDER BY score DESC, identity_id", params).fetchall()
        return [self._row(row) for row in rows]

    def add_disposition(self, tenant_id: str, disposition: Disposition) -> None:
        self._conn.execute(
            "INSERT INTO dispositions (tenant_id, identity_id, decision, note, decided_at) VALUES (?, ?, ?, ?, ?)",
            (tenant_id, disposition.identity_id, disposition.decision, disposition.note, to_iso(disposition.decided_at)),
        )

    def dispositions(self, tenant_id: str, identity_id: str) -> list[Disposition]:
        rows = self._conn.execute(
            "SELECT * FROM dispositions WHERE tenant_id = ? AND identity_id = ? ORDER BY id",
            (tenant_id, identity_id),
        ).fetchall()
        return [
            Disposition(r["identity_id"], r["decision"], r["note"], parse_ts(r["decided_at"])) for r in rows
        ]

    def latest_disposition(self, tenant_id: str, identity_id: str) -> Disposition | None:
        history = self.dispositions(tenant_id, identity_id)
        return history[-1] if history else None

    def reviewer_subjects(self, tenant_id: str) -> dict[str, set[str]]:
        """Finding subjects of identities by their *latest* decision: ``{"cleared": {...}, "escalated": {...}}``."""
        rows = self._conn.execute(
            "SELECT d.decision, r.findings_json FROM reviews r JOIN dispositions d "
            "ON d.tenant_id = r.tenant_id AND d.identity_id = r.identity_id "
            "AND d.id = (SELECT MAX(id) FROM dispositions WHERE tenant_id = r.tenant_id AND identity_id = r.identity_id) "
            "WHERE r.tenant_id = ?",
            (tenant_id,),
        ).fetchall()
        out: dict[str, set[str]] = {"cleared": set(), "escalated": set()}
        for row in rows:
            out[row["decision"]].update(f["subject"] for f in json.loads(row["findings_json"]) if f.get("subject"))
        return out

    @staticmethod
    def _row(row: sqlite3.Row) -> Review:
        return Review(
            tenant_id=row["tenant_id"],
            identity_id=row["identity_id"],
            recommendation=Recommendation(row["recommendation"]),
            score=row["score"],
            findings=[Finding.from_dict(d) for d in json.loads(row["findings_json"])],
            evaluated_at=parse_ts(row["evaluated_at"]) if row["evaluated_at"] else None,
        )
