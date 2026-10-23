---
id: hl-cq-q20-code-concept-sfinae
node: cpp-questions.e-templates
type: qa
step: 2
---
## Q
补全代码：写一个 concept `Priceable`，要求 `t.price()` 合法且返回值可转成 `double`；用它约束函数 `mark`；再写 C++11 的 SFINAE 版本 `mark_old`。

## A
```cpp
template <class T>
concept Priceable = requires(T t) { { t.price() } -> std::convertible_to<double>; };
template <Priceable T> double mark(const T& t) { return t.price(); }

template <class T> auto mark_old(const T& t) -> decltype(t.price()) { return t.price(); }   // SFINAE
```
- 基础模板同样每个类型实例化一份：`my_max<int>`、`my_max<double>`、`my_max<string>` 各有自己的代码。
- 非类型参数例：`template <class T> struct Box { T v; static constexpr std::size_t bytes = sizeof(T); };`。
