---
id: nr-amz-s11-starl
node: amazon.s11
type: qa
step: 2
---
## Q
【实习期：Kafka 事件流 · Spring · Spark（广度补充）】STAR-L 提纲（60–90 秒）

## A
**S**

- **2024** 年夏天实习，费用平台团队的事件流一侧
- 结算交易发布 **protobuf 事件到 Kafka**；定价服务**幂等**入账并发布费用事件

**T**

- 扩展线上 **Kafka → Snowflake 的 CDC 路径**
- 另有两个小件：**审计日志模块**和 **EOD 校验器**

**A**

- 把 **Kafka Connect sink** 扩展到 Snowflake（**Snowpipe Streaming**）
- 写**自定义 protobuf converter**：遇到坏消息返回 **null 记录**，不让 task 死掉
- 加 **CDC 过滤**：表白名单，**丢弃 delete**
- 写 **Spring Boot + JPA 审计日志模块**，动态 criteria 查询
- 写 **Spark 校验器**，**Airflow** 调度，EOD 检查定价计划来源

**R**

- 一个夏天**三个交付物**：CDC 扩展、审计日志、Spark 校验器
- 无业务数字

**L**

- **At-least-once + 幂等消费者** = 实际上的恰好一次
- **一条坏消息不能毒死管线**；和后来 Amex 管线的 "record, never drop" 是同一直觉
