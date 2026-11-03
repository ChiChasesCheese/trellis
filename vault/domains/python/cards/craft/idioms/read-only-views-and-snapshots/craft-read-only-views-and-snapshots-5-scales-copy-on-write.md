---
id: craft-read-only-views-and-snapshots-5-scales-copy-on-write
node: craft.idioms.read-only-views-and-snapshots
type: qa
step: 5
---
## Q
**只读视图与快照 · 从 tuple 快照到 MVCC 与只读副本**｜写法

每次读都拷贝 tuple 是 O(n)。读频率高到值得优化时怎么办？放大到数据库和服务，同样的「读者看到一致的旧版本」是怎么实现的？

## A
**要点。** 把拷贝从读路径挪到写路径：写者造一份新的不可变版本，再用一次引用替换发布（写时复制，copy-on-write）；读者读一次引用，之后遍历的是不会再变的旧版本，不加锁、不拷贝。

```python
class Logger:
    """读多写少：handlers 用 tuple 整体替换，读路径不加锁。"""
    def __init__(self) -> None:
        self._handlers: tuple[str, ...] = ()
        self._lock = threading.Lock()

    def add_handler(self, h: str) -> None:
        with self._lock:                        # 写者之间互斥
            self._handlers = self._handlers + (h,)   # 造新元组再换引用，旧元组不动

    def emit(self, msg: str) -> list[str]:
        hs = self._handlers                     # 读一次引用，之后遍历的是不可变快照
        out = []
        for h in hs:
            out.append(f"{h}:{msg}")
            if h == "a":
                self.add_handler("late")        # 遍历途中有人注册了新 handler
        return out

lg = Logger()
lg.add_handler("a"); lg.add_handler("b")
print("本次投递:", lg.emit("x"))               # 不受遍历中途的注册影响，也不报错
print("下一次投递:", lg.emit("y"))             # 新 handler 从下一次起生效
```

实际输出：

```
本次投递: ['a:x', 'b:x']
下一次投递: ['a:y', 'b:y', 'late:y']
```

**变化。** 三级用的是同一个思想，只是版本的粒度不同：进程内是一个 tuple 引用换成另一个；数据库是 MVCC（多版本并发控制，每个事务读自己开始时刻的版本，写者生成新版本，互不阻塞）；服务层是只读副本与物化视图（materialized view），对外只暴露只读 API，不暴露内部存储的可变引用。读者看到的可能是稍旧的版本，这是换来无锁的代价。

**代价。** 写时复制让写者每次付 O(n)：写多读少时反过来更差，这时应该读时拷贝，或者换成持久化数据结构（persistent data structure，更新时只新建变化的路径，其余结构共享）。元素很少时，这点拷贝根本不值得优化，别为它加复杂度。

**信号。** 读路径极热、写路径极冷，而且读者允许看到稍旧的一致版本。
