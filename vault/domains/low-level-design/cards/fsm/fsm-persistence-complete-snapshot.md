---
id: fsm-persistence-complete-snapshot
node: fsm.persistence
type: qa
step: 2
---
## Q
一个流处理器要“连续三次命中才确认”。快照里只存“已确认的帧”，从快照恢复后输出会和不中断时一样吗？快照里该放什么？

## A
**快照要带全部推导所需，恢复后与不中断一致**

- **没确认的进度也是状态**：命中了两次、还差一次，这个“2”不在快照里，恢复后要重新数三次，确认事件就晚了；
- **检验标准**：在任意位置中断、恢复、继续，输出必须和不中断相同；
- **快照必须是副本**：返回内部列表，恢复前被改动，快照就变了；
- **加载时校验**：版本号、字段完整、数值范围（次数在 1 到 N 之间）；不合法就拒绝，不猜；
- **恢复本身不产生事件**：已发过的不再发。

```python
class Counter:
    def __init__(self, n=0): self.n = n
    def feed(self, hit):
        self.n = self.n + 1 if hit else 0
        return self.n == 3                           # 第 3 次连续命中才确认

def run(hits, cut, lossy):
    c, out = Counter(), []
    for i, h in enumerate(hits):
        if i == cut: c = Counter(0 if lossy else c.n)     # 快照 → 恢复
        out.append(c.feed(h))
    return out

hits = [True] * 4
print(run(hits, None, False), run(hits, 2, False), run(hits, 2, True))
# 不中断 / 完整快照 / 丢了进度的快照
```

**知识点：**持久化与恢复（Persistence & Resume）
