# 基础课 · CPU 缓存与局部性（cache & locality）

> 写法说明见 `study/TEXTBOOK.md`。配套代码：[`examples/CacheDemo.java`](examples/CacheDemo.java)（本章第 2–7 节的所有「本机实测」都来自它一次完整运行的输出，原文见各节）。
> 前置：[complexity](complexity.md) 第 8 节（为什么「一步」不是等价的）。
> 被谁引用：`hc04`（`long[]` 环形缓冲 vs `ArrayDeque<Long>`）、`hc05`（装箱、数组式订单簿 `TickBook`）、`hc06`（指令数组 `int[]`、分支预测）、`hc02`（`long[]` 版归并堆）。
> 这是 Headlands JD 里 "performance" 的核心一章：本章的内容是 Java 低延迟岗位面试里被追问最多的底层知识。

---

## 0. 这一章在讲什么

上一章你学到「O(n) 比 O(n²) 好」。这一章要讲的是：**两个都是 O(n) 的程序，可以差 10–100 倍，原因是它们访问内存的方式不同。**

本章回答七个问题：

1. CPU 比内存快多少？计算机怎么掩盖这个差距？（第 1–2 节：内存层级）
2. 「缓存行」是什么？为什么读一个字节会读进一大块？（第 3 节）
3. 什么样的代码快，什么样的慢？（第 4 节：局部性，含实测）
4. 为什么 `long[]` 比 `ArrayList<Long>` 快一个数量级？（第 5 节：对象布局与指针追逐）
5. 数据怎么摆放最友好？（第 6 节：AoS vs SoA）
6. 两个线程各改各的变量，为什么也会互相拖慢？（第 7 节：伪共享）
7. 为什么同一段代码，数据排序后快了 9 倍？（第 8 节：分支预测）

---

## 1. 问题：CPU 在「等」

### 1.1 一个数量级的差距

一个 CPU 核心每秒执行几十亿条指令（本机约 3–4 GHz，一个时钟周期 ≈ 0.3 ns）。但是从主内存（DRAM）取一个数据要 **约 80–100 ns**（本机实测见 2.3 节：79 ns）——相当于 **300 个时钟周期**。

如果每条指令都要等 300 个周期的内存，CPU 99% 的时间是空转。现代计算机用「多级缓存」来弥补这个差距。

### 1.2 一个比喻（Brendan Gregg 在《Systems Performance》里用的缩放法）

把「1 个 CPU 周期」放大成「1 秒」，其他延迟按比例放大：

```text
CPU 周期 (~0.3 ns)          1 秒
L1 缓存 (~1 ns)             3 秒
L2 缓存 (~3 ns)             9 秒
L3 缓存 (~13 ns)            43 秒
主内存 (~100 ns)            约 6 分钟
SSD (~100 µs)               约 4 天
机械硬盘 (~5 ms)            约 数月
跨洋网络 (~100 ms)          约 数年
```

（数值取自 Gregg《Systems Performance》第 2 版第 2 章「Methodologies」的 "time scale of system latencies" 表，量级可信，具体行的数字请以原书为准。）

一次缓存未命中就是「CPU 去喝了一杯咖啡」。**写高性能代码的核心就是：别让 CPU 去喝咖啡。**

---

## 2. 内存层级（memory hierarchy）与真实延迟数字

### 2.1 是什么

```text
            速度最快、容量最小、最贵
                    ▲
   ┌────────────────────────────────┐
   │ 寄存器 (registers)  ~几百字节   │  ≤ 1 周期
   ├────────────────────────────────┤
   │ L1 缓存  每核 32–128 KB         │  ~4 周期  (~1 ns)
   ├────────────────────────────────┤
   │ L2 缓存  每核/每簇 256 KB–20 MB │  ~12–15 周期 (~3–7 ns)
   ├────────────────────────────────┤
   │ L3 / 系统级缓存  几 MB–几十 MB   │  ~40 周期 (~10–15 ns)
   ├────────────────────────────────┤
   │ 主内存 DRAM  GB 级               │  ~100 ns
   ├────────────────────────────────┤
   │ SSD / 磁盘 / 网络               │  µs – ms
   └────────────────────────────────┘
                    ▼
            速度最慢、容量最大、最便宜
```

### 2.2 公开来源的数字

* **Peter Norvig, *Teach Yourself Programming in 10 Years*** 末尾的 "Approximate timing for various operations on a typical PC"（该页面直接列出）：

  | 操作 | 时间 |
  |---|---|
  | execute typical instruction | 1 ns |
  | fetch from L1 cache memory | 0.5 ns |
  | branch misprediction | 5 ns |
  | fetch from L2 cache memory | 7 ns |
  | Mutex lock/unlock | 25 ns |
  | fetch from main memory | 100 ns |
  | send 2K bytes over 1 Gbps network | 20,000 ns |
  | read 1 MB sequentially from memory | 250,000 ns |
  | fetch from new disk location (seek) | 8,000,000 ns |
  | read 1 MB sequentially from disk | 20,000,000 ns |
  | send packet US to Europe and back | 150 ms |

  这是 Jeff Dean 在 Google 内部演讲「Numbers Everyone Should Know」的同一类表格的公开版本（Dean 的 LADIS 2009 keynote 幻灯片里有原始版）。绝对数字是约 2000 年代的硬件，**请记住量级和比例，不是精确值**。
