---
id: cc-toolbox-cache-lru-tiebreak
node: toolbox.cache
type: qa
---
## Q
Two accounts have never been used; two others were last used at the same instant. "Pick the least recently used" — what exactly do you pick?

## A
**"Least recently used" is not a total order.** Three decisions must be made explicit before it becomes one:

- Where do **never used** entries sit — before every used one, or after? Usually first, encoded as a leading flag: `0` for never used, `1` otherwise.
- Equal `last_used` → the declared tie-break, typically the id in plain string order (`a10 < a2`) ([[cc-output-ordering-string-vs-numeric]]).
- Does a **failed** acquire or a missed lookup count as a use? Usually not — otherwise a client hammering a busy resource keeps resetting its recency and it is never chosen.

```python
key = (0 if last_used is None else 1, last_used or 0, account_id)
```

A *release* keeps `last_used` unchanged: the entry was genuinely used recently, it is merely free again.

## Q zh
两个账户从未被使用过；另外两个的最后使用时间完全相同。「取最久未使用的那个」—— 到底取哪个？

## A zh
**「最久未使用」不是全序。** 要让它成为全序，必须显式做出三个决定：

- **从未使用过**的条目排在哪里 —— 所有用过的之前，还是之后？通常在最前，用一个前置标志编码：从未使用为 `0`，否则为 `1`。
- `last_used` 相同 → 用规定的 tie-break，通常是 id 的普通字符串序（`a10 < a2`）（[[cc-output-ordering-string-vs-numeric]]）。
- **失败**的获取或未命中的查找算不算一次使用？通常不算 —— 否则一个不停敲打忙碌资源的客户端会一直刷新自己的时间，永远轮不到它。

```python
key = (0 if last_used is None else 1, last_used or 0, account_id)
```

*释放*不改变 `last_used`：这个条目确实是刚被用过的，只是重新空闲了。
