---
id: hl-c09-bounds-at
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 6
---
## Q
`vector::operator[]` 和 `vector::at()` 越界时分别发生什么？AddressSanitizer 报什么？

## A
- `v.at(i)` 越界抛 `std::out_of_range`；`v[i]` **不检查**，越界静默读写堆外内存。
- 例：`std::vector<int> v{10,20,30}; v[3]`：没有 sanitizer 时读到垃圾；ASan 报 `heap-buffer-overflow`，`READ of size 4`，`0 bytes after 12-byte region`。
- 裸数组 `arr[4]`（4 个元素）同样没有检查。
- 实践：调试时用 `.at()`，用 `vector`/`string`/`array` 与迭代器代替裸数组和指针算术。
