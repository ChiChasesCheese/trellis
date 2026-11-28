---
id: bagu-memory-5-pollution-cold-start
node: a.agent.memory
type: qa
step: 5
---
## Q
**记忆污染与冷启动 · 写入门和取出门**｜追问

面试官：「记忆越存越多，怎么避免污染上下文？新用户一条记忆都没有时怎么办？」

## A
**基本回答。** 污染来自写太多或写错，所以在两头设门。写入门：用规则或重要度打分挡掉寒暄和临时猜测；多次跨会话验证过的偏好才升级为长期记忆；写前对个人敏感信息脱敏。取出门：只放最相关的几条，带来源，设数量和 Token 上限。冷启动时新用户前几轮只靠当前对话理解意图，用追问或行为信号形成「假设」但不写死，被多次验证后才入库。宁可不写，也不写错。
**一句话记住。** 记忆库像一本只记确认过的事实的账本：入口有门卫（写入门），不确定的传闻不记；出口有秘书（取出门），只递最相关的几页。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<rect x="10" y="4" width="190" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对话里出现的信息</text>
<rect x="10" y="46" width="190" height="76" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="105.0" y="65.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入门</text>
<text x="105.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">挡寒暄和临时猜测</text>
<text x="105.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多次跨会话验证才升级</text>
<text x="105.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">敏感信息先脱敏</text>
<rect x="226" y="66" width="110" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="281.0" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被挡下</text>
<text x="281.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">寒暄、假设语气</text>
<line x1="200" y1="86" x2="220.0" y2="86.0" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="226.0,86.0 220.0,89.0 220.0,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="140" width="190" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="157.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长期记忆（带来源）</text>
<rect x="10" y="184" width="190" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="105.0" y="204.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取出门</text>
<text x="105.0" y="219.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只放最相关的几条</text>
<text x="105.0" y="234.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带来源，设数量和上限</text>
<rect x="10" y="262" width="190" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="276.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进入上下文</text>
<line x1="105" y1="30" x2="105.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105.0,46.0 102.0,40.0 108.0,40.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="105" y1="122" x2="105.0" y2="132.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105.0,138.0 102.0,132.0 108.0,132.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="105" y1="166" x2="105.0" y2="176.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105.0,182.0 102.0,176.0 108.0,176.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="105" y1="246" x2="105.0" y2="256.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105.0,262.0 102.0,256.0 108.0,256.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="214" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">冷启动：</text>
<text x="214" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只靠当前对话，</text>
<text x="214" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">形成假设不写死</text>
</svg>
信息从上往下流：先过写入门，挡下的不入库；入库后取出时再过一道门，只放几条进上下文；右下角是新用户怎么办。
**讲明白。**
- **污染从哪里来：**写太多或写错。写错的记忆会在每次回答里反复出现，很难靠改提示词纠正。
- **写入门：**规则或重要度打分挡掉寒暄和临时猜测；多次跨会话验证过的偏好才升级为长期记忆；写前对个人敏感信息脱敏。假设语气（可能、也许）不入库；冲突信息要把旧值标记失效并记录时间，不直接覆盖；还要定期合并去重、淘汰过期条目。
- **取出门：**只放最相关的几条，带来源，设数量和 Token 上限。带来源，出了问题才能定位是哪条记忆造成的。
- **写入要幂等：**写入带幂等键，防止重试产生重复记忆。
- **冷启动怎么办：**新用户没有记忆，前几轮只靠当前对话理解意图，必要时追问一两个关键信息。可以用行为信号或群体默认值形成「假设」，但假设不写入长期记忆，等被多次验证后才入库。宁可不写，也不写错。
- **记忆投毒：**恶意内容也可能被写进记忆，所以记忆要带来源，出错时能按来源查出并批量清理。
- **用户的控制权：**用户应能查看和删除自己的记忆。
**举个例子。** 用户随口说了一句「我可能会买最贵的那款」。
1. **写入门判断：**这是假设语气，不入库。
2. **如果误入库：**被固化成「偏好高价」，之后每次推荐都偏贵，用户还看不出原因。
3. **什么时候才升级：**用户在多个会话里反复选了贵的款式，多次验证之后，才升级成长期偏好。
4. **新用户第一次来：**没有任何记忆，只靠当前对话；必要时问一两个关键信息，形成的「假设」只放在当前会话里。
**容易错。**
- **以为记得越多越好：**写太多会污染上下文，写错的更会反复出现。
- **把用户的假设当事实：**「可能」「也许」不是偏好，不能入库。
- **取出时全塞进上下文：**要只放最相关的几条，带来源，设上限。
- **写入重试不做幂等：**同一条记忆会被重复写入。
**业务场景。** 用户随口说「我可能会买最贵的那款」。若被固化成「偏好高价」，之后推荐一直偏贵；按规则，假设语气不入库。
**系统设计。** [[links.video-moderation-system|视频内容审核系统]]：发布前先审再放行，与记忆的写入门相近，写入前先检查。差异是审核对象是公开内容，记忆是用户私有数据，还要支持用户删除。
**可能问法。**
- 记忆太多影响效果怎么办？ → 两头设门。写入门用规则或重要度打分挡掉寒暄和临时猜测，多次跨会话验证过的才升级为长期记忆，还要定期合并去重、淘汰过期条目。取出门只放最相关的几条，设数量和 Token 上限，并带来源，便于定位是哪条记忆造成的问题。
- 新用户没有记忆怎么办？ → 冷启动时只靠当前对话理解意图，必要时追问一两个关键信息。可以用行为信号或群体默认值形成「假设」，但假设不写入长期记忆，等被多次验证后才入库。宁可不写，也不写错。
- 怎么防止记错？ → 写入前加门槛：假设语气（可能、也许）不入库，冲突信息要把旧值标记失效并记录时间、不直接覆盖，敏感信息先脱敏。写入带幂等键，避免重试产生重复记忆。用户可以查看和删除自己的记忆，记忆带来源，出错时能按来源追查并批量清理。
