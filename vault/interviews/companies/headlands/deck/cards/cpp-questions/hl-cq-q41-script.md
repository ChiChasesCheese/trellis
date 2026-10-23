---
id: hl-cq-q41-script
node: cpp-questions.j-cross-language
type: qa
step: 14
---
## Q
用英文 60 秒回答：Value semantics: what does `Order b = a;` do in C++? What is slicing? What's a dangling reference?

## A
结构：赋值是拷贝，别名要用引用 → 传参规则（`const T&`、`T&`、指针/`optional`）→ 切片（"animal" 对 "dog"），多态用指针/引用 → 悬空引用来源与编译器警告、ASan。

- In C++ `Order b = a;` makes a **copy**. In Java both names would refer to one object. To alias I use a **reference**, and vectors of objects deep-copy their elements.
- That drives parameter passing: by value copies, so for big read-only objects I take `const T&`; to modify, `T&`; for "may be absent", a pointer or `optional`.
- **Slicing**: assigning a derived object to a base-class variable copies only the base part and loses polymorphism - I showed `name()` returning "animal" through the copy and "dog" through a reference. So polymorphic objects are held by pointer or reference, typically `unique_ptr<Base>` in containers.
- **Dangling references** come from returning locals, invalidated vector iterators and views that outlive their owner; the compiler warns for the simple cases and ASan catches the rest.
