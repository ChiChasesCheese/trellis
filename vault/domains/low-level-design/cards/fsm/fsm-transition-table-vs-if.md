---
id: fsm-transition-table-vs-if
node: fsm.transition-table
type: qa
step: 2
---
## Q
放款函数写成 `if event == "disburse": return "active"`，漏了检查当前是否是待放款状态。这类缺陷用 `if` 链和用转移表，分别怎么暴露？

## A
**表里没有的组合必须明确报错**

- **`if` 链的症状**：只写了想到的组合，其余默认落到最后一行：原地不动，或直接放行；漏判当前状态，同一笔贷款可以放款多次；
- **表的做法**：（状态，事件）不在表里就抛错，任何没想到的组合都是显式拒绝；
- **读代码的成本**：表把规则和执行拆开，规则是数据，一眼看全；
- **边界**：如果每个状态的行为差异很大，表放不下（见“转移表与状态模式”）。

```python
def fire_if(state, event):
    if event == "disburse": return "active"           # 漏判状态
    if state == "active" and event == "settle": return "repaid"
    return state                                      # 漏掉的组合悄悄原地不动

TABLE = {("pending", "disburse"): "active", ("active", "settle"): "repaid"}
def fire(state, event):
    if (state, event) not in TABLE: raise ValueError((state, event))
    return TABLE[(state, event)]

print(fire_if("active", "disburse"))                  # active：第二次放款被默默接受
print(fire_if("repaid", "disburse"))                  # active：已还清又变回已放款
try: fire("active", "disburse")
except ValueError as e: print("rejected", e)          # rejected ('active', 'disburse')
```

**知识点：**转移表（Transition Table）
