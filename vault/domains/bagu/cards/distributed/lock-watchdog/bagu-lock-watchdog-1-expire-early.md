---
id: bagu-lock-watchdog-1-expire-early
node: a.distributed.lock-watchdog
type: qa
step: 1
---
## Q
**锁过期了业务没完 · 怎么办**｜必会

面试官：「锁的 TTL 设了 30 秒，但扣款流程偶尔因下游慢超过 30 秒，锁过期了业务还没执行完，怎么办？」

## A
**基本回答。** TTL 没有对所有情况都合适的值：设短了，业务没做完锁就提前释放；设长了，持有者崩溃后别人要等很久。常见做法是自动续期（看门狗，watchdog）：持有者还活着每隔 TTL 的三分之一左右跑一次 Lua，先确认 value 还是自己的才 `PEXPIRE`，以免把别人的锁续上；崩溃了就不再续期，锁自然过期。Redisson 默认 TTL 30 秒、每 10 秒续一次，只在加锁没指定 `leaseTime` 时启用，业务结束要停止续期并释放锁。同时下游写入要有条件更新或版本号兜底。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">业务要跑 45 秒，锁的 TTL 是 30 秒</text>
<text x="8" y="36" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">没有续期</text>
<rect x="20" y="42" width="297" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="168.5" y="56" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 的业务</text>
<rect x="20" y="66" width="198" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="119" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁 30 秒</text>
<line x1="218" y1="38" x2="218" y2="100" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="224" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">锁到期</text>
<text x="224" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 抢到锁</text>
<text x="20" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">之后两个持有者同时在写</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">看门狗每 10 秒续一次</text>
<rect x="20" y="154" width="297" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="168.5" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 的业务</text>
<rect x="20" y="178" width="297" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="168.5" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁一直在</text>
<line x1="86" y1="196" x2="86" y2="204" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="218" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10 秒</text>
<line x1="152" y1="196" x2="152" y2="204" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="152" y="218" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">20 秒</text>
<line x1="218" y1="196" x2="218" y2="204" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="218" y="218" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">30 秒</text>
<line x1="284" y1="196" x2="284" y2="204" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="284" y="218" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">40 秒</text>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A 崩了：续期停止，TTL 到期，锁自然释放</text>
</svg>
上半没有续期：锁到 30 秒就没了，业务还要再跑 15 秒，B 抢进来，之后两个持有者同时在写。下半有看门狗：每 10 秒把 TTL 重新延长，业务做完前锁一直在；A 崩了续期一停，TTL 到期，锁自然放掉。
**容易错。**
- **以为 TTL 设得足够长就行：** 太长，崩溃后别人要白等很久；而且总有比它更慢的情况。
- **续期不先确认锁是不是自己的：** 会把别人的锁续上，让它永远不过期。
- **业务结束忘了停止续期：** 续期线程还在跑，锁就一直不过期。
- **以为有了看门狗就万无一失：** 它救不了进程暂停，下游还要有条件更新或版本号兜底。
**业务场景。** 扣款流程偶尔因下游慢要跑 45 秒，锁 TTL 30 秒：没有续期时 t=31 秒 B 加锁成功，t=45 秒 A 才写完，同一笔账被处理两次。有看门狗每 10 秒续一次，A 做完前锁不丢；A 在 t=25 秒崩了，最后一次续期在 t=20 秒，锁到 t=50 秒自然过期，B 才能拿到。
