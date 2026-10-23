# 基础课 · 有序 Map：二叉搜索树、红黑树、跳表，与 `TreeMap` / `ConcurrentSkipListMap`

> 配套代码：[`examples/TreeDemo.java`](examples/TreeDemo.java)（普通 BST 的高度实验、40 行跳表、`TreeMap`/`ConcurrentSkipListMap` 的导航 API 演示）。
> 前置：O(log n)、折半的直觉；建议先读堆一章（树的数组布局）。

---

## 0. 这一章在讲什么

`HashMap` 能 O(1) 回答「key = 100 的值是多少」，但回答不了：

* 「所有 key 里最小的是哪个？」（订单簿的**最优卖价**）
* 「≤ 104 的最大 key 是哪个？」（**前驱 / 向下取整**）
* 「key 在 [103, 110) 之间的全部条目」（**范围查询**）
* 「按 key 从小到大遍历」

这些必须**按 key 有序**组织数据。三种做法：

1. **二叉搜索树（BST）**：最直观，但会退化。
2. **平衡树（红黑树）**：给 BST 加「自动保持矮胖」的规则，`TreeMap` 就是红黑树。
3. **跳表（skip list）**：用随机数代替复杂规则，天然适合并发，`ConcurrentSkipListMap` 就是跳表。

面试不会让你手写红黑树，但会问：为什么 `TreeMap` 是 O(log n)？为什么不直接用普通 BST？`TreeMap` 和 `HashMap` 怎么选？`firstEntry` 和 `floorKey` 有何区别？何时用 `ConcurrentSkipListMap`？

---

## 1. 问题：为什么不用「排好序的数组」或「HashMap + 排序」

| 方案 | 取最小 | 插入 | 范围查询 | 缺点 |
|---|---|---|---|---|
| 无序数组/`HashMap` | O(n) | O(1) | O(n) | 找最小、范围都要全扫 |
| 排好序的 `ArrayList` | O(1) | **O(n)**（二分找位置 O(log n)，但要挪元素） | O(log n + k) | 插入/删除慢 |
| `HashMap` + 每次用时排序 | O(n log n) | O(1) | O(n log n) | 排序太贵 |
| **平衡树 / 跳表** | **O(log n)** | **O(log n)** | **O(log n + k)** | 常数较大 |

订单簿：每秒几十万次「新增价位 / 撤单后删价位」，每次撮合还要「取最优价」。排好序的数组插入 O(L)（L 是价位数），平衡树 O(log L)——这就是价位放进有序 Map 的动机。

---

## 2. 二叉搜索树（Binary Search Tree, BST）

### 2.1 是什么

一棵二叉树，每个节点存一个 key，满足：

> **左子树的所有 key < 本节点的 key < 右子树的所有 key。**（对每个节点都成立）

```text
             50
           /    \
         30      70
        /  \    /  \
      20   40  60   80
```

### 2.2 为什么这个结构有用：查找 = 每一步丢掉一半

查 key = 60：从根 50 起。60 > 50 → 只可能在右边，整个左子树不用看；到 70，60 < 70 → 左边；到 60，找到，共 3 步。

```java
// 在 BST 里找 key：每步向左或向右，最多走「树高」步
static Node find(Node root, int key) {
    Node cur = root;
    while (cur != null) {
        if (key == cur.key) return cur;
        cur = key < cur.key ? cur.left : cur.right;
    }
    return null;
}

static final class Node {
    final int key;
    Node left, right;
    Node(int key) { this.key = key; }
}
```

### 2.3 三个基本操作

* **查找 / 插入**：沿「小去左、大去右」走到空位，插入新节点，O(树高)。
* **最小值**一直向左走到头，**最大值**一直向右走到头，O(树高)——就是 `firstKey()`/`lastKey()`。
* **中序遍历**（左 → 自己 → 右）得到**从小到大**，这就是 `TreeMap` 迭代有序的原因。
* **删除**：叶子直接删；只有一个孩子，让孩子顶替；有两个孩子，用「右子树的最小节点」（后继）替换它，再删掉那个后继。

**前驱/后继（floor / ceiling 的基础）**：`ceilingKey(x)`（≥ x 的最小 key）= 查找 x 的过程中**每次向左拐时记下当前节点**，最后一次记下的就是答案。例 `ceiling(55)`：50 → 55 > 50 向右（不记）；70 → 55 < 70 向左（记 70）；60 → 55 < 60 向左（记 60）；60 的左孩子为空，结束。答案 60 ✓。

