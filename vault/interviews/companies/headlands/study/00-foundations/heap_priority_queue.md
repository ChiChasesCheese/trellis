# 基础课 · 堆（heap）与 `PriorityQueue`

> 配套代码：[`examples/HeapDemo.java`](examples/HeapDemo.java)（手写 int 小根堆，每次交换都打印；以及 `PriorityQueue` 各种坑的复现），本章输出来自它。
> 前置：O(log n) 和「数步数」（复杂度一章）。

---

## 0. 这一章在讲什么

**堆只擅长一件事：不停地问「现在最小（或最大）的是谁？」，并且插入新元素、取走最小元素都很快（O(log n)）。**

它不擅长的也要先知道：不能按顺序遍历、不能按值快速查找、不能快速删除中间元素。很多 `PriorityQueue` bug 来自把它当「自动排序的列表」。

顺序：问题 → 堆的定义与数组布局 → 上浮/下沉演示 → O(n) 建堆证明 → `PriorityQueue` 的 API → 坑 → 什么时候**不**该用堆。

---

## 1. 问题：反复取最小值，笨办法有多笨

### 1.1 一个具体的场景

合并三条已排序的行情流：每次从「三条流各自的队头」里取最小的输出，然后让那条流前进一格。

* 流 A：1, 4, 9　流 B：2, 3, 8　流 C：5, 6, 7
* 队头是 {1, 2, 5} → 输出 1，A 前进，队头变成 {4, 2, 5} → 输出 2……

K 条流（K = 1000）时，每次取最小要面对 1000 个候选。

### 1.2 两个笨办法

**笨办法 1：每次扫描所有候选。**每次 O(K)，输出 N 个共 O(N·K)；K = 1000、N = 10⁷ 时 10¹⁰，太慢。

**笨办法 2：候选放进始终排好序的数组。**取最小 O(1)，但每次插入要找位置并挪动后面所有元素，O(K)，总共仍 O(N·K)。

**堆的折中**：取最小 O(1)，插入和删除最小 O(log K)。N = 10⁷、K = 1000 时 log₂ K ≈ 10，总共 10⁸ 量级，可接受。

关键洞察：**不需要把所有候选完全排好序**，只要「最小的那个永远在手边」。放松「完全有序」就换来更便宜的维护。

---

## 2. 堆是什么：一个约束 + 一个形状

### 2.1 定义

**二叉堆**（binary heap）是同时满足两个条件的二叉树：

1. **形状性质（shape property）**：**完全二叉树**——除最后一层每层都满，最后一层的节点从左往右紧挨着，没有空位。
2. **堆序性质（heap property）**：每个节点 ≤ 它的两个孩子（**小根堆 / min-heap**）；或每个节点 ≥ 孩子（大根堆 / max-heap）。

堆序只约束「父 vs 子」，**兄弟、堂兄弟之间没有大小关系**。

一个小根堆的例子（由插入 5, 3, 8, 1, 2 得到，后面会逐步推导）：

```text
            1
          /   \
         2     8
        / \
       5   3
```

检查：1 ≤ 2, 1 ≤ 8；2 ≤ 5, 2 ≤ 3。✓ 5 和 3 谁在左边没要求，8 比 5 大也不违规（不是父子）。

### 2.2 为什么「完全二叉树」重要：可以直接存进数组

完全二叉树没有空洞，可按「一层一层、从左到右」编号塞进普通数组，**不需要指针**：

```text
下标:     0   1   2   3   4
数组:   [ 1,  2,  8,  5,  3 ]

树形（括号里是下标）:
               1(0)
             /      \
          2(1)      8(2)
         /    \
      5(3)    3(4)
```

编号规则（根在下标 0）：

```text
节点 i 的左孩子   = 2i + 1
节点 i 的右孩子   = 2i + 2
节点 i 的父亲     = (i − 1) / 2      （整数除法，向下取整）
```

**为什么是这个公式？**第 k 层（根是第 0 层）有 2ᵏ 个节点，第 0 到 k−1 层共 2ᵏ − 1 个，所以第 k 层第一个节点下标是 2ᵏ − 1。设节点 i 是第 k 层第 j 个（j 从 0 起），则 i = 2ᵏ − 1 + j；它的孩子是下一层的第 2j 和 2j+1 个，下标 2ᵏ⁺¹ − 1 + 2j 和 +1。代入 2ᵏ = i + 1 − j：

```text
左孩子 = 2(i + 1 − j) − 1 + 2j = 2i + 1
右孩子 = 2i + 2
```

