---
id: ai-verification-differential
node: ai.verification
type: qa
step: 4
---
## Q
实现用了双端队列、堆这类优化，例子很难穷尽。怎么用随机输入验证它？参照实现该怎么写？

## A
**拿一个笨但明显对的实现对拍**

- **对拍**：同一串随机输入喂给快实现和参照实现，输出必须一致，发现分歧就缩小输入；
- **参照要笨**：直接按定义扫描全部历史，不优化、不共用被测代码的任何辅助函数；一样聪明就会一样错；
- **参照要独立**：它是你按合同写的，或者由智能体另写后你逐行读过，不是被测实现的改写；
- **固定种子**：失败要能重放，`random.Random(seed)` 记下种子。

```python
import random, collections

def fast(ts, limit, w):                      # 被测：双端队列只留窗口内的
    q, n = collections.deque(), 0
    for t in ts:
        while q and t - q[0] >= w: q.popleft()
        if len(q) < limit: q.append(t); n += 1
    return n

def naive(ts, limit, w):                     # 参照：每次扫描全部放行记录
    ok = []
    for t in ts:
        if sum(t - x < w for x in ok) < limit: ok.append(t)
    return len(ok)

for seed in range(300):
    ts = sorted(random.Random(seed).choices(range(50), k=20))
    assert fast(ts, 3, 10) == naive(ts, 3, 10), seed
```

<details class="pt"><summary>延伸</summary>

把 `fast` 里的 `>=` 改成 `>` 再跑，对拍会在某个种子上停下，并把种子报出来。输入要有足够多的碰撞（这里时间戳只取 0 到 49，所以相同时刻和恰好整窗都会出现），否则随机输入也碰不到边界。

</details>

**知识点：**验证输出（Verification）
