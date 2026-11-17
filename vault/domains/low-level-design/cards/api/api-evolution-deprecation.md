---
id: api-evolution-deprecation
node: api.evolution
type: qa
step: 2
---
## Q
要把 `get_user(id)` 改名为 `fetch_user(id)`。直接删掉旧名字会炸掉所有调用方。怎样弃用（deprecate）旧名字，`DeprecationWarning` 为什么经常没人看到？

## A
**保留旧名字、转发给新名字、发出警告，过一个明确的期限再删**

- **三步**：先加新名字；旧名字保留并转发；旧名字调用时 `warnings.warn(..., DeprecationWarning, stacklevel=2)`；
- **`stacklevel=2`**：让警告指向调用方的那一行，而不是旧函数内部，调用方才知道该改哪里；
- **为什么看不到**：默认过滤器只显示由 `__main__` 里的代码直接触发的 `DeprecationWarning`；库里的调用默认被忽略。pytest 默认会显示它们，生产环境不会；
- **要让人看到**：期限内对你自己的测试开 `-W error::DeprecationWarning`；给调用方的文档和发行说明写明删除的版本号；
- **到期再删**：文档写“在 2.0 删除”，到了 2.0 就真的删；没有期限的弃用永远不会完成。

```python
import warnings

def fetch_user(uid: int) -> dict:
    return {"id": uid}

def get_user(uid: int) -> dict:
    warnings.warn("get_user is deprecated, use fetch_user; removed in 2.0",
                  DeprecationWarning, stacklevel=2)
    return fetch_user(uid)

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    get_user(1)                                     # 这一行是调用方
print(caught[0].category.__name__, caught[0].lineno)
```

**知识点：**接口演进（API Evolution）
