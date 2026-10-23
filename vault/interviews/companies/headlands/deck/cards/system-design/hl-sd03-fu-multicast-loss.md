---
id: hl-sd03-fu-multicast-loss
node: system-design.sd03-low-latency-trading
type: qa
step: 37
---
## Q
追问：组播行情丢包、乱序、重复怎么办？

## A
序号 + A/B 双路「先到者胜」去重（已见序号位图）；任一路丢包无感；两路同缺 ⟹ 缺口：标记 STALE，请求重传或快照 + 增量重新对齐，对齐前禁止对该品种发新单；小窗口重排处理轻微乱序；监控缺口率、包间隔。

可以说：「缺口不是错误，是状态：该品种进入 STALE，策略看不到它也不能交易它。」
