---
id: problems-ride-sharing-in-progress-is-not-cancellable
node: problems.marketplaces.ride-sharing
type: qa
step: 5
tags: [grown]
---
## Q
网约车的行程已经处在 IN_PROGRESS（乘客已上车）时，乘客、司机还是平台可以取消它？为什么给 IN_PROGRESS 加一条通向 CANCELLED 的边是错的？

## A
**三方都不能。** IN_PROGRESS 只通向 COMPLETED。

候选人常常顺手加上这条边，理由是「万一路上出事呢」。但「车开了一半、乘客中途下车」在业务上**不是取消**，是「提前结束并按已走里程计费」——它有账要结、有钱要收，和取消的语义完全相反。把两件事挤进同一个状态，报表上「取消率」这个指标立刻失去意义，客服也无法区分「没接上人」和「半路下车」。

一般规律：**状态机的边是业务约定，不是防御性编程。**「以防万一」加出来的边，代价是一个语义被污染的终态。真需要中途结束，就加一个新动作（`end_early`）和一条新边，而不是复用 CANCELLED。

同理，取消权限要按方区分：还没人接单的行程上根本没有「这位司机」，所以司机方无权取消一趟 REQUESTED 的行程。
