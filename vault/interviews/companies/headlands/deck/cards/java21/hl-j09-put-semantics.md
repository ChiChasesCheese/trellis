---
id: hl-j09-put-semantics
node: java21.j09-sequenced-collections
type: qa
step: 13
---
## Q
`LinkedHashMap` 里 `put(k, v)`、`putLast(k, v)`、`putFirst(k, v)` 在 key 不存在和已存在时分别怎么处理位置？

## A
| 操作 | key 不存在 | key 已存在 |
|---|---|---|
| `put(k, v)` | 加到末尾 | **只改值，位置不变** |
| `putLast(k, v)` | 加到末尾 | 改值，**并把它挪到末尾** |
| `putFirst(k, v)` | 加到最前 | 改值，**并把它挪到最前** |

例：`{x=10, y=2, z=3}` 上 `putLast("x", 11)` 得 `{y=2, z=3, x=11}`。
