---
id: hl-c11-trivially-copyable
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 4
---
## Q
面试问：什么是平凡可拷贝（trivially copyable）类型？为什么重要？怎么在编译期检查？
Interview question: What does trivially copyable mean and why does it matter?

## A
- 定义：一个类型的拷贝可以安全地用**字节拷贝**代替：没有虚函数、没有用户定义的拷贝/移动/析构、所有成员也如此。
- 实测：`int`、只含基本类型的 POD 结构体 → true；`std::string`、含 `string` 成员的结构体、有虚函数的类、用户写了拷贝的类 → **false**。
- 检查：`std::is_trivially_copyable_v<T>`，可配 `static_assert`。
- 重要性：`memcpy`、共享内存、网络序列化、`atomic<T>`、`bit_cast` 都要求它。
- `string` 不是平凡可拷贝，因为内部有指向自己缓冲区的指针/所有权。
