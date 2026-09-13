"""Codebases: repositories studied as learning targets.

A codebase is declared, not discovered. The declaration says which paths hold
which kind of material, because the valuable parts of a repository are rarely
where a heuristic would look — the sharpest architecture decisions in the first
codebase we ingested live in a lint config. Declaring them is the due diligence.

    # codebases/quant-stroller.yaml
    repo: ChiChasesCheese/Quant-Stroller
    ref: main
    harvest:
      - path: .importlinter        kind: contracts
      - path: docs/adr/*.md        kind: decisions
      - path: docs/concepts/*.md   kind: subject
        lens: quant-infra
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# What a declared path holds, and therefore what triage may propose from it.
KINDS = {
    "contracts": "architecture rules with a stated rationale -> Case",
    "decisions": "decision records (ADRs) -> Case",
    "subject": "subject matter -> reading + clipping in its own domain",
    "glossary": "the codebase's own vocabulary -> compared, never imported",
}
CACHE_DIRNAME = ".trellis/codebases"


class CodebaseError(ValueError):
    """Raised for a malformed codebase declaration."""


@dataclass
class Harvest:
    path: str
    kind: str
    lens: str = ""


@dataclass
class Codebase:
    name: str
    repo: str
    ref: str = "main"
    harvest: list[Harvest] = field(default_factory=list)

    def cache(self, root: Path) -> Path:
        return Path(root) / CACHE_DIRNAME / self.name


@dataclass
class Artefact:
    """One file inside a codebase, with what it is meant to hold."""

    id: str          # kind:stem, stable across refs — the triage handle
    kind: str
    lens: str
    path: Path       # absolute, inside the cache
    rel: str         # repo-relative
    excerpt: str = ""  # a few lines of the content, so triage sees more than a name


def load_codebase(path: str | Path) -> Codebase:
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CodebaseError(f"{path}: top level must be a mapping")
    repo = data.get("repo")
    if not isinstance(repo, str) or repo.count("/") != 1:
        raise CodebaseError(f"{path}: 'repo' must look like owner/name")
    harvest: list[Harvest] = []
    errors: list[str] = []
    for i, raw in enumerate(data.get("harvest") or []):
        if not isinstance(raw, dict):
            errors.append(f"harvest[{i}] must be a mapping")
            continue
        kind = raw.get("kind")
        if kind not in KINDS:
            errors.append(f"harvest[{i}]: kind must be one of {sorted(KINDS)}")
            continue
        if not raw.get("path"):
            errors.append(f"harvest[{i}]: missing path")
            continue
        harvest.append(Harvest(path=str(raw["path"]), kind=kind,
                               lens=str(raw.get("lens", "") or "")))
    if not harvest:
        errors.append("declare at least one harvest path")
    if errors:
        raise CodebaseError(f"{path}:\n  " + "\n  ".join(errors))
    return Codebase(name=path.stem, repo=repo, ref=str(data.get("ref", "main")),
                    harvest=harvest)


def _git(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise CodebaseError((result.stderr or result.stdout).strip())
    return result.stdout.strip()


def fetch(codebase: Codebase, root: Path) -> str:
    """Shallow-clone or update the cache. Returns the resolved commit SHA,
    which is the provenance every artefact taken from it will carry."""
    cache = codebase.cache(root)
    if (cache / ".git").exists():
        _git("git", "-C", str(cache), "fetch", "--depth", "1", "origin", codebase.ref)
        _git("git", "-C", str(cache), "checkout", "--quiet", "FETCH_HEAD")
    else:
        cache.parent.mkdir(parents=True, exist_ok=True)
        _git("gh", "repo", "clone", codebase.repo, str(cache), "--",
             "--depth", "1", "--branch", codebase.ref)
    return _git("git", "-C", str(cache), "rev-parse", "HEAD")


def artefacts(codebase: Codebase, root: Path) -> list[Artefact]:
    """Every file the declaration points at, in declaration order."""
    cache = codebase.cache(root)
    out: list[Artefact] = []
    seen: set[Path] = set()
    for harvest in codebase.harvest:
        matches = sorted(cache.glob(harvest.path)) if any(
            c in harvest.path for c in "*?[") else [cache / harvest.path]
        for match in matches:
            if not match.is_file() or match in seen:
                continue
            seen.add(match)
            out.append(Artefact(
                id=f"{harvest.kind}:{match.stem}",
                kind=harvest.kind,
                lens=harvest.lens,
                path=match,
                rel=str(match.relative_to(cache)),
                excerpt=excerpt_of(match),
            ))
    return out


def excerpt_of(path: Path, chars: int = 240) -> str:
    """The first lines of a text file, frontmatter dropped — enough for a
    triage prompt to place it without reading it whole."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if raw.startswith("---\n"):
        parts = raw.split("---\n", 2)
        raw = parts[2] if len(parts) == 3 else raw
    text = " ".join(raw.split())
    return text[:chars] + ("…" if len(text) > chars else "")
