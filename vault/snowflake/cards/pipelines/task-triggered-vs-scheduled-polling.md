---
id: task-triggered-vs-scheduled-polling
node: pipelines.task-conditional-execution
type: qa
source: snowflake-docs
---
## Q
新数据到达时间不可预测的 ELT 流程，「定时任务 + `SYSTEM$STREAM_HAS_DATA` 检查」和「触发式任务（triggered task）」各有什么特点？

## A
定时任务加条件检查按固定节奏轮询：没有数据就跳过，但数据到达后要等到下一个调度点才会处理，延迟取决于调度间隔。触发式任务在流中出现新数据时就运行，免去了对数据源的频繁轮询，数据到达后立即处理，延迟更低。数据到达无规律且看重延迟时选触发式任务；希望处理节奏固定、批次可控时选定时加条件检查。
