# J17 · Foreign Function & Memory API：安全地用堆外内存、调 C 函数

> **Java 21 预览（第三次预览）；JDK 22 转正。** 编译 `javac --release 21 --enable-preview`，运行 `java --enable-preview`；调 C 函数再加 `--enable-native-access=ALL-UNNAMED`。
> 可运行代码：`examples/J17/`。前置：「堆」（heap）和 GC（J19 细讲）；不会 `ByteBuffer` 也行，第 1 节会说。

---

## 1. 先看痛点

### 1.1 从零讲：堆内与堆外

Java 对象住在 **堆**（heap）里，由 **GC**（Garbage Collector，垃圾回收器）自动管理：`new` 出来，没人引用了 GC 就回收。方便，但有代价：

* GC 工作时要**扫描**堆里的对象（找哪些还活着），对象越多越大工作量越大。
* 对象的位置和布局由 JVM 决定：每个对象有 12–16 字节对象头；数组里放 `Long` 是**指针数组**，每个元素指向别处。你无法控制「这 100 万条记录在内存里连续」。
* GC 回收/整理时会暂停或拖慢应用（现代 GC 把暂停压到毫秒以下，吞吐与内存占用仍有代价）。

**堆外内存**（off-heap / native memory）是堆之外、由 OS 直接分配的内存，GC 完全看不见。好处：

1. 能放**很大**的数据，且**不增加 GC 工作量**；
2. 布局由你定：连续、按缓存行对齐、像 C 的 `struct` 数组；
3. 可与别的进程共享（共享内存、`mmap` 文件），可直接交给 C 库。

代价：**你**负责释放；无保护的越界/用后释放就是 C 里的段错误（崩进程）。FFM API 的目标：**既要堆外的好处，又要 Java 级别的安全**。

### 1.2 Java 8 的做法与痛点（`examples/J17/J17Old.java`）

`ByteBuffer.allocateDirect(n)` 是 Java 1.4 起的堆外办法：

```java
final int REC = 24, ID = 0, PX = 8, QTY = 16;     // 偏移量全靠手算，是魔法数字
ByteBuffer buf = ByteBuffer.allocateDirect(n * REC).order(ByteOrder.nativeOrder());
buf.putLong(i * REC + PX, 18_950 + i);
long px = buf.getLong(i * REC + PX);
```

三个结构性痛点：

1. **容量是 `int`**：最大约 2 GB。想要 3 GB 的表？`allocateDirect((int) 3_000_000_000L)` 因为 `(int) 3e9 = -1294967296` 抛 `IllegalArgumentException`，只能拆成多个 buffer。
2. **没有 `close()`**：要等 GC 发现 `ByteBuffer` 不可达再由 `Cleaner` 释放；GC 不紧张时可能很久不释放，`-XX:MaxDirectMemorySize` 满了就 `OutOfMemoryError: Direct buffer memory`。想「用完立刻还」只能用 `sun.misc.Unsafe` 或反射黑科技。
3. **没有结构**：偏移量、类型靠人记，改一个字段要改一堆魔法数字。

另一条路 **JNI**（Java Native Interface）调 C：要写 C 代码、生成头文件、编译成 `.so`、处理平台差异，繁琐易错。FFM 的第二个目标就是**取代 JNI**。

---

## 2. 语法逐条讲

> JDK 21 预览 API。5.1 列出 JDK 22 的不兼容变化。

### 2.1 `Arena`：内存的「生命周期」

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment seg = arena.allocate(32, 8);     // 32 字节，8 字节对齐；已清零
    ...
}   // close()：这块内存立刻归还；之后访问 seg → IllegalStateException
```

| 工厂方法 | 谁能访问 | 谁来释放 | 用途 |
|---|---|---|---|
| `Arena.ofConfined()` | **只有创建它的线程**（别的线程访问抛 `WrongThreadException`） | 你 `close()` | 默认选择，最快 |
| `Arena.ofShared()` | 任何线程 | 你 `close()`（关闭时要与所有线程同步，较慢） | 多线程共享；堆外 ticker map 用它 |
| `Arena.ofAuto()` | 任何线程 | **GC** 回收（不能手动 close） | 不想管释放，但仍要比 `ByteBuffer` 更清晰的接口 |
| `Arena.global()` | 任何线程 | 永不释放 | 程序级常量 |

### 2.2 `MemorySegment`：带边界的一段内存

```java
seg.set(ValueLayout.JAVA_LONG, 0, 18_950L);        // 偏移（字节）0 处写 long
seg.get(ValueLayout.JAVA_INT, 8);                  // 偏移 8 处读 int
seg.setAtIndex(ValueLayout.JAVA_LONG, 2, 7L);      // 按元素下标（偏移 = 2 * 8）
seg.byteSize();                                     // 长度（long，不是 int：可超过 2GB）
```

* 每次访问都**检查边界**和**生命周期**（所属 `Arena` 是否还活着）：越界 → `IndexOutOfBoundsException`，关闭后访问 → `IllegalStateException`（`Already closed`）。
* **`ValueLayout`** 描述"这个位置是什么类型"：`JAVA_LONG`、`JAVA_INT`、`JAVA_DOUBLE`、`JAVA_BYTE`、`ADDRESS`（指针）等。`JAVA_LONG` 要求偏移是 8 的倍数（对齐）；不对齐用 `JAVA_LONG_UNALIGNED`。

### 2.3 `MemoryLayout`：用声明代替魔法数字

```java
static final StructLayout FILL = MemoryLayout.structLayout(
        ValueLayout.JAVA_LONG.withName("id"),
        ValueLayout.JAVA_LONG.withName("px"),
        ValueLayout.JAVA_INT.withName("qty"),
        MemoryLayout.paddingLayout(4));            // 补到 8 的倍数
