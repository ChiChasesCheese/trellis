# hc16 · Tree DP on a Desk Hierarchy（C++20 版）

> 读者：会写 C++ 基础语法（`vector`、循环、函数），其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。下面所有代码块按顺序拼起来就是一份能编译、能通过全部测试的完整实现（文件 `reference.hpp`）。

## 1. 题目

### 1.1 台树

交易公司的台（desk）按上下级排成一棵**树**（tree）：一个根台（root），每个台最多一个直接上级（parent），可以有任意多个下级（child）。每个台有一个整数 PnL（当日盈亏，单位 tick，可以为负，用 `long long`，不用浮点数）。

* 台编号 `0..n-1`。树用**父数组**（parent array）给出：`parent[i]` 是 `i` 的上级，根是 `-1`。**不保证 `parent[i] < i`**，根也不一定是 0。
* 另一种输入是**边列表**（edge list）：`n-1` 条无向边加一个指定的根，要自己定向。
* `|pnl| ≤ 10^12`，`n ≤ 10^6`：任何和的绝对值 ≤ `10^18`，小于 `LLONG_MAX ≈ 9.22×10^18`，**所有查询都不会溢出**。越界输入在建树时拒绝。
* 「选一些台」允许一个都不选，所以答案不为负；空树和全负的树答案是 0。

### 1.2 四个 Part

| Part | 内容 |
|---|---|
| 1 | `DeskTree::of_parents` 校验并建树；`max_pnl()`：任何一个台和它的直接上级不同时被选的最大总 PnL（树上的打家劫舍） |
| 2 | `of_edges`（无向边列表，定向）；`plan()`：还原选了哪些台，平局规则固定 |
| 3 | `max_down_path()`、`max_path_sum()`（可拐弯）、`best_subtree()`（平局取小编号） |
| 4 | 全部方法在 10^5 层的链上、512 KiB 栈里不爆栈；`max_pnl_recursive()` 是教科书递归版，用来亲眼看它崩 |

### 1.3 样例

```
          0 (1)
         /     \
     1 (4)     2 (-9)
     /   \      /   \
 3 (6)  4 (3) 5 (7)  6 (1)
```

`parent = {-1, 0, 0, 1, 1, 2, 2}`，`pnl = {1, 4, -9, 6, 3, 7, 1}`。每个台算两个数：`take` = 选它时它的子树里的最大值，`skip` = 不选它时的最大值。

| 台 | take | skip |
|---|---|---|
| 3、4、5、6（叶子） | 6、3、7、1 | 0、0、0、0 |
| 1 | 4 | 6 + 3 = 9 |
| 2 | -9 | 7 + 1 = 8 |
| 0 | 1 + 9 + 8 = 18（孩子 1、2 不选，用它们的 skip） | max(4, 9) + max(-9, 8) = 17 |

* `max_pnl() = 18`。
* `plan() = {18, {0, 3, 4, 5, 6}}`：根 `18 > 17` 选；根被选，1、2 不选；3、4、5、6 各自 `take > skip` 选。
* `max_down_path() = 11`（0 → 1 → 3），`max_path_sum() = 13`（3 → 1 → 4，在 1 号拐弯：6 + 4 + 3），`best_subtree() = {0, 13}`（根和 1 号都是 13，取小编号）。
* 平局例：`parent = {-1, 0}`、`pnl = {5, 5}`：`take[0] = skip[0] = 5`，相等不选根，`plan() = {5, {1}}`。

## 2. 数据结构选型

| 需求 | 选择 | 原因 |
|---|---|---|
| 存树 | `parent` 数组 + **CSR**（`child_start_`、`child_list_` 两个 `vector<int>`） | `vector<vector<int>>` 要分配 n 个小 vector，10^6 个台时慢且碎；CSR 只有两块连续内存 |
| 处理顺序 | **BFS 顺序** `order_`（父亲排在孩子前面）倒着扫 | 孩子先于父亲，不用递归；`parent[i] < i` 不成立也没关系 |
| DP 状态 | 两个 `vector<long long>`（`in`/`out`）；结果「推给父亲」 | 只需要 `parent[]`，不需要孩子列表 |
| 选中标记 | `vector<char>`，不用 `vector<bool>` | `vector<bool>` 是位压缩的代理类型，取引用、并行写都有坑 |

