---
id: augmented-assign-list-vs-tuple-int
node: model.mutability
type: qa
source: python-docs
---
## Q
为什么 `a_list += [1, 2, 3]` 会就地修改 `a_list` 本身，而 `a_tuple += (1, 2, 3)` 和 `an_int += 1` 却是创建新对象、重新绑定名字？

## A
`+=` 对可变对象（如 list）等价于调用它的就地方法（相当于 `list.extend`），直接修改原对象内容，其他引用同一对象的名字也会看到变化；而 tuple 和 int 是不可变类型，没有就地修改能力，`+=` 只能算出新值，让左边的名字重新绑定到一个新对象，原对象保持不变。
