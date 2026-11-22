---
id: aid-e2e-ui
node: t05.end-to-end-ui-browser-automation
type: qa
step: 1
tags: [摘要]
---
## Q
**E2E 与 UI 测试 · browser automation**｜摘要 · 追问

让 agent 做一个界面功能，它怎么知道页面真的对了？成本和脆弱点在哪？

## A
**browser automation＝让 agent 操作真实浏览器：打开页面、点击、截图，再对照设计稿或预期。**

| 作用 | 例 |
|---|---|
| 检查 | 截图与设计稿对照；点完"保存"看到成功提示 |
| 发现单元测试看不到的 | 样式被覆盖、按钮被遮住、路由没注册 |

**脆弱点：**
- 选择器依赖页面结构，界面一改测试就坏；
- 时序：异步加载，需要等待条件而不是固定 sleep；
- 浏览器原生弹窗等，agent 可能看不到（Anthropic 实验里 Claude 看不到浏览器原生的 alert 弹窗，依赖它们的功能更容易出错）；
- 成本：每次截图、读页面都占 context；一次完整流程比单元测试贵得多。

**做：** 只对关键用户路径做 E2E；其余靠单元和集成测试。
**别做：** 把所有测试都做成 E2E。

**出处：** Anthropic Engineering《Effective harnesses for long-running agents》（Testing）；Claude Code docs《Best practices》（Give Claude a check to run：浏览器截图）
