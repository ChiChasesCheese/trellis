---
id: fsm-transition-table-validate
node: fsm.transition-table
type: qa
step: 4
---
## Q
转移表也会写错：一个状态没有任何入边，或者一个非终态没有出边。怎么在加载时就发现？

## A
**表是数据，可以用代码检查它本身**

- **不可达状态**：从起始状态出发走不到，规则里有这行也永远用不上，多半是漏写了入边；
- **死胡同**：不是终态却没有任何出边，进入后就卡住；
- **终态**：明确列出（已还清、已拒绝），终态没有出边是对的；
- **何时检查**：模块加载或测试里各一次，表改了就重跑。这种检查只有数据驱动的写法才做得到，`if` 链做不到。

```python
TABLE = {("pending", "disburse"): "active", ("pending", "reject"): "rejected",
         ("active", "settle"): "repaid"}
STATES = {"pending", "active", "repaid", "rejected", "frozen"}

def check(table, states, start, terminal):
    seen, todo = {start}, [start]
    while todo:
        s = todo.pop()
        for (src, _), dst in table.items():
            if src == s and dst not in seen: seen.add(dst); todo.append(dst)
    dead = {s for s in states - terminal if not any(k[0] == s for k in table)}
    return {"unreachable": states - seen, "dead_ends": dead}

print(check(TABLE, STATES, "pending", {"repaid", "rejected"}))
# {'unreachable': {'frozen'}, 'dead_ends': {'frozen'}}
```

**知识点：**转移表（Transition Table）
