---
id: cc-input-norm-once-at-the-boundary
node: input.normalization
type: qa
---
## Q
Company names must be compared ignoring case, punctuation, entity suffixes and a leading article. Where in the program does that transformation belong?

## A
**In one `normalize(name)` called at the boundary, with both forms stored on the record.**

```python
rec = {"raw": name, "key": normalize(name)}
```

Normalizing at each comparison site means five call sites drift apart the moment a Part 3 rule adds a suffix to strip; normalizing destructively means you can no longer print what the user typed. Keeping `raw` beside `key` costs one field and settles every later question about which form to compare and which to display. See [[cc-input-norm-key-canonical-print-original]].

## Q zh
公司名的比较要忽略大小写、标点、公司后缀和开头的冠词。这个变换该放在程序的哪个位置？

## A zh
**放进一个在边界处调用的 `normalize(name)`，并在记录上同时保存两种形式。**

```python
rec = {"raw": name, "key": normalize(name)}
```

在每个比较点各自归一化，意味着一旦 Part 3 的规则多剥一个后缀，五处调用点就会开始漂移；而破坏性地归一化，则让你再也打印不出用户输入的原文。把 `raw` 和 `key` 并排保存只多一个字段，却一次性解决了"比较用哪种、显示用哪种"的所有后续问题。见 [[cc-input-norm-key-canonical-print-original]]。
