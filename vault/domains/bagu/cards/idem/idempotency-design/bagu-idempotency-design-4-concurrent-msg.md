---
id: bagu-idempotency-design-4-concurrent-msg
node: a.idem.idempotency-design
type: qa
step: 4
---
## Q
**幂等 · 两条相同消息同时到达两台实例**｜必会

面试官：「两条完全一样的消息同时分发到两台实例，业务不允许重复处理，你怎么写？」

## A
**基本回答。** 在同一个本地事务里先插去重表（messageId 唯一键），再执行业务；两个实例并发插入，只有一个成功，另一个撞唯一键直接忽略。
**一句话记住。** 两个人同时抢同一个座位，不靠谁先问过、谁先看到空位，而是座位只有一个，谁先坐下谁赢，后到的发现有人了就走开。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="8" y="16" width="80" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="48" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 A</text>
<rect x="8" y="116" width="80" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="48" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例 B</text>
<rect x="126" y="56" width="100" height="58" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="176" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">去重表</text>
<text x="176" y="89.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">messageId</text>
<text x="176" y="104.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">唯一键</text>
<line x1="88" y1="33" x2="126" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,66.0 118.6,63.8 122.8,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="88" y1="133" x2="126" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,104.0 122.4,110.8 118.5,105.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="256" y="16" width="76" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="294" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">插入成功</text>
<text x="294" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">执行业务</text>
<rect x="256" y="116" width="76" height="34" rx="3" stroke-width="1.2" fill="none" style="stroke:var(--dim,#6b7280)"/>
<text x="294" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">撞唯一键</text>
<text x="294" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直接忽略</text>
<line x1="226" y1="70" x2="256" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,38.0 253.5,45.3 248.9,40.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="226" y1="100" x2="256" y2="130" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,130.0 248.8,127.3 253.3,122.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个事务里：先插去重表，再做业务</text>
</svg>
两台实例同时拿到同一条消息，都去往去重表插入同一个 messageId。数据库保证唯一键只能插入一次：一台成功后去执行业务，另一台撞键，直接忽略这条消息。
**讲明白。**
- **为什么不先查后写：**先 `SELECT` 看有没有处理过、再写，两台实例会同时查到「没有」，然后都去执行。唯一约束由数据库原子裁决，没有这个空档。
- **去重和业务同一个事务：**去重记录和业务数据在同一个本地事务里提交。业务失败回滚时，去重记录一起回滚，这条消息之后重试就能正常重新处理，不会被当成已处理而丢掉。
- **并发插入的细节：**两个事务同时插同一个唯一键时，后插入的那个会等第一个事务提交或回滚：提交了它就撞键失败，回滚了它就能插入成功。
- **分布式锁不够：**锁只缩小并发窗口。拿到锁后仍要查业务状态或幂等记录，因为锁可能过期，锁释放后重复消息再来也挡不住。
- **怎么验证方案有效：**同一个号并发发 50 到 100 个请求，最终只能有一次真正执行。
- **还要验证异常路径：**测超时重试、业务半途异常，再对订单、流水、去重表做数据校验，看有没有重复记录。
**举个例子。** 积分消息 M1001（给用户加 10 分）同时到达实例 A、B：
1. **A 开事务：**`INSERT INTO dedup(message_id) VALUES('M1001')` 成功，继续给用户加 10 分。
2. **B 同时开事务：**同样插入 M1001，因为 A 还没提交，B 的插入先等待。
3. **A 提交：**去重记录和加分一起提交。B 的插入随即撞唯一键，报错，B 捕获后直接忽略这条消息。
4. **另一种情况：**如果 A 加分时出错回滚，去重记录也跟着回滚，B 的插入就能成功，由 B 来处理，消息不会丢。
**容易错。**
- **先查后写：**两个实例同时查到「没处理过」就都会执行，要靠唯一约束。
- **去重记录单独提交：**去重记录先提交、业务后失败，这条消息以后就被当成已处理，数据丢了。要和业务同一个事务。
- **以为拿了分布式锁就安全：**锁过期、主从切换都会出现两个持有者，拿到锁后仍要查幂等记录。
**业务场景。** 积分发放消息同时到达两台实例，去重表唯一键只让一台加积分，另一台直接返回。
**系统设计。** [[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：同一条通知被两台 worker 取到，面试官问「怎么保证用户只收到一次」，答去重表加唯一键。
**相关题。** 练习题 idempotent-transfer、练习题 notification-service
**可能问法。**
- 并发重复消息怎么处理？ → 在同一个本地事务里先往去重表插入（messageId 唯一键），再执行业务；两个实例并发插入，只有一个成功，另一个撞唯一键就直接忽略。唯一约束是数据库的原子裁决，不依赖先查后写；去重记录和业务同事务，业务回滚去重也回滚，之后才能正常重入。
- 分布式锁能保证幂等吗？ → 不能。锁只是缩小并发窗口，锁过期、主从切换都可能出现两个持有者，锁释放后重复消息再来，锁也挡不住。拿到锁后仍要查业务状态或幂等记录，真正的保证是唯一键或条件更新。
- 怎么验证幂等方案有效？ → 同一个号并发发 50 到 100 个请求，最终只能有一次真正执行；再测超时重试、业务半途异常这些路径，最后对订单、流水、去重表做数据校验，看有没有重复记录。
