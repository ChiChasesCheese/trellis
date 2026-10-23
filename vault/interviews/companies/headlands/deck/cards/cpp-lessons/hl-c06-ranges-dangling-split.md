---
id: hl-c06-ranges-dangling-split
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 17
---
## Q
`std::ranges::find(std::vector<int>{1,2,3}, 2)` 返回什么？为什么？再写出用 ranges 按逗号切分字符串和取反转后的前三个。

## A
- 对**临时容器**用 ranges 算法，返回的不是迭代器，而是 `std::ranges::dangling`：因为临时 vector 在语句末就销毁，迭代器会悬空；对返回值的使用**编译不过**，把悬空 bug 提前到编译期。
- 切分与反转：

```cpp
for (auto part : csv | rv::split(','))
    std::cout << std::string(part.begin(), part.end()) << ' ';   // AAPL MSFT NVDA
for (int x : v | rv::reverse | rv::take(3)) {}                   // 10 9 8
```
- 视图遍历期间底层容器不能被修改；`filter` 缓存 `begin()`，多次遍历的复杂度要小心。
