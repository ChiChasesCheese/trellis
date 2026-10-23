"""Shared interview-kit tools: the practice runtime and the authoring tools.

A company kit is two folders:

    vault/interviews/companies/<co>/     the kit (learning area): problems, loop/rounds, study, CONTENTS.md
    research/companies/<co>/             the research area: catalog/, reports/, sources, the interview tree

Practice runtime, imported by a kit's own runners (`drill.py`, `loop/mock.py`):

    progress          the cross-problem progress log and board (`progress.configure(ROOT)` first)
    pytest_progress   a pytest plugin, loaded with `-p trellis.kit.pytest_progress`

Authoring tools, run as `trellis kit <tool> --co <name>`; every one takes `--kit` and `--research`:

    pareto summary contents coverage verify_suites harvest mirror refresh_check
    build_report_html articles_readme check_tree progress

Forks between companies are options, not copies; `profiles.py` holds the per-company defaults.
"""
from .paths import Kit, Profile, PROFILES, REPO, resolve_kit

__all__ = ["Kit", "Profile", "PROFILES", "REPO", "resolve_kit"]