### 2.4 致命问题：BST 会退化成链表

BST 所有操作是 O(**树高**)，不是 O(log n)，树高取决于**插入顺序**：

依次插入 1, 2, 3, 4, 5：

```text
  1
   \
    2
     \
      3
       \
        4
         \
          5
```

树高 = 5 = n，查找一次要走 n 步 → 退化成链表。

实验（`TreeDemo` 第 1 部分，n = 5000 个不同 key）：

```text
sorted inserts: height 5000  (a linked list)
random inserts: height 28  (log2(5000) = 12.3)
```

* 已排序输入：高度 5000 = n。
* 随机输入：高度 28，约 log₂ n 的 2.3 倍（随机构造的 BST 期望高度是 O(log n)，精确常数约 3 log₂ n）。

**为什么是真实风险**：订单簿价位、时间戳、自增 id **常常递增**——恰好是 BST 的最坏输入。生产环境不能用普通 BST。

---

## 3. 为什么要「平衡」：一个自我修复的 BST

### 3.1 想法

每次插入/删除后**检查树是否太歪**，歪了就局部调整，让高度始终 O(log n)。基本动作叫**旋转（rotation）**。

### 3.2 旋转：改变形状但不改变顺序

```text
   右旋 (rotate right at y)
        y                       x
       / \                     / \
      x   C        ──▶        A   y
     / \                         / \
    A   B                       B   C

   左旋是它的逆操作。
```

旋转前后中序遍历都是 `A x B y C`——**顺序没变，只是 x 和 y 的上下关系换了**，所以随时可用来调整形状而不破坏 BST 性质，且只改常数个指针，O(1)。

### 3.3 平衡树的几种流派

| 名称 | 平衡规则 | 特点 |
|---|---|---|
| AVL 树（1962） | 任何节点左右子树高度差 ≤ 1 | 最矮，查找最快；插入删除旋转较多 |
| **红黑树**（Bayer 1972；Guibas–Sedgewick 1978） | 给节点染色，用染色规则间接限制高度 | 查找略慢于 AVL，插入删除旋转少（插入 ≤ 2 次，删除 ≤ 3 次）；**JDK `TreeMap`、C++ `std::map`、Linux 内核调度器（CFS）都用** |
| B 树 / B+ 树 | 一个节点存很多 key，所有叶子同深度 | 为磁盘设计：一次读一个块，树很矮；数据库索引的主力 |
| Treap、Splay 等 | 随机优先级 / 自调整 | 实现简单，不保证最坏 |

---

## 4. 红黑树（Red-Black Tree）直觉

> 本节**不是完整证明**，目标是回答「为什么高度是 O(log n)」和「`TreeMap` 内部大概在干什么」。

### 4.1 规则（CLRS 的五条）

每个节点染成红或黑，满足：

1. 每个节点非红即黑。
2. **根是黑的。**
3. 所有叶子（空指针 NIL）算黑的。
4. **红节点的两个孩子都是黑的**（所以不会有两个红节点相连）。
5. **从任一节点到它的所有后代叶子的路径上，黑节点数相同**（称为该节点的「黑高度」）。

```text
          38(B)
         /     \
      19(R)    41(B)
      /   \       \
   12(B) 31(B)    50(R)
```

（括号里是颜色。路径 38→19→12→NIL 的黑节点：38, 12 共 2 个；38→41→NIL：38, 41 共 2 个；38→41→50→NIL：38, 41 共 2 个；红节点 19、50 的孩子均为黑或 NIL ✓。）

### 4.2 为什么这五条保证高度 O(log n)（证明草图）

设树高为 h，根的黑高度为 bh。

1. 规则 4：**任何根到叶路径上红节点不相邻**，至少一半是黑的，所以 **bh ≥ h/2**。
2. 黑高度为 bh 的子树至少有 **2^bh − 1** 个内部节点。（归纳：bh = 0 是空树，0 个；否则两个孩子的黑高度至少 bh − 1，各至少 2^(bh−1) − 1 个，加自己共 2^bh − 1。）
3. 所以 n ≥ 2^bh − 1 ≥ 2^(h/2) − 1，解得 **h ≤ 2 log₂(n + 1)**。

红黑树最高是完美平衡树的 2 倍；n = 10⁶ 时最高约 40 层（实际平均 20–25 层）。

