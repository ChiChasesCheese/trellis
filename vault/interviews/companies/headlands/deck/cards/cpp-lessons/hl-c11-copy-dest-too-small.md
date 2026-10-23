---
id: hl-c11-copy-dest-too-small
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 13
---
## Q
`std::copy(v.begin(), v.end(), w.begin())` 当 `w` 比 `v` 短（例如空 vector）时会怎样？怎么修？

## A
- `std::copy` **不会扩容**，`w.begin()` 之后写入越界，是 UB。
- 修法二选一：
  1. 先 `w.resize(v.size())`。
  2. 用 `std::back_inserter(w)` 作为目标，让它 `push_back`。

```cpp
std::copy(v.begin(), v.end(), std::back_inserter(w));
```
