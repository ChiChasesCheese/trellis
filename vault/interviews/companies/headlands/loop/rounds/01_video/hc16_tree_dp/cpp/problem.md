# hc16 · 交易台层级树上的 DP（C++20 版）

交易公司的台（desk）按上下级组成一棵树：一个根台，每个台最多一个直接上级，可以有任意多个下级。每个台有一个整数 PnL（当日盈亏，单位 tick，可以为负，用 `long long`，不用浮点数）。你要在这棵树上做动态规划：先求「不能同时选一个台和它的直接上级」时的最大总 PnL（树上的打家劫舍），再把选了哪些台还原出来，然后求最大路径和与最大子树和，最后面对一条 10^5 层的链：递归写法会栈溢出，必须改成迭代。C++ 版的额外考点是：栈溢出是信号、不是异常；`std::llabs(LLONG_MIN)` 是 UB；`size_t` 和 `int` 混着比较会出错。签名都在 `starter.hpp`（命名空间 `desk`）。

## 读题前你需要知道

- **树、根、父 / 子、叶子、子树**：树用**父数组**（`parent[i]` 是台 `i` 的直接上级，根台是 `-1`）或**边列表**（`n-1` 条无向边加一个指定的根）表示。**不保证 `parent[i] < i`**，根也不一定是 0 号。
- **动态规划**（DP）：把大问题拆成子问题，答案存起来只算一次。「每个台选或不选」是两个状态。
- **BFS 顺序**：按层走一棵树，父亲总排在孩子前面；把这个顺序倒着扫，就等于「先处理孩子，再处理父亲」。
- **调用栈**（call stack）：每层递归占一块栈空间，栈大小固定。C++ 里栈溢出是 `SIGSEGV`，进程直接死掉，`try/catch` 接不住，所以测试只能在子进程里观察它。
- **有符号溢出是 UB**：`std::llabs(LLONG_MIN)` 的结果放不进 `long long`，UBSan 会终止测试。检查范围要直接比较两端。

## 背景

- 台编号 `0..n-1`，`pnl[i]` 的范围是 `-10^12 .. 10^12`（含端点），`n ≤ 10^6`。任何选择和、子树和、路径和的绝对值都不超过 `10^6 × 10^12 = 10^18`，小于 `LLONG_MAX`，所以只要输入合法，所有查询都不会溢出。
- 「选一些台」允许一个都不选，所以答案不会是负数；空树和全负的树答案都是 0。

## 公共类型（starter 已给出）

```cpp
inline constexpr long long MAX_ABS_PNL = 1'000'000'000'000LL;
inline constexpr int MAX_DESKS = 1'000'000;

struct Plan {                       // 一个选择方案：total = 被选台的 PnL 之和；desks 升序
    long long total;
    std::vector<int> desks;
    friend bool operator==(const Plan&, const Plan&) = default;
};
struct Subtree {                    // 以 root 为根的子树的 PnL 总和
    int root;
    long long total;
    friend bool operator==(const Subtree&, const Subtree&) = default;
};
```

`size()` 和 `root()` 返回 `int`，空树的 `root()` 是 `-1`；用 `size_t` 的话 `-1` 会回绕成 `2^64 - 1`。

## Part 1 · 建树 + 最大总 PnL

| 签名 | 要求 |
|---|---|
| `static DeskTree of_parents(const std::vector<int>& parent, const std::vector<long long>& pnl)` | 校验并建树；入参会被拷贝，建树之后再改入参，树不受影响；`n = 0` 是合法的空树 |
| `int size() const` / `int root() const` | 台数；根台编号，空树是 `-1` |
| `long long max_pnl() const` | 任何一个台和它的直接上级不能同时被选（兄弟、隔代可以同时选）时的最大总 PnL |

`of_parents` 抛 `std::invalid_argument`，信息固定，**按这个顺序**检查：

| 顺序 | 条件 | `what()` |
|---|---|---|
| 1 | `parent.size() != pnl.size()` | `length mismatch` |
| 2 | 台数大于 `MAX_DESKS` | `too many desks` |
| 3 | 某个 `pnl` 超出 `±MAX_ABS_PNL` | `invalid pnl` |
| 4 | 某个 `parent[i]` 越界（不是 `-1` 又不在 `0..n-1`）或等于 `i` | `invalid parent` |
| 5 | `n > 0` 且 `-1` 的个数不是恰好 1 个 | `invalid root` |
| 6 | 根到不了所有台 | `cycle` |

