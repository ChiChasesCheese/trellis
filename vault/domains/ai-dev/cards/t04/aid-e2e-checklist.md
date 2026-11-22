---
id: aid-e2e-checklist
node: t04.end-to-end-verification
type: qa
step: 2
tags: [实践]
---
## Q
**E2E · 一份最小清单**｜实践 · 必会

agent 改了一个下单接口。你要它拿什么证据回来，才算"运行过了"？

## A
| 步骤 | 证据 |
|---|---|
| 1. 启动 | 启动命令和"ready"的日志行 |
| 2. 真实请求 | 实际 `curl` 的命令和响应体、状态码 |
| 3. 失败路径 | 故意发一个非法请求，看到预期的 4xx，而不是 500 |
| 4. 副作用 | 数据库里确实有这条订单；没有重复 |
| 5. 日志 | 没有未处理的异常；错误信息有用 |
| 6. 界面（如有） | 截图与设计稿对照 |

**做：** 把这份清单写进 prompt 或 CLAUDE.md 的"如何验证"一节；要求贴**命令和输出**。
**别做：** 接受"我测试过了"这种句子。

**出处：** Claude Code docs《Best practices》（Give Claude a check to run：ask Claude for evidence）