* **Ulrich Drepper, *What Every Programmer Should Know About Memory* (2007)**，第 3.1 节有一个很小的算例：假设主存访问 200 周期、缓存访问 15 周期，一段代码对 100 个数据各访问 100 次，没有缓存要花 2,000,000 周期，所有数据都能放进缓存则只要 168,500 周期，「提升 91.5%」。第 3.3.2 节用 Pentium 4 实测：工作集在 L1d 内每个元素 < 10 周期，超过 L1d 约 28 周期，超过 L2 则 480 周期以上。

### 2.3 在本机实测的「延迟阶梯」

`CacheDemo` 第 4 部分做**指针追逐**（pointer chasing）：建一个大小为 W 的 `int[] next`，里面是一个随机的单圈排列（每个下标指向下一个要访问的下标），然后反复执行 `p = next[p]`。每次读取依赖上一次的结果，所以 CPU 没法并行或预取，**测得的时间就是真实的单次访问延迟**。

本机（Apple M6，`sysctl` 报告：缓存行 128 B，L1d 96–128 KB 随核类型不同，L2 约 8–20 MB，页大小 16 KB）的真实输出：

```text
working set        4 KB:   1.26 ns/load
working set       16 KB:   1.26 ns/load
working set       64 KB:   1.26 ns/load
working set      256 KB:   2.20 ns/load
working set     1024 KB:   2.84 ns/load
working set     4096 KB:   5.56 ns/load
working set    16384 KB:   7.19 ns/load
working set    65536 KB:  51.35 ns/load
working set   262144 KB:  78.60 ns/load
```

画成「阶梯」：

```text
ns/load
 80 |                                              ┌──────────── 262 MB: 79 ns
 60 |                                     ┌────────┘  64 MB: 51 ns
 40 |
 20 |
  8 |                          ┌──────────             4–16 MB: 5.6–7.2 ns   (L2)
  3 |              ┌───────────┘                       256 KB–1 MB: 2.2–2.8 ns
  1 |──────────────┘                                   ≤ 64 KB: 1.26 ns      (L1)
    +--------+--------+--------+--------+--------+--------+--------+-------→ 工作集大小
          64 KB    256 KB     1 MB     4 MB     16 MB    64 MB    256 MB
```

读法：

* ≤ 64 KB：1.26 ns，全在 L1（约 4 个周期）。
* 工作集超过 L1 容量后，延迟分阶段上升（L2 区间 2–7 ns）。
* 工作集超过约 20 MB（本机 L2 大小）后，跳到 51 ns；再大到 256 MB，达到 79 ns（真正的 DRAM + TLB 缺失）。
* 从 L1 到主存，**延迟差了约 60 倍**。

**注意**：这些数字是这台机器、这次运行的；换一台机器（比如 x86 服务器）阶梯的位置和高度都会变，但**形状**不变。准备面试时记形状和量级：L1 ~1 ns、L2 ~几 ns、L3 ~10 ns、DRAM ~100 ns。

---

## 3. 缓存行（cache line）：缓存搬运的最小单位

### 3.1 是什么

CPU 不是一个字节一个字节地从内存读数据到缓存，而是**一次读一整行**（cache line）。x86 和大多数 ARM 服务器核的缓存行是 **64 字节**；Intel 手册、ARM 的 Cortex 技术参考手册里都是 64 B。**本机（Apple 芯片）是 128 字节**——用 `sysctl hw.cachelinesize` 可以查，输出 `hw.cachelinesize: 128`。所以「缓存行 = 64 字节」是常见值而不是定律，面试时说「通常 64 字节，在 Apple M 系列上是 128」会显得你是真测过的。

Drepper 第 3 章：「nowadays the norm is 64 bytes」。

### 3.2 为什么要按行搬

内存芯片（DRAM）打开一行之后，连续传输多个字的代价很低，但"开一行"本身很贵（Drepper 第 2.2 节）。所以一次取 64 字节比取 8 次 8 字节划算得多。

### 3.3 它怎么工作：地址被切成三段

```text
64 字节缓存行的地址划分（以 32 位地址为例）:

   31                      6 5          0
   ┌────────────────────────┬───────────┐
   │   行号（行地址）         │ 行内偏移   │      偏移 = 低 6 位 = 0..63
   └────────────────────────┴───────────┘
   行号再分成：  [ tag | set ]
        set 决定放进缓存的哪一组（相联度 8 路 = 一组放 8 行）
        tag 用来核对这一行是不是我要的
```

读地址 `A` 的过程：先把 `A` 的低 6 位清零，得到所在行的起始地址；检查缓存里有没有这一行（有 = 命中，几个周期）；没有（缺失，miss）就去下一级整行取回来，放进缓存（可能挤掉一行旧的）。

**你需要记住的推论**：

1. 读 `a[0]` 之后，`a[1]`…`a[15]`（`int` 数组，64 B 行）**已经免费在缓存里了**。
2. 相距 ≥ 64 字节（或 128，视机器）的两次访问，几乎一定是两次不同的缓存行读取。
3. 缓存按「组」映射，两个地址若 `set` 相同会互相竞争（冲突缺失）。当数组的步长恰好是 2 的大幂（比如 4096 字节）时，会反复落在同一组而互相挤掉——Drepper 第 3.3.1 节详细讨论。

---

## 4. 局部性（locality）：什么代码对缓存友好

### 4.1 两种局部性

* **时间局部性（temporal）**：刚用过的数据，很可能马上再用。→ 缓存留着它。例：循环里反复累加同一个变量。
* **空间局部性（spatial）**：用了某个地址，很可能马上用它旁边的地址。→ 缓存行把旁边的也搬来了。例：顺序遍历数组。

