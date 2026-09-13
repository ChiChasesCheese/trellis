---
id: runtime-openresty-shared-dict
node: runtimes.lua-openresty
type: qa
---
## Q
Lua code stores a purge generation in a module-level table. Some requests see the update and others do not. Explain and fix.

## A
Nginx workers are separate OS processes; each has its own Lua VM and module globals. A module table is worker-local, so updates diverge. Use `ngx.shared.DICT` for small cross-worker state with atomic operations, or an external store/control-plane broadcast for durable fleet-wide state. Shared dict is finite local memory with eviction and no cross-host replication, so it cannot be the sole source of truth for global purge.

## Q zh
Lua 把 purge generation 存在 module-level table 中，部分请求看到更新，另一些看不到。解释原因并修复。

## A zh
Nginx worker 是独立 OS process；每个都有自己的 Lua VM 和 module global。module table 只在单个 worker 内，因此更新会分叉。小型跨 worker 状态可使用带 atomic operation 的 `ngx.shared.DICT`；durable fleet-wide state 应使用 external store 或 control-plane broadcast。shared dict 只是有限的本机内存，会 eviction，也不跨 host replication，因此不能成为 global purge 的唯一 source of truth。
