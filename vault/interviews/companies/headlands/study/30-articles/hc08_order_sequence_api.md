# hc08 · Order Sequence API（Put / Delete + 亚线性前缀查询）—— 讲义

> 读者：只会基本 Java（类、方法、循环、`ArrayList` / `HashMap`）。

---

## 1. 这道题在问什么

### 1.1 用大白话

一排**排队的订单**，每张有编号（`id`）和数量（`quantity`），新订单排**队尾**。操作：

* `put(id, qty)`：新订单排队尾；
* `delete(id, qty)`：删掉某张订单（或减少数量）；
* `countUpTo(id)`：从队头数到这张订单（含），一共几张；
* `qtyUpTo(id)`：从队头到这张订单（含），数量之和；
* `idAt(k)`：队伍里第 k 张订单的编号（补的第 4 个接口）。

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

### 1.3 难点

100 万张订单时，每次 `qtyUpTo` 从队头一张张加要几十万次，问 100 万次就是 10^11~10^12 次加法。题目要「**亚线性**（sublinear）查询」：时间增长比订单数 n 慢，如 O(log n)，这需要**树状数组（Fenwick tree）**。再追问：删除之后怎么办？内存会不会越用越多？——Part 3。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 前缀和（prefix sum）

`P(i) = a[1] + … + a[i]`。`qtyUpTo` 就是前缀和，`countUpTo` 是"每张订单值为 1"的前缀和。两个极端：

| 做法 | 查询 `P(i)` | 修改 `a[j]` |
|---|---|---|
| 每次现算（从头加到 i） | O(n) | O(1) |
| 提前存所有 P | O(1) | O(n)（后面所有 P 都要加变化量） |

订单不断进出、查询也多时都不行；树状数组**折中**：两者都 O(log n)。

### 2.2 二进制与「最低位的 1」（lowbit）——树状数组的钥匙

二进制里最右边的 `1` 对应的数值叫 **lowbit**：`6 = 110₂` → 2；`12 = 1100₂` → 4；`7 = 111₂` → 1；`8 = 1000₂` → 8。树状数组"每格负责多长一段"，长度恰是 lowbit(下标)。

**`i & -i`**：整数用**补码**，`-i` = 按位取反再加 1。4 位 `i = 6`：

```
 i      =  0110
~i      =  1001      （每一位取反）
-i      = ~i + 1 = 1010      （加 1：最右边连续的 1 变 0 并向左进位，进到原来 i 的最低位 1 的位置停下）
 i & -i =  0110
          1010
        = 0010  = 2        ← 只有"最低位的 1"这一位两边都是 1
```

为什么只剩最低位的 1：`~i` 里最低位 1 右边的 0 变 1、最低位的 1 变 0；加 1 后右边那串 1 进位变回 0，进位在最低位的 1 处变回 1。所以 `-i` 与 `i` 在"最低位 1 及右边"相同、左边相反，相与只剩那一位。

### 2.3 树状数组（Fenwick tree / Binary Indexed Tree）——从零推导

**目标**：`add(i, delta)`（`a[i] += delta`）和 `prefix(i)` 都 O(log n)。**想法**：不存每个 `a[i]` 或 `P(i)`，而存**若干段区间的和**，让每个前缀拆成**很少几段**。**规则**：`tree[i]` 存 `a` 在区间 **(i - lowbit(i), i]** 上的和，即以 i 结尾、长度为 lowbit(i) 的一段。

n = 8，`a = [3, 1, 4, 1, 5, 9, 2, 6]`：

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

"每个格子管多长"的图（横条表示 tree[i] 管的范围）：

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

`prefix(7)`：`tree[7]` 管 (6,7]，剩 `prefix(6)`；`tree[6]` 管 (4,6]，剩 a1..a4；`tree[4]` 管 (0,4]，4 − 4 = 0 结束。`prefix(7) = 2 + 14 + 9 = 25` ✓。

