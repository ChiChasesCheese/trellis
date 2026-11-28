---
id: bagu-tcc-6-compare
node: a.idem.tcc
type: qa
step: 6
---
## Q
**TCC · 与 2PC、Saga 的取舍**｜追问

面试官：「TCC 和 2PC、Saga 比，有什么取舍？什么时候选 TCC？」

## A
**基本回答。** 2PC 靠数据库层面事务，整个过程持锁，强一致但阻塞、有单点；TCC 靠业务代码预留，不长期持锁，最终一致；Saga 每步直接提交，靠补偿撤销，隔离性弱。资金类、要隔离性的选 TCC。
TCC 要写 Try、Confirm、Cancel 三套逻辑，还要处理空回滚、悬挂、幂等；Saga 写正向和补偿两套。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 204">
<rect x="66" y="6" width="84" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2PC</text>
<rect x="154" y="6" width="84" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="196" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TCC</text>
<rect x="242" y="6" width="84" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Saga</text>
<text x="8" y="59" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">持锁</text>
<rect x="66" y="40" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全程持锁</text>
<rect x="154" y="40" width="84" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="196" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只预留</text>
<rect x="242" y="40" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每步提交</text>
<text x="8" y="93" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一致性</text>
<rect x="66" y="74" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">强一致</text>
<rect x="154" y="74" width="84" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="196" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最终一致</text>
<rect x="242" y="74" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最终一致</text>
<text x="8" y="127" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">隔离性</text>
<rect x="66" y="108" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">强</text>
<rect x="154" y="108" width="84" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="196" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">靠冻结</text>
<rect x="242" y="108" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">弱</text>
<text x="8" y="161" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">适合</text>
<rect x="66" y="142" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">少用</text>
<rect x="154" y="142" width="84" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="196" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">资金类</text>
<rect x="242" y="142" width="84" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长流程</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">流程长、含外部系统 → Saga</text>
</svg>
三列对比三种方案，每一行是一个维度。高亮的 TCC 列：不一直持锁，靠预留（冻结）保证隔离，适合资金类。
**举个例子。** 同样「第 3 步失败」，三种方案的表现：
1. **下单（余额 + 优惠券）用 TCC：**前两步只是冻结，别人看不到变化；第 3 步失败，Cancel 把冻结还回去，中间状态没有暴露。
2. **机票酒店组合预订用 Saga：**机票和酒店各自已经提交，第 3 步（租车）失败，要依次对酒店、机票做补偿（退订）。
3. **Saga 的中间状态：**在补偿完成之前，别人能看到机票已订、酒店已订，需要语义锁。
4. **2PC：**整个过程所有参与方一直持锁，别人想用这些资源只能等，高并发下吞吐上不去。
**容易错。**
- **以为 TCC 比 Saga 好：**TCC 业务侵入更大，外部系统没法预留就用不了，流程长时用 Saga 更合适。
- **以为 Saga 有隔离性：**每步直接提交，中间状态对外可见，隔离性弱。
- **以为 2PC 没有缺点：**整个过程持锁、协调者单点、吞吐低，高并发难以承受。
