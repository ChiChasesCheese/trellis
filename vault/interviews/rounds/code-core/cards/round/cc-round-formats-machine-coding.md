---
id: cc-round-formats-machine-coding
node: round.formats
type: qa
---
## Q
A 90-minute machine-coding round asks for a working in-memory system that the interviewer will actually run at the end. What is being graded, and what is a waste of that clock?

## A
**A running demo plus the shape of the code**: responsibilities split sensibly, and one obvious place to add the next rule.

- Graded: does it run on the stated flows; could a reviewer add a feature without editing five files; are the invariants enforced in one place.
- Wasted: full class diagrams, persistence, a framework, or validation nobody asked for.
- Build the core flow end-to-end in the first half so extensions land on something that already runs — an unrunnable design is scored as zero flows, not as a nice design.

## Q zh
一个 90 分钟的 machine coding 轮要求交出一个能跑的内存系统，面试官最后会真的运行它。这在评什么，而什么是在浪费时间？

## A zh
**一个能跑的 demo，加上代码的形状**：职责划分合理，并且有一个显而易见的地方可以加下一条规则。

- 评分点：既定流程能不能跑通；别人加功能是否要改五个文件；不变量是否只在一处强制。
- 浪费：完整类图、持久化、引入框架、没人要求的校验。
- 前一半时间把核心流程端到端跑通，扩展才有东西可落。跑不起来的设计按"零个流程"计分，而不是按"设计不错"计分。
