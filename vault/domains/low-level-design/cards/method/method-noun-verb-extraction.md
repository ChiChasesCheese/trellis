---
id: method-noun-verb-extraction
node: method.modeling
type: qa
---
## Q
In noun–verb extraction from a requirements statement, what do nouns, verbs, and constraint sentences each become — and which nouns should you reject?

## A
- **Nouns** → candidate classes; **verbs** → responsibilities (methods), assigned to the noun that owns the data the verb touches.
- **Constraint sentences** ("a spot holds one vehicle") → invariants some class must enforce.
- **Reject**: synonyms of an existing noun, and attributes in disguise — "registration number" is a field on `Vehicle`, not a class.


## Q zh
在需求陈述的名词–动词提取中，名词、动词和约束句各变成什么 — 以及哪些名词你应该拒绝?

## A zh
- **名词** → 候选类；**动词** → 责任（方法），分配给拥有动词触及数据的名词。
- **约束句**（"一个位置持有一辆车"）→ 某个类必须执行的不变式。
- **拒绝**: 现有名词的同义词，以及伪装成属性 — "注册号"是 `Vehicle` 上的字段，不是类。
