---
id: hl-c05-operator-bracket-inserts
node: cpp-lessons.c05-stl-containers
type: qa
step: 16
---
## Q
`std::map` / `unordered_map` 的 `operator[]` 查询一个不存在的 key 会发生什么？只想查询应该用什么？

## A
- `operator[]` 会**插入**一个默认构造的值（`int` 为 0），`size()` 随之变化。
- 因此它也破坏 `const` 正确性：`const map` 上没有 `operator[]`。
- 只想查用 `find`（返回迭代器，和 `end()` 比较）或 `contains`（C++20），不会插入：

```cpp
if (auto it = m.find(k); it != m.end()) use(it->second);
```
- 实测：`m[5]` 后值为 0、`size` 变 1；`find()` 不改 `size`。
