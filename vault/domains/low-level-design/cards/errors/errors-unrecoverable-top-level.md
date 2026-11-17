---
id: errors-unrecoverable-top-level
node: errors.unrecoverable
type: qa
step: 2
---
## Q
请求处理的最外层该怎么处理没人接的异常？日志里记什么，对外返回什么？

## A
**对内记全，对外只给请求号**

- **预期失败先接**：`ServiceError` 这类按合同回响应（4xx 或 503），不进缺陷流程；
- **其余 `Exception` 是缺陷**：记完整的栈（`logging.exception`）、请求号、请求的关键标识，然后回 500；
- **对外不泄露内部**：不返回栈、SQL、路径，只给一个请求号，用户报问题时你能在日志里一搜就找到；
- **日志里别写密钥和个人数据**：记标识和摘要，不记原始请求体；
- **一个请求的缺陷不该带走整个进程**：每个请求在自己的事务里，失败就回滚；但守恒这类不变量被破坏，说明数据可能已经坏了，要告警，必要时停服务。

```python
import logging, uuid

class ServiceError(Exception): ...
def top_level(handler, request):
    try:
        return 200, handler(request)
    except ServiceError as e:
        return 400, str(e)                                # 预期失败：照合同回
    except Exception:
        rid = uuid.uuid4().hex[:8]
        logging.exception("unhandled, request %s", rid)   # 完整栈进日志
        return 500, f"internal_error {rid}"               # 对外只给请求号
def buggy(req): return req["missing"]
print(top_level(lambda r: "ok", {}), top_level(buggy, {})[0])   # (200, 'ok') 500
```

**知识点：**不可恢复错误与顶层处理（Crash vs Recover）
