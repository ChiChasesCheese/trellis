---
id: bank-rule-engine-composite-stateless
node: bank.machine-coding.rule-engine
type: qa
step: 4
---
## Q
票务推荐的一级规则是「离客户六十英里内」与别的规则的组合，组合可以嵌套，别处写的规则也要能放进来。组合子怎么写？规则对象能不能把上一次的答案记下来省得重算？

## A
**组合体和叶子同接口，规则自己不记事**

- **组合（Composite）**：`AllOf`、`AnyOf` 自己也有 `matches(event, ctx)`，所以能无限嵌套。成员只要有这个方法（`typing.Protocol` 的结构化类型），别处写的规则不必继承任何基类；
- **用内置的 `all` 和 `any`**：天然短路，空集语义正确。手写循环去累计，容易变成「只留最后一条的结果」：第一条不过、最后一条过，整体却通过了；
- **规则无状态**：同一个规则对象服务很多客户、很多次调用，答案只取决于收到的 `event` 和 `ctx`。「谁在问、现在几点、查哪张表」全部从 `ctx` 来；
- **记忆的后果**：给 `Near` 加一个以城市为键的结果字典，先问一位 35 英里的客户得到 `True`，再问一位 50 英里的客户，还是 `True`，第二位的答案是第一位留下的；
- **要缓存，缓存放在一次调用的范围里**：一次 `recommend` 内，同一位客户、同一个出发点才是固定的，调用结束就丢。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Near:
    miles: int
    def matches(self, e, ctx): return ctx[e["city"]] <= self.miles   # 只用收到的参数

@dataclass(frozen=True)
class AllOf:
    rules: tuple                                  # 成员只要有 matches 就行，AllOf 自己也有
    def matches(self, e, ctx): return all(r.matches(e, ctx) for r in self.rules)

rule = AllOf((Near(60), AllOf((Near(40),))))      # 嵌套
show = {"city": "Tacoma"}
print(rule.matches(show, {"Tacoma": 35}), rule.matches(show, {"Tacoma": 50}))  # True False
```

<details class="pt"><summary>延伸</summary>

不要为此搭运算符重载的规则框架（`a & b | c`）：优先级和短路规则又要使用者多记一遍。运营要新建活动时写的是数据，不是表达式。完整的推荐器与五个线上现象见 [[solution-lcp-event-campaigns|活动推荐规则修复（Event Campaigns）]]，可叠加的折扣规则是同构的题：[[solution-amz-discount-engine]]。

</details>

**知识点：**规则引擎（Rule Engine）
