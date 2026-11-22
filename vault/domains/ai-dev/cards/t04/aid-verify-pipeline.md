---
id: aid-verify-pipeline
node: t04.verification-generation-review-bottleneck
type: qa
step: 2
tags: [实践]
---
## Q
**审查变成流程**｜实践 · 必会

团队决定"AI 写的代码必须经过验证"。流程里要放哪几道关，各挡什么？

## A
| 关 | 谁执行 | 挡什么 |
|---|---|---|
| 1. agent 自己跑 check | agent（Stop hook 强制） | 编译错误、类型错误、明显的测试失败 |
| 2. CI | 机器 | 在干净环境里复现；防"在我的 session 里通过" |
| 3. 对照 spec 的独立审查 | 另一个 session 或模型 | 漏实现的需求、缺的边界测试 |
| 4. 人的审查 | 提交者 + 审查者 | 设计是否合理、是否读懂、安全 |
| 5. 合并保护 | 分支规则 | 绕过前面所有关的路径 |

**做：** 越靠前的关越便宜、越自动；人只在 3、4 看机器看不到的。
**别做：** 让第 4 关承担全部（它是最贵、最容易疲劳的一关）。

**官方框架：** 谁有"最后一句话"——不是 agent 的总结，而是测试、CI、分支保护和批准合并的人。

**出处：** Claude Code docs《Best practices》（Deterministic and non-deterministic instructions 表：Who has the last word）