FILL.byteSize();                                    // 24
FILL.byteOffset(PathElement.groupElement("px"));    // 8，JDK 替你算
VarHandle PX = FILL.varHandle(PathElement.groupElement("px"));   // 读写 px 字段的 VarHandle
SequenceLayout POOL = MemoryLayout.sequenceLayout(1_000_000, FILL);   // 100 万个 FILL
```

* `structLayout`：像 C 的 `struct`；`sequenceLayout(n, elem)`：像 C 的数组；`paddingLayout`：显式填充。
* `layout.varHandle(路径)` 给你一个 **`VarHandle`**（一个能对变量做各种强度原子读写的句柄，见 J16）：JIT 能把它内联成一条加载/存储指令。JDK 21 里 `POOL.varHandle(sequenceElement(), groupElement("px"))` 得到的句柄，调用是 `PX.get(segment, index)` / `PX.set(segment, index, value)`。

### 2.4 调 C 函数：`Linker` + `FunctionDescriptor`

```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
        linker.defaultLookup().find("strlen").orElseThrow(),
        FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));   // size_t strlen(const char*)
long len = (long) strlen.invokeExact(cString);
```

* **downcall**：Java 调 C。`FunctionDescriptor.of(返回类型, 参数类型...)` 描述 C 签名，得到 `MethodHandle`。
* **upcall**：C 回调 Java（如 `qsort` 的比较函数），用 `linker.upcallStub(...)`。
* `allocateUtf8String("...")`（JDK 21 名字）：把 Java 字符串复制成以 `\0` 结尾的 C 字符串。
* 这些是**受限方法**（restricted methods）：能破坏内存安全（传错签名就崩进程）。JDK 21 不带 `--enable-native-access=ALL-UNNAMED` 会打印警告（见 3 节）。

---

## 3. 编译器和 JVM 到底做了什么

* **编译器**：识别预览 API，要求 `--enable-preview`，无新语法。
* **每次 `MemorySegment` 访问**：边界检查 + 生命周期检查 + 线程检查（`ofConfined`）。JIT 内联后消掉大部分（循环里的边界检查可外提/消除），热路径性能接近原生数组，但**不是零成本**。
* **分配**：`arena.allocate` 底层是 `malloc`/`posix_memalign` 类调用，并**保证清零**；`close()` 是 `free`。JVM 里没有对应堆对象，GC 不扫描；可用 `-XX:NativeMemoryTracking=summary` 观察堆外使用。
* **`downcallHandle`**：JVM 运行时**生成一小段机器码**（桩，stub）做调用约定转换（寄存器传参、栈布局），这就是取代 JNI 的方式——不需要预编译的 C 胶水代码；一次调用成本与 JNI 同量级或更低。
* **受限方法警告**：不带 `--enable-native-access` 运行 `J17Ex3`：

```
WARNING: A restricted method in java.lang.foreign.Linker has been called
WARNING: java.lang.foreign.Linker::downcallHandle has been called by the unnamed module
WARNING: Use --enable-native-access=ALL-UNNAMED to avoid a warning for this module
```

* **预览标记**：用了 FFM 的类被标记为依赖预览，必须 `--enable-preview` 运行。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——分配、读写、越界与关闭（`J17Ex1.java`）

输出：

```
byteSize = 32, 新分配的第一个 long = 0
读回: px=18950 qty=100
getAtIndex(2) = 7
越界 -> IndexOutOfBoundsException
arena 关闭后访问 -> IllegalStateException: Already closed
shared arena：另一线程写入 -> 主线程读到 99
confined arena：别的线程访问 -> WrongThreadException
```

三种"安全网"：新内存清零、越界抛异常（而不是读垃圾/崩溃）、关闭后抛异常（而不是 use-after-free）。

### 例 2：进阶——用 `MemoryLayout` 开一个 100 万条成交记录的堆外池（`J17Ex2.java`）

`struct Fill { long id; long px; int qty; pad }` = 24 字节，`sequenceLayout(1_000_000, FILL)` = 24 000 000 字节：

```java
MemorySegment pool = arena.allocate(POOL);
POOL_PX.set(pool, i, 18_950L + (i % 100));            // (segment, 元素下标, 值)
long px = (long) POOL_PX.get(pool, i);
```

输出：

```
FILL.byteSize = 24, alignment = 8
offset(px) = 8, offset(qty) = 16
pool.byteSize = 24000000
n = 1000000, qty = 102999997, notional = 1956948443049, VWAP = 18999.500000461165
```

对照堆上做法：`record Fill(long id, long px, int qty)` + `Fill[] pool = new Fill[1_000_000]`：每个 `Fill` 是独立对象（对象头 + 字段，约 32 字节），数组里是 100 万个引用，GC 要追踪 100 万个对象；堆外版本是 **一块连续的 24 MB**，GC 眼里"一个都没有"，离开 `try` 块立刻归还，不用等 GC。

手算核对 qty：`100 + (i % 7)`，7 个一循环平均 103：1 000 000 × 100 + Σ(i%7) = 100 000 000 + (142857 个完整循环 × 21 + 剩余 1 个周期中前 1 个元素 `0`) = 100 000 000 + 2 999 997 = 102 999 997，吻合。

### 例 3：调用 C 函数（`J17Ex3.java`）

```java
MethodHandle strlen = linker.downcallHandle(libc.find("strlen").orElseThrow(),
        FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));
