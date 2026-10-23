---
id: hl-c10-new-failure
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 4
---
## Q
面试问：C++ 的 `new` 内存不足时怎么办？`malloc` 呢？工业代码常怎么做？
Interview question: What happens when `new` fails?

## A
- `new` 抛 `std::bad_alloc`；`new (std::nothrow) T` 返回 `nullptr`，像 `malloc`。
- `malloc` 返回 `NULL`，**必须检查**。
- 可设置 `new_handler`。
- 实测请求约 8 EiB：`malloc` → `NULL`，`new char[...]` → 抛 `bad_alloc`，`nothrow` 版 → `nullptr`。
- 工业代码常在**启动时预分配**、运行期不分配，避免热路径上的失败与延迟。
