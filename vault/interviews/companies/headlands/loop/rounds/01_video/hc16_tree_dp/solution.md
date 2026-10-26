# hc16 · 解法与原理

这是一道状态定义的题：每个台只有「选」和「不选」两种状态，答案只依赖子树，所以孩子必须先于父亲算出来。难点在两处：规则要说清（平局、空树、全负怎么办），以及 10 万层的链不能用递归。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll compute two values per desk: the best total in its subtree if I take it, and if I skip it. Before I start: is `parent[i] < i` guaranteed? Is the root always desk 0? And may I pick nothing, so the answer is never negative?"

面试官通常会说：不保证顺序，根可以是任何一个台，一个都不选是合法的。第一条决定了你不能「从 n-1 倒着扫父数组」，必须沿着树走出一个顺序。

## Part 1 · 建树 + 最大总 PnL

**思路**：先写构造函数——数一遍 `-1` 找根，同时把每个台挂到它上级的孩子列表里；然后从根做 BFS，把台依次写进 `order`；如果 `order` 没装满 n 个，说明有环。DP 只有两行：倒着扫 `order`，每个台处理完后把自己的值加到上级身上。

**原理：状态和转移**

`take[v]` 是选 `v` 时 `v` 的子树最大总和，`skip[v]` 是不选 `v` 时的最大总和。

```
take[v] = pnl[v] + Σ skip[孩子]              选了 v，孩子都不能选
skip[v] = Σ max(take[孩子], skip[孩子])      不选 v，每个孩子自己挑更好的
答案   = max(take[根], skip[根])
```

孩子的孩子可以选，这已经包含在孩子的 `skip` 里了。样例树里：`take[1] = 4`、`skip[1] = 6 + 3 = 9`；`take[2] = -9`、`skip[2] = 7 + 1 = 8`；`take[0] = 1 + 9 + 8 = 18`、`skip[0] = 9 + 8 = 17`，答案 18。

**原理：为什么倒着扫 BFS 顺序就够了**

BFS 从根出发，父亲先入队，所以 `order` 里每个台都排在它的所有孩子前面。倒着扫，处理到 `v` 时它的孩子都已经处理过、并且已经把值加进了 `take[v]` 和 `skip[v]`。这等于后序遍历（先孩子后父亲），却不需要递归，栈深是 O(1)。

递归写法在 10 万层的链上会失败：每一层调用在线程栈上放一个栈帧，栈的大小是固定的。Java 抛 `StackOverflowError`；C++ 没有异常可抓，进程直接收到 `SIGSEGV`。把栈调大只是推迟问题，链再长一个数量级还是会爆。根治办法是用自己的数组代替调用栈，这就是 `order`。

测试里特意用了两种链：`parent[i] = i - 1` 和 `parent[i] = i + 1`。后者的编号顺序和层次顺序相反，偷懒的「从 n-1 往 0 扫」会在这里出错。

**Java**

```java
public DeskTree(int[] parent, long[] pnl) {
    int n = parent.length;
    if (pnl.length != n) throw new IllegalArgumentException("length mismatch");
    this.parent = parent.clone();
    this.pnl = pnl.clone();
    List<List<Integer>> children = new ArrayList<>();
    for (int i = 0; i < n; i++) children.add(new ArrayList<>());
    int root = -1;
    for (int i = 0; i < n; i++) {
        if (parent[i] == -1) {
            if (root != -1) throw new IllegalArgumentException("more than one root");
            root = i;
        } else if (parent[i] < 0 || parent[i] >= n || parent[i] == i) {
            throw new IllegalArgumentException("invalid parent: " + parent[i]);
        } else {
            children.get(parent[i]).add(i);
        }
    }
    order = new int[n];
    int tail = 0;
    if (n > 0) {
        if (root == -1) throw new IllegalArgumentException("no root");
        order[tail++] = root;
        for (int head = 0; head < tail; head++)
            for (int c : children.get(order[head])) order[tail++] = c;
        if (tail != n) throw new IllegalArgumentException("cycle");
    }
}

private long[][] solve() {                     // {take, skip}
    int n = pnl.length;
    long[] take = pnl.clone(), skip = new long[n];
    for (int i = n - 1; i > 0; i--) {          // 倒着扫：孩子先于父亲
        int v = order[i], p = parent[v];
        take[p] += skip[v];
        skip[p] += Math.max(take[v], skip[v]);
    }
    return new long[][] {take, skip};
}

public long maxPnl() {
    if (pnl.length == 0) return 0;
    long[][] s = solve();
    return Math.max(s[0][order[0]], s[1][order[0]]);
}
```