**CSR**（compressed sparse row）怎么建：先数每个节点有几个孩子，做前缀和得到每个节点孩子区间的起点，再扫一遍把孩子填进去。

v 的孩子在 `child_list_` 里的下标范围是 `child_start_[v] .. child_start_[v+1]-1`。

**BFS 顺序倒扫**为什么对：BFS 从根出发，先访问根，再访问根的孩子，再访问孩子的孩子，一个节点总是在它的父亲**之后**入队；于是 `order_` 里每个节点都排在它所有孩子**前面**。倒着扫，就是「先处理孩子，再处理父亲」，正好是 DP 的依赖方向。

**为什么不能从 `n-1` 倒着扫 `parent[]`**：那等于假设 `parent[i] < i`。反向链 `parent = {1, 2, 3, -1}` 里 0 的父是 1，处理 1 的时候 0 的结果还没推上来。

## 3. 类型

```cpp
// hc16 · Tree DP on a desk hierarchy — C++20 reference.  Statement: ../problem.md (Java: reference/DeskTree.java).
// Build once: validate, CSR child lists, a BFS order (parents before children).  Every query is a loop over that order
// in reverse (children before parents), so the stack depth is O(1).  Only max_pnl_recursive() recurses, on purpose.
#pragma once

#include <algorithm>
#include <climits>
#include <cstddef>
#include <stdexcept>
#include <utility>
#include <vector>

namespace desk {

/// |pnl| limit: every subtree sum / path sum / selection sum stays <= 10^6 * 10^12 = 10^18 < LLONG_MAX, so nothing overflows.
inline constexpr long long MAX_ABS_PNL = 1'000'000'000'000LL;
inline constexpr int MAX_DESKS = 1'000'000;

/// A selection: total = sum of the chosen desks' PnL; desks ascending.
struct Plan {
    long long total;
    std::vector<int> desks;
    friend bool operator==(const Plan&, const Plan&) = default;
};
/// Subtree summary: total PnL of the subtree rooted at `root`.
struct Subtree {
    int root;
    long long total;
    friend bool operator==(const Subtree&, const Subtree&) = default;
};
```

* `Plan` / `Subtree` 用 C++20 的 `friend bool operator==(...) = default;`：逐成员比较，测试里直接 `CHECK_EQ(plan, Plan{18, {0, 3, 4, 5, 6}})`。
* `MAX_ABS_PNL` 和 `MAX_DESKS` 是接口的一部分；`inline constexpr` 变量放在头文件里不会重复定义。
* 台数、编号用 `int`（`-1` 表示「没有」，用 `size_t` 会回绕成 2^64-1）；和 `vector::size()` 比较时用 `static_cast<std::size_t>`，不要让有符号数隐式转无符号。

## 4. 建树：`of_parents` 与 `of_edges`

### 4.1 父数组入口（Part 1）

```cpp
class DeskTree {
public:
    /// parent[i] = superior of desk i, -1 = root; n = 0 is a valid empty tree.  Indices need not be smaller than i.
    /// Throws std::invalid_argument, checked in this order: "length mismatch", "too many desks", "invalid pnl",
    /// "invalid parent" (out of range or self), "invalid root" (n > 0 and not exactly one -1), "cycle".
    static DeskTree of_parents(const std::vector<int>& parent, const std::vector<long long>& pnl) {
        if (parent.size() != pnl.size()) throw std::invalid_argument("length mismatch");
        check_pnl(pnl);
        const int n = static_cast<int>(parent.size());
        int root = -1, roots = 0;
        for (int i = 0; i < n; ++i) {
            int p = parent[i];
            if (p == -1) {
                ++roots;
                root = i;
            } else if (p < 0 || p >= n || p == i) {
                throw std::invalid_argument("invalid parent");
            }
        }
        if (n > 0 && roots != 1) throw std::invalid_argument("invalid root");
        return DeskTree(parent, pnl, root);
    }
```

