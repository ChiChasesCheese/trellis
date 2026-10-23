"""Where a kit and its research area live, and the per-company defaults for the tool options."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field, replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KITS_REL = Path("vault") / "interviews" / "companies"
RESEARCH_REL = Path("research") / "companies"

# Layout of the problem sets, for summary: tried in this order, the ones that exist are scanned.
SUMMARY_DIRS = ("problems", "loop/rounds/03_phone_coding", "loop/rounds/04_ood")

# Coverage buckets: id prefix -> label, in print order. A kit overrides the labels it renames.
COVERAGE_LABELS = {"q": "OA", "pc": "电面 coding", "od": "OOD", "sd": "系统设计"}


@dataclass(frozen=True)
class Profile:
    """Defaults for the options where companies differ. Every field has a command-line override."""

    # pareto / contents: round names that get weight 1.0 (pareto --focus is the comma-joined string)
    focus: tuple[str, ...] = ("OA", "电面", "phone")
    contents_focus: tuple[str, ...] = ("OA", "电面", "PS", "技术筛")
    table: str = "总表"
    title_col: str | None = None
    # contents: practice-codebase kit (titles from RANK.md, walkthrough links, codebase footer)
    codebase: bool = False
    # coverage
    coverage_labels: dict = field(default_factory=lambda: dict(COVERAGE_LABELS))
    # summary
    summary_dirs: tuple[str, ...] = SUMMARY_DIRS
    # articles_readme: pin every article to one round dir ("" = look the dir up under loop/rounds)
    articles_round_dir: str = ""
    articles_round_label: str = "R1 coding"
    # check_tree
    noncode: dict = field(default_factory=dict)
    study_base: str = "kit"  # "kit": study/ paths are relative to the kit root; "loop": to kit/loop
    oa_in_problems: bool = True  # qNN ids live in kit/problems/ rather than loop/rounds/
    # verify_suites: pass -o addopts= to pytest (kits whose pytest.ini addopts would hide the summary line)
    clear_addopts: bool = False


_SNOWFLAKE_NONCODE = {"ai": "00_ai_screen", "rc": "01_recruiter", "exp": "06_project_deep_dive",
                      "hm": "07_hm_behavioral", "tm": "08_team_matching"}

PROFILES: dict[str, Profile] = {
    "stripe": Profile(
        summary_dirs=("problems",),
        noncode={"rc": "01_recruiter", "hm": "02_hm", "bq": "08_behavioral"},
        study_base="loop",
        oa_in_problems=False,
    ),
    "snowflake": Profile(
        focus=("OA", "电面", "PS", "技术筛"),
        title_col="题",
        noncode=_SNOWFLAKE_NONCODE,
    ),
    "millennium": Profile(
        focus=("第一轮",),
        coverage_labels={"q": "OA", "pc": "第一轮 coding", "od": "OOD", "sd": "系统设计"},
        articles_round_dir="01_first_round",
        articles_round_label="R1 coding",
        noncode={"rc": "00_recruiter", "py": "02_python_internals", "exp": "03_project_deep_dive",
                 "hm": "05_hm_behavioral"},
    ),
    "abnormal": Profile(
        focus=("AI screen",),
        contents_focus=("AI screen",),
        codebase=True,
        coverage_labels={"cb": "AI screen 代码库", "cr": "Code review", "ic": "Incident", "sd": "系统设计",
                         "pc": "旧流程 coding", "q": "OA", "od": "OOD"},
        noncode={"hm": "04_manager_deep_dive", "team": "05_team_values"},
        clear_addopts=True,
    ),
    "headlands": Profile(focus=("电面",), noncode=_SNOWFLAKE_NONCODE),
    "amazon": Profile(),
}


@dataclass(frozen=True)
class Kit:
    """A kit directory, its research directory, and the profile of defaults."""

    kit: Path
    research: Path
    profile: Profile = field(default_factory=Profile)
    co: str = ""

    @property
    def project(self) -> Path:
        """The uv project that runs the kit's pytest suites (this repository)."""
        return REPO

    def with_profile(self, **changes) -> "Kit":
        return replace(self, profile=replace(self.profile, **changes))


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    """--co / --kit / --research. SUPPRESS keeps a value given before the tool name from being overwritten."""
    parser.add_argument("--co", default=argparse.SUPPRESS,
                        help="company name: --kit defaults to vault/interviews/companies/<co>, "
                             "--research to research/companies/<co>")
    parser.add_argument("--kit", type=Path, default=argparse.SUPPRESS,
                        help="the kit directory in the vault (learning area)")
    parser.add_argument("--research", type=Path, default=argparse.SUPPRESS,
                        help="the research directory (catalog/, reports/, the interview tree)")


def resolve_kit(co: str | None = None, kit: Path | str | None = None, research: Path | str | None = None,
                root: Path | None = None) -> Kit:
    """`--co stripe` -> the two default directories; `--kit` / `--research` override either one."""
    base = root if root is not None and (root / KITS_REL).is_dir() else REPO
    if co is None and kit is None and research is None:
        raise SystemExit("error: give --co <company> (or --kit and --research)")
    name = co or (Path(kit).resolve().name if kit else Path(research).resolve().name)
    kit_dir = Path(kit) if kit else base / KITS_REL / name
    research_dir = Path(research) if research else base / RESEARCH_REL / name
    if not kit_dir.is_dir():
        raise SystemExit(f"error: kit directory not found: {kit_dir}")
    return Kit(kit=kit_dir.resolve(), research=research_dir.resolve(), profile=PROFILES.get(name, Profile()), co=name)


def kit_from_args(args: argparse.Namespace) -> Kit:
    return resolve_kit(getattr(args, "co", None), getattr(args, "kit", None), getattr(args, "research", None),
                       getattr(args, "root", None))