验算：i = 1（值 2），左孩子下标 3（值 5），右孩子下标 4（值 3）。✓

**为什么用数组不用节点对象？**

* 没有 `left`/`right`/`parent` 指针，每个节点省 3 个引用；
* 数组是连续内存，缓存友好：访问 `a[i]` 后 `a[i+1]` 大概率已在缓存里；
* 「最后一个元素」就是 `a[size−1]`，增删末尾 O(1)——O(log n) 算法的关键。

### 2.3 高度：为什么是 O(log n)

n 个节点的完全二叉树高度（层数）是 ⌊log₂ n⌋ + 1；n = 1,000,000 只有 20 层，堆的所有「走一条路径」的操作最多 20 步。

---

## 3. 插入：上浮（sift-up）

### 3.1 想法

新元素先放**数组末尾**（保持完全二叉树），但可能比父亲小、破坏堆序。修复：**和父亲比，比父亲小就交换，一直换到不比父亲小或到根。**

### 3.2 为什么这样能修好

插入前整棵树合法。新元素 x 放到末尾后，唯一可能违规的是 (x, x 的父亲)。若 x < 父亲 p，交换后：

* x 在 p 原位置，x < p ≤ p 原来的所有后代，所以向下没有违规；
* p 到了 x 原位置，p 的新孩子是 x 原来的孩子（叶子，没有）和 p 原来的另一个孩子（p ≤ 它）；
* 唯一可能新的违规是 (x, x 的新父亲)，继续同样处理。

每步 x 上一层，最多 log n 层，O(log n)。

### 3.3 逐步演示：依次插入 5, 3, 8, 1, 2

每步都是 `HeapDemo` A1 的真实输出（`swap a[i]=… <-> a[j]=…` 是被交换的两个位置）。

```text
add 5
  数组 [5]

add 3          新元素放到下标 1，父亲是下标 0（值 5）；3 < 5，交换
  swap a[1]=3 <-> a[0]=5
  数组 [3, 5]
            3
           /
          5

add 8          放到下标 2，父亲下标 0（值 3）；8 ≥ 3，不交换
  数组 [3, 5, 8]
            3
          /   \
         5     8

add 1          放到下标 3，父亲 (3−1)/2 = 1（值 5）；1 < 5，交换
  swap a[3]=1 <-> a[1]=5
               现在 1 在下标 1，父亲是下标 0（值 3）；1 < 3，交换
  swap a[1]=1 <-> a[0]=3
  数组 [1, 3, 8, 5]
            1
          /   \
         3     8
        /
       5

add 2          放到下标 4，父亲 (4−1)/2 = 1（值 3）；2 < 3，交换
  swap a[4]=2 <-> a[1]=3
               现在 2 在下标 1，父亲下标 0（值 1）；2 ≥ 1，停
  数组 [1, 2, 8, 5, 3]
            1
          /   \
         2     8
        / \
       5   3
```

### 3.4 Java 写法（`HeapDemo.MinHeap.siftUp`）

```java
// 数组 a 是小根堆，把下标 i 的元素上浮到合适位置
static void siftUp(int[] a, int i) {
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (a[parent] <= a[i]) break;         // 父亲已经不大于我：堆序成立，停
        int t = a[parent]; a[parent] = a[i]; a[i] = t;
        i = parent;
    }
}
```

**平均比最坏好得多**：最坏插入 O(log n)（新元素是全局最小，一路换到根）；随机顺序插入时新元素大概率偏大，很快停下。`HeapDemo` A3（n = 10⁶ 个随机 int）：n 次插入总共只交换 1,280,829 次，平均 **1.28 次**——随机数据下插入平均 O(1)；**递减序列**每次都换到根，才是 log n。

---

## 4. 取出最小：下沉（sift-down）

### 4.1 想法

最小元素永远在根（下标 0）。取走它后根成空位；让某个孩子顶上来会层层留空位，很麻烦。更聪明的做法：

1. **把数组最后一个元素搬到根**，长度减 1（形状仍是完全二叉树）；
2. 此时根可能比孩子大。让它**和两个孩子里较小的比，比孩子大就交换**，一路向下，直到不大于两个孩子（或没有孩子）。

### 4.2 为什么要选「较小的孩子」

根 x 要下沉，左孩子 l、右孩子 r，且 l < r：

* 和 r 交换：r 上去，但 l < r，l 成了 r 的孩子，孩子比父亲小，违规；
* 和 l 交换：l 上去，r > l，(l, r) 合法 ✓。

