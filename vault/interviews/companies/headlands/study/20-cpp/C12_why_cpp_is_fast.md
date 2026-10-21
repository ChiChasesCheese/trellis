# C12 · 为什么 C++ 快（以及 Java 在哪里不输）

> 面试原题：*Why is C++ faster than other languages?* 追问：*...than other compiled languages?* 目标：给出**机制**而不是口号，并且诚实地说出 Java 的强项。

## 1. 先说清楚"快"指什么

* **吞吐（throughput）**：单位时间做多少事。
* **延迟（latency）**：一件事多久，尤其是**尾延迟**（p99、p99.9、最坏）。交易系统关心后者。
* **可预测性**：同样的输入每次耗时是否一样。

C++ 的优势主要体现在**尾延迟、可预测性和对内存布局的控制**；稳态吞吐上，热点代码经 JIT 的 Java 可以接近。

## 2. 机制一：运行期系统很薄（"不用不付费"）

* 没有垃圾回收：没有 GC 线程抢核，没有停顿（safepoint）；你不分配就没有分配成本。
* 数组/`vector` 默认**不做边界检查**（`operator[]`），整数运算直接是机器指令（代价是越界成为未定义行为：标准不要求程序此后有任何确定行为）。
* 没有虚拟机和预热：编译一次，进程启动即是满速；Java 要解释 → C1 → C2 逐步优化，并可能因为类型假设失效而**去优化（deoptimization）**。
* 虚函数**只有声明了 `virtual` 才付费**；非虚调用是普通函数调用，且可内联。
* 零开销抽象：迭代器、算法、lambda、`unique_ptr` 在优化后与手写代码生成相同的机器码。

下面三种求和写法生成近乎相同的向量化循环（汇编指令数 75 / 79 / 79 条）：

```cpp
[[gnu::noinline]] long sum_raw(const int* p, std::size_t n) { long t = 0; for (std::size_t i = 0; i < n; ++i) t += p[i]; return t; }
[[gnu::noinline]] long sum_accumulate(const std::vector<int>& v) { return std::accumulate(v.begin(), v.end(), 0L); }
[[gnu::noinline]] long sum_rangefor(const std::vector<int>& v) { long t = 0; for (int x : v) t += x; return t; }
```

排序：比较函数在编译期已知，直接内联进排序循环；`qsort` 每次比较都要经函数指针间接调用：

```text
sums agree: 1
sort 5000000 ints:  std::sort 76.7377 ms,  std::sort + lambda 206.752 ms,  qsort 289.1 ms (qsort/std::sort = 3.76739x)
identical results: 1
```

（这里 `std::sort` 默认 `<` 版本更快，是因为该标准库对整数的默认比较有无分支分区的专用路径；用 lambda 的版本仍然内联，但仍比 `qsort` 快；确切倍数依赖实现。）

## 3. 机制二：值类型与内存布局 → 缓存

现代 CPU 的瓶颈往往是**内存**而不是算术：一次主存访问约等于几百条指令。CPU 以缓存行（通常 64 字节）为单位取数据，并预取顺序访问的数据。

* C++：`vector<Order>` 是一整块连续内存，每个元素就是 `Order` 本身。
* Java：`List<Order>` 是引用数组，每个 `Order` 是堆上另一个带对象头（约 12–16 字节）的对象，GC 搬动后相邻关系还可能变化。遍历 = 指针追逐。
* 结构体字段顺序影响 padding；"热字段"和"冷字段"分开（SoA，struct of arrays）能让只访问部分字段的循环少读几倍数据。

```cpp
struct Order { std::uint64_t id; std::int64_t px; std::int64_t qty; std::uint8_t side; };            // 32 bytes with padding
struct OrderBad { std::uint8_t side; std::uint64_t id; std::uint8_t flag; std::int64_t px; std::int64_t qty; };   // padding between fields
struct OrderPacked { std::uint64_t id; std::int64_t px; std::int64_t qty; std::uint8_t side; std::uint8_t flag; };
```

```cpp
struct Soa { std::vector<std::uint64_t> id; std::vector<std::int64_t> px; std::vector<std::int64_t> qty; };
```

四百万个订单，按 `px*qty` 求和（每个订单的纳秒数）：

