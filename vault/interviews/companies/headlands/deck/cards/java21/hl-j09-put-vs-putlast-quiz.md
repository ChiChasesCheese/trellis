---
id: hl-j09-put-vs-putlast-quiz
node: java21.j09-sequenced-collections
type: qa
step: 33
---
## Q
`LinkedHashMap` 里已有 key `"x"`，`put("x", 1)` 和 `putLast("x", 1)` 有什么区别？

## A
- `put("x", 1)`：**只改值，位置不变**；
- `putLast("x", 1)`：改值，并把 `"x"` **挪到最后**。

类似地 `putFirst("x", 1)` 挪到最前。