规律：**每步 `i -= i & -i` 抹掉 i 二进制里最低位的 1**（7 = 111₂ → 110₂ → 100₂ → 000₂）。步数 = i 的二进制 1 的个数 ≤ log₂(n)，这就是 O(log n)。

```java
long prefix(int i) {
    long r = 0;
    for (; i > 0; i -= i & -i) r += tree[i];    // 抹掉最低位的 1，直到 i = 0
    return r;
}
```

#### 修改 `add(i, delta)`：把变化加到所有"管着 i 的格子"

`a[3]` 加 10 后，区间含下标 3 的是 `tree[3]`、`tree[4]`、`tree[8]`。从 3 出发，"下一个管着我的格子"是 `3 + lowbit(3) = 4`，`4 + 4 = 8`，`8 + 8 = 16 > n` 结束。

```
add(3, +10):   i = 3 → 更新 tree[3]
               i = 3 + 1 = 4 → 更新 tree[4]
               i = 4 + 4 = 8 → 更新 tree[8]
               i = 8 + 8 = 16 > 8 → 停
```

为什么 `i += lowbit(i)` 跳到"下一个覆盖 i 的格子"：加 lowbit 让最低位的 1 进位成更高位，j 的 lowbit 更大（区间更长），且 (j - lowbit(j), j] 包含 i 所在区间。每步 lowbit 至少翻倍，最多 log₂(n) 步。

```java
void add(int i, long delta) {
    for (; i <= n; i += i & -i) tree[i] += delta;    // 跳到下一个管着 i 的格子
}
```

### 2.4 用树状数组"数个数"和"找第 k 个"

两棵树：`sum[]` 按"插入下标"累加**数量** → `qtyUpTo`；`cnt[]` 每张活跃订单在自己下标记 1 → `countUpTo`，**也用来找第 k 张**。

**`idAt`：树上二分下降**。`cnt` 树里 `tree[pos + 2^j]` 恰是 `(pos, pos + 2^j]` 里的活跃订单数（pos 是 2^(j+1) 的倍数时），从大步长到小步长试探。例：8 个下标，下标 3 已删（洞）；`cnt = [1,1,0,1,1,1,1,1]`，树 `t1=1, t2=2, t3=0, t4=3, t5=1, t6=2, t7=1, t8=7`。找第 4 张：

```
pos = 0, rem = 4
步长 8: 看 t[8]=7，7 < 4? 不是 → 第 4 张在这一整块之内，不跳
步长 4: 看 t[0+4]=t4=3，3 < 4? 是 → 前 4 个下标里只有 3 张，第 4 张在后面：pos = 4, rem = 4-3 = 1
步长 2: 看 t[4+2]=t6=2，2 < 1? 不是 → 不跳
步长 1: 看 t[4+1]=t5=1，1 < 1? 不是 → 不跳
结果: 下标 pos+1 = 5
```

核对：活跃下标 1,2,4,5,… 第 4 个是 5 ✓。每步确定答案二进制一位，O(log n)。**数组大小须是 2 的幂**，步长才能从最高位对齐——容量总是 2 的幂的原因之一。

### 2.5 哈希表：id → 下标

id 可以是任意 `long`，先用 `HashMap<Long, Integer>` 换算成"插入下标"，平均 O(1)。（装箱把 `long` 包成 `Long` 对象，多占约 24 字节、多一次指针跳转，热路径要避免；这里是可接受的简化。）

### 2.6 摊还分析（amortized analysis）

偶尔很贵、多数很便宜的操作，把贵的代价**平摊**到之前的便宜操作上。例：`ArrayList.add` 满时复制到两倍大的新数组（O(n)），但要先经过 n 次便宜 add，n 次总代价 ≈ 2n，平均 O(1)。Part 3 的压缩是一次 O(容量) 重建，要证明平均每次 put 仍 O(1)——靠"压缩后留足空位，下一次压缩前至少做这么多次 put"。

### 2.7 数组的"留洞"与"压缩"

