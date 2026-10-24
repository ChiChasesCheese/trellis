---
id: pl-cpp-templates-concepts-found-concepts
node: cpp.templates-concepts
type: qa
step: 4
---
## Q
C++20 的 concepts 是什么？它改善了什么，在哪些地方并没有改变模板的本质？

## A
**concept** 是一个有名字的**编译期谓词**：对类型（或常量）回答"满足这组要求吗"。标准库提供了现成的：`std::integral`、`std::totally_ordered`（支持完整的比较）、`std::random_access_range` 等。你可以把它写在模板头部或 `requires` 子句里：

```cpp
template <std::totally_ordered T> T maxof(T a, T b) { return a < b ? b : a; }
template <class T> requires std::integral<T> std::string d2(T);
```

**改善一：错误在调用点报，且说得明白**。对 `std::ranges::sort(std::list<int>)`，本机真实报错只有 22 行：`candidate template ignored: constraints not satisfied`，`because 'std::list<int> &' does not satisfy 'random_access_range'`。对比 `std::sort(list)` 的 126 行内部回溯，读者一眼知道：链表不支持随机访问。对没有比较运算符的自定义类型调 `maxof`：`'NoOrder' does not satisfy 'totally_ordered'`。

**改善二：按约束重载**。`d2(2)` 与 `d2(2.5)` 分别选 `integral` 与 `floating_point` 版本，输出 `integral`、`floating`。当多个版本都满足时，约束更严格的那个被选（偏序"归并"，subsumption）。以前这需要复杂的 SFINAE 技巧。

**改善三：接口成为文档**。看签名就知道需要什么，不用读实现。

**没有改变的**：concepts 检查的是**调用点**，不检查模板体。`template <std::integral T> void bad(T x) { x.nonexistent(); }` 只要不被实例化就通过编译；用 `bad(1)` 实例化时才报 `member reference base type 'int' is not a structure or union`。也就是说 concept 保证"实参满足约束"，**不保证模板体只使用了约束声明过的操作**。

**与 Rust trait 的差别**：Rust 的泛型函数体只能使用 trait 约束里声明的方法，泛型体在定义时就被检查；C++ 的 concepts 是"入口检查"，体仍是鸭子类型。要让约束与实现一致，只能靠程序员和测试。

**要记住的一点**：concepts 是模板的**接口层**，解决"报错难读"和"重载选择"；它没有把模板改成"定义时检查"的泛型。
