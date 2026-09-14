---
id: cc-input-mal-corrupt-row-participates-in-nothing
node: input.malformed
type: qa
---
## Q
Rule: if any row of a dispute group carries the reason `withdrawn`, no row of that group is output. A row that says `withdrawn` is itself corrupted — does it still cancel the group?

## A
**No. A corrupted row is not a record; it never reaches the grouping stage at all.**

The pipeline order is the answer: validate → keep the survivors → group → apply group rules → render. A corrupted row is dropped (and counted) at stage one, so it cannot cancel anything, cannot create a group, and cannot contribute to a count.

This is a favourite hidden test precisely because a program that validates *while* grouping gets it wrong. Keeping validation as its own pass makes the answer fall out instead of needing a special case.

## Q zh
规则：如果某个争议分组里有任意一行的原因是 `withdrawn`，该组的所有行都不输出。若这行 `withdrawn` 本身是损坏行，它还会取消整组吗？

## A zh
**不会。损坏行不是一条记录，它根本到不了分组阶段。**

流水线顺序就是答案：校验 → 留下幸存者 → 分组 → 应用分组规则 → 渲染。损坏行在第一阶段就被丢弃（并计数），所以它取消不了任何东西、建不了组，也不参与任何计数。

这正是隐藏测试的心头好，因为**边分组边校验**的程序会答错。把校验独立成一趟，答案就自然成立，不需要特例。
