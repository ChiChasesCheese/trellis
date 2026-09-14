---
id: cc-rules-grp-parameter-from-current-row
node: rules.grouping
type: qa
---
## Q
Every transaction carries its own rule parameters, and the bonus fires on the 3rd and later transactions of a pair. Whose additive factor is added on the 4th transaction?

## A
**The 4th transaction's own — the row that triggers the rule supplies the parameter, not the row that started the group.**

```
alice: rows with additive 5, 5, 5, 7  ->  3rd adds 5, 4th adds 7  ->  +12
```

Caching "the group's factor" from the first row is a natural-looking optimization and a wrong answer. State it explicitly when you write the loop: the group decides *whether* the rule fires, the current row decides *with what*. The same split appears in tiered pricing and in fee tables — qualification and parameter come from different places.

## Q zh
每笔交易都带着自己的规则参数，而奖励在某组合的第 3 笔及以后触发。第 4 笔加的是谁的加法因子？

## A zh
**第 4 笔自己的 —— 触发规则的那一行提供参数，而不是开启该组的那一行。**

```
alice: rows with additive 5, 5, 5, 7  ->  3rd adds 5, 4th adds 7  ->  +12
```

从第一行缓存"这个组的因子"看起来像个自然的优化，实际是错误答案。写循环时就把它说清楚：组决定规则**是否**触发，当前行决定**用什么参数**。同样的分工出现在阶梯定价和费率表里 —— 资格与参数来自不同的地方。