删一个元素：后面全往前挪（O(n)，下标全变），或**原地留个洞**（O(1)，其他下标不变）。Fenwick 树按**下标**组织，往前挪要重建树；留洞只需把该下标的值改成 0。**代价**：洞永远占位，数组越来越长。**压缩**就是定期去掉所有洞、按原顺序给活的元素重新编号。

### 2.8 Java 21 的新东西

`record`、`sealed`、`switch` 模式匹配（第 6 节）；`SequencedCollection`（`getFirst()` / `getLast()` / `reversed()`）；`Math.addExact`。

---

## 3. 从最笨的解法开始

`ArrayList<long[]>` 按到达顺序存 `{id, qty}`：

```java
void put(long id, long qty)   { if (find(id) >= 0) throw ...; list.add(new long[]{id, qty}); }          // find 是 O(n)
long delete(long id, long q)  { int i = find(id); ... list.remove(i);  /* 或减量 */ }                   // O(n)：扫描 + 往前挪
long countUpTo(long id)       { return find(id) + 1; }                                                    // O(n)
long qtyUpTo(long id)         { long s = 0; for (long[] e : list) { s += e[1]; if (e[0] == id) break; } return s; }   // O(n)
long idAt(int k)              { return list.get(k - 1)[0]; }                                              // O(1)
```

**正确又短**，先写它（还可当"对拍"参照）。**慢**：每个操作 O(n)。5 万张订单、5 万次随机 `qtyUpTo` 约 **1.9 秒**；规模 ×10 时间约 ×100 ≈ **190 秒**；同样的 50 万 + 50 万树状数组约 **60 毫秒**。

---

## 4. 一步一步改进

### 第 1 步：纯 `HashMap` 够做 delete / 查找吗？

朴素版 `find(id)` O(n)，改用 `HashMap<Long, Integer> indexOf`（id → 下标）O(1)。**问题**：删除后后面下标都变，维护 map 值也是 O(n)。→ **让下标不变**：删除只"留洞"。

### 第 2 步：下标只增不减，删除留洞

put 时领递增下标 `nextIndex++`，永不变；删除只把 `qtyByIdx[i] = 0`，`indexOf` 的值永远有效。`qtyUpTo(id)` 变成"对下标 1..indexOf(id) 求和"，仍 O(n)，但已是标准的"**数组前缀和 + 单点修改**"。

### 第 3 步：套上树状数组

`sum[]` 树按下标累加数量，`cnt[]` 树累加"是否活着"（活 = 1）：
* `put`：新下标 `i` 上 `addCnt(i, +1)`、`addSum(i, qty)`；
* `delete`（整单）：`addCnt(i, -1)`、`addSum(i, -qty)`；
* `countUpTo(id) = prefixCnt(indexOf(id))`，`qtyUpTo(id) = prefixSum(indexOf(id))`；
* `idAt(k)`：在 `cnt` 树上二分下降（2.4），得下标，再读 `idByIdx[下标]`。

洞在两棵树里都是 0，不影响前缀和；订单先后 = 下标先后，所以"队头到 X"= 下标 1..idx(X)。全部 O(log n)。

### 第 4 步：部分删除

`qty` 小于剩余量时订单**不移除**、位置不变：`addSum(i, -qty)`、`qtyByIdx[i] -= qty`；`cnt` 树**不动**（还活着）。剩余量变 0 才 `addCnt(i, -1)` 并从 `indexOf` 删除。检查：`qty ≤ 0` 或 `qty >` 剩余 → 参数错（状态不变）；未知 id → `NoSuchElementException`。

### 第 5 步：下标空间写满了

Fenwick 数组大小固定为 `capacity`，删除不释放下标。哪怕只有 1000 张活跃订单，处理 200 万张也要 200 万大小——**内存跟"历史总量"走而非"当前活跃量"**（题目标签的 "memory management"）。

