---
id: hi-mock-uber-02-functional
node: sd.problem-breakdowns.uber.mock
type: qa
step: 2
---
## Q
**网约车 · 第 2 步 · 功能需求**｜模拟面试

面试官：「好，你来把功能需求列一下，挑最重要的几条。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说打算：** 「我挑三条核心功能，其余画到线外。线外的您想要哪条，随时可以挪进来。」
- **第一条：** 「乘客输入起点和终点，得到估价和预计到达时间；确认后按这个估价叫车。估价和叫车是一个流程的两步，我算一条。」
- **第二条：** 「叫车之后，系统匹配一位在附近、并且空闲的司机。」
- **第三条：** 「司机可以接受或拒绝订单；接受之后，导航到上车点，再到目的地。」
- **导航怎么做：** 「导航用司机手机的 GPS 加第三方地图，我们只把上车点和目的地坐标给他。」
- **线外：** 「乘客和司机互相评分、预约叫车、车型分类（X、XL、Comfort），我先画在线外。」
- **停下确认：** 「这样可以吗？」等面试官点头再往下走。
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 362">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">功能需求（线内 3 条）</text>
<rect x="8" y="26" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="47.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">1  估价并叫车</text>
<text x="18" y="62.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">输入起终点 → 看到估价和 ETA → 按估价叫车</text>
<rect x="8" y="86" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="107.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">2  匹配附近司机</text>
<text x="18" y="122.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">叫车后，系统找一位附近且空闲的司机</text>
<rect x="8" y="146" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="167.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">3  司机接单并导航</text>
<text x="18" y="182.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">接受或拒绝；接受后导航到上车点、目的地</text>
<line x1="8" y1="212" x2="332" y2="212" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线外（先不做，想要随时挪进来）</text>
<rect x="8" y="252" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">评分：乘客评司机、司机评乘客</text>
<rect x="8" y="288" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="306" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">预约叫车</text>
<rect x="8" y="324" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="342" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">车型分类：X、XL、Comfort</text>
</svg>
白板上新增：三张便签（线内三条功能）、一条虚线、虚线下三张灰框（线外）。
**为什么这样说。** （约 2 分钟，累计第 3 分钟。）面试官看你会不会取舍：三条功能够把主流程跑通，又留出时间给难点。弱的回答是列十几条，或者把「系统要高可用」这类非功能需求混进功能里，或者列完不确认。确认这一步也在展示你把面试官当搭档。
**面试官可能接着问。**
- 评分为什么放线外？ → 它是行程结束后的一次独立写入，不影响匹配主流程，也没有难的扩展性问题。时间有限，我先把主流程和难点讲透。
- 要不要加取消订单？ → 可以挪进来。它只是给行程多一个状态（requested、accepted、cancelled），对整体设计影响不大，我在实体那一步顺手带上。
- 支付呢？ → 放线外。支付是一整块独立系统，想听我再展开。
**常见失分。**
- **列得太多：** 十几条功能讲不完，主流程和深入问题都被挤掉。
- **不说线外：** 没有划线，面试官不知道你是忘了还是故意不做。
- **不确认：** 自己闷头定范围，面试官的期待和你的不一致，后面很被动。
