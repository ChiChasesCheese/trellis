---
id: bagu-tcc-4-hanging
node: a.idem.tcc
type: qa
step: 4
---
## Q
**TCC · 悬挂**｜必会

面试官：「Cancel 已经执行完，之后迟到的 Try 才到达，会发生什么？怎么防？」

## A
**基本回答。** 这叫悬挂（hanging）：迟到的 Try 若继续预留，资源永远没人 Confirm 或 Cancel。Try 先检查事务记录，发现该事务已有 Cancel 记录就拒绝执行。
**一句话记住。** 悬挂像退房手续都办完了，一份迟到的订房通知才送到前台：如果前台照单把房间占上，这个房间就永远空着，因为没人会来住，也没人会再来退。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 184">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① Cancel 先到</text>
<rect x="8" y="24" width="92" height="34" rx="3" stroke-width="1.2" fill="none" style="stroke:var(--dim,#6b7280)"/>
<text x="54" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xid 无记录</text>
<line x1="100" y1="41" x2="140" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,41.0 133.0,44.2 133.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="140" y="24" width="110" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="195" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CANCELLED</text>
<text x="8" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② 之后 Try 才到</text>
<rect x="140" y="100" width="110" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="195" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">迟到的 Try</text>
<line x1="195" y1="100" x2="195" y2="60" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="195.0,60.0 198.2,67.0 191.8,67.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="262" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">撞主键</text>
<text x="262" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">被拒绝</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">拒绝后，资源不会被永久冻结</text>
</svg>
先是 Cancel 到达，xid 的记录从「无」变成 CANCELLED；之后迟到的 Try 想插入 TRIED 记录，撞上同一个 xid 的主键，被拒绝，没有预留任何资源。
**讲明白。**
- **悬挂怎么发生的：**Cancel 已经执行完，之后迟到的 Try 才到达。网络延迟、重试都可能造成这种乱序。
- **为什么是个问题：**如果这个迟到的 Try 继续预留资源，这份资源永远不会有 Confirm 或 Cancel 来处理，因为事务早就结束了，资源就一直被占着。
- **怎么防：**Try 先检查事务记录，发现该事务已有 Cancel 记录就拒绝执行。
- **靠 CANCELLED 记录：**空回滚时写下的 `CANCELLED` 记录，正是防悬挂的依据。
- **主键撞键就是检查：**事务记录用 xid 做主键，Try 插入 `TRIED` 时撞键，就表示这个事务已经有记录了，Try 直接拒绝。
- **空回滚和悬挂是一对：**它们都因为 Cancel 先于 Try 到达。Cancel 先到时记录 `CANCELLED`，既处理了空回滚，也为拒绝之后迟到的 Try 提供了依据。
**举个例子。** 事务 T9，账户可用 100，要冻结 30：
1. **Cancel 先到：**日志里没有 T9，插入 `(xid=T9, CANCELLED)`，返回成功（空回滚）。
2. **迟到的 Try 到了：**它要先插入 `(xid=T9, TRIED)`，xid 是主键，撞键失败。
3. **结果：**Try 被拒绝，不冻结，可用仍是 100。
4. **如果不检查：**Try 照常冻结 30，可用变 70、冻结 30，但事务 T9 早已结束，没人再来解冻，这 30 元永久悬挂。
**容易错。**
- **以为 Cancel 之后不会再有 Try：**网络乱序、重试都会让 Try 迟到。
- **Try 不检查事务记录：**迟到的 Try 会成功预留，资源永久冻结。
- **把空回滚和悬挂当成两件独立的事：**它们靠同一条 CANCELLED 记录解决，一个处理 Cancel，一个拒绝 Try。
**业务场景。** 库存预占的 Try 因网络延迟晚到，此时订单已取消；Try 发现 Cancel 记录，拒绝预占，库存不会被永久占住。
**系统设计。** [[links.ticketmaster|票务预订（Ticketmaster）]]：座位预占请求延迟到达，面试官问「订单已取消座位还会被占吗」，答防悬挂检查。
**相关题。** 练习题 digital-wallet
**可能问法。**
- 什么是悬挂？ → Cancel 已经执行完，之后迟到的 Try 才到达。如果这个 Try 继续预留资源，这份资源永远不会有 Confirm 或 Cancel 来处理，就成了悬挂。
- 怎么防止 Cancel 后 Try 到达？ → Try 先检查事务记录，发现该事务已有 Cancel 记录就拒绝执行。实现上事务记录用 xid 做主键，Try 插入 `TRIED` 时撞键，说明已有记录，直接拒绝。
- 空回滚和悬挂有什么联系？ → 它们是一对，都因 Cancel 先于 Try 到达：Cancel 先到时 Try 还没执行，要空回滚并写下 `CANCELLED` 记录，不能报错；这条记录既处理了空回滚，也为拒绝之后迟到的 Try（悬挂）提供依据。
