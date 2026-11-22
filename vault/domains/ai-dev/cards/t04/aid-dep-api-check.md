---
id: aid-dep-api-check
node: t04.dependency-api
type: qa
step: 2
tags: [实践]
---
## Q
**API 核实 · 过时用法**｜实践 · 必会

agent 用了 `library.connect(url, timeout=5)`，能跑，但你的版本文档里这个参数已经改名。怎么系统地防这类问题？

## A
| 手段 | 做法 |
|---|---|
| 把文档给它 | 用 `@` 引入文档文件，或让它查官方文档页面，而不是凭记忆写 |
| 锁版本 | 锁文件里固定版本，并在 CLAUDE.md 里写"使用 X 版本" |
| 编译/类型检查 | 静态类型能挡住大部分不存在的方法；动态语言要靠测试 |
| 弃用警告当错误 | 测试和 CI 里开启，过时用法立刻红 |
| 审查时查新增 import | diff 里每个新 import 和新 API 调用都对一遍文档 |

**做：** 让它改完把用到的外部 API 列出来，附文档链接，你抽查。
**别做：** 因为"跑起来了"就相信——旧用法常常还能跑，只是行为变了或被标记弃用。

**出处：** Claude Code docs《Best practices》（Tell Claude what it can't see：@ 引入文件；Connect the tools：Web 工具查文档）
