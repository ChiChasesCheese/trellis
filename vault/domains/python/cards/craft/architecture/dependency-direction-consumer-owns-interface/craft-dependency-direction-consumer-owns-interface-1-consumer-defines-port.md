---
id: craft-dependency-direction-consumer-owns-interface-1-consumer-defines-port
node: craft.architecture.dependency-direction-consumer-owns-interface
type: qa
step: 1
---
## Q
**依赖方向 · 谁来定义「读磁盘」这个接口**｜架构

文件监听器要反复扫描目录、比对前后快照。直接在监听器里调 `os.scandir`，测试就得建临时目录、等文件时间戳变化。常见的补救是先写一个「磁盘类」再抽它的接口。接口应该从实现一侧抽出来，还是由监听器一侧来定义？各有什么后果？

## A
**要点。** 由使用方（consumer）定义接口，写成「我需要的最小能力」：监听器只需要「给我这个目录下所有文件的指纹」，所以接口只有一个方法 `scan`。真实磁盘和测试用的内存假实现都是适配器（adapter），去满足这个接口；依赖箭头从实现指向核心，核心不 import 任何基础设施。

```python
Snapshot = dict[str, tuple[int, int]]            # 路径 -> (mtime, size)

class FileSystem(Protocol):              # 监听器一侧定义：只要这一个能力
    def scan(self, root: str) -> Snapshot: ...

def diff(old: Snapshot, new: Snapshot) -> list[str]:
    return sorted([f"+{p}" for p in new.keys() - old.keys()]
                  + [f"-{p}" for p in old.keys() - new.keys()]
                  + [f"~{p}" for p in old.keys() & new.keys() if old[p] != new[p]])

class Watcher:
    def __init__(self, fs: FileSystem, root: str) -> None:
        self._fs, self._root = fs, root  # 不 import os，不碰真实磁盘
        self._last: Snapshot = fs.scan(root)

    def poll(self) -> list[str]:
        now = self._fs.scan(self._root)
        events, self._last = diff(self._last, now), now
        return events

class FakeFS:                            # 测试的适配器：一个字典就是整个磁盘
    def __init__(self) -> None:
        self.files: Snapshot = {"a.txt": (1, 10)}
    def scan(self, root: str) -> Snapshot:
        return dict(self.files)

fs = FakeFS()
w = Watcher(fs, "/data")
fs.files["b.txt"] = (2, 5)
fs.files["a.txt"] = (3, 12)
print(w.poll())
print(w.poll())
```

建好监听器后再加 `b.txt`、改 `a.txt`，连续轮询两次，实际输出：

```
['+b.txt', '~a.txt']
[]
```

**为什么。** 从实现一侧抽接口，往往会把磁盘类的全部方法原样搬过来，接口变大，使用方被迫依赖用不到的东西；使用方定义则天然最小。`Protocol` 是结构化类型（structural typing），适配器不需要继承它。

**代价。** 接口只有一个实现、一个假实现时，抽象本身就是成本；它在「测试需要替身」或「确实有多种实现」时才赚回来。
