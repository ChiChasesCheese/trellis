---
id: hl-c02-ref-pointer-pitfalls
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 12
---
## Q
C++ 引用和指针有哪五个常见的坑？

## A
1. **返回局部变量的引用或指针** = 悬空，函数返回后对象已销毁。
2. **`const_cast` 去掉 const 再写入原本就是 const 的对象** = 未定义行为（UB）。
3. **引用成员**使类不可赋值（引用不能换绑）。
4. **指针算术越界**不会报错，访问越界内存是未定义行为。
5. **指向 `vector` 元素的引用/指针**，在 `vector` 扩容重新分配内存后会**失效**。
