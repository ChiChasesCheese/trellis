"""Signal package. Importing a module here is what registers it."""
from .base import Finding, Signal, SignalContext, all_signals, signal, signal_names
from . import departing_exfil, off_hours_activity, unusual_login_location, volume_spike  # noqa: F401

__all__ = ["Finding", "Signal", "SignalContext", "all_signals", "signal", "signal_names"]
