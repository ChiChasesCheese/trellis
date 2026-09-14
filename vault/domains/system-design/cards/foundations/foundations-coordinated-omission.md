---
id: foundations-coordinated-omission
node: foundations.numbers
type: qa
---
## Q
Your load-test harness sends a request, waits for the response, then sends the next. Name the measurement error and the fix.

## A
**Coordinated omission**: by waiting, the harness backs off *exactly when the system is slow*, so queueing delay vanishes from the data — you measured service time, not response time, and high percentiles come out wildly optimistic.

Fix: generate load on a **fixed schedule independent of responses**, and clock each request from its *scheduled* send time, so time spent waiting behind a stall is counted. Measure at the client, where users actually wait.


## Q zh
你的负载测试工具发送请求、等待响应、然后发送下一个。这个测量误差叫什么，怎么修复？

## A zh
**协调遗漏（coordinated omission）**：通过等待，工具正好在系统变慢时退避，所以队列延迟从数据中消失 — 你测量的是服务时间，不是响应时间，高百分位看起来太乐观了。

修复：按**固定时间表生成负载，独立于响应**，从**计划**发送时刻给每个请求计时，所以等待在停滞后面的时间被计入。在客户端测量，用户实际等待的地方。
