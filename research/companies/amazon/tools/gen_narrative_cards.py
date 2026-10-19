"""Generate the Narrative Round `amazon` branch, studied in phases (Chi, 2026-10-19):

    01 完整故事 → 02 提纲（STAR-L） → 03 追问（含 senior） → 04 LP → 故事 → 05 技术深挖

    python3 research/companies/amazon/tools/gen_narrative_cards.py

Inputs: the LP outlines (vault/interviews/companies/amazon/lp/{stories/*.md, genai/stories.md, story_matrix.md}) and the
story material in research/companies/amazon/narrative/{<code>.json, lp_terms.json, tech.json}. Every card ends with a
footer of business-English expressions (proposals/narrative/AMAZON_STORY_AGENT.md). Writes
vault/interviews/rounds/narrative/cards/amazon/*.md (overwritten every run) and the `amazon` branch of
skeleton/narrative.yaml (replaced every run). Card ids of earlier runs are kept so review history follows the card.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
LP = ROOT / "vault/interviews/companies/amazon/lp"
MAT = ROOT / "research/companies/amazon/narrative"
OUT = ROOT / "vault/interviews/rounds/narrative/cards/amazon"
SKEL = ROOT / "skeleton/narrative.yaml"
# story names live in one place: name_stories.py
NAMES = dict(re.findall(r'"(S1[01]|S[1-9]|M1|R[1-3]|G[1-4])": "([^"]+)"', (HERE / "name_stories.py").read_text(encoding="utf-8")))
ORDER = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "M1", "R1", "R2", "R3",
         "G1", "G2", "G3", "G4"]
PHASES = [("amazon.full", "01 完整故事（先过一遍）"), ("amazon.outline", "02 提纲（STAR-L）"),
          ("amazon.followups", "03 追问（含 senior 追问）"), ("amazon.lp-map", "04 LP → 故事"),
          ("amazon.tech", "05 技术深挖：Snowflake、数据管线与 AWS")]


def sections(text: str) -> dict[str, str]:
    parts = re.split(r"^## (.+?)\s*$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}


def nest(md: str) -> str:
    """Python-Markdown nests a list only at a 4-space indent; the outlines use 2."""
    return re.sub(r"^((?:  )+)(?=[-*] |\d+\. )", lambda m: "    " * (len(m.group(1)) // 2), md, flags=re.M)


def label(name: str) -> str:
    return f'<span class="label">{name}</span>'


def footer(terms: list[dict]) -> str:
    if not terms:
        return ""
    rows = "".join(f"<br>• <b><i>{html.escape(t['en'])}</i></b> — {html.escape(t['zh'])}"
                   f"<br>&nbsp;&nbsp;&nbsp;<span style=\"opacity:.85\">“{html.escape(t['example'])}”</span>"
                   for t in terms)
    return f'\n\n<div class="sources"><b>表达 · business English</b>{rows}</div>\n'


def front(title: str, meta: str, question: str) -> str:
    return f'<p class="title">{html.escape(title)}<span class="meta">{html.escape(meta)}</span></p>\n\n{question}'


def labelled(md: str) -> str:
    """Lines starting with `名字｜` become label chips (tech.json convention)."""
    return re.sub(r"^(\S{1,8})｜", lambda m: label(m.group(1)) + " ", md, flags=re.M)


cards: dict[str, tuple[str, int, str, str]] = {}   # id -> (node, step, Q, A)
step = {leaf: 0 for leaf, _ in PHASES}


def add(cid: str, leaf: str, q: str, a: str) -> None:
    step[leaf] += 1
    cards[cid] = (leaf, step[leaf], q, a.strip())


# --- load outlines and material
story_text: dict[str, str] = {}
for p in (LP / "stories").glob("*.md"):
    story_text[p.stem.split("_")[0]] = p.read_text(encoding="utf-8")
g = (LP / "genai/stories.md").read_text(encoding="utf-8")
genai = [m for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", g, re.S | re.M) if "S · Situation" in m.group(2)]
for n, m in enumerate(genai, start=1):
    story_text[f"G{n}"] = m.group(2)
mat = {c: json.loads((MAT / f"{c}.json").read_text(encoding="utf-8")) for c in ORDER if (MAT / f"{c}.json").exists()}


def terms(code: str, kind: str) -> list[dict]:
    return mat.get(code, {}).get("terms", {}).get(kind, [])


# --- 01 完整故事
for code in ORDER:
    if code not in mat:
        continue
    m = mat[code]
    body = (f"{label('前因后果')}\n\n" + "\n".join(f"- {b}" for b in m["full_zh"]) +
            f"\n\n{label('英文口述（60–90 秒）')}\n\n{m['full_en']}" + footer(terms(code, "full")))
    add(f"nr-amz-{code.lower()}-full", "amazon.full",
        front(NAMES[code], "01 完整故事", "先在心里把前因后果过一遍，再用英文完整讲一遍。"), body)

# --- 02 提纲
for code in ORDER:
    name, text, low = NAMES[code], story_text.get(code, ""), code.lower()
    if code.startswith("G"):
        main_part = re.split(r"\n- 可选", text.partition("\n- 追问：")[0])[0]
        add(f"nr-amz-{low}-starl", "amazon.outline", front(name, "02 提纲", "适用 LP、开场 hook 和 STAR-L 提纲"),
            nest(main_part) + footer(terms(code, "starl")))
        continue
    sec = sections(text)
    head = re.search(r"^\*\*(.+?)\*\*\s*$", text, re.M)
    add(f"nr-amz-{low}-hook", "amazon.outline", front(name, "02 提纲", "开场第一句是什么？适用哪些 LP？要报哪些数字？"),
        (f"{label('开场')}\n\n**{head.group(1)}**\n\n" if head else "") +
        f"{label('适用 LP')}\n\n{nest(sec.get('适用 LP', ''))}\n\n{label('数字')}\n\n{nest(sec.get('数字', ''))}" +
        footer(terms(code, "hook")))
    star = re.sub(r"^### ([STARL])\s*$", lambda mm: label(mm.group(1)) + "\n", sec.get("S / T / A / R / L", ""),
                  flags=re.M)
    add(f"nr-amz-{low}-starl", "amazon.outline", front(name, "02 提纲", "STAR-L 提纲（60–90 秒）"),
        nest(star) + footer(terms(code, "starl")))
    if sec.get("换个 LP 讲"):
        add(f"nr-amz-{low}-relp", "amazon.outline", front(name, "02 提纲", "换成别的 LP 问时，强调哪一段？"),
            nest(sec["换个 LP 讲"]) + footer(terms(code, "relp")))

# --- 03 追问
for code in ORDER:
    name, text, low = NAMES[code], story_text.get(code, ""), code.lower()
    follow = (re.sub(r"^  ", "", text.partition("\n- 追问：")[2], flags=re.M) if code.startswith("G")
              else sections(text).get("追问与回答", ""))
    if follow.strip():
        add(f"nr-amz-{low}-followups", "amazon.followups", front(name, "03 追问", "面试官会追问什么？每个怎么答？"),
            nest(follow) + footer(terms(code, "followups")))
    for i, s in enumerate(mat.get(code, {}).get("senior", []), start=1):
        body = (f"{label('面试官在探')} {s['why']}\n\n{label('回答框架')}\n\n" + "\n".join(f"- {b}" for b in s["framework"])
                + f"\n\n{label('为什么这是最佳实践')}\n\n{s['best_practice']}" + footer(s.get("terms", [])))
        add(f"nr-amz-{low}-senior-{i}", "amazon.followups", front(name, "03 senior 追问", f"*\"{s['q']}\"*"), body)

# --- 04 LP → 故事
lp_terms = json.loads((MAT / "lp_terms.json").read_text(encoding="utf-8")) if (MAT / "lp_terms.json").exists() else {}
table = sections((LP / "story_matrix.md").read_text(encoding="utf-8")).get("每条 LP：先用哪个故事 / 备选", "")
for num, lp, first, alt in re.findall(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", table, re.M):
    add(f"nr-amz-lp{int(num):02d}", "amazon.lp-map", front(lp, "04 LP → 故事", "先用哪个故事？备选是什么？"),
        f"{label('先用')} **{first}**\n\n{label('备选')} {alt}\n\n"
        f"{label('讲法')} 先用一句话说这个 LP 在这件事里指什么，再进 S/T/A/R/L。" + footer(lp_terms.get(lp, [])))

# --- 05 技术深挖
if (MAT / "tech.json").exists():
    for t in json.loads((MAT / "tech.json").read_text(encoding="utf-8")):
        add(f"nr-amz-tech-{t['id']}", "amazon.tech", front("技术深挖", "05 Snowflake · 数据 · AWS", t["q"]),
            labelled(t["a"]) + footer(t.get("terms", [])))

# --- write
OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob("nr-amz-*.md"):
    old.unlink()
for cid, (node, st, q, a) in cards.items():
    (OUT / f"{cid}.md").write_text(f"---\nid: {cid}\nnode: {node}\ntype: qa\nstep: {st}\n---\n## Q\n{q}\n\n## A\n{a}\n",
                                   encoding="utf-8")

branch = ["  - id: amazon", "    order: 7", '    title: "Amazon · LP 故事（STAR-L）"',
          '    summary: "你自己的故事：先完整过一遍，再背提纲，再练追问，最后记 LP 映射；附技术深挖。"', "    children:"]
for leaf, title in PHASES:
    branch += [f"      - id: {leaf}", f'        title: "{title}"', f'        summary: "{title}"']
text = SKEL.read_text(encoding="utf-8")
text = re.sub(r"\n  - id: amazon\n.*?(?=\n  - id: |\Z)", "", text, flags=re.S).rstrip("\n")
SKEL.write_text(text + "\n\n" + "\n".join(branch) + "\n", encoding="utf-8")
print(f"{len(cards)} cards:", {leaf: step[leaf] for leaf, _ in PHASES})
