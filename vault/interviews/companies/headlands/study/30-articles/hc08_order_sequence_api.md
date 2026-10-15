# hc08 · Order Sequence API（Put / Delete + 亚线性前缀查询）—— 讲义

> 题面：`loop/rounds/01_video/hc08_order_sequence_api/problem.md` · 速查：同目录 `REPORT.md` · 代码：同目录 `reference/OrderSequence.java`
> 写法说明见 `study/TEXTBOOK.md`。读者设定：只会基本 Java（类、方法、循环、`ArrayList` / `HashMap` 的基本用法）。
> 题面只有 Put / Delete 的名字和「前缀 count / quantity」「亚线性」几个词有证据，其余 **(reconstructed)**。

---

## 1. 这道题在问什么

### 1.1 用大白话

你在管理一排**排队的订单**。每张订单有一个编号（`id`）和一个数量（`quantity`）。新订单总是**排到队尾**，所以队伍的顺序 = 到达顺序。你要提供这些操作：

* `put(id, qty)`：新订单排到队尾；
* `delete(id, qty)`：把某张订单删掉（或减少数量）；
* `countUpTo(id)`：从队头数到这张订单（含），队伍里一共有几张订单；
* `qtyUpTo(id)`：从队头到这张订单（含），数量加起来是多少；
* `idAt(k)`：队伍里第 k 张订单的编号（我们补的第 4 个接口）。

### 1.2 手算一遍

依次执行（订单写成 `id:数量`）：

```
put(10,5)   队伍: [10:5]
put(20,3)   队伍: [10:5, 20:3]
put(30,7)   队伍: [10:5, 20:3, 30:7]
countUpTo(30) = 3          （队头到 30，共 3 张）
qtyUpTo(20)   = 5 + 3 = 8
delete(20,3)  队伍: [10:5, 30:7]        （20 被整单删掉）
qtyUpTo(30)   = 5 + 7 = 12
idAt(2)       = 30
```

### 1.3 难点在哪里

如果订单有 100 万张，你每次问 `qtyUpTo` 都从队头一张张加，每次要加几十万次。问 100 万次，就是 10^11~10^12 次加法——几分钟。题目说的「**亚线性**（sublinear）查询」就是：**一次查询的时间要比订单数 n 增长得慢**，比如 O(log n)。
这需要一个叫**树状数组（Fenwick tree）**的数据结构。再往下追问：删除之后怎么办？内存会不会越用越多？——这是 Part 3。

---

## 2. 前置知识

### 2.1 前缀和（prefix sum）

**是什么**：数组 `a[1..n]` 的前缀和 `P(i) = a[1] + a[2] + … + a[i]`。「从队头到第 i 张订单的数量之和」就是 `P(i)`。

**为什么需要它**：本题的 `qtyUpTo` 就是前缀和；`countUpTo` 是"每张订单的值都是 1"的前缀和。

**它怎么工作**——两种极端做法：

| 做法 | 查询 `P(i)` | 修改 `a[j]` |
|---|---|---|
| 每次现算（从头加到 i） | O(n) | O(1)（直接改 a[j]） |
| 提前把所有 P 存成数组 | O(1)（直接读） | O(n)（改了 a[j]，后面所有的 P 都要加上变化量） |

两个极端各有一头是 O(n)。订单不断进出（修改很多）、查询也很多时，两个都不行。树状数组的思路是**折中**：查询和修改都做到 O(log n)。

### 2.2 二进制与「最低位的 1」（lowbit）——树状数组的钥匙

**是什么**：任何正整数写成二进制，最右边的那个 `1` 所在的位置，对应的数值叫 **lowbit**。
例：`6 = 110₂`，最右边的 1 在从右数第 2 位，lowbit(6) = `010₂` = 2。`12 = 1100₂`，lowbit = `0100₂` = 4。`7 = 111₂`，lowbit = 1。`8 = 1000₂`，lowbit = 8。

**为什么需要它**：树状数组的核心就是"每个格子负责多长的一段"，而这个长度恰好是 lowbit(下标)。

**怎么算——`i & -i`**：Java 的整数用**补码**表示，`-i` 等于「按位取反再加 1」。以 4 位为例演示 `i = 6`：

