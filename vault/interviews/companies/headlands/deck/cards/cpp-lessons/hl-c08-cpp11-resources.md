---
id: hl-c08-cpp11-resources
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 3
---
## Q
C++11 在资源管理和库上加了什么？为什么说智能指针是 C++11 最重要的变化之一？

## A
- **移动语义 / 右值引用**：避免深拷贝，值语义变快（`vector` 返回、扩容）。
- **智能指针** `unique_ptr`/`shared_ptr`/`weak_ptr`：用 RAII 取代手工 `new`/`delete`；`auto_ptr` 废弃（它的「拷贝即转移」语义有 bug）。
- 标准库补全：`unordered_map/set`、`array`、`tuple`（含 `std::tie`）、`chrono`、`regex`。
- 说「C++11 加了智能指针」不够，要说出**为什么**：RAII 取代 `new/delete`。
- 本质变化：资源由类型管理，值语义有了移动，不再手写 `new`/`delete`，并发有了标准内存模型。