CPU 还有**硬件预取器**（hardware prefetcher）：检测到你在顺序（或固定步长）访问，会提前把后面的行取进来，让缓存缺失根本不发生（Drepper 第 6.3 节）。顺序访问因此是最理想的模式。

### 4.2 实验 1：步长（stride）

`CacheDemo` 第 2 部分：在一个 256 MB 的 `int[]` 上，每隔 k 个元素读一个。k 越大，读的元素越少，但**每次读取是否命中新的缓存行**变了：

```text
stride   1 ints (   4 B):   20.78 ms for  67108864 elements -> 0.31 ns/elem
stride   2 ints (   8 B):   10.30 ms for  33554432 elements -> 0.31 ns/elem
stride   4 ints (  16 B):    5.17 ms for  16777216 elements -> 0.31 ns/elem
stride   8 ints (  32 B):    2.83 ms for   8388608 elements -> 0.34 ns/elem
stride  16 ints (  64 B):    2.38 ms for   4194304 elements -> 0.57 ns/elem
stride  32 ints ( 128 B):    7.60 ms for   2097152 elements -> 3.63 ns/elem
stride  64 ints ( 256 B):    4.33 ms for   1048576 elements -> 4.13 ns/elem
stride 128 ints ( 512 B):    2.16 ms for    524288 elements -> 4.12 ns/elem
```

看**每元素时间**那一列：

* 步长 ≤ 32 字节：0.31–0.34 ns/元素。一个缓存行里装下多个被读到的元素，行的代价摊薄了。
* 步长到 64 B：0.57；到 128 B（等于本机缓存行大小）：3.63；再往后稳定在约 4.1 ns。**一旦每次访问都落在新的缓存行里，每元素代价跳升约 12 倍。**
* 注意总时间并不单调（128 B 比 64 B 慢）：因为元素数量也在减半。真正说明问题的是「每元素」。
* 拐点出现在 64→128 字节，与 `hw.cachelinesize = 128` 吻合。（如果在 64 字节行的 x86 机器上做同样的实验，拐点在 64 字节。）

### 4.3 实验 2：行优先 vs 列优先

Java 的二维数组 `int[4096][4096]` 在内存里是「行的数组」：每一行是一个连续的 `int[4096]`（16 KB），行与行之间是不同的对象。

```text
m[0]  → [ m[0][0] m[0][1] m[0][2] ... m[0][4095] ]   ← 连续
m[1]  → [ m[1][0] m[1][1] ...                     ]   ← 另一个连续块
```

两种遍历：

```java
int n = 4096;
int[][] m = new int[n][n];
long s = 0;

// 行优先（row-major）：内层循环走的是同一行，地址连续
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        s += m[i][j];

// 列优先（column-major）：内层循环每次跳到下一行，地址相隔 16 KB
for (int j = 0; j < n; j++)
    for (int i = 0; i < n; i++)
        s += m[i][j];
```

`CacheDemo` 第 3 部分的真实输出：

```text
row-major   :    3.56 ms
column-major:   27.37 ms  (7.7x slower)
```

两段代码做的**加法次数完全一样**（1677 万次），复杂度都是 O(n²)，差 7.7 倍。列优先的每次访问都跳过 16 KB，等于每次都读一个新的缓存行，只用了其中 4 字节，其余 124 字节白搬了（本机 128 字节行）。多次运行这个数字在 6–9 倍之间波动。

**经验法则**：嵌套循环里，**让最内层循环的下标对应内存中连续变化的那一维**。

### 4.4 局部性与算法的关系

* 数组顺序扫描（O(n)）往往比"更聪明的"指针结构（比如链表、树）更快，即使后者渐近复杂度更好。n 不是特别大时，**排好序的数组 + 线性/二分查找 常常打败 `TreeMap`**。
* 哈希表的随机访问每次基本都是缓存缺失（桶位置随机）；这是 `HashMap.get` 还要 10 ns（见 complexity 第 8 节）而不是 1 ns 的原因之一。
* 堆（`PriorityQueue`）是数组，但"父→子"的跳跃（i→2i+1）在大堆里跨缓存行，所以堆排序比快排慢。

---

## 5. Java 的对象布局与指针追逐：为什么 `long[]` 完胜 `ArrayList<Long>`

### 5.1 `long[]` 在内存里长什么样

```text
long[] a = new long[4];

  对象头 (16 B)                       数据 (4 × 8 = 32 B)
 ┌───────────┬───────────┬─────┬─────┬─────┬─────┐
 │ mark word │ klass ptr │ len │ a[0]│ a[1]│ a[2]│ a[3]
 │  (8 B)    │  (4 B)    │(4 B)│ 8 B │ 8 B │ 8 B │ 8 B
 └───────────┴───────────┴─────┴─────┴─────┴─────┘
                    ← 一整块连续内存 →
```

一个 8 字节的 `long` 占 8 字节，加上整个数组共享一个 16 字节头。10⁷ 个 `long` ≈ 80 MB。实测每个元素 **8.2 字节**（`CacheDemo`：`heap per element: long[] 8.2 B`，多出的 0.2 来自测量噪声）。

### 5.2 `ArrayList<Long>` 在内存里长什么样

```text
ArrayList<Long> list
   │
   └─ Object[] elementData  ← 一个引用数组（每个引用 4 字节，开启压缩指针时）
         [ ref0 ][ ref1 ][ ref2 ] ...
            │       │       │
            ▼       ▼       ▼
         ┌──────┐ ┌──────┐ ┌──────┐
         │ Long │ │ Long │ │ Long │   ← 每个 Long 是堆上一个独立对象
         │ 头12B │ │      │ │      │      12 B 对象头 + 4 B 对齐空隙 + 8 B 值 = 24 B
         │ 值 8B │ │      │ │      │
         └──────┘ └──────┘ └──────┘
```