```text
sizeof: Order=32 OrderBad=40 OrderPacked=32 (field order changes padding)
notional sum (px*qty) over 4000000 orders, ns per order:
  vector<Order>                 : 0.3314
  vector<unique_ptr<Order>> shuf: 2.88323
  struct of arrays (px, qty)    : 0.154479
  sum of qty only, vector<Order>: 0.303479
  sum of qty only, SoA          : 0.0803396
(sink 0)
```

读法：连续的 `vector<Order>` 比"指针数组（Java 风格，内存顺序被打乱）"快约 8 倍；SoA 只读需要的两列，再快一倍多；只汇总一列时 SoA 又快 4 倍以上（整条缓存行都是有用数据，还能向量化）。`Order` 32 字节，字段顺序不当的 `OrderBad` 变成 40 字节。

## 4. 机制三：模板与内联 → 编译期单态化

泛型代码在编译期为每个类型生成专门版本，调用点可以内联，内联后常量传播、向量化、删除死代码接着发生。虚函数调用是**间接**调用，编译器通常看不到目标，无法内联：

```cpp
struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };
struct Sq : Shape { double s; explicit Sq(double x) : s(x) {} double area() const override { return s * s; } };
struct Rect : Shape { double w, h; Rect(double a, double b) : w(a), h(b) {} double area() const override { return w * h; } };
struct Tri : Shape { double b, h; Tri(double x, double y) : b(x), h(y) {} double area() const override { return 0.5 * b * h; } };
```

```cpp
struct SqV { double s; double area() const { return s * s; } };
struct RectV { double w, h; double area() const { return w * h; } };
struct TriV { double b, h; double area() const { return 0.5 * b * h; } };
using ShapeV = std::variant<SqV, RectV, TriV>;
```

```cpp
template <class S> double total_area(const std::vector<S>& v) { double t = 0; for (const auto& s : v) t += s.area(); return t; }   // resolved at compile time
```

对 200 万个形状求面积（每个形状的纳秒数）：

```text
sum of areas, 2000000 shapes:
  virtual call, random mix   : 4.27186 ns/shape
  std::variant + visit       : 3.89777 ns/shape
  std::function per element  : 4.7915 ns/shape
  template, one concrete type: 0.482917 ns/shape
```

读法：目标不可预测的虚调用 / `variant` / `std::function` 都在 4 ns 左右；同类型数据用模板函数（静态分发，内联，向量化）只要不到 0.5 ns。结论：**热路径上用静态多态（模板、`variant`、按类型分组存放），把虚函数留给冷路径或确实需要运行期扩展的地方**。

## 5. 机制四：CPU 友好、可预测

分支预测：同一个循环，数据随机 vs 已排序：

```cpp
[[gnu::noinline]] long sum_if_big(const std::vector<int>& v, std::vector<int>& out) {
    long t = 0;
    out.clear();
    for (int x : v) { if (x >= 128) { t += x; out.push_back(x); } }       // data-dependent branch with a side effect
    return t;
}
```

```text
  random data: 2.50036 ns/element (sum 7)
  sorted data: 0.420543 ns/element (sum 7)
```

随机数据每个元素约 6 倍慢，因为 `if` 一半对一半错、预测器失败。C++ 让你能控制数据顺序、用无分支写法、`alignas(64)` 对齐、预分配避免 `malloc`、`__builtin_prefetch`、SIMD 内建函数、线程绑核——这些在 JVM 之上要么不可能要么需要绕路。

## 6. 为什么比其他"编译型"语言也快？

编译本身不决定速度，决定速度的是**运行期还剩多少工作**和**你能控制多少**：

| | C++ | Rust | Go | Java (HotSpot) |
|---|---|---|---|---|
| 编译到机器码 | AOT | AOT | AOT | JIT（运行期） |
| GC | 无 | 无 | 有（并发 GC） | 有（可选多种） |
| 默认边界检查 | 无（`[]`） | 有（可被优化消除） | 有 | 有（可被 JIT 消除） |
| 值类型/内联嵌套结构 | 有 | 有 | 有（结构体） | 无（目前只有基本类型） |
| 泛型 | 模板（单态化） | 单态化 | 单态化+字典（1.18+） | 擦除 + 装箱 |
| 优化器成熟度 | 非常高 | 同后端 LLVM | 较弱（编译快优先） | 高（C2） |

