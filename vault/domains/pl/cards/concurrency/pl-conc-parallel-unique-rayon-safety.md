---
id: pl-conc-parallel-unique-rayon-safety
node: concurrency.parallelism
type: qa
step: 8
---
## Q
同样是「并行遍历 10 万个数并收集到一个 Vec」，Java 并行流和 Rust rayon 对错误写法的反应有何不同？这说明了什么？

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

说明：
- 并行 API 的易用性（`.parallel()`、`par_iter()`）会诱导程序员把顺序代码“一键并行”。顺序代码里无害的副作用，在并行里就成了数据竞争。
- Java 把正确性留给程序员，只在文档里提示“无状态、无干扰、无副作用”；Rust 把这些条件翻译成 trait bound，编译器强制。
- 通用规则：并行的函数式风格——用 `map`/`reduce`/`collect` 产生新值——而不是在循环里修改外部变量。
