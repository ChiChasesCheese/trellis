---
id: bagu-lock-redis-setnx-2-nx-px-value
node: a.distributed.lock-redis-setnx
type: qa
step: 2
---
## Q
**加锁命令 · NX 与 PX 为什么同一条、value 为什么随机**｜必会

面试官：「为什么 NX 和 PX 必须在同一条命令里？value 为什么要放随机值，固定放个 1 不行吗？」

## A
**基本回答。** 先 `SETNX` 再 `EXPIRE` 是两条命令，中间进程崩溃，key 就没有过期时间，锁永远释放不了，形成死锁（`TTL k` 返回 -1）；`SET key uuid NX PX 30000` 是一条原子命令（要么一起完成，要么都不发生）。value 放每次加锁唯一的随机值，是为了释放时能确认「这把锁还是我的」。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分成两条命令：中间可以崩</text>
<rect x="6" y="24" width="110" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SETNX k v</text>
<text x="61" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成功</text>
<line x1="116" y1="44" x2="205" y2="44" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="205" y1="44" x2="207" y2="44" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="214,44 207,47.2 207,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="160" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩</text>
<rect x="214" y="24" width="120" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="274" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">EXPIRE k 30</text>
<text x="274" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">永远没执行</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">key 没有过期时间：TTL = -1，永不释放</text>
<line x1="8" y1="108" x2="332" y2="108" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="8" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一条命令：加锁和设过期时间一起完成</text>
<rect x="6" y="142" width="328" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET k uuid NX PX 30000</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要么都成，要么都没发生，不会死锁</text>
</svg>
上半是两条命令：`SETNX` 成功后、`EXPIRE` 之前崩了，key 就永不过期。下半是一条 `SET ... NX PX`，加锁和设过期时间同时完成。
**容易错。**
- **以为先 SETNX 再 EXPIRE 也行：** 两条命令之间可以崩，没有过期时间的锁等于死锁。
- **value 随便放个 1：** 锁过期后无法确认「这把锁还是不是我的」，会误删别人的锁；放每次加锁唯一的随机值，UUID 或「客户端 ID:线程 ID」（便于重入），释放时 Lua 比较一致才删。
- **以为只要有 TTL 就不会误删：** 误删正是发生在 TTL 到期之后，所以释放时才要比对。
- **用时间戳当锁值抢锁：** 依赖各机器时钟，时钟不一致会让锁被提前抢走。

**业务场景。** 退款任务处理超过 30 秒，锁过期被另一个实例接手，原实例做完后直接 `DEL`，把新持有者的锁也删了，第三个请求随即进入，三个实例同时对同一笔订单退款。
