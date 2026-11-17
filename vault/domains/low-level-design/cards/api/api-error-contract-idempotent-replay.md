---
id: api-error-contract-idempotent-replay
node: api.error-contract
type: qa
step: 6
---
## Q
创建工单的接口带一个幂等键。同一个键第二次到达，请求内容相同和内容不同，各应该返回什么？为什么“内容不同”不能悄悄当成重放？

## A
**同键同内容回放原结果，同键异内容报冲突**

- **同键同内容**：返回第一次的结果，不再执行；调用方超时重试，看到的和没超时一样；
- **同键异内容**：409，`code` 单独一个，如 `idempotency_conflict`；它说明调用方复用了键，是调用方的 bug，该暴露；
- **比较什么**：规范化以后的请求（去掉无关空白、字段顺序），不是原始字节；
- **范围写清楚**：键的作用域是（用户，项目，键），别人的同名键不能碰到你的记录；
- **失败的结果也缓存**：如果第一次是 400，重放仍是同一个 400，否则同一个键两次的行为不一致。

```python
import json

seen: dict[tuple, tuple[str, dict]] = {}

def create(user: str, key: str, body: dict) -> tuple[int, dict]:
    fingerprint = json.dumps(body, sort_keys=True)
    prev = seen.get((user, key))
    if prev is None:
        seen[(user, key)] = (fingerprint, {"id": len(seen) + 1})
        return 201, seen[(user, key)][1]
    if prev[0] != fingerprint:
        return 409, {"error": "idempotency_conflict"}
    return 200, prev[1]                            # 回放：同一个结果

print(create("u", "k1", {"t": "a"}), create("u", "k1", {"t": "a"}), create("u", "k1", {"t": "b"}))
```

<details class="pt"><summary>延伸</summary>

键不能永久保留，保留期必须比客户端的重试窗口长。键过期以后同一个请求会被当成新请求，如果客户端的重试窗口比保留期长，就会重复创建；这条要写进合同，并让过期的键被明确拒绝。

</details>

**知识点：**接口的错误契约（Error Contract）
