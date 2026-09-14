---
id: leetcode-q-open-the-lock-pattern
node: backtracking-search.bidirectional-search
type: qa
anki: 1787102263208
tags: [lc::752, leetcode, pattern, recall]
---
## Q
如何用 BFS 求解「转动密码锁」类问题（如 LeetCode 752 Open the Lock）？核心思路是什么？

## A
把每个 4 位密码状态看作图中的一个节点，从 "0000" 出发做逐层 BFS：每层遍历队列中所有当前状态，对每一位数字尝试 +1/-1（取模 10）生成最多 8 个相邻状态；用 visited 集合去重，deadends 集合作为禁止访问的节点；当弹出状态等于 target 时返回当前层数 step，队列为空仍未找到则返回 -1。关键不变量：BFS 逐层扩展保证第一次到达 target 时的层数就是最短转动次数。

**Evidence**

```
que, visited, step = deque(["0000"]), {"0000"}, 0
while que:
    for _ in range(len(que)):
        cur = que.popleft()
        if cur == target:
            return step
        for i in range(4):
            d = int(cur[i])
            for nd in ((d + 1) % 10, (d - 1) % 10):
                nxt = cur[:i] + str(nd) + cur[i+1:]
                if nxt not in dead and nxt not in visited:
                    visited.add(nxt)
                    que.append(nxt)
    step += 1
return -1
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F752%20-%20Open%20the%20Lock)