所以**必须和较小的孩子换**。

### 4.3 逐步演示：从 `[1, 2, 8, 5, 3]` 开始，反复 poll

`HeapDemo` A2 的真实输出，括号里是说明。

```text
poll 第 1 次 —— 取走根 1
   把最后一个元素 3 搬到根:  [3, 2, 8, 5]
            3
          /   \
         2     8
        /
       5
   根 3 的孩子是 2 和 8，较小是 2；3 > 2，交换
  swap a[0]=3 <-> a[1]=2
   现在 3 在下标 1，孩子是下标 3（值 5）；3 ≤ 5，停
  → got 1, heap now [2, 3, 8, 5]
            2
          /   \
         3     8
        /
       5

poll 第 2 次 —— 取走 2
   最后一个元素 5 搬到根: [5, 3, 8]
   孩子 3 和 8，较小 3；5 > 3，交换
  swap a[0]=5 <-> a[1]=3
   5 到了下标 1，没有孩子（下标 3 ≥ size），停
  → got 2, heap now [3, 5, 8]

poll 第 3 次 —— 取走 3
   最后一个元素 8 搬到根: [8, 5]
   孩子只有 5；8 > 5，交换
  swap a[0]=8 <-> a[1]=5
  → got 3, heap now [5, 8]

poll 第 4 次 → got 5, heap now [8]
poll 第 5 次 → got 8, heap now []
```

取出顺序 1, 2, 3, 5, 8——从小到大。这就是**堆排序**的原理：建堆再 poll n 次得到有序序列，共 O(n log n)。

### 4.4 Java 写法（`HeapDemo.MinHeap.siftDown`）

```java
// 数组 a 的前 size 个元素是小根堆，把下标 i 的元素下沉到合适位置
static void siftDown(int[] a, int size, int i) {
    while (true) {
        int l = 2 * i + 1, r = l + 1, smallest = i;
        if (l < size && a[l] < a[smallest]) smallest = l;
        if (r < size && a[r] < a[smallest]) smallest = r;
        if (smallest == i) break;              // 两个孩子都不比我小：停
        int t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
```

复杂度：最多下沉到叶子，O(log n)。（搬到根的「最后一个元素」本来就大，通常沉到接近底部，平均接近 log n。）

---

## 5. 一次性建堆：为什么是 O(n) 而不是 O(n log n)

### 5.1 问题

n 个元素已在数组里，整理成堆。

**做法 A（朴素）**：逐个 `add`（上浮），每次 O(log n)，共 O(n log n)。

**做法 B（Floyd 建堆，1964）**：从**最后一个有孩子的节点**（下标 n/2 − 1）**倒着**到根，对每个节点做一次**下沉**。

```java
static void heapify(int[] a) {
    int n = a.length;
    for (int i = n / 2 - 1; i >= 0; i--) {   // 下标 >= n/2 的都是叶子，本来就是合法的堆
        siftDown(a, n, i);
    }
}

// 4.4 节的 siftDown，再贴一次，让这段代码可以单独编译
static void siftDown(int[] a, int size, int i) {
    while (true) {
        int l = 2 * i + 1, r = l + 1, smallest = i;
        if (l < size && a[l] < a[smallest]) smallest = l;
        if (r < size && a[r] < a[smallest]) smallest = r;
        if (smallest == i) break;
        int t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
```
做法 B 看起来也是「n/2 次下沉，每次 O(log n)」，但它真的是 **O(n)**。

### 5.2 手算例子：`PriorityQueue` 如何整理 `[9, 4, 7, 1, 8, 2, 6]`

`HeapDemo` B1 用 `new PriorityQueue<>(List.of(9, 4, 7, 1, 8, 2, 6))` 构造，输出 `[1, 4, 2, 9, 8, 7, 6]`。手推：

```text
初始数组（当作完全二叉树）       下标: 0 1 2 3 4 5 6
                                值:  [9,4,7,1,8,2,6]
            9
          /   \
         4     7
        / \   / \
       1   8 2   6

n = 7，从 i = n/2 − 1 = 2 开始往回到 0。

i = 2（值 7），孩子 2 和 6，较小 2；7 > 2，交换:
            9
          /   \
         4     2
        / \   / \
       1   8 7   6              数组 [9,4,2,1,8,7,6]

i = 1（值 4），孩子 1 和 8，较小 1；4 > 1，交换:
            9
          /   \
         1     2
        / \   / \
       4   8 7   6              数组 [9,1,2,4,8,7,6]

i = 0（值 9），孩子 1 和 2，较小 1；9 > 1，交换到下标 1:
            1
          /   \
         9     2
        / \   / \
       4   8 7   6
       再看 9（下标 1），孩子 4 和 8，较小 4；9 > 4，交换到下标 3:
            1
          /   \
         4     2
        / \   / \
       9   8 7   6              数组 [1,4,2,9,8,7,6]  ← 和程序输出一致
```

