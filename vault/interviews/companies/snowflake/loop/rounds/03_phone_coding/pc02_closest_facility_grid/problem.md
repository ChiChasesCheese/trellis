# pc02 · Closest Facility Grid — multi-source BFS, tie-broken source tracking, walls

**类型：** phone screen（40 min）· 3 part 递进 · 网格多源 BFS
**最近：** 2026-09 · **置信度：** MED-HIGH（Part1-2）/ 重建（Part3，见文末）

## 背景
"每个工位到最近卫生间的距离"是 Snowflake 电面池里"High Frequency"标记的一道多源 BFS 题：把所有
卫生间同时当作 BFS 起点，一次遍历算出每个工位的最短距离。本题在原题基础上递进：Part1 只要距离，
Part2 还要知道"是哪一个卫生间"（多个卫生间距离相同时如何 tie-break 是这题真正的难点），Part3
（重建）加入不可通行的墙体格子，逼迫实现从"网格坐标算曼哈顿距离"换成"真正沿网格走 BFS"。

## API 契约（英文签名）
```python
def nearest_bathroom_distances(grid: list[str]) -> list[int]: ...

def nearest_bathroom_with_location(grid: list[str]) -> list[tuple[int, tuple[int, int]]]: ...

def nearest_bathroom_with_obstacles(grid: list[str]) -> list[tuple[int, tuple[int, int]]]: ...
```
`grid` 是一个字符矩阵（`list[str]`，每行等长）：`'B'` = 卫生间，`'D'` = 工位，`'.'` = 空地，
`'#'`（仅 Part3 会出现）= 墙。所有函数返回值按**工位在网格里的行主序（row-major：先按行、同一行
按列）**排列，与它们在 `grid` 里出现的顺序一致——**不是**按 `(row, col)` 数值排序后再输出这种
歧义表述，就是"从上到下、同一行从左到右第一次遇到 `'D'` 的顺序"。

## 规则

### Part 1 — 多源 BFS：只要距离
`nearest_bathroom_distances(grid)`：对每个工位，返回它到最近卫生间的最短 4 方向步数（上下左右，
不能斜走）。用**多源 BFS**（所有卫生间同时作为起点入队，而不是对每个工位单独跑一次 BFS）保证
`O(rows × cols)` 而不是 `O(rows × cols × 工位数)`。**网格里一个卫生间都没有** → 每个工位的
距离都是 `-1`。

### Part 2 — 还要哪一个卫生间，tie-break 规则
`nearest_bathroom_with_location(grid)`：在 Part1 的距离之外，额外返回**是哪个卫生间**达成了这个
最短距离，以 `(row, col)` 表示。如果有多个卫生间到某个工位的最短距离相同，**选 `(row, col)`
字典序最小的那个**（先比 `row`，`row` 也相同再比 `col`）。这个 tie-break 不能靠"BFS 队列里谁先
被处理"这种实现细节偶然决定——必须是对"所有并列最近的卫生间"显式比较后的确定性选择（否则多源
BFS 用普通单队列实现时，谁赢完全取决于入队顺序，同一道题换一种写法就会给出不同答案）。找不到
可达卫生间时返回 `(-1, (-1, -1))`。

### Part 3 — 加入墙体格子（重建）
`nearest_bathroom_with_obstacles(grid)`：网格里可能出现 `'#'`（墙），BFS **不能穿过**墙格子。
这个变体逼着实现从"预先算好曼哈顿距离再排序挑最小"这种走捷径的写法（网格没有障碍物时曼哈顿距离
就是 BFS 距离，两者会给出相同结果，容易蒙混过关）切换成"真的沿着网格边跑 BFS"——本题的一个
worked example（例3）就是刻意构造一个曼哈顿距离很短但直线被墙挡住、必须绕路的场景，专门戳破这类
抄近路的实现。工位被墙完全隔绝、够不到任何卫生间时，和"没有可达卫生间"一样返回 `(-1, (-1, -1))`。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1（Part1，来源原文例子）**
```
grid = [
    "..B.",
    ".D..",
    "...D",
]
nearest_bathroom_distances(grid)
```
→ `[2, 3]`（工位 `(1,1)` 到卫生间 `(0,2)` 距离 2，工位 `(2,3)` 到 `(0,2)` 距离 3 —— 与来源原文的
"bathroom (0,2), desks (1,1)/(2,3) → distances 2/3" 完全一致）。**没有卫生间**时：
```python
nearest_bathroom_distances(["..D", "D.."])
```
→ `[-1, -1]`。

**例 2（Part2，tie-break：两个卫生间等距，取 `(row, col)` 更小的）**
```python
nearest_bathroom_with_location(["B.D.B"])
```
→ `[(2, (0, 0))]`（工位在 `(0,2)`，两个卫生间 `(0,0)` 和 `(0,4)` 都是距离 2，`(0,0)` 字典序更小，
胜出）。

