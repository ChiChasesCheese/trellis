---
id: problems-rate-limiter-used-is-the-seam
node: problems.components.rate-limiter
type: qa
step: 3
tags: [grown]
---
## Q
限流器（Rate Limiter）要同时支持固定窗口、令牌桶、滑动窗口日志、滑动窗口计数四种算法。可替换的接缝该切在 `allow(now, cost)` 上，还是更低的地方？

## A
切在更低的地方：四种算法唯一真正的差别是**此刻这个 key 已经占掉了多少额度**。

固定窗口说「格子里的计数」，令牌桶说「容量减去现有令牌」，滑动日志说「窗口内的条目数」，滑动计数说「加权估计值」。把它抽成 `_used(now) -> float`，判定骨架就只写一次：够不够、还剩多少、`cost` 超上限返回 `math.inf`、被拒时一份都不扣——这四条规则全在基类的 `check` 里。子类只剩 `_used`／`_retry_after`／`commit` 三个方法，每个十行以内。

切在 `allow` 上的代价是那四条规则被抄四遍，迟早不一致（最常见的走样是某个算法在被拒路径上仍然写了状态）。

红利是回收判据可以在基类里一行写完：`is_idle(now)` 就是 `self._used(now) <= 0.0`。因为占用为 0 的状态和刚新建的状态对任何后续判定给出完全相同的答案，删掉它是**观察上等价**的，四种算法白捡了正确的回收语义。