* 每个 `Long` 对象：12 字节头（8 B mark word + 4 B 压缩类指针）+ 4 字节填充（为了让 8 字节的 `long` 对齐到 8 的倍数）+ 8 字节值 = **24 字节**。
* 加上 `elementData` 里指向它的 4 字节引用：**每个元素 28 字节**。
* 实测（`CacheDemo`）：`heap per element: long[] 8.2 B, ArrayList<Long> 28.2 B`。**内存是 3.4 倍。**
* 内存多 3.4 倍意味着同样大小的缓存只能装下 `long[]` 的 1/3.4 的元素。

### 5.3 指针追逐（pointer chasing）

遍历 `ArrayList<Long>`，每个元素要：① 从 `elementData` 读引用；② **跳到那个地址**读 `Long` 对象里的值。第 ② 步的地址取决于第 ① 步的结果，CPU 必须先拿到引用才知道去哪儿读。如果这些 `Long` 对象散落在堆的各处，每次都是一次缓存缺失（~80 ns 级）。

`CacheDemo` 第 1 部分（10⁷ 个元素，求和）的真实输出：

```text
long[]                            :    2.09 ms  (0.21 ns/elem)
ArrayList<Long> (allocation order):    2.98 ms  (0.30 ns/elem)
ArrayList<Long> (shuffled)        :   34.01 ms  (3.40 ns/elem)
```

三行的含义：

1. **`long[]`：0.21 ns/元素。** 顺序读，预取器全程命中，甚至被 JIT 向量化（一条指令处理多个元素）。
2. **`ArrayList<Long>`，对象按分配顺序摆放：0.30 ns/元素，只比 `long[]` 慢 1.4 倍。** 这是个**陷阱**：JVM 给每个线程一块私有分配缓冲（TLAB），`new Long` 就是指针递增，所以连续创建的对象在内存里**恰好是紧挨着的**。遍历时虽然多一层间接，但访问地址仍然是顺序的，预取器仍然能识别。
3. **`ArrayList<Long>`，同样的对象但访问顺序被打乱：3.40 ns/元素，是 `long[]` 的 16 倍。** 这才是真实系统的样子：对象存活了一段时间，经历过多次 GC 搬移、被不同代码在不同时间创建，在堆里的物理顺序和你的逻辑顺序几乎没有关系。每次访问都是一次随机的缓存缺失。

结论：**`ArrayList<Long>` 在最好的情况下和 `long[]` 差不多，在真实系统里可以慢一个数量级；而且内存多用 3.4 倍，GC 压力也更大。** 这就是 hc04 的 `long[]` 环形缓冲、hc02 的 `mergeLongs`、hc05 的 `TickBook` 的动机。

### 5.4 其他常见 Java 对象的开销（压缩指针，64 位 JVM）

| 对象 | 大小 | 说明 |
|---|---|---|
| `Integer` / `Long` / `Double` | 16 / 24 / 16 B | 头 12 B + 值 + 对齐；`Integer` 4 B 值刚好填 4 B 空隙，所以 16 B |
| `Object[]` / `int[]` 的头 | 16 B | 12 B 头 + 4 B 长度 |
| `HashMap.Node` | 32 B | 头 12 + hash 4 + key/value/next 引用各 4，再对齐 |
| `HashMap<Integer,Integer>` 每条目 | 约 32 + 16 + 16 + 桶槽 4 ≈ 70 B | 存 8 字节有效数据 |

（具体大小可以用 OpenJDK 的 JOL 工具 `org.openjdk.jol` 打印，来源：OpenJDK Code Tools 项目。上表是按标准布局规则推算的，面试时说「约」。）

### 5.5 Java 的出路

* **用原始类型数组**：`long[]`、`int[]`；需要映射时用开放寻址 + 两个平行数组自己写，或者用库（Eclipse Collections、fastutil、Agrona 的 `Long2LongHashMap`）。
* **对象池 / 复用**：避免反复分配（hc05 `TickBook`）。
* **堆外内存**（`ByteBuffer.allocateDirect` / FFM 的 `MemorySegment`）：数据布局自己控制，不受 GC 搬移影响（见 [os_processes_threads_ipc](os_processes_threads_ipc.md)）。
* **Project Valhalla 的值类型（value classes）**：目标是让「`Long` 之类的小对象」没有头、能被平铺在数组里。JDK 21 里还没有，面试里知道它存在即可。

---

## 6. AoS vs SoA：数据怎么摆放最友好

### 6.1 是什么

* **AoS（Array of Structs，结构体数组）**：一个对象数组，每个对象带所有字段。Java 的默认做法。
* **SoA（Struct of Arrays，数组的结构体）**：每个字段一个原始类型数组，同一个下标对应同一条记录。

```java
// AoS：每个订单是一个对象，Order[] 里存的是引用
final class Order {
    long id;
    long price;
    int qty;
    boolean buy;
}

// SoA：四条平行数组，下标 i 合起来才是第 i 个订单
final class OrderColumns {
    final long[] id;
    final long[] price;
    final int[] qty;
    final boolean[] buy;

    OrderColumns(int capacity) {
        id = new long[capacity];
        price = new long[capacity];
        qty = new int[capacity];
        buy = new boolean[capacity];
    }
}
```

