---
id: fsm-flags-to-states-derive
node: fsm.flags-to-states
type: qa
step: 2
---
## Q
审核服务返回用户的违规数和 `flagged`（被封禁）。`flagged` 要不要单独存一个字段？

## A
**能从已有数据算出来的，现算，不另存**

- **第二份状态会对不上**：计数改了、标志忘了改，或者反过来；需要同步的代码到处都是；
- **现算**：`flagged = strikes >= 3`，只有一个事实来源（计数），没有第二个字段可以和它不一致；
- **规则变了也只改一处**：门槛从 3 改成 5，改一个常量；
- **例外**：计算很贵且读很多、或者标志代表一个不可由数据推出的人工决定（解封与否），才需要存；存了就要有对账；
- **表单的 `valid`、`can_submit` 同理**：由值推出，不缓存。

```python
BLOCK_AT = 3

class StrikeBook:
    def __init__(self): self.count = {}
    def reject(self, user): self.count[user] = self.count.get(user, 0) + 1
    def state(self, user):
        n = self.count.get(user, 0)
        return {"strikes": n, "flagged": n >= BLOCK_AT}          # 现算

b = StrikeBook()
for _ in range(3): b.reject("mia")
print(b.state("mia"), b.state("nobody"))
# {'strikes': 3, 'flagged': True} {'strikes': 0, 'flagged': False}
```

**知识点：**把标志位改成状态（Flags to States）
