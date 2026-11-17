---
id: errors-chaining-layers
node: errors.chaining
type: qa
step: 4
---
## Q
磁盘读失败，经过仓储层、服务层，最后变成对外的 503。每一层都换了异常类型，怎么保证出了问题还能从日志里找到最初的原因？对外的响应里该带多少？

## A
**每层换类型都带 `from`，对外只给码，根因进日志**

- **每一层都 `from e`**：`ServiceError` → `RepoError` → `OSError` 串成一条链，从最外层沿 `__cause__` 一路走回根因；
- **日志记整条链**：`logging.exception` 或 `traceback.format_exception` 会把链完整打印；
- **对外不带根因文本**：路径、SQL、内部地址不出门，用户拿到 503 加稳定的错误码和请求号；
- **每层换类型是为了让上层不依赖下层**：服务层看不到 `OSError`，以后仓储换成数据库，服务层代码不动；
- **断链的写法是缺陷**：中间某层写了 `from None` 或没写 `from`，日志里只剩最外一层，值班的人看不到根因。

```python
class RepoError(Exception): ...
class ServiceError(Exception): ...
def load():
    try: raise OSError("disk read failed")
    except OSError as e: raise RepoError("load") from e
def serve():
    try: load()
    except RepoError as e: raise ServiceError("503") from e

def chain(exc):
    while exc: yield type(exc).__name__; exc = exc.__cause__

try: serve()
except ServiceError as e: print(list(chain(e)))        # ['ServiceError', 'RepoError', 'OSError']
```

**知识点：**保留原因（Wrapping & Chaining）
