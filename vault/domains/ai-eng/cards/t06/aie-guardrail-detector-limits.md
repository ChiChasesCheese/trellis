---
id: aie-guardrail-detector-limits
node: t06.guardrail-detector
type: qa
step: 1
tags: [考点]
---
## Q
**Guardrail detector · 「拦住 95%」够不够**｜考点 · 必会

供应商宣称它的 prompt-injection 检测器「能拦住 95% 的攻击」。安全团队该不该把它当作防线？

## A
**不该。** 在 web 应用安全里，95% 是不及格：攻击者只需要找到剩下的 5%，而且可以自动反复试。Simon Willison 对这类产品「深表怀疑」，因为至今没人知道怎么 100% 可靠地防住提示注入。

**检测器的结构性局限：**

| 局限 | 原因 |
|---|---|
| 漏放 | 攻击样式无限，检测器只认已知模式或自己学到的分布；自动化攻击（如用一个攻击模型反复改写 prompt）通常二十次以内查询就能找到绕过 |
| 误杀 | 过严就拒绝正常请求；用 **false refusal rate** 衡量，和 **violation rate**（攻击得手的比例）必须一起看，一个「全拒」系统的 violation rate 为零但毫无用处 |
| 延迟 | 每多一层检测就多一次判断；有的团队因此不上 guardrail |
| streaming | 流式输出时难以评估半截回答，不安全内容可能在被拦之前已经发给用户 |

**正确用法：** 检测只是**一层**，不是边界。
1. 先用架构把后果限制住：最小权限、拆开 lethal trifecta、高风险操作要人工批准；
2. 再把检测器当作额外一层，降低被碰到的概率，并用攻击成功率衡量；
3. 默认假设检测器会被绕过，设计「被绕过之后最坏会发生什么」。

**出处：** Huyen《AI Engineering》ch10 §Guardrail implementation；ch5 §Defenses Against Prompt Attacks；Willison《The lethal trifecta》simonwillison.net/2025/Jun/16/the-lethal-trifecta/（2026-11-21 读）