**直觉版**：规则 5 让所有路径黑节点数相同，规则 4 禁止连续红色，所以最长路径（红黑交替）至多是最短路径（全黑）的 2 倍，树不可能比 2 倍更歪。

### 4.3 插入大致做什么

1. 按 BST 规则插入新节点，**染红**（红色不破坏规则 5）。
2. 若父亲也是红的（违反规则 4），看**叔叔**（父亲的兄弟）：
   * 叔叔是红：父亲和叔叔染黑，爷爷染红，把爷爷当新节点继续往上查（**重染色**，只改颜色，可能一路传到根）。
   * 叔叔是黑：做一次或两次**旋转** + 重染色，问题彻底解决，停止。
3. 最后把根染黑。

插入代价 = 找位置 O(log n) + 最多 O(log n) 次重染色 + **最多 2 次旋转**；删除类似，最多 3 次旋转。

### 4.4 另一个角度：红黑树 = 2-3 树（左倾红黑树）

2-3 树每个节点有 1 或 2 个 key（2 或 3 个孩子），**所有叶子同深度**。

2-3 树的插入：往一个已有 2 个 key 的节点里再塞一个，变成 3 个 key，就「分裂」：
把中间的 key 推到父亲里。分裂一路向上，只有根分裂时整棵树才长高一层。
所以整棵树永远是「完美平衡」的。

1. 起点：一个节点 `[10 | 20]`。
2. 插入 15：节点变成 `[10 | 15 | 20]`，过满。
3. 分裂：中间的 15 推上去成为新的根 `[15]`，左孩子 `[10]`，右孩子 `[20]`。

红黑树是把「2-3 树里的一个 3-节点」用「一条红色的边把两个二叉节点粘在一起」表示。红边 = 「这两个 key 在同一个 2-3 节点里」；规则 4（不连续红）= 一个 2-3 节点至多 2 个 key；规则 5（黑高度相同）= 所有叶子同深。这样「旋转 + 重染色」就是 2-3 树的「分裂/合并」。

### 4.5 代价：常数不小

O(log n) 里每一层都是一次**指针跳转**，节点散落在堆里，层数 × 缓存未命中 = 慢。100 万个随机 int key：

```text
HashMap<Integer,Integer> put 60 ns, get 10 ns
TreeMap<Integer,Integer> put 239 ns, get 215 ns
```

`TreeMap.get` 比 `HashMap.get` 慢约 20 倍，是 O(log n) 与 O(1) 加缓存行为（指针追逐）叠加的结果。**只有真的需要有序时才付这个代价。**

---

## 5. 跳表（Skip List）

### 5.1 动机：平衡树很难做成无锁并发

红黑树的旋转要同时改好几个节点的指针，重染色可能从叶子影响到根；让多线程同时插入/删除而不加全局锁非常难。

William Pugh 1990 年提出跳表：**用抛硬币代替复杂的平衡规则**，每次修改只动局部少量指针，天然适合无锁/细粒度锁并发。

### 5.2 是什么：多层有序链表

普通有序链表查找要一个个走，O(n)：

第 0 层（全部）：`head → 1 → 3 → 5 → 7 → 9 → 11 → 13 → 15 → NIL`

加一层「快车道」：每隔一个节点提一层，快车道上的节点指向快车道上的下一个，再来一层更快的……

| 层 | 从 head 往右依次经过 |
|---|---|
| 第 3 层 | head → 11 → NIL |
| 第 2 层 | head → 5 → 11 → NIL |
| 第 1 层 | head → 3 → 5 → 9 → 11 → 15 → NIL |
| 第 0 层 | head → 1 → 3 → 5 → 7 → 9 → 11 → 13 → 15 → NIL |

**查找 13**：从最高层的 head 出发。

1. 层 3：head → 11（11 < 13，前进）→ NIL（超过了），下降一层，停在 11。
2. 层 2：从 11 往右：NIL，下降。
3. 层 1：从 11 往右：15 > 13，不前进，下降。
4. 层 0：从 11 往右：13 = 13，找到。

路径：head →（层 3）11 →（层 1 下降，层 0）13，只经过了 3 个节点，而不是 7 个。

规则：**每层都「能往右走就往右，会超过就下降」**，像坐高铁换乘慢车。

### 5.3 层数怎么定：抛硬币

完美的「隔一个提一层」需要插入时重排整条链表，太贵。Pugh 的办法：插入时**抛硬币决定新节点有几层**：

