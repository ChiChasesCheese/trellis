---
id: bagu-bulkhead-1-pool-vs-semaphore
node: b.protect.bulkhead
type: qa
step: 1
---
## Q
**隔离（舱壁）· 线程池隔离与信号量隔离**｜追问

面试官：「风控、优惠券、积分三个下游共用一个线程池，风控一慢全挂了。怎么隔离？」

## A
**基本回答。** 隔离（bulkhead，舱壁）：多个下游共用一个线程池时，一个变慢会占满所有线程，别的下游也没线程可用。线程池隔离是每个下游一个独立有限线程池，慢依赖只耗尽自己的池，还能设超时中断，代价是线程多、上下文切换多，所以只对慢而不稳的依赖用；信号量隔离只用计数器限制并发数，不开新线程、不能超时中断，开销小，适合本地缓存这类快速调用。池大小按利特尔定律：线程数 ≈ 目标 QPS × 依赖 p99 延迟，再留余量。更大粒度还有：不同业务用不同数据库连接池，核心与非核心分开部署，按租户单元化，离线与在线分资源。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="6" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">没隔离：共用一个池</text>
<text x="190" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">隔离：各用各的池</text>
<rect x="6" y="26" width="144" height="126" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="78" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="78" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共用线程池</text>
<rect x="16" y="54" width="124" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">风控（慢，占满）</text>
<rect x="16" y="88" width="124" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">优惠券：没线程了</text>
<rect x="16" y="122" width="124" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">积分：没线程了</text>
<rect x="190" y="26" width="144" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">风控池</text>
<text x="262" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">慢，只耗自己</text>
<rect x="190" y="70" width="144" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="84.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">优惠券池</text>
<text x="262" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正常</text>
<rect x="190" y="114" width="144" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">积分池</text>
<text x="262" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正常</text>
<text x="8" y="178" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">线程池隔离：独立线程、可超时中断，线程多</text>
<text x="8" y="196" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">信号量隔离：只限并发数，不开新线程</text>
<text x="8" y="218" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">池多大：线程数 ≈ QPS × p99 延迟</text>
<text x="8" y="236" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">500 QPS × 0.1 s = 50 个线程</text>
</svg>
左边风控变慢占满共用池，其余两个下游没线程；右边各用各的池，只有风控受影响。
**业务场景。** 交易服务共用一个 20 线程池，风控平时 100 毫秒、变慢成 5 秒，每秒 100 个请求，不到一秒线程就被占满，优惠券和积分排队超时；隔离成风控池 10、优惠券池 5、积分池 5 后只有风控被拒绝。算池大小：风控 500 QPS、p99 100 毫秒，需 500 × 0.1 = 50 个线程再留余量。
**容易错。**
- **给所有下游都开线程池。**
- **以为信号量隔离能超时中断。**
- **只做线程池隔离：** 连接池、部署、数据库也要隔离。
