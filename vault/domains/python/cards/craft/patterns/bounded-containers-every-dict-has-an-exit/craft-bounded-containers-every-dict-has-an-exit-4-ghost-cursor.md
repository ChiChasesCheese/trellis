---
id: craft-bounded-containers-every-dict-has-an-exit-4-ghost-cursor
node: craft.patterns.bounded-containers-every-dict-has-an-exit
type: qa
step: 4
---
## Q
**有界容器 · 退订必须摘掉游标：幽灵订阅者怎样卡死整个发布端**｜架构

消息主题是一个有界日志：容量满了以后，发布者要等最慢的订阅者读过队头，才能丢掉队头（BLOCK 策略，一条不丢）。一个订阅者订阅过，之后进程崩了、再也没来读。发布端会怎样？`unregister` 里除了删游标，还必须做什么？

## A
**要点。** BLOCK 的放行条件是「最慢游标已越过队头」。游标表里留着一个再也不动的游标，最小游标就永远等于队头，日志永远满，发布者永远等。游标表是一个按订阅者 id 索引的字典，必须有出口：①显式退订时摘掉游标，**并唤醒**被它挡住的发布者（光删不唤醒，发布者仍睡在条件变量上）；②订阅者崩溃时没人调用退订，需要租约或心跳超时来回收。

```python
def can_append(self):
    if len(self.log) < self.cap: return True
    slowest = min(self.cursors.values(), default=self.start + len(self.log))
    return slowest > self.start                  # 队头被所有人读过才能淘汰

def unregister(self, sub_id):                    # 真实代码里：
    with self._not_full:
        self._cursors.pop(sub_id, None)
        self._not_full.notify_all()              # 叫醒被它挡住的发布者
```

```python
class Topic:
    """有界日志：只能丢掉所有游标都读过的队头；BLOCK 策略下队头被慢游标挡住时发布者要等。"""
    def __init__(self, cap):
        self.cap, self.log, self.start = cap, [], 0          # start = log[0] 的序号
        self.cursors = {}                                    # 订阅者 -> 下一条要读的序号
    def can_append(self):
        if len(self.log) < self.cap: return True
        slowest = min(self.cursors.values(), default=self.start + len(self.log))
        return slowest > self.start                          # 队头被所有人读过才能淘汰
    def append(self, m):
        assert self.can_append(), "BLOCK: 发布者要等"
        if len(self.log) >= self.cap: self.log.pop(0); self.start += 1
        self.log.append(m)
    def read(self, sub):
        i = self.cursors[sub]
        if i < self.start + len(self.log): self.cursors[sub] = i + 1; return self.log[i - self.start]

t = Topic(2)
t.cursors = {"alive": 0, "gone": 0}                  # gone 订阅过，但再也不会来读了
for m in "ab": t.append(m)
t.read("alive"); t.read("alive")
print("alive 读完了，还能发布吗:", t.can_append(), "<- 幽灵游标 gone 挡住了队头")
del t.cursors["gone"]                                # 退订必须摘掉游标（真实代码里还要 notify_all 叫醒发布者）
print("退订 gone 之后:", t.can_append())
```

订阅者 `alive` 读完了，`gone` 从没读过：

```
alive 读完了，还能发布吗: False <- 幽灵游标 gone 挡住了队头
退订 gone 之后: True
```

**为什么。** 这就是反压（backpressure）的代价：最慢的订阅者决定所有人的速度。三种溢出策略的差别正在于怎么处理这个代价：DROP_OLDEST 让发布者永不阻塞、慢订阅者丢消息；BLOCK 一条不丢、被慢者拖住；REJECT 让发布者立刻得到错误自己降级。选哪个是产品决定，但「游标有出口」对三者都成立，`cursor_count` 要在测试里断言退订后减一。

**代价。** 租约回收会误杀只是暂时慢的订阅者，所以回收之后它重新来读，要能发现自己已经掉队（`oldest_seq` 超过它的游标）并从保留窗口头部或最新位置重新开始。
