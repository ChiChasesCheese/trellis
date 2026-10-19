"""Generate the Narrative Round `amazon` branch: one leaf per story (S/R/M/G) plus an LP map, cards from the LP outlines.

    python3 research/companies/amazon/tools/gen_narrative_cards.py

Reads vault/interviews/companies/amazon/lp/{stories/*.md, genai/stories.md, story_matrix.md}; writes
vault/interviews/rounds/narrative/cards/amazon/*.md (stepped QA cards, overwritten on every run) and the `amazon`
branch of skeleton/narrative.yaml (replaced on every run). Cards are verbatim outline text, nothing invented.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LP = ROOT / "vault/interviews/companies/amazon/lp"
OUT = ROOT / "vault/interviews/rounds/narrative/cards/amazon"
SKEL = ROOT / "skeleton/narrative.yaml"


def sections(text: str) -> dict[str, str]:
    parts = re.split(r"^## (.+?)\s*$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}


def card(cid: str, node: str, step: int, q: str, a: str) -> str:
    # Python-Markdown nests a list only at a 4-space indent; the outlines use 2
    a = re.sub(r"^((?:  )+)(?=[-*] |\d+\. )", lambda m: "    " * (len(m.group(1)) // 2), a, flags=re.M)
    return f"---\nid: {cid}\nnode: {node}\ntype: qa\nstep: {step}\n---\n## Q\n{q}\n\n## A\n{a.strip()}\n"


def story_order(name: str) -> tuple:
    m = re.match(r"([SRMG])(\d+)", name)
    return ("SMRG".index(m.group(1)), int(m.group(2)))


leaves: list[tuple[str, str]] = []   # (leaf id, title)
files: dict[str, str] = {}

# --- LP map leaf (first in study order)
matrix = sections((LP / "story_matrix.md").read_text(encoding="utf-8"))
table = matrix.get("每条 LP：先用哪个故事 / 备选", "")
leaves.append(("amazon.lp-map", "LP → 先用哪个故事"))
step = 0
for row in re.findall(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", table, re.M):
    num, lp, first, alt = row
    step += 1
    files[f"nr-amz-lp{int(num):02d}.md"] = card(
        f"nr-amz-lp{int(num):02d}", "amazon.lp-map", step,
        f"Amazon LP「{lp}」：先用哪个故事？备选是什么？",
        f"- 先用：**{first}**\n- 备选：{alt}\n- 讲之前先说一句这个 LP 在这里指什么，再进 S/T/A/R/L。")

# --- S / R / M stories
for p in sorted((LP / "stories").glob("*.md"), key=lambda p: story_order(p.stem)):
    text = p.read_text(encoding="utf-8")
    sid = p.stem.split("_")[0]
    title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
    head = re.search(r"^\*\*(.+?)\*\*\s*$", text, re.M)
    sec = sections(text)
    leaf = f"amazon.{sid.lower()}"
    leaves.append((leaf, title))
    base = f"nr-amz-{sid.lower()}"
    lp = sec.get("适用 LP", "")
    nums = sec.get("数字", "")
    files[f"{base}-hook.md"] = card(f"{base}-hook", leaf, 1,
        f"【{title}】开场第一句是什么？适用哪些 LP？要报哪些数字？",
        (f"**{head.group(1)}**\n\n" if head else "") + f"**适用 LP**\n\n{lp}\n\n**数字**\n\n{nums}")
    star = sec.get("S / T / A / R / L", "")
    star = re.sub(r"^### ([STARL])\s*$", r"**\1**\n", star, flags=re.M)
    files[f"{base}-starl.md"] = card(f"{base}-starl", leaf, 2, f"【{title}】STAR-L 提纲（60–90 秒）", star)
    if sec.get("追问与回答"):
        files[f"{base}-followups.md"] = card(f"{base}-followups", leaf, 3,
            f"【{title}】面试官会追问什么？每个怎么答？", sec["追问与回答"])
    if sec.get("换个 LP 讲"):
        files[f"{base}-relp.md"] = card(f"{base}-relp", leaf, 4,
            f"【{title}】换成别的 LP 问时，强调哪一段？", sec["换个 LP 讲"])

# --- GenAI stories G1–G4
g = (LP / "genai/stories.md").read_text(encoding="utf-8")
genai = [m for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", g, re.S | re.M) if "S · Situation" in m.group(2)]
for n, m in enumerate(genai, start=1):
    gid, gtitle, body = f"G{n}", re.sub(r"^G\d · ", "", m.group(1).strip()), m.group(2)
    leaf = f"amazon.{gid.lower()}"
    title = gtitle
    leaves.append((leaf, title))
    main_part, _, follow = body.partition("\n- 追问：")
    main_part = re.split(r"\n- 可选", main_part)[0]
    files[f"nr-amz-{gid.lower()}-starl.md"] = card(f"nr-amz-{gid.lower()}-starl", leaf, 1,
        f"【{title}】适用 LP、开场 hook 和 STAR-L 提纲", main_part)
    if follow.strip():
        follow = re.sub(r"^  ", "", follow, flags=re.M)
        files[f"nr-amz-{gid.lower()}-followups.md"] = card(f"nr-amz-{gid.lower()}-followups", leaf, 2,
            f"【{title}】面试官会追问什么？每个怎么答？", follow)

# --- write cards (this folder is owned by the generator)
OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob("nr-amz-*.md"):
    old.unlink()
for name, body in files.items():
    (OUT / name).write_text(body, encoding="utf-8")

# --- skeleton branch
branch = ["  - id: amazon", "    order: 7", '    title: "Amazon · LP 故事（STAR-L）"',
          '    summary: "你自己的故事，按 LP 映射、STAR-L 提纲、追问与回答；先学 LP 映射，再按故事顺序复习。"',
          "    children:"]
for lid, title in leaves:
    t = title.replace('"', "'")
    branch += [f"      - id: {lid}", f'        title: "{t}"', f'        summary: "{t} 的提纲与追问。"']
text = SKEL.read_text(encoding="utf-8")
text = re.sub(r"\n  - id: amazon\n.*?(?=\n  - id: |\Z)", "", text, flags=re.S).rstrip("\n")
SKEL.write_text(text + "\n\n" + "\n".join(branch) + "\n", encoding="utf-8")
print(f"{len(leaves)} leaves, {len(files)} cards")