- 样例：`parent = {-1, 0, 0, 1, 1, 2, 2}`，`pnl = {1, 4, -9, 6, 3, 7, 1}`（根 0 有孩子 1、2；1 有孩子 3、4；2 有孩子 5、6）。`size()` 是 `7`，`root()` 是 `0`，`max_pnl()` 是 `18`。
- 空树：`size() = 0`，`root() = -1`，`max_pnl() = 0`。单个台：`{7}` 得 `7`，`{-7}` 和 `{0}` 得 `0`。全负 `{-1, -2, -3, -4}`（`parent = {-1, 0, 1, 1}`）得 `0`。
- 父子不能同选：`parent = {-1, 0}`，`pnl = {3, 4}` 得 `4`；`{3, -4}` 得 `3`；链 `{5, 1, 5}` 得 `10`；链 `{3, 5, 3}` 得 `6`。兄弟可以同选：根带三个孩子，`{10, 4, 4, 4}` 得 `12`，`{13, 4, 4, 4}` 得 `13`。
- `parent[i] > i`：`parent = {2, 2, -1}`，`pnl = {5, 6, 1}` 得 `11`；`parent = {1, 2, 3, -1}`，`pnl = {4, 1, 4, 1}` 得 `8`。根不是 0 号：`parent = {1, -1, 1}`，`pnl = {1, 1, 1}` 的 `root()` 是 `1`，`max_pnl()` 是 `2`。
- 非法输入：`parent = {-1, 2, 1}` 抛 `cycle`；`{1, 0}` 抛 `invalid root`；`{-1, -1}` 抛 `invalid root`；`{-1, 5}`、`{-1, -2}`、`{-1, 1}` 抛 `invalid parent`；`{-1, 2, 3, 1, 0}` 抛 `cycle`。
- 顺序：`parent = {-1, 9}`、`pnl = {BOUND + 1}` 先报 `length mismatch`；`{-1, 9}` 配 `{1, BOUND + 1}` 先报 `invalid pnl`；`{-1, -1, 9}` 先报 `invalid parent`（不是 `invalid root`）；`{-1, -1, 1}` 报 `invalid root`；`MAX_DESKS + 1` 个台报 `too many desks`。
- `pnl = ±10^12` 合法（`{BOUND}` 得 `BOUND`，`{-BOUND}` 得 `0`）；`BOUND + 1`、`-BOUND - 1`、`LLONG_MIN`、`LLONG_MAX` 都抛 `invalid pnl`。
- 不溢出：10^6 个台的星形（根加 999999 个叶子），全部 `pnl = 10^12`，`max_pnl() = 999999 × 10^12`，`best_subtree().total = 10^6 × 10^12`，`max_path_sum() = 3 × 10^12`，`max_down_path() = 2 × 10^12`。
- C++ 专属测试：建好的 `DeskTree` 能拷贝、能移动，拷贝出来的和移动之后的新对象答案都一样；`pnl = LLONG_MIN` 和 `LLONG_MIN + 1` 要抛 `invalid pnl`，而不是触发 UB。

## Part 2 · 还原方案 + 边列表输入

| 签名 | 要求 |
|---|---|
| `Plan plan() const` | `total` 与 `max_pnl()` 相同，`desks` 是被选中的台，升序 |
| `static DeskTree of_edges(int n, const std::vector<std::vector<int>>& edges, const std::vector<long long>& pnl, int root)` | `edges[i] = {a, b}` 是一条无向边，以 `root` 为根定向（离根近的一端是上级）；`n = 0` 时 `root` 被忽略 |

**平局规则**（最优方案不唯一，这条规则固定输出）：台 `v` 被选，当且仅当它的直接上级**没被选**，并且「`v` 的子树里选 `v` 时的最大值」**严格大于**「不选 `v` 时的最大值」。相等就不选。根没有上级，所以根被选当且仅当选它严格更好。

`of_edges` 的检查顺序和 `what()`：

| 顺序 | 条件 | `what()` |
|---|---|---|
| 1 | `n < 0` 或 `pnl.size() != n` | `length mismatch` |
| 2–3 | 台数过多 / `pnl` 越界 | `too many desks` / `invalid pnl` |
| 4 | `n > 0` 且 `root` 不在 `0..n-1` | `invalid root` |
| 5 | 某条边不是两个端点、端点越界、或 `a == b` | `invalid edge` |
| 6 | 边数不是 `max(0, n-1)`，或从 `root` 到不了所有台（重复边、环、多个连通块） | `not a tree` |

