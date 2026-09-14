# pc02 Closest Facility Grid — report

## Summary
把 Snowflake 电面池里"每个工位到最近卫生间"的多源 BFS 网格题（1point3acres 公开预览 + fastprep
"High Frequency"）做成 3-part 递进：Part1 只要距离 → Part2 还要确定的 tie-break（并列最短时选
`(row, col)` 最小的卫生间）→ Part3（重建）加入墙体格子，逼实现从"曼哈顿距离排序"换成真正的 BFS。

## Sources & confidence
MED-HIGH（Part1/2）——两个独立结构化来源（1point3acres 公开预览题 + fastprep），例子数值
`bathroom (0,2), desks (1,1)/(2,3) -> 2/3` 精确交叉验证（problem.md 例1 用同一组坐标复算）。
Part3 的墙体格子无一手/聚合站来源，是本题按"网格 BFS 题的常见延伸"自行设计，单独标注、不并入
上述评级。

## Approach by part
1. `_bfs_with_source` 是三个 part 共享的核心：把所有卫生间同时作为 BFS 起点，**按层**（而不是
   单个 FIFO 队列混着走）处理 frontier——每一层先收集"这一层所有候选者试图认领的下一层格子"，
   同一个格子被多个来源同时认领时，比较来源坐标取字典序更小的那个，再统一提交这一层的结果。这个
   "按层批量决议"是 Part2 tie-break 正确性的关键：如果用一个普通单队列 BFS，谁先出队纯粹取决于
   入队顺序，同一道题换一种实现会给出不同的"winner"。
2. Part1 只取 `_bfs_with_source` 的距离数组，按工位在网格里出现的行主序读出。
3. Part2 额外读出 `source` 数组（每个格子第一次被访问时记录的来源卫生间坐标），不可达时统一
   返回 `(-1, (-1, -1))`。
4. Part3 给 `_bfs_with_source` 传入 `blocked_char='#'`，扩展时跳过墙格子；其余逻辑与 Part2
   完全共享，只是这次"不可达"不只来自"没有卫生间"，也可能来自"被墙完全封死"。

## Pitfalls hidden tests target
- 多源 BFS 必须是一次遍历，不是对每个卫生间单独跑一次 BFS 再取最小值（复杂度测试用 1000×1000
  网格验证）
- Tie-break 必须显式比较"所有并列最近的来源"，不能依赖 BFS 实现细节里的偶然顺序
  （`test_worked_example_2_tie_break` 构造了故意会暴露这个 bug 的对称网格）
- Part3 的曼哈顿距离陷阱：同一个坐标关系，直线距离很短但被墙挡住必须绕远路（例3），配一个"去掉
  墙" 的对照组验证墙真的在起作用，而不是实现根本没检查 `'#'`
- 完全被墙封死的工位，和"网格里没有卫生间"一样返回 `(-1, (-1, -1))`，不能因为"存在卫生间"就
  误判为可达
- 行主序输出顺序：工位在 `grid` 里的物理出现顺序，不是按坐标数值重新排序

## Complexity & measured cost
`O(rows × cols)` 每个 part（每个格子最多入队一次）。1000×1000 网格（约 5% 工位、0.1% 卫生间随机
撒点）纯函数耗时约 0.57s，通过 `run_script` 端到端实测 well under 2s / 256MB。

## Test inventory
19 tests — part1: 6（含 1 io）· part2: 5（含 1 io、1 fmt）· part3: 4（含 1 io）；edge 10 · fmt 1 ·
io 3 · perf 1。

## Skills exercised
S05 图：多源 BFS、路径重建、valid tree 同族 · S08 复杂度再压一档（单源×N 次 vs 多源一次）
