---
id: hl-c10-malloc-vs-new
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 1
---
## Q
面试问：`malloc`/`free` 和 `new`/`delete` 有什么区别？
Interview question: What is the difference between `malloc` and `new`?

## A
核心一句：**`new` = 分配 + 构造，`delete` = 析构 + 释放；`malloc` 只管字节。**
- `malloc` 只分配**未初始化的字节**，`free` 只还内存，**不调析构**；返回 `void*` 要强转，大小自己算字节数。
- `new` 先 `operator new` 分配，再**调构造函数**；`delete` 先调**析构函数**再还内存；返回带类型指针，大小按类型算。
- 失败：`malloc` 返回 `NULL`，必须检查；`new` 抛 `std::bad_alloc`（`new(std::nothrow)` 返回 `nullptr`）。
- `operator new` 可全局或按类替换，`malloc` 不可重载。
- 对 `std::string` 这类非平凡类型，在 `malloc` 出来的内存上直接用是 **UB**（没有对象）。