```
 i      =  0110
~i      =  1001      （每一位取反）
-i      = ~i + 1 = 1010      （加 1：最右边连续的 1 变 0 并向左进位，进到原来 i 的最低位 1 的位置停下）
 i & -i =  0110
          1010
        = 0010  = 2        ← 只有"最低位的 1"这一位两边都是 1
```

为什么只剩最低位的 1：`~i` 里，原来 i 最低位 1 右边的那些 0 变成了 1，最低位的 1 本身变成了 0；加 1 之后，右边那串 1 全部进位变回 0，进位在最低位的 1 那里变回 1。
所以 `-i` 与 `i` 在"最低位的 1 及其右边"完全一样，在它左边完全相反——两者相与，只剩那一位。

**Java 里怎么写**：`int low = i & -i;`

### 2.3 树状数组（Fenwick tree / Binary Indexed Tree）——从零推导

**目标**：数组 `a[1..n]`，支持 ① `add(i, delta)`：`a[i] += delta`；② `prefix(i)`：求 `a[1]+…+a[i]`；都在 O(log n) 里完成。

**想法**：不存每个 `a[i]`，也不存每个 `P(i)`，而是存**若干段区间的和**，并让每个前缀都能拆成**很少几段**。

**规则**：`tree[i]` 存的是 `a` 在区间 **(i - lowbit(i), i]** 上的和，也就是以 i 结尾、长度为 lowbit(i) 的那一段。

以 n = 8 为例，数组 `a = [3, 1, 4, 1, 5, 9, 2, 6]`（下标 1..8）：

| i | 二进制 | lowbit | tree[i] 负责的区间 | tree[i] 的值 |
|---|---|---|---|---|
| 1 | 0001 | 1 | (0,1] = a1 | 3 |
| 2 | 0010 | 2 | (0,2] = a1..a2 | 3+1 = 4 |
| 3 | 0011 | 1 | (2,3] = a3 | 4 |
| 4 | 0100 | 4 | (0,4] = a1..a4 | 3+1+4+1 = 9 |
| 5 | 0101 | 1 | (4,5] = a5 | 5 |
| 6 | 0110 | 2 | (4,6] = a5..a6 | 5+9 = 14 |
| 7 | 0111 | 1 | (6,7] = a7 | 2 |
| 8 | 1000 | 8 | (0,8] = a1..a8 | 31 |

画成"每个格子管多长"的图（下标 1..8，横条表示 tree[i] 管的范围）：

```
下标:   1    2    3    4    5    6    7    8
a:      3    1    4    1    5    9    2    6
t[1]:  [3]
t[2]:  [  4   ]
t[3]:            [4]
t[4]:  [        9        ]
t[5]:                      [5]
t[6]:                      [   14  ]
t[7]:                                [2]
t[8]:  [                31                 ]
```

#### 查询 `prefix(i)`：把 [1, i] 拆成若干段

观察：`prefix(7)` 要 a1..a7。从 7 出发：
* `tree[7]` 管 (6,7]，拿走；剩下 a1..a6，即 `prefix(6)`，下标 7 - lowbit(7) = 7 - 1 = 6。
* `tree[6]` 管 (4,6]，拿走；剩下 a1..a4，下标 6 - lowbit(6) = 6 - 2 = 4。
* `tree[4]` 管 (0,4]，拿走；下标 4 - 4 = 0，结束。

`prefix(7) = tree[7] + tree[6] + tree[4] = 2 + 14 + 9 = 25`。核对：3+1+4+1+5+9+2 = 25 ✓。

规律：**每一步 `i -= i & -i`，就是把 i 二进制里最低位的 1 抹掉**。7 = 111₂ → 110₂ → 100₂ → 000₂，三步，因为 7 里有三个 1。
所以一次查询的步数 = i 的二进制里 1 的个数 ≤ log₂(n)。这就是 O(log n) 的来源。

```java
long prefix(int i) {
    long r = 0;
    for (; i > 0; i -= i & -i) r += tree[i];    // 抹掉最低位的 1，直到 i = 0
    return r;
}
```

#### 修改 `add(i, delta)`：把变化加到所有"管着 i 的格子"

`a[3]` 增加 10 之后，哪些 `tree[j]` 的区间包含下标 3？看表：`tree[3]`（(2,3]）、`tree[4]`（(0,4]）、`tree[8]`（(0,8]）。
从 3 出发："下一个管着我的格子"是谁？`3 + lowbit(3) = 3 + 1 = 4`；`4 + lowbit(4) = 8`；`8 + 8 = 16 > n`，结束。

