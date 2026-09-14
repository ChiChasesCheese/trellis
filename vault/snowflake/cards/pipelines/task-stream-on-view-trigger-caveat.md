---
id: task-stream-on-view-trigger-caveat
node: pipelines.task-conditional-execution
type: qa
source: snowflake-docs
---
## Q
一个触发式任务依赖某个视图上的流，视图带有过滤条件，只关心 `status = 'error'` 的行。为什么任务在大量无关写入时也频繁被触发？

## A
当任务由视图上的流触发时，视图查询所引用的任何表发生变化都会触发任务，无论视图中有什么连接、聚合或过滤条件。也就是说，触发判断看的是底层表是否有变更，而不是经过视图过滤后是否真有相关行，所以无关写入也会唤醒任务。需要更精确的触发时，应让流直接建在只含相关数据的表上，或在任务主体里再次判断。