所以 C++ ≈ Rust（同样无运行期开销，Rust 的安全检查多在编译期）；对 Go 的优势是无 GC 和更强的优化器；对 Java 的优势是布局和确定性。

## 7. 诚实地说：Java 赢在哪里 / 不输在哪里

* **运行期信息**：JIT 看得到真实的类型分布、分支概率，可以把原本的虚调用去虚化并内联（类似 PGO 的在线版本）；静态编译器没有这些信息（C++ 可以用 PGO/LTO 追平，但要额外流程）。
* **逃逸分析**：不逃出方法的对象可以被消除分配，甚至拆成寄存器。
* **分配速度**：TLAB 指针碰撞，几条指令；对象批量死亡时回收很便宜（只复制存活对象）。C++ 的 `malloc` 要慢，但可以用池避免。
* **安全与生产力**：没有 UB、没有悬空指针；同样的团队规模交付更快、更少安全漏洞。对多数业务，这比最后 20% 的性能更重要。
* **稳态热点循环**可以与 C++ 同一数量级；差距主要在 **预热、GC 暂停、对象头与指针追逐、缺少内联值类型、对硬件的控制**。
* 回答"那为什么交易公司用 C++？"：尾延迟、确定性、内核旁路网络与硬件接近、对内存布局的完全控制——不是 Java 慢，而是 Java 的**最差情况**和**不可控**成分更多。

## 8. 坑

1. 说"C++ 因为编译所以快"：不完整，Go/Java 也编译。
2. 说"C++ 一定比 Java 快"：对非热点或 I/O 密集的程序差别很小；写得差的 C++（到处 `shared_ptr`、虚函数、`std::list`、`endl`）可能更慢。
3. 把"零开销抽象"理解成所有东西免费：`std::function`、异常抛出路径、`shared_ptr` 拷贝、iostream 都有代价。
4. 微基准的陷阱：被优化器整个删除、冷缓存、没预热、没有多次取中位数。
5. 不测量就优化：先 profile（perf、Instruments、火焰图）。

## 9. 面试官接着会问

**Q：为什么 C++ 比 Java 快？Java 什么时候能追上？**
要点：第 2–5 节机制 + 第 7 节诚实对比；结尾落到"稳态可接近，尾延迟和布局是差距"。

**Q：为什么比 Go/Rust 快或慢？**
要点：表格；与 Rust 基本同级；Go 有 GC 和较弱优化器。

**Q：虚函数有多慢？怎么避免？**
要点：一次间接调用 + 阻止内联 + 分支预测失败；用模板/CRTP/`variant`、按类型分批处理、`final` 让编译器去虚化。

**Q：怎样在 C++ 里写低延迟代码？**
要点：热路径零分配（池/arena）、无锁数据结构（SPSC 队列）、缓存行对齐避免伪共享、数据局部性（连续、SoA）、避免系统调用与异常、线程绑核、预热、测量尾延迟。

**Q：缓存局部性是什么？**
要点：时间/空间局部性；缓存行；预取；`vector` 与 `list` 遍历的差异。

**口述版**："It isn't compilation alone. C++ has no GC or VM in the way, data is laid out by value so arrays of structs are contiguous and cache-friendly, templates and inlining remove abstraction cost, and I control allocation. Java closes much of the steady-state gap with its JIT - devirtualization, escape analysis - but C++ wins on tail latency and predictability, which is what matters in trading."

## 10. 自测

1. 为什么 `vector<Order>` 比 `vector<unique_ptr<Order>>` 遍历快？
2. 虚函数调用比普通调用慢在哪里？怎么避免？
3. 为什么说 Rust 和 C++ 速度相近而 Go 不同？
4. 列出 Java 比 C++ 强的 3 点。

<details><summary>答案</summary>

1. 值连续存放，缓存行全是有用数据且可预取；指针版每个元素一次间接寻址和潜在缓存未命中。
2. 间接调用（读虚表）、阻止内联、分支预测目标不稳定；用模板/`variant`/`final`/按类型分组。
3. Rust 与 C++ 都无 GC、值类型、单态化泛型、LLVM 级优化；Go 有 GC 暂停和较弱优化。
4. 运行期 profile 驱动的去虚化/内联、逃逸分析消除分配、内存安全与生产力（另有快速分配、跨平台、成熟库）。

</details>
