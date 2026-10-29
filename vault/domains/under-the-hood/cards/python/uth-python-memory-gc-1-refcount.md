---
id: uth-python-memory-gc-1-refcount
node: python.memory-gc
type: qa
step: 1
---
## Q
**对象什么时候被释放**｜Python · CPython 3.14

Python 怎么知道一个对象没人用了？`del x` 真的释放对象吗？

## A
**结构。** 每个对象头里有一个引用计数（reference count），多一个引用加 1，少一个减 1，归零立刻释放。

**细节。**

- `a = []` 后 `sys.getrefcount(a)` 是 2（变量加函数参数）；`b = a` 变 3；`del b` 回到 2。
- `del x` 只删掉名字，减一次计数；还有别的引用，对象就还在。
- 释放是确定性的，不用等扫描，`__del__` 也立刻执行。

**为什么。** 释放时机可预测、没有 GC 暂停；代价是每次赋值都要改计数，而且处理不了循环引用。

**对应 LeetCode：** LC 138 复制带随机指针的链表 · LC 133 克隆图
