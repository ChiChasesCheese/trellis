"""Applicant data sources. Importing this package registers every source."""
from vetting.sources import greenhouse, idp, workday  # noqa: F401  (import registers the @register_source classes)
from vetting.sources.base import SOURCES, Ingested, Source, register_source

__all__ = ["SOURCES", "Ingested", "Source", "register_source"]