### 5.3 为什么是 O(n)：证明草图

关键：**下沉的代价与「该节点到叶子的高度」成正比，而大部分节点高度很小。**

节点**高度** h = 它到最远叶子的距离（叶子 h = 0）。高度为 h 的节点至多 ⌈n / 2^(h+1)⌉ 个：

```text
h = 0 (叶子)       约 n/2 个      下沉代价 0（本来就不用动）
h = 1              约 n/4 个      下沉最多 1 步
h = 2              约 n/8 个      下沉最多 2 步
...
h = log n (根)     1 个           下沉最多 log n 步
```

总代价 ≤ Σ_{h=0}^{log n} (n / 2^(h+1)) · h = (n/2) · Σ h / 2^h。

已知 Σ_{h=0}^{∞} h / 2^h = 2（验证：S = 1/2 + 2/4 + 3/8 + …；S/2 = 1/4 + 2/8 + …；S − S/2 = 1/2 + 1/4 + 1/8 + … = 1，所以 S = 2）。所以总代价 ≤ (n/2) · 2 = **n**，即 O(n)。

**直觉**：一半的节点是叶子不用动，四分之一只下沉 1 层……「重活」只由很少的节点承担。做法 A 正相反——新元素在树底部（节点最多处），上浮距离 log n 量级，所以 O(n log n)。

**对比**（`HeapDemo` A3，n = 10⁶ 个随机 int，数交换次数）：

**实测对比**（`HeapDemo` A3，n = 10⁶ 个随机 int，数交换次数）：

```text
heapify (sift-down from n/2-1): 744,070 swaps  (0.74 per element)
n x add (sift-up)             : 1,280,829 swaps  (1.28 per element)
```

随机数据上差距只有 1.7 倍（随机数据对上浮很友好）；但做法 A 最坏 O(n log n)（递减输入），做法 B 最坏始终 O(n)。

### 5.4 Java 里的体现

* `new PriorityQueue<>(Collection)` 对非有序集合走 `heapify`（O(n)）。
* 对已有 `PriorityQueue` 调 `addAll(c)` 或逐个 `add` 是逐个上浮，O(m log n)。**一开始就知道全部元素，用构造器传集合更快**（与 `ArrayList` 构造器传集合比逐个 `add` 快同理）。

---

## 6. 堆能做什么、不能做什么

| 操作 | 堆 | 为什么 |
|---|---|---|
| 查看最小（`peek`） | **O(1)** | 在根 |
| 插入（`offer`/`add`） | **O(log n)** | 上浮 |
| 取出最小（`poll`） | **O(log n)** | 下沉 |
| 建堆（n 个元素一次性） | **O(n)** | Floyd |
| 查找某个值（`contains`） | O(n) | 只有父子有序，要全扫 |
| 删除某个值（`remove(Object)`） | O(n) | 先找（O(n)）再摘掉（O(log n)） |
| 按顺序遍历 | 不支持 | 数组顺序不是排序顺序 |
| 找第二小 | O(1) | 根的两个孩子之一，但 API 不提供 |

### 6.1 堆排序（heapsort）与 top-k

* **堆排序**：建堆 O(n)，poll n 次 O(n log n)。原地、不稳定、不需额外数组。实际比快排慢（缓存局部性差——下沉时 `i` 到 `2i+1` 跳跃大），所以 Java 库不用它做主排序，只在快排退化时当后备。
* **top-k 最大的 k 个**：维护**大小为 k 的小根堆**，新元素比堆顶大就替换堆顶。总复杂度 O(n log k)，空间 O(k)。`HeapDemo` B5 从 `5 1 9 3 7 8 2` 选 3 个最大的得 `[7, 8, 9]`。

反直觉：**找最大的 k 个要用小根堆**——堆顶是「当前 k 个里最小的」，也就是「下一个被淘汰的候选」，新来者只要比它大就能挤掉它。

### 6.2 K 路归并（hc02 的核心）

