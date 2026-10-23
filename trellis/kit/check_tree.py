"""校验 interview-loop.yaml（受限 YAML，不依赖 PyYAML）。

  trellis kit check_tree --co millennium            # 缺失路径 = warning，退出 0
  trellis kit check_tree --co millennium --strict   # 缺失路径 = error，退出 1
  trellis kit check_tree --co millennium --catalog  # 另检查 loop/CATALOG.md 是否含全部 problem ID
  trellis kit check_tree --co millennium --tree-md  # 另检查 loop/tree/TREE.md 是否含全部 round/skill/problem ID

树文件 interview-loop.yaml 在研究目录：research/companies/<co>/tree/（或老布局 loop/tree/），--tree 可指定。
题目与题集在 kit（vault）里：loop/rounds/<round>/<id>_*、problems/qNN_*、bank.json。

检查项：
  1. 每个 `problems: [..]` 里的 ID 能唯一解析到 loop/rounds/<round>/<id>_* 目录，
     非编码轮 ID 解析到 loop/rounds/<round>/bank.json（ID → 轮次目录的对照表是公司档案的一部分，见 profiles）；
     qNN 解析到 problems/qNN_*（stripe 不是这个布局，关掉）
  2. 每个 `study: [..]` / `cards: [..]` 路径存在（相对 kit 根，stripe 相对 kit/loop）
  3. round `id` 对应 loop/rounds/<id>/ 目录存在
  4. 同一 round 内 skill id 不重复；problem ID 至少被一个 skill 引用一次（信息性）
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from .paths import REPO, Kit

_LIST = re.compile(r"^\s*(problems|study|cards|core):\s*\[(.*)\]\s*$")
# round-level `core: [leaf, ...]` names the code-core leaves a round exercises
CORE_SKELETON = REPO / "skeleton" / "code-core.yaml"
_ID = re.compile(r"^(\s*)-\s*id:\s*(\S+)\s*$")


def parse(text: str):
    """返回 (rounds, prereq_paths)。rounds = [{id, skills:[{id, problems}], study}]"""
    rounds, prereq, cur_round, cur_skill = [], [], None, None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = _ID.match(line)
        if m:
            indent, ident = len(m.group(1)), m.group(2)
            if indent == 2:
                cur_round = {"id": ident, "skills": [], "study": []}
                rounds.append(cur_round)
                cur_skill = None
            elif indent == 6 and cur_round is not None:
                cur_skill = {"id": ident, "problems": []}
                cur_round["skills"].append(cur_skill)
            continue
        m = _LIST.match(line)
        if m:
            key, items = m.group(1), [s.strip() for s in m.group(2).split(",") if s.strip()]
            if key == "problems" and cur_skill is not None:
                cur_skill["problems"].extend(items)
            elif key == "core" and cur_round is not None:
                cur_round.setdefault("core", []).extend(items)
            elif key in ("study", "cards"):
                (cur_round["study"] if cur_round is not None else prereq).extend(items)
    return rounds, prereq


TREE_YAML = "interview-loop.yaml"


def tree_yaml(kit: Kit, explicit: Path | None = None) -> Path:
    """The tree file: --tree, else research/tree/, research/loop/tree/, kit/loop/tree/ (first that exists)."""
    if explicit:
        return explicit
    for base in (kit.research / "tree", kit.research / "loop" / "tree", kit.kit / "loop" / "tree"):
        if (base / TREE_YAML).exists():
            return base / TREE_YAML
    raise SystemExit(f"error: no {TREE_YAML} under {kit.research}/tree, {kit.research}/loop/tree or {kit.kit}/loop/tree")


def study_base(kit: Kit) -> Path:
    return kit.kit if kit.profile.study_base == "kit" else kit.kit / "loop"


def resolve(kit: Kit, pid: str) -> Path | None:
    """The directory (or bank.json) a problem id points to, or None."""
    rounds = kit.kit / "loop" / "rounds"
    noncode = kit.profile.noncode
    if pid in noncode:
        p = rounds / noncode[pid] / "bank.json"
        return p if p.exists() else None
    if kit.profile.oa_in_problems and re.match(r"^q\d+$", pid):
        hits = list((kit.kit / "problems").glob(f"{pid}_*"))
        return hits[0] if len(hits) == 1 else None
    hits = list(rounds.glob(f"*/{pid}_*"))
    return hits[0] if len(hits) == 1 else None


def _find(candidates: list[Path]) -> Path | None:
    return next((p for p in candidates if p.exists()), None)


def add_arguments(ap: argparse.ArgumentParser, common: argparse.ArgumentParser) -> None:
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--catalog", action="store_true")
    ap.add_argument("--tree-md", action="store_true")
    ap.add_argument("--tree", type=Path, default=None, help=f"the {TREE_YAML} to check (default: found under --research)")


def run(a, kit: Kit) -> int:
    loop = kit.kit / "loop"
    rounds_dir = loop / "rounds"
    base = study_base(kit)
    rounds, prereq = parse(tree_yaml(kit, a.tree).read_text(encoding="utf-8"))
    errors, warnings = [], []
    all_pids: set[str] = set()

    for r in rounds:
        if not (rounds_dir / r["id"]).is_dir():
            warnings.append(f"round dir missing: rounds/{r['id']}")
        seen = set()
        for s in r["skills"]:
            if s["id"] in seen:
                errors.append(f"duplicate skill id in {r['id']}: {s['id']}")
            seen.add(s["id"])
            for pid in s["problems"]:
                all_pids.add(pid)
                if resolve(kit, pid) is None:
                    warnings.append(f"problem not resolvable: {pid} (skill {r['id']}/{s['id']})")
        for path in r["study"]:
            if not (base / path).exists():
                warnings.append(f"study path missing: {path} (round {r['id']})")
    core_ids = set(re.findall(r"-\s*id:\s*(\S+)", CORE_SKELETON.read_text(encoding="utf-8"))) if CORE_SKELETON.exists() else set()
    for r in rounds:
        for leaf in r.get("core", []):
            if leaf not in core_ids:
                errors.append(f"core leaf not in skeleton/code-core.yaml: {leaf} (round {r['id']})")
    for path in prereq:
        if not (base / path).exists():
            warnings.append(f"prereq path missing: {path}")

    if a.catalog:
        cat = _find([loop / "CATALOG.md", kit.research / "loop" / "CATALOG.md"])
        if cat is None:
            errors.append("CATALOG.md missing")
        else:
            text = cat.read_text(encoding="utf-8")
            for pid in sorted(all_pids):
                if not re.search(rf"\|\s*{re.escape(pid)}\s*\|", text):
                    errors.append(f"CATALOG.md lacks row for {pid}")
    if a.tree_md:
        md = _find([loop / "tree" / "TREE.md", kit.research / "tree" / "TREE.md", kit.research / "loop" / "tree" / "TREE.md"])
        if md is None:
            errors.append("TREE.md missing")
        else:
            text = md.read_text(encoding="utf-8")
            for r in rounds:
                if r["id"] not in text:
                    errors.append(f"TREE.md lacks round {r['id']}")
                for s in r["skills"]:
                    if s["id"] not in text:
                        errors.append(f"TREE.md lacks skill {s['id']}")
            for pid in sorted(all_pids):
                if pid not in text:
                    errors.append(f"TREE.md lacks problem {pid}")

    if a.strict:
        errors, warnings = errors + warnings, []
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(
        f"rounds={len(rounds)} skills={sum(len(r['skills']) for r in rounds)} problems={len(all_pids)} "
        f"errors={len(errors)} warnings={len(warnings)}"
    )
    return 1 if errors else 0