```
add(3, +10):   i = 3 → 更新 tree[3]
               i = 3 + 1 = 4 → 更新 tree[4]
               i = 4 + 4 = 8 → 更新 tree[8]
               i = 8 + 8 = 16 > 8 → 停
```

为什么 `i += lowbit(i)` 恰好跳到"下一个覆盖 i 的格子"：加上 lowbit 会让最低位的 1 进位，变成更高位的 1，得到的数 j 的 lowbit 更大（区间更长），而且区间 (j - lowbit(j), j] 恰好把 i 所在的区间包含进去。每一步 lowbit 至少翻倍，所以最多 log₂(n) 步。

```java
void add(int i, long delta) {
    for (; i <= n; i += i & -i) tree[i] += delta;    // 跳到下一个管着 i 的格子
}
```

**总结**：两个操作都是 O(log n)；只用一个数组、循环体里只有加法和位运算，代码十来行。

### 2.4 用树状数组"数个数"和"找第 k 个"

本题要两棵树：
* `sum[]`：按"插入下标"累加**数量** → `qtyUpTo`；
* `cnt[]`：每张活跃订单在自己的下标处记 1 → `countUpTo`，**也用来找第 k 张**。

**找第 k 张（`idAt`）：在树上二分下降**。`cnt` 树里，`tree[pos + 2^j]` 恰好是区间 `(pos, pos + 2^j]` 里的活跃订单数（当 pos 是 2^(j+1) 的倍数时）。从大步长到小步长试探：

例：有 8 个下标，下标 3 已被删除（洞），活跃的是 1,2,4,5,6,7,8。`cnt` 数组 `[1,1,0,1,1,1,1,1]`，对应的树：`t1=1, t2=2, t3=0, t4=3, t5=1, t6=2, t7=1, t8=7`。找第 4 张：

```
pos = 0, rem = 4
步长 8: 看 t[8]=7，7 < 4? 不是 → 第 4 张在这一整块之内，不跳
步长 4: 看 t[0+4]=t4=3，3 < 4? 是 → 前 4 个下标里只有 3 张，第 4 张在后面：pos = 4, rem = 4-3 = 1
步长 2: 看 t[4+2]=t6=2，2 < 1? 不是 → 不跳
步长 1: 看 t[4+1]=t5=1，1 < 1? 不是 → 不跳
结果: 下标 pos+1 = 5
```

核对：活跃下标依次是 1,2,4,5,… 第 4 个是下标 5 ✓。每一步确定答案二进制里的一位，所以 O(log n)。**要求数组大小是 2 的幂**，步长才能从最高位对齐——这是我们的容量总是 2 的幂的原因之一。

### 2.5 哈希表：id → 下标

**是什么 / 为什么**：`countUpTo(id)` 拿到的是订单 id（可以是任意 `long`），要先换算成它的"插入下标"，用 `HashMap<Long, Integer>`，平均 O(1)。（装箱的代价见 hc05 讲义 2.7，这里的 `HashMap<Long,Integer>` 是可以接受的简化。）

### 2.6 摊还分析（amortized analysis）

**是什么**：有些操作偶尔很贵、大多数时候很便宜。把贵的操作的代价**平摊**到之前的便宜操作上，算出"平均每个操作多少"，叫摊还复杂度。

**例子**：`ArrayList.add` 在数组满时要把所有元素复制到一个两倍大的新数组（O(n)），但这要先经过 n 次便宜的 add 才会发生一次。n 次 add 总代价 ≈ n + n（复制）= 2n，平均每次 O(1)。

**为什么需要它**：本题 Part 3 的压缩（compaction）是一次 O(容量) 的重建，要证明"平均到每次 put 仍是 O(1)"——靠的就是"压缩之后留出足够多的空位，下一次压缩之前至少要做这么多次 put"。

### 2.7 数组的"留洞"与"压缩"

**是什么**：数组里删掉一个元素有两种做法：把后面的全部往前挪（O(n)，下标全变）；或者**原地做个记号，留下一个洞**（O(1)，其他元素下标不变）。
**为什么用留洞**：我们的 Fenwick 树是按**下标**组织的，如果删除时往前挪，所有后面订单的下标都变了，树要重建。留洞只需要在树里把这个下标的值改成 0。
**代价**：洞永远占着位置。下标只增不减，长期运行下数组会越来越长。**压缩**就是定期把洞都去掉、按原顺序把活的元素重新编号。

