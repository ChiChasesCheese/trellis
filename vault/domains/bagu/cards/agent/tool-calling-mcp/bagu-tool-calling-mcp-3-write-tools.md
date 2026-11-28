---
id: bagu-tool-calling-mcp-3-write-tools
node: a.agent.tool-calling-mcp
type: qa
step: 3
---
## Q
**写操作工具 · 权限、二次确认、幂等、审计**｜必会

面试官：「Agent 有『发起退款』这类写操作工具，你怎么保证它不会乱退、不会退两次？」

## A
**基本回答。** 原则是模型只提议，系统决定能不能做。写操作至少过四关。权限：按用户、租户、资源 ID 在服务端鉴权，不信模型传的身份。二次确认：拆成 `prepare_refund`（生成预案，展示金额和原因）和 `confirm_refund`（用户确认后才执行）。幂等：幂等键由可信执行层按业务请求 ID 和动作生成，不让模型提供，数据库唯一约束兜底。审计：记录模型提议、最终参数、执行人和结果，敏感字段脱敏。
**2026 亮点。** 远程 MCP 在往无状态演进：每个请求自带协议版本与能力，负载均衡可直接按 HTTP 头路由；代价是断流后在途请求会丢、客户端要用新请求 ID 重发，所以写工具的幂等键必须来自业务请求 ID，不能绑定传输层的请求或会话。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<rect x="6" y="4" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型提议 refund(1029)</text>
<text x="168" y="23" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只是提议，不可信输入</text>
<line x1="81" y1="34" x2="81.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,50.0 78.0,44.0 84.0,44.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="50" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 权限：服务端鉴权</text>
<text x="168" y="69" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按用户、租户、资源 ID</text>
<line x1="81" y1="80" x2="81.0" y2="90.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,96.0 78.0,90.0 84.0,90.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="96" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② prepare_refund</text>
<text x="168" y="115" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">生成预案：金额和原因</text>
<line x1="81" y1="126" x2="81.0" y2="136.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,142.0 78.0,136.0 84.0,136.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="142" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="81.0" y="161.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 用户确认 → confirm</text>
<text x="168" y="161" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">确认时重新校验订单状态</text>
<line x1="81" y1="172" x2="81.0" y2="182.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,188.0 78.0,182.0 84.0,182.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="188" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81.0" y="207.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 幂等键 + 唯一约束</text>
<text x="168" y="207" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">键由执行层生成，不由模型</text>
<line x1="81" y1="218" x2="81.0" y2="226.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,232.0 78.0,226.0 84.0,226.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="232" width="328" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="251.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑤ 审计：提议、最终参数、执行人、结果</text>
</svg>
从上到下是一次退款的路径：模型只是第一步的提议，后面每一关都由系统把守，最后留审计记录。
**容易错。**
- **让模型生成幂等键：**它每次重试可能生成不同的键，等于没有幂等。
- **确认凭证不绑定参数：**用户确认的是 50 元，执行时却被改成 500 元；凭证要绑定参数、用户和有效期，一次性消费。
- **确认时不再校验状态：**等待期间订单可能已经变了，会重复退款或退错。
- **把「只能退本人订单」写在提示词里当权限：**提示词不是安全边界，要在服务端按用户和资源 ID 校验。
- **工具按风险分级：**只读（限流和日志）、可逆写（幂等）、高风险如退款（确认加额度）、极高风险如删数据（默认禁止或走审批）。不能安全重试的工具，就不该让 Agent 随意调用。
**业务场景。** 用户在确认页等了 10 分钟，其间订单已被人工退款；确认时重新读取订单状态，发现已退款，拒绝再退。
