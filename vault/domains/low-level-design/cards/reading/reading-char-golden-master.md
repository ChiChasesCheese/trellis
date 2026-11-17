---
id: reading-char-golden-master
node: reading.characterization
type: qa
step: 2
---
## Q
一个函数有几十种输入组合，一条条手写断言太慢。想重构它，怎样用一批输入把它的现有行为整体钉住？和普通的单元测试区别在哪？

## A
**黄金快照（golden master）：用一批输入跑一遍，把输出存下来，之后逐字比较**

- **输入要覆盖广**：边界值、典型值、非法值，再加上固定种子生成的随机输入；
- **输出整体比较**：存成一个字典或 JSON，改动后重新跑，任何一项不同都能看到是哪个输入；
- **和单元测试的区别**：单元测试断言的是“应该是什么”；快照记录的是“现在是什么”，对错由你另外判断；
- **随机输入必须可重放**：用 `random.Random(seed)`，同一个种子永远同一批输入；否则每次快照都不同；
- **有意改变行为时更新快照**：改完逐项看差异，确认是预期内的，再把新输出存为新的快照；
- **不适合**：输出带时间戳、随机 id、字典顺序不稳定的函数，要先把这些去掉或固定。

```python
import json, random

def shipping(kg):
    if kg < 1: return 5
    if kg < 5: return 9
    return 9 + (kg - 5) * 2

rng = random.Random(42)                                    # 固定种子
inputs = [-3, 0, 0.99, 1, 4.99, 5] + [round(rng.uniform(0, 20), 1) for _ in range(5)]
snapshot = json.dumps({str(k): shipping(k) for k in inputs}, sort_keys=True)

# 重构之后：同样的输入，结果必须逐字相同
assert snapshot == json.dumps({str(k): shipping(k) for k in inputs}, sort_keys=True)
print(len(inputs), "个输入已钉住")
```

**知识点：**特征测试（Characterization Tests）
