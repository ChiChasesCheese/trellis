---
id: hi-c-sd-redis-n12-ratelimit-sliding
node: sd.deep-dives.redis.notes
type: qa
step: 12
---
## Q
**Redis · 限流：滑动窗口**｜摘要 · 必会

需要滑动窗口限流时用什么结构？每个请求的步骤是什么？

## A
- **结构：** 每个用户一个有序集合，请求时间戳当分数。
- **每个请求的步骤：** `ZREMRANGEBYSCORE` 删除窗口之外的旧条目 → `ZCARD` 数剩下多少 → 少于 N 就 `ZADD` 加入新请求。
- **原子性：** 整个序列写成 Lua 脚本，一次执行，避免并发请求交错。

```mermaid
flowchart TB
    Q["请求到达"] --> L
    subgraph L["Lua 脚本：一次原子执行"]
        R["ZREMRANGEBYSCORE<br/>删窗口外旧条目"] --> C["ZCARD 数剩下多少"]
        C --> D{"少于 N？"}
        D -->|"是"| A["ZADD 时间戳，放行"]
        D -->|"否"| X["拒绝"]
    end
```
