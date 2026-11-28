---
id: bagu-lock-watchdog-2-redisson
node: a.distributed.lock-watchdog
type: qa
step: 2
---
## Q
**Redisson 看门狗 · 默认时长、什么时候不续期**｜必会

面试官：「Redisson 的看门狗是怎么续期的？默认多长？什么时候不会续期？」

## A
**基本回答。** 调用 `lock()` 或 `tryLock()` 且不指定 `leaseTime` 时，锁的默认时长是 `lockWatchdogTimeout`，即 30 秒。加锁成功后启动定时任务，每 10 秒（时长的三分之一）检查持有线程，还在就把过期时间重置回 30 秒（续期脚本先用 `HEXISTS` 确认锁仍是自己的再 `PEXPIRE`，不是就取消续期；默认值可通过 `Config` 的 `lockWatchdogTimeout` 毫秒数调整）。进程崩溃就不再续期，最多 30 秒后锁过期。显式指定了 `leaseTime`，就不会续期，到期即释放。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">锁的剩余 TTL 随时间的变化</text>
<line x1="30" y1="36" x2="30" y2="150" stroke-width="1.2" stroke="currentColor"/>
<line x1="30" y1="150" x2="322" y2="150" stroke-width="1.2" stroke="currentColor"/>
<text x="34" y="46" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">30 秒</text>
<polyline points="30,50 84,83.3 84,50 138,83.3 138,50 300,150" stroke-width="1.5" fill="none" stroke="currentColor"/>
<line x1="30" y1="83.3" x2="322" y2="83.3" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="40" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚线处续回 30 秒</text>
<text x="172" y="57.7" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">t=25 崩溃</text>
<circle cx="165.0" cy="66.7" r="3" style="fill:var(--accent,#3b6fd4)"/>
<text x="30" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="84" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10 秒</text>
<text x="138" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">20 秒</text>
<text x="300" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">50 秒</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩溃后不再续期，最多 30 秒锁自然过期</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">指定了 leaseTime：不启动看门狗，到期即释放</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">间隔取三分之一：连漏两次续期也有余量</text>
</svg>
纵轴是锁剩余的 TTL，倒计时从 30 秒往下走，走到 20 秒（也就是过去 10 秒）就被拨回 30 秒。t=25 秒持有者崩溃，没人再续，倒计时一路走到 0。
**容易错。**
- **指定了 `leaseTime` 还以为会续期：** 不会，到期即释放。
- **以为看门狗保证只有一个持有者：** 它只保证线程还活着时锁不过期；进程被暂停时续期线程也停，锁照样过期。
- **短操作也走默认看门狗：** 多了续期的开销，短操作建议指定 `leaseTime`。
- **以为间隔越短越好：** 太频繁只会增加 Redis 的压力；三分之一已经能容忍漏掉两次续期。

**业务场景。** 日终批处理用 `lock()` 默认加锁，跑 5 分钟，看门狗一直续期，锁不会中途丢；而一个只需几百毫秒的发券操作，指定 `leaseTime` 为 10 秒，到期自动释放，不引入续期开销。