```text
抛硬币：正面继续往上一层，反面停。
P(至少 1 层) = 1,  P(至少 2 层) = 1/2,  P(至少 3 层) = 1/4, ...
```

第 i 层约 n/2^i 个节点，总共约 n + n/2 + n/4 + … = **2n** 个指针（期望）。无需全局重排：插入只改新节点和它前驱的指针。

### 5.4 复杂度：期望 O(log n)（直觉证明）

从找到的节点倒着看（backward analysis）：从底层目标节点出发，每步要么「向上」要么「向左」；某个节点「是否有更高一层」是独立抛硬币：1/2 向上，1/2 向左。共需向上约 log₂ n 层，期望总步数 2 log₂ n，期望时间 O(log n)。

注意是**期望**，不是最坏：最坏（所有节点只有 1 层）O(n)，概率随 n 指数级消失。

**实验**（`TreeDemo` 第 2 部分，向手写跳表按**升序**插入 100 万个 key——普通 BST 的最坏输入）：

```text
lanes used: 26 (log2(n) = 19.9), lookups found: 1000 of 1000
```

升序输入对跳表毫无影响：层数靠硬币，与 key 顺序无关。最高层数 26 略多于 log₂ n，是少数节点运气好。

### 5.5 最小的 Java 实现

`TreeDemo.SkipList` 只有 40 行：

```java
import java.util.Random;

public class MiniSkipList {
    static final int MAX_LEVEL = 32;

    static final class Node {
        final int key;
        final Node[] next;                         // next[i] = 第 i 层的下一个节点
        Node(int key, int level) { this.key = key; this.next = new Node[level]; }
    }

    final Node head = new Node(Integer.MIN_VALUE, MAX_LEVEL);
    final Random rnd = new Random(1);
    int levels = 1;                                // 当前实际用到的最高层数

    int randomLevel() {                            // 抛硬币
        int lvl = 1;
        while (lvl < MAX_LEVEL && rnd.nextBoolean()) lvl++;
        return lvl;
    }

    boolean contains(int key) {
        Node x = head;
        for (int i = levels - 1; i >= 0; i--) {    // 从最高层开始
            while (x.next[i] != null && x.next[i].key < key) x = x.next[i];   // 能往右就往右
        }                                           // 否则下降一层
        x = x.next[0];
        return x != null && x.key == key;
    }

    void insert(int key) {
        Node[] update = new Node[MAX_LEVEL];       // 每一层「插入点的前驱」
        Node x = head;
        for (int i = levels - 1; i >= 0; i--) {
            while (x.next[i] != null && x.next[i].key < key) x = x.next[i];
            update[i] = x;
        }
        int lvl = randomLevel();
        if (lvl > levels) { for (int i = levels; i < lvl; i++) update[i] = head; levels = lvl; }
        Node n = new Node(key, lvl);
        for (int i = 0; i < lvl; i++) { n.next[i] = update[i].next[i]; update[i].next[i] = n; }   // 像链表插入，每层一次
    }

    public static void main(String[] args) {
        MiniSkipList s = new MiniSkipList();
        for (int i = 0; i < 100; i++) s.insert(i * 2);
        System.out.println(s.contains(42) + " " + s.contains(43));   // true false
    }
}
```

### 5.6 红黑树 vs 跳表

| | 红黑树（`TreeMap`） | 跳表（`ConcurrentSkipListMap`） |
|---|---|---|
| 最坏复杂度 | **O(log n) 保证** | 期望 O(log n)，最坏 O(n)（概率极小） |
| 实现复杂度 | 高（旋转、case 分析） | 低（链表 + 抛硬币） |
| 修改的局部性 | 旋转/重染色可能影响到根 | 只改动前驱的几个指针 |
| 并发 | 难做无锁，通常整棵树加锁 | **容易做成无锁**（CAS） |
| 内存 | 每节点 3 个指针 + 颜色 | 平均每节点 2 个 next 指针 + 索引节点 |
| 范围扫描 | 中序遍历，要回溯 | 在第 0 层顺着链表走，**很快** |
| 单线程速度 | 更快（put 约 230 ns） | 更慢（put 约 390 ns） |

---

## 6. Java API：`TreeMap` 与 `ConcurrentSkipListMap`

### 6.1 它们的类型层次

