---
id: review-risk-check-order
node: review.risk-patterns
type: qa
step: 3
---
## Q
预约服务的读取函数里，检查顺序是“不存在 → 已取消 → 不是本人的”。评审时你为什么要求把“是不是本人的”提到“已取消”之前？

## A
**先验权限，再看状态：别人的资源要和不存在的资源一模一样**

- **错误响应本身就是信息**：对陌生人返回“已取消”，等于告诉他“这个 id 存在，而且别人取消过”；
- **别人的预约和不存在的预约要返回同一个错误**（都是 404），否则可以靠枚举 id 探测别人有哪些预约；
- **顺序**：先判断存在且属于当前用户，不满足就一律 404；之后才轮到状态相关的错误（409 已取消）；
- **评审信号**：校验逻辑里“状态检查”出现在“所有权检查”之前，或所有权不合时返回了 403 而不是 404；
- **测试这条规则**：用另一个用户去读一个“已取消”的预约，期望和读一个不存在的 id 完全相同。

```python
class NotFound(Exception): ...
class Cancelled(Exception): ...
DB = {1: {"owner": "ann", "status": "cancelled"}}

def get(rid, user, owner_first):
    r = DB.get(rid)
    if r is None: raise NotFound
    if owner_first and r["owner"] != user: raise NotFound   # 别人的 = 不存在
    if r["status"] == "cancelled": raise Cancelled
    if r["owner"] != user: raise NotFound
    return r

for owner_first in (False, True):
    try: get(1, "bob", owner_first)
    except Exception as e: print(owner_first, type(e).__name__)   # False Cancelled / True NotFound
```

**知识点：**diff 里的高风险信号（Risk Patterns）
