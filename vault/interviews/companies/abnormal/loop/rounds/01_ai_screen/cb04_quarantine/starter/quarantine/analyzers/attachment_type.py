from __future__ import annotations

import re

from quarantine.analyzers.base import AnalysisContext, Analyzer, register_analyzer
from quarantine.models import Report, Verdict

_DOUBLE_EXTENSION = re.compile(r"\.[a-z0-9]{2,4}\.(exe|scr|js|vbs)$")
_ARCHIVES = (".zip", ".rar", ".7z")


@register_analyzer
class AttachmentType(Analyzer):
    """Executable or script attachments, double extensions, and archives we cannot look inside."""

    name = "attachment_type"

    def analyze(self, report: Report, ctx: AnalysisContext) -> Verdict:
        risky = ctx.tenant(report).attachments.risky_extensions
        score, reasons = 0, []
        for att in report.attachments:
            name = att.filename.lower()
            if _DOUBLE_EXTENSION.search(name):
                score = max(score, 95)
                reasons.append(f"{att.filename}: double extension")
            elif name.endswith(risky):
                score = max(score, 75)
                reasons.append(f"{att.filename}: risky file type")
            elif name.endswith(_ARCHIVES):
                score = max(score, 40)
                reasons.append(f"{att.filename}: archive, contents unknown")
        return Verdict(self.name, score, tuple(reasons))
