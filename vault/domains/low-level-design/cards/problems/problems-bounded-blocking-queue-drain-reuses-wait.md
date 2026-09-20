---
id: problems-bounded-blocking-queue-drain-reuses-wait
node: problems.components.bounded-blocking-queue
type: qa
step: 7
tags: [grown]
---
## Q
给有界阻塞队列加一个 `drain(max_items=)`，一次取出最多 N 个元素给批量消费者。为什么它不应该『等到凑够 `max_items` 个才返回』，而是『叫醒之后有多少拿多少』？

## A
等到凑够意味着要重新设计一套等待逻辑：拿到第一批之后要判断『够不够、要不要继续等』，还要决定这段额外等待支不支持超时、会不会被 `close()` 打断——这些问题 `take` 的等待循环已经回答过一次（`while` 谓词、精确 `notify`、`close()` 语义），如果 `drain` 重新回答一遍，等于把同一套正确性论证复制一份，出 bug 的机会也跟着复制。`drain` 只在『完全没有元素且未关闭』时才等待，这正是 `take` 已经验证过的那段代码；一旦有至少一个元素就不再等待，把现有的（至多 `max_items` 个）一次性取走。这样加新方法完全不用碰已经调对的等待逻辑，也符合大多数批量消费者的真实需求——不想空手而归，也不想为了凑一个固定批次大小而无谓等待。