### 6.2 内存图

```text
AoS（Java）：
   Order[]  [ref][ref][ref][ref] ...
              │    │    │    │
              ▼    ▼    ▼    ▼             每个订单一个对象，约 40 字节
            ┌────┐ ┌────┐ ┌────┐           [头12|qty4|id8|price8|buy1+填充]
            │ ...│ │ ...│ │ ...│           只想读 price 和 qty，也要把整个对象的缓存行读进来

SoA：
   price[]  [p0][p1][p2][p3][p4][p5]...      连续的 long
   qty[]    [q0][q1][q2][q3][q4][q5][q6]...  连续的 int
   id[]     (这个查询里根本不碰，不占缓存)
```

### 6.3 实测

`CacheDemo` 第 5b 部分：500 万个订单，求「价格 ≥ 500 的订单的总数量」，每个订单只读 `price` 和 `qty` 两个字段：

```text
array of objects (allocation order):   12.48 ms
array of objects (shuffled)        :   28.57 ms
parallel arrays (struct of arrays) :    9.83 ms
```

* SoA 最快，比"对象按分配顺序"快 1.3 倍，比"对象顺序被打乱"（真实系统）快 **2.9 倍**。
* 差距没有第 5 节大，因为这个查询里还有一个数据相关的分支 `if (price >= 500)`，随机价格让分支预测失败（第 8 节）占去了相当一部分时间，把内存因素稀释了。**真实测量里经常有多个因素叠在一起，要逐一排除。**

### 6.4 什么时候选哪个

* 查询**只用到部分字段**，且要扫描大量记录（行情分析、聚合、风控批量检查）→ **SoA**。
* 每次操作**同时用到全部字段**，且按 id 随机访问单条记录 → AoS 没问题（SoA 要读 4 条数组的 4 个不同缓存行，反而更差）。
* 订单簿的热路径（hc05 的 `TickBook`）：用平行数组 `head[side][tick]`、`next[]`、`qty[]` 把链表也平铺成数组下标，是 SoA 思想的极致应用。

---

## 7. 伪共享（false sharing）：各改各的变量，却互相拖慢

### 7.1 先理解缓存一致性

多核 CPU 里每个核有自己的 L1/L2。如果核 A 和核 B 都缓存了同一缓存行，A 写了其中一个字节，B 手里那一行就**过期**了——硬件必须保证 B 下次读到新值。这套机制叫**缓存一致性协议**，最经典的是 **MESI**（Modified / Exclusive / Shared / Invalid，Drepper 第 3.3.4 节）：

```text
核 A 想写某行：必须先让其他所有核把这一行标成 Invalid，自己拿到独占 (Modified)。
核 B 之后再读/写这一行：发现自己的副本是 Invalid，必须从核 A 那里把整行拉过来。
```

**一致性的粒度是缓存行，不是变量。**

### 7.2 伪共享是什么

```text
同一个缓存行（64 或 128 字节）里放着两个互不相关的变量：

   ┌───────────────────── 一个缓存行 ─────────────────────┐
   │ counterA (线程1写)  │ counterB (线程2写) │ ......    │
   └────────────────────────────────────────────────────┘

线程1 在核 A 上写 counterA → 整行在核 B 上失效
线程2 在核 B 上写 counterB → 整行在核 A 上失效
→ 这一行在两个核之间来回"乒乓"，每次写都是跨核通信，~50–100 ns
```

两个线程**逻辑上完全独立**，没有共享任何变量，却因为物理上挨在同一缓存行而互相拖慢。所以叫"伪"共享（false sharing）。

### 7.3 实测

`CacheDemo` 第 6 部分：两个线程，各自对"自己的"计数器做 5000 万次 `incrementAndGet`（原子自增，保证每次都真的写内存）。两个计数器放在同一个 `AtomicLongArray` 里，相距 8 字节（同一行）/ 128 字节（本机缓存行大小，相邻行）/ 512 字节：

```text
counters   8 bytes apart:   838.1 ms
counters 128 bytes apart:   284.3 ms
counters 512 bytes apart:   153.0 ms
```

相距 8 字节（同一缓存行）最慢。我把整个 `CacheDemo` 完整跑了三次，8 字节组分别是 1638、1978、838 ms；128 字节组 312、315、284 ms；512 字节组 224、152、153 ms。所以**同一行比分开的行慢约 3–13 倍**，波动很大。为什么波动大：两个线程被操作系统调度到哪两个核上、它们之间隔了多远（同簇还是跨簇），都会影响乒乓的代价；macOS 也不允许把线程绑定到指定核心。结论方向稳定，具体倍数不稳定。

> **诚实的说明**：写 `CacheDemo` 之前，我用一次性的小程序（没有保存进 `examples/`）试过另外两种写法，各 5000 万次或 1 亿次：用 `setOpaque`/`getOpaque` 写，8 字节组和 512 字节组在本机上**几乎没有差别**（都约 124 ms）；用 `volatile` 写，8 字节组约 270 ms、128 字节组约 65 ms，有差别但很吵；用原子读改写（RMW，`incrementAndGet`）差别最明显（约 2200 ms 对 260 ms）。原因：原子 RMW 每次都必须先独占缓存行，对乒乓最敏感。所以 `CacheDemo` 选用了 `incrementAndGet`。**伪共享是否可见，取决于访问是什么类型的、跑在哪些核上。**这也是 `LongAdder` 内部的 `Cell` 要用 `@Contended` 隔开的原因：它们被原子更新。

