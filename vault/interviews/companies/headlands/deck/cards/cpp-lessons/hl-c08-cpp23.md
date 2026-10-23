---
id: hl-c08-cpp23
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 14
---
## Q
C++23 补了哪些 C++20 的缺口？`std::expected` 怎么用？

## A
- `std::expected<T, E>`（返回值或错误，不用异常，类似 Java 的 `Result<T,E>`）、deducing this、`ranges::to`、`views::zip`、`std::print`、`if consteval`。
- 编译器/标准库对 23 的支持还不齐，面试里单独提一句即可。

```cpp
std::expected<int, std::string> parse_qty(const std::string& s) {
    try { return std::stoi(s); }
    catch (...) { return std::unexpected("bad qty: " + s); }
}
```
- 成功得到 `100`，失败得到 `error: bad qty: abc`。