* **A（倍增，不够好）**：写满就扩两倍——活跃订单少时白白浪费，只增不减。
* **B（压缩 compaction）**：写满时把活跃订单**按原顺序**重编号 1..m，丢掉洞，重建树。新容量取"够用的最小 2 的幂"，活跃订单少时容量会**缩小**。

**容量取多少**：太紧（刚好 m+1）会压缩完马上写满，每次 put 都压缩，退化成每次 O(n)。要**留足空位**，取

```
newCap = 2 的幂 ≥ max(初始容量, m + m/2 + 1)
```

**摊还**：压缩一次 O(旧容量 + 新容量)；压缩后空位 = newCap − m ≥ newCap/3（newCap ≥ 1.5m + 1），下一次压缩前至少完成 newCap/3 次 put，每次分摊 ≤ O(newCap) / (newCap/3) = **O(1)**。

**线性建树**：逐个 `add` 是 O(m log n)；O(n) 做法：先把原始值填进 `tree[i]`，再从小到大遍历 i，把 `tree[i]` 加到"父节点" `tree[i + lowbit(i)]`：

```java
for (int i = 1; i <= newCap; i++) {
    int p = i + (i & -i);
    if (p <= newCap) { cnt[p] += cnt[i]; sum[p] += sum[i]; }
}
```

`tree[p]` 管的区间 = 自己一格 + 若干"孩子"区间，孩子正是 `j + lowbit(j) = p` 的 j；从小到大处理，保证 `tree[i]` 加到父节点时已收齐自己的孩子。

**数据**：活跃订单 ≤ 1000，200 万次 put + 删除最老的循环：容量稳定 **2048**（1501 向上取 2 的幂），共压缩 **1914** 次，约 150 ms；不压缩则数组要 200 万+，是活跃量的 2000 倍。

### 第 6 步：把"语义"包成命令接口

`parse` / `apply` / `render` / `replay`：文本命令 → sealed `Op` → sealed `Result` → 文本，让样例能用脚本写、方便验证。业务错误统一转成 `Err(message)`。

---

## 5. 逐段讲解法

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

数组大小都是 `capacity + 1`（下标 1 起，第 0 格不用——`0 & -0 == 0` 会死循环）。`qtyByIdx[i] > 0` 当且仅当下标 i 是活跃订单，无需单独的"活着"标志。

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

**顺序有讲究**：所有可能抛异常的检查都在任何修改之前——失败时对象保持原样。只要**全局总和** `totalQty` 不溢出，任何子和都不会溢出，所以只检查它一个数。压缩在领下标之前，完成后 `nextIndex` 重置为 `m + 1`，保证有空位。

### 5.3 `delete`

读 `have = qtyByIdx[i]`；`qty > have` 抛参数错；`left = have - qty`；`addSum(i, -qty)`；`left == 0` 时 `addCnt(i, -1)` 并 `indexOf.remove(id)`。返回 `left`，下标从不改变。

### 5.4 `idAt`：二分下降

```java
int pos = 0, rem = k;
for (int pw = capacity; pw > 0; pw >>= 1) {
    int nxt = pos + pw;
    if (nxt <= capacity && cnt[nxt] < rem) { pos = nxt; rem -= cnt[nxt]; }
}
return idByIdx[pos + 1];
```

手算见 2.4。`nxt <= capacity` 在容量是 2 的幂时其实永远为真，保留是为以后容量不是 2 的幂也不越界；前置检查 `1 ≤ k ≤ size` 保证答案存在。

### 5.5 `compact`

保存旧数组引用，`allocate(newCap)` 换新数组，顺序扫旧数组把活跃订单搬到 1..m（插入顺序不变），同时更新 `indexOf` 里的下标（对已存在 key 只替换 value，遍历期间无结构修改问题），最后线性建树。**压缩不能改变任何可观察行为**：从容量 4 起步做 6 万步随机操作，每步与朴素模型比对。

### 5.6 文本接口

`parse` 用 `switch` 表达式 + `yield`；`apply` 对 sealed `Op` 做记录模式匹配，捕获四类异常转成 `Err`；`render` 对 sealed `Result` 做穷尽 switch，`case Ok _` 用了未命名模式。

