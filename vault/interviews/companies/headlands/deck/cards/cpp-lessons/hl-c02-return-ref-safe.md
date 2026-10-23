---
id: hl-c02-return-ref-safe
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 13
---
## Q
面试问：C++ 函数返回引用安全吗？
Interview question: Is it safe to return a reference from a function?

## A
- 只有被引用的对象在函数**返回后仍然存在**才安全：类成员、静态变量、传入的参数引用。
- **局部变量**不行：返回后已销毁，引用悬空。
- 同理适用于返回指针和 `string_view`。
- 例：`const std::string& name() const { return name_; }` 安全（成员比调用者活得久，只要对象本身还在）。
