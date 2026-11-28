---
id: bagu-tool-calling-mcp-1-fc-chain
node: a.agent.tool-calling-mcp
type: qa
step: 1
---
## Q
**Function Calling · 一次工具调用的完整链路**｜必会

面试官：「用户说『帮我查订单 1029 到哪了』，从这句话到 Agent 给出回答，Function Calling 的链路是什么？模型真的执行了函数吗？」

## A
**基本回答。** 模型不执行函数，它只生成「调用意图」，真正执行在业务侧。链路是四步：服务端先注册工具，写明名称、用途描述和参数 Schema；模型选中 `query_order`，填出参数 `{"orderId": "1029"}`；业务侧校验参数、权限和订单归属，再执行真实调用；结果连同 `tool_use_id` 原样回填给模型，模型据此生成回答。
**2026 亮点。** 参数可让引擎按 JSON Schema 约束解码，语法错误基本消失，MCP 的工具结果也可声明 schema；但只保证语法，参数范围、资源归属和权限仍要服务端校验。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<rect x="4" y="4" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户</text>
<rect x="135" y="4" width="70" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型</text>
<rect x="266" y="4" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="301.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务侧</text>
<line x1="39" y1="30" x2="39" y2="240" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="170" y1="30" x2="170" y2="240" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="301" y1="30" x2="301" y2="240" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="104" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查订单 1029 到哪了</text>
<line x1="39" y1="60" x2="164.0" y2="60.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,60.0 164.0,63.0 164.0,57.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="235" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">query_order，id=t1</text>
<line x1="170" y1="96" x2="295.0" y2="96.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="301.0,96.0 295.0,99.0 295.0,93.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="235" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">校验权限、归属</text>
<text x="235" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再由业务侧执行</text>
<text x="235" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结果 + id=t1</text>
<line x1="301" y1="182" x2="176.0" y2="182.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,182.0 176.0,179.0 176.0,185.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="104" y="210" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回答</text>
<line x1="170" y1="216" x2="45.0" y2="216.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="39.0,216.0 45.0,213.0 45.0,219.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
模型和业务侧是两个角色：模型只发出意图，业务侧校验并执行，结果带着编号 t1 回来，对上号再回答。
**容易错。**
- **以为模型自己调了接口：**模型只产出意图，执行在业务侧。
- **以为提示词里写「不要越权」就安全：**模型可能被诱导，服务端要校验用户身份、资源归属和参数范围，写操作还要二次确认和审计。
- **并行调用时结果不带 id：**模型分不清哪个结果对应哪个调用，会张冠李戴。
- **工具描述一笔带过：**模型靠描述选工具，描述含糊就会选错或乱用。

**业务场景。** 用户在 App 里问别人的订单号：模型照样生成 `query_order` 调用，服务端发现订单不属于当前用户，拒绝执行。
