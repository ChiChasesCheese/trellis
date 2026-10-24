---
id: pl-memory-memory-layout-pitfall-pointers
node: memory.memory-layout
type: qa
step: 8
---
## Q
「元素指针的切片」和「元素值的切片」的遍历速度为什么能差一个数量级？

## A
同样是求 400 万个结构体里某个字段的和，Go 里两种数据布局：

```go
type P struct{ X, Y int64 }

v1 := make([]P, N)       // values stored inline: one contiguous block
v2 := make([]*P, N)      // 4M pointers, each to a separately allocated P
// v2 was then shuffled, so memory order differs from index order

for i := range v1 { s += v1[i].X }   // sequential reads
for i := range v2 { s += v2[i].X }   // one pointer hop per element
```

本机一次基准测试（N = 400 万，12 核 Apple 芯片）：

```console
BenchmarkInline     898533 ns/op      (about 0.9 ms)
BenchmarkPointers  8601992 ns/op      (about 8.6 ms)
```

约 10 倍。原因：
- `[]P` 是 64 MB 的连续内存，CPU 顺序读取，预取器提前把后面的缓存行读进来，几乎不会等内存。
- `[]*P` 的元素地址被打乱，每个 `v2[i].X` 要先读指针，再跳到随机地址，几乎每次缓存未命中。一次未命中的延迟是几十到上百 ns，这里各次加载互不依赖，CPU 能同时发出多个，摊下来每个元素约 2 ns，而顺序读取约 0.2 ns。如果是链表那样「下一个地址要等上一个读完才知道」的依赖链，就无法重叠，更慢。

这是「数据布局决定性能」最直观的例子：算法完全相同，复杂度同为 O(N)，常数差一个数量级。

踩坑场景：
- Java 里用 `List<Integer>` 或 `List<Point>` 做大批量计算，对象散落在堆中；换成 `int[]` 或者结构数组（把各字段拆成各自的数组，SoA，structure of arrays）可以显著加速。
- Python 里对大量数字做循环，每个都是堆对象；NumPy 在连续数组上批量运算。
- C++ 里同样的坑是 `std::vector<T*>`、`std::list` 和 `std::map`（每个节点单独分配）：能用 `std::vector<T>` 就别用它们。
- 在 Go、Rust 里不要无谓地使用 `[]*T`，除非元素确实需要共享或大到复制不划算。
