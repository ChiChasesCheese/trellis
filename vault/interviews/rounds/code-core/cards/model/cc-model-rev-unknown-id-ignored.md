---
id: cc-model-rev-unknown-id-ignored
node: model.reversal
type: qa
---
## Q
A reversal names an id your program has never seen. What are the three wrong responses?

## A
**Crashing, creating the entity, and counting it as a reversal.**

- `charges[cid]` raises `KeyError` and kills the run — the whole submission, not one test.
- `accounts[acct]` on a `defaultdict` invents a merchant that then appears in the output.
- Incrementing a "reversals seen" tally makes a later count wrong.

The right response is a silent no-op. It is the same branch as the double reversal, and it costs one `.pop(cid, None)`. Unknown-id reversals appear in every reversal-bearing statement's edge list precisely because all three failures are easy to write.

## Q zh
一次撤销引用了你的程序从未见过的 id。三种错误反应是什么？

## A zh
**崩溃、创建实体、把它计为一次撤销。**

- `charges[cid]` 抛出 `KeyError`，直接终止运行 —— 死的是整份提交，不是一个测试。
- 在 `defaultdict` 上访问 `accounts[acct]` 会凭空造出一个商户，随后出现在输出里。
- 给"已见撤销数"加一，会让后面的某个计数出错。

正确反应是静默 no-op。它和重复撤销是同一个分支，代价是一次 `.pop(cid, None)`。未知 id 的撤销之所以出现在每份带撤销的题面的边界清单里，正因为这三种失败都太容易写出来。