**C++**

```cpp
DeskTree(std::vector<int> parent, std::vector<long long> pnl) : parent_(std::move(parent)), pnl_(std::move(pnl)) {
    const int n = static_cast<int>(parent_.size());
    if (static_cast<int>(pnl_.size()) != n) throw std::invalid_argument("length mismatch");
    std::vector<std::vector<int>> children(n);
    int root = -1;
    for (int i = 0; i < n; ++i) {
        if (parent_[i] == -1) {
            if (root != -1) throw std::invalid_argument("more than one root");
            root = i;
        } else if (parent_[i] < 0 || parent_[i] >= n || parent_[i] == i) {
            throw std::invalid_argument("invalid parent");
        } else {
            children[parent_[i]].push_back(i);
        }
    }
    if (n == 0) return;
    if (root == -1) throw std::invalid_argument("no root");
    order_.push_back(root);
    for (std::size_t head = 0; head < order_.size(); ++head)
        for (int c : children[order_[head]]) order_.push_back(c);
    if (static_cast<int>(order_.size()) != n) throw std::invalid_argument("cycle");
}

std::pair<std::vector<long long>, std::vector<long long>> solve() const {
    std::vector<long long> take = pnl_, skip(pnl_.size(), 0);
    for (int i = static_cast<int>(order_.size()) - 1; i > 0; --i) {
        const int v = order_[i], p = parent_[v];
        take[p] += skip[v];
        skip[p] += std::max(take[v], skip[v]);
    }
    return {take, skip};
}

long long max_pnl() const {
    if (pnl_.empty()) return 0;
    auto [take, skip] = solve();
    return std::max(take[order_[0]], skip[order_[0]]);
}
```

复杂度：建树和 DP 都是 O(n) 时间、O(n) 空间；栈深 O(1)。

## Part 2 · 还原方案

**思路**：`take` 和 `skip` 已经有了，现在从根往下决定每个台选不选。BFS 顺序正着扫，父亲一定先于孩子被决定。

**原理：为什么这样还原是最优的**

台 `v` 在「上级没被选」的前提下，可以自由地在「选 `v`（得到 `take[v]`）」和「不选 `v`（得到 `skip[v]`）」之间挑更大的，所以 `take[v] > skip[v]` 就选。如果上级被选了，`v` 只能不选，它的子树取 `skip[v]`，这正是上级的 `take` 里用的值。每一步都和 DP 的转移一一对应，所以选出来的总和等于 `maxPnl()`。

平局时不选：`take[v] == skip[v]` 说明选不选总和一样，约定不选，方案才是确定的。顺带得到：PnL 为 0 的台永远不会被选，全负的树方案是空列表。

**Java**

```java
public List<Integer> plan() {
    int n = pnl.length;
    long[][] s = solve();
    boolean[] chosen = new boolean[n];
    for (int i = 0; i < n; i++) {              // 正着扫：父亲先于孩子
        int v = order[i];
        boolean parentTaken = parent[v] >= 0 && chosen[parent[v]];
        chosen[v] = !parentTaken && s[0][v] > s[1][v];
    }
    List<Integer> desks = new ArrayList<>();
    for (int v = 0; v < n; v++) if (chosen[v]) desks.add(v);
    return desks;
}
```

**C++**

```cpp
std::vector<int> plan() const {
    const int n = static_cast<int>(pnl_.size());
    auto [take, skip] = solve();
    std::vector<char> chosen(n, 0);
    for (int v : order_) {
        const bool parent_taken = parent_[v] >= 0 && chosen[parent_[v]];
        chosen[v] = !parent_taken && take[v] > skip[v];
    }
    std::vector<int> desks;
    for (int v = 0; v < n; ++v) if (chosen[v]) desks.push_back(v);
    return desks;
}
```

