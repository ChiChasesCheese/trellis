# pc25 Grep With Context Lines — report

## Summary
一手预览只给出函数签名与"像 grep -C"这一句。三段：Part 1 窗口合并（原题）；Part 2 GNU 风格
`--` 分组 + 不对称 `-B/-A`；Part 3 流式 O(lines_around) 内存版本，均为 **(reconstructed)**。

## Sources & confidence
MED（聚合站 TrueInterview 同步清单，题面付费，仅预览签名可见）：见
`../../../catalog/raw/github_repos.md` §2/§3。分组、`-B/-A`、流式版本均为重建，对照真实 GNU
grep 语义。

## Approach by part
1. 对每个命中位置标记 `[i-around, i+around]`（截断到边界）到一个布尔数组，最后按原序输出被标记
   的行——标记数组天然去重与合并重叠窗口。
2. 同样的标记逻辑，`before`/`after` 分开；输出时额外跟踪"上一个被保留行的下标"，下标不连续时插
   入 `"--"`。
3. 用一个容量为 `lines_around + 1` 的 `deque` 环形缓冲：新行入队时如果自己是命中，就地把队列里
   已有的最近 `lines_around` 行标记为保留，并设置"接下来 `lines_around` 行也保留"的计数器；队列
   超过容量时弹出最老的一行并按其标记决定是否输出。500+ 组随机数据验证与批量版本结果完全一致。

## Pitfalls hidden tests target
- 重叠/相邻窗口去重合并（`test_overlapping_windows_no_duplicates`）
- Part 2 的 `--` 不能出现在第一段前或最后一段后
- Part 3 用真正的一次性迭代器（生成器）测试，防止偷懒 `list(lines)` 之后复用 Part 1 实现
- 负数 `lines_around`/`before`/`after` 校验
- 命中行本身算不算自己窗口的一部分（算）

## Complexity & measured cost
Part 1/2：`O(n)` 标记 + `O(n)` 输出。Part 3：`O(n)` 时间、`O(lines_around)` 辅助空间（不含输出）。
perf：20 万行、稀疏命中（每 5000 行一个），端到端 < 2s。

## Test inventory
20 tests — part1 7（含 1 perf、1 io）· part2 5（含 1 io/fmt）· part3 6（含 1 io）；
edge 10 · fmt 1 · perf 1 · io 3。

## Skills exercised
S03（区间标记 + 合并）· 流式算法的"延迟定案"模式（有界环形缓冲区替代无界累积）· 对真实 grep
行为（`-B/-A/-C`、`--` 分组）的精确复刻。
