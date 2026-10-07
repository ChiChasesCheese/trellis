"""Importing this package registers the built-in analyzers."""
from quarantine.analyzers import (  # noqa: F401
    attachment_type,
    display_name_spoof,
    link_reputation,
    sender_reputation,
)
from quarantine.analyzers.base import ANALYZERS, AnalysisContext, Analyzer, register_analyzer
from quarantine.analyzers.runner import AnalyzerRunner

__all__ = ["ANALYZERS", "AnalysisContext", "Analyzer", "AnalyzerRunner", "register_analyzer"]
