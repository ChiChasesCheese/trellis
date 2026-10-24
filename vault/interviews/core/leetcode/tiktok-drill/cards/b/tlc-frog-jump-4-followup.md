---
id: tlc-frog-jump-4-followup
node: b.frog-jump
type: qa
step: 4
---
## Q
**LC 403 青蛙过河**｜追问

面试官接着问：（1）要输出一条具体的跳法？（2）石子数量扩大到几万，怎么剪枝？（3）允许第一步跳任意长度，或者允许向后跳，还能这么做吗？

## A
1. **输出跳法**：把集合换成字典 `jumps[pos][step] = 上一块石子位置`，到达终点后沿 `(pos, step)` 回溯：`prev = jumps[pos][step]`，再用 `step` 找 `prev` 处的上一跳，直到起点。空间仍是 `O(n^2)`。
2. **剪枝**：第 `i` 块石子上的最后一跳长度不会超过 `i`（每步至多比前一步多 `1`），所以 `k > i` 的状态不会出现，可以不存；另外若某相邻间距 `stones[i+1] − stones[i] > i + 1`，青蛙在前 `i + 1` 块石子上的任何一跳都不超过 `i + 1`，跨不过这个缺口，可以直接返回 `False`。
3. **起点任意 / 可后退**：起点任意只是把初始集合改成所有候选；允许向后跳后，位置不再单调，不能按升序一次扫完，需要 BFS / DFS 加 `visited[(pos, k)]`，因为同一状态可能被回头访问。

**Python 提醒**：往一个集合里加元素的同时遍历它会抛 `RuntimeError: Set changed size during iteration`；即使这里被 `step > 0` 避开，也可以先 `for k in list(jumps[pos])` 取快照，防止以后改动时踩坑。
