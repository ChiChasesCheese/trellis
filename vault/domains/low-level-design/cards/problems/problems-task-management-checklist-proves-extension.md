---
id: problems-task-management-checklist-proves-extension
node: problems.social.task-management
type: qa
step: 8
tags: [grown]
---
## Q
任务看板设计的第 4 关要求给卡片加一份可勾选的清单，这条加法为什么能证明“位置用秩维护、索引由 CardStore 统一管理”这个设计是对的？

## A
清单的增删和勾选只读写卡片自己身上的一个字典字段，不影响卡片所在的列、秩、指派人或到期日中的任何一项——而这几项恰好是三类索引（按列、按指派人、按到期日）依赖的全部数据。因此清单相关的方法不需要经过 `CardStore`，`CardStore` 里维护索引一致性的代码一行都不用改。这证明了当初把“会影响索引的字段”和“不会影响索引的字段”分开管理（前者只能通过 CardStore 写入）是一条站得住的边界，新功能只要不触碰前者，天然就不会破坏索引。
