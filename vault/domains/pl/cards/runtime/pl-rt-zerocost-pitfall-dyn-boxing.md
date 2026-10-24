---
id: pl-rt-zerocost-pitfall-dyn-boxing
node: runtime.zero-cost-abstractions
type: qa
step: 9
---
## Q
哪些写法会悄悄让“零成本抽象”失效，变成真实的运行时成本？请各举一个 Rust、Java、Go 的例子。

## A
抽象失效的共同原因是：**编译器或 JIT 看不到调用目标，或者数据被装进了堆对象。**

**Rust：`dyn` 阻断内联。** 同样的“偶数平方和”，把闭包换成 `&dyn Fn(u64) -> u64` 传入：
```rust
fn dynamic(v: &[u64], f: &dyn Fn(u64) -> u64) -> u64 {
    let mut s = 0;
    for &x in v { if x % 2 == 0 { s += f(x); } }
    s
}
```
50M 元素：约 17.5 毫秒，而迭代器链或手写循环约 6.6 毫秒，慢约 2.6 倍（一次测量）。虚表调用本身不贵，贵的是它阻止了内联、融合和向量化。

**Java：装箱。** 同一计算：
- `int[]` 手写循环 16.7 毫秒；
- `IntStream` 11.2 毫秒；
- `List<Integer>.stream()` 19.1 毫秒（一次测量，小整数在缓存里，装箱对象多数还是命中缓存）。
差距在这里不算大，但内存是另一回事：`int[]` 每元素 4 字节，`ArrayList<Integer>` 每元素约 4 字节引用加约 16 字节对象头与数据（取决于 JVM 配置），5000 万元素时占用相差数倍，缓存命中率也更差。更大的值（超出 `Integer` 缓存范围 -128 到 127）会真实分配对象。

**Go：接口与闭包的逃逸。** 把值赋给 `interface{}`、通过接口方法调用、闭包捕获局部变量，可能触发堆分配与间接调用。查看方法是：`go build -gcflags=-m` 看 “escapes to heap”，`go test -bench -benchmem` 看每次操作的分配数。

**共同的诊断套路**：
1. 先用基准测试 + 剖析器确认确实是热点；
2. 看分配（Rust 的 `cargo flamegraph`/dhat，Java JFR，Go `-benchmem`）与内联报告；
3. 把热路径上的间接调用与装箱换成静态类型。

教训：抽象不是免费的，免费的只是**编译器能证明的那部分**。
