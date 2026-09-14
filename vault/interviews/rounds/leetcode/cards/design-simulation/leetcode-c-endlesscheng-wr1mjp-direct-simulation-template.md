---
id: leetcode-c-endlesscheng-wr1mjp-direct-simulation-template
node: design-simulation.direct-simulation
type: cloze
anki: 1787272469780
tags: [concept-cloze, leetcode, recall, template]
---
模拟循环通常是 {{c1::读取操作 -> 更新状态 -> 记录需要的输出}}。

```
def simulate(operations):
    state = {}
    result = []
    for op, key, value in operations:
        if op == "set":
            state[key] = value
        elif op == "get":
            result.append(state.get(key, -1))
    return result
```

**Evidence**

1. 模拟

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.01%20-%20%E7%9B%B4%E6%8E%A5%E6%A8%A1%E6%8B%9F)
