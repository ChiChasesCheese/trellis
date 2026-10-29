---
id: tlc-remove-invalid-parentheses-5-alt
node: a.remove-invalid-parentheses
type: qa
step: 5
---
## Q
**LC 301 删除无效的括号**｜另一种解法

不先算最少删除量，换成「按删除个数分层」的做法：写出来，并说明它和带预算的回溯相比什么时候选哪个。

## A
**思路。** BFS。第 `0` 层只有原串；第 `k` 层是在第 `k-1` 层每个串上再删一个括号得到的所有串（集合去重）。每层先检查有没有有效串，有就整层返回——第一次出现有效串的层，删除个数一定最少。

```python
def remove_invalid_parentheses_bfs(s: str) -> list[str]:
    def valid(t: str) -> bool:
        balance = 0
        for ch in t:
            if ch == "(":
                balance += 1
            elif ch == ")":
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    level = {s}                                # 当前层：恰好删了 k 个字符得到的所有串
    while True:
        found = [t for t in level if valid(t)]
        if found:
            return found                       # 第一次出现有效串的层，就是删得最少的层
        level = {t[:i] + t[i + 1:] for t in level for i in range(len(t)) if t[i] in "()"}
```

运行：`"()())()"` → `['(())()', '()()()']`，`"(a)())()"` → `['(a())()', '(a)()()']`，`")("` → `['']`，`"((("` → `['']`。

**对比。** BFS 不需要先推导「最少删除量」，代码短、容易写对，适合面试里先给出正确解；但每层要生成并检查 `C(k, d)` 量级的串，每个检查 `O(n)`，括号多、需要删得多时开销大。带预算的回溯一开始就知道要删几个，剪枝掉绝大多数分支，在 `20` 个括号的上限下明显更快。数据小或想先保证正确性，选 BFS；要性能或被追问剪枝时，选预算回溯。

**别用的做法。** 不去重的 BFS：同一个串会被多条路径重复生成，层数一深就爆内存。