* `Map`
  * `SequencedMap`（Java 21）
    * `SortedMap`：`firstKey`、`lastKey`、`headMap`、`tailMap`、`subMap`、`comparator`
      * `NavigableMap`：`lowerKey`/`floorKey`/`ceilingKey`/`higherKey`、`firstEntry`、`pollFirstEntry`、`descendingMap`、带 inclusive 参数的 `headMap`/`tailMap`/`subMap`
        * `TreeMap`：红黑树，非线程安全
        * `ConcurrentNavigableMap`
          * `ConcurrentSkipListMap`：跳表，线程安全

声明变量写 `NavigableMap<K, V>`（要导航方法）或 `SequencedMap`（只用首尾）而不是具体类，方便换实现。

### 6.2 导航方法速查（统一用一个例子）

`asks = {101=50, 103=20, 105=70, 110=10}`（价格 → 数量）。输出来自 `TreeDemo` 第 3 部分。

| 方法 | 语义 | 例子 | 结果 | 没有时 |
|---|---|---|---|---|
| `firstKey()` / `lastKey()` | 最小 / 最大 key | | `101` / `110` | **抛** `NoSuchElementException` |
| `firstEntry()` / `lastEntry()` | 最小 / 最大条目 | | `101=50` | 返回 `null` |
| `pollFirstEntry()` / `pollLastEntry()` | 取出并删除最小 / 最大 | | | 返回 `null` |
| `floorKey(k)` | **≤ k** 的最大 key | `floorKey(104)` | `103` | `null`（`floorKey(100)` → `null`） |
| `lowerKey(k)` | **< k** 的最大 key | `lowerKey(103)` | `101` | `null` |
| `ceilingKey(k)` | **≥ k** 的最小 key | `ceilingKey(104)` | `105` | `null` |
| `higherKey(k)` | **> k** 的最小 key | `higherKey(105)` | `110` | `null` |
| `headMap(to)` | key **< to**（不含 to）的视图 | `headMap(105)` | `{101=50, 103=20}` | 空视图 |
| `headMap(to, true)` | key **≤ to** | `headMap(105, true)` | `{101=50, 103=20, 105=70}` | |
| `tailMap(from)` | key **≥ from**（含 from）的视图 | `tailMap(105)` | `{105=70, 110=10}` | |
| `subMap(from, to)` | `[from, to)` | `subMap(103, 110)` | `{103=20, 105=70}` | |
| `descendingMap()` | 反向视图 | | `{110=10, 105=70, 103=20, 101=50}` | |

口诀：**floor / ceiling 含相等，lower / higher 不含相等；`headMap` 默认不含边界，`tailMap` 默认含边界**（"一头一尾不对称"，最常见的 off-by-one）。每个 `xxxKey` 都有 `xxxEntry` 版本（同时返回 key 和 value），省一次 `get`。

### 6.3 视图是「活」的，而且有范围限制

```java
import java.util.*;

public class LiveViews {
    public static void main(String[] args) {
        TreeMap<Integer, Integer> asks = new TreeMap<>(Map.of(101, 50, 103, 20, 105, 70, 110, 10));
        NavigableMap<Integer, Integer> cheap = asks.headMap(104, true);   // 看的是同一棵树，不是拷贝
        asks.put(102, 5);
        System.out.println(cheap);                // {101=50, 102=5, 103=20}  ← 视图随原 Map 变化
        try {
            cheap.put(200, 1);                    // 往视图里写一个超出范围的 key
        } catch (IllegalArgumentException e) {
            System.out.println("key out of range");
        }
    }
}
```

`TreeDemo` 输出：`live view after put(102): {101=50, 102=5, 103=20}` 与 `put outside view range -> IllegalArgumentException`。

**性能坑**：`TreeMap` 子视图的 `size()` 是 **O(元素个数)**（要遍历计数）：100 万 key 的 `TreeMap` 上 `headMap(900_000).size()` 约 3 ms/次。想要「≤ k 的有多少个」(rank) 用 Fenwick 树/order-statistic tree，不要 `headMap(k).size()`。

### 6.4 `firstEntry()` 返回的是快照

Javadoc：「The methods `ceilingEntry(K)`, `firstEntry()`, `floorEntry(K)`, … return `Map.Entry` instances that represent snapshots of mappings as of the time of the call. They do not support mutation of the underlying map via the optional `setValue` method.」

`firstEntry().setValue -> UnsupportedOperationException (snapshot entry)`。改值用 `put(key, newValue)`。

### 6.5 一个撮合循环，演示 `firstEntry` / `pollFirstEntry`

