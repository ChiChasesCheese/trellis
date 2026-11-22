---
id: aie-constrained-decoding-guardrail
node: t06.structured-outputs-constrained-decoding-guardrai
type: qa
step: 1
tags: [考点]
---
## Q
**Constrained decoding · 保证格式，不保证内容**｜考点 · 必会

团队用 constrained decoding 强制模型只输出符合 JSON schema 的内容，宣布「输出安全了」。哪里不对？

## A
**constrained sampling 做了什么：** 生成每个 token 时，把不符合语法的 logit 过滤掉，只在合法 token 里采样。所以输出**一定可解析**、字段类型一定对。

**它没保证的：**

| 没保证 | 例子 |
|---|---|
| 内容正确 | `{"refund_amount": 99999}` 语法合法，金额错了 |
| 内容安全 | 字符串字段里照样可以带注入文字、恶意链接 |
| 业务规则 | 日期合法但在未来；ID 格式对但不存在 |
| 语义对齐 | 枚举值选错类别 |

**所以仍然要：**
1. **业务校验：** 范围、枚举、外键存在性、权限（把输出当 untrusted input）；
2. **不要把字符串字段直接拼进 SQL、命令、HTML**；
3. 重要字段做二次检查（规则或另一次模型判断）。

**代价：**
- 每种格式（JSON、YAML、regex、CSV）需要自己的 grammar，通用性差；
- 语法验证可能增加生成延迟；
- 有人认为这些资源不如用来训练更会遵循指令的模型。

**与 post-processing 的对比：** 约束解码在生成时挡住格式错误；post-processing 事后修补。无论哪种，都只解决**可解析**问题。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch2 §Constrained sampling；§Structured Outputs

</details>
