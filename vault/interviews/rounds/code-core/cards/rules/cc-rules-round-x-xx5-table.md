---
id: cc-rules-round-x-xx5-table
node: rules.rounding
type: qa
---
## Q
Before submitting, which arithmetic cases do you hand-check against the rounding rule?

## A
**Every input that lands exactly on a half — the graders build their tests from them.**

```
2.1% of 500 cents = 10.5   -> 11   (banker's gives 10)
$15.00 x 1/8      = 1.875  -> 1.88 (a two-step tie)
2.1% of 1000      = 21.0   -> 21   (exact, no tie: the control case)
2.1% of 99        = 2.079  -> 2    (well below the half)
```

Construct one deliberately: find the amount that makes the fee end in `.5` (here, any multiple of 500 cents). One exact-tie case, one just below and one just above is a complete test of a rounding rule, and it takes a minute.

## Q zh
提交之前，你要对着取整规则手工核对哪些算例？

## A zh
**所有恰好落在半数上的输入 —— 评测机的测试就是从它们造出来的。**

```
2.1% of 500 cents = 10.5   -> 11   (banker's gives 10)
$15.00 x 1/8      = 1.875  -> 1.88 (a two-step tie)
2.1% of 1000      = 21.0   -> 21   (exact, no tie: the control case)
2.1% of 99        = 2.079  -> 2    (well below the half)
```

自己刻意构造一个：找出让手续费恰好以 `.5` 结尾的金额（这里是 500 分的任意倍数）。一个恰好平局、一个略低、一个略高，就构成对取整规则的完整测试，而且只要一分钟。
