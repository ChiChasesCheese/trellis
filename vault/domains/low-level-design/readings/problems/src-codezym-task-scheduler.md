---
nodes: [problems.components.task-scheduler]
url: https://github.com/prsnt558908/CodeZymSolutions/tree/main/q22_job_scheduler
tags: [no-archive]
---
# CodeZymSolutions（镜像 codezym.com）— Job Scheduler（q22）

值得读，同样要先说清它解决的是哪个问题：这道"job scheduler"和本题解的"task scheduler"
名字相近，实际是**按能力把作业指派给机器**（`assignMachineToJob` 按机器的 `capabilities`
挑一台负载最轻或完成数最多的机器）——是一个调度算法题（scheduling policy / load
balancing），不涉及时间、不涉及延时或周期执行、没有堆。真正和本题解可比的地方只有一处：
它的 `register_criterion(code, key_fn)` 允许调用方注入一个新的选择策略而不改
`assignMachineToJob` 的任何一行，这和本题解"优先级只是堆排序键里多一栏，加它不改
`pop_due`"是同一种"扩展点设计在数据结构里，而不是设计成新增分支"的思路，值得对照着看。
这道题的核心数据结构是一个按机器分组的候选集合加 `min(key=...)`，不是按时间排序的堆，
所以"到期"与"取消"这两个本题解真正的难点，在这道题里都不存在。
