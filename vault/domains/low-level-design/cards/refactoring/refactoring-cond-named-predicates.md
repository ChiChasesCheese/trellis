---
id: refactoring-cond-named-predicates
node: refactoring.conditionals
type: qa
step: 2
---
## Q
活动匹配规则里，“`all_of` 要求每一条规则都匹配”写成了循环，里面每轮都 `matched = rule(x)`，结果只有最后一条规则起作用。这个缺陷是怎么来的？条件逻辑怎么写才不会出这种错？

## A
**用 `all` / `any` 表达“全部 / 任一”，把每个条件命名成谓词**

- **循环里反复赋值，后一次覆盖前一次**：`matched = rule(x)`，前面规则的结果被丢掉，只剩最后一条；
- **`all(rule(x) for rule in rules)` 直接说出意图**：不需要中间变量，也就没有被覆盖的机会；
- **短路求值**：`all` 遇到第一个 `False` 就停，`any` 遇到第一个 `True` 就停，不浪费计算；
- **长条件拆成有名字的小函数**：`is_nearby(show, user) and in_window(show, today)`，读代码就是读业务规则；
- **空列表要想清楚**：`all([])` 是 `True`，`any([])` 是 `False`；“没有规则”该算匹配还是不匹配，是规格问题。

```python
rules = [lambda x: x > 0, lambda x: x % 2 == 0, lambda x: x < 10]

def all_of_bad(x):
    matched = True
    for rule in rules:
        matched = rule(x)          # 缺陷：每轮覆盖，只剩最后一条的结果
    return matched

def all_of(x): return all(rule(x) for rule in rules)

print(all_of_bad(-4), all_of(-4))  # True False：-4 不满足第一条，被错误地放过
print(all([]), any([]))            # True False
```

**知识点：**简化条件（Simplifying Conditionals）
