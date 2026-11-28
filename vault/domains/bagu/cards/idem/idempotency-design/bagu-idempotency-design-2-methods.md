---
id: bagu-idempotency-design-2-methods
node: a.idem.idempotency-design
type: qa
step: 2
---
## Q
**幂等 · 实现方式与适用场景**｜必会

面试官：「幂等有哪些实现方式？各自适用什么场景？」

## A
**基本回答。** 唯一索引（创建类）、状态机条件更新（状态流转：`UPDATE order SET status='PAID' WHERE id=? AND status='UNPAID'`，第一次影响 1 行，重复影响 0 行，同时防止状态回退）、去重表（消费消息、回调：messageId 做唯一键，和业务数据放同一个本地事务）、乐观锁版本号（更新类）、Token（表单防重）。MySQL 8.0.46 实测：`INSERT IGNORE` 遇重复影响 0 行，普通插入重复主键报 1062。分布式锁只缩小并发窗口，不能当最终保证。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">方法</text>
<text x="174" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">适用场景</text>
<rect x="8" y="22" width="156" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">唯一索引</text>
<rect x="174" y="22" width="158" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="253" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">创建类</text>
<rect x="8" y="54" width="156" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">条件更新（状态机）</text>
<rect x="174" y="54" width="158" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">状态流转</text>
<rect x="8" y="86" width="156" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">去重表</text>
<rect x="174" y="86" width="158" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="253" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费消息、回调</text>
<rect x="8" y="118" width="156" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">乐观锁版本号</text>
<rect x="174" y="118" width="158" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="253" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">更新类</text>
<rect x="8" y="150" width="156" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86" y="167.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Token</text>
<rect x="174" y="150" width="158" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="253" y="167.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">表单防重</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分布式锁只缩小并发窗口，不是最终保证</text>
</svg>
左列是五种实现方式，右列是各自最适合的场景，对应关系记住就行。高亮的是条件更新：只让合法的状态流转发生一次，是支付状态最常用的做法。
**容易错。**
- **拿分布式锁当最终保证：**锁会过期，主从切换也可能出现两个持有者。最终保证要靠唯一键或条件更新。
- **乐观锁重试时重新读版本：**重新读到新版本再提交，同一个操作就被执行了两次，要带着请求 ID 或业务唯一键。
- **把唯一键冲突当失败：**创建类幂等里，撞键说明已经处理过，应当按成功返回，而不是报错给用户。

**业务场景。** 充值回调更新订单：条件更新只让「未支付」变「已支付」一次，重复回调影响行数为 0，直接返回成功。
