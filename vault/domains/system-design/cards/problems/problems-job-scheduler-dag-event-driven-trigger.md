---
id: problems-job-scheduler-dag-event-driven-trigger
node: problems.foundations.job-scheduler
type: qa
step: 6
tags: [grown]
---
## Q
In a distributed job scheduler that supports DAG (directed acyclic graph) task dependencies, why is a DAG step's 'due' condition fundamentally different from a time-based job's, and how does the scheduler determine when a downstream step becomes due?

## A
A one-off or cron job's due condition is purely a function of time -- it becomes due when the clock reaches a stored timestamp -- so it fits naturally into a timing-wheel or time-bucket discovery mechanism. A DAG step's due condition is event-driven instead: it becomes due only when every step it depends on has reached a succeeded state, which has nothing to do with wall-clock time. The scheduler determines this by checking, each time a step completes, which downstream steps list it as a dependency, and pushing a downstream step into the dispatch path as 'due' only once all of its listed dependencies have independently reached succeeded.

## Q zh
在一个支持 DAG（有向无环图）任务依赖的分布式任务调度器里，为什么一个 DAG step 的「到期」条件和基于时间的任务在根本上不同？调度器怎么判断一个下游 step 什么时候变为到期？

## A zh
一次性任务或 cron 任务的到期条件纯粹是时间的函数——时钟走到存好的时间戳就到期，所以能自然地放进时间轮或时间分桶的发现机制里。DAG step 的到期条件则是事件驱动的：只有当它依赖的全部前置 step 都进入 succeeded 状态时它才到期，这和墙上时钟的时间毫无关系。调度器的判断方式是：每当一个 step 完成时，查询有哪些下游 step 把它列为依赖，只有当某个下游 step 列出的全部依赖都各自独立进入 succeeded 之后，才把这个下游 step 作为「到期」推入分发路径。
