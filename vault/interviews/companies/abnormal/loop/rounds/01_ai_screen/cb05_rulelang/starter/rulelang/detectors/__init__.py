from rulelang.detectors.base import (
    DETECTORS,
    Detector,
    DetectorContext,
    detector_names,
    register_detector,
)

# Importing a module registers its detector.
from rulelang.detectors import (  # noqa: E402,F401  isort: skip
    impossible_travel,
    mailbox_forwarding_rule,
    mass_mailing,
    new_sender,
    suspicious_link,
    vendor_lookalike,
)
from rulelang.detectors.runner import DetectorRunner  # noqa: E402

__all__ = [
    "DETECTORS",
    "Detector",
    "DetectorContext",
    "DetectorRunner",
    "detector_names",
    "register_detector",
]
