---
id: craft-validated-construction-5-parse-dont-validate
node: craft.idioms.validated-construction
type: qa
step: 5
---
## Q
**构造即校验 · 从 `__post_init__` 到 API 边界的 schema 校验**｜写法

进程内，对象一构造就是合法的。服务面对的是不可信的 JSON 请求体，每个内部函数都再检查一遍字段，或者哪里都不检查。同样的思路怎么放大？

## A
**要点。** 同一个想法叫「解析而不是校验」（parse, don't validate）：在系统边界把不可信的数据**解析**成一个已校验的类型，之后内部函数只接收这个类型，不再重复检查。内部函数签名里写 `Transfer`，就等于声明「我拿到的一定是合法的」。

```python
class InvalidRuleSet(ValueError): ...

# 解析（parse）：把一团不可信的数据变成已校验的类型，只在边界做一次
@dataclass(frozen=True, slots=True)
class Transfer:
    src: str
    dst: str
    amount: int

    def __post_init__(self) -> None:
        if self.src == self.dst or self.amount <= 0:
            raise InvalidRuleSet("src != dst 且 amount > 0")

def parse_transfer(body: dict[str, Any]) -> Transfer:
    # bool 是 int 的子类，要显式排除，否则 True 会被当成金额 1
    amount = body.get("amount")
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise InvalidRuleSet("amount 必须是整数")
    return Transfer(str(body["src"]), str(body["dst"]), amount)

def execute(t: Transfer) -> str:          # 内部函数只收已校验的类型，不再重复检查
    return f"{t.src}->{t.dst}:{t.amount}"

print(execute(parse_transfer({"src": "a", "dst": "b", "amount": 5})))
for bad in ({"src": "a", "dst": "a", "amount": 5}, {"src": "a", "dst": "b", "amount": True}):
    try:
        parse_transfer(bad)
    except InvalidRuleSet as e:
        print("边界拒绝:", e)
```

实际输出：

```
a->b:5
边界拒绝: src != dst 且 amount > 0
边界拒绝: amount 必须是整数
```

**变化。** 进程内的校验失败是程序员的错（构造了非法对象），抛异常即可。边界上的失败是外部输入的错，要变成对客户端有用的 4xx 响应，带上哪个字段错了；边界还要处理类型陷阱，例如上面 `bool` 是 `int` 的子类，`True` 会被当成金额 1。

**代价。** 边界解析要写两遍类型（schema 和领域类型），常用的做法是用一份声明（如 pydantic、msgspec 这类库）同时生成两者；内部流转的类型一旦放宽（又出现了没经过解析的入口），所有「不用再检查」的假设就一起失效。

**信号。** 看到内部函数里到处是 `if x is None`、`if amount <= 0` 的重复检查，说明边界没有把数据变成一个可信类型。
