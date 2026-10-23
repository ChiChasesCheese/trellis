---
id: hl-c01-storage-duration
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 2
---
## Q
C++ 对象的三种存储期（storage duration）是什么？各自怎么得到、什么时候销毁？

## A
| 存储期 | 怎么得到 | 何时销毁 |
|---|---|---|
| 自动（automatic，俗称"栈"） | 局部变量 `Point p;` | 离开所在 `{}` 作用域，**立刻**、确定地销毁 |
| 动态（dynamic，俗称"堆"） | `new`、智能指针、`vector` 内部 | 你（或拥有它的对象）释放时 |
| 静态（static） | 全局变量、`static` 局部变量 | 程序结束 |

对比 Java：对象回收由 GC 决定，时间不确定；C++ 自动存储的销毁时刻由作用域决定，是确定的。「栈上」说的是对象本身所在的位置：`vector` 对象在栈上，它的元素在堆上。