- 样例的 `plan()` 是 `Plan{18, {0, 3, 4, 5, 6}}`：根 `18 > 17` 被选，台 1、2 不选，台 3、4、5、6 各自「选更好」而被选（1 + 6 + 3 + 7 + 1 = 18）。
- 平局：`parent = {-1, 0}`，`pnl = {5, 5}` 得 `Plan{5, {1}}`；`parent = {-1, 0, 0}`，`pnl = {6, 3, 3}` 得 `Plan{6, {1, 2}}`；`parent = {-1, 0, 1}`，`pnl = {3, 5, 3}` 得 `Plan{6, {0, 2}}`；`parent = {-1, 0, 1, 2}`，`pnl = {1, 5, 1, 5}` 得 `Plan{10, {1, 3}}`。
- 空树、全负、全 0 的树，方案都是 `Plan{0, {}}`。PnL 为 0 的台永远不会被选：`parent = {-1, 0, 1}`，`pnl = {0, 4, 0}` 得 `Plan{4, {1}}`。
- 边列表 `{{3,1},{0,2},{1,0},{4,1},{2,5},{6,2}}`，`n = 7`，`root = 0`，`pnl` 同样例：`root()` 是 `0`，`max_pnl()` 是 `18`，`plan()` 与父数组版相同。边的顺序、两个端点的先后都不影响结果。
- 换根：同一棵无向树以 `6` 为根，`root()` 是 `6`，`max_pnl()` 仍是 `18`，`max_path_sum()` 仍是 `13`；而 `plan()` 的平局和 `best_subtree()` 依赖根，会变。
- 小规模：`of_edges(0, {}, {}, 0)` 是空树；`of_edges(0, {}, {}, 99)` 也行（`root` 被忽略）；`of_edges(1, {}, {9}, 0).plan()` 是 `Plan{9, {0}}`；`of_edges(2, {{1, 0}}, {5, 5}, 1).plan()` 是 `Plan{5, {0}}`。
- 错误例子（`pnl = {1, 2, 3}`，`n = 3`）：`root = 3` 或 `-1` 抛 `invalid root`；边 `{1, 3}`、`{1, 1}`、`{1}`（只有一个端点）、`{1, 2, 0}`（三个端点）、`{}`、`{0, -1}` 抛 `invalid edge`；只有一条边 `{0, 1}`、`{{0,1},{1,2},{2,0}}`（三条边）、`{{0,1},{1,0}}`（重复边）抛 `not a tree`；`n = 4`、边 `{{0,1},{1,0},{2,3}}` 抛 `not a tree`；`n = 0` 却有边 `{0, 1}` 抛 `invalid edge`。

## Part 3 · 路径与子树

空树上三个方法都抛 `std::out_of_range`，`what()` 是 `empty tree`。

| 签名 | 要求 |
|---|---|
| `long long max_down_path() const` | 从某个台出发、每一步走到一个孩子的**非空**路径，最大 PnL 和（单个台也算） |
| `long long max_path_sum() const` | 树中任意一条**非空简单路径**的最大 PnL 和，可以先往上再往下，在某个台**拐弯** |
| `Subtree best_subtree() const` | 子树 PnL 总和最大的台；总和相同取**编号最小**的台 |

- 样例：`max_down_path()` 是 `11`（0 → 1 → 3），`max_path_sum()` 是 `13`（3 → 1 → 4，在 1 号拐弯），`best_subtree()` 是 `Subtree{0, 13}`（根和 1 号都是 13，取小编号）。
- 单个台 `{-4}`：三个方法都是 `-4`，`best_subtree()` 是 `Subtree{0, -4}`。路径不能为空，所以全负时答案是最不坏的单个台（可能为负）：`parent = {-1, 0, 1}`，`pnl = {-5, -3, -8}` 得 `max_down_path() = -3`，`max_path_sum() = -3`，`best_subtree() = Subtree{2, -8}`。
- 拐点本身为负也可能赢：根带两个孩子，`pnl = {-1, 6, 7}` 得 `max_path_sum() = 12`，`max_down_path() = 7`；`pnl = {-10, 6, 7}` 得 `max_path_sum() = 7`（不拐弯更好）。
- 拐弯只用最好的两条支路：根带四个孩子，`pnl = {1, 5, 9, 7, -2}` 得 `max_path_sum() = 17`（9 + 1 + 7），`max_down_path() = 10`。
- 子树和平局取小编号：`parent = {-1, 0, 0}`，`pnl = {-20, 5, 5}` 得 `Subtree{1, 5}`；`parent = {3, 3, 3, -1}`，`pnl = {2, 2, 2, -6}` 得 `Subtree{0, 2}`；`parent = {-1, 0}`，`pnl = {4, 0}` 得 `Subtree{0, 4}`。
- 所有结果都和朴素的暴力解对拍（随机小树，标签打乱，含 `pnl` 为负的情况）。

