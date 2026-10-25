# hc16 · Tree DP on a Desk Hierarchy（交易台层级树上的 DP）—— 讲义

> 读者：会基本 Java（类、方法、循环、数组、`ArrayList`），不要求学过动态规划。覆盖树上的打家劫舍、方案还原、最大路径和、10^5 层链的迭代改写。

---

## 1. 问题是什么

### 1.1 台树

交易公司的台（desk）按上下级排成一棵**树**：一个根台，每个台最多一个直接上级，可以有任意多个下级。每个台有一个整数 PnL（当日盈亏，单位 tick，可以为负）。
任务分四步：

1. **选台**：不能同时选一个台和它的直接上级，求最大总 PnL（树上的打家劫舍，house robber on a tree）。
2. **还原方案**：不只要数，还要知道选了哪些台；最优方案不唯一时规则必须固定。
3. **路径与子树**：最大的向下路径、最大的任意路径（可以拐弯）、总和最大的子树。
4. **深链**：台树退化成 10^5 层的链，递归写法栈溢出，必须改成迭代。

### 1.2 手算例子

```
          0 (1)
         /     \
     1 (4)     2 (-9)
     /   \      /   \
 3 (6)  4 (3) 5 (7)  6 (1)
```

括号里是 PnL。`parent = [-1, 0, 0, 1, 1, 2, 2]`：0 号是根，1、2 号的上级是 0，3、4 号的上级是 1，5、6 号的上级是 2。

**从叶子往上算。** 每个台算两个数：`take` = 选它时它的子树里能拿到的最大值，`skip` = 不选它时的最大值。

| 台 | take | skip |
|---|---|---|
| 3、4、5、6（叶子） | 6、3、7、1 | 0、0、0、0 |
| 1 | 4（它自己；孩子不能选） | 6 + 3 = 9（孩子各自选，互不相邻） |
| 2 | -9 | 7 + 1 = 8 |
| 0 | 1 + 9 + 8 = 18（孩子 1、2 都不选，用它们的 skip） | max(4, 9) + max(-9, 8) = 17 |

答案 `max(18, 17) = 18`。方案：根 `18 > 17` 选；根被选，1、2 不选；3、4、5、6 各自 `take > skip` 选。选了 `{0, 3, 4, 5, 6}`，1 + 6 + 3 + 7 + 1 = 18。

### 1.3 四个 Part

| Part | 内容 |
|---|---|
| 1 | 校验输入、建树；`maxPnl()` |
| 2 | `ofEdges`（无向边列表输入，要定向）；`plan()` 返回 `Plan(total, desks)`，平局时不选 |
| 3 | `maxDownPath()`、`maxPathSum()`（可拐弯）、`bestSubtree()`（平局取小编号） |
| 4 | 所有方法在 10^5 层的链上、512 KiB 的栈里不爆栈；`maxPnlRecursive()` 是教科书递归版，用来亲眼看它崩 |

---

## 2. 前置知识

### 2.1 树与父数组

**树**（tree）：n 个节点、n-1 条边、连通、没有环。选一个节点当**根**（root）之后，每个非根节点有唯一的**父**（parent），父的相邻节点叫**子**（child）。没有子的叫**叶子**（leaf）。节点 v 和它下面所有后代合在一起叫 v 的**子树**（subtree）。

存法之一是**父数组**（parent array）：`parent[i]` 是 i 的父，根写 `-1`。n 个数就够。**注意：不保证 `parent[i] < i`。**

例：`parent = [2, 2, -1]` 表示根是 2 号，0、1 号是它的孩子。

所以「从 n-1 倒着扫数组就是孩子先于父亲」是错的。要得到正确的处理顺序，必须沿着树走（2.3）。

另一种存法是**边列表**（edge list）：`{a, b}` 表示 a、b 之间有一条**无向**边，谁是上级要从指定的根出发走一遍才知道。

### 2.2 动态规划与打家劫舍

**动态规划**（dynamic programming，DP）：把大问题拆成子问题，子问题的答案记下来，每个只算一次。

先看**链**上的打家劫舍：一排房子，每间有钱 `a[i]`，不能偷相邻的两间，最多偷多少？对第 i 间有两种可能：偷它（那么 i-1 不能偷）或不偷（i-1 随便）。记

