# hc15 · Streaming Median（两个堆、滑动窗口、百分位、直方图）—— 讲义

> 读者：会基本 Java（类、方法、循环、`List` / `HashMap`）。覆盖：中位数的两堆做法、滑动窗口的惰性删除、任意百分位的三种结构（两堆 / 顺序统计树 / 树状数组直方图）。

---

## 1. 问题是什么

### 1.1 中位数与百分位

中位数（median）：把数排好序，取中间那个。奇数个没有歧义；偶数个有两个候选（**下中位数**、**上中位数**），要先约定。

百分位（percentile）：p% 分位是「p% 的数不超过它」的那个值。**最近秩法**（nearest-rank）：n 个数，排好序，第 `⌈p·n/100⌉` 个。`{15, 20, 35, 40, 50}`：

| p | `⌈p·5/100⌉` | 值 |
|---|---|---|
| 5 | 1 | 15 |
| 30 | 2 | 20 |
| 40 | 2 | 20 |
| 50 | 3 | 35 |
| 100 | 5 | 50 |

延迟监控里的 p99、成交价的分布都用它。

### 1.2 约定

* 价格是 `long` tick，Part 1–3 允许任意 `long`（含负数、`Long.MIN_VALUE`）。
* 偶数个数时 `median()` 取**下中位数**（第 ⌈n/2⌉ 小）。理由：结果是真实出现过的价格、仍是整数 tick、而且恰好等于 p = 50 的最近秩。需要平均数时用 `doubledMedian()`：返回中位数的**两倍**（偶数个时是两个中间值之和），它是整数，不需要舍入规则。
* 空结构上取值抛 `NoSuchElementException`；参数非法抛 `IllegalArgumentException`，且参数检查先于「是否为空」。

### 1.3 四个 Part

1. 数据流中位数：两个堆。
2. 只看最近 k 笔：滑动窗口，惰性删除。
3. 任意百分位：p 固定用两个堆；p 在查询时才给，用顺序统计树。
4. 价格范围有界：树状数组直方图，构造后零分配；100 万次操作的性能测试。

---

## 2. 前置知识

### 2.1 堆与 `PriorityQueue`

堆（heap）能 O(1) 看到最小（或最大）元素，O(log n) 插入、弹出堆顶。Java 的 `PriorityQueue` 默认是**最小堆**；最大堆写 `new PriorityQueue<>(Collections.reverseOrder())`。**不支持**高效删除任意元素（`remove(Object)` 是 O(n)）。

### 2.2 为什么两个堆能找中位数

把排好序的数列从中间切成两半：左半（较小的）放进最大堆 `lo`，右半（较大的）放进最小堆 `hi`。

```
排序后:  1  3  5 | 8  9  20
         lo 的堆顶=5 | hi 的堆顶=8
```

`lo` 的堆顶是左半最大的、`hi` 的堆顶是右半最小的——它们恰好是中间的两个数。只要维持两条不变式：

* `lo` 里每个数 ≤ `hi` 里每个数；
* `|lo| = |hi|` 或 `|lo| = |hi| + 1`；

则 `lo` 的堆顶就是下中位数。加一个数：放对边，再最多挪一个元素恢复平衡，O(log n)。

### 2.3 平衡 BST、子树大小与「第 k 小」

`TreeMap` 能按 key 有序，但**不能按名次取**。给 BST 每个结点多存「子树元素总数」`total`，就能从根往下走一次找第 r 小：

设左子树有 L 个元素，本结点的值出现 c 次，要找第 r 小：

| 条件 | 动作 |
|---|---|
| `r ≤ L` | 往左子树找第 r 小 |
| `r ≤ L + c` | 就是本结点的值 |
| 否则 | `r −= L + c`，往右子树找 |

BST 要平衡，否则有序输入会退化成链表（高度 n）。**树堆**（treap）= BST（按值）+ 堆（按随机优先级）：新结点按值插入后，用旋转把高优先级的结点转上去，期望高度 O(log n)，实现比红黑树短得多。

### 2.4 树状数组（Fenwick tree）

数组 `tree[1..T]`，`tree[i]` 存区间 `(i − lowbit(i), i]` 里的计数，`lowbit(i) = i & −i`。

* 点加：`for (i = x + 1; i <= T; i += i & −i) tree[i]++`，O(log T)；
* 前缀和：`for (i = x + 1; i > 0; i −= i & −i) s += tree[i]`，O(log T)；
* 第 r 小（倍增下降）：从最高位的 2 的幂 `step` 开始，`if (pos + step <= T && tree[pos + step] < r) { pos += step; r −= tree[pos]; }`，最后答案是 `pos`。

