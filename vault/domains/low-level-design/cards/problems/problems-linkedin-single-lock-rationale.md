---
id: problems-linkedin-single-lock-rationale
node: problems.social.linkedin
type: qa
step: 8
tags: [grown]
---
## Q
职业社交设计里，`LinkedInService` 用一把锁保护档案、连接图、技能反向索引和申请表，为什么不按功能模块分别加锁以提高并发度，而且 GIL 在这里能提供什么保护？

## A
接受连接请求要同时改请求状态、连接图和“待处理请求”索引，申请职位要同时查重复申请和写申请表——这些复合操作本身只有几十次字典和集合操作，拆锁换不到可观的并发度，反而可能在“判断”和“落地”之间开出竞态窗口，比如两个线程同时判断某个技能还没有反向索引条目，各自创建一个新的 `set` 互相覆盖。GIL 只保证单条字节码不被切开，`self._skill_index.setdefault(skill, set()).add(member_id)` 是好几条字节码组成的复合操作，GIL 管不住这种跨语句的竞态，必须靠显式的锁。
