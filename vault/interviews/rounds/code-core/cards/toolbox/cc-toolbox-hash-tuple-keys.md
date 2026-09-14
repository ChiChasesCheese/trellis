---
id: cc-toolbox-hash-tuple-keys
node: toolbox.hash
type: qa
---
## Q
Two records "link" when they carry the same value in the same field. What is the dict key, and what can never be one?

## A
**A tuple of the discriminating fields — `(field_index, value)` — so the same value in a different column does not link.** `A:x:y` and `B:y:x` then share no key.

- Keys must be hashable and immutable: `str`, `int`, `tuple`, `frozenset` yes; `list`, `dict`, `set` no. Freeze with `tuple(sorted(xs))` when order should not matter, `frozenset(xs)` when duplicates should not either.
- **Compose, do not concatenate.** `f"{a}:{b}"` collides as soon as a value contains the separator; `(a, b)` never does.
- Normalize the value **once**, on the way into the key, and use the same function at lookup — a half-normalized key is a silent miss, not an error.
- A tuple key costs a little more memory and hashing time than a string, and it is worth it every time.

## Q zh
两条记录「关联」的条件是在同一字段上取值相同。dict 的 key 是什么，什么绝不能当 key？

## A zh
**由区分字段组成的 tuple —— `(字段序号, 值)` —— 这样同一个值出现在不同列时就不会关联。** 于是 `A:x:y` 和 `B:y:x` 没有共同的 key。

- key 必须可哈希且不可变：`str`、`int`、`tuple`、`frozenset` 可以；`list`、`dict`、`set` 不行。顺序无关时用 `tuple(sorted(xs))` 冻结，连重复也无关时用 `frozenset(xs)`。
- **组合，不要拼接。** 只要值里含有分隔符，`f"{a}:{b}"` 就会碰撞；`(a, b)` 永远不会。
- 值只在进入 key 时归一化**一次**，查找时用同一个函数 —— 半归一化的 key 是一次静默的 miss，而不是报错。
- tuple key 比字符串多花一点内存和哈希时间，而这每一次都值得。