* 检查顺序固定：长度 → 台数 → pnl 范围（在 `check_pnl` 里）→ parent 越界或自指 → 根的个数 → 有环（在构造函数里）。测试靠这个顺序确定该报哪个错。
* 所有错误都是 `std::invalid_argument`，信息固定；`what()` 返回的字符串是接口的一部分。
* `parent[i] == -1` 要先判，因为 `-1` 同时也满足「`p < 0`」。
* 入参是 `const std::vector<…>&`，构造函数按值接收再 `std::move`：调用方之后改数组，树不受影响。

### 4.2 边列表入口（Part 2）

```cpp
    /// edges[i] = {a, b}: an undirected edge; the tree is oriented away from `root` (ignored when n = 0).
    /// Order: "length mismatch" (n < 0 or pnl.size() != n), "too many desks", "invalid pnl", "invalid root" (n > 0),
    /// "invalid edge" (not two endpoints / out of range / self-loop), "not a tree" (edge count != max(0, n-1) or not
    /// every desk reachable from root).
    static DeskTree of_edges(int n, const std::vector<std::vector<int>>& edges, const std::vector<long long>& pnl, int root) {
        if (n < 0 || pnl.size() != static_cast<std::size_t>(n)) throw std::invalid_argument("length mismatch");
        check_pnl(pnl);
        if (n > 0 && (root < 0 || root >= n)) throw std::invalid_argument("invalid root");
        for (const auto& e : edges) {
            if (e.size() != 2 || e[0] < 0 || e[0] >= n || e[1] < 0 || e[1] >= n || e[0] == e[1]) throw std::invalid_argument("invalid edge");
        }
        if (edges.size() != static_cast<std::size_t>(std::max(0, n - 1))) throw std::invalid_argument("not a tree");
        if (n == 0) return DeskTree({}, {}, -1);
        std::vector<int> start(n + 1, 0);
        for (const auto& e : edges) {
            ++start[e[0] + 1];
            ++start[e[1] + 1];
        }
        for (int v = 0; v < n; ++v) start[v + 1] += start[v];
        std::vector<int> adj(2 * edges.size());
        std::vector<int> fill(start.begin(), start.end() - 1);
        for (const auto& e : edges) {
            adj[fill[e[0]]++] = e[1];
            adj[fill[e[1]]++] = e[0];
        }
        std::vector<int> parent(n, -2), queue;
        queue.reserve(n);
        parent[root] = -1;
        queue.push_back(root);
        for (std::size_t head = 0; head < queue.size(); ++head) {
            int v = queue[head];
            for (int i = start[v]; i < start[v + 1]; ++i) {
                int w = adj[i];
                if (parent[w] == -2) {
                    parent[w] = v;
                    queue.push_back(w);
                }
            }
        }
        if (queue.size() != static_cast<std::size_t>(n)) throw std::invalid_argument("not a tree");
        return DeskTree(std::move(parent), pnl, root);
    }

    int size() const { return n_; }
    /// Root desk; -1 for the empty tree.
    int root() const { return root_; }
```

* 无向边在邻接 CSR 里存**两次**（`adj` 大小 `2 * edges.size()`）。
* `parent` 初值 `-2` 表示「还没访问」，根设 `-1`；BFS 时 `parent[w] == -2` 才认 w 为孩子。
* 校验顺序见注释：先看每条边本身是否合法（两个端点、范围、非自环）→ 再数边数 → 最后 BFS 数访问数。重复边会让 `n-1` 条边凑不出连通图，BFS 访问数不足，报 `"not a tree"`。
* `n == 0` 时 `root` 被忽略；`DeskTree({}, {}, -1)` 构造空树。
* 同一棵无向树，换根之后最大独立集和最大路径和不变，`plan()` 的平局与 `best_subtree()` 会变。

