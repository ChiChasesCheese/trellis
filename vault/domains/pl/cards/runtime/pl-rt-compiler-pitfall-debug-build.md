---
id: pl-rt-compiler-pitfall-debug-build
node: runtime.compiler-pipeline
type: qa
step: 9
---
## Q
为什么用 Rust 的 debug 构建做性能测试会得出错误结论？优化级别对 AOT 语言的运行速度有多大影响？

## A
AOT 编译器的优化是**可选的、成本高昂的**步骤。Rust 的 `cargo build`（debug）默认 `opt-level=0`，不做内联，保留溢出检查和调试信息，以换取最快的编译和最好的调试体验。抽象层在 debug 下并不“零成本”：迭代器的每个适配器、每个小函数都是真实的函数调用。

实验：同一段素数计数代码（`(2..).take_while(...).all(...)` 迭代器链），区间 0 到 800 万，单线程（一次测量）：
```
rustc cpu.rs        (opt-level=0): 1 thread  539777 primes 7.96s
rustc -O cpu.rs     (opt-level=3): 1 thread  539777 primes 0.63s
```
debug 慢约 13 倍。这与 Java 的情形相反：Java 的字节码本身不优化，但 JIT 在运行时总会优化热点，所以没有“debug 版比 release 版慢十倍”这回事。

典型事故：
1. **用 debug 构建做基准**，得出“Rust 比 Go 慢”的错误结论；
2. **把 debug 构建部署到生产**，CPU 突然飙升；
3. **测试跑得慢**，因为测试默认是 debug profile；
4. 反过来，release 构建默认**关闭整数溢出检查**（回绕），而 debug 会 panic：一个只在 release 下出现的数值 bug。

做法：
- 性能相关的一切（基准、压测、线上）只用 `--release`，基准用 `cargo bench` / criterion；
- 在 CI 里至少有一份 release 构建的测试，覆盖溢出等差异；
- 如果测试需要速度，给依赖开优化（见 profile 覆盖），或用 `[profile.test] opt-level = 1`。
- Go 的默认构建已带优化，`-gcflags="-N -l"` 才是调试用的关闭优化；Python 无此区分。
