---
id: hl-cq-q09-code-optional-variant
node: cpp-questions.b-standards
type: qa
step: 19
---
## Q
补全代码：写一个返回 `std::optional<int>` 的函数 `parse(std::string_view s)`，空串返回“无值”，否则返回长度；再声明一个装着字符串 `"hi"` 的 `std::variant<int, std::string>` 并用 `std::visit` 访问；最后写出 CTAD 创建 `pair` 和 `vector`。

## A
```cpp
std::optional<int> parse(std::string_view s) {
    if (s.empty()) return std::nullopt;
    return static_cast<int>(s.size());
}
std::variant<int, std::string> var = std::string("hi");
std::visit(Print{}, var);       // 按当前持有的类型调用对应重载
std::pair p(1, 2.5);            // CTAD：pair<int,double>
std::vector w{1, 2, 3};         // CTAD：vector<int>
```
