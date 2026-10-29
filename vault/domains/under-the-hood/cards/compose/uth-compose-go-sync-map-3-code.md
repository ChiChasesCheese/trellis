---
id: uth-compose-go-sync-map-3-code
node: compose.go-sync-map
type: qa
step: 3
---
## Q
**不变量与核心代码**｜Go · sync.Map 旧实现（1.25 及以前）

两张表之间要保持什么关系？什么时候把 `dirty` 提升成 `read`？

## A
**不变量。**

- `read` 的表一旦发布就不再增删 key，只允许原子地换 `entry` 里的值，所以读者不用锁
- `dirty` 非空时，含 `read` 的全部有效项外加新 key，这样提升时整张直接换上去
- 提升后 `dirty` 置空，下一次写新 key 才再复制一份
- 提升时机是 `misses` 达到 `len(dirty)`：未命中累计付出的加锁代价，已经抵得上一次复制

**细节。** "先攒着，攒够代价再整体搬过去"是摊还（把偶尔的大代价分摊到每次操作）的常见做法，LC 232 用两个栈实现队列是同一个套路。

```python
import threading


class SyncMap:
    def __init__(self) -> None:
        self.mu = threading.Lock()
        self.read: dict[str, list] = {}               # 只读表：发布后不增删 key，值装在 [v] 盒子里
        self.dirty: dict[str, list] | None = None     # 脏表：持锁才碰；非空表示有 read 里没有的 key
        self.misses = 0                               # 读不到 read、去锁里查 dirty 的次数

    def load(self, key: str) -> object | None:
        box = self.read.get(key)                      # 快路径：不加锁
        if box is None and self.dirty is not None:
            with self.mu:
                box = self.read.get(key)              # 加锁后再看一眼：可能刚被别人提升
                if box is None and self.dirty is not None:
                    box = self.dirty.get(key)
                    self.misses += 1
                    if self.misses >= len(self.dirty):    # 加锁代价攒够一次复制：提升
                        self.read, self.dirty, self.misses = self.dirty, None, 0
        return box[0] if box else None

    def store(self, key: str, value: object) -> None:
        box = self.read.get(key)
        if box is not None:                           # 已有 key：原地换值，不动表结构
            box[0] = value
            return
        with self.mu:
            box = self.read.get(key) or (self.dirty or {}).get(key)
            if box is None:
                if self.dirty is None:                # 第一个新 key：整张复制 read，O(N)
                    self.dirty = dict(self.read)
                box = self.dirty[key] = [None]
            box[0] = value
```

例：`store("a", 1)` 后 `dirty = {a}`；第一次 `load("a")` 在 `read` 里没有，加锁查 `dirty`，`misses = 1 ≥ 1`，提升；之后 `load("a")` 全走无锁的快路径。

**例题：** LC 232 用栈实现队列

只用两个栈实现先进先出队列：`push(x)` 放到队尾，`pop()` 移除并返回队首，`peek()` 返回队首，`empty()` 判断是否为空。进阶：每个操作均摊 O(1)。例：`push(1)`、`push(2)`、`peek()` → `1`，`pop()` → `1`，`empty()` → `False`。

```python
class MyQueue:
    def __init__(self) -> None:
        self.inbox: list[int] = []        # 只负责 push：新元素压在栈顶
        self.outbox: list[int] = []       # 只负责 pop / peek：栈顶就是队首

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _move(self) -> None:
        if not self.outbox:               # 只有 outbox 空了才倒，倒的时候整个 inbox 一次倒完
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._move()
        return self.outbox.pop()

    def peek(self) -> int:
        self._move()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
```
