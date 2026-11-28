---
id: hi-c-lld-patterns-x08-over-patterned
node: lld.in-a-hurry.patterns.exam
type: qa
step: 8
---
## Q
**设计模式 · 模式堆太多**｜考点 · 追问

停车场设计里你用了 Singleton、Factory、Builder、Observer、Strategy 五个模式，面试官让你只留真正需要的。你怎么删？

## A
- **先问每个模式解决的具体问题**，答不出就删
- **Singleton：** 删，用构造参数传入
- **Builder：** 车位、票据字段很少，删
- **Factory：** 车型固定且创建点只有一处时删
- **可能保留：** Strategy，如果计费规则多种且可切换；Observer，如果需求里有"车位满了要通知显示屏"
- 最后留下 0 到 2 个，并说出每个对应哪条需求
