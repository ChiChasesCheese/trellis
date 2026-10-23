---
id: hl-j14-tolist-pitfall
node: java21.j14-stream-api
type: qa
step: 5
---
## Q
把旧代码里的 `collect(Collectors.toList())` 批量换成 `stream.toList()` 有什么风险？

## A
`toList()` 返回不可修改列表。旧代码 `list = stream.collect(toList()); list.add(...)` 换成 `toList()` 会在**运行时**抛 `UnsupportedOperationException`，**编译器发现不了**。

所以改的时候要逐处检查这个列表后面有没有被 `add`/`sort`/`remove`。确实需要可变时用 `new ArrayList<>(stream.toList())` 或 `collect(toCollection(ArrayList::new))`。
