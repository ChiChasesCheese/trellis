---
id: craft-kw-only-positional-only-4-scales-adding-parameters
node: craft.idioms.kw-only-positional-only
type: qa
step: 4
---
## Q
**参数形态 · 给已发布的接口加参数，为什么加在 `*` 之后才兼容**｜写法

支付函数 `charge(amount, currency="USD")` 已经被很多调用方使用，现在要加一个幂等键。把新参数加在中间和加在 `*` 之后，对只会按位置传参的旧调用方各有什么后果？同样的问题放到 HTTP 接口上怎么对应？

## A
**要点。** 向后兼容的底线是：旧调用方不改一个字，行为不变。位置参数的含义由顺序决定，在中间插入新参数会让旧调用的第二个值落进新参数，不报错但含义变了。新增的可选参数加在 `*` 之后：旧调用不会碰到它，新调用方必须写名字，两边互不干扰。

```python
import inspect

def charge_v1(amount: int, currency: str = "USD") -> str:
    return f"{amount} {currency}"

def charge_v2_positional(amount: int, idempotency_key: str | None = None, currency: str = "USD") -> str:
    return f"{amount} {currency} key={idempotency_key}"        # 插在中间

def charge_v2_kwonly(amount: int, currency: str = "USD", *, idempotency_key: str | None = None) -> str:
    return f"{amount} {currency} key={idempotency_key}"        # 加在 * 之后

old_call = (500, "EUR")                                        # 旧调用方：位置传参
print(charge_v1(*old_call))
print(charge_v2_positional(*old_call))                         # "EUR" 变成幂等键，币种悄悄变回 USD
print(charge_v2_kwonly(*old_call))                             # 旧调用原样可用
print(charge_v2_kwonly(500, idempotency_key="k1"))
print(inspect.signature(charge_v2_kwonly))
```

实际输出：

```
500 EUR
500 USD key=EUR
500 EUR key=None
500 USD key=k1
(amount: int, currency: str = 'USD', *, idempotency_key: str | None = None) -> str
```

**为什么。** 第二行最危险：没有报错，金额收对了，币种却变成了 USD，这是钱的错误。仅关键字让新增参数成为纯加法。

**变化。** 在 HTTP 接口上，对应关系是：JSON 字段按名字传递，新增可选字段旧客户端不会发，服务端取默认值，天然兼容；protobuf 用字段编号，规则是只加新编号、不改旧编号的含义，同一个想法。反过来，只按位置解释的协议（数组形式的元组、CSV 列）一旦改列序就破坏所有旧客户端。

**信号。** 评审接口变更时问：旧调用方原样调用，结果还一样吗？新增参数能否只用名字传？
