---
id: amz-closest-store-how-asked-and-three-questions
node: amazon.amz-closest-store
type: qa
step: 1
tags: [grown]
---
## Q
增删查最近值（Add / Remove / Closest）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是一个整数集合：能放入（add）、拿走（remove），还能问「离 target 最近的数是哪个」；面试官随后会告诉你所有值落在一个已知的值域里。三个问题：(1) 两个数一样近怎么办——决定平局规则，默认取较小的；(2) 允许重复值吗——决定 remove 是删一个副本还是全部；(3) 值域多大——值域有界就能换成按值下标的树状数组（Fenwick tree），无界只能用有序列表。每个答案都会改变存储的选择，所以要在写代码前问清。