```
take[i] = a[i] + skip[i-1]                  偷第 i 间
skip[i] = max(take[i-1], skip[i-1])         不偷第 i 间
```

答案 `max(take[末], skip[末])`。**树**只是把「前一间」换成「所有孩子」：

```
take[v] = pnl[v] + Σ skip[孩子]
skip[v] = Σ max(take[孩子], skip[孩子])
```

为什么 `take[v]` 里是孩子的 `skip`：选了 v，孩子就不能选，只能取「不选孩子」的最优；孩子的孩子可以选，这已经包含在孩子的 `skip` 里了。
**状态定义**是这类题的全部灵魂：`take[v]` / `skip[v]` 只依赖 v 的**子树**，所以必须先算孩子、再算父亲。

「什么都不选」是合法方案，所以空树和全负的树答案是 0（而不是最大的负数）。

### 2.3 BFS 顺序与「倒着扫」

**BFS**（breadth-first search，广度优先遍历）：从根出发，先访问根，再访问根的所有孩子，再访问孩子的孩子……用一个**队列**（先进先出）实现；这里用一个 `int[] order` 数组加一个读下标就够：

```java
order[0] = root; int head = 0, tail = 1;
while (head < tail) {
    int v = order[head++];
    for (孩子 c of v) order[tail++] = c;
}
```

得到的 `order` 里，**每个节点都排在它的所有孩子前面**（父亲先入队）。把它**倒着**扫一遍，就是「先处理孩子，再处理父亲」，正好满足 DP 的依赖。
也就是说：BFS 顺序倒扫 = 后序遍历的替身，但不需要递归，也不需要栈。

### 2.4 调用栈、栈帧与 `StackOverflowError`

每次方法调用，JVM 在线程的**栈**（stack）上压一个**栈帧**（stack frame），放返回地址、参数、局部变量；方法返回时弹掉。递归就是同一个方法的栈帧一层压一层。
栈的大小**固定**（Java 线程默认约 1 MiB，可用 `-Xss` 调；C++ 主线程 8 MiB，自己创建的线程更小）。一个简单的递归方法每层约几十到一百多字节：

```
10^5 层 × 约 100 字节 ≈ 10 MB  >  512 KiB ~ 1 MiB
```

超了，Java 抛 `StackOverflowError`（它是 `Error` 不是 `Exception`；可以捕获，但之后程序状态通常不可信）。把栈调大只是推迟：链再长 10 倍照样爆。
**根治**：不用调用栈，改用自己的数组——这就是 2.3 的 BFS 顺序。

### 2.5 CSR：用两个数组存「每个节点的孩子」

`List<Integer>[] children` 要建 n 个 `ArrayList`，每个元素还要装箱成 `Integer`，n = 10^6 时又慢又占内存。**CSR**（compressed sparse row）用两个 `int[]` 搞定：

v 的孩子在 `childList` 里的下标范围是 `childStart[v] .. childStart[v+1]-1`。

做法（计数排序）：

1. 统计每个节点有几个孩子，放进 `childStart[v+1]`；
2. 对 `childStart` 做前缀和，`childStart[v]` 就是 v 的孩子区间的起点；
3. 再扫一遍 `parent[]`，把 `v` 填进它的父的区间里（用一份 `fill` 副本记当前写到哪）。

### 2.6 溢出与 `long`

`long` 范围约 ±9.22×10^18。题目把 `|pnl|` 限制在 10^12 以内、台数 ≤ 10^6，任何和的绝对值 ≤ 10^18，**不会溢出**。
这是一种常见的工程办法：不在每次加法上 `Math.addExact`，而是在入口把输入限制到「怎么加都放得下」的范围，并证明它。代价是超范围输入要在入口拒绝。
验证入口范围时写 `p > MAX || p < -MAX`，**不要**写 `Math.abs(p) > MAX`：`Math.abs(Long.MIN_VALUE)` 仍是 `Long.MIN_VALUE`（负数），会漏掉。

---

## 3. 从最笨的解法开始

**枚举所有子集**：n 个台，2^n 个选法，逐个检查有没有父子同选，取最大和。n = 20 就是 100 万种，n = 60 已经算不完。但它对**小树**永远正确，所以是最好的测试裁判（测试里就是这么对拍的）。

**递归 DP** 是下一步，也是面试第一版：

