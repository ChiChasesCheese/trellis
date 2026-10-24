---
id: pl-foundations-language-vs-implementation-found-refcount
node: foundations.language-vs-implementation
type: qa
step: 2
---
## Q
CPython 的引用计数（reference counting）是什么？一个对象什么时候被销毁？

## A
CPython 给每个对象附带一个整数：有多少个引用正指向它。变量赋值、放进列表、作为参数传入都会让计数加一；变量被重新赋值、离开作用域、被 `del` 则减一。计数降到 0 的那一刻，对象立刻被销毁，内存立刻回收，`__del__` 方法立刻被调用，不需要等待某个垃圾回收周期。

```python
import sys
x = []
print(sys.getrefcount(x))   # 2：变量 x，加上传给函数的临时引用
y = x
print(sys.getrefcount(x))   # 3
del y
print(sys.getrefcount(x))   # 2
```

实际输出 `2`、`3`、`2`（`getrefcount` 本身的参数多算一个引用）。

引用计数简单、可预测，对象用完即释放，内存占用平稳。它的两个弱点是：每次引用变化都要改计数，这是 Python 对象赋值有成本的原因之一，也是全局解释器锁（GIL）存在的原因，因为多线程同时修改计数会出错；另一个是循环引用（A 引用 B，B 引用 A）计数永远不为零，所以 CPython 另外带了一个周期性运行的循环垃圾检测器。这套机制是 CPython 的实现方式，不是 Python 语言规范的要求。
