---
id: api-hard-to-misuse-secret-once
node: api.hard-to-misuse
type: qa
step: 6
---
## Q
短链接服务创建时返回一个删除令牌（token）。令牌应该出现在哪些响应里？服务端校验令牌时用 `==` 比较有什么问题，该用什么？

## A
**秘密只给一次，比较用恒定时间**

- **只在创建响应里出现一次**：元数据、统计、列表接口里都不含令牌；服务端存的也最好是哈希，不是明文；
- **接口上没有取回它的方法**：丢了只能重新创建，这样“令牌被泄漏”的面最小；
- **`==` 逐字节比较，遇到第一个不同就返回**：耗时随匹配的前缀长度变化，攻击者可以靠时间差一位一位猜（时序攻击，timing attack）；
- **用 `secrets.compare_digest(a, b)`**：恒定时间比较；两边要么都是 `bytes`，要么都是纯 ASCII 的 `str`，含非 ASCII 字符会抛 `TypeError`，所以先 `.encode()` 再比；
- **缺失或为空的令牌是 400**，令牌不对是 403，短码不存在是 404：三种情形三种码。

```python
import secrets

STORED = secrets.token_urlsafe(16)

def can_delete(given: str) -> bool:
    return secrets.compare_digest(given.encode(), STORED.encode())

print(can_delete(STORED), can_delete("wrong"), can_delete("令牌"))
```

**知识点：**难以用错的接口（Hard to Misuse）