## 5. 查询：最大总 PnL 与方案

### 5.1 Part 1：`max_pnl()`

```cpp
    // ---------------- Part 1 ----------------

    /// Best total when no desk and its direct superior are both chosen.  Choosing nothing is allowed (empty / all-negative: 0).
    long long max_pnl() const {
        std::vector<long long> in, out;
        return solve_robber(in, out);
    }
```

核心是 `solve_robber`（第 8 节的代码）：

```
in[v]  初值 pnl[v]        （选 v）
out[v] 初值 0             （不选 v）
倒扫 order_：
    p = parent[v]
    in[p]  += out[v]                  父选：孩子只能不选
    out[p] += max(in[v], out[v])      父不选：孩子随便
答案 = max(in[root], out[root])，空树 0
```

状态定义是关键：`in[v]` / `out[v]` 只依赖 v 的**子树**，所以必须先算孩子。

### 5.2 Part 2：`plan()`

```cpp
    // ---------------- Part 2 ----------------

    /// Same value plus the chosen desks.  Tie rule: v is chosen iff its superior is not chosen and
    /// in[v] > out[v] (strictly better); equal means skip.  Desks ascending.
    Plan plan() const {
        std::vector<long long> in, out;
        long long total = solve_robber(in, out);
        std::vector<char> chosen(n_, 0);
        for (int v : order_) {
            int p = parent_[v];
            chosen[v] = (p < 0 || !chosen[p]) && in[v] > out[v];
        }
        Plan plan{total, {}};
        for (int v = 0; v < n_; ++v)
            if (chosen[v]) plan.desks.push_back(v);
        return plan;
    }
```

* 平局规则：`chosen[v] = (根 或 父没被选) && in[v] > out[v]`，**严格大于**才选；相等就不选。它只依赖 DP 值，所以自顶向下一遍就能还原，不用回溯。PnL 为 0 的台永远不被选；全负的树方案是 `{0, {}}`。
* `order_` 正着扫保证处理 v 时它的父亲已经定了。
* 最后按编号升序收集（`for v in 0..n-1`），所以 `desks` 天然升序。
* 全是 1 的链：偶数个台时方案是**奇数编号**：根的 `take == skip`，不选；下一个台选，再下一个被迫不选……

## 6. Part 3：路径与子树

```cpp
    // ---------------- Part 3 (empty tree: std::out_of_range("empty tree")) ----------------

    /// Best non-empty downward path (each step goes to a child).
    long long max_down_path() const {
        require_non_empty();
        return paths().first;
    }
    /// Best non-empty simple path anywhere (may go up then down, bending at one desk).
    long long max_path_sum() const {
        require_non_empty();
        return paths().second;
    }
    /// Desk whose subtree total is largest; ties go to the smallest id.
    Subtree best_subtree() const {
        require_non_empty();
        std::vector<long long> sum = pnl_;
        for (int i = n_ - 1; i > 0; --i) {
            int v = order_[i];
            sum[parent_[v]] += sum[v];
        }
        int best = 0;
        for (int v = 1; v < n_; ++v)
            if (sum[v] > sum[best]) best = v;
        return {best, sum[best]};
    }
```

* `down[v] = pnl[v] + max(0, 最好的孩子 down)`：负的支路不要。`top1[v]`、`top2[v]` 是 v 的孩子里最好的两条**非负** `down`，初值 0，天然实现「负的不要」。
* 拐弯路径在 v 处：`pnl[v] + top1[v] + top2[v]`。往上传给父亲的只能是**一条**支路 `down`，所以只在 `down > 0` 时更新父亲的 `top1/top2`。
* 路径不能为空：全是负数时答案是最大的单个台（可能为负数），所以 `best_down` / `best_path` 初值是 `LLONG_MIN`，不是 0。
* `best_subtree`：`sum` 倒扫累加，再按编号升序、**严格大于**才更新，平局取小编号。
* 空树抛 `std::out_of_range("empty tree")`（Java 版是 `NoSuchElementException`）。

