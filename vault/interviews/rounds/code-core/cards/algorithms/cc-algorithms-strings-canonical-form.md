---
id: cc-algorithms-strings-canonical-form
node: algorithms.strings
type: qa
---
## Q
`The Llama, Inc.`, `llama` and `Llama LLC` must all count as the same name. How do you model that, and what do you print?

## A
**Canonicalize once into a key; keep the original for display.**

- One function, and the **order of its steps is the rule**: casefold → recognise multi-token suffixes (`L.L.C.`) *before* punctuation is stripped → strip punctuation → drop a leading article → strip *all* trailing suffix words repeatedly (`Llama Inc. LLC`) → collapse whitespace.
- Two spellings collide **iff** their canonical forms are equal. The registry is `dict[canonical] -> original`, and the lookup must call the exact same function as the insert.
- A name whose canonical form is **empty** (`Inc.`, `The`, `&`) is not a name — reject it rather than registering the empty key, or the first such request claims everything.
- Print the original spelling, not the key ([[cc-output-formatting-one-place]]).
- Never canonicalize in two places. A second, slightly different normalizer is how "available" and "already taken" start disagreeing.

## Q zh
`The Llama, Inc.`、`llama` 和 `Llama LLC` 必须都算作同一个名字。怎么建模，输出什么？

## A zh
**一次性归一化成一个 key；保留原文用于显示。**

- 只写一个函数，而且**步骤顺序本身就是规则**：casefold → 在去标点*之前*识别多词后缀（`L.L.C.`）→ 去标点 → 去掉开头的冠词 → 反复剥掉*所有*结尾的后缀词（`Llama Inc. LLC`）→ 合并空白。
- 两种写法冲突**当且仅当**它们的规范形式相等。注册表是 `dict[canonical] -> original`，而查找必须调用与插入完全相同的那个函数。
- 规范形式为**空**的名字（`Inc.`、`The`、`&`）不是名字 —— 拒绝它而不是注册空 key，否则第一个这样的请求会把一切都占了。
- 打印原始写法，而不是 key（[[cc-output-formatting-one-place]]）。
- 绝不要在两个地方各做一次归一化。一个略有差异的第二版归一化函数，正是「可用」和「已被占用」开始互相矛盾的原因。