```java
long[] solve(int v) {                       // 返回 {take, skip}
    long take = pnl[v], skip = 0;
    for (int c : children(v)) {
        long[] r = solve(c);
        take += r[1];                        // 选 v：孩子只能用 skip
        skip += Math.max(r[0], r[1]);        // 不选 v：孩子随便
    }
    return new long[] {take, skip};
}
```

**正确**、短、O(n)。问题只有一个：树深 10^5 时递归 10^5 层，栈溢出。面试官几乎一定会问「如果这棵树是一条 10 万层的链呢？」。这个版本保留在 reference 里，叫 `maxPnlRecursive()`。

---

## 4. 一步一步改进

### 第 1 步：校验输入，固定错误顺序

输入可能是各种坏的：长度不等、PnL 超范围、父下标越界、没有根或有多个根、有环。面试里被追问「非法输入怎么办」时，要能说出**检查顺序**并保持稳定（测试靠它确定该报哪个错）：

长度不等 → 台数过多 → pnl 越界 → parent 越界 / 自己指自己 → 根的个数不是 1 → 有环。

「有环」的检测不用单独的算法：BFS 从根出发，如果访问到的节点数不足 n，剩下的节点就是挂在环里、从根够不着的。

### 第 2 步：建 CSR + BFS 顺序

校验之后，建 `childStart` / `childList`（2.5），再 BFS 得到 `order`（2.3）。这一步 O(n)，之后所有查询共用。

### 第 3 步：Part 1，倒扫一遍做 DP

不再递归；对 `order` 倒着扫，每个节点处理时它的孩子都已经处理完，直接把自己的结果**推给父亲**：

```java
for (int v = 0; v < n; v++) in[v] = pnl[v];          // in = take
for (int i = n - 1; i >= 0; i--) {
    int v = order[i], p = parent[v];
    if (p >= 0) {
        in[p]  += out[v];                           // 父选：孩子只能不选
        out[p] += Math.max(in[v], out[v]);          // 父不选：孩子随便
    }
}
```

「推给父亲」的写法不需要孩子列表，只要 `parent[]`。答案 `max(in[root], out[root])`，空树 0。

### 第 4 步：Part 2，还原方案与平局规则

DP 值已经有了，还原只需**自顶向下**再扫一遍（`order` 正着扫）：

```
chosen[v] = (v 是根 或 父没被选) 且 in[v] > out[v]
```

**平局规则**：`in[v] == out[v]` 时不选。这个规则有三个好处：它只依赖 DP 值，所以不用回溯；它在每个台上局部可判定；它让 PnL 为 0 的台永远不进方案。
例：两个台 `[5, 5]`（根 0、孩子 1）：`take[0] = 5`，`skip[0] = 5`，相等，所以根不选，选孩子，`Plan(5, [1])`。

**边列表输入**：把无向边建成邻接表（也是 CSR，每条边存两次），从 `root` BFS，第一次碰到的邻居就是孩子，记下它的父，得到 `parent[]`；如果 BFS 访问的节点不足 n，说明不连通（或者有重复边顶掉了连通性），报 `not a tree`。之后和父数组走同一条路。

### 第 5 步：Part 3，路径

**向下路径**：`down[v]` = 以 v 为起点、一路往下的最大路径和 = `pnl[v] + max(0, 最好的孩子 down)`。负的支路不要，所以和 0 取最大。
**拐弯路径**：在 v 拐弯 = 往下走左支、经过 v、再往下走右支 = `pnl[v] + 最好的 down + 第二好的 down`（负的都当 0）。

```
          v
        /   \
   (左支)    (右支)      拐弯路径 = 左支 + v + 右支
```

每个节点记两个数 `top1`、`top2`（孩子贡献来的最好两条非负 `down`），倒扫时算出自己的 `down` 后更新父亲的 `top1/top2`。全局答案取所有节点的最大值。
路径**不能为空**：全是负数时答案是「最不坏的单个台」，所以答案初值是 `Long.MIN_VALUE` 而不是 0。

**子树和**：`sum[v] = pnl[v] + Σ sum[孩子]`，倒扫时 `sum[parent[v]] += sum[v]`；最后按编号升序扫，**严格大于**才更新，平局自然取小编号。

### 第 6 步：Part 4，验证「不爆栈」