## 7. Part 4：10^5 层的链

面试官：「如果这棵树是一条 10 万层的链呢？」所有查询已经是对 `order_` 的循环，没有递归，栈深度 O(1)。唯一的递归是留作对照的教科书版：

```cpp
    // ---------------- Part 4 ----------------

    /// Textbook recursion; same answer as max_pnl().  Overflows the stack on a deep chain — kept to show why.
    long long max_pnl_recursive() const {
        if (n_ == 0) return 0;
        auto [take, skip] = solve_recursive(root_);
        return std::max(take, skip);
    }
```

它的答案和 `max_pnl()` 一样，但深链上会崩（实现见第 8 节的 `solve_recursive`）。

### 7.1 为什么递归会崩

每次函数调用在**调用栈**（call stack）上压一个**栈帧**（stack frame）：返回地址、参数、局部变量、保存的寄存器。递归就是同一个函数的栈帧一层叠一层。栈的大小固定：

* macOS / Linux 的主线程默认 8 MiB（`ulimit -s`）；自己创建的线程更小（macOS 上 512 KiB）。
* 这个递归每层约 48–100 字节（`-O2`），10^5 层 ≈ 5–10 MB；在 sanitizer 构建里每帧更大（ASan 加红区），更容易崩。

C++ 没有 `StackOverflowError`：栈尽头是一页**保护页**（guard page），碰到它操作系统发 `SIGSEGV`，进程直接终止——没有异常可以 `catch`。把栈调大（`ulimit -s`、`pthread_attr_setstacksize`）只是推迟问题，链再长一个数量级还会崩。**根治**：把调用栈换成自己的数组——这就是 BFS 顺序倒扫。

### 7.2 怎么测栈溢出

* `mt::run_on_stack(512 * 1024, fn)`：在一个只有 512 KiB 栈的线程里运行 `fn`（`std::thread` 不能指定栈大小，底层用 `pthread_attr_setstacksize`）。迭代版的方法必须在里面正常跑完 10^5 层的链。
* `mt::child_survives(fn)`：`fork` 出子进程跑 `fn`，返回子进程是不是正常结束。栈溢出是信号不是异常，只能从**另一个进程**观察到：递归版在子进程里崩溃，返回 `false`。

### 7.3 规模

10^6 个台的随机深树：建树 + `max_pnl` + `plan` + 路径 + 子树，`-O2` 下约 50 ms。10^6 层的链在 512 KiB 栈里也只要十几毫秒。

## 8. 内部实现

上面各方法用到的私有部分。

### 8.1 成员与构造

```cpp
private:
    int n_;
    int root_;
    std::vector<long long> pnl_;
    std::vector<int> parent_;
    std::vector<int> order_;        // BFS order: a parent always precedes its children
    std::vector<int> child_start_;  // CSR: children of v are child_list_[child_start_[v] .. child_start_[v+1])
    std::vector<int> child_list_;

    DeskTree(std::vector<int> parent, std::vector<long long> pnl, int root)
        : n_(static_cast<int>(parent.size())), root_(root), pnl_(std::move(pnl)), parent_(std::move(parent)),
          child_start_(n_ + 1, 0), child_list_(std::max(0, n_ - 1)) {
        for (int v = 0; v < n_; ++v)
            if (parent_[v] >= 0) ++child_start_[parent_[v] + 1];
        for (int v = 0; v < n_; ++v) child_start_[v + 1] += child_start_[v];
        std::vector<int> fill(child_start_.begin(), child_start_.end() - 1);
        for (int v = 0; v < n_; ++v)
            if (parent_[v] >= 0) child_list_[fill[parent_[v]]++] = v;
        if (n_ > 0) {
            order_.reserve(n_);
            order_.push_back(root_);
            for (std::size_t head = 0; head < order_.size(); ++head) {
                int v = order_[head];
                for (int i = child_start_[v]; i < child_start_[v + 1]; ++i) order_.push_back(child_list_[i]);
            }
            if (order_.size() != static_cast<std::size_t>(n_)) throw std::invalid_argument("cycle");
        }
    }
```

