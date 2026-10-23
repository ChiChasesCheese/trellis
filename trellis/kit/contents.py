"""全书目录：从知识树生成 CONTENTS.md（轮次 → 技能 → 题），题按 28 法则分数排序。

  trellis kit contents --co millennium      # 写 kit 里的 CONTENTS.md（勿手改，重跑覆盖）

单一来源：
  * 结构（哪轮有哪些技能、每个技能挂哪些题）= 研究目录里的 interview-loop.yaml
  * 分数（#refs × 时效 × 轮次权重）= 研究目录 catalog/RANK.md + pareto.py 的同一套函数
  * 题集目录 / 题解文章是否存在 = kit 的文件系统

选项：--focus 给哪些轮次权重 1.0（默认取该公司档案）；--codebase 练习代码库型 kit
（标题取 RANK.md，题解列优先 walkthrough / REVIEW_KEY，页首说明改为代码库用法）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

from . import check_tree as tree
from . import pareto
from .paths import Kit


def scores(kit: Kit, focus: list[str]) -> tuple[dict[str, tuple[float, str, str, str]], int]:
    head, body = pareto.load_table(kit.research / "catalog" / "RANK.md", "总表")
    iid, iref, idt, ist, iconf = (pareto.col(head, n) for n in ("ID", "#refs", "最近", "轮次", "置信度"))
    today = dt.date.today()
    out = {}
    for r in body:
        refs = int(re.search(r"\d+", r[iref]).group())
        sc = refs * pareto.recency(r[idt], today) * pareto.stage_weight(r[ist], focus)
        out[r[iid]] = (sc, r[iref], r[idt], r[iconf])
    ranked = sorted(out, key=lambda k: -out[k][0])
    total, acc, cut = sum(v[0] for v in out.values()), 0.0, len(ranked)
    for i, k in enumerate(ranked, 1):
        acc += out[k][0]
        if acc >= 0.8 * total:
            cut = i
            break
    return {k: out[k] + (i + 1 <= cut,) for i, k in enumerate(ranked)}, cut


def title_of(d: Path, rank_titles: dict[str, str] | None = None) -> str:
    pid = d.name.split("_", 1)[0]
    if rank_titles and pid in rank_titles:
        return rank_titles[pid]
    for name in ("problem.md", "prompt.md", "PR.md", "PAGE.md", "BRIEF.md"):
        f = d / name
        if f.exists():
            first = f.read_text(encoding="utf-8").splitlines()[0]
            title = re.sub(r"^#\s*", "", first).strip()
            return re.sub(rf"^{re.escape(pid)}\s*·\s*", "", title)
    return d.name


def add_arguments(ap: argparse.ArgumentParser, common: argparse.ArgumentParser) -> None:
    ap.add_argument("--focus", default=None, help="逗号分隔；命中这些字样的轮次权重 1.0（默认取该公司档案）")
    ap.add_argument("--codebase", action=argparse.BooleanOptionalAction, default=None,
                    help="练习代码库型 kit（默认取该公司档案）")
    ap.add_argument("--tree", type=Path, default=None, help="interview-loop.yaml（默认在 --research 下找）")
    ap.add_argument("--out", type=Path, default=None, help="写到这里（默认 <kit>/CONTENTS.md）")


def run(a, kit: Kit) -> int:
    root = kit.kit
    focus = [f.strip() for f in a.focus.split(",") if f.strip()] if a.focus is not None else list(kit.profile.contents_focus)
    codebase = kit.profile.codebase if a.codebase is None else a.codebase
    rank_titles = (dict(re.findall(r"^\| (\w+) \| ([^|]+?) \|", (kit.research / "catalog" / "RANK.md").read_text(encoding="utf-8"), re.M))
                   if codebase else None)

    text = tree.tree_yaml(kit, a.tree).read_text(encoding="utf-8")
    rounds, _prereq = tree.parse(text)
    names = dict(re.findall(r"- id: (\S+)\n\s+name: (.+)", text))
    sc, cut = scores(kit, focus)
    rp = root / "study" / "30-articles" / "README.md"
    readme = rp.read_text(encoding="utf-8") if rp.exists() else ""
    lc_links = dict(re.findall(r"^\| (\w+) \| (\[LC [^]]+\]\([^)]+\)) \|", readme, re.M))
    if codebase:
        tail = ("练习代码库（cb）用 `python3 loop/ai_screen.py start <cb> <t>`；"
                "Abnormal 在 LeetCode 公司标签源里没有题单（`catalog/raw/github_repos.md`）。")
    else:
        tail = f"LeetCode 原题的公司标签全表见 `../../core/leetcode/companies/{kit.co}.md`。"
    lines = [
        "# 目录 — 按轮次读，按分数练",
        "",
        "> 由 `trellis kit contents` 从 `interview-loop.yaml` + `catalog/RANK.md` 生成，**勿手改**。",
        "> 每个技能下的题按 28 法则分数（#refs × 时效 × 轮次权重）降序；**★ = cut line 以内**（累计 80% 流出次数）。",
        f"> 每题：题集目录（题面 + 测试 + 参考解）→ 题解文章（先做后读）。{tail}",
        "",
    ]
    for rnd in rounds:
        lines += [f"## {rnd['id']} · {names.get(rnd['id'], '')}", ""]
        study = rnd.get("study") or []
        if study:
            lines.append("先读：" + " · ".join(f"[{Path(s).stem}]({s})" for s in study))
            lines.append("")
        core = rnd.get("core") or []
        if core:
            lines.append("通用能力（[[Code Core MOC|code-core]] 卡组与练习）：" + " · ".join(f"[[{c}]]" for c in core))
            lines.append("")
        for sk in rnd.get("skills", []):
            probs = sk.get("problems") or []
            coded = [p for p in probs if p not in kit.profile.noncode]
            if not coded:
                lines += [f"- **{names.get(sk['id'], sk['id'])}** — 题库：`loop/rounds/{kit.profile.noncode[probs[0]]}/`" if probs else f"- **{names.get(sk['id'], sk['id'])}**"]
                continue
            lines += [f"### {names.get(sk['id'], sk['id'])}", "", "| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |", "|---|---|---|---|---:|---|---|"]
            for pid in sorted(coded, key=lambda p: -sc.get(p, (0,))[0]):
                d = tree.resolve(kit, pid)
                if d is None or not d.is_dir():
                    continue
                rel = d.relative_to(root).as_posix()
                art = root / "study" / "30-articles" / f"{d.name}.md"
                if art.exists():
                    art_cell = f"[题解](study/30-articles/{d.name}.md)"
                elif codebase:
                    art_cell = (f"[walkthrough]({rel}/walkthrough.md)" if (d / "walkthrough.md").exists()
                                else f"[REVIEW_KEY]({rel}/REVIEW_KEY.md)" if (d / "REVIEW_KEY.md").exists()
                                else f"[model_answer]({rel}/model_answer.md)" if (d / "model_answer.md").exists() else "—")
                else:
                    art_cell = lc_links.get(d.name, f"[model_answer]({rel}/model_answer.md)" if (d / "model_answer.md").exists() else "—")
                s = sc.get(pid)
                star = "★" if s and s[4] else ""
                lines.append(f"| {star} | **{pid}** {title_of(d, rank_titles)} | [`{rel}/`]({rel}/) | {art_cell} | {s[1] if s else '—'} | {s[2] if s else '—'} | {s[3] if s else '—'} |")
            lines.append("")
        lines.append("")
    (a.out or root / "CONTENTS.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    n = sum(1 for l in lines if l.startswith("| ") and "**" in l)
    print(f"CONTENTS.md: {n} 题，cut line 第 {cut} 行")
    return 0
