---
id: bank-rule-engine-rules-as-data
node: bank.machine-coding.rule-engine
type: qa
step: 1
---
## Q
运营要自己配「国家在美国或加拿大、而且年龄大于 17 就给新版」这类定向规则。规则该写成代码里的 `if` 分支、每个条件一个类，还是配置数据？操作符放在哪里？

## A
**规则是数据：条件三元组加一张操作符表**

- **条件**：`(attribute, op, value)` 三元组；规则是「条件列表加命中后给什么」。全是纯数据，能存、能校验、能复制，运营改配置不用发版；
- **操作符表**：`dict`，名字到纯函数。它同时是「合法操作符」的名单，校验和求值读同一份，加一个操作符只改一处；
- **为什么不是类层次**：每个操作符没有状态，一个函数就够。一操作符一个类在 Python 里只多文件，不多灵活；操作符要带配置（比如编译好的正则）时再升级成类；
- **写入时校验**：`parse_condition` 遇到未知操作符（比如 `gte`）当场抛 `ValueError: unknown op 'gte'`，不会等到某个用户的请求才炸；
- **冻结**：解析后存元组，调用方之后再改自己的字典，存下来的规则不受影响。

```python
OPS = {"eq": lambda a, b: a == b, "gt": lambda a, b: a > b, "in": lambda a, b: a in b}

def parse_condition(raw: dict) -> tuple:
    if raw["op"] not in OPS:                      # 写入配置时就校验，不等到求值
        raise ValueError(f"unknown op {raw['op']!r}")
    return (raw["attribute"], raw["op"], raw["value"])

def hit(cond, attrs):
    attr, op, value = cond
    return attr in attrs and OPS[op](attrs[attr], value)

cond = parse_condition({"attribute": "country", "op": "in", "value": ("US", "CA")})
print(hit(cond, {"country": "US"}), hit(cond, {"country": "MX"}))   # True False
```

<details class="pt"><summary>延伸</summary>

条件之间只有 AND 时，OR 靠多写几条规则表达（首条命中的赢）；真要在一条规则里嵌套 OR 与 NOT，数据形状就得变成树（`{"any": [...]}`），求值器递归。功能开关服务只要 AND 列表就够，见 [[solution-lcp-feature-flag|功能开关与实验分组（Feature Flag）]]。

</details>

**知识点：**规则引擎（Rule Engine）
