"""CommGraph."""
from __future__ import annotations

from datetime import timedelta

from rulelang.graph import CommGraph
from rulelang.store import connect, migrate


def _graph(tenant="acme"):
    conn = connect()
    migrate(conn)
    return CommGraph(conn, tenant)


def test_record_builds_directed_edges_with_first_and_last_contact(make_email):
    g = _graph()
    first = make_email(actor="a@acme.example", recipients=("b@acme.example", "c@acme.example"))
    later = make_email(actor="a@acme.example", recipients=("b@acme.example",), ts=first.ts + timedelta(days=2))
    g.record(first)
    g.record(later)
    edges = {e.dst: e for e in g.neighbors("a@acme.example")}
    assert set(edges) == {"b@acme.example", "c@acme.example"}
    assert edges["b@acme.example"].count == 2
    assert edges["b@acme.example"].first_ts == first.ts and edges["b@acme.example"].last_ts == later.ts
    assert g.neighbors("b@acme.example") == []  # edges are directed


def test_first_contact_is_none_for_strangers(make_email):
    g = _graph()
    g.record(make_email(actor="a@acme.example", recipients=("b@acme.example",)))
    assert g.first_contact("a@acme.example", "b@acme.example") is not None
    assert g.first_contact("b@acme.example", "a@acme.example") is None


def test_graphs_are_tenant_scoped(make_email):
    conn = connect()
    migrate(conn)
    CommGraph(conn, "acme").record(make_email(actor="a@acme.example", recipients=("b@acme.example",)))
    assert CommGraph(conn, "globex").neighbors("a@acme.example") == []


def test_non_email_events_add_no_edges(make_email):
    g = _graph()
    g.record(make_email(kind="login", actor="a@acme.example", recipients=("b@acme.example",)))
    assert g.neighbors("a@acme.example") == []
