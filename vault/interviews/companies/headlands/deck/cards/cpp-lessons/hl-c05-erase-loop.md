---
id: hl-c05-erase-loop
node: cpp-lessons.c05-stl-containers
type: qa
step: 12
---
## Q
写出 `vector`（或 `map`）"边遍历边删除偶数"的正确循环。为什么 `erase` 后不能直接 `++it`？

## A
```cpp
for (auto it = v.begin(); it != v.end();) {
    if (*it % 2 == 0) it = v.erase(it);   // erase 返回下一个有效迭代器
    else ++it;
}
```
- `erase(it)` 之后 `it` 已**失效**，再 `++it` 是 UB；必须用返回值 `it = v.erase(it)`。
- `map` 写法相同：`it = m.erase(it)`；节点容器里只有被删元素的迭代器失效。
- 例：`{1..6}` 得 `1 3 5`；`map` 键 `1,2,3,4` 删偶数后剩 `1=10 3=30`。
