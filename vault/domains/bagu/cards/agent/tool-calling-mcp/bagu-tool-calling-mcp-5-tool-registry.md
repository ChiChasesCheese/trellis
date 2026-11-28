---
id: bagu-tool-calling-mcp-5-tool-registry
node: a.agent.tool-calling-mcp
type: qa
step: 5
---
## Q
**工具很多 · 100 个工具怎么管，注册中心怎么设计**｜追问

面试官：「Agent 有 100 个工具，全放进提示词会怎样？工具注册中心怎么设计？」

## A
**基本回答。** 工具太多，全放进提示词会撑大上下文，也让模型选错。思路是注册中心加检索加分层暴露。注册中心保存每个工具的名称、描述、参数 Schema、风险等级、权限标签、版本；每轮先按任务检索出相关的 5 到 10 个工具再交给模型，不是 100 个全给；合并功能重叠的工具，重写描述，写清「何时用、何时不用」；高风险工具由代码按权限过滤，不暴露给无权的用户。用混淆矩阵（该选 A 却被选成 B 的次数）找常被选错的工具对，再改它们的描述；工具要有版本和灰度，不兼容变更会改变模型判断。
**2026 亮点。** 工具上百个时渐进式暴露：先只给工具名，需要时按名字或描述检索，最后才加载完整 schema；大结果让 Agent 写代码在沙箱里过滤，个别案例能把十几万 token 降到约两千。`tools/list` 要保持确定顺序，否则前缀缓存失效。代价是多维护沙箱和监控，只有十来个工具时全部暴露更省事。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="4" width="324" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="21.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">注册中心：100 个工具</text>
<text x="170.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">名称·描述·Schema·风险·权限·版本</text>
<rect x="34" y="64" width="272" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">代码按权限过滤</text>
<text x="170.0" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高风险不暴露给无权的用户</text>
<rect x="62" y="124" width="216" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按任务语义检索</text>
<text x="170.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取最相关的 5 到 10 个</text>
<rect x="100" y="184" width="140" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">交给模型</text>
<text x="170.0" y="217.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5~10 个工具</text>
<line x1="170" y1="46" x2="170.0" y2="58.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,64.0 167.0,58.0 173.0,58.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="106" x2="170.0" y2="118.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,124.0 167.0,118.0 173.0,118.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="166" x2="170.0" y2="178.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,184.0 167.0,178.0 173.0,178.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
一百个工具像漏斗一样逐层缩小：先过滤掉没权限的，再按任务挑最相关的几个，最后才交给模型。
**容易错。**
- **把所有工具都交给模型自己挑：**上下文变大、选错率变高，还多花 Token。
- **工具描述只写一句功能：**没写「何时不用」，相近工具互相抢着被选。
- **权限靠提示词约束：**模型可能被诱导，要在代码里过滤。
- **随意增删工具不管缓存：**列表一变，提示词缓存整体失效，成本和延迟上升；可保持列表不变，用状态机屏蔽当前不可用的工具。

**业务场景。** 支付相关工具有查订单、查支付单、查退款、发起退款等几十个，名称相近。用户问「钱怎么还没到账」，只暴露查询类工具，发起退款默认不进候选。
