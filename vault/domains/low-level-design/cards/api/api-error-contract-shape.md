---
id: api-error-contract-shape
node: api.error-contract
type: qa
step: 1
---
## Q
一个服务有十几种失败，每种都自己拼一个错误响应：有的返回 `{"msg": "..."}`，有的返回 `{"error": "..."}`，有的直接返回字符串。调用方写重试和提示逻辑时会碰到什么？错误响应应该有什么形状，哪一部分才算承诺？

## A
**错误只有一种形状：状态码加稳定的机器码**

- **一个出口**：服务内部只抛一种带 `status` 和 `code` 的异常，只有适配层一处把它变成响应；
- **`code` 是承诺**：`invalid_limit`、`list_not_found` 这类短标识，改名等于破坏性变更，调用方的 `if code == ...` 依赖它；
- **`message` 不是承诺**：给人看的文字，措辞随时可改；调用方不许解析它；
- **形状固定**：连 405、坏 JSON、路径不存在这些“框架层”的失败也走同一个形状，否则调用方要写两套解析；
- **好认**：错误响应只有 `error` 一个键，调用方靠“有没有 `error` 键”就能分辨成败。

```python
class ServiceError(Exception):
    def __init__(self, status: int, code: str, message: str = ""):
        super().__init__(code)
        self.status, self.code, self.message = status, code, message

def to_response(exc: ServiceError) -> tuple[int, dict]:
    return exc.status, {"error": exc.code}      # 唯一出口，message 只进日志

print(to_response(ServiceError(400, "invalid_limit", "limit must be 1..50")))
print(to_response(ServiceError(405, "method_not_allowed")))
```

<details class="pt"><summary>延伸</summary>

状态码只表示大类（400、404、409），同一个状态码下可能有很多种失败，所以调用方真正分支的依据是 `code`。要给人看细节，另加一个字段，但在合同里明说它不稳定。

</details>

**知识点：**接口的错误契约（Error Contract）
