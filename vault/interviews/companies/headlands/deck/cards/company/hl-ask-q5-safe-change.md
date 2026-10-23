---
id: hl-ask-q5-safe-change
node: company.questions-to-ask
type: qa
step: 6
---
## Q
反问面试官："24 小时系统怎么安全变更"，英文怎么问？为什么好，好 / 坏答案各透露什么？

## A
> "The system trades around the clock. How do you test and roll out an infrastructure change so that it never needs a maintenance window — and what does a bad deploy look like here?"

- **为什么好**：JD 要 fully automated, scalable, maintainable solutions with extensive testing；系统 24 小时运行，又说生产变更几周内就能上线——快和稳同时成立，是怎么做到的？
- **好答案**：分层测试（模拟 / 对账 / 灰度）、有回滚、有"出过什么事故后改了什么"的具体例子。
- **坏答案**："我们很小心"或"有时凌晨手工改"。迭代快又没有安全网，通常靠个人英雄主义，你要在 on-call 里付出代价。
