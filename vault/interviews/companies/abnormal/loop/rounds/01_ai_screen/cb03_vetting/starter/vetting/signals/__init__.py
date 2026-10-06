"""Signals. Importing this package registers every signal."""
from vetting.signals import (  # noqa: F401  (import registers the @register_signal classes)
    disposable_email,
    ip_geo_mismatch,
    resume_name_mismatch,
    voip_phone,
    vpn_hosting_ip,
)
from vetting.signals.base import SIGNALS, Signal, SignalContext, all_signals, register_signal

__all__ = ["SIGNALS", "Signal", "SignalContext", "all_signals", "register_signal"]