### 2.5 惰性删除（lazy deletion）

堆里要删的元素不在堆顶时，不立刻删，而是在旁边记一笔「这个值待删 +1」；等它浮到堆顶时，发现待删表里有它，再弹出并把记录减 1。代价：堆里会暂时留着没用的元素；平衡两个堆的时候，要用**有效元素个数**，不能用 `heap.size()`。

---

## 3. Part 1：两个堆

最笨的做法：每次 `median()` 把全部数排序再取中间，O(n log n)；或者每加一个数就插入有序 `ArrayList`，O(n)。

```java
public void add(long price) {
    if (lo.isEmpty() || price <= lo.peek()) lo.add(price);      // 小的一边
    else hi.add(price);
    if (lo.size() > hi.size() + 1) hi.add(lo.poll());           // lo 太多：挪一个到 hi
    else if (hi.size() > lo.size()) lo.add(hi.poll());          // hi 太多：挪一个回 lo
}

public long median() {
    if (lo.isEmpty()) throw new NoSuchElementException("no prices yet");
    return lo.peek();                                           // 下中位数
}
```

检查：先加 5 → `lo=[5]`；加 15 → `15 > 5` 进 `hi`，`|lo| = |hi| = 1`，中位数 `lo.peek()=5`；加 1 → `1 ≤ 5` 进 `lo=[5,1]`，`|lo| = 2 = |hi| + 1` 成立；加 3 → `3 ≤ 5` 进 `lo=[5,3,1]`，3 > 2，挪 5 到 `hi`，`lo=[3,1]`，`hi=[5,15]`，中位数 3 ✓。

`doubledMedian()`：奇数个时 `lo.peek() + lo.peek()`，偶数个时 `lo.peek() + hi.peek()`；用 `Math.addExact`，`Long.MAX_VALUE` 附近溢出就抛。**为什么不直接 `(a + b) / 2`**：`a + b` 会溢出，而且 `/ 2` 要决定怎么舍入。

---

## 4. Part 2：滑动窗口中位数（惰性删除）

只看最近 k 个价格。新来一个，最老的一个要滑出窗口。需要从堆里删一个**任意**位置的值。

### 4.1 设计

* 环形缓冲 `long[] ring`（大小 k）记下窗口里的值，才知道谁要滑出。
* 两个堆 `lo` / `hi`，各一张 `delayed` 表（`HashMap<Long, Integer>`），各一个有效元素个数 `loValid` / `hiValid`。
* 旧值 `old` 属于哪个堆？`lo` 里每个数 ≤ `hi` 里每个数，所以 `old ≤ lo.peek()` ⇒ 在 `lo`，否则在 `hi`。相等时：`lo` 的堆顶本身就是一份有效的 `old`，所以记在 `lo` 是安全的。
* 每次 `add` 后：按有效个数平衡，然后 `prune` 两个堆顶（堆顶在 `delayed` 里就弹掉），保证 `median()` 读到的堆顶是有效的。

```java
public void add(long price) {
    long old = 0;
    boolean evict = count == k;
    if (evict) { old = ring[head]; ring[head] = price; head = (head + 1) % k; }
    else { ring[(head + count) % k] = price; count++; }

    if (loValid == 0 || price <= lo.peek()) { lo.add(price); loValid++; }
    else { hi.add(price); hiValid++; }

    if (evict) {
        if (old <= lo.peek()) { delayedLo.merge(old, 1, Integer::sum); loValid--; }
        else                  { delayedHi.merge(old, 1, Integer::sum); hiValid--; }
    }
    if (loValid > hiValid + 1)      { prune(lo, delayedLo); hi.add(lo.poll()); loValid--; hiValid++; }
    else if (loValid < hiValid)     { prune(hi, delayedHi); lo.add(hi.poll()); hiValid--; loValid++; }
    prune(lo, delayedLo);
    prune(hi, delayedHi);
    if (lo.size() + hi.size() - loValid - hiValid > 2L * k) rebuild();
}
```

注意顺序：先放新值，再记旧值待删，最后统一平衡一次。插入和删除各让 `loValid − hiValid` 变化 ±1，合起来最多偏离目标 2，挪一个元素就能恢复；旧值归属用 `old <= lo.peek()` 判断，此时 `lo.peek()` 必须是有效的（上一次操作结束时已 `prune`）。

