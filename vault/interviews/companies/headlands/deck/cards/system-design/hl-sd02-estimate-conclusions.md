---
id: hl-sd02-estimate-conclusions
node: system-design.sd02-job-scheduler
type: qa
step: 8
---
## Q
任务调度器的估算得出哪四条设计结论？

## A
1. **容量不是问题，可用性与突发才是**：一台机器放得下全部元数据，所以分片的理由是**故障半径、分发吞吐的隔离**，不是存不下；
2. **近期窗口很小**：时间轮只管未来十几分钟，远期放磁盘；
3. **整点突发是 SLO 杀手**：必须有（a）足够的分发能力，或（b）让调用方给出容忍窗口（`notBefore = t`，`notAfter = t + slack`），调度器在窗口内摊平（smear）；
4. **有界延迟是一个预算**：tick + 队列 + 分发 + 故障切换。
