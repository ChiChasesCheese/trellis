import logging

from filevault.logging_setup import configure_logging


def test_configure_is_idempotent():
    configure_logging("info")
    configure_logging("debug")
    root = logging.getLogger("filevault")
    assert len([h for h in root.handlers if getattr(h, "_filevault", False)]) == 1
    assert root.level == logging.DEBUG
    configure_logging("warning")


def test_unknown_level_falls_back_to_warning():
    configure_logging("loudest")
    assert logging.getLogger("filevault").level == logging.WARNING
