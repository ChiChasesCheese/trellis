"""Project: one domain's skeleton and everything hanging off it, loaded.

The CLI used to be the only thing that knew how to open a domain. Digest,
triage and sync all need the same view, so it lives here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .cards import Card, load_cards
from .cases import CASES_DIRNAME, load_cases
from .clippings import CLIPPINGS_DIRNAME, Clipping, load_clippings
from .drills import Drill, load_drills
from .readings import Reading, load_readings
from .skeleton import Skeleton, load_skeleton
from .validate import validate

# Provenance a reading written from a corpus carries beside `nodes`.
CORPUS_KEYS = frozenset({"corpus", "section"})


@dataclass
class Project:
    skeleton: Skeleton
    cards: list[Card] = field(default_factory=list)
    card_errors: list[str] = field(default_factory=list)
    readings: list[Reading] = field(default_factory=list)
    reading_errors: list[str] = field(default_factory=list)
    drills: list[Drill] = field(default_factory=list)
    drill_errors: list[str] = field(default_factory=list)
    cases: list[Reading] = field(default_factory=list)
    case_errors: list[str] = field(default_factory=list)
    clippings: dict[str, Clipping] = field(default_factory=dict)

    def report(self):
        return validate(self.skeleton, self.cards, self.card_errors,
                        self.readings, self.reading_errors,
                        self.drills, self.drill_errors, self.clippings,
                        self.cases, self.case_errors)

    def content_dir(self, root: Path) -> Path:
        """This domain's folder inside the Obsidian vault. Not the vault
        itself — `vault/` is one Obsidian vault holding every domain."""
        return content_dir(root, self.skeleton)


def content_dir(root: Path, skeleton: Skeleton) -> Path:
    """Where a domain's cards, readings, drills, cases and map notes live:
    `vault/<folder>`, the folder its skeleton declares (the slug by default)."""
    return Path(root) / "vault" / skeleton.folder


def domains(root: Path) -> list[str]:
    return [f.stem for f in sorted((Path(root) / "skeleton").glob("*.yaml"))]


def load_project(root: Path, domain: str) -> Project:
    """Raises SkeletonError for a malformed skeleton; content errors are
    collected on the project for validate to report."""
    root = Path(root)
    project = Project(skeleton=load_skeleton(root / "skeleton" / f"{domain}.yaml"))
    vault = project.content_dir(root)
    if (vault / "cards").exists():
        project.cards, project.card_errors = load_cards(vault / "cards")
    if (vault / "readings").exists():
        project.readings, project.reading_errors = load_readings(
            vault / "readings", CORPUS_KEYS)
    if (vault / "drills").exists():
        project.drills, project.drill_errors = load_drills(vault / "drills")
    if (vault / CASES_DIRNAME).exists():
        project.cases, project.case_errors = load_cases(vault / CASES_DIRNAME)
    if (vault / CLIPPINGS_DIRNAME).exists():
        project.clippings = load_clippings(vault / CLIPPINGS_DIRNAME)
    return project


def load_loop(root: Path, names: list[str] | None = None):
    """Every domain loaded, with its Traces read back onto it: the view the
    Brief, the Feed, grow and the Workbench all share. A domain with no
    cards is included deliberately — every one of its leaves is uncovered,
    which is exactly what "worth writing" exists to say. Returns
    (projects, assessments, traces, ages) keyed by domain."""
    from .hold import assess
    from .traces import load_traces, traces_path
    root = Path(root)
    names = names if names is not None else domains(root)
    projects, assessments, traces, ages = {}, {}, {}, {}
    for domain in names:
        project = load_project(root, domain)
        file = load_traces(traces_path(root, domain))
        traces[domain] = file.traces if file else {}
        projects[domain] = project
        assessments[domain] = assess(project.skeleton, project.cards, traces[domain])
        ages[domain] = file.age_days if file else None
    return projects, assessments, traces, ages


def all_skeletons(root: Path) -> dict[str, Skeleton]:
    return {d: load_skeleton(Path(root) / "skeleton" / f"{d}.yaml") for d in domains(root)}


def vault_note_names(root: Path) -> set[str]:
    """Every note name in the vault. Names must stay unique because card
    links resolve a note by name, not by path."""
    return {p.stem for p in (Path(root) / "vault").rglob("*.md")}
