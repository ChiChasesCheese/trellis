---
id: pl-abstraction-generics-implementation-best-practice
node: abstraction.generics-implementation
type: qa
step: 8
---
## Q
了解泛型的实现方式后，资深工程师在各语言里怎样据此写代码？

## A
- **Java（擦除）**：性能敏感的数值路径避免 `List<Integer>`，用 `int[]` 或基本类型专用集合；需要运行期类型时显式传 `Class<T>`（类型令牌），不要靠反射猜；设计泛型 API 时不要期望运行期能区分 `List<A>` 和 `List<B>`。
- **Rust（单态化）**：控制代码膨胀。对大函数使用「薄泛型外壳」：泛型函数只做类型转换，然后调用一个非泛型的内部函数，这样大体积的逻辑只生成一份。

```rust
pub fn read<P: AsRef<Path>>(p: P) -> io::Result<String> {
    fn inner(p: &Path) -> io::Result<String> { /* 大量逻辑，只编译一次 */ }
    inner(p.as_ref())
}
```

  标准库的 `std::fs::read` 就是这个写法。编译时间成为问题时，用 `cargo build --timings` 找出被重复实例化最多的泛型函数。
- **Go**：热点循环上，值类型的泛型与手写等价；对指针类型的泛型方法，知道调用会经过字典。性能敏感的路径用基准测试验证，不要假设泛型一定更快或更慢。
- **Python**：泛型对运行期无影响，不需要考虑性能。

通用原则：**把泛型保留在接口层，把重逻辑下沉到非泛型函数**，这样既有类型安全，又不重复生成大量代码。
