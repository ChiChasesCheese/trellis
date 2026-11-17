---
id: api-returns-fixed-shape
node: api.returns
type: qa
step: 5
---
## Q
风险评分接口：通过时返回 `{"score": 12, "decision": "allow", "components": {...}}`，被拒绝时只返回 `{"decision": "deny"}`。调用方的代码会在哪里出问题？返回值的形状应该由什么决定？

## A
**每个分支返回同一种形状，字段恒定**

- **字段由合同定，不由分支定**：被拒的请求同样有 `score` 和 `components`，调用方才能记录和展示“为什么被拒”；
- **缺键是隐性的分支**：`result["score"]` 在拒绝路径上 `KeyError`，只有测试到那条路径才发现；
- **恰好这些键**：测试断言键集合相等，而不是“包含”，才能发现不小心多出来的内部字段（泄漏）；
- **类型也恒定**：`remaining` 永远是 `int`，不要有时是 `int`、有时是 `"unlimited"`；真正的布尔就是 `True`/`False`，不是 `0/1`；
- **内部对象不外泄**：在出口把冻结的内部记录转成新字典，别把内部结构直接交出去。

```python
from dataclasses import dataclass
@dataclass(frozen=True)
class Verdict:
    decision: str
    score: int
    components: tuple[tuple[str, int], ...]

def score(amount: int) -> dict:
    parts = (("amount", min(amount // 100, 60)),)
    total = sum(p for _, p in parts)
    v = Verdict("deny" if total >= 50 else "allow", total, parts)
    return {"decision": v.decision, "score": v.score, "components": dict(v.components)}

assert score(9000).keys() == score(100).keys()     # 键集合相等
```

**知识点：**返回值设计（Return Values）