---

## 6. Java 21 特性小课

### `record`

旧：手写类 + `equals/hashCode/toString`；新：`record Entry(long id, long qty) {}`，`s.entries()` 能直接和 `List.of(new Entry(1,10), ...)` 比较（`equals` 按字段）。

### `sealed` + `switch` 模式匹配 + record 解构

```java
return switch (op) {
    case Put(var id, var q)  -> { put(id, q); yield new Ok(); }
    case Delete(var id, var q) -> new Num(delete(id, q));
    ...
};
```
旧写法是一串 `if (op instanceof Put) { Put p = (Put) op; ...}`；新增一种命令时旧写法编译通过但运行时落入 else，新写法因"switch 未穷尽"编译报错。

### `switch` 表达式与 `yield`

`parse` 里每个 case 多行（先 `args(t, 3)` 检查参数个数，再 `yield new Put(...)`）；旧写法需 `break` 和临时变量。

### Sequenced Collections、未命名模式 `_`（预览）、Stream

`getFirst()` / `getLast()` / `reversed()` 取代 `list.get(list.size() - 1)`；空列表抛 `NoSuchElementException`，比 `IndexOutOfBounds` 清楚。`case Ok _ -> "OK"`：`Ok` 无字段可绑，`_` 表示"不关心"，需 `--enable-preview`。`entries()` 用 `IntStream.range(1, nextIndex).filter(i -> qtyByIdx[i] > 0).mapToObj(i -> new Entry(...)).toList()`（旧写法 for 循环 + 手建 `ArrayList`）；`toList()` 返回**不可变**列表。**不该用**：热路径（流有开销）；`entries()` 只用于调试和测试。

---

## 7. 追问预演

**Q1. 为什么用 Fenwick 而不是线段树？**
需求只有求和（可逆）。Fenwick 一个数组、常数小、十几行；线段树更强（区间最值、区间修改）但用不上。Fenwick 的限制：运算须有逆元（求和可以，最大值不行）。
说：「只有单点修改 + 前缀求和，Fenwick 更简单更快；要区间最大值我会换线段树。」

**Q2. 能不能 O(1) 查询？**
前缀和数组查询 O(1) 但修改 O(n)；除非订单只增不删（put 时一次算好 `P(i)`）。有 delete 就必须折中。

**Q3. 删除后下标越来越大，内存怎么办？**
写满时压缩、按原顺序重编号，新容量 ≥ 1.5m+1 的 2 的幂，摊还 O(1)，容量跟活跃量走。"为什么 1.5 不是 1.0"：1.0 时压缩完马上写满，退化成 O(n)；留出 ≥ 1/3 空位才摊还 O(1)。

**Q4. 压缩期间会不会有一次 put 特别慢？**
会：一次 O(容量)，摊还只保证平均。低延迟系统可做**增量压缩**（后台逐步搬）或**双缓冲**（一半在用、一半悄悄重建再切换）。

**Q5. 多线程怎么办？**
树状数组是普通数组，无同步。(1) `ReentrantReadWriteLock`（读多写少收益大）；(2) 单线程所有者 + 命令队列（交易系统常见）；(3) 分片不行：按 id 哈希分段但"前缀"跨分片。别说"用 `ConcurrentHashMap`"：一个线程更新两棵树、另一个查询会读到"改了一半"的状态，它只保证 map 本身线程安全。

**Q6. `idAt(k)` 怎么 O(log n)？**
在 cnt 树上二分下降（2.4），每步确定答案二进制一位。可说：「这就是 Fenwick 树上的 lower_bound。」

**Q7. id 很大、很稀疏怎么办？**
`HashMap<Long,Integer>` 不依赖 id 取值范围；Fenwick 按**插入下标**建，不需离散化。若要按 id（或价格）大小做前缀，就要先离散化或用动态开点线段树。