## Part 4 · 10^5 层的链：不能递归

| 签名 | 要求 |
|---|---|
| `long long max_pnl_recursive() const` | 教科书递归版，答案必须与 `max_pnl()` 一样；在 512 KiB 的线程栈上遇到 10^5 层的链会让进程崩溃 |

**其余所有方法**（`max_pnl`、`plan`、`max_down_path`、`max_path_sum`、`best_subtree`，以及 `of_parents` / `of_edges` 本身）都必须在 10^5 层的链上、512 KiB 的线程栈里正常工作。starter 给的提示：建树时用 BFS 得到一个「父亲在孩子前面」的顺序，所有查询都按它倒着扫；`parent[i]` 可以大于 `i`，所以不能简单地从 `n-1` 倒着扫父数组。

- 链 `parent[i] = i - 1`（根是 0），10^5 个台、`pnl` 全是 1：`max_pnl()` 是 `50000`；`plan().desks` 是奇数编号 `1, 3, 5, ..., 99999`（偶数个台时根的「选」与「不选」平局，不选）；`max_down_path()` 和 `max_path_sum()` 是 `100000`；`best_subtree()` 是 `Subtree{0, 100000}`。
- 反向链 `parent[i] = i + 1`（根是 `n - 1`，编号顺序和层次顺序相反）：`root()` 是 `99999`，`max_pnl()` 是 `50000`，`plan().desks` 是偶数编号 `0, 2, ..., 99998`，`best_subtree()` 是 `Subtree{99999, 100000}`。
- 同一条反向链用边列表 `{i+1, i}` 输入，`root = 99999`，结果相同。
- 交替正负的链 `+3, -1, +3, -1, ...`（10^5 个台）：`max_pnl()` 是 `150000`，`max_down_path()` 和 `max_path_sum()` 是 `100001`，`best_subtree()` 是 `Subtree{0, 100000}`。
- 宽树：根（`pnl = 150000`）带 `99999` 个孩子（`pnl = 2`）：`max_pnl()` 是 `2 × 99999`，`max_path_sum()` 是 `150004`，`max_down_path()` 是 `150002`，`plan().desks` 是 `1..99999`。
- 递归版在小树上与迭代版一致（样例得 `18`，空树得 `0`，随机小树对拍）。在一个 512 KiB 栈的子进程里对 10^5 层的链调用 `max_pnl_recursive()`，子进程必须崩溃；同样的栈上迭代版返回 `50000`；100 层的浅链上递归版返回 `50`。
- 规模：10^6 个台、随机的深树（每个台的父亲取自它前面最近的 4 个），建树 + `max_pnl` + `plan` + `max_path_sum` + `max_down_path` + `best_subtree` 要在 2 秒内。10^6 层的链在 512 KiB 栈里建树、`plan`、`max_path_sum`、`max_pnl` 也要在 2 秒内。

## 边界清单

- 空树（所有方法）；单个台（正 / 负 / 0）；全负；父子相等的平局；兄弟同时被选；PnL 为 0 的台
- `parent[i] > i`；根不是 0 号；`pnl = ±10^12` 的边界；`LLONG_MIN`（`llabs` 陷阱）；10^6 个台的星形不溢出
- 所有检查的先后顺序；入参被拷贝；建好的树能拷贝、能移动
- 边列表：重复边、环、非连通、自环、端点越界、边只有一个或三个端点、换根
- 全负时最大路径是单个台；拐点本身为负；拐弯用最好的**两条**支路；子树和平局取小编号
- 10^5 层的两种方向的链、交替正负的链、10^5 个孩子的宽树；`max_pnl_recursive` 在浅链上正确、深链上崩溃

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc16_tree_dp          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc16_tree_dp --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc16_tree_dp --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc16_tree_dp                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。`max_pnl_recursive` 的栈溢出测试在子进程里跑，所以主进程不会被杀掉。

## 相关变体

- 树以逐行流的形式到达（先到孩子后到父亲，或边乱序）：先收齐再建 BFS 顺序，不能假设父亲先出现。
- 每个台有成本、要恰好选 k 个台：状态里多一维 `dp[v][j]`，复杂度 O(n·k)。
- 「选了 v 就必须选它的上级」（最大权闭合子图）：`take[v] = pnl[v] + Σ max(0, take[孩子])`，另一类 DP。
- 树上直径、最近公共祖先、换根 DP：同一套「BFS 顺序倒扫 + 正扫」。
