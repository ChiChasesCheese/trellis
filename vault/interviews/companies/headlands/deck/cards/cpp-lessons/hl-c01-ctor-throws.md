---
id: hl-c01-ctor-throws
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 11
---
## Q
C++ 类的构造函数体抛异常时，哪些析构函数会运行？这对资源管理有什么启示？

## A
- **已经构造好的成员子对象会被析构**（按相反顺序），但**类自己的析构函数不会运行**，因为这个对象从未"完整存在"。
- 例：成员 `Part a`、`Part b` 构造完，构造函数体 `throw`，输出依次是 `Part b destroyed`、`Part a destroyed`，不会出现 `~Machine runs`。
- 启示：资源要放进**成员对象**里（每个成员自己是 RAII），不要在构造函数里裸 `new` 后存进裸指针成员——这种情况下裸指针指向的内存会**泄漏**，因为没有任何析构函数替它释放。
