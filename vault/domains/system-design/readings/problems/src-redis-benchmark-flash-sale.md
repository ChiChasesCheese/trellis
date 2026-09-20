---
nodes: [problems.commerce.flash-sale]
url: https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/
---
# Redis benchmark

值得读：官方基准测试给出了具体、可引用的吞吐数字——裸机服务器不开 pipelining 时 `SET`
约 180,180 请求/秒，开 16 条 pipelining 后可达约 153.6 万请求/秒。本题用这组数字精确计算
了单个热 key 相对裸露购买峰值（10 万 QPS）的安全边际只有约 1.8 倍，据此论证准入控制不是
可选项而是必需品；比大多数题解文章更具体的地方是给出了"什么时候真的需要给热 key 分片"的
量化判据，而不是想当然地说"Redis 单实例肯定够用"或"必须分片"两个极端。

%% trellis:begin %%
## Source
[Open the original ↗](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/)

## Archived copy
![[src-redis-benchmark-leaderboard-clip]]
%% trellis:end %%