try (Arena arena = Arena.ofConfined()) {
    MemorySegment cStr = arena.allocateUtf8String("AAPL.O");
    long len = (long) strlen.invokeExact(cStr);
}
```

输出（带 `--enable-native-access=ALL-UNNAMED`）：

```
strlen("AAPL.O") = 6
getpid() == ProcessHandle.current().pid() ? true
```

不用写一行 C 代码。`invokeExact` 要求调用点的静态类型**精确**匹配（`(long)` 强转、参数是 `MemorySegment`），否则运行时抛 `WrongMethodTypeException`。

---

## 5. 坑与限制

### 5.1 预览 API：后续版本改了什么

| | JDK 21（本课） | JDK 22（**转正**） |
|---|---|---|
| 状态 | 第三次预览，要 `--enable-preview` | **正式 API**，不需预览参数 |
| 字符串 | `arena.allocateUtf8String(s)` | 改名 `arena.allocateFrom(s)` |
| `MemoryLayout.varHandle` 的坐标 | `(MemorySegment, long… 每个开放路径元素一个)` | `(MemorySegment, long 基偏移, long… 每个开放路径元素一个)` —— **多一个"基偏移"坐标**。例 2 的 `PX.get(pool, i)` 在 22 要写成 `PX.get(pool, 0L, i)` |
| 受限方法 | 不带 `--enable-native-access` 打印一次警告 | 同；新增 JAR 清单属性 `Enable-Native-Access` 可在可执行 JAR 中授权；未来版本可能强制要求该选项 |
| 其他 | | 新增：下行调用可传堆上段（linker 选项）、可编程构建 C 函数描述符、更好支持变长数组、本地字符串可用任意字符集 |

JDK 21 相对 JDK 20 的主要变化：`Arena` 统一了生命周期管理；布局路径新增解引用地址布局的元素；Linker 新增优化短调用的选项；新增基于 libffi 的回退 linker；移除 `VaList`。

### 5.2 手动 `close()` 才是责任所在

忘了 `close()`（`ofConfined`/`ofShared`）= 内存泄漏，GC 帮不了你；`ofAuto()` 由 GC 回收但时机不确定。用 `try-with-resources`。`Arena.close()` 二次调用会抛异常，所以堆外 ticker map 的 `close()` 写成 `if (arena.scope().isAlive()) arena.close();`。

### 5.3 关闭后的 `MemorySegment` 引用不是 `null`

仍持有引用，但访问抛 `IllegalStateException`——安全（不崩）但是运行时错误；别把 segment 存进比 arena 活得更久的对象。

### 5.4 线程限制

`ofConfined` 的 segment 被别的线程访问抛 `WrongThreadException`。测试框架换线程（如 JUnit 超时断言在别的线程运行）时用 `ofShared`。

### 5.5 `ofShared().close()` 比较慢

关闭时需保证没有其他线程正在访问，JVM 要握手（类似安全点）。别在热路径反复开关 shared arena。

### 5.6 边界检查与对齐

* 热循环里每次访问仍有检查（JIT 通常能优化，不保证）；
* `JAVA_LONG` 在不 8 字节对齐的偏移访问抛 `IllegalArgumentException`，不对齐访问用 `JAVA_LONG_UNALIGNED`。

### 5.7 它不能让"错误的 C 签名"变安全

`FunctionDescriptor` 写错（如把 `int` 写成 `long`），JVM 无从得知，轻则乱码，重则崩进程——`downcallHandle` 是受限方法的原因。

### 5.8 何时不该用

数据量不大、没有 GC 压力证据时，`long[]` / 对象数组更简单更安全，JIT 对它们优化得最好。先用 JFR 确认 GC 是瓶颈，再考虑堆外。

---

## 6. 真实代码里的 FFM

**`OffHeapTickerMap`**（堆外的定长哈希表），整个文件就是本课的真实例子：

```java
import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;
...
private static final long SLOT_BYTES = 16;
...
// ofShared：允许别的线程使用（JUnit 的超时断言会换线程）；ofConfined 只允许创建它的线程访问，略快
this.arena = Arena.ofShared();
this.seg = arena.allocate(capacity * SLOT_BYTES, 64);   // 分配出来的内存保证已清零，所以 key == 0 就是空格
...
private long keyAt(int slot) { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES); }
private long valueAt(int slot) { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES + 8); }
...
@Override
public void close() {
    if (arena.scope().isAlive()) arena.close();
}
```

对应本课：

* **`Arena.ofShared()` vs `ofConfined()`**（2.1、5.4）：作者在注释里解释了为什么选 shared。
* **`arena.allocate(size, 64)`**：第二个参数是**对齐**，64 = 一条缓存行；"4 个 16 字节槽位正好一行"，一次探测落在同一条缓存行内。
* **"内存保证已清零，所以 key == 0 就是空格"**（2.2）：用「全零 = 空槽」省掉初始化，同时 `checkKey` 要求 key > 0。
* **`seg.get(ValueLayout.JAVA_LONG, 字节偏移)`**：手算偏移（`slot * SLOT_BYTES`），没用 `MemoryLayout`，因为槽位只有 `[key:8][value:8]` 两个字段；字段多了就该用 2.3。
* **类注释里的动机**："GC 完全看不见它：不管表有多大，GC 扫描/整理的工作量都不变（低延迟系统避免 GC 抖动的常见手段）"；"代价：要手动 close()；没有自动扩容（固定容量，超过就报错）；每次访问有边界检查（JIT 能消掉大部分）"。面试时可直接当答案。
* `close()` 的 `isAlive()` 检查：5.2。

**面试话术**：「为什么堆外？」——「GC 不扫描，延迟可预期；布局连续并对齐缓存行；可换成共享内存。代价：手动 close、固定容量、有边界检查。JDK 21 里 FFM 还是预览，22 转正，生产环境我会先评估版本。」

参考实现没用到 `Linker`（downcall），那部分只在例 3。

---

## 7. 自测题

1. `ByteBuffer.allocateDirect` 有哪三个结构性问题？FFM 各用什么解决？
2. `Arena.ofConfined()` 与 `ofShared()` 的区别？`OffHeapTickerMap` 为什么选 `ofShared()`？
3. 下面代码运行会怎样？
   ```java
   MemorySegment s;
   try (var a = Arena.ofConfined()) { s = a.allocate(16, 8); }
   s.get(ValueLayout.JAVA_LONG, 0);
   ```
4. 用 `MemoryLayout` 写一个 `struct { int side; int qty; long px; }` 的布局，并说出 `px` 的偏移。
5. JDK 21 → JDK 22，FFM API 有哪些要改的地方（至少两处）？

<details><summary>答案</summary>

1. 容量是 `int`（≤2GB）→ `MemorySegment.byteSize()` 是 `long`；无法确定性释放 → `Arena` + `close()`；无结构、偏移靠魔法数字 → `MemoryLayout`/`VarHandle`。
2. `ofConfined` 只能创建它的线程访问，最快；`ofShared` 任何线程可访问，但 `close()` 要与其他线程同步，较慢。选 `ofShared` 是因为 JUnit 超时断言会换线程，confined 会抛 `WrongThreadException`。
3. 抛 `IllegalStateException`（arena 已关闭），不崩进程，因为每次访问都检查生命周期。
4. ```java
   StructLayout L = MemoryLayout.structLayout(
       ValueLayout.JAVA_INT.withName("side"), ValueLayout.JAVA_INT.withName("qty"),
       ValueLayout.JAVA_LONG.withName("px"));
   ```
   `px` 偏移 8（前两个 int 共 8 字节，且 8 字节对齐），总大小 16。
5. FFM 在 22 转正，不再需 `--enable-preview`；`allocateUtf8String` 改名 `allocateFrom`；`MemoryLayout.varHandle` 的句柄多一个"基偏移"`long` 坐标；另新增 `Enable-Native-Access` 清单属性。

</details>

---

「延伸」J18 比较器与接口：`Comparator` 组合器和 `default`/`static` 接口方法。
