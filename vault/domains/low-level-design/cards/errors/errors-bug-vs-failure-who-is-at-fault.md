---
id: errors-bug-vs-failure-who-is-at-fault
node: errors.bug-vs-failure
type: qa
step: 5
---
## Q
内容审核服务调用的远程审核器超时了。这条评论该按“违规”拒绝、按“通过”放行，还是别的？为什么？

## A
**依赖出错是 503：不是用户的错，也不能放行**

- **谁的错决定返回什么**：用户输入错是 4xx；依赖不可用是 503；我们自己的缺陷是 500；
- **当成违规**：宕机一小时，所有正在发评论的好用户都被记一次违规，一批人被封号；
- **当成通过**：审核器一挂，所有违规内容放进来，宕机期间等于没有审核；
- **正确做法**：503，什么都不改（评论、违规数、id），由调用方稍后重试；
- **只翻译 `Exception`**：`KeyboardInterrupt`、`SystemExit` 不是审核器的失败，原样穿过。

```python
class ServiceError(Exception):
    def __init__(self, status: int, code: str):
        super().__init__(code); self.status, self.code = status, code

def moderate(text: str, checker) -> str:
    try: ok = checker(text)
    except Exception as exc: raise ServiceError(503, "checker_unavailable") from exc
    if not ok: raise ServiceError(422, "content_rejected")
    return "published"

def down(text): raise TimeoutError
for chk in (lambda t: True, lambda t: False, down):
    try: print(moderate("hi", chk))
    except ServiceError as e: print(e.status, e.code)   # published / 422 / 503
```

**知识点：**缺陷与预期失败（Bugs vs Failures）
