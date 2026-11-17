---
id: errors-boundary-check-order
node: errors.boundary-validation
type: qa
step: 8
---
## Q
一个请求里 `limit` 和 `user` 都非法；另一个请求里 `user` 合法但不存在。服务按什么顺序检查、各返回什么？顺序为什么要固定并写进测试？

## A
**顺序固定：形状、类型、范围，最后才查存在**

- **格式先于存在**：校验失败（400）不依赖任何存储，排在查找（404）之前；否则同一个坏输入因为查不到先报 404，调用方改完又收到 400；
- **字段之间**：多个字段都错时，按合同写明的顺序报第一个，代码里就是上下排列的 `if`；
- **格式先于冲突**：409 要读状态，必然在 400 之后；
- **测试**：造“两个字段都错”的输入，断言报的是排在前面的；否则调换两行代码，没有一个测试会变红。

```python
class ServiceError(Exception): ...

USERS = {"bob"}

def recommend(user, limit):
    if type(limit) is not int or not 1 <= limit <= 50:
        raise ServiceError(400, "invalid_limit")        # 合同：limit 在前
    if not isinstance(user, str) or not user.strip():
        raise ServiceError(400, "invalid_user")
    if user not in USERS:
        raise ServiceError(404, "user_not_found")       # 查存在放最后
    return []

try: recommend("", 0)
except ServiceError as e: print(e.args)                 # (400, 'invalid_limit')
```

**知识点：**边界校验（Validate at the Boundary）
