# q03 · Tree Height Reduction (三合一：删叶子 / 剪子树 / 换根)

**Type:** bespoke OA + 电面 · **Stage:** OA + Phone Screen · **Last asked:** 2026-08 ·
**Frequency:** 3 独立来源 · **Confidence:** MED-HIGH

## 背景

"树高压缩"是 Snowflake 题库里横跨 OA 和电面反复出现的题族：给一棵有根树，要求把最大深度/高度压到
某个阈值以内，但"怎么压"（删叶子？删子树？还是把子树接到根下？）在三个不同来源里是三种不同的题面、
**三种不同的节点编号 / 深度约定**。本题把三者合并成三个 part，**每个 part 严格遵循它自己来源的
约定，不强行统一**——这也是这题真正的坑：把 part 之间的编号/深度基准搞混，是隐藏测试里最常见的
失分点。

## 输入格式（stdin）

第一行永远是 `PART <1|2|3>`，决定后面按哪种格式解析。**三个 part 的数组/换行格式各不相同**：

```
PART 1
n
parent[0] parent[1] ... parent[n-2]      # 长度 n-1；n=1 时这一行为空行
k
```
```
PART 2
n
parent[0] parent[1] ... parent[n-1]      # 长度 n；parent[root] == -1
k
```
```
PART 3
tree_nodes
edge_count
tree_from[0] ... tree_from[edge_count-1]  # edge_count=0 时为空行
tree_to[0] ... tree_to[edge_count-1]      # edge_count=0 时为空行
max_operations
```

## 输出（stdout）

- PART 1：一行，删除的节点 id，升序、空格分隔（没有要删的就输出空行）。
- PART 2：一行，一个整数（删除次数）。
- PART 3：一行，一个整数（能达到的最小高度）。

---

## Part 1 — Minimum N-ary Tree Depth Deletions（删叶子，输出 id）

**来源**：FastPrep, Medium, Phone Screen —
https://www.fastprep.io/problems/snowflake-minimum-nary-tree-deletions （置信度 MED）

**原题引用（verbatim-ish）**：
> Given a rooted n-ary tree... via a parent array, find the minimum set of nodes to delete so
> the tree's maximum depth doesn't exceed k. Only non-root leaf nodes can be deleted... return
> node IDs in ascending order.

**约定（仅本 part 适用）**：节点编号 `1..n`。`parent` 长度 `n-1`：`parent[i]`（0-indexed 的 i）
给出节点 `i+2` 的父节点（节点 1 永远是根，没有对应的 parent 项）。**深度：根深度 = 1**（深度按节点数
算，根是第 1 层，它的孩子是第 2 层……）。

**推导（不是猜的）**：因为沿任意"根→节点"路径深度严格递增，一个节点深度超过 k 当且仅当它**必须**
被删——不存在"只删某个更浅的祖先"就能救它的办法（那样反而会连带删掉本来合法的浅层节点）；而它自己
总能在"先删完它自己所有更深的后代（它们也都超过 k，理应先删）"之后，作为叶子被最后删掉。所以：

> **答案就是所有深度 > k 的节点 id，升序排列。**

（根节点即便深度超过 k 也不能被删——只是按本 part 的深度约定，根深度恒为 1，所以只有 `k=0` 这种
不该出现的退化输入才会让根本身"超标"；实现里仍显式排除根，防御这种情况。）

## Part 2 — Prune a Multiway Tree to a Maximum Depth（剪子树，只算数量）

**来源**：PracHub, Medium, Technical Screen —
https://prachub.com/coding-questions/prune-a-multiway-tree-to-a-maximum-depth （置信度 MED）

**原题引用（verbatim-ish）**：
> Given a rooted multiway tree as a parent array, return the minimum explicit subtree deletions
> needed to keep every remaining node within a maximum depth while preserving the root.

**约定（仅本 part 适用，和 Part 1 不同！）**：节点 **0-indexed**；`parent[i]` = 节点 `i` 的父节点
下标；`parent[root] == -1`。**深度：根深度 = 0。**

**推导**：这里每次删除是删掉**一整棵子树**（比逐节点删便宜），所以答案不是"数出所有超标节点"，而是
数**最顶层的超标节点**：