为什么两张 `delayed` 表而不是一张：相等的值可能同时在两个堆里。一张共享的表会让 `hi` 的 `prune` 弹掉「本该记在 `lo`」的那份，两个堆的有效个数就和实际内容对不上。分开记账，个数永远对得上。

### 4.2 内存会不会涨

会。升序的流里，`lo` 的堆顶一直在变大，旧的小值沉在堆底，永远浮不上来——堆里的元素会长到 O(n)。修法：失效元素（`size − valid`）超过 2k 就**整体重建**：把环形缓冲里的 k 个值排序，前一半进 `lo`，后一半进 `hi`，清空 `delayed`。O(k log k)，至少隔 2k 次 `add` 才发生一次，摊还 O(log k)。堆里最多 `k + 2k = 3k` 个元素（`retained() ≤ 4k` 是测试的上界）。

### 4.3 其它做法

* `TreeMap<价格, 个数>`：加删 O(log k)，但取第 k/2 小要走迭代器 O(k)。
* 顺序统计树（Part 3）：加、删、取名次都是 O(log k)，但要实现「删除」。
* 排好序的 `ArrayList` + 二分插入 / 删除：每次 O(k)（`memmove`），k 小时反而最快。

### 4.4 小测

`slide({1, 3, -1, -3, 5, 3, 6, 7}, 3)` 应得 `{1, 1, 1, -1, -1, 3, 5, 6}`（逐窗口见 `problem.md`）。对拍：每步排序最近 k 个，取第 ⌈m/2⌉ 个。

---

## 5. Part 3：任意百分位

### 5.1 最近秩的算术

`rank = ⌈p·n/100⌉`。写成 `Math.ceilDiv(p * n, 100)` 要小心 `p * n` 溢出（`n` 大时）。题里要求 `n` 到 `Long.MAX_VALUE` 也对，拆开算：

```java
public static long rank(long n, int p) {
    if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
    if (p < 1 || p > 100) throw new IllegalArgumentException("p must be in 1..100: " + p);
    return n / 100 * p + ((n % 100) * p + 99) / 100;
}
```

`n = 100a + b`（`0 ≤ b < 100`）：`p·n/100 = a·p + p·b/100`，前一项是整数，后一项向上取整 `(p·b + 99) / 100`。`a·p ≤ n`，不会溢出。`rank(Long.MAX_VALUE, 50)` = `⌈MAX/2⌉` = `4611686018427387904`。

### 5.2 固定 p：两个堆

`lo` 装最小的 `rank(n, p)` 个数，`hi` 装其余。加一个数后 `n` 加 1，`rank` 最多加 1，所以最多挪一两个元素：

```java
n++;
if (lo.isEmpty() || price <= lo.peek()) lo.add(price); else hi.add(price);
long target = OrderStatistics.rank(n, p);
while (lo.size() > target) hi.add(lo.poll());
while (lo.size() < target) lo.add(hi.poll());
```

`value()` = `lo.peek()`。`p = 50` 时和 Part 1 完全一样（`rank = ⌈n/2⌉`）。局限：`p` 在构造时固定。要同时回答 p50、p95、p99 就要三个实例；`p` 在查询时才给，就不行了。

### 5.3 任意 p：顺序统计树（树堆）

结点放在数组里（下标 0 = 空），不为每个元素 `new`：

```java
private long[] key; private int[] cnt, left, right, total, prio;
```

* 相同的值合并成一个结点，`cnt` 记个数；
* `total[t] = cnt[t] + total[left[t]] + total[right[t]]`，每次结构变化后 `pull(t)` 重算；
* 插入：按值往下走，回溯时若孩子的优先级比自己大就旋转；

```java
private int insert(int t, long x) {
    if (t == 0) return newNode(x);
    if (x == key[t]) {
        cnt[t]++;
    } else if (x < key[t]) {
        int c = insert(left[t], x);          // 先算再存：insert 里可能扩容，换掉 left 数组
        left[t] = c;
        if (prio[left[t]] > prio[t]) {       // 右旋
            int l = left[t];
            left[t] = right[l]; right[l] = t;
            pull(t); pull(l);
            return l;
        }
    } else { /* 对称：左旋 */ }
    pull(t);
    return t;
}
```

**一个真实的坑**：`left[t] = insert(left[t], x);` 在 Java 里先求值左边的数组引用 `left`，再调用 `insert`；`insert` 里 `newNode` 扩容会把 `left` 字段换成新数组，随后的赋值写进了**旧数组**，结果悄悄丢掉一个孩子指针，`size()` 比实际少。所以先 `int c = insert(...)` 再存。

`kth(rank)`：

