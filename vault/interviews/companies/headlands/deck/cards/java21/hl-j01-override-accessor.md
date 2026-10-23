---
id: hl-j01-override-accessor
node: java21.j01-record
type: qa
step: 26
---
## Q
`record` 能不能重写访问器？重写时有什么要求，哪里容易出错？

## A
可以重写，但必须 `public`、返回类型相同。

陷阱：如果让 `symbol()` 返回的值与字段不同，`equals` / `toString` 仍按**字段**算，两者就不一致了。约定**访问器应返回对应组件的值**（编译器不强制）；要"加工后的视图"就另起方法名。
