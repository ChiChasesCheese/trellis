---
id: cc-model-rec-parallel-dicts-are-an-object
node: model.records
type: qa
---
## Q
Your program has grown `fraud[acct]`, `total[acct]`, `mcc[acct]` and `flagged[acct]`, all keyed by the same id. What has happened, and what do you do about it mid-round?

## A
**Four dicts keyed by the same id are one record that has not been named yet.** The cost shows up when an entity must be created, copied or deleted: four places to remember, and the fourth one is the bug.

```python
accounts[acct] = {"fraud": 0, "total": 0, "mcc": None, "flagged": False}
```

Convert when a *third* parallel dict appears, or the moment you need "does this entity exist" — with a record it is one `in` test rather than a guess about which dict is authoritative. Two parallel dicts are usually still fine; do not refactor late for tidiness alone. See [[cc-round-time-no-late-refactor]].

## Q zh
你的程序里长出了 `fraud[acct]`、`total[acct]`、`mcc[acct]`、`flagged[acct]`，全部用同一个 id 作 key。发生了什么？做题过程中该怎么办？

## A zh
**用同一个 id 作 key 的四个 dict，其实是一个还没被命名的记录。** 代价在需要创建、复制或删除实体时显现：要记住四个地方，而第四个就是 bug。

```python
accounts[acct] = {"fraud": 0, "total": 0, "mcc": None, "flagged": False}
```

在出现**第三个**并行 dict 时转换，或者在你需要判断"这个实体是否存在"时立刻转换 —— 有了记录，那就是一次 `in` 判断，而不是猜哪个 dict 才是权威。两个并行 dict 通常还好；不要仅为整洁而在后期重构。见 [[cc-round-time-no-late-refactor]]。
