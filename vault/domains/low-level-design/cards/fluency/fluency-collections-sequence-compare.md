---
id: fluency-collections-sequence-compare
node: fluency.collections
type: qa
step: 5
---
## Q
汇率路线是货币序列，比如 `("USD", "EUR")`，边数相同时要按字典序选。有人把序列拼成 `"USDEUR"` 再比字符串。为什么这样会选错？序列怎么比较？

## A
**序列逐项比较，别拼成字符串**

- **`tuple` 和 `list` 逐项比较**：先比第一项，相同再比第二项；一个是另一个的前缀时，短的更小；
- **拼接丢掉了边界**：`("AB", "C")` 与 `("A", "BC")` 拼出来都是 `"ABC"`，字符串比较认为相等，序列比较能区分；货币码长度不一时就会错；
- **可以直接比较**：`min(routes)`、`sorted(routes)` 对元组组成的列表都是按字典序；先比边数再比序列，就把 key 写成 `(len(route), route)`；
- **`list` 与 `tuple` 之间不能互相比较**：`[1] < (1,)` 抛 `TypeError`，统一一种；
- **同一个原则**：多个排序维度合成元组放进 key，不要为了排序把字段拼成字符串。

```python
a, b = ("AB", "C"), ("A", "BC")
print("".join(a) == "".join(b))              # True：拼接后分不出
print(a < b, b < a)                          # False True：逐项比较，"A" < "AB"

routes = [("USD", "JPY", "EUR"), ("USD", "EUR"), ("USD", "GBP")]
print(min(routes, key=lambda r: (len(r), r)))          # ('USD', 'EUR')
print(("USD", "JPY") < ("USD", "JPY", "EUR"))          # True：前缀更小
```

**知识点：**容器的选择与惯用法（Collections Idioms）
