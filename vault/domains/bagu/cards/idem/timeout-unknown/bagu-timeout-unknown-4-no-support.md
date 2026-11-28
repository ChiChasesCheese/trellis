---
id: bagu-timeout-unknown-4-no-support
node: a.idem.timeout-unknown
type: qa
step: 5
---
## Q
**超时未知 · 对方不支持幂等和查询**｜追问

面试官：「如果对方既不支持幂等，也没有查询接口，怎么办？」

## A
**基本回答。** 这样的依赖不能自动重试，只能走人工和对账，并在设计上要求对方补充查询接口。
**一句话记住。** 对方既不给收据（幂等）又不让你查单（查询），就像把钱交给一个不开发票的小摊：出了问题只能靠月底对账本，靠人去核。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="8" y="8" width="324" height="50" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有幂等 + 有查询</text>
<text x="170" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">自动重试、查询、对账，能自动收敛</text>
<rect x="8" y="70" width="324" height="50" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缺一个能力</text>
<text x="170" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不能自动收敛，调低自动化程度</text>
<rect x="8" y="132" width="324" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两个都没有</text>
<text x="170" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">人工队列 + 次日对账文件补单或冲正</text>
<line x1="170" y1="58" x2="170" y2="70" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="170.0,70.0 166.8,63.0 173.2,63.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<line x1="170" y1="120" x2="170" y2="132" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="170.0,132.0 166.8,125.0 173.2,125.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
</svg>
从上到下，自动化程度逐级下降：两个能力都有，系统能自己收敛；缺一个，就不能自动收敛；两个都没有，只能靠人工队列和第二天的对账文件。
**讲明白。**
- **无幂等：**重试可能重复，对方不会认出这是同一笔。
- **无查询：**无法确认结果，不知道超时的那笔到底成没成。
- **缺一不能自动收敛：**两个能力缺一就不能自动收敛，所以不能自动重试，更不能自动重扣。
- **走人工和对账：**超时订单挂起进人工队列，次日用渠道的对账文件确认最终状态，再补单或冲正。自动化程度调低。
- **暂时没有时：**用较长的人工复核间隔代替自动重试，不再自动重扣。
- **接入前提是查询接口：**在设计评审里把「提供按请求号查询的接口」列为接入前提，推动对方补上。
- **不因业务着急放宽：**对方暂时没有时，靠对账兜底和人工复核，不能因为业务着急就放宽成自动重试。
**举个例子。** 某小渠道没有查询接口，也不支持幂等，一笔 100 元的订单超时：
1. **不自动重试：**没有幂等，重试可能重复扣 100 元；没有查询，也不知道第一次成没成。
2. **挂起：**订单标成「处理中」，进入人工队列。
3. **次日对账：**拿到渠道的对账文件，看里面有没有这笔。有，补单入账；没有，冲正。
4. **长期：**在接入评审里要求对方提供按请求号查询的接口。
**容易错。**
- **以为有重试就行：**没有幂等和查询，重试要么重复扣款，要么不知道结果。
- **业务着急就自动重试：**正确性比速度重要，要靠对账和人工兜底。
- **只要求幂等不要求查询：**没有查询，就无法确认超时的结果，两个都需要。
**业务场景。** 某小渠道没有查询接口，超时订单进入人工队列，次日用渠道对账文件补单或冲正。
**系统设计。** [[links.tt-payment-reconciliation|支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）]]：面试官问「渠道不给查询接口怎么保证不错账」，答日终对账和人工队列。
**相关题。** 练习题 double-entry-ledger
**可能问法。**
- 渠道不支持查询怎么办？ → 不能自动重试：没有幂等，重试可能重复；没有查询，无法确认结果。超时订单进入人工队列，次日用渠道对账文件补单或冲正，自动化程度调低。
- 无法自动重试时怎么办？ → 走人工加对账：超时订单挂起进人工队列，用较长的人工复核间隔代替自动重试，再用对账文件确认最终状态后补单或冲正，不再自动重扣。
- 怎么推动对方补接口？ → 在设计评审里把「提供按请求号查询的接口」列为接入前提；对方暂时没有时，靠对账兜底和人工复核，不能因为业务着急就放宽成自动重试。
