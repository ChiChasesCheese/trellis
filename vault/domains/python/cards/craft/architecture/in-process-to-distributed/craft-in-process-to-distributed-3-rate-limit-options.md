---
id: craft-in-process-to-distributed-3-rate-limit-options
node: craft.architecture.in-process-to-distributed
type: qa
step: 3
---
## Q
**从单进程到分布式 · 限流器扩到多台机器有哪几种做法，各错在哪里**｜架构

进程内限流器按 key 分片，每个分片一把锁，限额是精确的。服务扩成 4 台后，总限额还是每秒 8 个请求。三种常见做法：每个请求都去共享的 Redis 计数、每台机器分到 `限额/4` 的本地配额、各机器本地计数再定期同步。它们的误差来源是什么？

## A
**要点。** 精确性与延迟、可用性互换：集中计数（Redis，通常用 Lua 脚本保证检查加扣减是原子的）精确，但每个请求多一次网络往返，且限流器本身成了依赖；本地配额没有网络调用，但流量不均时某台早早用完而别的机器还有空，误差来自负载倾斜；定期同步是中间路线，误差来自两次同步之间各机器看不到彼此。

```python
def global_limit(requests: list[str], limit: int) -> int:
    return min(len(requests), limit)                       # 集中计数：精确

def local_quota(requests: list[str], limit: int, servers: list[str]) -> int:
    quota = {s: limit // len(servers) for s in servers}    # 每台分得 limit/N
    allowed = 0
    for s in requests:
        if quota[s] > 0:
            quota[s] -= 1
            allowed += 1
    return allowed

servers = ["s1", "s2", "s3", "s4"]
even = [servers[i % 4] for i in range(8)]              # 请求均匀
skew = ["s1"] * 8                                      # 请求全打到 s1
print("限额 8，均匀流量: 集中", global_limit(even, 8), " 本地配额", local_quota(even, 8, servers))
print("限额 8，倾斜流量: 集中", global_limit(skew, 8), " 本地配额", local_quota(skew, 8, servers))
```

限额 8，4 台；8 个请求，一次均匀打到四台，一次全打到 s1，实际输出：

```
限额 8，均匀流量: 集中 8  本地配额 8
限额 8，倾斜流量: 集中 8  本地配额 2
```

**为什么。** 进程内的分片锁对应「按 key 分片到不同 Redis 实例」：竞争被分散到不同的分片上，同一个 key 永远落到同一个分片，状态不必在分片间同步。

**代价。** 选哪种取决于允许多大的误差：计费类限额要精确，用集中计数；防刷类允许超一点，本地配额加同步就够，并且要明确限流器挂了时是放行还是拒绝（fail-open 还是 fail-closed）。
