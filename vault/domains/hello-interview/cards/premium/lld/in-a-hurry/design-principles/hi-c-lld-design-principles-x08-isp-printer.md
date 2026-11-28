---
id: hi-c-lld-design-principles-x08-isp-printer
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 8
---
## Q
**设计原则 · 多功能打印机接口**｜考点 · 追问

`Machine` 接口有 `print`、`scan`、`fax` 三个方法，基础款打印机被迫实现后两者为空。怎么按 ISP 改，改完怎么使用？

## A
- **拆分：** `Printer`、`Scanner`、`Fax` 三个小接口
- **组合：** 多功能机实现三个，基础款只实现 `Printer`
- **使用方：** 只声明自己需要的能力，如 `def run(p: Printer)`，传基础款也能工作
- **代价：** 接口数量变多；若总是一起使用，可合成 `MultiFunction` 组合接口