```java
import java.util.*;

public class SweepBook {
    public static void main(String[] args) {
        TreeMap<Integer, Integer> asks = new TreeMap<>(Map.of(101, 50, 103, 20, 105, 70, 110, 10));
        int need = 80;                                              // 买入 80 手，从最低卖价开始吃
        while (need > 0 && !asks.isEmpty()) {
            Map.Entry<Integer, Integer> level = asks.firstEntry();  // 最优价：O(log n)
            int take = Math.min(need, level.getValue());
            System.out.print(take + "@" + level.getKey() + " ");
            need -= take;
            if (take == level.getValue()) asks.pollFirstEntry();    // 吃光，整档删除
            else asks.put(level.getKey(), level.getValue() - take); // 部分成交，更新数量
        }
        System.out.println("-> remaining " + asks);                  // 50@101 20@103 10@105 -> remaining {105=60, 110=10}
    }
}
```

买盘（bids）最优价是**最高价**，所以买盘 `TreeMap` 用 `new TreeMap<>(Comparator.reverseOrder())`，让 `firstEntry()` 返回最高价。

### 6.6 比较器决定「相等」，不是 `equals`

`TreeMap` 判断两个 key 是否相同，**只看比较器是否返回 0**：

```java
import java.util.*;

public class CaseInsensitiveKeys {
    public static void main(String[] args) {
        TreeMap<String, Integer> ci = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
        ci.put("AAPL", 1);
        ci.put("aapl", 2);          // 比较器认为是同一个 key：覆盖值，保留旧 key 对象
        System.out.println(ci + " size=" + ci.size());      // {AAPL=2} size=1
    }
}
```

比较器只比较对象的一部分字段（如只比价格），不同对象就被当成「同一个 key」互相覆盖（Javadoc：「ordering must be consistent with equals」）。**订单簿里同价订单要放进同一个 `TreeMap`，必须让比较器区分它们（价格相同再比序号），或把同价订单放进「价位」的队列里。**

### 6.7 其他坑

* **fail-fast 迭代器**：遍历 `TreeMap` 时修改它（除 `iterator.remove()`）抛 `ConcurrentModificationException`；遍历时删除用 `entrySet().removeIf(...)` 或 `Iterator.remove()`。
* **key 不可变**：放进去后别改变决定比较结果的字段，否则树内部顺序被破坏（同 `PriorityQueue` 的坑）。
* **`null`**：`TreeMap` 自然序下不允许 `null` key；`ConcurrentSkipListMap` 不允许 `null` key 或 value。
* **`TreeMap` 非线程安全**：多线程用 `Collections.synchronizedSortedMap` 或换 `ConcurrentSkipListMap`。

### 6.8 `ConcurrentSkipListMap` 特有的东西

Javadoc 要点：

* 「implements a concurrent variant of SkipLists providing expected average log(n) time cost for the containsKey, get, put and remove operations … Insertion, removal, update, and access operations safely execute concurrently by multiple threads.」
* 迭代器和 spliterator 是 **weakly consistent**（弱一致）：遍历期间别的线程的修改可能看见也可能看不见，但不抛 `ConcurrentModificationException`，也不重复返回同一元素。
* 「bulk operations `putAll`, `equals`, `toArray`, `containsValue`, and `clear` are **not guaranteed to be performed atomically**」。
* 「Like most other concurrent collections, this class does not permit the use of null keys or values」。
* `compute` / `computeIfAbsent` / `merge` 的函数「is **NOT guaranteed to be applied once atomically**」——与 `ConcurrentHashMap` 不同，函数可能被调多次（竞争失败时重试），所以必须无副作用。
* 返回的 `Map.Entry` 都是快照，不支持 `setValue`。
* `size()`：旧资料说是 O(n) 遍历计数；JDK 21 上 100 万条目 `size()` 仅约 0.1 微秒，说明新版本维护了计数器——但别在面试里断言，说「历史上 O(n)，现在的实现不一定，不应依赖」。

**何时用**：多个线程同时读写同一个有序 Map，且读多写少或写操作分散（如多线程更新不同价位）。单线程用 `TreeMap`——更快（put 约 230 ns vs 390 ns）。热点就是「同一个最优价」时跳表也救不了你（所有线程竞争同一个节点），更常见的设计是**单线程拥有订单簿**。

---

## 7. 选择指南：什么时候用哪个

