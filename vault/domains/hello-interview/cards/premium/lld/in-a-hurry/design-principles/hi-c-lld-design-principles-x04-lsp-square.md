---
id: hi-c-lld-design-principles-x04-lsp-square
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 4
---
## Q
**设计原则 · 正方形继承矩形**｜考点 · 必会

`Square` 继承 `Rectangle`，重写 `set_width` 时同时改高度。调用方写了 `r.set_width(5); r.set_height(2); assert r.area() == 10`，传入 `Square` 会怎样？说明违反了什么，怎么办？

## A
- **结果：** 面积变成 4，断言失败
- **违反：** LSP——子类破坏了父类的行为承诺（宽高可独立设置）
- **根因：** 数学上"是一个"，行为上不是
- **改法：** 不继承；两者都实现只读的 `Shape.area()`，或用不可变对象，各自构造
