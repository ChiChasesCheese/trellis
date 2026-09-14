# od10 Student / Result OOP — report

## Summary
2026-05 AIML 实习 OA 第二题（与 q19 同场）：`Result` 继承 `Student`，3 科成绩、百分比、及格线 33.33%、处理复查。原帖只有骨架，具体规则大多为重建。2-part：Part 1 继承 + 校验 + `Decimal` 百分比 + 报告 → Part 2 复查规则 + 排名 **(reconstructed)**。

## Sources & confidence
HIGH 于题目存在与骨架（Reddit `1t0ogu7` 一手）；interviewfox 回忆（LOW）措辞一致。校验范围、四舍五入方式、复查次数与只升不降、排名规则为重建，题面逐条标注。

## Approach by part
1. `Student` 校验学号与名字；`Result.__init__` 先 `super().__init__` 再校验 3 科 0–100；`percentage` 用 `Decimal(sum) * 100 / 300` 再 `quantize(0.01, ROUND_HALF_UP)`；`marks` 返回副本。
2. `recheck` 先校验（非法不消耗机会），再查"已复查集合"，再比较新旧分数；`Registry.top` 以 `(-percentage, roll)` 排序。命令流统一在 `run_commands`。

## Pitfalls hidden tests target
- 及格线边界（100 vs 99）；float 比较误差
- HALF_UP 两位小数与 `0.00`
- 8 种非法构造；`marks` 被外部修改
- 重复学号 / 坏 ADD 行 → `ERROR`
- 复查的消耗语义：非法不消耗、相等或更低仍消耗
- 同分排名按学号；`TOP 0`、空注册表
- 5 万人 + 5 万次复查的性能

## Complexity & measured cost
ADD / REPORT / RECHECK O(1)；TOP O(n log n)。5 万人 + 5 万次复查 + 一次 TOP 端到端 < 3 s。

## Test inventory
27 tests — part1 17（含 8 参数化非法构造、1 io、1 fmt）· part2 10（含 4 参数化、1 perf、1 io）；edge 20 · fmt 1 · perf 1 · io 2。

## Skills exercised
S09 契约先行（继承、校验、封装）· Decimal 精度 · 状态型规则（一次性复查）
