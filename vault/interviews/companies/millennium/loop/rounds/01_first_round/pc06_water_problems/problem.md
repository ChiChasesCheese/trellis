# pc06 · Water Problems：Container With Most Water → Trapping Rain Water → 二维版

> 45 分钟第一轮编码题；Part 1、Part 2 是**同一轮**里报道的两道原题，Part 3 **(reconstructed)**。

## 背景

LeetCode Discuss 帖 7423863（Quant Dev-Python 岗）报道：Millennium LEaD 第一轮 45 min 编码，**Round 1 一次给了两道"盛水"题**——LC 11（Container With Most Water）和 LC 42（Trapping Rain Water）；TechPrep 2026 的 Millennium 题单同样收录这两题。两题看着像，考点却不同：LC 11 是"选两块板子"，LC 42 是"每根柱子头上能积多少水"——面试官常常先问 11 热身，再问 42 追问"如果是所有柱子呢"。

## API 契约（英文签名）

```python
def max_container_area(heights: list[int]) -> int
def trap_prefix_suffix(heights: list[int]) -> int
def trap_two_pointer(heights: list[int]) -> int
def trap_2d(grid: list[list[int]]) -> int
```
- `heights` 必须是 `list[int]`，元素非负；否则 `ValueError`。
- `grid` 必须是非空的矩形（每行等长）`list[list[int]]`，元素非负；否则 `ValueError`。

## 规则

### Part 1 — LC 11：Container With Most Water（双指针）

`heights[i]` 是竖线的高度，选两条竖线 `i < j`，与 x 轴围成的容器能装 `min(heights[i], heights[j]) * (j - i)` 的水，求最大值。双指针从两端向中间收缩：**每次移动较矮的那一侧**——移动较高的那一侧，宽度必然减 1，而高度仍然被那根矮的卡住（或更矮），面积只可能不变或变小；只有移动矮的那一侧才有可能找到更大的面积。

### Part 2 — LC 42：Trapping Rain Water（先 O(n) 空间，再 O(1) 空间）

柱子 `i` 头上能积的水是 `max(0, min(左边最高柱子, 右边最高柱子) - heights[i])`。

先给出容易在压力下推出的版本 `trap_prefix_suffix`：从左扫一遍得到 `left_max[i]`，从右扫一遍得到 `right_max[i]`，逐个柱子套公式，O(n) 时间、O(n) 空间。

再给出面试官常追问的 `trap_two_pointer`：双指针从两端向中间走，各自维护一个"目前为止的最大高度"（`left_max` / `right_max`），**每步移动 `left_max`/`right_max` 较小的那一侧**——因为较小的那一侧，另一侧路径上必然存在一根不矮于它的柱子（否则该侧的 running max 不会是当前的较小值），所以当前指针头上的水完全由它自己这一侧的 running max 决定，不需要提前算好整个数组的 `right_max`。O(n) 时间、**O(1) 额外空间**。

### Part 3 — 二维盛水（LC 407 的做法） **(reconstructed)**

从"一排柱子"推广到"一整块高度图"`grid[i][j]`：边界格子存不住水（水会流出网格），每个内部格子头上能积的水由"从边界不下坡也能摸到它的最低那圈围墙"决定。做法：用最小堆从边界格子开始向内扩张——**每次都先处理堆里当前水位最低的那个格子**，它的未访问邻居能积的水就是 `max(0, 当前水位 - 邻居自身高度)`，再把邻居按 `max(当前水位, 邻居自身高度)` 入堆（水位只会不降）。`grid` 长或宽小于 3 时无法围水，返回 `0`。

## Worked examples（全部由 `solution.py` 实际运行得出）

**Part 1**
- `max_container_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) = 49`（下标 1 与 8，高度 8 和 7，宽 7）
- `max_container_area([1, 1]) = 1`
- `max_container_area([]) = 0`，`max_container_area([5]) = 0`（少于两条竖线）

**Part 2**
- `trap_two_pointer([0,1,0,2,1,0,1,3,2,1,2,1]) = 6`，`trap_prefix_suffix` 在同一输入上同样是 `6`
- `trap_two_pointer([4,2,0,3,2,5]) = 9`，`trap_prefix_suffix` 在同一输入上同样是 `9`
- `trap_two_pointer([]) = 0`，`trap_two_pointer([5]) = 0`，`trap_two_pointer([5, 3]) = 0`（少于 3 根柱子存不住水）

