---
id: hi-c-sd-distributed-rate-limiter-b01-lua-token-bucket
node: sd.problem-breakdowns.distributed-rate-limiter.beyond
type: qa
step: 1
---
## Q
**分布式限流器 · 令牌桶的 Lua 脚本与 Python 调用**｜拓展 · 加分

把"读、算、写"放进一个 Lua 脚本，具体怎么写？时钟该用谁的，键什么时候过期？

## A
```python
import redis

# 令牌桶：读、算、写在 Redis 里一次原子完成
TOKEN_BUCKET = """
local key      = KEYS[1]
local capacity = tonumber(ARGV[1])   -- 桶容量（允许的突发）
local rate     = tonumber(ARGV[2])   -- 每秒补充的令牌数
local now_ms   = tonumber(ARGV[3])   -- 当前毫秒；生产里改为 redis.call('TIME')
local cost     = tonumber(ARGV[4])

local state  = redis.call('HMGET', key, 'tokens', 'ts')
local tokens = tonumber(state[1])
local ts     = tonumber(state[2])
if tokens == nil then               -- 新客户端从满桶开始
  tokens, ts = capacity, now_ms
end

tokens = math.min(capacity, tokens + (now_ms - ts) / 1000 * rate)
local allowed = 0
if tokens >= cost then
  tokens = tokens - cost
  allowed = 1
end

redis.call('HSET', key, 'tokens', tokens, 'ts', now_ms)
-- 空闲够久桶会自己回满，这时键里没有信息量，可以过期
redis.call('PEXPIRE', key, math.ceil(capacity / rate * 1000) * 2)
return {allowed, tostring(tokens)}
"""

def make_limiter(r: redis.Redis):
    script = r.register_script(TOKEN_BUCKET)   # 内部走 EVALSHA，脚本正文只传一次
    def allow(key: str, capacity: int, rate: float, now_ms: int, cost: int = 1):
        ok, left = script(keys=[key], args=[capacity, rate, now_ms, cost])
        return bool(ok), float(left)
    return allow
```
- **验证：** 容量 3、每秒补 1 个，同一毫秒连发 5 次，结果是放行 3 次、拒绝 2 次；2 秒后再发，补回 2 个令牌，放行。
- **时钟用谁的：** 若由各网关传入时间，不同网关的时钟偏差会让补充量不一致。生产里在脚本里用 `redis.call('TIME')` 取 Redis 自己的时钟（Redis 5 起脚本按效果复制，允许读时间），所有网关就共用一个时间源。
- **过期时间：** 取"从空桶补满所需时间"的约两倍。再久未访问的桶一定已满，等价于不存在，删了也不影响结果，同时避免闲置键占满内存。
- **为什么用 EVALSHA：** 每次只传一个 40 字符的摘要，而不是整段脚本，省带宽；`register_script` 会在缺失脚本时自动补载入。
- **模式。** 把读改写做成服务端脚本：让数据所在的节点一次完成判断与更新，避免客户端往返中间被插入。