**Q8. 能否支持"在中间插入订单"？**
不能直接：下标要按位置排好。用平衡树（order-statistic tree，如带子树大小的红黑树 / treap）或 skip list；或离线先知道所有操作、预先分配下标。

---

## 8. 常见误区

1. **下标从 0 开始。** `i & -i` 对 0 恒为 0，`i += i & -i` 的循环在 i = 0 时死循环。下标要 1 起。
2. **删除后把后面的订单往前挪。** 改变所有后续下标、破坏 `indexOf`。正确是留洞。
3. **`cnt` 和 `sum` 混用一棵树。** 部分删除时订单还活着（count 不变）数量减少，需要两棵独立的树。
4. **部分删除也 `addCnt(i, -1)`。** 订单数就错了。
5. **压缩后忘了更新 `indexOf`。** 后续查询指向旧下标，悄悄返回错数。
6. **先改后检查溢出。** `totalQty` 溢出抛异常时 Fenwick 已被改一半。检查放最前面。
7. **压缩容量取"刚好 m+1"。** 压缩完马上写满，每次 put 都压缩。要留余量。
8. **`idAt` 在 `capacity` 不是 2 的幂时直接套二分下降。** 步长序列对不齐，越界或取错。
9. **重复 id 当作更新。** 同一 id 同时只能有一张活跃订单；重复 `put` 抛异常，删光后同一 id 可再 `put`，且排到**最后**。
10. **查询已删除的 id 返回 0。** 应抛 `NoSuchElementException`；"0"让调用方分不清"没有订单"和"前面没有订单"。

---

## 9. 自测题

**Q1（手算）** `a = [2, 7, 1, 8, 2, 8]`，写出 Fenwick 的 `tree[1..6]`，并用树算 `prefix(5)`。

<details><summary>答案</summary>lowbit：1,2,1,4,1,2。tree[1]=2；tree[2]=9；tree[3]=1；tree[4]=2+7+1+8=18；tree[5]=2；tree[6]=2+8=10。prefix(5)：5 → tree[5]=2；5-1=4 → tree[4]=18；4-4=0。和 = 20 ✓（2+7+1+8+2）。</details>

**Q2（手算）** 对上题的树执行 `add(2, +5)`，列出被更新的 tree 下标。

<details><summary>答案</summary>i=2 → tree[2]；2+2=4 → tree[4]；4+4=8 > 6 停。tree[2]=14，tree[4]=23。</details>

**Q3（概念）** `i & -i` 对 i = 12（1100₂）得多少？为什么？

<details><summary>答案</summary>4。-12 = ~12 + 1：~1100 = ...0011，+1 = ...0100，与 1100 相与 = 0100 = 4，只剩最低位的 1。</details>

**Q4（复杂度）** 压缩时新容量取 `max(minCap, 2m)` 和 `max(minCap, 1.5m+1)` 各有什么得失？

<details><summary>答案</summary>`2m`：压缩更少（空位 ≥ m），摊还常数更小；但内存多占（向上取 2 的幂又翻倍，容量最坏是活跃量的 4 倍）。`1.5m+1`：压缩更勤但容量更紧。都是摊还 O(1)，只是常数与内存的取舍。关键是"空位必须与 m 成正比"。</details>

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

<details><summary>答案</summary>(1) `indexOf.get(id)` 对未知 id 返回 null，拆箱 NPE，应抛 `NoSuchElementException`；(2) 没检查 `qty ≤ 0`（负数会加量）；(3) 没检查 `qty > 剩余`（数量变负、洞与活跃订单混淆）；(4) 没更新 `totalQty`。</details>

**Q6（小编程）** 用 Fenwick 写 `rangeSum(int l, int r)`，求 `a[l..r]` 之和。

<details><summary>答案</summary>`prefix(r) - prefix(l - 1)`。l = 1 时 `prefix(0) = 0`，循环不执行，正好。</details>

---

「延伸」CLRS《算法导论》「摊还分析」一章。