> **答案 = 满足「深度 > k 且它自己的父节点深度 <= k」的节点个数。**
> （如果父节点自己也超标，父节点那一刀已经把这个节点也带走了，不能重复计数。）

## Part 3 — Minimum Height with ≤ max_operations Re-root Ops（换根，求最小高度）

**来源**：FastPrep, Medium, Tree/Binary-Search, OA —
https://www.fastprep.io/problems/snowflake-minimum-height （置信度 MED）

**原题引用（verbatim-ish）**：有根树，根 = 1；"each operation detaches a child subtree and
reattaches it directly under the root"；最多 `max_operations` 次操作，最小化结果树的高度。

**约定（仅本 part 适用）**：节点 **1-indexed**，根 = 1；**高度按边数算**（只有根一个点时高度 = 0）。
树用显式边表给出：`tree_from[i] -> tree_to[i]`（父 → 子）。

**算法**（对下面给的官方例子逐步手算验证过，直接照此实现）：对每个候选高度 `H` 做可行性判断
`total_ops(H) <= max_operations`，`H` 用二分搜索；可行性判断用一个递归 `fix`：

```
def fix(v, d, H):
    # v 目前处于深度 d（不动的话），求让 v 的整棵原始子树满足高度 H 的最少操作数
    if d + height(v) <= H:
        return 0
    if d > H:
        # v 自己已经超标，必须被换根（换根后新深度是 1）
        return 1 + fix_children_only(v, 1, H)
    cut_cost = 1 + fix_children_only(v, 1, H)             # 现在就剪 v
    keep_cost = sum(fix(c, d + 1, H) for c in children(v))  # 把决定权交给孩子
    return min(cut_cost, keep_cost)

def fix_children_only(v, newd, H):
    return sum(fix(c, newd + 1, H) for c in children(v))

def total_ops(H):
    return fix_children_only(root, 0, H)   # 根永远不能被剪
```

`height(v)` = v 的原始子树里，从 v 往下到任意叶子的最大边数。

⚠️ **`H = 0` 的特判（原伪代码没写全的一个坑）**：换根操作永远把节点接到**根**下面，新深度**恒为
1**，不可能是 0——只有根节点本身深度才是 0。所以只要树里除了根还有别的节点，`H = 0` **永远不可行**，
不管 `max_operations` 给多大都救不了（`fix` 里 `if d > H: return 1 + fix_children_only(v, 1, H)`
这一行隐含假设"换根就能让 v 合规"，但没检查换根后的新深度 `1` 是否真的 `<= H`；当 `H = 0` 时这个
假设是错的）。实现时把 `H = 0` 单独短路处理：只有当树只有根节点（没有其他节点）时才可行。

## Worked Examples（三个 part 各自手算验证）

### Part 1
1. `parent=[1,1,2,2,3,4], k=3` → **`[7]`**
   （7 号节点链路 1→2→4→7，深度 4 > 3；其余都 ≤ 3）
2. `parent=[1,2,3,4], k=2` → **`[3,4,5]`**
   （一条链 1-2-3-4-5，节点 3/4/5 深度分别是 3/4/5，均 > 2）

### Part 2
1. `parent=[-1,0,0,1,1,3], k=2` → **`1`**
   （只有节点5深度3>2；它的父节点3深度2<=2，是唯一的顶层超标点）
2. **一族超标叶子在同一个"已超标"祖先下面，应该只算 1 次**：
   `parent=[-1,0,1,2,2,2], k=1` → **`1`**
   （树：0-1-2，2下面挂3个叶子3,4,5；深度：0,1,2,3,3,3。超标(>1)的是节点2,3,4,5。节点2的父节点1
   深度1<=1，节点2是顶层超标点；节点3/4/5的父节点是2，而2自己深度2>1也超标，所以3/4/5不算顶层——
   算上节点2那一刀已经把它们都删了。答案 1，不是 4。）
3. **同样 3 个叶子，但挂在"未超标"的父节点下面，应该算 3 次**：
   `parent=[-1,0,1,1,1], k=1` → **`3`**
   （树：0-1，1下面挂3个叶子2,3,4；深度：0,1,2,2,2。节点1深度1<=1未超标。节点2/3/4深度2>1超标，
   它们的父节点1未超标，所以各自都是顶层超标点，答案 3。）

