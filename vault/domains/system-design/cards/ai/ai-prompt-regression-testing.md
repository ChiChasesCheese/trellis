---
id: ai-prompt-regression-testing
node: ai.evals
type: qa
---
## Q
A teammate "just tweaks the prompt" in production config, and a provider model upgrade lands next month. What discipline prevents these from silently breaking your AI feature?

## A
Treat **prompt + model version + parameters as one deployable artifact**:

- Prompts live in **version control**, not a dashboard textbox; every change goes through the offline eval suite in CI like any code change.
- **Pin exact model versions** — a prompt is tuned against one model's behavior, and "same prompt, new model" is a breaking-change risk with no compile error.
- Provider **deprecations force migrations**, so re-running the full eval suite against the new model is the migration test plan.
- Edits fix the case in front of you and regress cases you're not looking at — only the suite catches the trade.

## Q zh
一个队友在生产配置中"只是调整 prompt"，提供商模型升级下个月到来。什么纪律防止这些默默地破坏你的 AI 功能？

## A zh
把 **prompt + 模型版本 + 参数视为一个可部署的工件**：

- Prompt 存在于 **版本控制** 中，而不是仪表板文本框；每次更改都通过离线 eval 套件在 CI 中进行，就像任何代码更改一样。
- **固定精确的模型版本** — prompt 针对一个模型的行为进行了调整，"相同的 prompt，新模型"是一个没有编译错误的破坏性更改风险。
- 提供商 **弃用强制迁移**，所以针对新模型重新运行完整的 eval 套件是迁移测试计划。
- 编辑修复了你面前的情况并回归你没有看的情况 — 只有套件捕捉权衡。
