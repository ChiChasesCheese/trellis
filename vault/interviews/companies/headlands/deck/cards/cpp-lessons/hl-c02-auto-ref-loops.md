---
id: hl-c02-auto-ref-loops
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 8
---
## Q
范围 for 循环里 `for (auto e : v)`、`for (auto& e : v)`、`for (const auto& e : v)` 有什么区别？`for (auto x : vec) x *= 2;` 能改 `vec` 吗？

## A
- `auto e`：**复制**每个元素，修改的是副本，`vec` 不变。所以 `for (auto x : vec) x *= 2;` **不能**改 `vec`。
- `auto& e`：引用，**就地修改**原元素。
- `const auto& e`：只读且**不复制**。
- 拿不准就写 `const auto&`。

```cpp
std::vector<int> v{1, 2, 3};
for (auto& e : v) e *= 2;   // v 变成 2 4 6
```
