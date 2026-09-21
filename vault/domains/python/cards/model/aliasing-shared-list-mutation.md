---
id: aliasing-shared-list-mutation
node: model.mutability
type: qa
source: python-docs
---
## Q
执行 `y = x` 之后，调用 `y.append(10)` 为什么会让 `x` 也看到新增的元素？

## A
`y = x` 不复制对象，只是让新名字 `y` 和已有名字 `x` 引用（reference）同一个 list 对象；list 是可变（mutable）类型，`append` 就地修改这个对象的内容而不是创建新对象。因为 `x` 和 `y` 指向同一份数据，通过任意一个名字访问都能看到修改后的结果，这就是别名（aliasing）。
