---
id: bagu-tcc-1-three-apis
node: a.idem.tcc
type: qa
step: 1
---
## Q
**TCC · Try、Confirm、Cancel 各做什么**｜必会

面试官：「下单要同时冻结库存和优惠券，用 TCC 怎么做？三个接口各做什么？」

## A
**基本回答。** 每个参与方提供三个接口：Try 检查并预留资源，不做最终变更；Confirm 真正提交，使用预留的资源；Cancel 释放预留。事务管理器先调所有 Try，全成功调 Confirm，任一失败调 Cancel。
**一句话记住。** TCC 像订酒店：先交押金占房（Try），入住时把押金转成房费（Confirm），不住了就退押金（Cancel）。房间一直是你的，但钱还没真正花出去。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="100" y="6" width="140" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="25.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务管理器</text>
<rect x="20" y="70" width="130" height="40" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库存服务</text>
<text x="85" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">三个接口</text>
<rect x="190" y="70" width="130" height="40" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">优惠券服务</text>
<text x="255" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">三个接口</text>
<line x1="150" y1="36" x2="85" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,70.0 89.7,63.9 92.7,69.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="190" y1="36" x2="255" y2="70" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,70.0 247.3,69.6 250.3,63.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 先对所有参与方调 Try（预留）</text>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 全成功 → 都调 Confirm（提交）</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ 任一失败 → 都调 Cancel（释放）</text>
</svg>
事务管理器是指挥，库存服务和优惠券服务是两个参与方，每个都实现了 Try、Confirm、Cancel 三个接口。指挥按三步走：先全部预留，全成功再提交，有一个失败就全部释放。
**讲明白。**
- **Try 只预留不变更：**检查资源够不够，够就把它预留出来（比如把库存冻结），但不做最终的变更。预留之后，这份资源别人用不了。
- **Confirm 真正提交：**使用 Try 预留的资源完成最终变更，比如把冻结的库存真正扣掉。
- **Cancel 释放预留：**把 Try 预留的资源还回去，比如把冻结的库存还给可用。
- **谁来调度：**事务管理器先调所有参与方的 Try，全部成功就调所有的 Confirm，任何一个 Try 失败就调所有的 Cancel。
- **每一步都是本地事务：**每个接口在自己的服务里是一个本地事务，资源只是被预留，所以没有数据库层面的长事务，也没有长时间持锁。
- **不依赖 XA：**不需要数据库支持 XA（分布式事务协议）。代价是业务侵入强：每个操作要写三个接口。
- **对比 2PC：**2PC 靠数据库层面的事务，整个过程一直持锁；TCC 追求最终一致，不一直占着业务资源的锁。
**举个例子。** 下单要冻结库存 1 件和优惠券 1 张，库存可用 10 件：
1. **Try 库存：**可用 10 变成 9，冻结 1。
2. **Try 优惠券：**这张券从可用变成冻结。两个 Try 都成功。
3. **Confirm：**库存的冻结 1 件变成真正扣减，优惠券的冻结变成已使用，订单成功。
4. **另一种结果：**如果优惠券 Try 失败（券已过期），管理器对库存调 Cancel，冻结的 1 件还回可用，库存重新是 10。
**容易错。**
- **以为 TCC 是数据库事务：**它是业务层面的三个接口，数据库只管各自的本地事务。
- **以为 Try 就是扣：**Try 只预留，真正的变更在 Confirm。
- **以为只写一个正向接口就行：**每个操作要有 Confirm 和 Cancel 配套，工作量是三倍。
**业务场景。** 下单时 Try 冻结库存和优惠券，Confirm 扣减，Cancel 释放。
**系统设计。** [[links.tt-flash-sale-ticketing|秒杀抢票（排队、限流、防超卖）]]：下单链路涉及库存、优惠券、订单，面试官问「跨服务怎么保证一致」，答 TCC 预留加确认。
**相关题。** 练习题 digital-wallet
**可能问法。**
- TCC 是什么？ → Try、Confirm、Cancel 的分布式事务方案：每个参与方提供三个接口，Try 检查并预留资源，Confirm 真正提交，Cancel 释放预留；事务管理器先调所有 Try，全成功调 Confirm，任一失败调 Cancel，追求最终一致。
- TCC 的三个阶段各做什么？ → Try：检查并预留资源，不做最终变更；Confirm：真正提交，使用预留的资源；Cancel：释放预留。每一步都是本地事务，资源只是被预留，没有数据库层面的长事务和长时间持锁。
- TCC 和本地事务的区别？ → 本地事务靠数据库 ACID 一次提交；TCC 跨服务，把一个事务拆成三个业务接口，资源只是被预留。它不依赖数据库的 XA 能力，也不像 2PC 一直持锁，代价是业务侵入强，每个操作都要写三个接口。
