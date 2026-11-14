---
id: cbr-loop-ai-assisted
node: loop.what-each-tests
type: qa
step: 3
---
## Q
Cerebras 的「允许用 AI 的面试轮」怎么进行、怎么评分、怎么准备？

## A
- **形式**：提前通知可以用 AI，而且希望你用。任务是真实的：读一个小代码库、给已有服务加功能、调查一份运维数据、改进开发工具、把不完整的需求做成原型。做完讨论扩展性、安全、可观测性、可维护性。
- **评分五项**：把问题框清楚、**验证**、判断、沟通、负责（ownership）。高级岗更看取舍和长期行为。
- **验证具体指**：交给工具前先读懂代码；给工具足够上下文；读生成的代码；能解释和调试它；测边界情况。
- **准备**：
  1. 先读代码、说出计划，再让 AI 动手。
  2. 每次生成后读 diff、跑测试、自己补一个边界用例。
  3. 说出哪些部分**没有**交给 AI、为什么。
- **你的真实习惯**："Plan with the agent, write the test first in each phase, and let CI and thresholds gate it; in money code I read every diff."
