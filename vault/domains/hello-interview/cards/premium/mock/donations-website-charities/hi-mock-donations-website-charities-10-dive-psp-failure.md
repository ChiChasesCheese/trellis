---
id: hi-mock-donations-website-charities-10-dive-psp-failure
node: qb.sd.donations-website-charities.mock
type: qa
step: 10
---
## Q
**限时捐款网站 · 第 10 步 · 深入三：PSP 故障、备用通道、尖峰，收尾**｜模拟面试

面试官：「如果主 PSP 挂了，或者特别慢，会怎样？有没有备用方案？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先分两类失败：** 被拒绝（卡被拒、余额不足、风控拦截）是业务结果，换 PSP 没用，让用户换卡或钱包；没拿到结果（超时、5xx、连不上）才可能是 PSP 故障。
- **熔断器：** 对主 PSP 的调用包熔断，滑动窗口内失败率超阈值（例：20 秒内超 50%，示例值，上线按数据调）就打开，新捐款直接走备用；过一会儿半开，放少量探测，恢复再关。熔断打开时正在飞的请求仍按原规则（超时记 UNKNOWN 等对账），只影响之后新建的捐款。
- **关键规则：** UNKNOWN 的捐款在对账查清前绝不转给另一家 PSP 重发：幂等键只在一家 PSP 内有效，主 PSP 其实已扣，备用再扣就双扣。顺序是先查或先取消，确认没扣，才能换路由；路由只在 CREATED 时选，进入 PROCESSING 就锁定，donation 行记 psp 字段，对账去对的那家查。
- **令牌绑定 PSP：** 令牌来自主 PSP 的前端组件，备用用不了，切到备用浏览器要用备用的组件重新取令牌。另提供钱包（Apple Pay、PayPal）作备用支付方式。
- **PSP 变慢：** 并发 = 吞吐 × 延迟：2,000 × 0.5 秒 = 1,000；慢到 2 秒是 4,000，线程池占满、整站被拖死。所以对 PSP 加并发闸约 1,000（与约定额度对齐），超出立刻返回「排队中」，入队由后台 worker 调，前端轮询。
- **没来得及展开：** 欺诈防护（卡测试攻击：按 IP 和设备限速、验证码、PSP 风控）、先授权后请款（授权失败可放心换通道，代价多一次调用、延迟翻倍）、活动结束后的全量对账和数据处置。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 342">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">PSP 的回答 → 记成什么 → 怎么走</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">明确拒绝：卡被拒、余额不足、风控</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">记 FAILED，不切 PSP（卡本身有问题）</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 提示换卡或换钱包，用户新开一笔</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">没拿到答案：超时、5xx、连不上</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">记 UNKNOWN，绝不转给另一家 PSP</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 对账查清、必要时先取消，再谈重试</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">熔断已打开时才创建的新捐款</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">记 CREATED，psp = 备用</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 浏览器改用备用 PSP 的前端组件取令牌</text>
<rect x="8" y="236" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="256" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">对账确认「没扣」的旧捐款</text>
<text x="18" y="271" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">记 FAILED（已取消）</text>
<text x="18" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 用户新开一笔：新 donationId，可走任一家</text>
<text x="8" y="314" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">幂等键只在一家 PSP 内有效；令牌也只属于</text>
<text x="8" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发它的那一家，所以换通道一定要重新取令牌</text>
</svg>
白板上新增：一张决策表：PSP 的四种回答分别记成什么、怎么走。

**常见失分。**
- **把 UNKNOWN 转给备用：** 幂等键不跨 PSP，可能双扣，最危险的一句话。
- **拒绝也切 PSP：** 卡本身有问题，换通道只多一次失败。
- **忘记令牌绑定：** 切到备用后旧令牌用不了。
- **不限并发：** PSP 变慢时线程堆满，整站一起挂。
- **没有收尾：** 面试官只记得最后一个问题。
