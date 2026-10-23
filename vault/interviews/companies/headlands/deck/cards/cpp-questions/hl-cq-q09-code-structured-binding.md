---
id: hl-cq-q09-code-structured-binding
node: cpp-questions.b-standards
type: qa
step: 17
---
## Q
补全代码：遍历 `std::map<std::string, int> m`，用 C++17 结构化绑定取出 `sym` 和 `px`；再写一个 `if` 语句，在条件里先执行 `auto it = m.find("AAPL")` 并判断它不等于 `m.end()`。

## A
```cpp
for (const auto& [sym, px] : m) { /* ... */ }          // 结构化绑定

if (auto it = m.find("AAPL"); it != m.end()) {         // if 带初始化语句
    /* 用 it */
}
```
`it` 的作用域只在这个 `if` 内。