K 条已排序的流，堆里放 K 个元素（每条流当前的队头）。反复：`poll` 出最小的 → 输出 → 把这条流的下一个元素 `offer` 进去。每输出一个 O(log K)，总共 O(N log K)。

对比：笨办法 A 全部拼起来再排序 O(N log N)；笨办法 B 依次两两合并 O(N·K)。堆版本两者都更好，而且是**流式**的——不必一次读完所有数据。

---

## 7. `java.util.PriorityQueue` 的 API 与实现细节

### 7.1 它就是数组实现的二叉堆

Javadoc 开头：「An unbounded priority queue based on a priority heap.」内部是 `Object[] queue`，用的就是第 2 节的下标公式；`siftUp`/`siftDown` 同第 3、4 节（JDK 用「空洞下沉」优化：待下沉元素拿在手里，孩子逐个上移，最后一次放入，省一半写入）。

### 7.2 构造器

```java
import java.util.*;

public class PqCtors {
    public static void main(String[] args) {
        PriorityQueue<Integer> a = new PriorityQueue<>();                       // 自然顺序，小的先出；初始容量 11
        PriorityQueue<Integer> b = new PriorityQueue<>(64);                     // 指定初始容量（必须 >= 1）
        PriorityQueue<Integer> c = new PriorityQueue<>(Comparator.reverseOrder()); // 大根堆
        PriorityQueue<Integer> d = new PriorityQueue<>(256, Comparator.reverseOrder());
        PriorityQueue<Integer> e = new PriorityQueue<>(List.of(9, 4, 7, 1));    // 从集合建堆：O(n) heapify
        System.out.println(a.size() + " " + b.size() + " " + c.size() + " " + d.size() + " " + e.peek());
    }
}
```

* 初始容量不能是 0（`IllegalArgumentException`），所以参考实现里有 `Math.max(1, k)`。
* 容量不够自动扩容：小于 64 时翻倍加 2，否则增加一半（约 1.5 倍），几何增长，摊还 O(1)。已知规模时传初始容量能避免扩容。

### 7.3 方法一览与复杂度

| 方法 | 作用 | 复杂度 | 空队列时 |
|---|---|---|---|
| `offer(e)` / `add(e)` | 插入 | O(log n) | —（无界，不会满） |
| `peek()` | 看堆顶 | O(1) | 返回 `null` |
| `element()` | 看堆顶 | O(1) | 抛 `NoSuchElementException` |
| `poll()` | 取走堆顶 | O(log n) | 返回 `null` |
| `remove()` | 取走堆顶 | O(log n) | 抛 `NoSuchElementException` |
| `remove(Object o)` | 删除某个元素（`equals` 相等的第一个） | **O(n)** | 返回 false |
| `contains(Object o)` | 是否含有 | **O(n)** | false |
| `size()` / `isEmpty()` | | O(1) | |
| `clear()` | 清空 | O(n) | |
| `iterator()` / `toString()` / `toArray()` | 按**数组下标顺序** | O(n) | **不是排序顺序**，见 8.1 |

`add` 与 `offer` 对 `PriorityQueue` 没区别（不会因满而失败）。`null` 元素不允许（`NullPointerException`），因为 `poll` 用 `null` 表示「空」。元素必须可比较：实现 `Comparable` 或传 `Comparator`，否则 `ClassCastException`。

### 7.4 `Comparator` 的常用写法

```java
import java.util.*;

public class PqComparators {
    record Order(long id, int price, int qty) {}

    public static void main(String[] args) {
        // 价格升序，价格相同时按 id 升序（先到先得）
        Comparator<Order> byPriceThenId = Comparator.comparingInt(Order::price).thenComparingLong(Order::id);
        // 价格降序（买盘最优价最高）
        Comparator<Order> byPriceDesc = Comparator.comparingInt(Order::price).reversed();
        PriorityQueue<Order> bids = new PriorityQueue<>(byPriceDesc.thenComparingLong(Order::id));
        bids.add(new Order(2, 100, 5));
        bids.add(new Order(1, 100, 7));
        bids.add(new Order(3, 101, 1));
        System.out.println(bids.poll() + " " + bids.poll() + " " + bids.poll());
        System.out.println(byPriceThenId.compare(new Order(1, 1, 1), new Order(2, 1, 1)));
    }
}
```

输出（价格 101 最优，其次价格 100 里 id 小的先出）：`Order[id=3, price=101, qty=1] Order[id=1, price=100, qty=7] Order[id=2, price=100, qty=5]`，比较结果 `-1`。

---

## 8. `PriorityQueue` 的坑（每一条都有复现）

