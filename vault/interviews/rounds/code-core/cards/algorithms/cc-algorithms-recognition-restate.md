---
id: cc-algorithms-recognition-restate
node: algorithms.recognition
type: qa
---
## Q
The statement is full of domain vocabulary — freezes, settlements, routing. How do you reach a known technique without mis-matching?

## A
**Strip the nouns and restate the input and the objective in structural terms.** "Free windows across a day given busy periods" is interval complement; "fewest transfers that zero everyone out" is partition into zero-sum subsets; "which region serves this request" is nearest-point-with-capacity.

- Then **check the mapping against the worked example before coding**. A wrong match costs the whole problem, and the example is the cheapest test you will ever run.
- Watch what the restatement drops — capacity limits, tie-breaks, inclusive endpoints. Those details are what make the problem bespoke, and they are where the hidden tests live.
- If nothing matches, the answer is usually simulation plus careful bookkeeping. That is a legitimate technique, not a failure to recognise one.
- Say the restatement out loud in an interview; it is the step that shows judgement, and a wrong one gets corrected before it costs you code.

## Q zh
题面全是领域词汇 —— 冻结期、结算、路由。怎么在不匹配错的前提下找到已知技术？

## A zh
**剥掉名词，用结构化语言重述输入和目标。** 「给定忙碌时段求一天中的空闲窗口」是区间取补；「让所有人归零的最少转账数」是划分成零和子集；「哪个区域来服务这个请求」是带容量的最近点查询。

- 然后**在写代码前把这个映射对照样例检验一遍**。匹配错会赔掉整道题，而样例是你能跑的最便宜的测试。
- 注意重述丢掉了什么 —— 容量上限、tie-break、闭区间端点。正是这些细节让题目变得定制化，也正是隐藏测试所在之处。
- 如果什么都对不上，答案通常是模拟加细致记账。那是一种正当技术，而不是没认出技术。
- 面试里把重述说出来；这一步展示判断力，而且说错了会在你付出代码之前被纠正。
