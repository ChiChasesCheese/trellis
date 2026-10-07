"""Daily volume far above the user's own baseline (z-score on bytes)."""
from __future__ import annotations

from typing import Iterable, Sequence

from ..events import Event
from .base import Finding, Signal, SignalContext, signal


@signal("volume_spike")
class VolumeSpike(Signal):
    def evaluate(self, ctx: SignalContext, user: str, events: Sequence[Event]) -> Iterable[Finding]:
        cfg = ctx.config
        for action in cfg.volume_spike_actions:
            todays = [e for e in events if e.action is action]
            if not todays:
                continue
            baseline = ctx.baselines.get(user, action, ctx.day)
            if baseline is None:
                continue
            total = sum(e.bytes for e in todays)
            spread = max(baseline.std_bytes, baseline.mean_bytes * cfg.min_std_fraction, 1.0)
            z = (total - baseline.mean_bytes) / spread
            if z < cfg.volume_z_threshold:
                continue
            yield Finding(
                signal=self.name,
                user=user,
                ts=todays[-1].ts,
                strength=min(1.0, z / cfg.volume_z_cap),
                reasons=(f"{action.value} volume {total / 1e6:.0f} MB is {z:.1f} sigma above baseline "
                         f"({baseline.mean_bytes / 1e6:.0f} MB/day)",),
                evidence={"action": action.value, "bytes": total, "z": round(z, 2)},
            )