| 需求 | 用什么 | 原因 |
|---|---|---|
| 只要按 key 查/改，不要有序 | `HashMap` | O(1)，最快 |
| 要保持插入顺序遍历 | `LinkedHashMap` | `HashMap` + 双向链表 |
| 取最小/最大、前驱后继、范围查询、有序遍历 | **`TreeMap`** | 红黑树，O(log n) |
| 同上，多线程并发 | **`ConcurrentSkipListMap`** | 跳表，无锁读、细粒度写 |
| 只要反复取最小，不要范围、不要前驱后继 | `PriorityQueue` | 堆更简单更快 |
| 数据几乎不变，只查询 | 排好序的数组 + `Arrays.binarySearch` | 连续内存，缓存友好 |
| key 是有界小整数（如 tick 价位） | **数组下标**，配位图/最优价指针 | O(1)，无指针追逐 |
| 要「第 k 小」「小于 x 的有多少个」 | Fenwick 树 / order-statistic 树 | `TreeMap` 做不到 O(log n) 的 rank |
| 数据比内存大，要持久化的有序索引 | B+ 树（关系数据库）/ LSM-tree（RocksDB 等） | 为磁盘设计 |

### 7.1 与分布式存储的联系

* **LSM-tree**（Log-Structured Merge-tree）的写入路径：先写日志，再写入内存里的有序结构 **memtable**；内存表满了整体排序落盘成不可变的有序文件（SSTable）。LevelDB、RocksDB 的 memtable 默认是**跳表**，HBase 的 MemStore 底层用 `ConcurrentSkipListMap`。选跳表是因为并发写入友好、范围扫描顺着第 0 层走、实现简单。
* **B+ 树**：关系数据库（InnoDB、PostgreSQL）的主索引。每个节点装满一个磁盘页，几百个 key，树高通常只有 3–4 层；叶子用链表串起来，范围扫描顺序读。
* **Redis** 的 `ZSET`（元素较多时）用跳表 + 哈希表：跳表负责按分数排序/范围查询，哈希表负责按成员 O(1) 查分数。

---

## 8. 常见误区

1. **「`TreeMap` O(log n)，所以只比 `HashMap` 慢一点点」。**慢得不止一点点：`get` 215 ns vs 10 ns，约 20 倍——原因是指针追逐，不只是多了 log n 步。
2. **`headMap(k)` 包含 k。**不包含（`headMap(k, true)` 才含）；`tailMap(k)` 包含 k。
3. **用 `firstKey()` 判断空。**空 Map 上 `firstKey()` 抛 `NoSuchElementException`；`firstEntry()` 返回 `null`。循环里用 `firstEntry()` 并判 `null`，或先 `isEmpty()`。
4. **`floorKey` 返回 `null` 时直接解包。**`int p = map.floorKey(x);` 在 `null` 时 NPE。
5. **订单簿里一价位一个订单。**同价订单因比较器相等互相覆盖；key 带序号，或 value 是队列。
6. **`headMap(k).size()` 当 rank 用。**O(n)（6.3）。
7. **遍历中修改。**`for (var e : map.entrySet()) map.remove(...)` → `ConcurrentModificationException`。

---

## 9. 面试追问预演

**Q1：`TreeMap` 为什么是 O(log n)？**
答：「底层是红黑树。五条规则保证最长路径不超过最短路径的两倍，高度不超过 2 log₂(n+1)。get/put/remove 沿一条根到叶的路径走，最多 O(log n) 步；插入删除后用最多常数次旋转加 O(log n) 次重染色恢复规则。」

**Q2：为什么不直接用普通二叉搜索树？**
答：「高度取决于插入顺序，升序插入会退化成链表，O(n)。价格、时间戳、自增 id 恰好常常递增。实验：5000 个升序 key 高度就是 5000，随机的只有 28。」

**Q3：红黑树和跳表，你选哪个？**
答：「单线程要最坏保证用红黑树，即 `TreeMap`。多线程并发读写同一个有序结构用跳表，因为插入只改局部指针，容易做成无锁；JDK 里有现成的 `ConcurrentSkipListMap`。代价是跳表是概率结构，最坏 O(n) 概率极小，单线程也更慢（put 390 ns 对 230 ns）。」

**Q4：订单簿的价位用 `TreeMap`，还有什么更快的方案？**
答：「价格是有界整数时（按 tick 编号）用数组下标 O(1) 访问价位，最优价用指针或位图维护。`TreeMap` 每层一次指针跳转，缓存不友好，100 万 key 上 get 约 200 ns。远离中间价的稀疏价位可回退到 `TreeMap`。」