### 7.4 怎么避免

1. **填充（padding）**：让每个被不同线程高频写的变量独占一个缓存行。

   ```java
   // 手工填充：在热字段前后各留 7 个 long（共 56 字节）。64 字节行够用；Apple 128 字节行需要更多。
   final class PaddedCounter {
       long p1, p2, p3, p4, p5, p6, p7;      // 前填充
       volatile long value;
       long q1, q2, q3, q4, q5, q6, q7;      // 后填充
   }
   ```

   注意：JVM 可能重排字段（它按大小分组放置），所以手工 padding 不是 100% 可靠。常见的稳妥做法是**通过继承层次**强制顺序（Disruptor 就这么做）：父类放前填充，子类放字段，孙类放后填充，因为 JVM 不会把子类字段排到父类字段前面。
2. **`@jdk.internal.vm.annotation.Contended`**：JDK 内部注解，让 JVM 自动在字段前后加填充（默认 128 字节）。`LongAdder` 的 `Striped64.Cell`、`ConcurrentHashMap` 的 `CounterCell` 就用它。用户代码要用需加 `--add-exports java.base/jdk.internal.vm.annotation=ALL-UNNAMED` 和 `-XX:-RestrictContended`。
3. **按线程分片，最后合并**：用 `LongAdder` 代替 `AtomicLong` 做高并发计数。
4. **设计上避免**：让每个线程写自己的数据结构，只在需要时读别人的（比如 SPSC 环形缓冲，head 和 tail 分开放在不同缓存行，见 os 章）。

### 7.5 读写都不共享也有风险：读-读不会，但"写-读"会

只读共享（多个核都只读同一行）没有问题，每个核都持有 Shared 副本。问题只在**有写者**时出现。所以"不变对象 + 多线程读"是对缓存最友好的并发设计。

---

## 8. 分支预测（branch prediction）

### 8.1 先理解流水线

CPU 不是"取一条、执行一条"，而是像工厂流水线：取指 → 解码 → 执行 → 写回，每一级同时处理不同的指令，一个周期可以出好几条指令的结果。

遇到 `if (x > 0)` 这样的条件分支，**下一步该取哪条指令，要等 `x > 0` 算出来才知道**。如果等，流水线就空了十几个周期。所以 CPU 会**猜**（预测）这个分支会走哪边，先沿着猜的方向继续取指执行（**推测执行**）：

* 猜对了：没有任何损失。
* 猜错了：推测执行的结果全部作废，清空流水线，从正确的位置重新开始。惩罚 **约 10–20 个周期**（Intel 的优化手册和 Agner Fog 的 microarchitecture 手册都给出这个量级；Norvig 表里写的是 5 ns）。

### 8.2 预测器怎么猜

现代预测器会记录每个分支最近的历史（以及相关分支的历史），识别模式：「总是跳」「总是不跳」「交替」「每 8 次一轮」都能学会。**随机的 50/50 模式学不会**，只能蒙，一半猜错。

### 8.3 实测：同一份数据，排序前后

`CacheDemo` 第 5 部分：400 万个 `0..255` 的随机整数，循环 20 遍，`if (v >= 128) out[k++ & mask] = v`。

```text
random  :  181.00 ms
sorted  :   19.99 ms
```

**完全一样的数据、一样的代码、一样的复杂度，排序后快 9 倍。**

* 随机顺序：`v >= 128` 是 50% 概率的随机事件，预测器基本瞎猜，一半的分支错误，每次错误付出十几个周期。
* 排序后：前一半全是 `<128`，后一半全是 `>=128`，分支几乎永远可预测（只在中间切换一次）。

这个实验要小心：**JIT 有时会把这类分支编译成无分支的条件移动指令（cmov / csel）**，那么排序前后就看不出差别。我在这里让分支带了一个副作用（写 `out[k++]`），使它难以被转换。所以结果取决于 JIT 做了什么——**这也说明了为什么性能结论要实测，不能只靠推理**。

### 8.4 对写代码的影响

* **热循环里的数据相关分支**要特别警惕：数据"随机"时会很贵。
* 避免分支的写法：用算术代替判断（`sum += (v >= 128 ? v : 0)` 常被编译成 csel）、查表代替 `switch`（hc06 的「解码一次，`int[]`，无分支」就是这个思想）、把数据按类别分开（先分区再处理，不在循环里判断）。
* 低延迟交易系统里常见的做法：让**热路径**（比如收到行情后决定下单的那条路径）里几乎不出现不可预测的分支，把罕见情况（错误处理、日志）放到冷路径。热路径上"最常见的情况"应当总是同一个走向。
* Java 没有 `__builtin_expect` / `likely` 提示，但 JIT 会根据运行时的分支统计自己排布代码（热路径放在一起）。

---

## 9. 把这些用在性能分析上：一个检查清单

遇到"这段代码为什么慢"，按顺序问：

1. **复杂度对吗？** n 是多少？有没有隐藏的 O(n)（`list.contains`、字符串拼接）？
2. **在分配吗？** 热路径里有没有 `new`、装箱、`stream`/lambda 捕获、`String.format`？（`-Xlog:gc`、JFR 的分配剖析、`async-profiler -e alloc`）
3. **数据怎么摆的？** 指针追逐多吗？能不能换成原始类型数组 / SoA？
4. **访问模式？** 顺序、固定步长还是随机？嵌套循环下标顺序对吗？
5. **分支可预测吗？** 数据相关的分支能不能消掉？
6. **多线程共享吗？** 有没有伪共享？锁争用？
7. **测对了吗？** JIT 预热了吗？有没有被死代码消除？见下一节。

