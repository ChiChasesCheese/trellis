---
id: cc-performance-hot-loop-rescan-entities
node: performance.hot-loop
type: qa
---
## Q
An event updates one merchant's counters, and your loop then walks every merchant to rebuild the flagged set. 10^5 events, 10^4 merchants. What is wrong, and what is the rule?

## A
**Re-evaluate exactly the entity the event touched.** The full re-scan is O(events × entities) = 10^9 — the third classic blowup, and the one that hides best because each individual pass looks cheap.

- Keep the derived answer as maintained state (a `set` of flagged ids) and update it in the same branch that changed the counters.
- Only the touched entity can change status, so the full pass is provably redundant.
- If the answer genuinely needs a global pass, do it **once after** the loop, not inside it.
- The same argument applies to reversals: a refund or dispute touches one entity, so it triggers one re-evaluation.

## Q zh
一个事件更新了某个商户的计数器，接着你的循环遍历所有商户重建被标记的集合。10^5 个事件，10^4 个商户。问题在哪？规则是什么？

## A zh
**只重新评估这个事件碰到的那个实体。** 全量重扫是 O(事件数 × 实体数) = 10^9 —— 第三种经典爆炸，也是最会藏的一种，因为单看每一趟都很便宜。

- 把派生答案当作维护中的状态（一个被标记 id 的 `set`），在改计数器的那个分支里同步更新它。
- 只有被触碰的实体状态会变，所以全量遍历是可证明多余的。
- 如果答案确实需要一次全局遍历，就在循环**结束后做一次**，不要放循环里。
- 同样的论证适用于冲正：一次退款或拒付只碰一个实体，因此只触发一次重新评估。
