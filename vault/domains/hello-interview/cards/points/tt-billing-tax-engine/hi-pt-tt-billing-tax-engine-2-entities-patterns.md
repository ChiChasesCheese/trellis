---
id: hi-pt-tt-billing-tax-engine-2-entities-patterns
node: tt.lld.tt-billing-tax-engine.points
type: qa
step: 2
---
## Q
**计费与计税引擎 · 核心实体与模式**｜出自：计费与计税引擎 › 核心实体与接口

计费引擎的 Txn、Line、Rule、FeeEngine 各是什么，用到哪些设计模式？

## A
**实体。** Txn 不可变，ts 是交易发生时间；Line(rule_id, kind, version, amount) 是一行费用，kind 区分费用与税；Rule.apply(txn, prior_lines) 返回全精度金额或 None。
**引擎。** FeeEngine 每商户存同下标的生效时间列表 starts 和规则集列表 versions。
**模式。** 策略（每条规则一种计算）、责任链（后面的规则看得到前面结果）、装饰器（Capped 包住任意规则）。
