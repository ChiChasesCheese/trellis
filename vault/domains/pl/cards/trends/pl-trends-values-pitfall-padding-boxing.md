---
id: pl-trends-values-pitfall-padding-boxing
node: trends.value-types
type: qa
step: 11
---
## Q
布局问题在生产里怎样出现？结构体填充浪费内存、对象数组的随机访问、`__dict__` 的内存膨胀各是什么样子？

## A
**1. 填充悄悄浪费内存（Go、Rust 的 `repr(C)`）**。一个只有三个字段的结构体：

```go
type Bad  struct { A bool; B int64; C bool }   // unsafe.Sizeof = 24
type Good struct { B int64; A bool; C bool }   // unsafe.Sizeof = 16
```

真实输出：24 字节对 16 字节。一亿个这样的结构体，差距是 800 MB。Rust 默认会自动重排，所以默认布局下只有 16 字节，但在 `#[repr(C)]` 下（FFI 需要）又变回 24 字节。

**2. 对象数组的乱序访问（Java）**。把一千万个 `record P(int x, int y, int z)` 放进数组再乱序访问，真实结果约 55 ms，而同样数据的 `int[]` 约 13 ms。症状：算法没问题，性能分析里全是缓存未命中；代码看起来无可挑剔。

**3. `__dict__` 膨胀（Python）**。每个普通实例都带一个字典：一个三个属性的实例，实例本身 48 字节，`__dict__` 288 字节，合计超过 330 字节；用 `__slots__` 只有 56 字节。百万个对象的差距是 330 MB 对 56 MB，直接决定服务是否 OOM。

**4. 装箱（Java 泛型）**。`List<Integer>` 里每个元素是 `Integer` 对象，`Map<Integer, Integer>` 每个条目有两个 `Integer` 加一个节点。热路径上的这类容器是 GC 压力与缓存未命中的首要来源。

**共同模式**：这些问题都不会让程序出错，只是让它慢或占内存，而且在小数据量下完全察觉不到，随数据规模增长才暴露。

**防线**：
1. 为关键结构体写大小断言（Rust 里用 `static_assertions` crate 的 `const_assert!(size_of::<T>() == 16)`，Go 的测试里检查 `unsafe.Sizeof`）。
2. 基准测试使用生产规模的数据量，而不是玩具规模。
3. 用分析工具看内存：Java 的 JFR 分配分析、Go 的 `pprof -alloc_space`、Python 的 `tracemalloc`。
4. 评审时，对“大量小对象”的设计问一句：它们可以是值，或者可以是列吗？
