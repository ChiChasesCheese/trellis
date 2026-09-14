---
id: cc-rules-grp-key-defines-independence
node: rules.grouping
type: qa
---
## Q
The same customer buys at two merchants, and the same pair buys twice in one hour. Which counters are involved?

## A
**Three independent counters, because three different keys are involved.**

```
(merchant, customer)         -> repeat-customer rule
(merchant, customer, hour)   -> hourly-density rule
merchant                     -> the score itself
```

The same customer at two merchants has two separate `(merchant, customer)` counters — the key defines what "the same" means, and nothing else does. Read the key out of the sentence literally: "by the same customer at the same merchant within one hour" names all three components, and dropping one silently merges groups that the rule keeps apart. See [[cc-model-idx-composite-tuple-key]].

## Q zh
同一位顾客在两个商户消费，而同一个组合在一小时内消费两次。牵涉到哪些计数器？

## A zh
**三个互相独立的计数器，因为牵涉到三种不同的 key。**

```
(merchant, customer)         -> repeat-customer rule
(merchant, customer, hour)   -> hourly-density rule
merchant                     -> the score itself
```

同一顾客在两个商户有两个独立的 `(merchant, customer)` 计数器 —— key 定义了"同一个"是什么意思，别的都不定义。照字面从句子里读出 key：「同一顾客在同一商户一小时内」点名了全部三个成分，少一个就会悄悄把规则本要分开的组合并起来。见 [[cc-model-idx-composite-tuple-key]]。
