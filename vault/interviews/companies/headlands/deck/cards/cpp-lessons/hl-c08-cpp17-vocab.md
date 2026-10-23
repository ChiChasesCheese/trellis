---
id: hl-c08-cpp17-vocab
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 7
---
## Q
C++17 的「词汇类型」`optional`、`variant`、`any`、`string_view` 分别解决什么问题？结构化绑定和 `if` 初始化语句呢？

## A
- `std::optional<T>`：「可能没有值」，不用 null 或哨兵值。
- `std::variant<A,B,C>`：类型安全联合体（对应 Java 的 sealed interface），用 `std::visit` 访问。
- `std::any`：类型擦除的任意值。
- `std::string_view`：零拷贝字符串视图。
- 以前靠指针/哨兵值/裸 `union`。
- **结构化绑定** `auto [k, v] = ...`：解包 pair/tuple/结构体；**`if`/`switch` 带初始化**：缩小变量作用域。

```cpp
if (auto [it, inserted] = m.try_emplace("AAPL", 100); inserted) { /* ... */ }
for (const auto& [sym, qty] : m) std::cout << sym << ' ' << qty;
```
