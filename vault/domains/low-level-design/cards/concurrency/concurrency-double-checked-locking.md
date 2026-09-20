---
id: concurrency-double-checked-locking
node: concurrency.patterns
type: qa
step: 6
---
## Q
Java 里的双重检查锁定（double-checked locking）要求把单例字段声明成一个特殊的可见性修饰符，否则可能读到"构造了一半"的对象。这个坑在 Python 里存在吗？

## A
不存在，原因是 GIL：一次属性赋值（`STORE_ATTR`/`STORE_NAME`）是单条字节码，而右边的构造调用在这条字节码执行之前已经完整跑完——不会出现"引用先被别的线程看到、对象内部字段还没填完"这种指令重排（instruction reordering）暴露给 Python 层的情况，所以 Java 那个修饰符想解决的那类可见性 bug 在 CPython 里本来就不发生。

真正需要防的是另一件事：两个线程都看到"还没初始化"从而都构造了一次（重复工作或重复副作用），修法是照样用锁做检查加构造：

```python
_instance = None
_lock = threading.Lock()

def get_instance():
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = Expensive()
    return _instance
```

但在 Python 里更地道的做法通常是绕开手写双重检查：模块级别的对象在 `import` 时只会被构建一次（导入系统自带锁，天然线程安全），或者用 `functools.cache` 包一个无参工厂函数——不过要注意它的并发语义是"缓存结构本身线程安全，但如果两个线程同时是第一次调用，被包装的函数仍可能并发执行两次"，如果构造函数有副作用（比如打开一次性资源），仍然需要额外加锁。
