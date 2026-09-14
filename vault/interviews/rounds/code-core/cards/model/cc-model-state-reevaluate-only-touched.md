---
id: cc-model-state-reevaluate-only-touched
node: model.entity-state
type: qa
---
## Q
After each event you must know the current set of flagged merchants. Re-evaluate everyone, or just one?

## A
**Just the merchant the event touched — an event changes exactly one entity's inputs.**

```python
apply(event, rec)
if is_flagged(rec): flagged.add(rec.id)
else:               flagged.discard(rec.id)
```

Re-scanning all merchants per event is 10^5 × 10^4 operations and will time out. The pattern generalizes: *incremental maintenance* keeps a derived set in step with an event stream in O(1) per event, and the `discard` branch is what makes it correct under reversals — the entity that stops qualifying must be removed, not merely not re-added.

## Q zh
每个事件之后你都要知道当前被标记的商户集合。重算所有人，还是只算一个？

## A zh
**只算这个事件触及的那个商户 —— 一个事件恰好只改变一个实体的输入。**

```python
apply(event, rec)
if is_flagged(rec): flagged.add(rec.id)
else:               flagged.discard(rec.id)
```

每个事件都重扫全部商户是 10^5 × 10^4 次操作，一定超时。这个模式可推广：**增量维护**能以每事件 O(1) 的代价让派生集合与事件流保持同步，而 `discard` 分支正是它在撤销下仍然正确的原因 —— 不再满足条件的实体必须被移除，而不只是"不再被加入"。