```java
int t = root; long r = rank;
while (true) {
    long l = total[left[t]];
    if (r <= l) t = left[t];
    else if (r <= l + cnt[t]) return key[t];
    else { r -= l + cnt[t]; t = right[t]; }
}
```

`percentile(p)` = `kth(rank(size, p))`；`countAtMost(v)`：从根往下，`v < key[t]` 往左，否则加上 `total[left] + cnt` 再往右。

有序输入下树堆不会退化（优先级是随机的）。这也是测试里「升序插入 20 万个再降序插入 20 万个」要验证的。

### 5.4 怎么选

| 结构 | 查询 | 适用 | 局限 |
|---|---|---|---|
| 两个堆 | O(1) | 一个固定的 p | p 固定；换 p 要重建 |
| 顺序统计树 | O(log n) | 任意 p、值域无界、要名次 / 排名 | 实现复杂，常数大 |
| 直方图（Part 4） | O(log T) | 值域有界 | 只能表示 `0..T−1`；内存 O(T) |
| 近似草图（t-digest / HdrHistogram） | O(1) 级 | 数据量太大、能容忍误差 | 不精确 |

---

## 6. Part 4：价格有界——`TickHistogram`

价格就是 0 到 100 万 tick。直接数：`counts[price]++`；第 r 小要从 0 往后累加，O(T)。换成树状数组，两个操作都是 O(log T)，且构造时一次分配：

```java
public void add(long price) {
    if (price < 0 || price >= maxTick) throw new IllegalArgumentException("price out of range: " + price);
    for (int i = (int) price + 1; i <= maxTick; i += i & -i) tree[i]++;
    total++;
}

public long kth(long rank) {
    if (rank < 1 || rank > total) throw new IllegalArgumentException("rank out of range");
    int pos = 0;
    long r = rank;
    for (int step = top; step > 0; step >>= 1) {      // top = Integer.highestOneBit(maxTick)
        int next = pos + step;
        if (next <= maxTick && tree[next] < r) { pos = next; r -= tree[next]; }
    }
    return pos;                                        // 下标 pos + 1 对应价格 pos
}
```

* `maxTick` 不是 2 的幂时，`next <= maxTick` 这个判断必不可少。
* `tree` 用 `long[]`：累计个数可能超过 `int`。
* 构造之后 `add` / `percentile` 没有任何分配——测试用 `ThreadMXBean.getThreadAllocatedBytes` 验证 80 万次操作分配 < 256 KB。
* 内存：`T = 2^20` 时 8 MB；上限 `MAX_TICKS = 2^22`（32 MB）。

### 100 万次操作的数量级（Java，预热后）

| 结构 | 实测 |
|---|---|
| `StreamingMedian`（add + median） | 约 55 ms |
| `WindowMedian`（k = 10^4） | 约 100 ms |
| `TwoHeapPercentile`（p = 95） | 约 25 ms |
| `OrderStatistics`（add + percentile） | 约 400 ms |
| `TickHistogram`（add + percentile） | 约 70 ms |

---

## 7. Java 21 特性小课

* **`Math.addExact`**：`doubledMedian` 里两个中间值之和溢出就抛 `ArithmeticException`，而不是回绕成错误的负数。
* **`Math.ceilDiv`（Java 18）**：向上取整除法一步到位；测试里用它写独立的百分位基准。注意它也会在 `p * n` 溢出时给错，所以实现里用拆开的算法。
* **`Random.nextLong(bound)`（Java 17，`RandomGenerator`）**：有界随机数，不用手写取模。
* **`Collections.reverseOrder()` / `HashMap.merge`**：最大堆一行；`delayed.merge(v, 1, Integer::sum)` 一行完成「计数加一」。
* **`Integer.highestOneBit`**：树状数组倍增下降的起点。
* **`var`**：右边类型显然时省掉重复的泛型。

---

## 8. 追问预演

**Q1. 偶数个数时中位数怎么定？**
给出选择和理由：下中位数 ⇒ 仍是整数 tick、是真实价格、与 p = 50 的最近秩一致。要平均数就返回两倍（整数），或定点数加明确的舍入规则；`(a + b) / 2` 会溢出，写成 `a + (b − a) / 2`（`a ≤ b`）。

**Q2. 为什么不直接用 `TreeMap` / 有序列表？**
取第 k/2 小不是 O(1)：`TreeMap` 要遍历；有序 `ArrayList` 插入 O(n)。两个堆让取中位数 O(1)。

**Q3. 滑动窗口里怎么删？**
惰性删除：记账，浮到堆顶再弹；平衡按有效个数；每次操作后保证堆顶有效。内存问题用「失效元素超过 2k 就重建」解决。