**Q5：我要一个「第 k 小」或「小于 x 的元素个数」，用 `TreeMap` 行吗？**
答：「不行，`headMap(x).size()` 是 O(n)。用 Fenwick 树（价格离散化后）或者带子树大小的平衡树（order-statistic tree），O(log n)。」

---

## 10. 自测题

**Q1（手算）** 依次向空 BST 插入 `50, 30, 70, 20, 40, 60, 80, 65`，画出树，并写出它的中序遍历。

<details><summary>答案</summary>

```text
            50
          /    \
        30      70
       /  \    /  \
     20   40  60   80
                \
                 65
```

中序遍历（左-根-右）：20 30 40 50 60 65 70 80，升序。65 > 60 → 60 的右孩子。

</details>

**Q2（手算）** 在 Q1 的树里，`ceilingKey(62)` 和 `floorKey(62)` 各是多少？写出路径。

<details><summary>答案</summary>

查 62：50（62>50 向右，floor 候选 50）→ 70（62<70 向左，ceiling 候选 70）→ 60（向右，floor 候选 60）→ 65（62<65 向左，ceiling 候选 65）→ 65 的左孩子为空，结束。`floorKey(62)` = 60，`ceilingKey(62)` = 65。

</details>

**Q3（概念）** 红黑树的规则 4（红节点的孩子必须是黑的）和规则 5（黑高度相同）合起来，为什么推出高度 ≤ 2 log₂(n+1)？

<details><summary>答案</summary>

规则 5 让所有根到叶路径黑节点数都是 bh；规则 4 让红节点不相邻，任何路径至多一半是红的，h ≤ 2·bh。黑高度为 bh 的子树至少 2^bh − 1 个节点，所以 n ≥ 2^bh − 1 ≥ 2^(h/2) − 1，得 h ≤ 2 log₂(n+1)。

</details>

**Q4（代码）** 给定价位表 `TreeMap<Integer,Integer> book`，写一个方法返回「价格在 [lo, hi] 区间内的总数量」。复杂度？

<details><summary>答案</summary>

```java
import java.util.*;

public class RangeSum {
    static long volumeBetween(NavigableMap<Integer, Integer> book, int lo, int hi) {
        long sum = 0;
        for (int qty : book.subMap(lo, true, hi, true).values()) sum += qty;   // [lo, hi]，两端都含
        return sum;
    }

    public static void main(String[] args) {
        TreeMap<Integer, Integer> book = new TreeMap<>(Map.of(101, 50, 103, 20, 105, 70, 110, 10));
        System.out.println(volumeBetween(book, 102, 105));   // 90
    }
}
```

复杂度 O(log n + k)，k 是区间内价位数：O(log n) 找起点，之后顺序遍历 k 个。查询非常频繁时维护前缀和（Fenwick 树）达到 O(log n)。

</details>

**Q5（辨析）** `TreeMap.firstEntry().setValue(0)` 能把最优价位的数量改成 0 吗？

<details><summary>答案</summary>

不能，抛 `UnsupportedOperationException`：`firstEntry()` 返回调用时刻的快照条目。用 `map.put(key, 0)`，或 `pollFirstEntry()` 删除整个价位。

</details>

**Q6（辨析）** 一个 `ConcurrentSkipListMap` 上，线程 A 遍历，线程 B 同时 `put`。A 会抛 `ConcurrentModificationException` 吗？A 一定能看到 B 刚加的元素吗？

<details><summary>答案</summary>

不会抛。迭代器弱一致：可能看见也可能看不见 B 在迭代创建之后的修改，但不重复、不崩溃，也不保证某个一致快照。需要一致快照就用 `TreeMap` + 外部锁，或持久化（不可变）结构。

</details>

**Q7（设计）** 你要做一个本地「定时器」，支持：加入 (到期时间, 任务)、取消某任务、取出所有已到期任务。选 `PriorityQueue` 还是 `TreeMap`？

<details><summary>答案</summary>

取消是关键：`PriorityQueue.remove(Object)` 是 O(n)。用 `TreeMap<Long, List<Task>>` 或 `TreeSet<(到期时间, 序号)>` 加 `HashMap<taskId, key>`，取消 O(log n)；取到期任务用 `headMap(now, true)`。取消很少时，`PriorityQueue` + 懒删除（标记取消，poll 到时丢弃）更快。

</details>

---

「延伸」下一章：CPU 缓存与局部性。
