"""Runtime configuration. One frozen dataclass; override from a TOML file with `--config`."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field, fields, replace
from pathlib import Path
from typing import Any, Mapping

from .errors import ConfigError
from .events import Action


def _default_weights() -> dict[str, float]:
    return {
        "unusual_login_location": 0.8,
        "volume_spike": 0.9,
        "off_hours_activity": 0.4,
        "departing_exfil": 1.0,
    }


@dataclass(frozen=True)
class Config:
    db_path: str = "insiderwatch.db"
    internal_domains: tuple[str, ...] = ("acme.example",)
    default_timezone: str = "UTC"

    # baselines
    baseline_window_days: int = 30
    baseline_min_days: int = 14  # fewer observed days than this = cold start, no baseline

    # signals
    volume_spike_actions: tuple[Action, ...] = (Action.FILE_DOWNLOAD,)
    volume_z_threshold: float = 3.0
    volume_z_cap: float = 6.0
    min_std_fraction: float = 0.1  # std floor as a fraction of the mean, avoids z blow-ups
    business_hours: tuple[int, int] = (9, 17)

    # departing employees (signals/departing_exfil.py)
    departure_window_days: int = 14  # watch this many days before the last day
    departure_notice_days: int = 14  # assumed notice period when only a resignation date is known
    departing_exfil_actions: tuple[Action, ...] = (
        Action.FILE_DOWNLOAD,
        Action.FILE_SHARE_EXTERNAL,
        Action.EMAIL_FORWARD_EXTERNAL,
        Action.MESSAGE_EXPORT,
    )

    # alert cases (alerts/cases.py)
    case_window_hours: int = 48  # an alert joins the user's open case if within this gap of its last alert

    # scoring: risk = weight * strength, then decayed by age
    signal_weights: Mapping[str, float] = field(default_factory=_default_weights)
    default_signal_weight: float = 0.2
    alert_threshold: float = 0.15
    score_half_life_days: float = 14.0
    severity_medium: float = 0.4
    severity_high: float = 0.7

    # delivery
    notifier: str = "console"
    slack_webhook_url: str = "https://hooks.slack.example/T000/B000/insiderwatch"

    # feature flags (see CONTRIBUTING.md)
    feature_flags: Mapping[str, bool] = field(default_factory=lambda: {"legacy_dlp_rules": False})

    def flag(self, name: str) -> bool:
        return bool(self.feature_flags.get(name, False))

    def weight_for(self, signal_name: str) -> float | None:
        return self.signal_weights.get(signal_name)


def load_config(path: str | Path | None = None) -> Config:
    """Defaults, optionally overridden by a TOML file. Unknown keys are an error."""
    cfg = Config()
    if path is None:
        return cfg
    try:
        raw: dict[str, Any] = tomllib.loads(Path(path).read_text())
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigError(f"cannot read config {path}: {exc}") from exc
    known = {f.name for f in fields(Config)}
    unknown = sorted(set(raw) - known)
    if unknown:
        raise ConfigError(f"unknown config keys: {', '.join(unknown)}")
    if "signal_weights" in raw:
        raw["signal_weights"] = {**cfg.signal_weights, **raw["signal_weights"]}
    for key in ("volume_spike_actions", "departing_exfil_actions"):
        if key in raw:
            raw[key] = tuple(Action(a) for a in raw[key])
    for key in ("internal_domains", "business_hours"):
        if key in raw:
            raw[key] = tuple(raw[key])
    return replace(cfg, **raw)
