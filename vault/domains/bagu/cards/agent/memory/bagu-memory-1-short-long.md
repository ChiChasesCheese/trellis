---
id: bagu-memory-1-short-long
node: a.agent.memory
type: qa
step: 1
---
## Q
**Agent 记忆 · 短期记忆和长期记忆的区别**｜必会

面试官：「Agent 的短期记忆和长期记忆有什么区别？各自放在哪里，怎么管？」

## A
**基本回答。** 短期记忆是当前会话的工作状态：对话历史和工具返回的中间结果，放在上下文窗口里，会话结束就没了。长期记忆跨会话保留：用户偏好、历史决策、经验教训，存在外部存储，新会话只按当前问题取回相关的几条。短期记忆太长就滑动窗口或摘要压缩旧轮次、大结果只留引用、子任务隔离上下文。
**2026 亮点。** 长任务把关键决策和待办写进外部笔记（如 NOTES.md），上下文重置后先读回来；数据只留路径，用到再取。要写决策和未解决问题，不是流水账；笔记过期或写错会误导后续步骤。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="4" y="4" width="150" height="112" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="34.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">短期：上下文窗口</text>
<text x="79.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="79.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对话历史</text>
<text x="79.0" y="79.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工具返回的中间结果</text>
<text x="79.0" y="94.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">会话结束就没了</text>
<rect x="186" y="4" width="150" height="112" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261.0" y="34.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长期：外部存储</text>
<text x="261.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="261.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户偏好</text>
<text x="261.0" y="79.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">历史决策</text>
<text x="261.0" y="94.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">经验教训</text>
<line x1="156" y1="40" x2="178.0" y2="40.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="184.0,40.0 178.0,43.0 178.0,37.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①</text>
<line x1="184" y1="84" x2="162.0" y2="84.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="156.0,84.0 162.0,81.0 162.0,87.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">②</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 对话结束后异步抽取，写入长期</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 新会话按当前问题取回相关的几条</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">短期控膨胀：摘要压缩 · 卸载引用 · 子任务隔离</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长期写入按尽力而为，重试要幂等</text>
</svg>
左边是窗口里的短期记忆，右边是外部存储的长期记忆；箭头一是写入，箭头二是取回。
**容易错。**
- **把整段旧聊天塞进新会话：**占满窗口，关键信息被稀释；应该只取回相关的几条。
- **同步写长期记忆，阻塞回复：**抽取在对话结束后异步做，用户不该为它多等；按尽力而为（best effort）设计，允许少量漏写，重试要幂等，幂等键用源消息 ID 加抽取批次 ID。
- **把长期记忆当成 RAG：**长期记忆是用户个人的、随对话写入；RAG 是外部共享的知识。
- **以为窗口够大就不用管：**上下文越长，中间的信息越容易被忽略。