**Part 3**
- ```
  grid = [[1, 4, 3, 1, 3, 2],
          [3, 2, 1, 3, 2, 4],
          [2, 3, 3, 2, 3, 1]]
  trap_2d(grid) = 4
  ```
- ```
  grid = [[3, 3, 3, 3, 3],
          [3, 2, 2, 2, 3],
          [3, 2, 1, 2, 3],
          [3, 2, 2, 2, 3],
          [3, 3, 3, 3, 3]]
  trap_2d(grid) = 10   # 内圈 8 个高度 2 的格子各积 1（水位被外圈的 3 顶住）= 8，中心 1 个高度 1 的格子积 2，共 10
  ```

## `main()` 命令流

Part 1/2：每行一组空格分隔的 `heights`。Part 3：先一行行数 `R`，再 `R` 行网格（列数从第一行推断）；可以多个 `R` + 网格块背靠背。

```
PART 1                          PART 2                            PART 3
1 8 6 2 5 4 8 3 7                0 1 0 2 1 0 1 3 2 1 2 1            3
1 1                              4 2 0 3 2 5                        1 4 3 1 3 2
→ 49                             → 6                                3 2 1 3 2 4
  1                                9                                2 3 3 2 3 1
                                                                     → 4
```

## 边界清单

- `heights = []` / 单元素 / 两元素（Part 1 两元素仍能围出面积；Part 2 需要 ≥ 3 根柱子才存得住水）
- 单调递增或单调递减的 `heights`（Part 2 应为 0）
- `heights` 或 `grid` 含负数 → `ValueError`
- `grid` 行长不一致、`grid` 为空 → `ValueError`
- `grid` 的行数或列数 < 3（无法围水）→ 返回 `0`
- Part 2 的两个实现（`trap_prefix_suffix` 与 `trap_two_pointer`）在同一输入上必须给出相同答案
- Part 3 全部格子等高（不积水）、中心比四周低很多（水位被最低的一圈"围墙"卡住，不是被最高的柱子卡住）

## 追问

1. **为什么双指针（Part 1）一定正确？** 交换论证：固定短的那侧不动、只动高的那侧，面积不会变大（宽度变小，高度仍受限于矮的那侧）；所以每一步移动矮的那侧是唯一可能找到更优解的动作，不会漏掉最优解。
2. **Part 2 的双指针为什么不用提前算好 `right_max`？** 谁的 running max 小，谁这一侧的水就已经被另一侧"担保"过了——另一侧路径上必然有一根不矮于它的柱子，所以当前柱子头上的水只取决于自己这一侧见过的最高点。
3. **Part 3 为什么用最小堆而不是最大堆？** 水位由"最低的围墙"决定，必须先处理堆里水位最低的格子，才能保证每个格子第一次被访问时用到的就是它能达到的最高水位（更晚访问只会被更高的水位覆盖，那是错的——水不可能凭空绕过一堵矮墙）。
4. **Part 1 与 Part 2 能不能共用一套双指针框架？** 形式像，但移动条件的"意义"不同：Part 1 移动矮的一侧是因为矮的一侧限制了面积；Part 2 移动 running max 较小的一侧是因为那一侧的水量已经确定。混着讲容易把两题的正确性证明搞反。

## 来源与置信度

- **HIGH（一手）**：LeetCode Discuss 7423863（Quant Dev-Python，Millennium LEaD 第一轮 Round 1，同一轮两题）：LC 11 `https://leetcode.com/problems/container-with-most-water/`、LC 42 `https://leetcode.com/problems/trapping-rain-water/`；TechPrep 2026 Millennium 题单同列这两题。
- Part 3（LC 407 `https://leetcode.com/problems/trapping-rain-water-ii/` 的最小堆做法）未见于该轮的一手报道，标 **(reconstructed)**：是"从一排柱子到一整块高度图"最自然的追问方向。

## 考什么

双指针的正确性证明（交换论证）· 同一问题从 O(n) 空间压到 O(1) 空间的思路（Part 2）· 把一维的"运行最大值"推广到二维的"最小堆扩张"（Part 3）。