**Q4. 两个堆能算 p95 吗？**
能：`lo` 装 `⌈0.95·n⌉` 个。但 p 固定；要多个 p 或 p 在查询时才给，就用顺序统计结构。

**Q5. 值域有界时最快的是什么？**
直方图 + 树状数组：预分配、零分配、缓存友好。T 很大（比如 10^9）时退回树，或用近似草图（t-digest / GK / HdrHistogram）。

**Q6. 需要近似分位数怎么办？**
t-digest、GK、HdrHistogram：空间 O(1/ε)，误差有界；监控场景常用。

**Q7. 多线程怎么办？**
每个线程一份局部结构，定期合并。直方图直接逐桶相加，最容易合并；堆不好合并；或单写者 + 发布快照。

**Q8. 数据是乱序 / 有重复价格呢？**
都支持：堆允许重复；树堆把重复值合并成一个带计数的结点；直方图天然计数。

---

## 9. 常见误区

1. **偶数个取了上中位数或平均数，`(a + b) / 2` 溢出。**
2. **平衡条件写反。** `lo` 应当不少于 `hi`，且至多多一个；新数放错边（`<` 与 `<=` 在重复值上的差别）。
3. **窗口没满就开始删。**
4. **惰性删除用 `heap.size()` 做平衡。** 应当用有效个数。
5. **堆顶是失效元素时读中位数。** 每次操作后要 `prune` 两个堆顶。
6. **一张 `delayed` 表给两个堆共用。** 相等的值会记错堆。
7. **升序流里堆无限增长。** 要在失效元素多时重建。
8. **百分位向下取整。** 应当 `⌈p·n/100⌉`；`p·n` 溢出；`p = 0` / 101 没拒绝；空时先检查 p 还是先检查空。
9. **未平衡的 BST。** 有序输入退化成链表（栈溢出或超时）。
10. **数组扩容后写进旧数组。** `left[t] = insert(left[t], x)` 先求值数组引用。
11. **树状数组下标从 0 开始。** `i & −i` 在 0 上死循环；`maxTick` 不是 2 的幂时倍增下降越界。

---

## 10. 自测题

**Q1（手算）** 依次加入 `7, 7, 1, 9`，每次之后的下中位数？

<details><summary>答案</summary>`7`；`{7,7}` → 7；`{1,7,7}` → 7；`{1,7,7,9}` → 第 2 小 = 7。即 `7, 7, 7, 7`。</details>

**Q2（手算）** `{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}` 的 p90、p50、p10 各是多少？

<details><summary>答案</summary>排序 `1 1 2 3 3 4 5 5 6 9`，n = 10。p90：`⌈9⌉ = 9` → 第 9 个 = 6；p50：`⌈5⌉ = 5` → 3；p10：`⌈1⌉ = 1` → 1。</details>

**Q3（手算）** 窗口 k = 2，流 `5, 9, 1, 4`，每步的窗口中位数？

<details><summary>答案</summary>`[5]` → 5；`[5,9]` → 5；`[9,1]` → 1；`[1,4]` → 1。即 `5, 5, 1, 1`。</details>

**Q4（复杂度）** 为什么惰性删除后每个元素仍然只进出堆一次、摊还 O(log k)？

<details><summary>答案</summary>每个价格进一次堆、最多出一次堆（浮到堆顶被弹，或重建时被丢弃）；重建 O(k log k)，至少隔 2k 次 add 才发生，摊到每次 add 是 O(log k)。</details>

**Q5（找 bug）** 下面的 `rank` 有什么问题？

```java
static long rank(long n, int p) { return (p * n + 99) / 100; }
```

<details><summary>答案</summary>`p * n` 在 `n` 接近 `Long.MAX_VALUE` 时溢出；改用 `n / 100 * p + ((n % 100) * p + 99) / 100`。还漏了 `p`、`n` 的参数检查。</details>

**Q6（设计）** 价格范围是 0 到 10^9，每秒 100 万次更新，要随时查 p99。你会选什么？

<details><summary>答案</summary>10^9 的直方图太大（8 GB）。选项：顺序统计树（精确，O(log n)）；对数分桶直方图 / HdrHistogram / t-digest（近似，空间小，误差有界）。说明精度要求后再选。</details>

---

## 延伸阅读

* Java 文档：`PriorityQueue`、`Math.ceilDiv`、`RandomGenerator`。
* 树堆（treap）与树状数组（Fenwick tree）的算法教程。