迭代版在 10^5 层链上本来就没有递归，只需要测试它：测试用 `new Thread(null, body, "name", 512 * 1024)` 起一个**只有 512 KiB 栈**的线程跑深链——大约几千层递归就会崩，10^5 层远远超过。
两种方向都要测：根是 0 的链，和根是 n-1 的链（编号顺序与层次顺序相反）。后者专门抓「从 n-1 倒扫 parent」的偷懒写法。

---

## 5. 逐段讲解法

### 5.1 字段

```java
private final int n, root;
private final long[] pnl;
private final int[] parent;
private final int[] order;        // BFS 顺序：父亲在孩子前面
private final int[] childStart;   // CSR
private final int[] childList;
```

全部是数组，没有 `List<Integer>`，没有装箱。`ofParents` 里 `parent.clone()`、`pnl.clone()`：入参被调用方改了不能影响树。

### 5.2 建树

```java
this.childStart = new int[n + 1];
for (int v = 0; v < n; v++) if (parent[v] >= 0) childStart[parent[v] + 1]++;
for (int v = 0; v < n; v++) childStart[v + 1] += childStart[v];
this.childList = new int[Math.max(0, n - 1)];
var fill = Arrays.copyOf(childStart, n);
for (int v = 0; v < n; v++) if (parent[v] >= 0) childList[fill[parent[v]]++] = v;
```

三步就是 2.5 的计数排序。然后 BFS 填 `order`，`tail != n` 就抛 `IllegalArgumentException("cycle")`。

### 5.3 `solveRobber`

即第 3 步的循环：`in` 初值 `pnl`，`out` 初值 0（`new long[n]`），倒扫推给父亲。`plan()` 复用它再正扫一遍：

```java
for (int v : order) {
    int p = parent[v];
    chosen[v] = (p < 0 || !chosen[p]) && in[v] > out[v];
}
var desks = IntStream.range(0, n).filter(v -> chosen[v]).boxed().toList();
```

正扫保证处理 v 时它的父亲 `chosen[p]` 已经定了。

### 5.4 `paths`

```java
for (int i = n - 1; i >= 0; i--) {
    int v = order[i];
    long down = pnl[v] + top1[v];
    bestDown = Math.max(bestDown, down);
    bestPath = Math.max(bestPath, pnl[v] + top1[v] + top2[v]);
    int p = parent[v];
    if (p >= 0 && down > 0) {                 // 只有正的才值得往上传
        if (down > top1[p]) { top2[p] = top1[p]; top1[p] = down; }
        else if (down > top2[p]) { top2[p] = down; }
    }
}
```

`top1/top2` 初值 0，天然实现了「负的支路不要」。`down` 为负就不往上传。

### 5.5 `bestSubtree`

`sum` 从 `pnl.clone()` 开始，倒扫（`i > 0`，跳过根）`sum[parent[v]] += sum[v]`；再 `for v = 1..n-1` 严格大于才换。

### 5.6 `ofEdges`

校验顺序见 problem.md。核心：`start/adj` 是无向邻接 CSR（每条边两个方向各存一次）；`parent` 初值 `-2` 表示「还没访问」；根设 `-1`；BFS 时 `parent[w] == -2` 才认 w 为孩子。`tail != n` → `not a tree`。

---

## 6. Java 21 特性小课

### `record`（含紧凑构造器）

```java
public record Plan(long total, List<Integer> desks) {
    public Plan { desks = List.copyOf(desks); }
}
public record Subtree(int root, long total) {}
```

旧写法要手写字段、构造器、getter、`equals`、`hashCode`、`toString`。record 一行，`equals` 按字段比较，测试直接 `assertEquals(new Plan(18, List.of(0, 3, 4, 5, 6)), plan)`。
紧凑构造器里 `List.copyOf` 让结果不可变，调用方改不了、传入的列表之后被清空也不影响它。

### `IntStream` + `boxed().toList()`

```java
var desks = IntStream.range(0, n).filter(v -> chosen[v]).boxed().toList();
```

一行完成「按编号升序收集被选的台」。`Stream.toList()`（Java 16）返回不可变列表。热路径不要这样写（装箱），这里只在结果出口用一次。

### `var`、`Objects.requireNonNull`

`var fill = Arrays.copyOf(childStart, n);`：右边已经说明类型就用 `var`。`Objects.requireNonNull(parent);` 是明确的卫语句：`null` 立刻抛 NPE，而不是在后面某行莫名其妙崩。

### 在指定栈大小的线程里跑（测试）

