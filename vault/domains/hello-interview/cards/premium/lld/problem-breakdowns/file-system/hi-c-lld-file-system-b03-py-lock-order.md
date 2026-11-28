---
id: hi-c-lld-file-system-b03-py-lock-order
node: lld.problem-breakdowns.file-system.beyond
type: qa
step: 4
---
## Q
**内存文件系统 · Python：加锁顺序要用不会变的键**｜拓展 · 加分

`move` 要同时锁两个文件夹。为什么用路径字符串排序不稳，该用什么？同一个文件夹在两端时怎么办？

## A
**模式。** 全序加锁：所有线程按同一个不可变的键顺序拿锁。

```python
import itertools
import threading
from contextlib import ExitStack

_ids = itertools.count()          # 每个文件夹创建时拿一个单调编号，终身不变


class Folder:
    def __init__(self) -> None:
        self.ident = next(_ids)
        self.lock = threading.Lock()
        self.files: set[str] = set()


def move(a: Folder, b: Folder, name: str) -> None:
    ordered = sorted({a, b}, key=lambda f: f.ident)   # 集合去重：同一个文件夹只锁一次
    with ExitStack() as st:
        for f in ordered:
            st.enter_context(f.lock)                   # 退出时按相反顺序自动释放
        a.files.discard(name)
        b.files.add(name)


x, y = Folder(), Folder()
x.files.add("p")
y.files.add("q")


def shuffle(src: Folder, dst: Folder, name: str) -> None:
    for _ in range(2000):
        move(src, dst, name)
        move(dst, src, name)


ts = [threading.Thread(target=shuffle, args=(x, y, "p")),
      threading.Thread(target=shuffle, args=(y, x, "q"))]
for t in ts:
    t.start()
for t in ts:
    t.join(timeout=20)
assert not any(t.is_alive() for t in ts)               # 两个方向相反的移动不会互相卡死
assert x.files | y.files == {"p", "q"}
```
- **为什么路径不稳：** 路径会随改名和移动变化；两个线程在不同时刻看到的"字母序"可能不同，顺序就不一致了。用创建时分配、永不改变的编号。
- **去重：** 源和目标是同一个文件夹时，`Lock` 不可重入，重复拿会自己卡死；`set` 去重解决。
- **`ExitStack`：** 数量不定的锁用它统一管理，异常时也会释放。
- **仍然没解决的：** 解析路径本身（找到那两个文件夹）也在读树；解析和加锁之间树可能被改，需要重新验证或在持锁后再解析。
- **何时不用：** 一把全局锁足够时，不要引入这套机制。