### Part 3
1. **官方例子**：`tree_nodes=4, tree_from=[3,1,2], tree_to=[2,3,4], max_operations=1` → **`2`**
   （边：3→2、1→3、2→4，构成链 1→3→2→4。`height(4)=0, height(2)=1, height(3)=2`。二分验证：
   `total_ops(2)=1<=1` 可行；`total_ops(1)=2>1` 不可行。所以答案是 2——剪掉边 2→4，把 4 直接接到
   根1下面，新树分支 1-3-2（高度2）和 1-4（高度1），最大高度2。）
2. **不需要任何操作（0 ops 已满足）**：`tree_nodes=4, tree_from=[1,1,1], tree_to=[2,3,4],
   max_operations=0` → **`1`**（根1带3个叶子，原始高度就是1；`total_ops(1)=0<=0` 直接可行，
   不需要任何换根操作）。
3. **更宽的分支树，手推递归**：`tree_nodes=6, tree_from=[1,1,2,2,3], tree_to=[2,3,4,5,6]`
   （树：1→2,3；2→4,5；3→6；heights: 4=0,5=0,6=0,2=1,3=1,1=2）。
   - `max_operations=1` → **`2`**（原高度就是2；`total_ops(1)`手推 = 3，>1不可行，所以答案停在
     原高度2，不能再降）。
   - `max_operations=3` → **`1`**（`total_ops(1)=3<=3`可行：需要把3个叶子4,5,6全部单独剪掉——
     注意"剪中间节点2或3"救不了，因为剪完2之后它的孩子4,5会落在深度2，仍然超过H=1，所以2和3
     两个中间节点都不值得剪，必须逐叶剪，恰好花3刀）。

## 隐藏测试边界清单

- **三个 part 各自的编号/深度约定不要混用**：Part 1 是 1-indexed 根深度1，Part 2 是 0-indexed
  根深度0，Part 3 是 1-indexed、高度按边数（根单独一个点=0）。
- 单节点树（只有根）：Part 1/2 答案应为空/0；Part 3 原始高度就是 0。
- `k` / `H` / `max_operations` = 0（最严格情况）。Part 3 里 `H=0` 意味着"树里只能有根节点"——
  只要还有别的节点，无论 `max_operations` 给多大都不可行（见上面的 `H=0` 特判说明）。
- `k` / `max_operations` 已经满足、不需要任何删除或操作（答案是空集合/0/原始高度）。
- Part 2："顶层超标点"去重逻辑：同一个已超标祖先下面一堆超标后代只算 1 次（见 worked example 2 vs 3
  的对比）。
- Part 3："剪中间节点救不了深层后代"的情况（worked example 3 的 `max_operations=1→2` 分支）——
  剪一刀不一定比逐叶剪便宜，取决于树形状。
- **极端偏斜（链状）树**，大小到约 1000-2000：这是这题真正的性能考点（见下方"复杂度与实测的
  偏差说明"——链状树会让 Part 3 的递归退化到接近平方级，不是线性）。

## 变体

- Part 3 的原题也常见"给定 max_operations 求最小高度"反过来问"给定目标高度求最少操作数"——本题
  的 `total_ops(H)` 子过程本身就是反过来问法的答案，等价。
- 有的转述版本让候选人只写 `minimumDepthDeletions` / `minimumSubtreeDeletionsForDepth` /
  `getMinimumHeight` 三个独立函数，不需要 stdin/stdout；这里通过 `PART` 行 + `main()` 同时覆盖。

## 来源与置信度

- https://www.fastprep.io/problems/snowflake-minimum-nary-tree-deletions — Part 1，MED。
- https://prachub.com/coding-questions/prune-a-multiway-tree-to-a-maximum-depth — Part 2，MED。
- https://www.fastprep.io/problems/snowflake-minimum-height — Part 3，MED。
- 综合置信度 MED-HIGH：三个来源相互独立但主题高度一致（"树高压缩"反复出现在 Snowflake 的 OA 与
  电面题库里），个别来源未逐字验证细节故不评 HIGH。

## 考什么

skills: **S04** 树：深度计算、删叶子/剪子树、换根 · 多约定题面下的"契约先行"（先把每个 part 自己
的编号/深度基准写清楚，再动手）· 迭代化避免递归深度问题（Part 3 用显式栈算高度）· 复杂度实测与
诚实标注（见 REPORT.md）。
