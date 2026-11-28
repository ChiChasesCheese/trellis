---
id: bagu-timeout-unknown-3-safe-retry
node: a.idem.timeout-unknown
type: qa
step: 3
---
## Q
**超时未知 · 同一个幂等键重试为什么安全**｜必会

面试官：「查询没查到记录，你就重新发请求，会不会重复扣款？」

## A
**基本回答。** 不会，前提是用同一个幂等键或请求号重发，且对方按它去重：已处理过会返回原结果，没处理过则正常处理一次。换新请求号才会重复扣款。
**一句话记住。** 同一个请求号就像同一张取餐小票：重复出示，店员只会给你同一份餐；换一张新小票，就当成新的一单，又给你做一份。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个请求号</text>
<rect x="8" y="24" width="72" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再发 R1</text>
<rect x="100" y="24" width="116" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="158" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道：见过 R1</text>
<rect x="236" y="24" width="96" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回原结果</text>
<text x="284" y="53" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只扣 1 次</text>
<line x1="80" y1="41" x2="100" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,41.0 93.0,44.2 93.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="216" y1="41" x2="236" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,41.0 229.0,44.2 229.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">换成新请求号</text>
<rect x="8" y="106" width="72" height="34" rx="3" stroke-width="1.2" fill="none" style="stroke:var(--dim,#6b7280)"/>
<text x="44" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">换成 R2</text>
<rect x="100" y="106" width="116" height="34" rx="3" stroke-width="1.2" fill="none" style="stroke:var(--dim,#6b7280)"/>
<text x="158" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道：新请求</text>
<rect x="236" y="106" width="96" height="34" rx="3" stroke-width="1.2" fill="none" style="stroke:var(--dim,#6b7280)"/>
<text x="284" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">又扣一次</text>
<text x="284" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">共扣 2 次</text>
<line x1="80" y1="123" x2="100" y2="123" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="100.0,123.0 93.0,126.2 93.0,119.8" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<line x1="216" y1="123" x2="236" y2="123" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="236.0,123.0 229.0,126.2 229.0,119.8" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求号是对方识别「同一笔」的唯一凭据</text>
</svg>
第一行是正确做法：重发时带着同一个请求号 R1，渠道认出见过，直接返回原来的结果，用户只被扣一次。第二行是错误做法：换成新请求号 R2，渠道当作一笔新请求，又扣一次。
**讲明白。**
- **对方靠请求号去重：**对方的唯一性约束保证同一个请求号只生效一次。已经处理过，就返回原来的结果；没处理过，就正常处理一次。
- **为什么不能换请求号：**换新请求号对方会当作一笔新请求，而第一次可能其实已经成功（只是响应丢了），就会重复扣款。换号等于绕过这道保护。
- **请求号要提前生成：**幂等键要在首次请求前生成并持久化，重试时复用，而不是每次重发都重新生成。
- **参数也要一致：**重试要带与原请求完全相同的幂等键，参数也保持一致。
- **最稳的收敛流程：**先用同一请求号查询，确认对方「从未见过该请求号」，再重发。这样完整地走完了查询、重试两步。
- **对方幂等不可靠怎么办：**如果对方的幂等不可靠，就降低自动化程度，转人工或对账。
**举个例子。** 用户支付 100 元，请求号 R1：
1. **第一次：**渠道已经扣款成功，但响应丢了，我方超时。
2. **查询：**用 R1 查询，渠道没有响应或查不到，不能确定。
3. **同号重发：**再次发送 R1，渠道发现 R1 已处理过，直接返回第一次的成功结果，用户只被扣一次。
4. **反例：**如果这次换成新请求号 R2，渠道把它当新的一笔，用户被扣 200 元。
**容易错。**
- **以为重试就会重复扣款：**同一请求号重发是安全的，前提是对方按它去重。
- **每次重试都新生成请求号：**对方认不出是同一笔，就重复扣了，要先生成并持久化。
- **不管对方是否支持幂等：**对方幂等不可靠时，自动重试不安全，要降低自动化程度。
**业务场景。** 渠道其实已扣款但响应丢失，同请求号重发，渠道返回原来的成功结果，用户只被扣一次。
**系统设计。** [[links.tt-wallet-ledger-service|钱包与复式账本服务（余额、冻结、转账、多币种）]]：转账调用下游超时，面试官问「重试会不会重复转账」，答同键重试加下游唯一约束。
**相关题。** 练习题 idempotent-transfer
**可能问法。**
- 超时后重试安全吗？ → 只有用同一个幂等键或请求号重发，且对方按它去重时才安全：已处理过返回原结果，没处理过则正常处理一次。最好先用同一请求号查询确认从未见过，再重发。
- 重试要带什么？ → 要带与原请求完全相同的幂等键或请求号，参数也保持一致。幂等键要在首次请求前生成并持久化，重试时复用，而不是每次重新生成。
- 为什么不能换请求号？ → 换新请求号对方会当作一笔新请求，而第一次可能其实已经成功（只是响应丢了），就会重复扣款。对方靠请求号的唯一约束保证同一笔只生效一次，换号等于绕过这道保护。
