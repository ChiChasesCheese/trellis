---
id: bagu-distributed-limit-1-redis-lua-quota
node: b.protect.distributed-limit
type: qa
step: 1
---
## Q
**分布式限流 · 多实例共享配额、Redis 故障怎么办**｜追问

面试官：「多个网关实例共享某商户 1000 QPS 的配额，怎么限？限流用的 Redis 挂了呢？」

## A
**基本回答。** 商户 1000 QPS 是所有网关实例合计，各自数会各放行 1000。Redis + Lua 固定窗口：`INCR` 计数，返回 1（窗口第一个请求）才设 `EXPIRE`，超阈值返回 0。`INCR` 和 `EXPIRE` 必须在同一个 Lua 里原子执行，否则 `INCR` 后崩溃，key 永不过期、计数一直涨，用户被永久限流。滑动窗口用 ZSet（score 是时间戳，`ZREMRANGEBYSCORE` 删窗口外的、`ZCARD` 判断、`ZADD` 记录），不会像固定窗口在边界突刺（末尾加下一窗口开头可放行接近两倍）；令牌桶用 Lua 存上次补充时间和当前令牌数。代价是每个请求一次 Redis 往返，限流器成热点；另一条路是配额分片：全局 10,000 QPS 分给 10 个实例各 1000，本地令牌桶限流，每秒按实际流量重新分配，没有网络开销、精度略低。Redis 挂了：fail-open（放行保可用，退化为本地限流，普通 API）或 fail-closed（拒绝保安全，资金、防刷类）。后端仍要自保护，内部调用和重试风暴也会压垮服务。
**2026 亮点。** Redis 8.8 起固定窗口可用原生命令 `INCREX` 一条完成（如 `INCREX key BYINT 1 UBOUND 100 EX 60 ENX`，实际增量为 0 即拒绝），不再需要 Lua；仍是固定窗口有边界突刺，多活下各副本只按本地值校验上限，合并后可能超限。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="6" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">方案一：Redis + Lua</text>
<text x="190" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">方案二：配额分片</text>
<rect x="6" y="30" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 1</text>
<line x1="62" y1="44" x2="81" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="88.0,44.0 81.0,47.2 81.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="66" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 2</text>
<line x1="62" y1="80" x2="81" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="88.0,80.0 81.0,83.2 81.0,76.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="102" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 3</text>
<line x1="62" y1="116" x2="81" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="88.0,116.0 81.0,119.2 81.0,112.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="88" y="30" width="84" height="112" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="130" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INCR</text>
<text x="130" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">EXPIRE</text>
<text x="130" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（Lua 原子）</text>
<rect x="190" y="30" width="144" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全局 10000 QPS</text>
<rect x="190" y="92" width="40" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例1</text>
<text x="210" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000</text>
<line x1="210" y1="62" x2="210" y2="92" stroke-width="1.2" stroke="currentColor"/>
<rect x="242" y="92" width="40" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例2</text>
<text x="262" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000</text>
<line x1="262" y1="62" x2="262" y2="92" stroke-width="1.2" stroke="currentColor"/>
<rect x="294" y="92" width="40" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="314" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例3</text>
<text x="314" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000</text>
<line x1="314" y1="62" x2="314" y2="92" stroke-width="1.2" stroke="currentColor"/>
<text x="190" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">本地令牌桶限流，每秒</text>
<text x="190" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按实际流量重新分配</text>
<text x="6" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个请求一次往返</text>
<text x="6" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">限流器成热点</text>
<text x="6" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Redis 挂了：</text>
<rect x="6" y="206" width="160" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="225" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fail-open：放行保可用</text>
<rect x="174" y="206" width="160" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="225" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fail-closed：拒绝保安全</text>
<text x="6" y="256" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">普通 API 常 fail-open；资金、防刷类 fail-closed</text>
</svg>
左边三个网关共用一个 Redis 计数；右边全局配额切成 10 份各自本地限流；底部是 Redis 挂掉的两种选择。
**代码。**
```lua
local current = redis.call("INCR", KEYS[1])
if current == 1 then
  redis.call("EXPIRE", KEYS[1], ARGV[1])   -- 首次计数才设窗口时长
end
if current > tonumber(ARGV[2]) then return 0 end   -- 超限
return 1
```
**业务场景。** 阈值缩成 3、窗口 1 秒：网关 1 的 `INCR` 得 1 设 `EXPIRE`，网关 2、3 得 2、3 放行，网关 1 再来得 4 返回 0；1 秒后 key 消失从头数。
**容易错。**
- **INCR 和 EXPIRE 分开写。**
- **Redis 故障不设预案：** 要事先定 fail-open 还是 fail-closed。
- **只在网关限流。**
