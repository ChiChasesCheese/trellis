---
id: ail-work-app-architecture-trace-and-guardrails
node: work.app-architecture
type: qa
step: 3
---
## Q
客户发来截图：HR 机器人把年假天数答错了，你却复现不出来。上线后该记什么？护栏又该放在哪、花多少代价？

## A
**每个请求记一条完整轨迹（trace）：当时的提示版本、模型、检索到的片段、token 和耗时；没有它，出错只能猜。**

```json
{
  "trace_id": "t-8f2",
  "prompt_version": "hr-v14",
  "model": "sonnet-5.5", "effort": "low",
  "retrieved": ["doc-12#3", "doc-40#1"],
  "tool_calls": [],
  "tokens": {"in": 5120, "out": 310, "cached": 4800},
  "latency_ms": 2300,
  "guardrail": "pass"
}
```

- **复现：** 同样的提示版本、检索片段和模型，就能重放。这条里 `doc-12` 若是旧版制度，根子就在检索，不在模型。
- **账单：** 按提示版本、模型和强度分组，能看出费用从哪里来。
- **护栏的代价：** 规则型（正则、格式校验）几乎免费；再调一次模型做检查，会多一次延迟和费用，还会误杀。
- **隐私：** 原文里常有个人信息，要脱敏或设短保留期。

**新进展（2026 年 6 月）。** OpenTelemetry 把生成式 AI 的追踪约定搬进了独立仓库：模型调用、`invoke_agent`、`execute_tool` 各是一种 span；智能体和工具这部分仍标为"开发中"，记录提示和回答原文默认关闭，要使用方自己打开。

<details class="pt"><summary>想一想：为什么标准把"记录提示和回答原文"设成可选？</summary>提示和回答里常含个人或机密信息，默认全记会带来合规风险。所以要由使用方按场景决定记多少、记多久。</details>
