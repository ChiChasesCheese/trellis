---
id: cc-python-pitfalls-mutate-while-iterating
node: python.pitfalls
type: qa
---
## Q
`for k in d: if bad(k): del d[k]` raises `RuntimeError: dictionary changed size during iteration`. The list version does not raise — it silently drops half the matches. Give the rules.

## A
**Never structurally modify a container you are iterating.**

- **dict / set**: any size change raises `RuntimeError`. Iterate a snapshot — `for k in list(d):` — or rebuild: `d = {k: v for k, v in d.items() if not bad(k)}`.
- **list**: `for x in xs: xs.remove(x)` does not raise. The cursor advances past the element that shifted into the freed slot, so it skips every other match — a wrong answer with no exception, which is worse.
- Changing a **value** in place is always safe; it is adding and removing **keys** or elements that invalidates the iterator.
- Deleting during iteration is also how a "clean up expired entries" pass silently keeps half of them.

## Q zh
`for k in d: if bad(k): del d[k]` 会抛 `RuntimeError: dictionary changed size during iteration`。list 版本不抛异常 —— 它悄悄漏掉一半匹配项。给出规则。

## A zh
**绝不要在遍历一个容器时改动它的结构。**

- **dict / set**：任何长度变化都抛 `RuntimeError`。遍历一份快照 —— `for k in list(d):` —— 或者重建：`d = {k: v for k, v in d.items() if not bad(k)}`。
- **list**：`for x in xs: xs.remove(x)` 不报错。游标越过了那个被移到空位上的元素，于是每隔一个就漏掉一个 —— 得到错误答案却没有异常，这更糟。
- 原地改**值**永远安全；是增删**键**或元素让迭代器失效。
- 一个「清理过期条目」的遍历之所以会悄悄留下一半，也正是这个原因。