### 8.1 坑 1：遍历顺序不是排序顺序

最常见的错误：把 `PriorityQueue` 当「自动排序的集合」，直接 `for (x : pq)` 或 `System.out.println(pq)`。`HeapDemo` B1：

```text
toString / iterator : [1, 4, 2, 9, 8, 7, 6]
poll() until empty  : 1 2 4 6 7 8 9
```

`toString` 打印的是内部数组 `[1, 4, 2, 9, 8, 7, 6]`（5.2 手推的那个堆），不是 `[1, 2, 4, 6, 7, 8, 9]`。Javadoc：「The Iterator provided in method iterator() and the Spliterator provided in method spliterator() are not guaranteed to traverse the elements of the priority queue in any particular order.」

**正确做法**：要有序输出就反复 `poll`；或拷贝再排序：`var sorted = new ArrayList<>(pq); Collections.sort(sorted);`。

### 8.2 坑 2：相同优先级的元素，出队顺序不确定（不稳定）

「稳定」指相同优先级按插入顺序出队。`PriorityQueue` **不保证**（Javadoc：「ties are broken arbitrarily」）。`HeapDemo` B2（8 个任务，优先级交替 0, 1, 0, 1, …，到达顺序 t0…t7）：

```text
arrival t0..t7, priorities 0 1 0 1 0 1 0 1 -> t0 t4 t6 t2 t1 t3 t5 t7
with sequence-number tie-break            -> t0 t2 t4 t6 t1 t3 t5 t7
```

第一行：优先级 0 的四个任务出队顺序是 t0 t4 t6 t2，不是到达顺序 t0 t2 t4 t6。这是堆内部结构造成的，不是随机，但依赖实现细节，**换个 JDK 版本都可能变**。

**修法**：给每个元素一个单调递增序号，比较器加 `thenComparingLong(seq)`——第二行就稳定了。订单簿「同价位先到先得（价格-时间优先）」必须这样做。

```java
import java.util.*;

public class StablePq {
    record Entry(String name, int priority, long seq) {}

    public static void main(String[] args) {
        PriorityQueue<Entry> pq = new PriorityQueue<>(
                Comparator.comparingInt(Entry::priority).thenComparingLong(Entry::seq));
        long counter = 0;
        for (int i = 0; i < 6; i++) pq.add(new Entry("t" + i, i % 2, counter++));
        StringBuilder sb = new StringBuilder();
        while (!pq.isEmpty()) sb.append(pq.poll().name()).append(' ');
        System.out.println(sb);   // t0 t2 t4 t1 t3 t5
    }
}
```

### 8.3 坑 3：改了元素里决定顺序的字段，堆不会知道

`PriorityQueue` 没有「更新优先级」（decrease-key）方法。入队后修改排序键，堆内部数组不会重排，之后的 `peek`/`poll` 就错了。`HeapDemo` B3：

`HeapDemo` B3 的真实输出：

```text
peek() after b8.k = 1 -> 5   (should be 1)
peek() after remove+add -> 1
```

四个元素 5, 6, 7, 8 入堆后把 8 改成 1，堆顶仍是 5（堆没重新整理）。

**修法**：

1. **先 remove 再 add**：`pq.remove(x); x.key = newKey; pq.add(x);`，`remove(Object)` 是 O(n)。
2. **懒删除（lazy deletion）**：不删旧条目，直接插入带新优先级的**新条目**；`poll` 出来时检查是否过期（和 map 里记录的最新版本对不上），过期就丢弃再 `poll`。Dijkstra、事件调度的标准技巧，每个操作保持 O(log n)。
3. **索引堆**（indexed priority queue）：自己实现，额外维护 `位置[id]`，支持 O(log n) 的 decrease-key。

**让元素不可变**（`record`）是最好的预防。

### 8.4 坑 4：比较器写成减法会溢出

```java
// 坑：x - y 在差值超过 int 范围时溢出，符号错误
new PriorityQueue<Integer>((x, y) -> x - y);
// 正确
new PriorityQueue<Integer>(Integer::compare);
```

`HeapDemo` B4（放 `Integer.MIN_VALUE`、1、−1）：

```text
bad comparator poll order  : -1 1 -2147483648
Integer::compare poll order: -2147483648 -1 1
```

错的版本先吐出 −1、1，最后才是最小的 `Integer.MIN_VALUE`：`1 - Integer.MIN_VALUE` 溢出成负数，比较器误认为「1 小于 MIN_VALUE」。永远用 `Integer.compare` / `Long.compare` / `Comparator.comparingInt`。