复杂度：O(n) 时间，O(n) 空间。

## Part 3 · 口头追问和回答

**1. 最大路径和（可以拐弯）怎么算？**

再定义 `down[v]`：从 `v` 出发、一直往下走的最大路径和，`down[v] = pnl[v] + max(0, 最好的孩子的 down)`，负的支路不要。经过 `v` 拐弯的路径是 `pnl[v]` 加上最好的两条非负支路。所有 `v` 上的拐弯路径取最大，就是答案。同样按倒序 BFS 一遍扫完，O(n)。样例树的答案是 13：在 1 号拐弯，6 + 4 + 3。如果要求路径非空而且全是负数，答案是最不坏的单个台，所以「负支路按 0」只能用在加到别人身上的时候，不能用在初始化答案上。

**2. 每个台作根时的答案各是多少？**

换根（rerooting）：先按原来的根倒着扫，得到每个台的子树答案（向下）；再正着扫一遍，把「去掉 `v` 的子树之后，上面那一块」的答案传给 `v`，合并成「以 `v` 为根」的答案。这里要对兄弟的值做前缀、后缀合并，或者对可逆的运算（加法）直接减掉。总共两遍扫，O(n)，而不是对每个根重跑一遍的 O(n²)。

**3. 恰好选 k 个台怎么改？**

状态多一维：`take[v][j]`、`skip[v][j]` 表示 `v` 的子树里恰好选 j 个台的最大和。合并孩子时是一次背包式的合并（knapsack merge）。合并时 j 只枚举到 min(子树大小, k)，总复杂度是 O(n·k)，不是 O(n·k²)，因为每一对台只在它们的最近公共祖先处被合并一次。

**4. 树一行一行地来，孩子可能先于父亲到达怎么办？**

不能假设父亲先出现。先把所有 `(台, 上级, PnL)` 收齐，再建孩子列表和 BFS 顺序，然后做一遍 DP；这就是现在的做法。如果必须边收边出答案，只有在每个台的孩子都到齐之后它的值才确定，所以要记录每个台还在等几个孩子，等待数降到 0 的台再向上传值。

**5. 「选了一个台就必须选它的上级」怎么改？**

这是最大权闭合子图（maximum weight closure）的树形版本，状态变了：`best[v] = pnl[v] + Σ max(0, best[孩子])`，含义是「`v` 已经被选中（它的上级也都选了）」时，`v` 的子树能再得到的最大值，孩子的值为正才值得带上。被选中的台总是一块包含根的连通区域，答案是 `max(0, best[根])`；不再需要选和不选两个状态。

**6. 不用显式的 BFS 顺序，还能怎么避开递归爆栈？**

三种办法。第一，自己写一个显式栈（explicit stack），模拟递归的前序和后序。第二，在一个栈更大的线程里跑递归：Java 的 `Thread` 构造函数能指定栈大小，C++ 用 `pthread_attr_setstacksize`；这只是把上限抬高，深度再大一个数量级还是会爆。第三，尾递归在这里帮不上忙：DP 要在孩子返回之后再合并，不是尾调用，而且 Java 不做尾调用优化，C++ 也不保证。

## 常见错误

1. 假设 `parent[i] < i`，从 n-1 倒着扫父数组：根不是 0 号、父亲编号更大时，处理顺序就错了。
2. 递归写 DFS：10 万层的链栈溢出（Java 抛 `StackOverflowError`，C++ 段错误）。
3. `take[v]` 里加了孩子的 `take`：违反「父子不能同选」。
4. 答案取 `take[根]`，没有和 `skip[根]` 比较；或者全负时返回负数，而题目允许一个都不选。
5. `plan()` 平局时选了台：方案不确定，测试里的期望对不上。
6. 没检查环：有环的输入从根走不到所有台，BFS 提前结束，后面的数组全是 0，答案静默地错。