### 2.8 Java 21 的新东西（本题用到）

* `record`、`sealed`、`switch` 模式匹配：见 hc05 讲义第 6 节；
* `SequencedCollection`：`entries()` 返回的 `List` 可以直接 `getFirst()` / `getLast()` / `reversed()`；
* `Math.addExact`：溢出时抛异常。

---

## 3. 从最笨的解法开始

**最笨**：`ArrayList<long[]>` 按到达顺序存 `{id, qty}`。

```java
void put(long id, long qty)   { if (find(id) >= 0) throw ...; list.add(new long[]{id, qty}); }          // find 是 O(n)
long delete(long id, long q)  { int i = find(id); ... list.remove(i);  /* 或减量 */ }                   // O(n)：扫描 + 往前挪
long countUpTo(long id)       { return find(id) + 1; }                                                    // O(n)
long qtyUpTo(long id)         { long s = 0; for (long[] e : list) { s += e[1]; if (e[0] == id) break; } return s; }   // O(n)
long idAt(int k)              { return list.get(k - 1)[0]; }                                              // O(1)
```

**正确、又短**，Part 1 就该先写出这个（它还可以当之后"对拍"的参照）。

**慢在哪**：每个操作 O(n)。实测（本机）：5 万张订单、5 万次随机 `qtyUpTo`，朴素扫描需要约 **1.9 秒**；规模扩大 10 倍（50 万 / 50 万），时间大约是 100 倍 ≈ **190 秒**。同样的 50 万 + 50 万，树状数组版本约 **60 毫秒**。
所以题目说"sublinear"——它在等你拿出 O(log n) 的方案。

---

## 4. 一步一步改进

### 第 1 步：一个纯 `HashMap` 就够做 delete / 查找吗？

**发现问题**：朴素版里 `find(id)` 是 O(n)。
**想法**：`HashMap<Long, Integer> indexOf`：id → 下标，O(1)。
**问题**：下标是数组里的位置，删除一个元素后后面的下标都变了——维护 map 里的值也是 O(n)。
→ 这提示我们要**让下标不变**：删除只"留洞"。

### 第 2 步：下标只增不减，删除留洞

**想法**：每张订单在 put 时领一个递增的下标 `nextIndex++`，永远不变。删除时只把 `qtyByIdx[i] = 0`。这样 `indexOf` 里的值永远有效。
**新问题**：`qtyUpTo(id)` 现在是"对下标 1..indexOf(id) 求 qty 的和"，仍然 O(n)（要跳过洞扫过去）。但这已经是一个标准的"**数组前缀和 + 单点修改**"问题了。

### 第 3 步：套上树状数组

**想法**：`sum[]` 树按下标累加数量，`cnt[]` 树累加"是否活着"（活 = 1）。
* `put`：在新下标 `i` 上 `addCnt(i, +1)`、`addSum(i, qty)`；
* `delete`（整单）：`addCnt(i, -1)`、`addSum(i, -qty)`；
* `countUpTo(id)` = `prefixCnt(indexOf(id))`，`qtyUpTo(id)` = `prefixSum(indexOf(id))`；
* `idAt(k)`：在 `cnt` 树上二分下降（2.4 节），得到下标，再读 `idByIdx[下标]`。
**为什么这样对**：洞在两棵树里的值都是 0，不会影响任何前缀和；订单的先后顺序 = 下标的先后顺序，所以"从队头到订单 X"= 下标 1..idx(X)。
**新复杂度**：四个查询 / 修改都是 O(log n)，`put` 也是 O(log n)。

### 第 4 步：部分删除

**问题**：`delete(id, qty)` 里 `qty` 小于剩余量时怎么办？
**想法**：订单**不移除**，位置不变，只是数量减少：`addSum(i, -qty)`，`qtyByIdx[i] -= qty`；`cnt` 树**不动**（订单还活着）。只有剩余量变 0 才 `addCnt(i, -1)` 并从 `indexOf` 里删除。
**要检查的**：`qty ≤ 0` → 参数错；`qty >` 剩余 → 参数错（状态不变）；未知 id → `NoSuchElementException`。

### 第 5 步：下标空间写满了

