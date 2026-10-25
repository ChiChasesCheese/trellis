"""Write vault/interviews/companies/headlands/07-practice-java-cpp.md: every kit problem as a Java pass and a C++ pass,
with the commands to start and test each, in interview order. Re-run after adding a problem.

    uv run python research/companies/headlands/tools/gen_practice.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KIT = ROOT / "vault/interviews/companies/headlands"
ROUNDS = [("00_oa", "OA 原题"), ("01_video", "视频面编码题"), ("03_lld", "设计与并发（LLD）")]

TRACKED = set(subprocess.run(["git", "ls-files", str(KIT)], capture_output=True, text=True, cwd=ROOT).stdout.split())

lines = [
    "# 07 · Java 和 C++ 各写一遍：练习清单",
    "",
    "每道题先用 Java 写一遍，再用 C++ 写一遍，按考场条件：关掉 AI 补全，计时，先说思路再写，写完自己造用例跑。"
    "每道题按 Part 推进，前两个 Part 是一场面试最常走到的地方，后面的 Part 当追问练。写完对照 `reference` 和讲义找差距，"
    "把卡住的点记在该题下面。",
    "",
    "## 怎么用",
    "",
    "在 `interviews/companies/headlands/` 目录下运行（每道题的命令在下面表格里）：",
    "",
    "```bash",
    "python3 tools/jtest.py start <题目目录>     # 复制 Java 空壳到 work/，在 work/ 里写",
    "python3 tools/jtest.py run   <题目目录> --tag part1",
    "python3 tools/cpptest.py start <题目目录>   # 复制 C++ 空壳到 cpp/work.hpp",
    "python3 tools/cpptest.py run   <题目目录> --tag part1",
    "```",
    "",
    "- **限时**：Part 1 约 15 分钟，Part 1 + 2 约 35 分钟；超时就停，读讲义，第二天重写。",
    "- **C++ 那一遍**：先过一遍 [[CPP_CONVENTIONS]] 和 C++ 讲义 C16（CoderPad 现场），注意整数溢出、迭代器失效、`const&` 传参。",
    "- **两遍之间**：不要看 Java 的代码写 C++；先想清楚两种语言里各自地道的数据结构（`TreeMap` 对 `std::map`，`ArrayDeque` 对 `std::deque`）。",
    "",
]
total = 0
for folder, title in ROUNDS:
    base = KIT / "loop/rounds" / folder
    if not base.is_dir():
        continue
    rows = []
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        prob = d / "problem.md"
        if not prob.exists() or str(prob.relative_to(ROOT)) not in TRACKED:
            continue  # only problems already committed: the page must not link work in progress
        head = prob.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        rel = d.relative_to(KIT)
        has_cpp = (d / "cpp" / "starter.hpp").exists()
        art = KIT / "study/30-articles" / f"{d.name}.md"
        link = f"[[{d.name}\\|讲义]]" if str(art.relative_to(ROOT)) in TRACKED else "—"
        cpp_cell = "☐" if has_cpp else "（暂无 C++ 版）"
        rows.append(f"| {head} | ☐ | {cpp_cell} | {link} | `{rel}` |")
        total += 1
    if rows:
        lines += [f"## {title}", "", "| 题 | Java | C++ | 讲义 | 目录 |", "|---|---|---|---|---|", *rows, ""]
lines += ["## 模拟题（Java / Maven）", "",
          "`mock_maven/` 是两道 Maven 项目形式的模拟题，只练 Java：先读 `mock_maven/README.md`。", ""]
(KIT / "07-practice-java-cpp.md").write_text("\n".join(lines), encoding="utf-8")
print(total, "problems")