* 构造函数是 `private`：只能经 `of_parents` / `of_edges` 创建，保证对象一旦存在就是合法的树（类不变式，class invariant）。
* 三步 CSR：数孩子 → 前缀和 → 用 `fill` 副本记当前写到哪、填进去。`child_list_` 的大小是 `max(0, n-1)`，因为 n 个节点的树恰有 n-1 个「非根」节点。
* BFS 把 `order_` 当队列用（`push_back` + 一个读下标 `head`）；最后 `order_.size() != n_` 说明有些台从根够不着，也就是有环，抛 `"cycle"`。
* 初始化列表的顺序要和成员**声明顺序**一致（否则 `-Wreorder`，`-Werror` 下是编译错误）。

### 8.2 校验与 `solve_robber`

```cpp
    static void check_pnl(const std::vector<long long>& pnl) {
        if (pnl.size() > static_cast<std::size_t>(MAX_DESKS)) throw std::invalid_argument("too many desks");
        for (long long p : pnl)
            if (p > MAX_ABS_PNL || p < -MAX_ABS_PNL) throw std::invalid_argument("invalid pnl");  // no llabs: llabs(LLONG_MIN) is UB
    }

    void require_non_empty() const {
        if (n_ == 0) throw std::out_of_range("empty tree");
    }
```

* 范围检查写 `p > MAX_ABS_PNL || p < -MAX_ABS_PNL`，**不要**写 `std::llabs(p) > MAX_ABS_PNL`：`llabs(LLONG_MIN)` 会溢出，是**未定义行为**（undefined behavior，UB）；测试在 UBSan 下跑，会直接终止。

```cpp
    /// in[v] / out[v]: best total inside v's subtree with v chosen / not chosen.  Returns the root's max, 0 for the empty tree.
    long long solve_robber(std::vector<long long>& in, std::vector<long long>& out) const {
        in = pnl_;
        out.assign(n_, 0);
        for (int i = n_ - 1; i >= 0; --i) {
            int v = order_[i];
            int p = parent_[v];
            if (p >= 0) {
                in[p] += out[v];
                out[p] += std::max(in[v], out[v]);
            }
        }
        return n_ == 0 ? 0 : std::max(in[root_], out[root_]);
    }
```

### 8.3 `paths` 与 `solve_recursive`

```cpp
    /// {best downward path, best path}; top1 / top2 = the two best child downward paths, negatives count as 0 (not taken).
    std::pair<long long, long long> paths() const {
        std::vector<long long> top1(n_, 0), top2(n_, 0);
        long long best_down = LLONG_MIN, best_path = LLONG_MIN;
        for (int i = n_ - 1; i >= 0; --i) {
            int v = order_[i];
            long long down = pnl_[v] + top1[v];
            best_down = std::max(best_down, down);
            best_path = std::max(best_path, pnl_[v] + top1[v] + top2[v]);
            int p = parent_[v];
            if (p >= 0 && down > 0) {
                if (down > top1[p]) {
                    top2[p] = top1[p];
                    top1[p] = down;
                } else if (down > top2[p]) {
                    top2[p] = down;
                }
            }
        }
        return {best_down, best_path};
    }
```

```cpp
    std::pair<long long, long long> solve_recursive(int v) const {
        long long take = pnl_[v], skip = 0;
        for (int i = child_start_[v]; i < child_start_[v + 1]; ++i) {
            auto [ct, cs] = solve_recursive(child_list_[i]);
            take += cs;
            skip += std::max(ct, cs);
        }
        return {take, skip};
    }
};

}  // namespace desk
```

## 9. 和 Java 版的区别

