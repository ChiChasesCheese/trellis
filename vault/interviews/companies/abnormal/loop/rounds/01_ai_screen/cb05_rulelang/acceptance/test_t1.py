"""t1 -- customer rules. New names: the `[rules]` table in tenant config; results show up via GET /signals."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb05_support import (  # noqa: E402
    A, BAD_LINK, OLD_DOMAIN, T0, YOUNG_DOMAIN, build_env, email, make_config, run_cli, tenant_toml,
)

pytestmark = pytest.mark.t1

RULE = "sender.domain_age_days < 7 and any(link.host in intel.bad_hosts)"


def rules_env(codebase_root_path, tmp_path, rules: dict[str, str]):
    """An app whose acme tenant file defines ``rules`` (TOML literal strings, so expressions may hold double quotes)."""
    body = "[rules]\n" + "".join(f"{name} = '{expr}'\n" for name, expr in rules.items())
    return build_env(codebase_root_path, tmp_path, {"acme": tenant_toml(body)})


def mail(event_id, sender_domain, links=(), subject="hello", tenant="acme", to=None):
    return email(event_id, tenant, T0, f"x@{sender_domain}", to or [f"erin@{A}"], subject, links)


@pytest.mark.core
def test_ticket_example_flags_a_young_sender_with_a_bad_link(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"young_bad_link": RULE})
    env.ingest("acme", [mail("e1", YOUNG_DOMAIN, [BAD_LINK])])
    assert "young_bad_link" in env.detectors("acme", "e1")


@pytest.mark.core
def test_an_old_sender_with_a_bad_link_is_not_flagged(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"young_bad_link": RULE})
    env.ingest("acme", [mail("e1", YOUNG_DOMAIN, [BAD_LINK]), mail("e2", OLD_DOMAIN, [BAD_LINK])])
    assert "young_bad_link" in env.detectors("acme", "e1")
    assert "young_bad_link" not in env.detectors("acme", "e2")


@pytest.mark.core
def test_a_young_sender_with_clean_links_is_not_flagged(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"young_bad_link": RULE})
    env.ingest("acme", [mail("e1", YOUNG_DOMAIN, [BAD_LINK]), mail("e2", YOUNG_DOMAIN, ["https://docs.example/a"]),
                        mail("e3", YOUNG_DOMAIN, [])])
    assert "young_bad_link" in env.detectors("acme", "e1")
    assert "young_bad_link" not in env.detectors("acme", "e2") | env.detectors("acme", "e3")


@pytest.mark.core
def test_a_rule_signal_has_the_same_shape_as_a_builtin_signal(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"young_bad_link": RULE})
    env.ingest("acme", [mail("e1", YOUNG_DOMAIN, [BAD_LINK])])
    by_name = {s["detector"]: s for s in env.signals("acme", "e1")}
    assert "suspicious_link" in by_name and "young_bad_link" in by_name  # the builtin still fires too
    assert set(by_name["young_bad_link"]) == set(by_name["suspicious_link"])
    assert by_name["young_bad_link"]["event_id"] == "e1"
    assert by_name["young_bad_link"]["severity"] in {"low", "medium", "high", "critical"}


@pytest.mark.core
def test_and_binds_tighter_than_or_and_not_and_parentheses_work(codebase_root_path, tmp_path):
    rules = {
        "prec": f'sender.domain == "{YOUNG_DOMAIN}" or sender.domain == "{OLD_DOMAIN}" and subject == "Invoice"',
        "negated": f'not (sender.domain == "{OLD_DOMAIN}") and subject == "Invoice"',
    }
    env = rules_env(codebase_root_path, tmp_path, rules)
    env.ingest("acme", [mail("young_hello", YOUNG_DOMAIN, subject="Hello"), mail("old_hello", OLD_DOMAIN, subject="Hello"),
                        mail("old_inv", OLD_DOMAIN, subject="Invoice"), mail("young_inv", YOUNG_DOMAIN, subject="Invoice")])
    assert "prec" in env.detectors("acme", "young_hello")      # and binds tighter than or
    assert "prec" not in env.detectors("acme", "old_hello")
    assert "prec" in env.detectors("acme", "old_inv")
    assert "negated" in env.detectors("acme", "young_inv")
    assert "negated" not in env.detectors("acme", "old_inv")


@pytest.mark.core
def test_a_syntax_error_exits_2_naming_the_rule_and_the_position(codebase_root_path, tmp_path):
    source = 'sender.domain == == "x"'
    cfg = make_config(codebase_root_path, tmp_path, {"acme": tenant_toml(f'[rules]\nbroken_rule = \'{source}\'\n')})
    events = tmp_path / "events"
    events.mkdir()
    (events / "e.jsonl").write_text("")
    done = run_cli(codebase_root_path, "run", str(events), "--tenant", "acme", "--db", str(tmp_path / "r.db"),
                   "--config-dir", str(cfg))
    assert done.returncode == 2, done.stderr
    assert "broken_rule" in done.stderr
    second_op = source.rindex("==") + 1  # 1-based column of the offending token (0-based is tolerated)
    assert re.search(rf"\b({second_op}|{second_op - 1})\b", done.stderr), done.stderr
    assert "Traceback" not in done.stderr


@pytest.mark.core
def test_an_unknown_field_is_rejected_when_the_config_loads(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"good": "sender.internal", "typo": "sender.favourite_colour == 3"})
    with pytest.raises(Exception) as exc:
        env.ingest("acme", [mail("e1", YOUNG_DOMAIN)])
    assert "typo" in str(exc.value) or "favourite_colour" in str(exc.value)
    assert env.app.pipeline.signals.list("acme") == []  # nothing ran before the error


@pytest.mark.core
def test_rules_belong_to_the_tenant_that_defined_them(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"young_bad_link": RULE})
    env.ingest("acme", [mail("a1", YOUNG_DOMAIN, [BAD_LINK])])
    env.ingest("globex", [mail("g1", YOUNG_DOMAIN, [BAD_LINK], tenant="globex", to=["kim@globex.example"])])
    assert "young_bad_link" in env.detectors("acme", "a1")
    assert "young_bad_link" not in env.detectors("globex", "g1")
    assert "suspicious_link" in env.detectors("globex", "g1")


@pytest.mark.core
def test_cli_signals_lists_the_rule_hit(codebase_root_path, tmp_path):
    cfg = make_config(codebase_root_path, tmp_path, {"acme": tenant_toml(f'[rules]\nyoung_bad_link = "{RULE}"\n')})
    events = tmp_path / "events"
    events.mkdir()
    (events / "e.jsonl").write_text(__import__("json").dumps(mail("e1", YOUNG_DOMAIN, [BAD_LINK])) + "\n")
    common = ["--db", str(tmp_path / "r.db"), "--config-dir", str(cfg)]
    assert run_cli(codebase_root_path, "run", str(events), "--tenant", "acme", *common).returncode == 0
    done = run_cli(codebase_root_path, "signals", "e1", "--tenant", "acme", *common)
    assert done.returncode == 0, done.stderr
    assert "young_bad_link" in done.stdout and "suspicious_link" in done.stdout


@pytest.mark.stretch
def test_comparing_a_number_with_a_string_is_rejected_at_load(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"mixed_up": 'sender.domain_age_days > "7"'})
    with pytest.raises(Exception) as exc:
        env.ingest("acme", [mail("e1", YOUNG_DOMAIN)])
    assert "mixed_up" in str(exc.value)


@pytest.mark.stretch
def test_a_rule_cannot_run_code(codebase_root_path, tmp_path):
    marker = tmp_path / "PWNED"
    env = rules_env(codebase_root_path, tmp_path, {"evil": f'__import__("os").system("touch {marker}")'})
    with pytest.raises(Exception) as exc:
        env.ingest("acme", [mail("e1", YOUNG_DOMAIN)])
    assert "evil" in str(exc.value)
    assert not marker.exists()


@pytest.mark.stretch
def test_in_also_works_on_text(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"urgent": '"urgent" in subject'})
    env.ingest("acme", [mail("e1", OLD_DOMAIN, subject="very urgent: pay"), mail("e2", OLD_DOMAIN, subject="lunch")])
    assert "urgent" in env.detectors("acme", "e1") and "urgent" not in env.detectors("acme", "e2")


@pytest.mark.stretch
def test_a_rule_cannot_take_a_builtin_detectors_name(codebase_root_path, tmp_path):
    env = rules_env(codebase_root_path, tmp_path, {"new_sender": "sender.internal"})
    with pytest.raises(Exception) as exc:
        env.ingest("acme", [mail("e1", OLD_DOMAIN)])
    assert "new_sender" in str(exc.value)


@pytest.mark.regression
def test_builtin_detectors_still_fire_without_any_rules(codebase_root_path, tmp_path):
    env = build_env(codebase_root_path, tmp_path)
    env.ingest("acme", [mail("e1", YOUNG_DOMAIN, [BAD_LINK])])
    assert env.detectors("acme", "e1") == {"new_sender", "suspicious_link"}


@pytest.mark.regression
def test_signals_are_still_tenant_scoped(codebase_root_path, tmp_path):
    env = build_env(codebase_root_path, tmp_path)
    env.ingest("acme", [mail("e1", YOUNG_DOMAIN, [BAD_LINK])])
    assert env.client("globex").get("/signals", params={"event_id": "e1"}).status_code == 404
    assert env.client("acme").get("/signals", params={"event_id": "e1"}).status_code == 200
