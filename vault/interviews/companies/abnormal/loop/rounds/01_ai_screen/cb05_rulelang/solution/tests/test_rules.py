"""The customer rule language: parsing, load-time checks, evaluation, and the CustomRuleDetector."""
from __future__ import annotations

import shutil

import pytest

from rulelang.app import create_app
from rulelang.config import CONFIG_DIR, FIXTURES_DIR
from rulelang.errors import ConfigError
from rulelang.rules import RuleSyntaxError, compile_rule
from rulelang.rules.fields import Scope

TICKET_RULE = "sender.domain_age_days < 7 and any(link.host in intel.bad_hosts)"


@pytest.fixture
def scope_for(app, make_email):
    from rulelang.intel import IntelStore

    intel = IntelStore(app.settings.for_tenant("acme").intel)

    def _scope(**kw):
        return Scope(make_email(**kw), intel, ("acme.example",))

    return _scope


def _config_with(tmp_path, tenant_toml: str):
    cfg = tmp_path / "config"
    shutil.copytree(CONFIG_DIR, cfg)
    (cfg / "tenants" / "acme.toml").write_text('[tenant]\ninternal_domains = ["acme.example"]\n' + tenant_toml)
    return create_app(config_dir=cfg, fixtures_dir=FIXTURES_DIR)


def test_ticket_rule_matches_young_sender_with_bad_link(scope_for):
    rule = compile_rule("young_bad_link", TICKET_RULE)
    hit = scope_for(actor="x@fresh-supplier.example", links=("https://login-secure.evil-payments.example/p",))
    assert rule.matches(hit)
    assert not rule.matches(scope_for(actor="x@oldcorp.example", links=hit.event.links))
    assert not rule.matches(scope_for(actor="x@fresh-supplier.example", links=("https://fine.example/",)))


def test_precedence_not_and_parentheses(scope_for):
    s = scope_for(actor="x@oldcorp.example", subject="Invoice")
    assert compile_rule("r", 'sender.domain == "a.example" or sender.domain == "oldcorp.example" and subject == "Invoice"').matches(s)
    assert not compile_rule("r", '(sender.domain == "a.example" or sender.domain == "oldcorp.example") and not subject == "Invoice"').matches(s)
    assert compile_rule("r", '"INVOICE" in subject').matches(s) is False  # case-sensitive substring
    assert compile_rule("r", '"nvoic" in subject').matches(s)


def test_unknown_age_never_matches(scope_for):
    s = scope_for(actor="x@never-seen.example")
    assert not compile_rule("r", "sender.domain_age_days < 7").matches(s)
    assert not compile_rule("r", "sender.domain_age_days != 7").matches(s)


def test_any_over_recipients(scope_for):
    s = scope_for(recipients=("a@acme.example", "b@globex.example"))
    assert compile_rule("r", 'any(recipient.domain == "globex.example")').matches(s)
    assert not compile_rule("r", 'any(recipient.domain == "other.example")').matches(s)


@pytest.mark.parametrize(
    "source,needle,column",
    [
        ('sender.domain == == "x"', "expected a field", 18),
        ("sender.domain_age_days <", "end of rule", 25),
        ('subject == "unterminated', "unexpected character", 12),
        ("sender.favourite_colour == 3", "unknown field", 1),
        ('sender.domain_age_days > "7"', "compares numbers", 24),
        ("link.host == 'x'", "inside any", 1),
        ("any(subject == 'x')", "exactly one", 1),
        ("sender.domain", "true/false", 1),
        ('__import__("os")', "expected", 11),
    ],
)
def test_load_time_errors_carry_rule_name_and_position(source, needle, column):
    with pytest.raises(RuleSyntaxError) as exc:
        compile_rule("my_rule", source)
    assert "'my_rule'" in str(exc.value) and needle in str(exc.value) and exc.value.column == column


def test_custom_rule_signal_has_the_builtin_shape(tmp_path, make_email):
    app = _config_with(tmp_path, f'[rules]\nyoung_bad_link = "{TICKET_RULE}"\n')
    signals = app.pipeline.process(
        make_email(actor="x@fresh-supplier.example", links=("https://login-secure.evil-payments.example/p",))
    )
    assert sorted(s.detector for s in signals) == ["new_sender", "suspicious_link", "young_bad_link"]
    custom = next(s for s in signals if s.detector == "young_bad_link")
    assert set(custom.to_dict()) == set(signals[0].to_dict()) and custom.evidence["expression"] == TICKET_RULE


def test_bad_rule_fails_the_tenant_load_not_the_event(tmp_path, events_dir):
    app = _config_with(tmp_path, '[rules]\nbroken = "sender.nope < 3"\n')
    with pytest.raises(ConfigError, match="unknown field"):
        app.pipeline.ingest_dir(events_dir, "acme")
    assert app.pipeline.signals.list("acme") == []


def test_rule_name_clashing_with_a_builtin_is_rejected(tmp_path, events_dir):
    app = _config_with(tmp_path, '[rules]\nnew_sender = "sender.internal"\n')
    with pytest.raises(ConfigError, match="clash"):
        app.pipeline.ingest_dir(events_dir, "acme")


def test_rules_are_per_tenant(tmp_path, make_email):
    app = _config_with(tmp_path, '[rules]\nany_mail = "recipient_count >= 1"\n')
    assert "any_mail" in [s.detector for s in app.pipeline.process(make_email())]
    other = make_email(tenant_id="globex", actor="lee@globex.example", recipients=("kim@globex.example",))
    assert "any_mail" not in [s.detector for s in app.pipeline.process(other)]
