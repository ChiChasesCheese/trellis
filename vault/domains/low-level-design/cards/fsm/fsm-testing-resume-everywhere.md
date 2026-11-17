---
id: fsm-testing-resume-everywhere
node: fsm.testing
type: qa
step: 3
---
## Q
有“快照与恢复”功能的状态机，怎么证明恢复后和不中断时一样，而不是只测几个例子？

## A
**随机输入，在每个切点都做一次快照恢复**

- **性质**：对任意输入序列、任意切点，“前半段、快照、恢复、后半段”的输出等于“不中断”的输出；
- **做法**：生成很多随机序列，对每个位置各切一次，逐个比较；固定种子，失败可复现；
- **能抓到什么**：快照漏掉的字段（如没确认的进度），只有在恰好切在那里时才暴露；
- **参照要独立**：不中断的那一遍不经过快照代码。

```python
import random

class P:
    def __init__(self, n=0): self.n = n
    def feed(self, hit):
        self.n = self.n + 1 if hit else 0; return self.n == 3

def run(xs, cut=None):
    p, out = P(), []
    for i, x in enumerate(xs):
        if i == cut: p = P(p.n)                       # 快照再恢复
        out.append(p.feed(x))
    return out

rng = random.Random(7)
for _ in range(200):
    xs = [rng.random() < 0.7 for _ in range(12)]
    assert all(run(xs, c) == run(xs) for c in range(len(xs)))
```

**知识点：**状态机的穷尽测试（Exhaustive Testing）