| 点 | Java | C++20 |
|---|---|---|
| 返回方案 | `record Plan(long total, List<Integer> desks)`，紧凑构造器 `List.copyOf` | `struct Plan`，`operator== = default`；成员是普通 `vector`，调用方拿到的是副本 |
| 入参拷贝 | `parent.clone()` | 按值接收 + `std::move`（或直接从 `const&` 拷贝） |
| 非法输入 | `IllegalArgumentException`；`null` → NPE | `std::invalid_argument`；没有 `null` 引用，不需要 NPE 用例 |
| 空树的路径查询 | `NoSuchElementException` | `std::out_of_range` |
| 校验 `pnl` | `p > MAX \|\| p < -MAX`（`Math.abs(Long.MIN_VALUE)` 是负数的坑） | 同样不用 `llabs`：`llabs(LLONG_MIN)` 是 UB |
| 栈溢出 | 抛 `StackOverflowError`，可以断言 | 进程被信号杀死，必须用子进程观察 |
| 选中标记 | `boolean[]` | `vector<char>`（避开 `vector<bool>`） |
| 整数比较 | 无符号问题不存在 | `vector::size()` 是无符号，和 `int` 比较要显式转换 |
| 拷贝 / 移动 | 引用语义，没有这个问题 | `DeskTree` 全是 `vector` 成员，默认拷贝 / 移动都正确 |

## 10. 陷阱

1. 从 `n-1` 倒着扫 `parent[]`，`parent[i] > i` 时全错；要用 BFS 顺序。
2. 选 v 时加了 `max(in, out)`；应该只加孩子的 `out`。
3. 全负的树答案写成负数；`plan()` 在全负树上不是 `{0, {}}`；平局取了「选」。
4. 最大路径把负支路也加上；拐弯只用一条支路；全负时返回 0。
5. `bestSubtree` 平局取大编号（用了 `>=` 或倒着扫）。
6. `std::llabs(p) > MAX_ABS_PNL`：`LLONG_MIN` 是 UB。
7. `pnl.size() != n` 之类的比较：`size_t` 和 `int` 混比，`n < 0` 转成巨大的无符号数。
8. 校验顺序错：先报了 pnl 越界而不是长度不等；根的个数检查放在环检查之后。
9. 边列表：只数边数不数访问数（重复边、环）；`n == 0` 时仍检查 `root`。
10. 初始化列表顺序和成员声明顺序不一致（`-Wreorder`）。
11. `vector<vector<int>>` 存 10^6 个节点的孩子：10^6 次小分配，慢且占内存；用 CSR。
12. 以为把栈调大就解决了深链：只是推迟；链再长 10 倍仍然崩。

## 11. 面试官会追问什么（senior）

**Q1. 为什么 BFS 顺序倒扫而不是 DFS 后序？** 两者都保证孩子先于父亲。BFS 顺序只要一个数组加一个下标；DFS 后序要自己维护显式栈和「孩子处理完没有」的状态。

**Q2. 为什么 `take[v]` 里加的是孩子的 `skip`？** 选了 v，直接下级不能选；孙辈可以选，已经包含在孩子的 `skip` 里。

**Q3. 平局规则为什么重要？** 最优方案不唯一，没有规则时调用方没法比较输出。规则要局部可判定（`in > out`），只靠 DP 值自顶向下还原，不用回溯。

**Q4. 溢出怎么论证？** 入口限制 `|pnl| ≤ 10^12`、`n ≤ 10^6`，任何和 ≤ 10^18 < 9.22×10^18。要支持任意 `long long`：用 `__builtin_add_overflow` 并规定「真实答案超出范围才报错」（对非负累加可证明中间值溢出当且仅当最终答案溢出），或者 `__int128`。

**Q5. 栈溢出为什么是崩溃而不是异常？** 栈尽头的保护页被访问，硬件触发缺页，操作系统发 `SIGSEGV`；此时栈已经用完，连运行 `catch` 的空间都没有。可以用 `sigaltstack` 在备用栈上处理信号，但也只能打日志后退出，不能恢复。

