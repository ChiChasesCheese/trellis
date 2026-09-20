---
nodes: [problems.foundations.job-scheduler]
url: https://dropbox.tech/infrastructure/asynchronous-task-scheduling-at-dropbox
tags: []
---
# How we designed Dropbox's ATF — an async task framework

值得读：Dropbox 生产系统 ATF 的第一手设计文档——用索引查询代替全表扫描找到期任务、
`Enqueued→Claimed` 状态机加心跳超时防止重复领取、9,000 任务/秒和 95% 任务 5 秒内
开始执行的真实披露数字。本题解在此基础上多加了一层单调递增的 fencing token（ATF
本身没有披露这个机制），并用分层时间轮取代了 ATF 依赖数据库索引扫描的发现方式。

%% trellis:begin %%
## Source
[Open the original ↗](https://dropbox.tech/infrastructure/asynchronous-task-scheduling-at-dropbox)

## Archived copy
![[src-dropbox-job-scheduler-clip]]
%% trellis:end %%
