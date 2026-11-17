---
id: bank-rule-engine-empty-missing
node: bank.machine-coding.rule-engine
type: qa
step: 3
---
## Q
规则的 `conditions` 是空列表；用户缺了规则要看的属性；属性类型和配置对不上（年龄传成 `"18"`，布尔值遇上 `gt`，数字遇上 `contains`）。这三种情况各该返回什么？

## A
**空条件全中，缺失与错型都不中**

- **空条件**：条件之间是 AND，`all([])` 是 `True`，空列表命中所有人；OR 相反，`any([])` 是 `False`。排在前面的空条件规则会吞掉后面所有规则，所以它是合法配置，但评审时要看得见；
- **属性缺失**：条件为 `False`，`neq` 和 `not_in` 也一样。「没填国家」不等于「国家不是美国」，否则没填的用户会掉进「非美国」规则；
- **类型不符**：条件为 `False`，不抛 `TypeError`。一个用户的脏属性不该让整次求值失败；
- **布尔不是数字**：`isinstance(True, int)` 为 `True`，所以数字比较用 `type(x) in (int, float)`，否则 `gt 0` 会命中 `true`；
- **两种错分开处理**：配置里的类型错（`gt` 配了字符串）是写入时的校验错误；用户属性的类型错是求值时的「不命中」。

```python
OPS = {
    "neq": lambda a, b: a != b,
    "gt": lambda a, b: type(a) in (int, float) and a > b,    # bool、str 都不当数字
    "contains": lambda a, b: isinstance(a, str) and b in a,  # 只对字符串属性
}

def hit(cond, attrs):
    attr, op, value = cond
    return attr in attrs and OPS[op](attrs[attr], value)     # 属性缺失：一律不命中

print(all([]), any([]))                          # True False：空条件命中所有人
print(hit(("country", "neq", "US"), {}))         # False，缺失的 neq 也不命中
print(hit(("age", "gt", 17), {"age": "18"}))     # False，不抛 TypeError
print(hit(("age", "gt", 0), {"age": True}))      # False，布尔不是数字
print(hit(("name", "contains", "a"), {"name": 5}))   # False，不抛 TypeError
```

<details class="pt"><summary>延伸</summary>

缺失当 `False` 的代价是：「国家不是美国」覆盖不到没填国家的用户。真要覆盖，就加一个显式的「属性缺失」操作符，而不是改 `neq` 的语义。相等与比较里布尔和数字怎么分开，见 [[solution-lcp-feature-flag|功能开关与实验分组（Feature Flag）]]。

</details>

**知识点：**规则引擎（Rule Engine）
