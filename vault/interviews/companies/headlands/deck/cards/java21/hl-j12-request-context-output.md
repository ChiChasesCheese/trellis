---
id: hl-j12-request-context-output
node: java21.j12-scoped-values
type: qa
step: 16
---
## Q
请求上下文实验里，`fork` 出的两个虚拟线程、用 `Thread.ofVirtual().start` 开的野线程、第二个请求，分别打印出什么上下文？这说明了什么？

## A
- `fork` 出的「取额度」「取行情」子线程仍带 `t-001/ACC-7`：**继承生效**。
- 用 `Thread.ofVirtual().start` 开的野线程打出 `<无上下文>`：**不继承**。
- 第二个请求带 `t-002/ACC-9`，与第一个**不串号**：绑定随 `call` 返回消失。

结论：只有结构化并发继承；绑定随块结束自动消失，不会泄漏到下一个请求。