**例 3（Part3，曼哈顿距离骗不过 BFS：直线被墙挡住必须绕路）**
```python
grid = [
    "B#D",
    ".#.",
    "...",
]
nearest_bathroom_with_obstacles(grid)
```
→ `[(6, (0, 0))]`（卫生间 `(0,0)` 到工位 `(0,2)` 的曼哈顿距离是 2，但中间两格 `(0,1)`/`(1,1)`
都是墙，必须绕到底排 `(2,0)→(2,1)→(2,2)` 再往上走，真实最短路径是 6 步）。**完全被墙隔绝**：
```python
nearest_bathroom_with_obstacles(["B#D"])
```
→ `[(-1, (-1, -1))]`（唯一路径被墙截断，够不到任何卫生间）。

## `main()` 命令流
三个 part 输入格式相同：首行之后是 `"<rows> <cols>"`，接着 `rows` 行网格（每行 `cols` 个字符）。

**Part1** 输出：每个工位一行，该工位到最近卫生间的距离（行主序）。
**Part2 / Part3** 输出：每个工位一行 `"<dist>,<row>,<col>"`（行主序），够不到卫生间时输出
`"-1,-1,-1"`。

## 边界清单
- 网格里没有任何 `'D'` → 空输出列表（三个函数都要处理）
- 网格里没有任何 `'B'` → 每个工位距离 `-1`（Part1）/ `(-1, (-1, -1))`（Part2/3）
- 单格网格（`1×1`），该格本身是 `'B'` 或 `'D'` 或两者都不是的退化情况
- 多个卫生间到同一工位并列最短：tie-break 必须是"所有并列最近的卫生间里 `(row, col)` 最小"，
  不能是"BFS 遍历顺序里先发现的那个"（测试会构造让朴素单队列实现和正确 tie-break 给出不同答案的
  网格）
- Part3：工位被墙完全包围（四个方向都是 `'#'` 或网格边界）→ 无法离开原地，视为不可达
- Part3：直线曼哈顿距离很短但被墙挡住必须绕远路（例3），以及墙不影响的对照组（同样布局去掉墙，
  距离应该更短）用于交叉验证实现真的在做 BFS 而不是抄近路算曼哈顿距离
- 网格规模上限 `1000 × 1000`（约 1e6 格）：必须是一次多源 BFS，不能对每个工位各跑一次 BFS

## 追问
1. "如果工位比卫生间多得多（比如 10⁶ 个工位、10 个卫生间），单源 BFS 循环 10 次 vs 多源 BFS
   一次，复杂度差在哪？"——期望候选人说清楚：单源 BFS 从每个卫生间各跑一次是 `O(B × R × C)`，
   多源 BFS 把所有卫生间一起入队是 `O(R × C)`，与卫生间数量无关。
2. "Part2 的 tie-break 如果换成'返回所有并列最近的卫生间列表'而不是选一个，你的实现要怎么改？"——
   期望候选人指出按层处理 BFS（frontier 一层一层扩展）的写法只需要把"选更小的" 改成"收集全部"，
   而如果原来偷懒用了单队列 FIFO 实现，这个改动会很痛苦，因为单队列版本从一开始就没有保留"这一
   层所有候选来源"的信息。
3. "生产环境里工位/卫生间的位置会变化（重新装修、新开工区），你会怎么避免整个 1000×1000 网格
   重新跑一遍 BFS？"——开放式延伸，期望提到增量更新（只重算受影响区域）、分区/网格分块缓存，
   不要求现场实现。

## 变体
- Part1/2 与来源原文（1point3acres 公开预览题 + fastprep "High Frequency" 标记）逐字对应；
  Part3 的墙体格子是本题的重建延伸，工位/卫生间/墙的三元素组合是网格 BFS 题里最常见的下一步
  追问方向，但未见到 Snowflake 面试的直接一手记录，因此单独标注置信度。

## 来源与置信度
- https://www.1point3acres.com/interview/problems/94f2a5c6-db25-4269-9359-a47bcc61d8b8
  （公开预览题，company 标签 Snowflake）："Given a 2D grid with bathrooms ('B'), desks ('D')...
  determine the shortest Manhattan distance from each desk to its nearest bathroom using
  4-directional movement... multi-source BFS." 约束 `1 ≤ m, n ≤ 1000`；例子"bathroom at (0,2),
  desks (1,1)/(2,3) → distances 2/3；no bathrooms → all -1"。
- https://www.fastprep.io/problems/snowflake-closest-bathroom-desk-grid ——"Closest Bathroom /
  Desk on a Grid (Snowflake Phone Screen)"，标记 "High Frequency"，tags BFS/grid/two-pointer/
  heap，约 60 分钟时长。
- `catalog/raw/coding_phone_onsite.md` #4、`catalog/CATALOG.md` Table A pc02 行；置信度
  **MED-HIGH**（Part1/2）：两个独立结构化来源，例子数值精确交叉验证。Part3（墙体格子）**无
  一手或聚合站来源**，是本题按"网格 BFS 题的常见下一步"自行设计的延伸，置信度不并入上述评级。

## 考什么
S05 图：多源 BFS、路径重建、valid tree 同族 · S08 复杂度再压一档（单源×N 次 vs 多源一次）
