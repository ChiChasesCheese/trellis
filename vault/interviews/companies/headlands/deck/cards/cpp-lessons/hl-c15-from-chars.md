---
id: hl-c15-from-chars
node: cpp-lessons.c15-io-performance
type: qa
step: 5
---
## Q
写出用 `std::from_chars` 严格解析数字的模板函数 `parse_num<T>(string_view)`。`stoi`、`strtol`、`from_chars` 的区别？

## A
```cpp
template <class T>
std::optional<T> parse_num(std::string_view s) {
    T v{};
    auto [p, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    if (ec != std::errc{} || p != s.data() + s.size()) return std::nullopt;  // 拒绝 "12abc" 和 ""
    return v;
}
```
- `from_chars`（`<charconv>`，C++17）：**不抛异常、不看 locale、不分配**，返回（结束指针，错误码）；检查 `ptr == end` 才能拒绝 `12abc`。整数和浮点都支持（浮点较晚，旧编译器要用 `strtod`）。
- `stoi`：抛异常，且对 `"12abc"` 返回 12 不报错；有 `string` 开销。
- `strtol`：错误码风格，受 locale 影响。
