---
id: data-evolution-versioned-policy
node: data.evolution
type: qa
step: 2
---
## Q
风控规则每个月调整阈值。判定记录里只存了结果 `deny`，三个月后有人质疑一笔当时被拒的订单，怎么证明当时为什么拒绝？规则应该怎样存、怎样改？

## A
**规则是带版本号的不可变数据，判定记录存下它用的版本**

- **改规则就是发新版本**：`v7` 不会被原地改写，改阈值发 `v8`；旧版本一直保留，可以重放；
- **判定记录存四样**：输入、策略版本、各分项得分、最终决定；以后拿输入加版本重算，必须得到同一个结果；
- **引擎无状态**：规则和输入都从参数来，不读全局变量、不读“当前时间”（需要的时间由调用方传入）；
- **一次报价或判定用同一个版本**：开始时取版本号，整个过程都用它，中途有人发布新版本也不影响；
- **回滚也是新版本**：回到旧规则，发一个内容与 `v7` 相同的 `v9`，历史不被改写。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Policy:
    version: int
    deny_at: int

POLICIES = {7: Policy(7, 50), 8: Policy(8, 40)}           # 只增加，不修改

def decide(score: int, policy: Policy) -> dict:
    return {"score": score, "policy": policy.version,
            "decision": "deny" if score >= policy.deny_at else "allow"}

print(decide(45, POLICIES[7]), decide(45, POLICIES[8]))   # 当时的版本给出当时的结论
```

**知识点：**字段演进（Schema Evolution in Code）
