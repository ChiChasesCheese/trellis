# hc16 · 交易台层级树上的 DP

交易公司的台（desk）按上下级组成一棵树：一个根台，每个台最多一个直接上级，可以有任意多个下级，每个台有一个当日 PnL（盈亏，整数，可为负）。面试官先问：选一些台，任何一个台和它的直接上级不能同时被选，最大总 PnL 是多少？这是树上的打家劫舍（house robber on a tree）。接着问选了哪些台，最后问：如果这棵树是 10 万层的链呢？递归会栈溢出，所以从第一版就写成迭代。

## 面试官会怎么说

> "The desks form a tree; `parent[i]` is the direct superior of desk i, `-1` for the root. Each desk has a PnL. Pick desks so that no desk and its direct parent are both picked, maximizing total PnL."
> 接着会问："Now tell me which desks you picked." "What if the tree is a chain of 100,000 desks?" "What about the best path in the tree?" "What if I want exactly k desks?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：`parent[i] < i` 吗？根一定是 0 吗？全是负数时可以一个都不选吗？ |
| 3–17 分钟 | **Part 1**：建树 + 最大总 PnL（迭代） |
| 17–32 分钟 | **Part 2**：还原选了哪些台 |
| 32–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 建树 + 最大总 PnL（约 14 分钟）

| 语言 | 签名 |
|---|---|
| Java | `new DeskTree(int[] parent, long[] pnl)` · `long maxPnl()` |
| C++ | `DeskTree(std::vector<int> parent, std::vector<long long> pnl)` · `long long max_pnl() const`，命名空间 `desktree` |

- `parent[i]` 是台 `i` 的直接上级，根是 `-1`。**不保证 `parent[i] < i`，根也不一定是 0 号。** `n = 0` 是合法的空树。
- 建树时抛 `IllegalArgumentException`（C++ 抛 `std::invalid_argument`）的情况：两个数组长度不同、没有根、不止一个根、下标越界或自己当自己的上级、有环（从根走不到所有台）。
- `maxPnl()`：任何台和它的直接上级不能同时选，兄弟和隔代可以同时选；一个都不选是合法方案，所以答案不会是负数。
- 必须在 10^5 层的链上正常工作：不能递归。做法是建树时 BFS 出一个「父亲排在孩子前面」的顺序，DP 按这个顺序倒着扫。
- 例子：

```
          0 (1)
         /     \
     1 (4)     2 (-9)
     /   \      /   \
 3 (6)  4 (3) 5 (7)  6 (1)
```

`parent = [-1, 0, 0, 1, 1, 2, 2]`，`pnl = [1, 4, -9, 6, 3, 7, 1]`，`maxPnl() = 18`（选 0、3、4、5、6：1 + 6 + 3 + 7 + 1）。
`parent = [2, 2, -1]`、`pnl = [3, 4, 5]` 的根是 2 号，答案 7（选 0 号和 1 号，比只选根的 5 好）。
10 万个台、PnL 全是 1 的链，答案是 50000，不管链是 `parent[i] = i - 1` 还是 `parent[i] = i + 1`。

## Part 2 · 还原方案（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `List<Integer> plan()` |
| C++ | `std::vector<int> plan() const` |

- 返回一个最优方案选中的台号，**升序**，总和等于 `maxPnl()`。
- 最优方案可能不止一个，平局规则固定：台 `v` 被选，当且仅当它的直接上级没被选，并且 `take[v] > skip[v]`（严格大于）。相等就不选。
- 从根往下判断：根没有上级，所以根被选当且仅当 `take > skip`；根被选时它的孩子一律不选。
- 例子：样例树的 `plan() = [0, 3, 4, 5, 6]`。`parent = [-1, 0]`、`pnl = [5, 5]` 时 `take[0] = skip[0] = 5`，平局不选根，`plan() = [1]`。全负的树和空树，`plan()` 是空列表。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 最大路径和：路径可以先上后下，在某个台拐弯，怎么算？
2. 每个台作根时的答案各是多少（换根，rerooting）？
3. 恰好选 k 个台怎么改？
4. 树不是一次给齐，而是一行一行地来（孩子可能先于父亲到达），怎么办？
5. 不是「父子不能同选」，而是「选了一个台就必须选它的上级」，怎么改？
6. 不用显式的 BFS 顺序，还有什么办法避开递归爆栈？

## 边界

- 空树、单个台（正 / 负 / 0）、全负
- 父子 PnL 相等的平局
- `parent[i] > i`、根不是 0 号
- 10^5 层的两种链：根在 0 号和根在 n-1 号

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc16_tree_dp       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc16_tree_dp --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc16_tree_dp       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc16_tree_dp --tag part1
```
