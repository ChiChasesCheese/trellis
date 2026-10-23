---
id: hl-c02-string-view-span
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 9
---
## Q
`std::string_view` 和 `std::span` 是什么？为什么适合当函数参数？

## A
视图（view）= **一个指针 + 一个长度**，**不拥有**数据，`sizeof` 都是 16 字节。
- `string_view` 能接受字面量、`std::string`、字符数组，**不分配内存**；`first_token` 之类的 `substr` 是 O(1)，只是新的（指针，长度）。
- `std::span<const int>` 能接受 `vector`、`std::array`、C 数组、子区间，用一个参数覆盖它们。

```cpp
int count_char(std::string_view s, char c);
long sum(std::span<const int> xs) {
    return std::accumulate(xs.begin(), xs.end(), 0L);
}
```
对比 Java：`String` 参数是廉价引用；C++ 的 `std::string` 按值会复制。
