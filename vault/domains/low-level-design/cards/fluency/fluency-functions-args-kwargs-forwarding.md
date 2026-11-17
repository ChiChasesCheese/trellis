---
id: fluency-functions-args-kwargs-forwarding
node: fluency.functions
type: qa
step: 2
---
## Q
装饰器里的 `wrapper(*args, **kwargs)` 是干什么的？为什么业务函数自己写 `def charge(amount, **opts)` 反而会让拼错的参数名悄悄通过？

## A
**`*args/**kwargs` 只用来转发，业务函数写明参数**

- **收集与展开**：`*args` 收集多余的位置参数成 `tuple`，`**kwargs` 收集多余的关键字参数成 `dict`；调用时 `f(*xs, **kw)` 反过来展开；
- **适合转发的地方**：装饰器、包装函数、代理；`wrapper` 不关心被包装函数的签名，原样传过去；配合 `functools.wraps(fn)` 保留 `__name__` 和文档；
- **业务函数里用 `**opts` 吞掉所有选项**：调用方写 `curency="EUR"`（拼错）不会报错，函数默默用默认的 `USD`，金额币种就错了；写明参数 `*, currency="USD"`，拼错立刻 `TypeError`；
- **展开重名**：`dict(a=1, **{"a": 2})` 抛 `TypeError`；合并字典要覆盖时用 `{**d1, **d2}`，后面的赢；
- **何时用 `**kwargs` 当数据**：处理不确定的键（透传给另一个库）；这时在边界上校验允许的键集合，把多余的键拒绝。

```python
import functools

def timed(fn):
    @functools.wraps(fn)                    # 保留名字与文档
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)          # 原样转发
    return wrapper

@timed
def charge(amount, *, currency="USD"):
    return amount, currency

print(charge(5, currency="EUR"), charge.__name__)    # (5, 'EUR') charge
try: charge(5, curency="EUR")
except TypeError as e: print(e)                      # 拼错立刻报错

def loose(amount, **opts): return amount, opts.get("currency", "USD")
print(loose(5, curency="EUR"))                       # (5, 'USD')：悄悄用了默认值
```

**知识点：**函数签名与参数（Function Signatures）
