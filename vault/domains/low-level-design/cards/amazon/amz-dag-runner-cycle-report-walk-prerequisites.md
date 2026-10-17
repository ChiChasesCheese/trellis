---
id: amz-dag-runner-cycle-report-walk-prerequisites
node: amazon.amz-dag-runner
type: qa
step: 4
tags: [grown]
---
## Q
在 Amazon DAG 执行器里，Kahn 算法卡住后怎样得到具体的环？以 {"app":["x"],"x":["y"],"y":["x"]} 为例。

## A
卡住的节点入度都大于 0，所以每个都至少还有一个同样卡住的前置依赖。从任一卡住的节点出发不断跳到它卡住的前置依赖，路径必然重复，截取重复段就是环，O(V)。例中卡住 app、x、y；从 app 走 app→x→y→x，截得环 (x, y)；app 只是挂在环下面，不属于环，所以不进结果。

```python
def find_cycle(need, stuck):
    node, path, pos = next(iter(stuck)), [], {}
    while node not in pos:
        pos[node] = len(path); path.append(node)
        node = next(d for d in need[node] if d in stuck)
    return path[pos[node]:]
```
