---
id: craft-frozen-value-objects-1-fingerprint-by-value
node: craft.idioms.frozen-value-objects
type: qa
step: 1
---
## Q
**不可变值对象 · 为什么请求指纹不用普通类也不用元组**｜写法

幂等转账要判断「同一个键带来的两次请求内容是否相同」。最直接的写法是随手建一个普通类，或者把字段拼成元组存起来。这两种写法各自在哪里出问题？`@dataclass(frozen=True, slots=True)` 到底多给了什么？

## A
**要点。** 值对象（value object）的身份由内容决定：字段都相同就是同一个东西。这需要三样：按字段比较的 `==`、与之一致的 `hash`、交出去之后别人改不了。普通类三样都没有：`==` 默认比较身份（是不是同一个内存对象）。元组有 `==` 却不带字段名和类型。冻结的数据类（frozen dataclass）由装饰器生成这三样。

```python
# 朴素版：普通类，没写 __eq__ / __hash__
class PlainReq:
    def __init__(self, src, dst, amount):
        self.src, self.dst, self.amount = src, dst, amount

# 冻结值对象：eq、hash、只读都是生成的
@dataclass(frozen=True, slots=True)
class Req:
    src: str
    dst: str
    amount: int

seen = {}                                   # 键 -> 第一次的请求指纹

def check(fp_a, fp_b):
    seen["k1"] = fp_a
    return seen["k1"] == fp_b               # 同键重试：内容相同吗？

print("普通类  同内容重试 ==", check(PlainReq("a", "b", 5), PlainReq("a", "b", 5)))
print("frozen  同内容重试 ==", check(Req("a", "b", 5), Req("a", "b", 5)))
print("frozen  改了金额   ==", check(Req("a", "b", 5), Req("a", "b", 6)))

# 元组指纹能比较，但不带类型和字段名：转账与退款的元组碰巧相同就判成同一个
@dataclass(frozen=True, slots=True)
class Refund:
    src: str
    dst: str
    amount: int

print("元组    转账 == 退款:", ("a", "b", 5) == ("a", "b", 5))
print("frozen  转账 == 退款:", Req("a", "b", 5) == Refund("a", "b", 5))

r = Req("a", "b", 5)
try:
    r.amount = 999                          # 交出去之后别处想改也改不了
except Exception as e:
    print("改字段:", type(e).__name__)
print("可作字典键:", {r: "receipt-1"}[Req("a", "b", 5)])
```

同一个键、两次内容相同的请求，实际输出：

```
普通类  同内容重试 == False
frozen  同内容重试 == True
frozen  改了金额   == False
元组    转账 == 退款: True
frozen  转账 == 退款: False
改字段: FrozenInstanceError
可作字典键: receipt-1
```

**为什么。** 元组指纹的问题不在语法，而在语义：转账和退款的字段碰巧一样就被判为同一个请求，而且调用处只能靠位置记住哪一位是金额。数据类的 `==` 先比较类型再比较字段，名字也进了代码。

**代价。** 状态变化要造新对象（见「用 replace 表达状态变化」）。只有字段会变的对象（账户余额、会话）才不该写成值对象。