**发现问题**：Fenwick 数组大小是固定的 `capacity`。每次 `put` 领一个新下标，删除不释放下标。哪怕任何时候只有 1000 张活跃订单，处理 200 万张订单也需要 200 万大小的数组——**内存跟着"历史总量"走，而不是"当前活跃量"**。这就是题目标签里的 "memory management"。

**想法 A（倍增，不够好）**：写满就把数组扩成两倍。——对"活跃订单很少"的场景白白浪费，数组只增不减。
**想法 B（压缩 compaction）**：写满时，把活跃订单**按原顺序**重新编号为 1..m，丢掉所有洞，重新建树。新容量取"够用的最小 2 的幂"，所以活跃订单少时容量还会**缩小**。

**压缩后的容量取多少**：太紧（刚好 m+1）会导致压缩完马上又写满，每次 put 都压缩 → O(n) 每次，退化。要保证压缩后**留出足够多的空位**。我们取

```
newCap = 2 的幂 ≥ max(初始容量, m + m/2 + 1)
```

**摊还分析**：压缩一次的代价 O(旧容量 + 新容量)。压缩之后空位数 = newCap − m ≥ newCap/3（因为 newCap ≥ 1.5m + 1，所以 m ≤ newCap/1.5，空位 ≥ newCap − newCap/1.5 = newCap/3）。
下一次压缩之前至少要完成 newCap/3 次 put。所以每次 put 分摊到的压缩代价 ≤ O(newCap) / (newCap/3) = O(3) = **O(1)**。

**线性建树**：压缩后要重建 Fenwick 树。逐个 `add` 是 O(m log n)；有 O(n) 的做法：先把每个下标的原始值填进 `tree[i]`，然后从小到大遍历 i，把 `tree[i]` 加到它的"父节点" `tree[i + lowbit(i)]` 上：

```java
for (int i = 1; i <= newCap; i++) {
    int p = i + (i & -i);
    if (p <= newCap) { cnt[p] += cnt[i]; sum[p] += sum[i]; }
}
```

为什么对：`tree[p]` 管的区间 = 它自己那一格 + 若干个"孩子"区间，孩子正是满足 `j + lowbit(j) = p` 的那些 j；从小到大处理，保证 `tree[i]` 加到父节点时它已经收齐了自己的孩子。

**实测**：活跃订单 ≤ 1000，200 万次 put + 删除最老的循环：容量稳定在 **2048**（1000 + 500 + 1 = 1501 → 向上取 2 的幂 2048），共压缩 **1914** 次，总耗时约 150 ms。如果不压缩，数组要 200 万+，且是活跃量的 2000 倍。

### 第 6 步：把"语义"包成一层命令接口

`parse` / `apply` / `render` / `replay`：文本命令 → sealed `Op` → sealed `Result` → 文本。目的是让样例能用脚本写，方便测试，并练习 sealed + 模式匹配。业务错误统一转成 `Err(message)`。

---

## 5. 逐段讲参考解

### 5.1 状态

```java
private int capacity;          // 2 的幂
private int[] cnt;             // Fenwick：活跃订单数
private long[] sum;            // Fenwick：剩余数量
private long[] idByIdx;        // 下标 → id
private long[] qtyByIdx;       // 下标 → 剩余数量（0 = 洞）
private int nextIndex = 1;     // 下一个可用下标
private final HashMap<Long, Integer> indexOf = new HashMap<>();
private long totalQty;
```

所有数组大小都是 `capacity + 1`（Fenwick 用 1 起的下标，第 0 格不用——因为 `0 & -0 == 0`，从 0 开始会死循环）。`qtyByIdx[i] > 0` 当且仅当下标 i 上是一张活跃订单，所以不需要单独的"活着"标志。

### 5.2 `put`

```java
if (qty <= 0) throw new IllegalArgumentException(INVALID_QTY);
if (indexOf.containsKey(id)) throw new IllegalArgumentException(DUPLICATE_ID);
long newTotal = Math.addExact(totalQty, qty);        // 溢出 → ArithmeticException，此时还没改任何东西
if (nextIndex > capacity) compact();                  // 下标空间写满：先压缩
int i = nextIndex++;
...
addCnt(i, 1); addSum(i, qty); indexOf.put(id, i);
totalQty = newTotal;
```

