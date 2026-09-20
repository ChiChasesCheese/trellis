---
nodes: [problems.social.task-management, structure.state-machines]
tags: [problem]
---
# Drill：任务看板（Trello / Jira）

一个任务看板：几块看板，每块有若干列，卡片在列之间移动、能重新排序；每块看板有自己的一套
工作流转移规则；卡片能指派、打标签、设截止日期；产品要能按人查跨看板的卡、查全站逾期的卡、
按列分组看一块看板。看板成员权限系统不在这道题里。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：看板、列、卡片。建卡默认追加到列尾；同一列内能重新排序。先决定
  "位置怎么存"——整数下标每次插入都要重排后面所有卡，这个决定不对，后面每一步都会拖慢。
- 第 2 关（约 20 分钟）：工作流转移、指派、标签、截止日期。跨列移动前必须查这块看板自己
  的转移表，不允许硬编码"待办/进行中/完成"三段式。想清楚"活动记录存在哪里"——它是"这张卡
  上发生过什么"的唯一真相来源。
- 第 3 关（约 15 分钟）：三条查询——一个人跨所有看板的指派卡、全站逾期的卡、一块看板按列
  分组的视图——都必须是查索引，不能扫全部卡片。归档一张卡要让它从这些索引里消失。
- 第 4 关（选做）：给卡片加一份可勾选的清单，或者按史诗/优先级加一个横向的 swimlane 视图。
  评分点是"加它有没有碰到位置维护或工作流转移那段代码的任何一行"。

**怎么练**：把 `vault/domains/low-level-design/problems/task-management/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/task-management -q`。

**评分点**
- 位置用可排序的浮点秩维护，不用整数下标——插入或移动只写被移动的那张卡自己的一个数字（[[problems-task-management-rank-not-index]]）。
- 秩的间距被反复挤占最终会耗尽，此时应该整列重排而不是让排序坏掉或让异常泄漏给调用方（[[problems-task-management-rank-exhausted-rebalance]]）。
- 工作流是一张按看板各自声明的转移表，不是给每个状态各写一个类——状态之间没有行为差异，只有"允许转到哪里"这一项数据差异（[[problems-task-management-workflow-table-not-state-classes]]）。
- 工作流不能硬编码成全局唯一的"待办/进行中/完成"三段式，不同看板需要不同的状态和转移规则（[[problems-task-management-workflow-per-board]]）。
- 逾期查询只需要一份"未归档且设了到期日"的过滤索引，不需要一棵按日期排序的树——判据是产品要的是批量查询，不是"下一个最快到期的" （[[problems-task-management-overdue-filtered-index]]）。
- 归档要立刻把卡从三类索引里摘除，不能只打标记留给每条查询自己过滤（[[problems-task-management-archive-shrinks-indexes]]）。
- 列本身就是工作流的状态节点，不给卡片另开一个可能和列脱节的 status 字段（[[problems-task-management-list-is-workflow-state]]）。
- 加清单不碰位置维护或工作流转移的任何一行代码——只有会影响索引的字段才需要经过统一的写入入口（[[problems-task-management-checklist-proves-extension]]）。

**题解**：[[solution-task-management]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
