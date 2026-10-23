---
id: hl-c10-placement-new
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 6
---
## Q
面试问：placement new 是什么？什么时候用？使用时要注意什么？
Interview question: What is placement new and when do you use it?

## A
- `new (地址) T(args)`：在你给的内存上构造对象，**不分配**。
- 对应地要**手动析构**：`p->~T()`（或 C++20 `std::destroy_at`），内存本身由你另行管理。
- 用途：`vector` 预留容量里在尾部构造元素；`optional`/`variant` 的内部存储；对象池；共享内存里构造对象。
- 注意：
  1. 存储必须**对齐**：`alignas(T) unsigned char buf[sizeof(T)]`。
  2. 读取用 `std::launder`，或保存 `new` 返回的指针。
  3. `std::construct_at` / `std::destroy_at` 是 C++20 的无裸语法版本。