工具：`perf stat`（看 cache-misses、branch-misses、IPC，Brendan Gregg 的博客和书里有完整用法）、`perf c2c`（专门找伪共享）、JFR、async-profiler。macOS 上用 Instruments。

---

## 10. 关于本章的测量方法（诚实说明）

`CacheDemo` 是教学用的**粗糙**基准：同一个 JVM 内取若干次运行的最小值，没有隔离其他进程，没有绑核，用 `volatile` 的 `sink` 防止死代码消除。**严肃的 Java 性能测量应使用 JMH**（OpenJDK 的 Java Microbenchmark Harness），它处理预热、分叉进程、黑洞消费结果等问题。本章的数字请当作"量级与方向"，不是精确的 benchmark 结论；多次运行有 ±30% 以上的波动（伪共享的波动更大，见 7.3）。

```text
# JMH 的典型用法（需要 org.openjdk.jmh 依赖，这里仅示意，不是本章的可编译代码）
@State(Scope.Thread) @BenchmarkMode(Mode.AverageTime) @OutputTimeUnit(TimeUnit.NANOSECONDS)
public class SumBench {
    long[] data = new long[10_000_000];
    @Benchmark public long sumLongArray() { long s = 0; for (long v : data) s += v; return s; }
}
```

---

## 11. 常见误区

1. **「O(n) 就是 O(n)，访问顺序无所谓」。**第 4.3 节：同样的 1677 万次加法，列优先慢 7.7 倍。
2. **「`ArrayList<Long>` 和 `long[]` 只差一点点自动装箱」。**在最好情况下是，在真实堆里是 16 倍（第 5.3 节），内存是 3.4 倍。
3. **「缓存行 64 字节」。**常见，但 Apple M 系列是 128（本机 `sysctl hw.cachelinesize`）；伪共享的填充大小要按目标机器来；JVM 的 `@Contended` 默认用 128 来覆盖两种。
4. **「加了 padding 就一定没有伪共享」。**JVM 会重排字段；要用继承层次或 `@Contended`，并实测验证。
5. **「并发就是加线程」。**共享可写数据的线程越多，越容易遇到乒乓。每个线程只写自己的行是最快的。
6. **「微基准的数字可以直接拿来说」。**不用 JMH 的数字要标"粗略"。面试里说"我实测过，量级是…，我知道这不是严谨的 JMH 结果"比说一个精确但不可信的数字更好。
7. **用时间复杂度替代性能分析。**在 Headlands 这类公司，面试官更可能问"你怎么知道它是瓶颈？你会看什么指标？"

---

## 12. 面试追问预演

**Q1：为什么 `long[]` 比 `ArrayList<Long>` 快？**
答：「三个原因。第一，内存：`Long` 是对象，有 12 字节头，加上对齐和引用，每元素 28 字节对 8 字节，我实测 28.2 对 8.2。第二，间接：遍历要先读引用再跳到对象，如果对象不在一起就是随机访问，缓存缺失；我实测打乱顺序后慢 16 倍。第三，GC：10⁷ 个小对象给 GC 增加压力。`long[]` 是一块连续内存，预取器和向量化都能用上。」

**Q2：什么是缓存行？你怎么利用它？**
答：「CPU 和内存之间搬运数据的最小单位，x86 通常 64 字节，Apple 芯片 128。读一个字节会读进整行，所以相邻数据免费。利用方法：顺序访问、让热字段挨在一起、遍历时让内层循环走连续的那一维。反过来，要避免两个线程各自写同一行里的不同变量。」

**Q3：什么是伪共享？怎么发现和解决？**
答：「两个线程写的变量在同一个缓存行，MESI 协议让这一行在两个核之间来回失效，性能骤降，但代码里看不出共享。发现：`perf c2c` 或 VTune 的 false sharing 分析，或者观察加线程反而变慢。解决：填充或 `@Contended` 把热变量隔开，或者按线程分片再合并，`LongAdder` 就是这么做的。我在本机测过，相邻 8 字节的两个原子计数器比相隔一行的慢 3–13 倍。」

**Q4：为什么排序后的数组处理更快？**
答：「分支预测。数据相关的 `if` 在随机数据下无法预测，每次预测错误大约 10–20 个周期；排序后分支行为有规律，预测几乎总对。我测过 9 倍差距，但要注意 JIT 可能把简单分支编译成条件移动，那就看不出差异。」

**Q5：二叉树、链表、数组，在 CPU 眼里区别是什么？**
答：「数组连续，预取友好；链表和树是指针追逐，每步依赖上一步的地址，无法预取，每个节点潜在一次缓存缺失。所以 n 不大时排好序的数组加二分常常赢过 `TreeMap`，我测过 `TreeMap.get` 215 ns 而 `HashMap.get` 10 ns。」

---

## 13. 自测题

**Q1（概念）** 本机缓存行 128 字节。`int[]` 的一个缓存行装多少个 `int`？顺序遍历时平均每多少次访问发生一次缓存行加载？

<details><summary>答案</summary>

128 / 4 = 32 个。顺序遍历时每 32 次访问加载一次新行（实际上硬件预取会提前加载，所以程序感觉不到等待）。

</details>

**Q2（估算）** 一个 `ArrayList<Long>` 有 1000 万个元素，每个元素约 28 字节。总共约多少内存？如果换成 `long[]`？

<details><summary>答案</summary>

10⁷ × 28 B ≈ 280 MB；`long[]`：10⁷ × 8 B = 80 MB。

