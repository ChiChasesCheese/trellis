---
id: amz-splitwise-simplify-debts
node: amazon.amz-splitwise
type: qa
step: 5
tags: [grown]
---
## Q
在分账设计里，追加需求「最少笔转账结清全组」，怎么做？它能保证最少吗？

## A
先算每人净额（别人欠他的减去他欠别人的），净额为正的是债权人，为负的是债务人。每次让最大债务人还给最大债权人 `min(两者)`，至少一方清零，所以至多 n-1 笔。例：A +50、B -30、C -20，得 B→A 30、C→A 20。贪心不保证最少——真正最少等价于把人划分成尽可能多个「净额和为 0」的小组，是 NP 难问题；面试说清这一点即可。
```python
def simplify(net):
    pos = [(v, u) for u, v in net.items() if v > 0]
    neg = [(-v, u) for u, v in net.items() if v < 0]
    out = []
    while pos and neg:
        pos.sort(); neg.sort()
        c, cu = pos.pop(); d, du = neg.pop()
        t = min(c, d)
        out.append((du, cu, t))
        if c > t: pos.append((c - t, cu))
        if d > t: neg.append((d - t, du))
    return out
```