**顺序有讲究**：所有可能抛异常的检查都在任何修改之前——失败时对象保持原样。总量 `totalQty` 溢出检查很关键：Fenwick 里的每个节点是 `a` 的某段之和，只要**全局总和**不溢出，任何一段子和都不会溢出，所以只用检查 `totalQty` 一个数。
压缩发生在领下标之前，压缩完 `nextIndex` 被重置为 `m + 1`，保证有空位。

### 5.3 `delete`

读出 `have = qtyByIdx[i]`；`qty > have` 抛参数错；`left = have - qty`；`addSum(i, -qty)`；`left == 0` 时 `addCnt(i, -1)` 并 `indexOf.remove(id)`。
返回 `left`：调用方一眼看出订单是否被删光。注意订单位置（下标）从不改变。

### 5.4 `idAt`：二分下降

```java
int pos = 0, rem = k;
for (int pw = capacity; pw > 0; pw >>= 1) {
    int nxt = pos + pw;
    if (nxt <= capacity && cnt[nxt] < rem) { pos = nxt; rem -= cnt[nxt]; }
}
return idByIdx[pos + 1];
```

2.4 节手算过。`nxt <= capacity` 这个判断在 capacity 是 2 的幂时其实永远为真（`pos` 只由比 `pw` 更大的不同 2 的幂相加而成），保留它是为了即使以后容量不是 2 的幂也不会越界。前置检查 `1 ≤ k ≤ size` 保证答案存在。

### 5.5 `compact`

先保存旧数组引用，`allocate(newCap)` 换新数组，然后顺序扫旧数组把活跃订单搬到 1..m（顺序不变 → 插入顺序不变），同时更新 `indexOf` 里的下标（`put` 对已存在 key 只是替换 value，遍历期间不会出结构修改问题）；最后线性建树。`compactions++` 供测试观察。
**测试保证了"压缩不改变任何可观察行为"**：`differentialWithTinyCapacityAndPartialDeletes` 从容量 4 起步，6 万步随机操作，每步都和朴素模型比对。

### 5.6 文本接口

`parse` 用 `switch` 表达式 + `yield`；`apply` 对 sealed `Op` 做记录模式匹配，捕获四类异常转成 `Err`；`render` 对 sealed `Result` 做穷尽 switch，`case Ok _` 用了未命名模式。

---

## 6. Java 21 特性小课

### J01 `record`

旧：`Entry` 要手写类 + `equals/hashCode/toString`。新：`record Entry(long id, long qty) {}`。测试里 `assertEquals(List.of(new Entry(1,10), ...), s.entries())` 能直接比较，就是因为 record 的 `equals` 按字段比。

### J02 + J03 + J04 `sealed` + `switch` 模式匹配 + record 解构

```java
return switch (op) {
    case Put(var id, var q)  -> { put(id, q); yield new Ok(); }
    case Delete(var id, var q) -> new Num(delete(id, q));
    ...
};
```
旧写法是一串 `if (op instanceof Put) { Put p = (Put) op; ...}`；新增一种命令时，旧写法编译通过但运行时落入 else；新写法编译器因"switch 未穷尽"报错。

### J05 `switch` 表达式与 `yield`

`parse` 里每个 case 有多行（先 `args(t, 3)` 检查参数个数，再 `yield new Put(...)`）。旧写法需要 `break` 和一个临时变量。

### J09 Sequenced Collections

`s.entries().getFirst()`、`.getLast()`、`.reversed()`：旧写法 `list.get(list.size() - 1)`；对空列表，新的 `getFirst()` 抛 `NoSuchElementException`（比 `get(0)` 的 `IndexOutOfBounds` 语义更清楚）。

### J13 未命名模式 `_`（预览）

`case Ok _ -> "OK"`：`Ok` 没有字段可绑，写 `_` 表示"我不关心"。Java 21 需要 `--enable-preview`。

### J14 `Stream.toList()`、`IntStream`

`entries()`：`IntStream.range(1, nextIndex).filter(i -> qtyByIdx[i] > 0).mapToObj(i -> new Entry(...)).toList()`。旧写法是 for 循环 + 手建 `ArrayList`；`toList()` 返回**不可变**列表，调用方改不了内部状态的快照。**不该用**：热路径上（流有开销）；`entries()` 只用于调试和测试。

### J15 `Math.addExact`、`Math.clamp`（未用）

`addExact` 守住 `totalQty` 不溢出。

