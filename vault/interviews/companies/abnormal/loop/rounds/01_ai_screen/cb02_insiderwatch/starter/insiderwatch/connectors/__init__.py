"""Connector package. Importing a module here is what registers it; replay only runs registered sources."""
from .base import Connector, RawRecord, register_connector, registered_connectors
from . import m365_audit, okta, slack_audit  # noqa: F401  (registration side effects)

__all__ = ["Connector", "RawRecord", "register_connector", "registered_connectors"]
