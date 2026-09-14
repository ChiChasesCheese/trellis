---
id: cc-input-norm-suffix-and-article
node: input.normalization
type: qa
---
## Q
`The Llama, Inc. LLC` and `llama` must compare equal. Write the normalization order and name the step that must not move.

## A
**Lower · separators to spaces · split · strip entity suffixes repeatedly · drop one leading article · rejoin.**

```python
toks = name.lower().replace("&", " ").replace(",", " ").split()
while toks and toks[-1] in SUFFIXES:      # repeatedly: "Inc. LLC"
    toks.pop()
if toks and toks[0] in ARTICLES:          # once, not repeatedly
    toks.pop(0)
```

The step that must not move: recognize multi-dot suffixes like `l.l.c.` **before** turning punctuation into spaces, or it fragments into three tokens and survives. Also decide what an empty result means — it is a real state ("The Inc." normalizes to nothing) and usually must be rejected rather than stored as `""`.

## Q zh
`The Llama, Inc. LLC` 与 `llama` 必须比较相等。写出归一化顺序，并指出哪一步不能挪位置。

## A zh
**转小写 · 分隔符变空格 · 切分 · 反复剥公司后缀 · 去掉一个开头冠词 · 重新拼接。**

```python
toks = name.lower().replace("&", " ").replace(",", " ").split()
while toks and toks[-1] in SUFFIXES:      # repeatedly: "Inc. LLC"
    toks.pop()
if toks and toks[0] in ARTICLES:          # once, not repeatedly
    toks.pop(0)
```

不能挪的一步：像 `l.l.c.` 这样带多个点的后缀必须在把标点变成空格**之前**识别，否则它会碎成三个 token 而幸存下来。另外要决定空结果意味着什么 —— 那是一个真实状态（`The Inc.` 归一化后什么都不剩），通常必须拒绝，而不是当作 `""` 存起来。
