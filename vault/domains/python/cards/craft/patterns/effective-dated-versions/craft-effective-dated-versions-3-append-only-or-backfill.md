---
id: craft-effective-dated-versions-3-append-only-or-backfill
node: craft.patterns.effective-dated-versions
type: qa
step: 3
---
## Q
**生效时间版本 · 发布新版本时，允许补录一个更早生效的版本吗**｜架构

价格表发布接口有两种设计：只允许新版本的生效时间晚于现有所有版本（追加），或者允许按生效时间插入任意位置（补录）。各自的代价是什么？实际的账单系统里怎么选？

## A
**要点。** 追加：发布就是列表尾部加一项，已经出过账的时间段永远不会被改变；补录：可以修正历史，但补录之后同一个时刻查到的价格变了，**已经出过的账单就和价格表对不上了**。要补录，必须同时有「重新计价并产生调整行」的机制，否则历史被悄悄改写。

```python
from bisect import bisect_right, insort
from dataclasses import dataclass

@dataclass(frozen=True)
class V:
    start: int
    rate: int

class Strict:                                   # billing-tax-engine：只允许往后追加
    def __init__(self): self.v = []
    def publish(self, start, rate):
        if self.v and start <= self.v[-1].start:
            raise ValueError(f"生效时间必须晚于 {self.v[-1].start}")
        self.v.append(V(start, rate))

class Backfill:                                 # amz-aws-billing：按生效时间插入，允许补录
    def __init__(self): self.v = []
    def publish(self, start, rate):
        insort(self.v, V(start, rate), key=lambda x: x.start)
    def at(self, ts):
        i = bisect_right(self.v, ts, key=lambda x: x.start) - 1
        if i < 0: raise LookupError(ts)
        return self.v[i].rate

s = Strict(); s.publish(200, 250)
try: s.publish(100, 290)
except ValueError as e: print("Strict 拒绝补录:", e)

b = Backfill(); b.publish(200, 250)
print("补录前 ts=150:", end=" ")
try: b.at(150)
except LookupError: print("无价格")
b.publish(100, 290)
print("补录后 ts=150:", b.at(150), "<- 已经出过的账单被悄悄改变了")
```

在 200 秒生效的价格之上补录一个 100 秒生效的版本：

```
Strict 拒绝补录: 生效时间必须晚于 200
补录前 ts=150: 无价格
补录后 ts=150: 290 <- 已经出过的账单被悄悄改变了
```

**为什么。** 追加版本把「发布」变成纯粹的新增事实，旧账不受影响；真的发现错误时，用 `reprice(txn, previous, rules, version)`：用更正后的规则重算，**只追加调整行**，原来的行不改（与账本一样，纠错只靠追加）。补录版本适合内部报表这类「按当前最佳知识重算全部历史」的场景，不适合已经对外开过账单的系统。

**代价。** 追加版意味着「发错了生效时间」必须靠新版本来覆盖，不能撤销；补录版把一致性责任交给调用方。

**信号。** 需求里出现「已发布的账单不得变」「审计」「更正」：追加加调整行；「重新计算所有历史」「回溯定价」：补录。
