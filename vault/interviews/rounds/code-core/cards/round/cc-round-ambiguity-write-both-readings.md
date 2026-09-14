---
id: cc-round-ambiguity-write-both-readings
node: round.ambiguity
type: qa
---
## Q
A rule reads: "a merchant is flagged when its fraudulent charges exceed the category's maximum." You can read it two ways and the statement never disambiguates. What do you do before choosing?

## A
**Write both readings down in one line each — the act of writing them names the input that separates them.**

```
A: flagged iff fraud_count >  max      # "exceeds"
B: flagged iff fraud_count >= max      # "reaches the maximum"
```

The distinguishing case is `fraud_count == max`, which is exactly the case the hidden tests will contain. Now you are choosing between two named behaviours instead of guessing at prose, you have a test case either way, and the choice is one comparison operator to flip. See [[cc-rules-thr-strict-vs-non-strict]].

## Q zh
一条规则写着：「当商户的欺诈扣款 *exceed* 该类别的上限时被标记。」你能读出两种意思，而题面从未澄清。选之前先做什么？

## A zh
**把两种读法各写成一行 —— 写下来的动作本身就点出了区分它们的输入。**

```
A: flagged iff fraud_count >  max      # "exceeds"
B: flagged iff fraud_count >= max      # "reaches the maximum"
```

区分用例正是 `fraud_count == max`，而这恰恰是隐藏测试一定会包含的用例。现在你是在两个有名字的行为之间做选择，而不是猜正文；无论选哪个都有测试用例；而改变选择只是翻转一个比较符。见 [[cc-rules-thr-strict-vs-non-strict]]。
