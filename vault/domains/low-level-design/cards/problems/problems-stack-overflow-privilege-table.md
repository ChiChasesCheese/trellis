---
id: problems-stack-overflow-privilege-table
node: problems.social.stack-overflow
type: qa
step: 4
tags: [grown]
---
## Q
问答社区设计里，评论需要 50 声望、降票需要 125 声望、编辑他人帖子需要 2000 声望，为什么不给这三项权限各建一个 `PrivilegyPolicy` 接口和一个实现类，而是用一张 `Mapping[Privilege, int]` 加一个 `.can(reputation, privilege)` 方法？

## A
因为三个“策略实现类”的行为完全一样——都只是一次数值比较，差别只在门槛数字，这是数据的差异而不是行为的差异。子类或接口的正当理由是行为不同，不是参数不同。用一张表查阈值，加一项新权限只需要往字典和枚举里各加一行，`.can()` 的代码一行不动；建一组只有一行逻辑的策略类，换回来的收益是零，却多背了几个只有一个方法的类。
