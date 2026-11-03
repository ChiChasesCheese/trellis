---
id: craft-notify-outside-the-lock-4-stale-event
node: craft.patterns.notify-outside-the-lock
type: qa
step: 4
---
## Q
**锁内记事件、锁外派发 · 事件到达顺序和产生顺序不一致怎么办**｜模式

两个线程各自在锁内产生了事件 1 和事件 2，出锁后各自派发。线程 1 在出锁后被调度走了一会儿，订阅者会先收到 2，再收到 1。订阅者拿 1 去覆盖自己的「当前状态」就错了。怎么处理？这是锁外派发的代价还是缺陷？

## A
**要点。** 这是锁外派发明确付出的代价，换来的是不会死锁、不会被慢订阅者卡住。两种做法：（1）事件带单调递增的序号（seq），订阅者丢弃比自己已见过更小的序号；（2）所有派发走单独一个队列、单个派发线程，顺序由队列决定。

```python
lock = threading.Lock()
seq = 0
seen: list[int] = []
latest = 0

def make_event() -> int:
    global seq
    with lock:
        seq += 1                 # 锁内产生，顺序确定
        return seq

def subscriber_naive(n: int) -> None:
    seen.append(n)

def subscriber_by_seq(n: int) -> None:
    global latest
    if n > latest:               # 迟到的旧事件直接丢弃
        latest = n
        seen.append(n)

def publisher(sub, delay: float) -> None:
    n = make_event()
    time.sleep(delay)                  # 锁外：被调度走了一会儿
    sub(n)

for sub in (subscriber_naive, subscriber_by_seq):
    seq, latest = 0, 0
    seen.clear()
    a = threading.Thread(target=publisher, args=(sub, 0.05))
    a.start(); time.sleep(0.01)
    b = threading.Thread(target=publisher, args=(sub, 0.0))
    b.start(); a.join(); b.join()
    print(sub.__name__, "订阅者看到的顺序", seen)
```

线程 1 在锁外睡 50 毫秒，线程 2 不睡，实际输出：

```
subscriber_naive 订阅者看到的顺序 [2, 1]
subscriber_by_seq 订阅者看到的顺序 [2]
```

**为什么。** 事件必须是事实快照，而不是「对象的引用」：订阅者收到事件时对象早已变了，读引用就读到了新状态。序号让订阅者能识别过期。

**代价。** 方案（1）订阅者要自己维护位点；方案（2）派发有延迟并要处理队列满。需要「严格按序、不丢」时，用队列加专用线程，或下一张卡的发件箱。
