---
id: hl-c08-cpp17-optional-variant-code
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 8
---
## Q
写出用 `std::from_chars` 严格解析整数、返回 `std::optional<int>` 的函数，以及一个 `std::variant<int,double,std::string>` 的 visitor。

## A
```cpp
std::optional<int> parse_int(std::string_view s) {
    int v = 0;
    auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    if (ec != std::errc{} || ptr != s.data() + s.size()) return std::nullopt;
    return v;
}

using Msg = std::variant<int, double, std::string>;
struct Visitor {
    std::string operator()(int i) const { return "int " + std::to_string(i); }
    std::string operator()(double d) const { return "double " + std::to_string(d); }
    std::string operator()(const std::string& s) const { return "string " + s; }
};
// std::visit(Visitor{}, msg)
```
- 严格：`ptr` 必须走到末尾，否则 `"42abc"` 也会被当成功。
