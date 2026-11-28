---
id: hi-c-lld-correctness-x01-lock-too-early
node: lld.concurrency.correctness.exam
type: qa
step: 1
---
## Q
**并发正确性 · 找出锁的错误**｜考点 · 必会

下面代码的 `book` 有什么问题？怎么改？
```python
def book(self, seat, who):
    with self._lock:
        free = seat not in self._owner
    if free:
        self._owner[seat] = who
        return True
    return False
```

## A
- **问题：** 锁在检查之后就释放，写入在锁外，别的线程可以在两步之间插入，双订回来
- **修法：** 把检查、写入、返回都放进同一个 `with` 块
- **类似错误：** 检查用 `lock1`、更新用 `lock2`，两把互不协调
- **规则：** 同一个不变量的所有操作用同一把锁