</details>

**Q3（读代码）** 下面两个函数哪个更快？为什么？

```java
static long sumA(int[][] m) {
    long s = 0;
    for (int i = 0; i < m.length; i++)
        for (int j = 0; j < m[i].length; j++) s += m[i][j];
    return s;
}

static long sumB(int[][] m) {
    long s = 0;
    for (int j = 0; j < m[0].length; j++)
        for (int i = 0; i < m.length; i++) s += m[i][j];
    return s;
}
```

<details><summary>答案</summary>

`sumA` 更快（大矩阵上快数倍）。`m[i]` 是一整行连续的 `int[]`，`sumA` 内层沿着一行连续访问；`sumB` 内层每次换一行（地址相隔一整行的字节数），几乎每次访问都是新的缓存行。注意：`sumB` 还假设所有行等长。

</details>

**Q4（设计）** 你要给一个订单簿存 100 万个订单，字段有 `id`（long）、`price`（long）、`qty`（int）、`side`（boolean）。热路径是"撮合时按价位顺序扫描订单的 qty"。你会用对象数组还是平行数组？为什么？

<details><summary>答案</summary>

平行数组（SoA）：扫描只用 `qty`（以及按价位找订单的链接），不碰 `id`/`price`/`side`，`qty` 数组是连续的 `int`，一个缓存行装 16–32 个订单的数量，扫描几乎全命中。对象数组每个订单约 40 字节，读 `qty` 要拉进整个对象，且对象可能散落在堆里。如果还要按 id 随机取全部字段，可以另配一个 `id → 下标` 的映射。

</details>

**Q5（判断）** 判断：两个线程分别对两个**不同**的 `volatile long` 字段高频自增，这两个字段在同一个对象里，所以不存在共享问题。

<details><summary>答案</summary>

错。它们很可能在同一个缓存行里（对象不大时），产生伪共享。"不同变量"不等于"不同缓存行"。解决：把字段拆到不同缓存行（`@Contended` 或填充），或每个线程各用一个独立对象并填充，或改用 `LongAdder`。

</details>

**Q6（实验设计）** 你怀疑一段 Java 代码慢是因为分支预测失败。你怎么验证？

<details><summary>答案</summary>

（1）用 `perf stat -e branches,branch-misses` 看分支预测失败率；（2）把输入数据排序（或者构造一份完全可预测的数据）重新跑，看时间是否明显下降；（3）把分支改成无分支写法再比较；（4）用 JMH 以免被 JIT 预热、死代码消除误导。若排序后显著变快，基本可以确认。

</details>

**Q7（概念）** 为什么随机访问 `HashMap` 的 `get` 比顺序读数组慢那么多，而且 O(1) 并不意味着"快到可以忽略"？

<details><summary>答案</summary>

`HashMap.get` 要：算哈希、读桶数组（随机位置，缓存缺失）、读 `Node` 对象（另一次缓存缺失）、比较 key（可能还要读 key 对象，第三次缺失）。O(1) 只说明操作数与 n 无关，不说明每一步都在缓存里。本机实测 `get` 约 10 ns（缓存友好的 100 万 key 场景），而顺序读数组 < 1 ns。

</details>

---

## 14. 延伸阅读（只列权威来源）

* **Ulrich Drepper, *What Every Programmer Should Know About Memory*, 2007**（Red Hat；akkadia.org/drepper/cpumemory.pdf）：第 2 章（DRAM 工作原理）、**第 3 章（CPU 缓存：3.1 大图景、3.2 缓存如何运作、3.3 实现细节含 3.3.1 相联度、3.3.2 缓存效应实测、3.3.4 MESI 一致性）、第 6 章（程序员该怎么做：6.2 缓存访问、6.3 预取、6.4.1 伪共享，含图 6.10 的伪共享实测）**。例子是 2007 年硬件，但原理一字未过时。
* **Hennessy & Patterson,《Computer Architecture: A Quantitative Approach》**，第 2 章「Memory Hierarchy Design」与附录 B「Review of Memory Hierarchy」；第 3 章讲分支预测。
* **Intel® 64 and IA-32 Architectures Optimization Reference Manual**：缓存行 64 字节、分支预测与分支惩罚、伪共享的避免建议；以及 **Agner Fog, *The microarchitecture of Intel, AMD and VIA CPUs***（agner.org/optimize）：各代 CPU 的分支预测器与误预测惩罚的实测。
* **Arm® Cortex-A 系列 Technical Reference Manual**：ARM 核的缓存行与缓存层级描述。Apple 芯片的 128 字节缓存行可以在 macOS 上用 `sysctl hw.cachelinesize` 自己验证。
* **Brendan Gregg,《Systems Performance》第 2 版**：第 2 章（延迟的时间尺度表）、第 6 章「CPUs」、第 7 章「Memory」；`perf` 的缓存/分支计数器用法。
* **Peter Norvig, *Teach Yourself Programming in 10 Years***（norvig.com/21-days.html）末尾的时间表；**Jeff Dean, "Numbers Everyone Should Know"**（LADIS 2009 keynote）。
* **Martin Thompson 的 Mechanical Sympathy 博客**与 **LMAX Disruptor 技术论文**（Thompson, Farley, Barker, Gee, Stewart, 2011）：Java 低延迟系统里 padding、缓存行、单写者原则的第一手资料。
* **OpenJDK JOL（Java Object Layout）工具**与 **JEP 142「Reduce Cache Contention on Specified Fields」**（`@Contended` 的来源）。
