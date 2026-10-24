---
id: pl-conc-parallel-unique-rayon-safety
node: concurrency.parallelism
type: qa
step: 8
---
## Q
同样是「并行遍历并汇总」，Java 并行流、Rust rayon 和 C++ 并行算法对错误写法的反应有何不同？这说明了什么？

## A
错误写法：并行遍历里直接往共享列表里 `add` / `push`。

Java：
```java
List<Integer> out = new ArrayList<>();
IntStream.range(0, 100_000).parallel().forEach(out::add);
```
编译通过，运行输出 `size = 14316 (expected 100000)`（再跑一次是 13615）。`ArrayList` 不是线程安全的，大量元素丢失，也可能抛 `ArrayIndexOutOfBoundsException`。正确做法是 `collect`：`.boxed().collect(Collectors.toList())`，得到 `size = 100000`。

Rust rayon：
```rust
let mut out = Vec::new();
(0..100_000).into_par_iter().for_each(|i| out.push(i));
```
编译错误：
```
error[E0596]: cannot borrow `out` as mutable, as it is a captured variable in a `Fn` closure
expects `Fn` instead of `FnMut`
```
rayon 的 `for_each` 要求闭包是 `Fn + Sync`（可被多线程同时调用），而 `push` 需要可变借用，所以编译器拒绝。正确做法是用 `collect()`，或 `map` 之后归并。

C++（C++17 并行算法，对 100 万个 1 求和，`-fexperimental-library` 编译）：
```cpp
long long total = 0;
std::for_each(std::execution::par, v.begin(), v.end(),
              [&](int x) { total += x; });   // [&] captures total by reference
```
`-Wall -Wextra` 下没有任何警告，运行三次输出 `total = 116305`、`113446`、`122904`（期望 1000000）。`-fsanitize=thread` 能报出 data race；语言本身不拒绝。数据竞争在 C++ 里是未定义行为，所以这里只是碰巧得到错值而不是崩溃。

说明：
- 并行 API 的易用性（`.parallel()`、`par_iter()`）会诱导程序员把顺序代码“一键并行”。顺序代码里无害的副作用，在并行里就成了数据竞争。
- Java 和 C++ 把正确性留给程序员，只在文档里提示“无状态、无干扰、无副作用”（Java 至少不会因此未定义，C++ 会）；Rust 把这些条件翻译成 trait bound，编译器强制。
- 通用规则：并行的函数式风格——用 `map`/`reduce`/`collect` 产生新值——而不是在循环里修改外部变量。
