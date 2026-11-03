---
id: craft-default-forms-5-across-problems
node: craft.idioms.default-forms
type: qa
step: 5
---
## Q
**省掉标志变量 · 候位、计费、缓存、账本里几种“少一个变量”的写法**｜写法

餐厅候位、计费引擎、TTL 缓存、复式账本都用了 `min(default=)`、`for-else`、`next(..., None)`、海象运算符。它们解决的是同一类问题吗？

## A
**要点。** 是。共同点：一个**可变的标志变量**（`found`、`best`、`done`），在多个出口都必须正确更新，漏一处就是只在特定输入出现的 bug。这四种写法都把“有没有”编码进表达式本身的值，或循环自身的结构里，少了一种状态，就少了一种漏更新的方式。

```python
# restaurant-waitlist：元组键 + default，一次比较两条规则
fit = min(((sizes[t], t) for t in free if sizes[t] >= size), default=None)

# restaurant-waitlist：整队没人能坐就结束，不用标志变量
else:
    return seated

# billing-tax-engine：找第一个能跑的，找不到就是有环
ready = next((r for r in pending if all(n in done for n in r.needs)), None)
if ready is None:
    raise InvalidRuleSet(f"规则依赖成环: {[r.rule_id for r in pending]}")

# ttl-cache：取值并判断，loop-and-a-half
while (key := self._expiry.pop_due(now)) is not None:

# double-entry-ledger：查到就用，不重复 get
if (seq := self._by_id.get(entry.id)) is not None:
```

边界：同一行里 `next` 嵌套 `all`，再套一层条件，就读不动了；这时候写成带名字的小函数（`_is_ready(rule, done)`），一行 `next` 的价值不变，可读性回来了。

**见于。** restaurant-waitlist、billing-tax-engine、ttl-cache、double-entry-ledger。

**信号。** 代码里出现 `found = False`、`best = None` 加循环里改它们，或者同一个函数在循环前后各调一次。
