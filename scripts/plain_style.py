"""Machine-checkable half of proposals/WRITING_RULES.md, shared by the content gates.

    uv run python scripts/plain_style.py <file.md | cards.json> [...]

`problems(text, source_heading)` returns the defects of one page: provenance words before the final source section,
third-person narration anywhere, and mermaid diagrams that will not fit Obsidian's reading column.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Words that belong only in the final source section.
PROVENANCE = ["一亩三分地", "1p3a", "1point3acres", "Hello Interview", "hellointerview", "面经", "帖子", "楼主",
              "置信度", "重建", "reconstructed", "推断", "报告里", "据报告", "有人报告", "被报告"]
# Narration about the text or its sources, never allowed. Regexes, so a compound word that merely contains the
# phrase (工作者, 版本文件, 基本题型) is not a false hit.
THIRD_PERSON = [r"本篇", r"(?<![版样根基资日脚剧成账])本文(?![件档本])", r"(?<![基课样])本题(?![型单库])", r"这道题",
                r"(?<![工著劳创])作者", r"我们认为", r"候选人说", r"据报道", r"笔者"]
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
MERMAID = re.compile(r"^```mermaid\n(.*?)^```", re.S | re.M)
NODE = re.compile(r"\b([A-Za-z_][\w]*)\s*(?:\[\[|\[\(|\(\(|\[|\(|\{\{|\{|>)(\"?)([^\]\)\}\n]*?)\2\s*(?:\]\]|\)\]|\)\)|\]|\)|\}\}|\})")
MAX_NODES, MAX_LABEL, MAX_PARTICIPANTS, MAX_CLASSES = 12, 16, 5, 8


def mermaid_problems(block: str) -> list[str]:
    head = block.lstrip().splitlines()[0].strip() if block.strip() else ""
    out: list[str] = []
    if re.match(r"(flowchart|graph)\s+(LR|RL)\b", head):
        out.append(f"mermaid `{head}`: use TB/TD so it fits the page")
    if head.startswith(("flowchart", "graph")):
        nodes = {}
        for m in NODE.finditer(block):
            if m.group(1) in ("subgraph", "end", "style", "classDef", "class", "click", "direction"):
                continue
            nodes[m.group(1)] = m.group(3)
        if len(nodes) > MAX_NODES:
            out.append(f"flowchart has {len(nodes)} nodes > {MAX_NODES}: split it")
        long = [lab for lab in nodes.values() if len(re.sub(r"<br\s*/?>", "", lab)) > MAX_LABEL]
        if long:
            out.append(f"flowchart labels longer than {MAX_LABEL} chars: {long[:3]}")
    if head.startswith("sequenceDiagram"):
        parts = set(re.findall(r"^\s*(?:participant|actor)\s+(\S+)", block, re.M))
        if len(parts) > MAX_PARTICIPANTS:
            out.append(f"sequenceDiagram has {len(parts)} participants > {MAX_PARTICIPANTS}")
    if head.startswith("classDiagram"):
        classes = set(re.findall(r"^\s*class\s+(\w+)", block, re.M))
        if len(classes) > MAX_CLASSES:
            out.append(f"classDiagram has {len(classes)} classes > {MAX_CLASSES}")
    return out


def problems(text: str, source_heading: str | None) -> list[str]:
    """Defects of one markdown page. `source_heading` is the final section where provenance may appear
    (None: provenance words are not allowed anywhere, e.g. on a card)."""
    out: list[str] = []
    body = text
    if source_heading:
        idx = text.find(f"\n## {source_heading}")
        if idx < 0:
            out.append(f"no final '## {source_heading}' section")
        else:
            body = text[:idx]
            if re.search(r"^## ", text[idx + 4:], re.M):
                out.append(f"'## {source_heading}' is not the last section")
    prose = FENCE.sub("", body)
    for w in PROVENANCE:
        if w.lower() in prose.lower():
            out.append(f"provenance word before the source section: {w}")
    all_prose = FENCE.sub("", text)
    for pattern in THIRD_PERSON:
        hit = re.search(pattern, all_prose)
        if hit:
            out.append(f"third-person narration: {hit.group(0)}")
    for block in MERMAID.findall(text):
        out += mermaid_problems(block)
    return out


def main(argv: list[str]) -> int:
    bad = 0
    for arg in argv:
        path = Path(arg)
        if path.suffix == ".json":
            for card in json.loads(path.read_text(encoding="utf-8")):
                found = problems(card.get("question_md", "") + "\n" + card.get("answer_md", ""), None)
                if found:
                    bad += 1
                    print(f"FAIL {path.name}:{card.get('id')}" + "".join(f"\n       - {p}" for p in found))
        else:
            text = path.read_text(encoding="utf-8")
            heading = next((h for h in ("来源与延伸阅读", "来源与延伸", "来源") if f"\n## {h}" in text), "来源")
            found = problems(text, heading)
            if found:
                bad += 1
                print(f"FAIL {path}" + "".join(f"\n       - {p}" for p in found))
    print(f"{'ok' if not bad else str(bad) + ' file(s)/card(s) fail'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
