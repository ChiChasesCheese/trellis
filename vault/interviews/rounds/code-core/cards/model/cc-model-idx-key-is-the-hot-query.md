---
id: cc-model-idx-key-is-the-hot-query
node: model.index
type: qa
---
## Q
How do you choose the key of your main dict?

## A
**From the question the hot path has to answer, not from what the input looks like.**

The input arrives as rows of `(charge_id, account, amount, code)`; the hot query in Part 4 is "given a charge id, which account and was it fraud?" — so the ledger is keyed by `charge_id`, and the counters are keyed by `account`, because *their* hot query is "what is this account's ratio?".

Two structures with two keys is the normal answer, not a failure of design. The failure is one structure keyed by whatever the first part happened to iterate, followed by a linear scan in the last part.

## Q zh
你怎么给主 dict 选 key？

## A zh
**从热点路径必须回答的问题出发，而不是从输入长什么样出发。**

输入是一行行 `(charge_id, account, amount, code)`；Part 4 的热点查询是「给定 charge id，属于哪个账户、是不是欺诈？」—— 所以这本账以 `charge_id` 为 key；而计数器以 `account` 为 key，因为**它们**的热点查询是「这个账户的比率是多少？」。

两个结构、两个 key 是正常答案，不是设计失败。失败是只有一个结构、key 取自第一部分恰好遍历的东西，然后在最后一部分做线性扫描。
