---
id: hi-pt-tt-cache-consistency-hot-keys-5-replica-lag
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 8
---
## Q
**缓存一致性与热点 Key · 从库延迟与版本号保护**｜追问 · 出自：缓存一致性与热点 Key › 深入 4

即使 A 已删除缓存，回填为什么还会写入旧值？有哪些办法防止旧版本覆盖新版本？

## A
**问题。** 回填读从库，而从库尚未同步最新数据，B 读到旧值回填，缓存里的旧值留到 TTL。
**办法。** 对刚失效的 key，回填读主库；失效消息延迟一个主从延迟上界再删一次（延迟双删，用延迟消息而非线程睡眠）；缓存值带版本号，回填用 Lua 脚本比较，旧版本不覆盖新版本。
```lua
if (not cur) or tonumber(cur) < tonumber(ARGV[1]) then ... end
```
