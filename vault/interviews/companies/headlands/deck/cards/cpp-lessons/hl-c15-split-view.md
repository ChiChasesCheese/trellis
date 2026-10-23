---
id: hl-c15-split-view
node: cpp-lessons.c15-io-performance
type: qa
step: 4
---
## Q
写出返回 `std::vector<std::string_view>` 的 `split(s, sep)`。为什么不用 `istringstream` 切分？

## A
```cpp
std::vector<std::string_view> split(std::string_view s, char sep = ' ') {
    std::vector<std::string_view> out;
    while (!s.empty()) {
        auto pos = s.find(sep);
        if (pos == std::string_view::npos) { out.push_back(s); break; }
        if (pos > 0) out.push_back(s.substr(0, pos));   // 跳过重复分隔符产生的空字段
        s.remove_prefix(pos + 1);
    }
    return out;
}
```
- `string_view` 切分只产生（指针，长度），**不拷贝、不分配**；返回的视图在原字符串存活期间有效。
- 想要数字就别为了切分去构造 `istringstream`：每次要构造一个带 locale 的流对象。
