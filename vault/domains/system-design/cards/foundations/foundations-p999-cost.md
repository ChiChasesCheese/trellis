---
id: foundations-p999-cost
node: foundations.numbers
type: qa
---
## Q
Why does each further latency nine (p99 → p999) cost disproportionately more to fix — and when is p999 still worth paying for?

## A
The extreme tail is dominated by effectively **random events** — GC pauses, page faults, TCP retransmits, context switches, background compactions — not your code path, so code optimization stops helping; you're buying overprovisioning, hedging, and isolation instead. Queueing compounds it: one slow request delays everything behind it on that worker.

Worth it when the tail hits the most valuable traffic (Amazon tracks p999 because the slowest requests correlate with the heaviest-data, highest-spend customers) or when fan-out amplifies the tail into the median — [[foundations-tail-latency-amplification]].


## Q zh
为什么每多修一个延迟的"9"（p99 → p999）成本都不成比例地更高 — 什么时候 p999 仍然值得花这个钱？

## A zh
极端尾部主要由基本随机的事件主导 — GC 暂停、缺页、TCP 重传、上下文切换、后台压缩 — 而不是你的代码路径，所以代码优化不再有帮助；你买的是超量配置、对冲请求和隔离。排队会放大它：一个慢请求会拖慢它在那个 worker 后面排队的一切。

值得投入的情况：尾部命中了最有价值的流量（Amazon 追踪 p999，因为最慢的请求往往与数据量最大、消费最高的客户相关），或者 fan-out 会把尾部放大成用户面对的中位数 — 见 [[foundations-tail-latency-amplification]]。
