%% trellis:begin %%
# 分布式基础
*B 其余知识点*

分布式锁、CAP、共识、一致性哈希、全局 ID、RPC 与网关。

## Topics
- [[domains/bagu/map/b.distributed.lock-choice|Redis 锁、ZooKeeper 锁、数据库锁怎么选]]
- [[domains/bagu/map/b.distributed.lock-zookeeper|用 ZooKeeper 实现分布式锁与 ZooKeeper 基础（临时顺序节点, Watch）]]
- [[domains/bagu/map/b.distributed.fencing-token|Fencing Token、租约与脑裂防护]]
- [[domains/bagu/map/b.distributed.consensus|共识算法：Raft、Paxos、ZAB 与拜占庭/Gossip（了解级）]]
- [[domains/bagu/map/b.distributed.consistent-hashing|一致性哈希与虚拟节点（Consistent Hashing）]]
- [[domains/bagu/map/b.distributed.distributed-id|全局唯一 ID：雪花、号段、UUID（Snowflake, Leaf）]]
- [[domains/bagu/map/b.distributed.rpc-gateway-lb|RPC、API 网关与负载均衡（RPC vs HTTP, Gateway, Load Balancing）]]
- [[domains/bagu/map/b.distributed.microservice-governance|微服务拆分与治理：拆分粒度、注册发现、配置中心、分布式 Session]]
- [[domains/bagu/map/b.distributed.multi-region|多区域：数据驻留与归属区域写入（Multi-Region, Home Region）]]
%% trellis:end %%

## Notes
