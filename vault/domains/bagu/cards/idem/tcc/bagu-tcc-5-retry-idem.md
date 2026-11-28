---
id: bagu-tcc-5-retry-idem
node: a.idem.tcc
type: qa
step: 5
---
## Q
**TCC · Confirm、Cancel 失败与幂等**｜追问

面试官：「Confirm 或 Cancel 失败了怎么办？为什么它们必须幂等？」

## A
**基本回答。** 事务日志记录执行状态，失败就不断重试直到成功（Try 通过后，Confirm 理论上一定能成功，因为资源已预留）；多次失败告警，人工处理。重试意味着会重复调用，所以必须幂等。
Confirm、Cancel 都先判断状态，已是 `CONFIRMED` 或 `CANCELLED` 就直接返回成功；Cancel 还要容忍 Try 没到的空回滚，并拒绝之后迟到的 Try，否则资源会被永久冻结。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<rect x="8" y="6" width="114" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="65" y="31.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Confirm 第 1 次</text>
<rect x="128" y="6" width="204" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="230" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库短暂不可用：失败</text>
<text x="230" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">状态仍是 TRIED</text>
<rect x="8" y="56" width="114" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="65" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Confirm 第 2 次</text>
<rect x="128" y="56" width="204" height="42" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="230" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">条件更新成功</text>
<text x="230" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TRIED → CONFIRMED</text>
<rect x="8" y="106" width="114" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="65" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Confirm 第 3 次</text>
<rect x="128" y="106" width="204" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="230" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重复到达，已是 CONFIRMED</text>
<text x="230" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直接返回成功，不再扣减</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">失败就重试到成功；重试必须幂等</text>
</svg>
事务管理器对同一个 Confirm 重试了三次：第 1 次遇到数据库故障，失败，状态不变；第 2 次成功，状态从 TRIED 变成 CONFIRMED；第 3 次是重复到达，接口看到已是 CONFIRMED，直接返回成功，没有再扣一次。
**举个例子。** 订单 30 元，冻结 30 后 Confirm 扣款：
1. **第 1 次 Confirm：**数据库短暂不可用，失败，日志状态仍是 TRIED。
2. **管理器重试：**第 2 次 `UPDATE ... SET status='CONFIRMED' WHERE xid=? AND status='TRIED'` 影响 1 行，扣款完成。
3. **网络超时造成重复：**第 1 次其实有一个请求延迟到了，现在又执行一次，状态已是 CONFIRMED，条件更新影响 0 行，直接返回成功。
4. **结果：**只扣了一次 30 元。
**容易错。**
- **以为 Confirm 不会失败：**暂时性故障（数据库抖动）会让它失败，要重试。
- **重试时不判断状态：**重复扣减或重复解冻，余额错账。
- **无限高频重试：**要用指数退避，并设告警，转人工，不能静默放弃。