---

## 7. 追问预演

**Q1. 为什么用 Fenwick 而不是线段树？**
思考：两者都是 O(log n) 的"前缀和 + 单点修改"。需求只有求和（可逆的运算：能"减掉"）。
答案要点：Fenwick 只要一个数组、常数小、代码十几行；线段树功能更强（区间最值、区间修改），但本题用不上。Fenwick 的限制：运算必须有逆元（求和可以，求最大值不行）。
可以说的话：「我们只有单点修改 + 前缀求和，Fenwick 更简单更快；如果要区间最大值我会换线段树。」

**Q2. 能不能 O(1) 查询？**
可以用"前缀和数组"让查询 O(1)，但每次修改要 O(n) 更新后面所有前缀和；除非订单只增不删且从不修改（那么 `P(i)` 在 put 时一次性算好）。因为有 delete，必须在查询和更新间折中，Fenwick 把两个都压到 O(log n)。

**Q3. 删除之后下标越来越大，内存怎么办？**
Part 3：写满时压缩，按原顺序重新编号，新容量 ≥ 1.5m+1 的 2 的幂。摊还 O(1)；容量跟活跃量走（实测 1000 个活跃订单，处理 200 万个订单，容量稳定 2048）。
追问 "为什么是 1.5 而不是 1.0"：1.0 时压缩完马上写满，每次 put 都压缩，退化成 O(n)；留出 ≥ 1/3 的空位才有摊还 O(1)。

**Q4. 压缩期间会不会有一次 put 特别慢？**
会：一次 O(容量)。摊还分析只保证平均。如果是低延迟系统不能接受尾延迟，可以做**增量压缩**（后台逐步搬）或**双缓冲**（一半在用，一半悄悄重建，再切换）。这是诚实的取舍。

**Q5. 多线程怎么办？**
思考：查询是读，put/delete 是写。树状数组是普通数组，没有任何同步。
答案要点：(1) 最简单：一把 `ReentrantReadWriteLock`（读多写少时收益大；写频繁时读锁也被阻塞）；(2) 单线程所有者 + 命令队列（交易系统常见）；(3) 分片：按 id 哈希分成多段，但"前缀"跨分片，不能简单分片。
不要说"用 `ConcurrentHashMap`"：一个线程在更新两棵树、另一个线程在查询，会读到"树已经改了一半"的不一致状态——`ConcurrentHashMap` 只保证 map 本身的线程安全。

**Q6. `idAt(k)` 怎么做到 O(log n)？**
在 cnt 树上二分下降（2.4 节），每步确定答案二进制的一位。可以说出：「这就是 Fenwick 树上的 lower_bound。」

**Q7. 如果 id 很大、很稀疏怎么办？**
`HashMap<Long,Integer>` 不依赖 id 的取值范围；Fenwick 按**插入下标**而不是按 id 建，所以不需要离散化。如果题目让你按 id（或价格）的大小做前缀，就要先离散化或用动态开点线段树。

**Q8. 能否支持"在中间插入订单"？**
不能直接：下标要按位置排好。用平衡树（order-statistic tree，如带子树大小的红黑树 / treap）或 skip list；或离线先知道所有操作，预先分配好下标。

---

## 8. 常见误区

1. **下标从 0 开始。** Fenwick 的 `i & -i` 对 0 恒为 0，`for (; i > 0; i -= i & -i)` 和 `for (; i <= n; i += i & -i)` 在 i = 0 时一个不进循环、一个死循环。数组下标要 1 起（测试里的 `everySmallSizeEveryPrefix` 覆盖 1..70 张订单）。
2. **删除后把后面的订单往前挪。** 会改变所有后续订单的下标、破坏 `indexOf`。正确是留洞。
3. **`cnt` 和 `sum` 混用一棵树。** 部分删除时订单还活着（count 不变）而数量减少，需要两棵独立的树。
4. **部分删除也 `addCnt(i, -1)`。** 订单数就错了（测试 `partialDeleteKeepsPositionAndCount`）。
5. **压缩后忘了更新 `indexOf`。** 所有后续查询指向旧下标，悄悄返回错数。
6. **先改后检查溢出。** `totalQty` 溢出抛异常时，Fenwick 已经被改了一半。所有检查要放在最前面（测试 `totalQuantityOverflowIsRejected` 检查"抛异常后状态不变"）。
7. **压缩容量取"刚好 m+1"。** 压缩完马上写满，每次 put 都压缩。要留余量。
8. **`idAt` 在 `capacity` 不是 2 的幂时直接套二分下降。** 步长序列对不齐，会越界或取错。
9. **重复 id 当作更新。** 题面里 id 同时只能有一张活跃订单；重复 `put` 抛异常，删光后同一个 id 可以再 `put`，并且排到**最后**。
10. **查询已删除的 id 返回 0。** 应该抛 `NoSuchElementException`；"0"会让调用方无法区分"没有订单"和"前面没有订单"。

