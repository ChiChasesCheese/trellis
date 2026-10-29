%% trellis:begin %%
# Kubernetes workqueue：队列 + 待处理集合 + 处理中集合
*数据结构组合：开源框架里的类设计*

控制器的工作队列保证同一个 key 不重复排队、也不会被两个工人同时处理：一个先进先出队列、一个 dirty 集合、一个 processing 集合怎样配合；处理中又被改动的 key 怎样处理完再重新入队。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-k8s-workqueue-1-need]]
2. [[uth-compose-k8s-workqueue-2-parts]]
3. [[uth-compose-k8s-workqueue-3-code]]
4. [[uth-compose-k8s-workqueue-4-real]]
5. [[uth-compose-k8s-workqueue-5-interview]]
%% trellis:end %%

## Notes
