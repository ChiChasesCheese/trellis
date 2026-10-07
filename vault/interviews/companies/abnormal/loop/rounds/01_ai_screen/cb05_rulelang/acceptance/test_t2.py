"""t2 -- detector dependencies. Uses only the existing `Detector.requires`, `register_detector`, `DETECTORS`
and the tenant `[detectors] disabled` key; skips are observed through the existing `rulelang.metrics`."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb05_support import A, BAD_LINK, T0, YOUNG_DOMAIN, build_env, email, tenant_toml  # noqa: E402

pytestmark = pytest.mark.t2

LOOKALIKE = "billing@acme-vend0r.example"  # new_sender + vendor_lookalike (which requires new_sender)


@pytest.fixture(autouse=True)
def restore_registry():
    from rulelang import metrics
    from rulelang.detectors import DETECTORS

    metrics.reset()
    saved = dict(DETECTORS)
    yield
    DETECTORS.clear()
    DETECTORS.update(saved)


def make_detector(name: str, requires: tuple[str, ...] = (), boom: bool = False):
    """Register a detector that fires always; its summary says whether its inputs were there."""
    from rulelang.detectors import Detector, register_detector
    from rulelang.models import Severity

    class _D(Detector):
        kinds = ("email",)

        def evaluate(self, event, ctx):
            if boom:
                raise RuntimeError("boom")
            ok = all(r in ctx.signals for r in requires)
            return self.signal(event, Severity.LOW, "with-input" if ok else "WITHOUT-INPUT")

    _D.name, _D.requires = name, tuple(requires)
    return register_detector(_D)


def mail(event_id="e1", frm=f"ivy@{A}"):
    return email(event_id, "acme", T0, frm, [f"erin@{A}"])


def summaries(env, event_id="e1"):
    return {s["detector"]: s["summary"] for s in env.signals("acme", event_id)}


def skip_count() -> int:
    from rulelang import metrics

    return sum(v for k, v in metrics.snapshot().items() if "skip" in k)


def with_disabled(root, tmp_path, *names):
    listed = ", ".join(f'"{n}"' for n in names)
    return build_env(root, tmp_path, {"acme": tenant_toml(f"[detectors]\ndisabled = [{listed}]\n")})


@pytest.mark.core
def test_builtin_results_do_not_depend_on_registration_order(codebase_root_path, tmp_path):
    from rulelang.detectors import DETECTORS

    (tmp_path / "a").mkdir()
    baseline_env = build_env(codebase_root_path, tmp_path / "a")
    baseline_env.ingest("acme", [mail("e1", LOOKALIKE)])
    baseline = summaries(baseline_env)
    assert "vendor_lookalike" in baseline  # sanity: the dependent detector fires in the default order

    reordered = dict(reversed(list(DETECTORS.items())))
    DETECTORS.clear()
    DETECTORS.update(reordered)
    (tmp_path / "b").mkdir()
    env = build_env(codebase_root_path, tmp_path / "b")
    env.ingest("acme", [mail("e1", LOOKALIKE)])
    assert summaries(env) == baseline


@pytest.mark.core
def test_a_detector_registered_before_its_input_still_sees_it(codebase_root_path, tmp_path):
    make_detector("zz_child", requires=("zz_parent",))
    make_detector("zz_parent")
    env = build_env(codebase_root_path, tmp_path)
    env.ingest("acme", [mail()])
    assert summaries(env) == {"zz_child": "with-input", "zz_parent": "with-input"}


@pytest.mark.core
def test_a_three_level_chain_registered_backwards(codebase_root_path, tmp_path):
    make_detector("zz_c", requires=("zz_b",))
    make_detector("zz_b", requires=("zz_a",))
    make_detector("zz_a")
    env = build_env(codebase_root_path, tmp_path)
    env.ingest("acme", [mail()])
    assert summaries(env) == {"zz_a": "with-input", "zz_b": "with-input", "zz_c": "with-input"}


@pytest.mark.core
def test_a_cycle_is_reported_at_startup_naming_its_members(codebase_root_path, tmp_path):
    make_detector("cyc_a", requires=("cyc_b",))
    make_detector("cyc_b", requires=("cyc_c",))
    make_detector("cyc_c", requires=("cyc_a",))
    make_detector("innocent")
    with pytest.raises(Exception) as exc:
        env = build_env(codebase_root_path, tmp_path)
        env.ingest("acme", [mail()])
    text = str(exc.value)
    assert all(n in text for n in ("cyc_a", "cyc_b", "cyc_c")), text
    assert "innocent" not in text


@pytest.mark.core
def test_disabling_an_upstream_skips_its_dependant_and_counts_it(codebase_root_path, tmp_path):
    make_detector("zz_up")
    make_detector("zz_down", requires=("zz_up",))
    make_detector("zz_other")
    env = with_disabled(codebase_root_path, tmp_path, "zz_up")
    env.ingest("acme", [mail()])
    assert summaries(env) == {"zz_other": "with-input"}
    assert skip_count() >= 1


@pytest.mark.core
def test_a_crashing_upstream_skips_its_dependant_but_not_the_rest(codebase_root_path, tmp_path):
    make_detector("zz_up", boom=True)
    make_detector("zz_down", requires=("zz_up",))
    make_detector("zz_other")
    env = build_env(codebase_root_path, tmp_path)
    env.ingest("acme", [mail("e1"), mail("e2")])
    for event_id in ("e1", "e2"):
        assert summaries(env, event_id) == {"zz_other": "with-input"}
    assert skip_count() >= 2  # once per event


@pytest.mark.stretch
def test_skips_cascade_down_the_chain(codebase_root_path, tmp_path):
    make_detector("zz_a")
    make_detector("zz_b", requires=("zz_a",))
    make_detector("zz_c", requires=("zz_b",))
    env = with_disabled(codebase_root_path, tmp_path, "zz_a")
    env.ingest("acme", [mail()])
    assert summaries(env) == {}
    assert skip_count() >= 2


@pytest.mark.stretch
def test_requiring_an_unregistered_detector_fails_at_startup(codebase_root_path, tmp_path):
    make_detector("zz_orphan", requires=("ghost",))
    with pytest.raises(Exception) as exc:
        env = build_env(codebase_root_path, tmp_path)
        env.ingest("acme", [mail()])
    assert "ghost" in str(exc.value)


@pytest.mark.regression
def test_default_signals_are_unchanged(codebase_root_path, tmp_path):
    env = build_env(codebase_root_path, tmp_path)
    env.ingest("acme", [email("e1", "acme", T0, f"x@{YOUNG_DOMAIN}", [f"erin@{A}"], links=[BAD_LINK]),
                        mail("e2", LOOKALIKE)])
    assert env.detectors("acme", "e1") == {"new_sender", "suspicious_link"}
    assert env.detectors("acme", "e2") == {"new_sender", "vendor_lookalike"}


@pytest.mark.regression
def test_disabling_an_unrelated_detector_changes_nothing_else(codebase_root_path, tmp_path):
    env = with_disabled(codebase_root_path, tmp_path, "mass_mailing")
    env.ingest("acme", [mail("e1", LOOKALIKE)])
    assert env.detectors("acme", "e1") == {"new_sender", "vendor_lookalike"}
    assert skip_count() == 0
