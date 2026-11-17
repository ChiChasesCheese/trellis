---
id: errors-narrow-wide-lies
node: errors.narrow-catch
type: qa
step: 3
---
## Q
HTTP 适配器写成 `try: 解析 limit 并调用服务; except ValueError: 返回 400 invalid_limit`。服务内部抛的 `ValueError` 会被怎样处理？

## A
**太宽的 `except` 会给别人的错贴上自己的标签**

- **服务内部的 `ValueError` 也被说成 `invalid_limit`**：一条损坏的数据让所有请求回 400，用户反复改参数，我们的缺陷却被藏起来；
- **`ValueError` 是个大家族**：`UnicodeDecodeError` 也是它的子类，读请求体时的解码错同样会落进来；
- **做法**：`try` 只包解析，调用服务放在后面，服务里的异常按它自己的方式处理（缺陷变成 500）；
- **测试要钉住**：服务抛 `ValueError` 时，适配器不能返回 `invalid_limit`；
- **判别**：`except` 里的消息承诺了一个原因，`try` 里就只能放得出这个原因的代码。

```python
def fetch(limit):
    raise ValueError("corrupt row")             # 服务内部的缺陷

def wide(raw):
    try: return 200, fetch(int(raw))
    except ValueError: return 400, "invalid_limit"

def narrow(raw):
    try: limit = int(raw)
    except ValueError: return 400, "invalid_limit"
    return 200, fetch(limit)                    # 在 try 外面

print(wide("5"), issubclass(UnicodeDecodeError, ValueError))   # (400, 'invalid_limit') True
try: narrow("5")
except ValueError as e: print("缺陷露出来了：", e)
```

**知识点：**捕获的范围（Narrow Catch）