```java
var t = new Thread(null, () -> { ... }, "sized-stack", 512 * 1024);
```

四参数构造器的最后一个参数是栈大小的**建议值**（字节）。测试用它把栈钉在 512 KiB，让 `StackOverflowError` 稳定重现；然后在线程里捕获 `Throwable`，交回测试线程重新抛出。

---

## 7. 追问预演

**Q1. 为什么 BFS 顺序倒扫而不是 DFS 后序？**
两者都保证孩子先于父亲。BFS 顺序只要一个数组加一个下标；DFS 后序要显式栈并记「孩子处理完没有」。要点：任何「父亲在孩子前」的顺序倒过来都满足 DP 依赖。
说：「我需要的只是一个拓扑序，BFS 数组倒过来就是，不需要递归也不需要栈。」

**Q2. 为什么 `take[v]` 加的是孩子的 `skip`？**
选了 v，直接下级不能选，只取各自「不选」的最优；孙辈可以选，已经包含在孩子的 `skip` 里。

**Q3. 平局为什么要有规则？**
最优方案可能不止一个，没有规则调用方没法比较输出、测试也没法写。规则要局部可判定（`take > skip`），只靠 DP 值自顶向下就能还原，不用回溯。

**Q4. 溢出怎么论证？**
入口限制 `|pnl| ≤ 10^12`、`n ≤ 10^6`，任何和 ≤ 10^18 < 9.22×10^18。如果必须支持任意 `long`：`Math.addExact`，并规定「真实答案超出范围才抛」。对打家劫舍这是可证明的——`best` 和 `skip` 恒非负，且 `best(孩子) ≤ best(父)`，中间值溢出当且仅当最终答案溢出。更大范围用 `BigInteger`。

**Q5. 为什么递归会崩？不想改迭代怎么办？**
栈帧 × 深度 > 栈上限。可以 `new Thread(null, r, name, 512L << 20)` 加大栈，但只是推迟；JVM 不保证尾递归优化。根治：显式栈 / BFS 顺序。
说：「递归深度等于树高，树高没有上界，所以我把调用栈换成数组。」

**Q6. 最大路径和为什么拐点用两条最好的支路？**
经过 v 拐弯的路径是「左支 + v + 右支」，每条支路是 v 的某个孩子的向下路径，各取最大的两条；负的支路不如不走，所以和 0 取最大。

**Q7. 台一个个到达（流式）怎么办？**
只追加叶子：影响的只有祖先链，重算 `take/skip`，最坏 O(深度)；深链上退化为 O(n²)。要更快：重链剖分（HLD）+ 线段树维护 2×2 的 max-plus 矩阵，单次更新 O(log² n)。

**Q8. 森林（多个根）呢？**
加一个 PnL = 0 的虚拟总根；或每棵树分别算：打家劫舍相加，路径取最大。

**Q9. 怎么测？**
手算样例；对拍（2^n 枚举当裁判，随机小树，打乱标签）；构造性用例（两种方向的 10^5 链，已知答案 50000）；512 KiB 小栈线程验证不爆栈；错误顺序逐条测。

---

## 8. 常见误区

1. **从 `n-1` 倒着扫 `parent[]` 当「孩子先于父亲」。** `parent[i] > i` 时全错；要用 BFS 顺序。
2. **选 v 时加了 `max(take, skip)`。** 选 v 孩子只能用 `skip`。
3. **全负的树答案写成负数。** 什么都不选 = 0。路径题则相反：路径不能为空。
4. **平局取「选」。** 规则是严格大于才选；PnL 为 0 的台不进方案。
5. **最大路径把负支路也加上。** 与 0 取最大；全负时答案是单个最大的台，不是 0。
6. **拐弯只用一条支路 / 把拐点的 `down` 当拐弯路径往上传。** 往上传的只能是「一条」支路。
7. **`Math.abs(p) > MAX` 校验。** `Math.abs(Long.MIN_VALUE)` 是负数，漏判。
8. **入参不拷贝。** 调用方之后改数组，树悄悄变了。
9. **`bestSubtree` 平局取大编号。** 倒着扫或用 `>=` 会选到后面的台。
10. **用 `List<List<Integer>>` 存孩子。** 10^6 个台时装箱 + n 个 `ArrayList` 又慢又占内存；用 CSR。
11. **边列表只数边数。** `n-1` 条边但有重复边或环，图可能不连通；必须从根 BFS 数访问数。
12. **以为 `catch (StackOverflowError)` 能解决问题。** 能捕获，但栈上的状态已不可信；正解是不递归。