**Q6. 为什么用 CSR 而不是 `vector<vector<int>>`？** 内存连续、两次分配；缓存友好；建树是计数排序，O(n)。

**Q7. 流式地一个个加台怎么办？** 只追加叶子：影响祖先链，重算 `take/skip`，最坏 O(深度)；深链上 O(n²)。要更快：重链剖分 + 线段树维护 2×2 max-plus 矩阵，单次更新 O(log² n)。

**Q8. 森林（多个根）呢？** 加一个 PnL = 0 的虚拟总根；或每棵树分别算：打家劫舍相加，路径取最大。

**Q9. 怎么测？** 手算样例；对拍（`2^n` 枚举当裁判，随机小树，打乱标签）；构造性用例（两种方向的 10^5 链，已知答案 50000）；512 KiB 小栈线程验证不爆栈；子进程验证递归版真的会崩；错误顺序逐条测；UBSan 抓 `llabs(LLONG_MIN)`。

## 12. 自测

1. 为什么 `take[v]` 用孩子的 `skip` 而不是 `max(take, skip)`？
2. `parent = {-1, 0, 1}`，`pnl = {3, 5, 3}`：`max_pnl()` 和 `plan()`？
3. `parent = {-1, 0}`，`pnl = {5, 5}`：`plan()`？
4. 根 0 带三个孩子，`pnl = {-1, 6, 7, 2}`：`max_path_sum()` 和 `max_down_path()`？
5. 下面的循环对 `parent = {1, 2, -1}` 为什么错？

```cpp
for (int v = n - 1; v >= 0; --v) {
    int p = parent[v];
    if (p >= 0) { in[p] += out[v]; out[p] += std::max(in[v], out[v]); }
}
```

6. 为什么检查 `pnl` 范围不能用 `std::llabs`？
7. 10^5 层链、512 KiB 栈：你有哪几种办法，各有什么代价？

<details><summary>答案</summary>

1. 选了 v，v 的直接孩子不能选，只能取「不选孩子」的最优，即孩子的 `skip`；孩子的孩子可以选，已包含在 `skip` 里。用 `max` 会允许父子同选。
2. 叶子 2：take 3，skip 0。台 1：take 5，skip 3。根：take = 3 + 3 = 6，skip = max(5, 3) = 5。答案 6。根 `6 > 5` 选，台 1 不选，台 2 父没选且 `3 > 0`，选。`{6, {0, 2}}`。
3. `take[0] = 5`，`skip[0] = 5`，相等不选根；台 1 的父没选，`5 > 0` 选。`{5, {1}}`。
4. `down(1) = 6`，`down(2) = 7`，`down(3) = 2`，`down(0) = -1 + 7 = 6`。在 0 拐弯：`-1 + 7 + 6 = 12`。`max_path_sum() = 12`，`max_down_path() = 7`（单独走 2 号）。
5. 它假设 `parent[v] < v`。这里先处理 v = 2（根，跳过），再处理 v = 1：此时 1 的孩子 0 还没把结果推上来，`in[1]` / `out[1]` 还是初值，推给 2 的值是错的。要按 BFS 顺序倒扫。
6. `llabs(LLONG_MIN)` 的结果 `2^63` 放不进 `long long`，是有符号溢出，属于未定义行为；UBSan 会终止进程，没有 sanitizer 时也可能被编译器当成「永远非负」而优化掉检查。直接比较 `p > MAX || p < -MAX`。
7. (1) BFS 顺序倒扫：O(1) 栈、O(n) 额外数组，推荐。(2) 显式栈做迭代后序：栈放堆上，要记「孩子处理完没有」，代码更长。(3) 加大线程栈：只是推迟上限，链再长又崩，每个线程占的虚拟内存也更多。(4) 依赖编译器的尾调用优化：标准不保证，而且这个递归本身不是尾递归。

</details>