### 8.5 坑 5：`PriorityQueue` 不是线程安全的

多线程读写用 `java.util.concurrent.PriorityBlockingQueue`（单把锁，内部同样是堆）或自己加锁。高并发低延迟场景更常见的设计是**单线程拥有堆**，其他线程通过队列把任务/事件交给它。

### 8.6 坑 6：`remove(Object)` 和 `contains` 是 O(n)

一百万元素的 `PriorityQueue` 上每处理一个事件就 `remove(obj)`，整体 O(n²)。用懒删除或索引堆。

### 8.7 坑 7：`PriorityQueue(Collection)` 对 `SortedSet` 和另一个 `PriorityQueue` 有特殊路径

传入 `SortedSet` 或 `PriorityQueue` 时构造器**沿用它的比较器**并直接拷贝（已是合法顺序，不用重新 heapify）；传入其他 `Collection` 用自然顺序并 heapify。元素不可比较则构造时抛 `ClassCastException`。

### 8.8 坑 8：没有「最大 k 个」的现成 API

需要自己写 top-k（6.1）。`stream().sorted().limit(k)` 是 O(n log n)，n 很大 k 很小时不如手写堆 O(n log k)。

---

## 9. 堆在性能敏感代码里的常数问题

* **装箱**：`PriorityQueue<Long>` 里每个 `Long` 是堆上对象，比较要追指针（cache miss）。合并多路流时把堆做成 `long[]` 加平行数组，就是为消掉这个开销。
* **d 叉堆**：二叉改 4 叉，树更矮（log₄ n = (log₂ n)/2），孩子在数组里相邻（一次缓存行读入），上浮更便宜、下沉要比 4 个孩子。很多高性能实现（如 Boost 的 `d_ary_heap`）用 4 叉或 8 叉；`PriorityQueue` 是二叉。
* **价格有界的订单簿**，最优价用「数组 + 位图/指针」比堆更好：O(1) 找最优价、O(1) 插入。堆只在候选集合无界、没有结构可利用时才是正确选择。
* **取消订单**要按 id 删除，而堆 `remove(Object)` 是 O(n)——订单簿**不用** `PriorityQueue` 而用 `TreeMap` + 价位队列的原因之一。

---

## 10. 什么时候用堆，什么时候不用

| 需求 | 用什么 |
|---|---|
| 反复取最小/最大，增量插入 | **`PriorityQueue`** |
| K 路归并、事件模拟（按时间触发）、定时器 | **`PriorityQueue`** |
| 最大的 k 个 | 大小为 k 的 **小根堆** |
| 需要有序遍历、范围查询、前驱/后继 | `TreeMap`，不是堆 |
| 按 id 取消/改优先级 | 索引堆，或 `TreeMap` + `HashMap`，或懒删除 |
| 键是有界小整数 | 桶数组（计数排序式），O(1) |
| 并发多线程竞争同一个队列 | `PriorityBlockingQueue` 或「单线程 + 队列」模式 |

---

## 11. 面试追问预演

**Q1：为什么 `PriorityQueue` 的 `poll` 是 O(log n)，`peek` 是 O(1)？**
答：「堆顶永远是最小元素，在数组下标 0，所以 peek O(1)。poll 把末尾元素搬到根再下沉，路径长度是树高 log n，每层常数次比较。」

**Q2：建堆为什么是 O(n)？**
答：「从最后一个非叶子节点倒着下沉。高度为 h 的节点最多 n/2^(h+1) 个，每个最多下沉 h 步，总和 Σ h·n/2^(h+1) = O(n)，因为 Σ h/2^h 收敛到 2。逐个插入是 O(n log n)。」

**Q3：怎么用 `PriorityQueue` 合并 K 个有序数组？时间和空间？**
答：「堆里放 K 个元素：（值，数组编号，下标）。poll 最小的，输出，把同一数组的下一个元素 offer 进去。每个元素进出堆一次，O(N log K)，空间 O(K)。比较器加数组编号做平局裁决保证稳定。」

**Q4：我要支持「修改某个任务的优先级」，怎么做？**
答：「`PriorityQueue` 不支持 decrease-key。修改很少就 remove 再 add（O(n)）；通用做法是懒删除：保留旧条目，插入新版本，poll 出来时核对版本号丢弃过期的；必须严格 O(log n) 且旧条目不能留，就实现带位置表的索引堆。」