---

## 9. 自测题

**Q1（概念）** 为什么 `take[v]` 用孩子的 `skip` 而不是 `max(take, skip)`？

<details><summary>答案</summary>选了 v，v 的直接孩子不能选，只能取「不选孩子」的最优，即孩子的 `skip`；孩子的孩子可以选，已包含在 `skip` 里。用 `max` 会允许父子同选。</details>

**Q2（手算）** `parent = [-1, 0, 1]`，`pnl = [3, 5, 3]`。求 `maxPnl` 和 `plan`。

<details><summary>答案</summary>叶子 2：take 3，skip 0。台 1：take 5，skip 3。根 0：take = 3 + skip(1) = 3 + 3 = 6，skip = max(5, 3) = 5。答案 6。根 `6 > 5` 被选，台 1 不选，台 2：父没选且 `3 > 0`，被选。`Plan(6, [0, 2])`。</details>

**Q3（手算）** `parent = [-1, 0]`，`pnl = [5, 5]`，`plan()` 是什么？

<details><summary>答案</summary>`take[0] = 5`，`skip[0] = 5`，相等不选根；台 1 的父没选，`5 > 0` 被选。`Plan(5, [1])`。</details>

**Q4（手算）** 根 0 带三个孩子，PnL 为 `[-1, 6, 7, 2]`（孩子 1、2、3）。`maxPathSum` 和 `maxDownPath`？

<details><summary>答案</summary>`down(1) = 6`，`down(2) = 7`，`down(3) = 2`，`down(0) = -1 + 7 = 6`。拐弯在 0：`-1 + 7 + 6 = 12`。`maxPathSum = 12`，`maxDownPath = 7`（单独走 2 号）。</details>

**Q5（找 bug）** 下面的 `solveRobber` 对 `parent = {1, 2, -1}`（链 2 → 1 → 0）为什么错？

```java
for (int v = n - 1; v >= 0; v--) {
    int p = parent[v];
    if (p >= 0) { in[p] += out[v]; out[p] += Math.max(in[v], out[v]); }
}
```

<details><summary>答案</summary>它假设 `parent[v] < v`。这里先处理 v = 2（根，无父，跳过），再处理 v = 1：此时 1 的孩子 0 还没把结果推上来，`in[1]` / `out[1]` 还是初值，推给 2 的值是错的。要按 BFS 顺序倒扫。</details>

**Q6（设计）** 10^5 层链、512 KiB 栈。你有哪几种办法，各有什么代价？

<details><summary>答案</summary>(1) BFS 顺序倒扫：O(1) 栈、O(n) 额外数组，推荐。(2) 显式栈做迭代后序：栈放堆上，要记「孩子处理完没有」的状态，代码更长。(3) 加大线程栈（`new Thread(null, r, name, size)`）：只是推迟上限，链再长就又崩，且每个线程都占那么大的虚拟内存。(4) 依赖尾递归优化：JVM 不保证，这个递归本身也不是尾递归。</details>

**Q7（小编程）** 写 `static long maxDownFrom(int[] parent, long[] pnl)`，只用一个按 BFS 顺序给出的 `int[] order`，返回所有 `down[v]` 的最大值（`down[v] = pnl[v] + max(0, 最好的孩子 down)`）。

<details><summary>答案</summary>

```java
static long maxDown(int[] parent, long[] pnl, int[] order) {
    long[] best = new long[pnl.length];     // 每个台孩子里最好的非负 down
    long ans = Long.MIN_VALUE;
    for (int i = order.length - 1; i >= 0; i--) {
        int v = order[i];
        long down = pnl[v] + best[v];
        ans = Math.max(ans, down);
        if (parent[v] >= 0 && down > best[parent[v]]) best[parent[v]] = down;
    }
    return ans;
}
```
</details>

---

## 延伸阅读

* CLRS《算法导论》动态规划一章；LeetCode 337「打家劫舍 III」、124「二叉树中的最大路径和」。
* Java 语言规范与 JVM 规范中关于线程栈和 `StackOverflowError` 的章节；`java.lang.Thread` 构造器的 `stackSize` 参数文档。
