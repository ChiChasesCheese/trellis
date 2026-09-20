---
id: python-typing-literal
node: python.typing
type: qa
step: 3
tags: [grown]
---
## Q
`Literal["asc", "desc"]` 相比直接用 `str` 作为排序方向参数的类型，多提供了什么？

## A
`str` 只说“这是个字符串”，任何拼写错误（`"dsc"`）都要跑到运行时才会被发现（甚至可能不报错，静默走了默认分支）。`Literal["asc", "desc"]` 把参数收窄成**一个封闭的有限取值集合**，类型检查器能在调用点直接标红拼错的字面量，效果类似一个只有两个成员的 `Enum`，但不需要额外定义、导入一个枚举类型，适合“这个字符串本来就是配置/API 里约定俗成的字面量”的场景。
