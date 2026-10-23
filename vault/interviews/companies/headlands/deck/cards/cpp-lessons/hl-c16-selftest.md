---
id: hl-c16-selftest
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 19
---
## Q
自测：为什么 `std::sort(l.begin(), l.end())` 对 `std::list` 编译失败？自己写的 `CHECK` 宏相对 `assert` 的安全点是什么？

## A
- `std::sort` 需要**随机访问迭代器**；`list` 只有双向迭代器，应使用 `l.sort()`。
- `NDEBUG` 下 `assert` 被移除，测试变成空操作；`CHECK` 总是执行。
