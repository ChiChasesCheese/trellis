---
id: aie-guardrails-tradeoffs
node: t06.input-output-guardrails
type: qa
step: 2
tags: [考点]
---
## Q
**Guardrails · 误杀、漏放与延迟**｜考点 · 必会

产品用流式输出（边生成边显示）。你想加一个"有毒内容"输出检查。会遇到什么问题？还要权衡什么？

## A
**问题 1：流式输出与输出检查冲突。** 默认是整段生成完才显示；流式是每生成一个 token 就推给用户，等待更短，但**很难评估不完整的回答**，不安全的内容可能在被拦截之前已经显示出去了。

| 方案 | 做法 |
|---|---|
| 先缓冲再放行 | 攒一小段检查完再推送，延迟略增 |
| 检查已经发出的部分 | 发现问题就中止并撤回，用户可能已看到一部分 |
| 关键场景不用流式 | 安全优先时放弃流式 |

**问题 2：reliability 与 latency 的取舍。** 有些团队认为延迟更重要，**决定不上 guardrails**，因为它们会显著增加延迟。

**问题 3：误杀。** 不只统计安全失败，还要看 **false refusal rate**（本可以安全回答却被拒绝的比例）。过度安全的系统会阻碍正常使用、让用户沮丧。

**问题 4：自托管还是 API。** 用第三方 API，供应商通常已内置一些 guardrails，要自己做的少；自托管则不需要把请求发到外部，也少了很多输入端的防护需求。

**检查清单：**
1. 每一层误杀率与漏放率各是多少（在评测集上测）；
2. 每一层增加多少延迟和成本；
3. 触发率有监控吗（被拦截多少、重试多少、转人工多少）；
4. 防线之外有没有设计层面的限制（最小权限）。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch10 §Guardrail implementation；ch5 §Defenses Against Prompt Attacks（false refusal rate）

</details>
