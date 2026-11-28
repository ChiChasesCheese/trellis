---
id: bagu-redlock-3-kleppmann
node: a.distributed.redlock
type: qa
step: 3
---
## Q
**Kleppmann 的批评 · Antirez 的回应**｜必会

面试官：「RedLock 被 Kleppmann 批评了什么？Antirez 又怎么回应的？」

## A
**基本回答。** Kleppmann（2016）三点批评：一，算法假设网络延迟、进程停顿、时钟漂移都有上界，现实中 GC 停顿、时钟跳变、包延迟会打破这些假设；二，没有 fencing token，持有者暂停后仍会出现两个客户端都认为自己持锁；三，只要效率，单实例锁就够，RedLock 过重，要正确性，它又不够，该用有共识算法的系统。Antirez 回应：时钟问题可用单调时钟和多数派检查缓解；加锁之后的进程停顿，任何锁都有同样问题。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="6" y="6" width="160" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="86" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kleppmann（2016）</text>
<rect x="174" y="6" width="160" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Antirez 的回应</text>
<rect x="6" y="40" width="160" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="62.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">假设延迟、停顿、</text>
<text x="86" y="77.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时钟漂移都有上界</text>
<rect x="174" y="40" width="160" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="62.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时钟：用单调时钟</text>
<text x="254" y="77.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">和多数派检查缓解</text>
<rect x="6" y="100" width="160" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有 fencing token</text>
<text x="86" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">暂停后两人都持锁</text>
<rect x="174" y="100" width="160" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加锁后的进程停顿</text>
<text x="254" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">是所有锁共同的问题</text>
<rect x="6" y="160" width="160" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="182.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要效率：单实例够</text>
<text x="86" y="197.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要正确：用共识系统</text>
<rect x="174" y="160" width="160" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="182.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分歧：要的是安全性</text>
<text x="254" y="197.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还是尽力而为的效率</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">现实风险：GC 停顿、NTP 时钟跳变、包延迟</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">更稳妥：配合 fencing token</text>
<text x="8" y="272" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TTL 过期用的不是单调时钟，调系统时间会出事</text>
</svg>
左列是 Kleppmann 的三点批评，右列是对应的回应：时钟问题可以缓解，进程停顿是所有锁共有的，第三点其实是一个选型分歧，看你要的是安全性还是效率。
**容易错。**
- **以为 RedLock 有多数派就绝对安全：** 它依赖时间假设，时钟跳变和进程停顿都能打破。
- **以为 Antirez 完全驳倒了批评：** 他指出加锁后的进程停顿是所有锁共有的问题，但没有 fencing token 这一点并没有消失。
- **把争论当成谁对谁错：** 本质是你要安全性还是效率，需求不同，结论不同。
- **以为单调时钟只是理论：** 系统时间被调整是真实发生的事，Redis 的 TTL 过期用的不是单调时钟。
**业务场景。** 机器 NTP 校时把系统时间向前拨了几秒，Redis 中的锁提前过期，两个实例同时处理同一个用户的积分结算。
