---
nodes: [problems.components.task-scheduler]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/task-management-system.md
---
# awesome-low-level-design — Designing a Task Management System

值得读，但要先纠正一个名字上的误会：这篇题面挂着"任务管理系统"的名字，内容却是一个
**Jira/Trello 式的任务跟踪应用**——标题、指派人、状态（pending/in-progress/completed）、
按条件搜索、`TaskSortStrategy`——完全不涉及"在某个时刻或按某个周期自动执行一段代码"这件事，
本题解要写的调度引擎（延时、周期、取消、并发工作线程）在它里面没有对应物。这是搜索这个题目
时最容易踩的坑：题名相似，问题完全不同。它唯一和本题解相关的地方是 `TaskPriority` 枚举——
对照一下会发现，跟踪应用里的"优先级"只是给人看的一个展示字段，而本题解里的优先级是参与堆
排序的真实比较键，两者形似神离。它的 `TaskManager` 仍然用 `__new__` 单例，这一点和本站
其它题解里反复出现的反例一致。