---

## 9. 自测题

**Q1（手算）** `a = [2, 7, 1, 8, 2, 8]`，写出 Fenwick 的 `tree[1..6]`，并用树算 `prefix(5)`。

<details><summary>答案</summary>lowbit：1,2,1,4,1,2。tree[1]=2；tree[2]=2+7=9；tree[3]=1；tree[4]=2+7+1+8=18；tree[5]=2；tree[6]=a5+a6=2+8=10。prefix(5)：5 → tree[5]=2；5-1=4 → tree[4]=18；4-4=0。和 = 20。核对 2+7+1+8+2 = 20 ✓。</details>

**Q2（手算）** 对上题的树执行 `add(2, +5)`，列出被更新的 tree 下标。

<details><summary>答案</summary>i=2 → tree[2]；2+2=4 → tree[4]；4+4=8 > 6 停。更新 tree[2]、tree[4]。tree[2]=14，tree[4]=23。</details>

**Q3（概念）** `i & -i` 对 i = 12（1100₂）得多少？为什么？

<details><summary>答案</summary>4。-12 = ~12 + 1：~1100 = ...0011，+1 = ...0100（低 4 位），与 1100 按位与 = 0100 = 4。只剩最低位的 1。</details>

**Q4（复杂度）** 压缩时新容量取 `max(minCap, 2m)` 和取 `max(minCap, 1.5m+1)` 各有什么得失？

<details><summary>答案</summary>`2m`：压缩更少（空位 ≥ m），摊还常数更小；但内存多占（容量最坏是活跃量的 4 倍：向上取 2 的幂又翻一倍）。`1.5m+1`：压缩更勤但容量更紧。两者都是摊还 O(1)，只是常数与内存的取舍。关键是"空位必须与 m 成正比"。</details>

**Q5（找 bug）** 下面的 `delete` 有什么问题？

```java
long delete(long id, long qty) {
    int i = indexOf.get(id);
    qtyByIdx[i] -= qty;
    addSum(i, -qty);
    if (qtyByIdx[i] == 0) { addCnt(i, -1); indexOf.remove(id); }
    return qtyByIdx[i];
}
```

<details><summary>答案</summary>(1) `indexOf.get(id)` 对未知 id 返回 null，拆箱时 NPE，应抛 `NoSuchElementException`；(2) 没检查 `qty ≤ 0`（负数会加量）；(3) 没检查 `qty > 剩余`（数量变成负数、洞与活跃订单混淆）；(4) 没有更新 `totalQty`。</details>

**Q6（小编程）** 用 Fenwick 写 `rangeSum(int l, int r)`，求 `a[l..r]` 的和。

<details><summary>答案</summary>`prefix(r) - prefix(l - 1)`。注意 l = 1 时 `prefix(0) = 0`，循环不执行，正好。</details>

---

## 10. 延伸阅读

* Peter M. Fenwick, "A New Data Structure for Cumulative Frequency Tables", *Software: Practice and Experience* 24(3), 1994——树状数组的原论文，短，值得一读它的动机（压缩算术编码里的累计频率表）。
* Cormen 等《算法导论》第 17 章「摊还分析」（聚合法 / 核算法 / 势能法）——Part 3 压缩的摊还证明所依据的方法。
* Java SE 21 API：`java.util.SequencedCollection`、`java.lang.Math.addExact`、`java.util.stream.Stream.toList`。
* JEP 431（Sequenced Collections）、JEP 441（Pattern Matching for switch）、JEP 440（Record Patterns）、JEP 443（Unnamed Patterns and Variables, Preview）。
* Joshua Bloch《Effective Java》第 3 版 Item 76「Strive for failure atomicity」——"失败时对象保持原样"的原则，对应 `put` 里"先检查再修改"。
