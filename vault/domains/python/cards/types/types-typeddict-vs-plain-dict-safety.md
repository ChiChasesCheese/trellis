---
id: types-typeddict-vs-plain-dict-safety
node: types.typeddict-literal
type: qa
source: python-docs
---
## Q
给一个 JSON 形状的字典用 `TypedDict` 加类型和直接用 `dict[str, Any]` 相比，换来的安全性体现在哪个阶段？运行时安全性有区别吗？

## A
区别只体现在静态检查阶段：`TypedDict` 让检查器知道每个键该有什么值类型、哪些键必需，能在 `b['label']` 写成 `b['lable']` 这种拼写错误或类型不匹配时于开发期报错；`dict[str, Any]` 完全没有这种约束，任何键、任何类型都能通过检查。两者在运行时的安全性没有差别——`TypedDict` 实例本身就是普通 `dict`，运行时既不校验键是否存在，也不校验值类型，出错都要等到真正访问数据时才会暴露。
