"""`trellis kit <tool> --co <name> [...]`: the shared interview-kit authoring tools.

Every tool takes `--co` (a company name), `--kit` (the vault kit directory) and `--research` (the research
directory); `--co stripe` means vault/interviews/companies/stripe + research/companies/stripe. The options may
come before or after the tool's own arguments.
"""

from __future__ import annotations

import argparse
import importlib

from .paths import add_common_arguments, kit_from_args

TOOLS = {
    "pareto": "rank a markdown table by rounds x refs x recency and print the cut line",
    "summary": "table of every problem set: tests by marker, measured perf, status",
    "contents": "write the kit's CONTENTS.md from the interview tree and the ranking",
    "coverage": "how much of the reported-question sightings the built problems cover",
    "verify_suites": "accept problem sets: reference green, empty starter red (codebase sets too)",
    "harvest": "Reddit / Hacker News / Xiaohongshu interview-report harvester",
    "mirror": "list, search and scaffold problems from the 1point3acres mirror",
    "refresh_check": "maintain and re-verify the source registry (catalog/sources.json)",
    "build_report_html": "assemble the Stripe OA HTML report",
    "articles_readme": "regenerate study/30-articles/README.md",
    "check_tree": "validate the interview tree (interview-loop.yaml) against the kit",
    "progress": "the practice progress board (progress.jsonl)",
}


def _module(name: str):
    return importlib.import_module(f"{__package__}.{name}")


def add_parser(subparsers, parents=()) -> argparse.ArgumentParser:
    """Register the `kit` group on a parent argparse subparsers object."""
    p_kit = subparsers.add_parser(
        "kit", parents=list(parents),
        help="shared interview-kit tools: trellis kit <tool> --co <name> (pareto, summary, contents, coverage, "
             "verify_suites, harvest, mirror, refresh_check, ...)",
    )
    common = argparse.ArgumentParser(add_help=False)
    add_common_arguments(common)
    tools = p_kit.add_subparsers(dest="tool", required=True, metavar="TOOL")
    for name, summary in TOOLS.items():
        mod = _module(name)
        sp = tools.add_parser(name, aliases=[name.replace("_", "-")] if "_" in name else [], parents=[common],
                              help=summary, description=mod.__doc__,
                              formatter_class=argparse.RawDescriptionHelpFormatter)
        mod.add_arguments(sp, common)
        sp.set_defaults(tool_name=name)
    return p_kit


def run(args) -> int:
    kit = kit_from_args(args)
    return _module(args.tool_name).run(args, kit) or 0
