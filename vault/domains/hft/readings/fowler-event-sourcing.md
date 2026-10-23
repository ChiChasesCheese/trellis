---
nodes: [architecture.sequencer-journal, architecture.simulation]
url: https://martinfowler.com/eaaDev/EventSourcing.html
---
# 事件溯源（Event Sourcing）

把状态的每一次变化记录成事件，状态由事件回放得到的模式。

**读的时候提取：**
- 事件日志 + 回放能带来什么：审计、调试、重建。
- 确定性回放需要什么前提。

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/eaaDev/EventSourcing.html)

## Archived copy
![[fowler-event-sourcing-clip]]
%% trellis:end %%
