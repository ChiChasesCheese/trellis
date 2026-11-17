---
id: errors-retry-failure-leaves-no-trace
node: errors.retry
type: qa
step: 5
---
## Q
重置密码时，写入新密码失败了，一次性重置码还应该有效吗？如果先清除重置码、再写密码，会出什么问题？

## A
**成功以后才消耗凭据，失败要原样留着**

- **错误的顺序**：先清码再写库，写库失败时码没了、密码也没改，用户只能重新申请，重试无路可走；
- **正确的顺序**：先存密码，成功以后再清码，最后才返回 `True`；
- **失败不留痕**：码仍然有效，重试看到的世界和第一次一样，这是“可以重试”的前提；
- **同样的道理**：限流器里被拒绝的请求不写时间戳，否则越频繁地重试，恢复得越晚；
- **更稳的做法**：存密码和清码放进同一个事务，不靠顺序。

```python
class Resets:
    def __init__(self):
        self.pw, self.codes = {}, {"u1": "123"}
    def reset(self, user: str, code: str, new_pw: str, db_ok: bool = True) -> bool:
        if self.codes.get(user) != code:
            return False
        if not db_ok:
            raise OSError("db down")        # 写库失败：码还在
        self.pw[user] = new_pw              # 1 先存密码
        del self.codes[user]                # 2 再清码
        return True
r = Resets()
try: r.reset("u1", "123", "x", db_ok=False)
except OSError: print("失败后码还在：", dict(r.codes))
print(r.reset("u1", "123", "x"), r.pw)      # True {'u1': 'x'}
```

**知识点：**重试与退避（Retry & Backoff）
