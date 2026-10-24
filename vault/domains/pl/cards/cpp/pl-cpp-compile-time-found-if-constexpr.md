---
id: pl-cpp-compile-time-found-if-constexpr
node: cpp.compile-time
type: qa
step: 5
---
## Q
`if constexpr` 与普通 `if` 有什么不同？为什么它能取代很多 SFINAE 和模板特化？

## A
**区别**：普通 `if` 的两个分支**都要通过编译**，只是运行时选一个。`if constexpr` 的条件必须是编译期常量，**未选中的分支在模板里被丢弃，不会被实例化**，因此里面可以写对当前类型根本不成立的代码。

```cpp
template <class T> std::string kind(const T& x) {
  if constexpr (std::is_integral_v<T>) return "int:" + std::to_string(x + 1);
  else return "other:" + std::string(x);   // 对 int 无效，但被丢弃
}
// kind(41) → "int:42"    kind(std::string("s")) → "other:s"
```

`kind(41)` 实例化 `T = int`，`else` 分支里的 `std::string(x)`（从 `int` 构造）本来无法编译，但因为被丢弃，不会报错。实测输出：`int:42 other:s`。

**对比普通 `if`**：同样的函数去掉 `constexpr`，用 `int` 调用时报错：`no matching conversion for functional-style cast from 'int' to 'std::string'`——因为两个分支都被编译。

**为什么能取代 SFINAE / 特化**：以前"对整数做 A，对其他类型做 B"需要两个重载加 `enable_if`，或者两个类模板特化。现在一个函数体里按类型分支，读起来就像普通代码；逻辑集中，不再散落在多个重载里。

**注意事项**：
1. 条件必须依赖模板参数，才会有"丢弃"的效果；在非模板函数里，`if constexpr` 的丢弃分支仍会被完整检查，实测 `else` 里的非法转换照样报错；
2. 被丢弃的分支里的 `return` 类型不参与返回类型推导，所以可以让不同分支返回不同类型（使用 `auto` 返回时尤其有用）；
3. 它不是运行时开销：生成的代码里只有选中的那一支。

**对比 Rust**：Rust 没有对应物，因为 trait 的特化和 `cfg` 各担一部分；Zig 的 `comptime if` 与它同类。

**要记住的一点**：写模板时需要按类型分叉，优先用 `if constexpr`，其次 concepts 重载，最后才是 `enable_if`。
