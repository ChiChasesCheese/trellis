---
nodes: [measurement.coordinated-omission, measurement.distributions, measurement.histograms, measurement.timestamps]
tags: [drill]
---
# 练习：一份漂亮的延迟报告，凭什么不能信

压测工具按"发一个请求、等响应、再发下一个"的方式工作，目标速率每毫秒 1 个，共跑 10 秒，应有 10000 个请求。系统正常时 1 ms 响应，中间卡了 1 秒。报告写着 p99.9 约 1 ms，非常稳。另一份报告的目标是每秒 1000 个、测 60 秒，只记录了 5.4 万个样本。

**要你给出的**
- 算出这份报告漏掉了什么：工具记录了多少样本，真实的 p99 大约是多少。
- 写出至少 3 个判断一份延迟报告被污染的迹象，并判断第二份报告出了什么问题。
- 给出两种修正办法，解释闭环和开环测试的区别；再说明测行情处理延迟时起点应该取哪里。
- 回答两个追问：5 台机器各报了 p99，能不能取平均当整体 p99；一条流程经过 10 个环节、每个环节 99% 的时候都快，整条流程遇到慢环节的概率约多少。

**评分要点**
- 机制：工具卡住时自己也不再发请求，本该在卡顿期间到达的请求没有被记录，最慢的部分就和被测系统"协同"漏掉了 ([[hft-measurement-coordinated-omission-mechanism]])
- 数字：工具记录约 9000 个 1 ms 样本加 1 个 1 s 样本；真实情况是卡顿的 1 秒里本该有 1000 个请求，等待时间从约 1 秒递减到 1 ms，真实 p99 约 0.9 秒，被低估约一千倍 ([[hft-measurement-coordinated-omission-mechanism]])
- 识别迹象：记录的请求数少于目标速率 × 时长（第二份：60000 个应有、只有 54000 个，约 10% 的时间被卡住）；max 对不上 GC 日志里已知的长停顿；尾部过于平滑；测量与被测逻辑同一线程同步发—等—发 ([[hft-measurement-coordinated-omission-symptoms]])
- 修正：按计划发送时间计算延迟，或开环按固定速率发送不等响应；HdrHistogram 的 `recordValueWithExpectedInterval` 在预期间隔 1 ms 时记录到 1 s，会补上约 999 个合成样本。闭环测"一个请求最快多久"，开环测持续负载下的真实感受 ([[hft-measurement-coordinated-omission-fix]])
- 行情测量起点要取到达网卡（最好是硬件时间戳），不是开始处理：线程卡 1 ms 时，从"开始处理"算只有 5 µs，从"到达网卡"算是 1005 µs，报价已经过期 ([[hft-measurement-coordinated-omission-market-data]], [[hft-measurement-timestamps-wire-to-wire]])
- 百分位不能取平均也不能相加：要把各机器的直方图逐桶合并再读 p99；各环节 p99 相加既可能高估也可能低估。保存可合并的 HdrHistogram，在端到端入口和出口直接打点 ([[hft-measurement-distributions-no-averaging-percentiles]], [[hft-measurement-histograms-merge-and-read]])
- 尾部放大：1 − 0.99^10 = 1 − 0.904 ≈ 9.6%，约每 10 次就有 1 次受影响；独立假设下成立，真实系统里慢事件常相关（同一次 GC 同时拖慢多个环节） ([[hft-measurement-distributions-tail-amplification]])
- 交易系统更关心 p99.9 和 max，因为慢样本集中在最忙的时刻；只报均值会骗人：998 次 5 µs 加 2 次 5 ms，均值约 15 µs，p99.9 却是 5000 µs ([[hft-measurement-distributions-busy-time]], [[hft-measurement-distributions-mean-hides]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
