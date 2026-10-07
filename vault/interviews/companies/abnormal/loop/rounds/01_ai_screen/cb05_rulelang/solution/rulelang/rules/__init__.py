"""The customer rule language: ``sender.domain_age_days < 7 and any(link.host in intel.bad_hosts)``."""
from rulelang.rules.compiler import CompiledRule, compile_rule
from rulelang.rules.parser import RuleSyntaxError

__all__ = ["CompiledRule", "RuleSyntaxError", "compile_rule"]
