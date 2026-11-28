---
id: hi-fix-retry-key-09-three-keys
node: fix.retry-key
type: qa
step: 3
---
## Q
**三道边界三个键 · 重试键**｜补强

面试官：「你让浏览器生成了 checkout_attempt_id。那调 PSP 的时候，直接把这个键当 PSP 的幂等键传过去，不就行了吗？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先承认能用：** 「一次点击只调一次 PSP 的简单流程，直接透传是成立的。但我不这么做，有三个原因。」
- **键空间不同：** 「我们库里的唯一约束带着 user_id，按用户隔离；PSP 的幂等键是按我们整个商户账号算的，所有用户共用。客户端的键是不可信输入，两个用户撞上同一个值，PSP 会把 A 的结果回给 B，或者报参数冲突。」
- **一次结账不止一次调用：** 「卡被拒后换卡再付，还是同一笔捐款；同一个 PSP 键会直接拿回缓存的拒绝。主 PSP 挂了切备用，也是另一家、另一个令牌。所以 PSP 的键对应一次支付尝试：donation_id 加第几次。」
- **生命周期不同：** 「PSP 的幂等键只保留有限时间（例如 Stripe 满 24 小时后就可能被清掉，Adyen 约 7 到 14 天）；对账、退款、收据要一个永久的引用号，我把 donation_id 写进 PSP 的 metadata。」
- **一句话收住：** 「每道边界一个键：浏览器到我们用 checkout_attempt_id，我们到 PSP 用 payment_attempt_id，对账用 donation_id。三者靠唯一约束一一对应，所以都是稳定的。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 376">
<rect x="20" y="8" width="120" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="80.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<text x="80.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">结账页</text>
<polyline points="80,48 80,106" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,106 76.8,99 83.2,99" style="fill:var(--accent,#3b6fd4)"/>
<text x="90" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① checkout_attempt_id</text>
<text x="90" y="86" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">客户端生成，防重复点击</text>
<rect x="20" y="106" width="300" height="64" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="135.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款 API + 数据库</text>
<text x="170.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">donation_id ← 唯一约束(user, key)</text>
<polyline points="80,170 80,236" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,236 76.8,229 83.2,229" style="fill:var(--accent,#3b6fd4)"/>
<text x="90" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② payment_attempt_id</text>
<text x="90" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">= donation_id + 第 n 次</text>
<text x="90" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">服务端派生，防自己超时重发</text>
<rect x="20" y="236" width="120" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="80.0" y="253.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主 PSP</text>
<text x="80.0" y="268.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">商户全局键空间</text>
<rect x="200" y="236" width="120" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="260.0" y="253.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">备用 PSP</text>
<text x="260.0" y="268.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新令牌、新尝试</text>
<polyline points="140,256 200,256" fill="none" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="170" y="300" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ metadata: donation_id</text>
<text x="170" y="316" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对账、退款、收据：永久引用号</text>
<text x="8" y="348" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">换卡或切 PSP：同一笔捐款，新的一次尝试，新键</text>
<text x="8" y="364" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一次尝试超时重发：同一个键</text>
</svg>
白板上：三道边界各自的键，以及换卡、切 PSP 时只换第二个键。
**为什么这样说。** 面试官在试探你是不是只会说「两边都做幂等」。强的回答说出每个键由谁生成、在哪道边界生效、什么时候换新；弱的回答是「一个键用到底」，换卡或切 PSP 时就出错。
**面试官可能接着问。**
- 同一次支付尝试超时了，重发用什么键？ → 同一个 payment_attempt_id。PSP 要么返回第一次的结果，要么只处理这一次。
- 换卡之前，上一次尝试的结果还不知道呢？ → 先查清或取消上一次尝试，确认没扣款，再开新的尝试；不然可能两张卡都扣。
- 为什么不用服务端随机生成的 UUID 当 PSP 键？ → 也可以，但必须先落库再调用；从 donation_id 派生的好处是崩溃后不用找回那个随机值，算一下就有。
**常见失分。**
- **一个键用到底：** 换卡时拿回缓存的拒绝，切 PSP 时键在另一家不存在，对账时键已经过期。
- **只说做幂等：** 没说哪个值、谁生成、在哪道边界，面试官听不到机制。
- **未知结果就换通道：** 上一次尝试没查清就切 PSP，可能扣两次。
