---
id: principles-yagni-in-round
node: principles.simplicity
type: qa
---
## Q
In the machine coding round, how do you reconcile YAGNI with the interviewer's known love of extensibility probes?

## A
**Build seams, not features.** An interface at a variation point the requirements actually signal (pricing, spot allocation) costs one file and makes the probe answer additive. Don't build unrequested capability — config systems, factories over a single implementation, generics "for later."

When probed about something you skipped, pointing at the seam where it plugs in scores; dead speculative code reads as poor judgment, not foresight.

## Q zh
在迭代开发中应用 YAGNI 是什么样子？

## A zh
YAGNI（你不需要它）意味着不要添加你现在不需要的功能。在迭代中：

第一次迭代：
- 实现最小的东西来传递测试
- 不要"预计"分支、扩展、配置

第二次迭代：
- 需要第二个实现者或变化吗？现在进行抽象
- 发现重复的代码吗？现在提取它

这与投机泛化相反。结果代码更简单、更易理解、更快交付。反讽刺的是，YAGNI 导致比过度工程的代码更长久的架构。
