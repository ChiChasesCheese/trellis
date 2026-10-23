---
id: hl-c03-unique-ptr-ownership
node: cpp-lessons.c03-smart-pointers
type: qa
step: 3
---
## Q
`unique_ptr` 作为函数返回值、按值参数、`const T&` 参数各表示什么？`auto b = a;` 为什么编译不过？`std::move(a)` 之后 `a` 是什么状态？

## A
- 函数**返回** `unique_ptr`：把所有权交给调用者（`std::make_unique<Order>(id)`，一个表达式，异常安全）。
- 函数**按值接收** `unique_ptr`：取得所有权，调用者要写 `std::move`，函数结束时对象销毁。
- **只想用一下**：传 `const T&`（不能为空）或 `const T*`（可为空），不要传 `unique_ptr`；`get()` 取出裸指针，所有权仍在智能指针手里。
- `auto b = a;` 不能编译：拷贝会产生两个拥有者，拷贝构造被删除，错误在编译期暴露。
- `auto b = std::move(a);` 之后所有权转移，`a` 为**空**（`nullptr`），`b` 持有对象。
