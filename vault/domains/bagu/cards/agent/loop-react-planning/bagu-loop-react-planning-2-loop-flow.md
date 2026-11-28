---
id: bagu-loop-react-planning-2-loop-flow
node: a.agent.loop-react-planning
type: qa
step: 2
---
## Q
**Agent Loop · 完整流程是什么**｜必会

面试官：「讲讲 Agent Loop 的完整流程。工具执行完的结果是怎么回到模型那里的？」

## A
**基本回答。** Agent Loop 就是一个循环。先初始化：载入系统提示、工具列表和用户请求。然后模型看当前上下文，选择直接回答，或者调用某个工具。执行器真正执行工具，把结果作为观察（Observation）追加回上下文，再回到模型。直到模型给出最终答案，或者命中停止条件（最大轮数、Token 预算、超时）。
**一句话记住。** Agent Loop 就是「看一眼 → 动一下 → 再看一眼」：每动一下，结果要写在眼前的黑板（上下文）上，下一轮才看得见。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="6" y="4" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="19.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 初始化上下文</text>
<text x="81.0" y="34.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">系统提示·工具·请求</text>
<rect x="6" y="76" width="140" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="76.0" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 模型决策</text>
<text x="76.0" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">答案 or 调工具</text>
<rect x="200" y="76" width="134" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267.0" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 执行器执行</text>
<text x="267.0" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务侧真正执行</text>
<rect x="200" y="150" width="134" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267.0" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 观察</text>
<text x="267.0" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结果写回上下文</text>
<rect x="6" y="168" width="124" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直接回答：结束</text>
<text x="68.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或命中停止条件</text>
<line x1="81" y1="42" x2="81.0" y2="70.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,76.0 78.0,70.0 84.0,70.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="146" y1="96" x2="194.0" y2="96.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="200.0,96.0 194.0,99.0 194.0,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="173" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调工具</text>
<line x1="267" y1="116" x2="267.0" y2="144.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="267.0,150.0 264.0,144.0 270.0,144.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="200" y1="170" x2="124.97309204445389" y2="119.35683713000637" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,116.0 126.7,116.9 123.3,121.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="140" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">再来一轮</text>
<line x1="60" y1="116" x2="60.0" y2="162.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,168.0 57.0,162.0 63.0,162.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
沿着数字走一圈：模型决策，要么直接答完收工，要么调工具；工具结果写回上下文，再回到模型。
**讲明白。**
- **四步循环：**初始化上下文；模型决策；执行器执行工具；把观察写回上下文，回到第二步，直到答案出来或被迫停止。
- **结果为什么必须写回：**模型自己看不到外部世界，只能靠上下文里的内容做判断。结果不写回，下一轮模型就不知道工具返回了什么，没法决定继续查、换工具还是直接回答。
- **谁真正执行：**执行权在业务侧，模型只产生「想调什么」。
- **什么时候停：**两类：模型认为信息够了，输出最终答案；或者命中停止条件，包括最大轮数（常设 5 到 20）、Token 预算、总超时，还可以加重复动作检测。兜底条件必须有，不能只靠模型自己停。
- **上下文越转越长：**每轮追加观察，关键信息会被稀释，需要裁剪和摘要。
- **最少搞定三层：**模型调用、工具调用、上下文组织。
**举个例子。** 用户问「昨天充值的 100 币没到账」。
1. **第 1 轮：**模型选择查订单，观察是「已支付」，写回上下文。
2. **第 2 轮：**模型看到已支付，决定查入账流水，观察是「没有记录」。
3. **第 3 轮：**再查渠道回调记录，发现回调失败。
4. **第 4 轮：**信息够了，模型不再调工具，答复用户并提交补单申请。每一步选什么，都取决于上一步的观察。
**容易错。**
- **以为模型自己执行了工具：**模型只输出想调用什么，执行由业务侧的执行器完成。
- **以为只靠模型自己停：**模型每一轮都会给出「下一步」，必须有最大轮数、预算、超时做兜底。
- **工具结果不回填：**模型不知道结果，只能瞎猜或原地重复。
- **以为上下文越长越好：**越长越稀释关键信息，还更贵更慢。
**业务场景。** 用户问「昨天充值的 100 币没到账」：先查订单，已支付；再查入账流水，没有；再查渠道回调记录，发现回调失败；最后答复并提交补单申请。每一步都取决于上一步的观察。
**系统设计。** 对话式 AI 聊天服务（简化版 ChatGPT）：加上工具后一次回复变成多轮模型调用，追问「流式输出怎么衔接多轮调用、一次请求要占多久」。
**可能问法。**
- 讲讲 Agent 的执行流程。 → 先载入系统提示、工具列表和用户请求；模型看上下文，选择直接回答或调用工具；执行器真正执行工具，把结果作为观察追加回上下文；回到上一步继续，直到模型给出最终答案或命中最大轮数、Token 预算、超时。
- 观察结果为什么要写回上下文？ → 模型自己看不到外部世界，只能靠上下文里的内容做判断。结果不写回，下一轮模型就不知道工具返回了什么，没法决定继续查、换工具还是直接回答。
- Loop 什么时候停？ → 两类：模型认为信息够了，输出最终答案；或者命中停止条件，包括最大轮数（常设 5 到 20）、Token 预算、总超时，还可以加重复动作检测。兜底条件必须有，不能只靠模型自己停。
