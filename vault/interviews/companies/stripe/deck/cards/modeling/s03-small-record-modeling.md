---
id: s03-small-record-modeling
node: stripe.modeling
type: qa
---

## Q
"proper data structures" 这句评分标准具体考什么？什么时候用 `dict`、什么时候用 `@dataclass`、什么时候要写一个真正的类？

## A
**为什么考**：这是"proper data structures"那一句的直接考点。

**标准做法**：

```python
from dataclasses import dataclass, field

@dataclass
class Account:
    total: int = 0
    fraud: int = 0
    mcc: str | None = None

accounts: dict[str, Account] = defaultdict(Account)   # key = account_id
```

**什么时候用 `dict`，什么时候用 `@dataclass`，什么时候用真正的类：**

| 情况 | 用什么 |
|---|---|
| 3 个以下字段，只读不改 | `tuple` 或 `dict` |
| 4+ 个字段，要按名字取 | `@dataclass`（自带 `__repr__`，调试时是救命的） |
| 有不变量要维护（余额不能为负、状态机） | 真正的类，把校验放进方法里 |
| 只是"每个 id 一个计数器" | `defaultdict(int)`，别过度建模 |

**信号：当你有 3 个以上并行的 `dict[str, X]` 用同一个 key 时，它们应该是一个记录。**

**典型翻车**：`defaultdict` 的隐式建键 —— `if accounts[x].total > 0:` 这一句会**创建** `x`，
于是"从未出现过的账户"也进了输出。查询用 `.get()`，只有写入才用 `[]`。
