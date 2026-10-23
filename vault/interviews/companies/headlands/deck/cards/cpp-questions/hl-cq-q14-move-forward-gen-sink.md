---
id: hl-cq-q14-move-forward-gen-sink
node: cpp-questions.c-memory-ownership
type: qa
step: 24
---
## Q
三个追问：`std::move` 和 `std::forward` 的区别？编译器什么时候会自动生成移动构造函数？接收参数后要存起来，该按值传还是传 `const T&`？

## A
- **`move` vs `forward`**：`move` 总是转成右值；`forward<T>` 只在原参数是右值时才转成右值。
- **自动生成移动构造**：只有在你自己没声明任何拷贝操作或析构函数时才会生成。
- **参数要存起来（sink 参数）**：按值接收，再 `std::move` 进成员；只读使用则用 `const T&`。
