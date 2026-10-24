---
id: pl-rt-opt-pitfall-dce-benchmark
node: runtime.optimizations
type: qa
step: 10
---
## Q
为什么微基准（microbenchmark）里的循环有时测出来是几十纳秒？优化器的死代码消除怎样毁掉基准，各语言用什么办法防它？

## A
基准代码常常是：计时、跑被测函数、丢掉结果、计时。优化器看到**结果没有任何人用**，被测函数又没有副作用，按“可观察行为不变”规则就可以把整个调用删掉。

Rust 实测（`-O`，10 亿次迭代的整数运算循环）：
```rust
let t = Instant::now(); let _ = work(n);              // result unused
println!("result unused:  {:?}", t.elapsed());        // 42ns
let r = work(black_box(n)); black_box(r);
println!("black_box used: {:?}", t.elapsed());        // 137ms
```
输出 `result unused: 42ns` 和 `black_box used: 137.129042ms`：前者什么也没测，编译器连循环都删了；`std::hint::black_box` 告诉编译器“把这个值当作可能被外部使用”，循环才被保留。

**其他语言**：Java 的 JIT 同样有权这样做；本机上的同类例子里 HotSpot 保留了循环（每遍约 215 ms），但这是一个**实现细节**而非保证，所以 JMH（Java 微基准框架）要求把结果交给 `Blackhole.consume`。Go 编译器不会删除这种循环（实测约 225 ms），但在 `testing.B` 里仍惯例把结果存进包级变量（sink）。Python 解释器不会删代码，没有这个问题。

另外三个常把基准做错的原因：
1. **常量传播**：入参是常量时，整个计算在编译期完成。要让输入来自 `black_box` 或运行时数据。
2. **预热**：JIT 语言的头几次迭代跑在解释器/低层级编译里；基准必须包含预热并看稳定后的数值。
3. **用 debug 构建测**：Rust 默认 debug 构建的迭代器链会慢一个数量级。

做法：用语言各自的基准框架（Go `testing.B`、Java JMH、Rust `criterion`/`divan`、Python `pyperf`/`timeit`），不要手写 `time.now()` 减法；怀疑结果太好时，对比两个数量级不同的 `n`，耗时不随 `n` 变化就是被消除了。
