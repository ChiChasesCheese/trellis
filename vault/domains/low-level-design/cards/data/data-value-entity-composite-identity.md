---
id: data-value-entity-composite-identity
node: data.value-entity
type: qa
step: 5
---
## Q
栈帧（stack frame）的名字是 `main`、`parse`、`parse`（递归调用）。如果按名字识别帧，会把什么算错？一个对象的身份有时不止一个字段，怎么表示？

## A
**身份可以是几个字段合成的键**

- **同名不同帧**：递归时第二个 `parse` 和第一个是不同的帧；火焰图或统计里按名字合并，就把深度信息抹掉了；
- **用完整路径当身份**：从根到这一帧的名字序列 `("main", "parse", "parse")`；
- **换了根也不同**：`("a", "parse")` 与 `("b", "parse")` 是两个帧，只看名字会合并；
- **复合键写成元组**：元组可哈希、按内容比较，直接当 `dict` 的键，不用自己写 `__eq__`；
- **测试要用对抗输入**：递归、换根、换顺序的样例；全是不同名字的简单样例，只按名字比较的错误实现也能通过。

```python
from collections import Counter

samples = [("main", "parse"), ("main", "parse", "parse"), ("main", "parse", "parse"), ("lib", "parse")]
by_name = Counter(path[-1] for path in samples)
by_path = Counter(samples)
print(by_name)                       # Counter({'parse': 4})：深度和来源都没了
print(by_path[("main", "parse", "parse")])    # 2
```

**知识点：**值对象与实体（Value vs Entity）
