---
id: craft-protocol-callable-abc-2-protocol-structural
node: craft.idioms.protocol-callable-abc
type: qa
step: 2
---
## Q
**策略接口 · 实现者是冻结数据类时，为什么用 Protocol 而不是 ABC**｜写法

计费引擎里的规则（`Rule`）是一个个 `frozen=True` 的数据类，文件监听器的 `FileSystem` 在测试里要换成内存假实现。接口分别用了 `Protocol`。继承 ABC 同样能表达「必须有 `apply`」，为什么不用？

## A
**要点。** `Protocol`（协议类）是结构化类型（structural typing）：只要对象有同名同形的成员，类型检查器就认为它满足接口，**不需要继承**。ABC 是名义类型（nominal typing）：必须显式继承。实现者本来就是别的东西（数据类、已有的第三方类、测试里临时写的假对象）时，Protocol 不要求它们多一层继承，也不会把接口的存在渗透进实现者的类层次里。

```python
class Rule(Protocol):
    rule_id: str
    def apply(self, amount: Decimal) -> Decimal | None: ...

@dataclass(frozen=True, slots=True)
class PercentFee:                       # 没有继承 Rule
    rule_id: str
    pct: Decimal
    def apply(self, amount: Decimal) -> Decimal | None:
        return amount * self.pct / 100

def total(rules: list[Rule], amount: Decimal) -> Decimal:
    return sum((r.apply(amount) or Decimal(0) for r in rules), Decimal(0))

class FakeRule:                         # 测试里临时写一个，同样没有基类
    rule_id = "fake"
    def apply(self, amount):
        return Decimal(1)

print(total([PercentFee("fee", Decimal(3)), FakeRule()], Decimal(200)))
print("PercentFee 的基类:", [c.__name__ for c in PercentFee.__mro__])
```

实际输出：

```
7
PercentFee 的基类: ['PercentFee', 'object']
```

**为什么。** 接口由使用方（`total`）定义，写在使用的一侧：「我只需要对象会 `apply`」。实现者对此一无所知，所以第三方类也能直接传进来。

**代价。** Protocol 只在类型检查器里生效；运行时传错对象，要等到调用时才报 `AttributeError`。ABC 在实例化时就拒绝缺方法的子类（见第 3 张卡）。Protocol 也不能给实现者提供共享代码。
