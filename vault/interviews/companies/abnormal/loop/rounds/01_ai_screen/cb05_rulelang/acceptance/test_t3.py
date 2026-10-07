"""t3 -- blast radius. New names: GET /blast-radius?account=&since=, `blast-radius` CLI command,
`[blast_radius] max_hops`. The response shape is not fixed by the ticket, so the helpers below accept any
sensible one: a list under any key, each entry naming an address and carrying its path."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb05_support import (  # noqa: E402
    A, T0, VENDOR, build_env, compromise_scenario, email, person, run_cli, stamp, tenant_toml,
)

pytestmark = pytest.mark.t3

ADDRESS_KEYS = ("address", "account", "addr", "email", "person", "user")
DANA = person("dana")


def _text(path) -> str:
    if isinstance(path, str):
        return path
    return " ".join(p if isinstance(p, str) else " ".join(str(v) for v in p.values()) for p in path)


def people(body) -> dict[str, str]:
    """{address: path as text} from whatever list the endpoint returned."""
    items = body if isinstance(body, list) else next(v for v in body.values() if isinstance(v, list))
    found = {}
    for item in items:
        if isinstance(item, str):
            found[item] = ""
            continue
        address = next(item[k] for k in ADDRESS_KEYS if k in item)
        path = next((v for k, v in item.items() if "path" in k.lower() or "chain" in k.lower()), [])
        found[address] = _text(path)
    return found


@pytest.fixture
def env(codebase_root_path, tmp_path):
    env = build_env(codebase_root_path, tmp_path)
    env.ingest("acme", compromise_scenario())
    return env


def query(env, tenant="acme", account=DANA, since=T0):
    return env.client(tenant).get("/blast-radius", params={"account": account, "since": stamp(since)})


@pytest.mark.core
def test_default_hop_limit_lists_the_expected_people(env):
    resp = query(env)
    assert resp.status_code == 200, resp.json
    found = people(resp.json)
    assert {person("erin"), person("pat"), VENDOR, person("frank"), person("gus")} <= set(found)
    for left_out in ("old", "old2", "ivy", "zoe", "hank"):
        assert person(left_out) not in found, left_out
    assert DANA not in found


@pytest.mark.core
def test_every_person_comes_with_the_path_that_put_them_there(env):
    found = people(query(env).json)
    assert person("erin") in found[person("frank")] and DANA in found[person("frank")]
    assert person("erin") in found[person("gus")]
    assert DANA in found[person("erin")]


@pytest.mark.core
def test_contacts_before_the_compromise_do_not_count(env):
    found = people(query(env).json)
    assert person("old") not in found and person("old2") not in found
    assert person("pat") in found  # emailed before *and* after: the later contact counts
    later = people(query(env, since=T0.replace(hour=12)).json)
    assert person("pat") not in later and person("erin") not in later


@pytest.mark.core
def test_the_hop_limit_is_a_tenant_setting(codebase_root_path, tmp_path):
    results = {}
    for hops in (1, 3):
        sub = tmp_path / f"hops{hops}"
        sub.mkdir()
        e = build_env(codebase_root_path, sub, {"acme": tenant_toml(f"[blast_radius]\nmax_hops = {hops}\n")})
        e.ingest("acme", compromise_scenario())
        resp = query(e)
        assert resp.status_code == 200, resp.json
        results[hops] = set(people(resp.json))
    assert person("erin") in results[1] and person("frank") not in results[1] and person("gus") not in results[1]
    assert person("hank") in results[3] and person("frank") in results[3]


@pytest.mark.core
def test_external_addresses_are_reported_but_never_expanded(codebase_root_path, tmp_path):
    e = build_env(codebase_root_path, tmp_path, {"acme": tenant_toml("[blast_radius]\nmax_hops = 5\n")})
    e.ingest("acme", compromise_scenario())
    found = people(query(e).json)
    assert VENDOR in found
    assert person("zoe") not in found


@pytest.mark.core
def test_other_tenants_cannot_see_it(env):
    assert person("erin") in people(query(env).json)
    other = query(env, tenant="globex")
    assert not any(person(n) in other.body.decode() for n in ("erin", "pat", "frank", "gus"))


@pytest.mark.core
def test_the_cli_prints_the_same_people(codebase_root_path, tmp_path):
    rows = compromise_scenario()
    events = tmp_path / "events"
    events.mkdir()
    (events / "e.jsonl").write_text("\n".join(__import__("json").dumps(r) for r in rows) + "\n")
    db = str(tmp_path / "r.db")
    assert run_cli(codebase_root_path, "run", str(events), "--tenant", "acme", "--db", db).returncode == 0
    done = run_cli(codebase_root_path, "blast-radius", DANA, "--since", stamp(T0), "--tenant", "acme", "--db", db)
    assert done.returncode == 0, done.stderr
    for name in ("erin", "pat", "frank", "gus"):
        assert person(name) in done.stdout
    assert person("hank") not in done.stdout and person("old") not in done.stdout


@pytest.mark.stretch
def test_a_forward_cannot_predate_the_message_it_forwards(env):
    # erin mailed jon at T0+30m, half an hour before dana's mail reached her at T0+60m.
    found = people(query(env).json)
    assert person("jon") not in found
    assert person("frank") in found


@pytest.mark.stretch
def test_bad_input_is_a_400(env):
    client = env.client("acme")
    assert client.get("/blast-radius", params={"since": stamp(T0)}).status_code == 400
    assert client.get("/blast-radius", params={"account": DANA}).status_code == 400
    assert client.get("/blast-radius", params={"account": DANA, "since": "yesterday-ish"}).status_code == 400


@pytest.mark.regression
def test_ingest_and_signals_still_work(codebase_root_path, tmp_path):
    e = build_env(codebase_root_path, tmp_path)
    e.ingest("acme", [email("x1", "acme", T0, "bob@fresh-supplier.example", [person("erin")])])
    assert {s["detector"] for s in e.signals("acme", "x1")} == {"new_sender"}


@pytest.mark.regression
def test_a_reply_from_a_known_contact_is_still_not_a_new_sender(env):
    # the scenario has dana writing to the vendor, so the vendor writing back is not a first contact
    env.ingest("acme", [email("x2", "acme", T0.replace(day=11), VENDOR, [DANA])])
    assert env.signals("acme", "x2") == []
