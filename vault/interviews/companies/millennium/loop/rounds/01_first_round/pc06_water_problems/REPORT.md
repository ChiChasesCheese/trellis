# pc06 Water Problems — report

## Summary
一手报道：Millennium LEaD 第一轮 45 min 编码的 Round 1 一次给了两道"盛水"题——LC 11（Container With Most Water）与 LC 42（Trapping Rain Water）。3-part：Part 1 双指针求最大容器面积（一手原题）→ Part 2 先 O(n) 空间再 O(1) 空间求积水量（一手原题及其常见追问）→ Part 3 二维高度图的积水量，最小堆做法 **(reconstructed)**。

## Sources & confidence
HIGH（一手）：LeetCode Discuss 7423863（Quant Dev-Python，Round 1，同一轮两题）+ TechPrep 2026 Millennium 题单，两者都列 LC 11 与 LC 42；Part 3（LC 407 的最小堆做法）未见一手报道，标 (reconstructed)，是"一维柱子到二维高度图"最自然的推广。

## Approach by part
1. 双指针从两端向中间收缩，每次移动较矮的一侧——交换论证：移动较高一侧，宽度必减、高度仍受矮的一侧限制，面积只可能不变或变小。
2. 先给 O(n) 空间版本（`left_max[i]` / `right_max[i]` 两个数组 + 逐格套公式），再给 O(1) 额外空间版本（双指针各自维护 running max，谁的 running max 小就移动谁——另一侧必有不矮于它的柱子担保）。
3. 从边界格子开始，用最小堆总是先扩张当前水位最低的格子；未访问邻居的积水是 `max(0, 当前水位 - 邻居自身高度)`，邻居入堆的水位是 `max(当前水位, 邻居自身高度)`。

## Pitfalls hidden tests target
- Part 1：`heights` 含负数 / 非 `int` → `ValueError`；空数组、单元素（少于两条竖线，返回 0）；全部相同高度
- Part 2：少于 3 根柱子存不住水；单调升/降序列积水为 0；两种实现（O(n) 空间 / O(1) 空间）必须在同一输入上给出相同答案（含 300 组随机数组的交叉验证）
- Part 3：`grid` 为空、行长不一致、含负数 → `ValueError`；全部等高不积水；网格小于 3×3 不积水；中心低、四周高时水位被**最低的一圈围墙**卡住而不是被最外层最高的柱子卡住（"moat" 用例）；与逐层 flood-fill 的暴力对照（60 组随机 3×3–6×6 网格）

## Complexity & measured cost
Part 1/2：O(n) 时间、O(1)（`trap_two_pointer`）或 O(n)（`trap_prefix_suffix`）空间。Part 3：O(m·n·log(m·n)) 时间（每个格子进出一次最小堆）。编排者验证：Part 1 与暴力 O(n²) 枚举在 300 组随机数组上 0 处不一致；Part 2 的两种实现互相一致且都与暴力 O(n) 前后缀法一致；Part 3 与"逐层水位 + flood fill"暴力在 60 组随机网格上 0 处不一致。perf：10 万根柱子的数组，`solution.py` 作为脚本端到端 < 2 s。

## Test inventory
24 tests — part1 8（含 1 io）· part2 9（含 1 perf、1 io）· part3 7（含 1 io/fmt）；edge 13 · fmt 1 · perf 1 · io 3。`grep -c "def test" test_pc06.py` = 24。

## Skills exercised
双指针的正确性证明（交换论证）· 同一问题从 O(n) 空间压到 O(1) 空间（Part 2 的两种实现对照）· 一维"运行最大值"到二维"最小堆扩张"的推广（Part 3）· 网格类问题的输入校验（矩形、非负、最小尺寸）。
