---
id: aid-e2e-run-it
node: t04.end-to-end-verification
type: qa
step: 1
tags: [摘要]
---
## Q
**运行它 · end-to-end verification**｜摘要 · 必会

agent 说"功能完成，类型检查和单元测试通过"。你为什么还要让它真的把服务跑起来？

## A
**类型检查和单元测试都不是"功能正确"。** 它们验证的是模块内部和 mock 之后的行为；真实环境里的配置、网络、数据库、前端渲染不在其中。

**end-to-end verification：** 启动服务、发真实请求、看日志，必要时在浏览器里看界面。

| 层 | 能发现 | 发现不了 |
|---|---|---|
| type check | 类型不匹配 | 逻辑错误 |
| unit test | 单个函数的错误 | 组件之间的连接、真实配置 |
| **e2e** | 启动失败、路由没注册、接口约定对不上 | 没写成检查的需求 |

**Anthropic 的发现（长任务实验）：** agent 常常只做了单元测试或 `curl` 检查就把功能标成完成；提示它用浏览器自动化、像真实用户那样测试，结果明显改善。

**官方做法：** 完成后让它跑 `/verify`，构建、运行应用并查看结果，抓测试和类型检查漏掉的问题。

**出处：** Anthropic Engineering《Effective harnesses for long-running agents》（Testing）；Claude Code docs《Best practices》（Give Claude a check to run）
