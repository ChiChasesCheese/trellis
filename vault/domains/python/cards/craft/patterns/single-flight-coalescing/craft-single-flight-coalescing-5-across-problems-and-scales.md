---
id: craft-single-flight-coalescing-5-across-problems-and-scales
node: craft.patterns.single-flight-coalescing
type: qa
step: 5
---
## Q
**单飞合并 · 缓存回源、幂等转账、通知去重里的同一个动作，放大到 CDN 和分布式锁**｜模式

TTL 缓存的 `get_or_load`、幂等转账、通知服务的去重，看起来是读、写、发送三件不同的事。它们共享什么？放到多台机器上，这个「同一个 key 只做一次」要怎么做？

## A
**要点。** 同一个动作：对每个 key 维护「正在做」的登记；第一个到达的占位并真正去做，之后到达的看见登记就不再做。三者的差别是后到者的行为（等并共享结果 / 等并返回第一次的结果 / 返回占位），以及失败时怎么交接。

```python
# ttl-cache.get_or_load：登记 key → Event，领跑者先写缓存后唤醒
waiter = self._inflight.get(key); leader = waiter is None
# idempotent-transfer：登记 (client, key) → 记录，等待 rec.done，返回 rec.result
if not rec.done.wait(self._wait): raise StillRunning(...)
# notification-service：登记 key → (时间, 结果)，重复则返回占位
return entry[1] if entry[1] is not None else _PENDING
```

**见于。** ttl-cache、idempotent-transfer、notification-service。

**不变的。** 「登记 + 判断是不是第一个」必须在同一个临界区；要有失败时的交接（`finally` 移交，或可被接手的租约）；登记表自己有生命周期（过期、容量上限）。**变化的。** 后到者等还是返回占位；是否存结果；要不要比对请求指纹。

**信号。** 需求里出现「同一个 key 的并发请求」「重复提交」「热点」「客户端会重试」「只能执行一次」；或者监控里出现缓存失效瞬间后端的流量尖峰。

**尺度对照。** 单进程：锁 + `Event`。多机：每台机器的单飞只合并本机的请求，N 台机器同时过期仍会回源 N 次，所以要再加一层：CDN 和反向代理的请求合并（collapsed forwarding，同一个 URL 的并发回源请求在边缘合并）；或者用共享存储里带过期时间的租约（lease）争夺领跑者，Facebook 的 memcache 用 lease 抑制踩踏就是这种用法；幂等键则落在带唯一约束的存储里，保存首次请求的结果供重试读取（Stripe 的 Idempotency-Key 是这个思路）。变化：领跑者可能死掉，登记必须带过期时间，且接手后旧领跑者的迟到写入要被拒绝，单机里 `finally` 就能解决的交接，到了多机变成租约和 fencing（用递增的令牌拒绝过期持有者）。