**Q5：`PriorityQueue` 迭代为什么不是有序的？**
答：「它只保证父不大于子，兄弟之间无序，迭代走内部数组顺序。要有序必须 poll，代价 O(n log n)。」

---

## 12. 自测题

**Q1（手算）** 依次 `add` 4, 7, 2, 9, 1，画出每一步之后的数组（小根堆）。

<details><summary>答案</summary>

```text
add 4: [4]
add 7: [4, 7]            7 的父亲是 4，7 ≥ 4，不换
add 2: [4, 7, 2] → 2 < 4，换 → [2, 7, 4]
add 9: [2, 7, 4, 9]      9 的父亲下标 1（值 7），9 ≥ 7，不换
add 1: [2, 7, 4, 9, 1] → 父亲下标 1（7），1 < 7 换 → [2, 1, 4, 9, 7]
                          → 父亲下标 0（2），1 < 2 换 → [1, 2, 4, 9, 7]
```

</details>

**Q2（手算）** 对 `[1, 2, 4, 9, 7]` 做一次 `poll`，写出结果数组。

<details><summary>答案</summary>

取走 1；末尾 7 搬到根：`[7, 2, 4, 9]`。根 7 的孩子是 2 和 4，较小是 2，7 > 2，交换：`[2, 7, 4, 9]`。7 在下标 1，孩子下标 3 的值 9，7 ≤ 9，停。结果 `[2, 7, 4, 9]`。

</details>

**Q3（下标）** 下标 11 的节点，父亲是谁？它的孩子下标是多少？

<details><summary>答案</summary>

父亲 (11 − 1) / 2 = 5。左孩子 2×11 + 1 = 23，右孩子 24。

</details>

**Q4（概念）** 为什么「找最大的 k 个」用的是小根堆而不是大根堆？

<details><summary>答案</summary>

堆里要保存「目前最大的 k 个」，其中最小的是「下一个会被淘汰」的，需要 O(1) 看到并 O(log k) 移除——正是小根堆的堆顶。新元素比堆顶大就替换。大根堆堆顶是最大的，没法快速知道该淘汰谁。

</details>

**Q5（代码）** 写一个函数，返回数组中第 k 大的元素（1 ≤ k ≤ n），复杂度 O(n log k)。

<details><summary>答案</summary>

```java
import java.util.PriorityQueue;

public class KthLargest {
    static int kthLargest(int[] a, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>(k);   // 小根堆，保存当前最大的 k 个
        for (int x : a) {
            if (heap.size() < k) heap.add(x);
            else if (x > heap.peek()) { heap.poll(); heap.add(x); }
        }
        return heap.peek();                                      // 这 k 个里最小的就是第 k 大
    }

    public static void main(String[] args) {
        System.out.println(kthLargest(new int[]{3, 2, 1, 5, 6, 4}, 2));   // 5
    }
}
```

</details>

**Q6（调试）** 下面代码想按 `Task.deadline` 从早到晚处理任务，同一 deadline 按提交顺序。有什么问题？

```java
import java.util.*;

public class Q6 {
    static class Task { long deadline; String name; Task(long d, String n) { deadline = d; name = n; } }
    public static void main(String[] args) {
        PriorityQueue<Task> pq = new PriorityQueue<>((a, b) -> (int) (a.deadline - b.deadline));
        pq.add(new Task(3_000_000_000L, "x"));
        pq.add(new Task(1, "y"));
        System.out.println(pq.poll().name);
    }
}
```

<details><summary>答案</summary>

两个问题。（1）`(int)(a.deadline - b.deadline)`：long 差值强转 int 会截断。3_000_000_000 − 1 = 2_999_999_999 截成 int 是 −1_294_967_297（负数），比较器认为 "x" 比 "y" 早，`poll()` 先吐 "x"，而 deadline 更早的是 "y"。用 `Long.compare`。（2）同 deadline 的顺序没保证（不稳定），需序号字段加 `thenComparingLong(seq)`。另外 `deadline` 是可变字段，入队后别改。

</details>

**Q7（辨析）** 一个堆里有一百万个元素，你想判断「某个值 x 是否在堆中」。能做得比 O(n) 好吗？

<details><summary>答案</summary>

仅靠堆不行：堆只保证父子有序，没有兄弟间信息，无法剪枝。要么多维护一个 `HashSet`（或 `HashMap<id, count>`）与堆同步，查询 O(1)；要么换成 `TreeSet`/`TreeMap`。

</details>

---

「延伸」下一章：有序映射与树（`ordered_maps_trees.md`）。
