---
id: s20-self-test-discipline
node: stripe.solving
type: qa
---

## Q
自测时最容易漏掉的一步是什么？写了测试就等于测试有效吗？

## A
见 `09-debug-and-selftest.md`。核心三条：
1. 样例**复制粘贴**跑，不手敲。
2. 每个 part 自己编 2–3 个边界。
3. **确认测试真的会失败** —— 把实现改坏一行，测试必须变红。不会红的测试等于没写。
