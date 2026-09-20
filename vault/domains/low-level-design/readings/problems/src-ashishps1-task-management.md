---
nodes: [problems.social.task-management]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/task-management-system.md
---
# Designing a Task Management System

值得读：需求列表覆盖创建/更新/删除任务、指派、提醒、按条件搜索、并发访问，可以用来核对
有没有漏项。它的 Python 参考实现把状态做成了教科书式的状态模式——`TaskState` 是一个
`ABC`，`TodoState`/`InProgressState`/`DoneState` 各是一个子类，且状态集合硬编码成
TODO/IN_PROGRESS/DONE/BLOCKED 四段，非法转移时用 `print` 打印一句提示而不是抛异常，调用方
因此没有办法用程序判断这次转移到底成没成功。这正是本文"关键设计决策"里明确讨论并拒绝的
两件事——每个状态一个类、以及硬编码的三/四段式——的一个真实反例；本文用一张按看板各自声明
的转移表取代它，非法转移抛 `IllegalTransitionError`。它的 `TaskList` 也没有位置的概念，
任务只是 `append` 进一个列表，没有讨论"插入到中间"要付出的代价。
