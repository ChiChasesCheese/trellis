---
id: nested-comprehension-beyond-two-levels-antipattern
node: iteration.comprehensions
type: qa
source: python-docs
---
## Q
把一个三层嵌套、带条件过滤的循环硬写成一个单行嵌套推导式，为什么通常被认为是反模式？

## A
推导式的可读性优势来自把「做什么」压缩成一行，但超过约两层 for（尤其再叠加多个 if 或复杂表达式）会让求值顺序和作用域关系很难一眼看出，读者必须在脑子里手动展开成嵌套循环才能确认语义。嵌套推导式本质上和多层 for 循环等价，一旦超过大约两层，改写成显式的多层 for 循环（或者用 `zip()` 这类内建函数替代）通常比塞进一个推导式更清楚。
