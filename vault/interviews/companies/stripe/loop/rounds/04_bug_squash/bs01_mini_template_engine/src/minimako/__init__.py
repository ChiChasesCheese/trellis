"""minimako — a tiny Mako-style template engine (interview bug-squash fixture).

Public surface: `Template`, `TemplateLookup`.
"""

from .template import Template
from .lookup import TemplateLookup

__all__ = ["Template", "TemplateLookup"]
