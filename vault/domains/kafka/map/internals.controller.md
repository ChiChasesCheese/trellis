%% trellis:begin %%
# 控制器（controller）的角色与选举
*集群内部机制：控制器、复制协议与存储*

理解控制器在集群中承担的元数据管理与首领选举职责，以及控制器自身如何被选出。

**Requires:** [[domains/kafka/map/core.cluster-roles|broker、集群与多集群架构中的角色分工]]

## Readings
- [[kafka-6-1-cluster-membership|集群的成员关系：broker如何注册与被发现]]
- [[kafka-6-2-controller-kraft|控制器的选举与职责，以及KRaft带来的变革]]

## Cards (5)
1. [[kafka-internals-controller-role]]
2. [[kafka-internals-controller-election]]
3. [[kafka-internals-controller-epoch-zombie]]
4. [[kafka-internals-controller-leader-election-flow]]
5. [[kafka-internals-controller-startup-load-latency]]
%% trellis:end %%

## Notes
