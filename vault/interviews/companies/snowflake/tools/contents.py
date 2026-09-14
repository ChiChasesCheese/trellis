#!/usr/bin/env python3
"""全书目录：从知识树生成 CONTENTS.md（轮次 → 技能 → 题），题按 28 法则分数排序。

  python3 tools/contents.py            # 写 CONTENTS.md（勿手改，重跑覆盖）

单一来源：
  * 结构（哪轮有哪些技能、每个技能挂哪些题）= loop/tree/interview-loop.yaml
  * 分数（#refs × 时效 × 轮次权重）= catalog/RANK.md + tools/pareto.py 的同一套函数
  * 题集目录 / 题解文章是否存在 = 文件系统
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import re
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
FOCUS = ["OA", "电面", "PS", "技术筛"]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pareto = _load("pareto", KIT / "tools" / "pareto.py")
tree = _load("check_tree", KIT / "loop" / "tree" / "check_tree.py")


def scores() -> tuple[dict[str, tuple[float, str, str, str]], int]:
    head, body = pareto.load_table(KIT / "catalog" / "RANK.md", "总表")
    iid, iref, idt, ist, iconf = (pareto.col(head, n) for n in ("ID", "#refs", "最近", "轮次", "置信度"))
    today = dt.date.today()
    out = {}
    for r in body:
        refs = int(re.search(r"\d+", r[iref]).group())
        sc = refs * pareto.recency(r[idt], today) * pareto.stage_weight(r[ist], FOCUS)
        out[r[iid]] = (sc, r[iref], r[idt], r[iconf])
    ranked = sorted(out, key=lambda k: -out[k][0])
    total, acc, cut = sum(v[0] for v in out.values()), 0.0, len(ranked)
    for i, k in enumerate(ranked, 1):
        acc += out[k][0]
        if acc >= 0.8 * total:
            cut = i
            break
    return {k: out[k] + (i + 1 <= cut,) for i, k in enumerate(ranked)}, cut


def problem_dir(pid: str) -> Path | None:
    p = tree.resolve(pid)
    return p if p and p.is_dir() else None


def title_of(d: Path) -> str:
    for name in ("problem.md", "prompt.md"):
        f = d / name
        if f.exists():
            first = f.read_text(encoding="utf-8").splitlines()[0]
            title = re.sub(r"^#\s*", "", first).strip()
            return re.sub(rf"^{re.escape(d.name.split('_', 1)[0])}\s*·\s*", "", title)
    return d.name


def main() -> None:
    text = (KIT / "loop" / "tree" / "interview-loop.yaml").read_text(encoding="utf-8")
    rounds, _prereq = tree.parse(text)
    names = dict(re.findall(r"- id: (\S+)\n\s+name: (.+)", text))
    sc, cut = scores()
    readme = (KIT / "study" / "30-articles" / "README.md").read_text(encoding="utf-8")
    lc_links = dict(re.findall(r"^\| (\w+) \| (\[LC [^]]+\]\([^)]+\)) \|", readme, re.M))
    lines = [
        "# 目录 — 按轮次读，按分数练",
        "",
        "> 由 `python3 tools/contents.py` 从 `loop/tree/interview-loop.yaml` + `catalog/RANK.md` 生成，**勿手改**。",
        "> 每个技能下的题按 28 法则分数（#refs × 时效 × 轮次权重）降序；**★ = cut line 以内**（累计 80% 流出次数）。",
        "> 每题：题集目录（题面 + 测试 + 参考解）→ 题解文章（先做后读）。LeetCode 原题的公司标签全表见 `../../core/leetcode/companies/snowflake.md`。",
        "",
    ]
    for rnd in rounds:
        lines += [f"## {rnd['id']} · {names.get(rnd['id'], '')}", ""]
        study = rnd.get("study") or []
        if study:
            lines.append("先读：" + " · ".join(f"[{Path(s).stem}]({s})" for s in study))
            lines.append("")
        for sk in rnd.get("skills", []):
            probs = sk.get("problems") or []
            coded = [p for p in probs if p not in tree.NONCODE]
            if not coded:
                lines += [f"- **{names.get(sk['id'], sk['id'])}** — 题库：`loop/rounds/{tree.NONCODE[probs[0]]}/`" if probs else f"- **{names.get(sk['id'], sk['id'])}**"]
                continue
            lines += [f"### {names.get(sk['id'], sk['id'])}", "", "| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |", "|---|---|---|---|---:|---|---|"]
            for pid in sorted(coded, key=lambda p: -sc.get(p, (0,))[0]):
                d = problem_dir(pid)
                if d is None:
                    continue
                rel = d.relative_to(KIT).as_posix()
                art = KIT / "study" / "30-articles" / f"{d.name}.md"
                art_cell = (f"[题解](study/30-articles/{d.name}.md)" if art.exists()
                            else lc_links.get(d.name, f"[model_answer]({rel}/model_answer.md)" if (d / "model_answer.md").exists() else "—"))
                s = sc.get(pid)
                star = "★" if s and s[4] else ""
                lines.append(f"| {star} | **{pid}** {title_of(d)} | [`{rel}/`]({rel}/) | {art_cell} | {s[1] if s else '—'} | {s[2] if s else '—'} | {s[3] if s else '—'} |")
            lines.append("")
        lines.append("")
    (KIT / "CONTENTS.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    n = sum(1 for l in lines if l.startswith("| ") and "**" in l)
    print(f"CONTENTS.md: {n} 题，cut line 第 {cut} 行")


if __name__ == "__main__":
    main()
