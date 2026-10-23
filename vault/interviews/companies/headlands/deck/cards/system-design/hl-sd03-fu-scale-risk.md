---
id: hl-sd03-fu-scale-risk
node: system-design.sd03-low-latency-trading
type: qa
step: 44
---
## Q
追问：怎么扩展到更多品种和跨品种风控？

## A
加分片；分片内无共享；跨品种全局限额拆成每个分片的预算（credit），分片内用本地计数器检查，周期性异步再平衡，预算保守；或全局视图放在独立 Risk Gateway（更慢但全局）；高流动性品种独占核心。

可以说：「局部检查通过但全局超限是预算滞后的代价，所以预算要保守，并且全局检查有独立兜底。」
