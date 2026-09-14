# pc05 Max Events II — report

## Summary
2026-06 一手电面原题 LC 1751（至多 k 个不重叠活动的最大价值，闭区间）。做成 3-part：Part 1 原题 → Part 2 输出一个最优方案 **(reconstructed)** → Part 3 去掉 k 限制并放大到 10^5 **(reconstructed)**。

## Sources & confidence
HIGH 于题号、轮次、时长（1p3a thread-1179486 / t.me 28733 摘要）；follow-up 具体内容不可读，Part 2/3 按同族常见追问重建并在题面标注。

## Approach by part
1. 按 start 排序；`nxt[i] = bisect_right(starts, end_i)`（闭区间，所以要严格大于）；`dp[j][i] = max(dp[j][i+1], v_i + dp[j-1][nxt[i]])`。O(n log n + n·k)。
2. 保留整张表，从 `(i=0, j=k)` 往前走：`take ≥ skip` 且价值为正就选，跳到 `nxt[i]`；否则 `i+1`。方案下标排序后输出。
3. 按 end 排序；`best[i] = max(best[i-1], v_i + best[p])`，`p = bisect_left(ends, start_i)`（结束严格早于开始的活动个数）。O(n log n)。

## Pitfalls hidden tests target
- 闭区间：`[1,2]` 与 `[2,3]` 冲突（`bisect_right` 写成 `bisect_left` 就错）
- `k = 0` / 空列表 / `k > n`
- 同一区间重复出现；同一天多个单日活动
- Part 2 方案必须合法：数量 ≤ k、不重叠、价值和等于最优、下标升序无重复（随机 400 组校验）
- 非法输入抛 `ValueError`
- Part 1 在 `k·n = 10^6` 下的时间；Part 3 在 `n = 10^5` 下的时间

## Complexity & measured cost
Part 1 O(n log n + n·k) 时间、O(n·k) 空间（为 Part 2 保留整表）；Part 3 O(n log n) / O(n)。编排者用暴力枚举在 3000 组随机小输入上交叉验证三个 part，0 不一致。perf：Part 3 n = 10^5 端到端 < 2 s；Part 1 n = 2·10^4、k = 50 端到端 < 4 s（纯 Python 双层循环，预算放宽并在测试里写明）。

## Test inventory
22 tests — part1 11（含 4 个参数化样例、1 perf、1 io）· part2 5（含 1 io、1 fmt）· part3 5（含 1 perf、1 io）；edge 9 · fmt 1 · perf 2 · io 3。

## Skills exercised
S03 加权区间调度 · S08 复杂度再压一档 · S02（对比）计数 DP 的状态设计
