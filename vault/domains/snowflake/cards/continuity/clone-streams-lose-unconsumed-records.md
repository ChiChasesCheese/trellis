---
id: clone-streams-lose-unconsumed-records
node: continuity.zero-copy-clone
type: qa
source: snowflake-docs
---
## Q
克隆一个包含源表和流（Stream，记录表变更的对象）的模式后，克隆里的流还能读出源流中尚未消费的变更吗？

## A
不能，克隆中流里尚未消费的记录不可访问。这与表的时间旅行（Time Travel）行为一致：表被克隆后，克隆表的历史从克隆创建的那一刻才开始，克隆之前的变更历史不属于克隆表，流也就无从读取。
