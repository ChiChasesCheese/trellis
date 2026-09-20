---
nodes: [problems.booking.meeting-scheduler]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/009-meeting-scheduler
tags: [no-archive]
---
# 009-meeting-scheduler

值得读：五语言并排（含 Python）、附带分阶段的 boilerplate 与 `DESIGN.md`，仓库没有 LICENSE
文件。Python 实现里时间用裸整数时间戳而不是 `datetime`，冲突判断和本文的半开区间逻辑一致，但
配房逻辑做成了 `FirstAvailable`/`BestFit`/`PriorityBased` 三个只有一个方法的策略类，`bookMeeting`
没有任何锁保护，也没有周期会议、多人找空档、时区的建模。本文在这三点上明确反着做，见「关键设计
决策」决策二、六。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/009-meeting-scheduler)
%% trellis:end %%
