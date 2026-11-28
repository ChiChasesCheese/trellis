---
id: bagu-saga-1-compensation
node: b.idem.saga
type: qa
step: 1
---
## Q
**Saga · 补偿、编排方式与没有隔离性的代价**｜追问

面试官：「订票、订酒店、租车三步，租车失败了怎么办？没有隔离性会出什么问题？」

## A
**基本回答。** Saga 把一个长事务拆成一串本地事务 T1…Tn，每个 Ti 都配一个补偿动作 Ci，按顺序一步步执行；如果第 k 步失败，就按反方向依次执行 C(k−1)…C1。每一步都是直接提交，补偿是语义上的撤销（订的酒店退订、付的钱退款，不是回滚到原状），所以中间状态对外是可见的，Saga 缺少隔离性。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">正向：每步本地事务直接提交</text>
<rect x="6" y="28" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T1</text>
<text x="54" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订机票</text>
<rect x="122" y="28" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T2</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订酒店</text>
<rect x="238" y="28" width="96" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T3</text>
<text x="286" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">租车失败</text>
<line x1="102" y1="48" x2="115" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122.0,48.0 115.0,51.2 115.0,44.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="218" y1="48" x2="231" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="238.0,48.0 231.0,51.2 231.0,44.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="104" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">反向：从失败点往回补偿</text>
<rect x="6" y="116" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="132.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C1</text>
<text x="54" y="147.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">退机票</text>
<rect x="122" y="116" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="132.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C2</text>
<text x="170" y="147.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">退酒店</text>
<line x1="286" y1="68" x2="286" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="286" y1="92" x2="170" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="170" y1="92" x2="170" y2="109" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,116.0 166.8,109.0 173.2,109.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="122" y1="136" x2="109" y2="136" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102.0,136.0 109.0,132.8 109.0,139.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="184" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">每步都已提交，中间状态别人看得见</text>
<text x="8" y="202" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">补偿 = 语义撤销（退款），不是回滚到原状</text>
<text x="8" y="220" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">补偿要幂等、可重试，仍失败转人工</text>
<text x="8" y="238" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">出票/发货这类不可补偿的步骤放最后</text>
</svg>
上排是正向的三步，每步已经提交；T3 失败后，蓝色箭头指向 C2，再依次往回补偿到 C1。
**容易错。**
- **以为补偿就是回滚：** 回滚能回到原状，补偿只是再做一笔反向操作，别人期间看到过中间状态。
- **以为补偿不会失败：** 补偿也会超时、报错，要能重试且幂等。
- **把不可补偿的步骤放前面：** 发货、出票这类做了就撤不掉的步骤，应放在最后（pivot transaction，转折事务，过了它就不会回头），可能失败的步骤放前面；补偿缺隔离还可用语义锁（订单先设 `PENDING`）或可交换的更新。补偿可能比正向先到，先登记「已取消」，正向到了就拒绝。
- **用协同式做长流程：** 协同式没有中心，各服务靠事件触发下一步，流程分散难追踪、可能循环依赖，只适合很短的流程；推荐编排式，由中心协调器依次调用、失败时反向补偿。
- **资金类硬上 Saga：** 要强隔离的资金场景选 TCC（先 Try 预留再 Confirm 或 Cancel）；流程长、步骤多、含外部系统、能容忍中间状态的才选 Saga。

**业务场景。** 机票加酒店加租车的行程预订，租车失败后按反序退酒店、退机票；每个退订请求带业务号，重复到达也只退一次。
