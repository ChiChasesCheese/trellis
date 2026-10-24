---
id: pl-conc-gil-found-refcount
node: concurrency.gil
type: qa
step: 2
---
## Q
CPython 的引用计数（reference counting）是什么？一个对象的计数怎么变化，循环引用为什么需要额外的垃圾回收器？

## A
CPython 管理内存的主要办法：**每个对象头里有一个整数计数器，记录“有多少个引用指向我”**。
- 新增一个引用（赋值给变量、放进列表/字典、作为参数传入）→ 计数 +1；
- 引用消失（变量被重新赋值、`del`、离开作用域、容器被销毁）→ 计数 −1；
- 计数降到 0 → **立即**释放这个对象（并递归减少它引用的对象的计数）。

可以用 `sys.getrefcount` 观察（它自己作为参数会多算 1）：
```python
x = []
sys.getrefcount(x)   # 2   (variable x + the argument)
y = x
sys.getrefcount(x)   # 3
d = {"k": x}
sys.getrefcount(x)   # 4
del y, d
sys.getrefcount(x)   # 2
```
实际输出依次为 `2`、`3`、`4`、`2`。

**好处**：对象不再被用的瞬间就被回收，内存占用平稳、可预测；析构（`__del__`、`with` 之外的资源释放）时机确定。**代价**：
1. 每次赋值、传参都要读写计数器，慢；
2. 多线程同时改同一个计数器会出错（读-改-写不是原子的），这正是需要 GIL 的原因；
3. **循环引用**：A 引用 B，B 又引用 A，即使外部再没人引用，两者的计数都是 1，永远不会降到 0。
```python
a, b = Node(), Node()
a.other, b.other = b, a    # cycle
del a, b                   # counts drop to 1, nothing is freed
gc.collect()               # the cycle detector finds them: 2 unreachable objects
```
为此 CPython 另有一个**循环垃圾回收器**（`gc` 模块），定期从根对象出发做可达性分析，回收不可达的环。执行 `gc.collect()` 返回找到的不可达对象数，这里是 `2`，随后两个对象的析构函数才被调用。

Java 和 Go 用追踪式 GC（从根出发找可达对象），没有计数器，也就没有这个问题和这个需要全局锁的理由。
