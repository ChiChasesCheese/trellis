---
nodes: [problems.components.text-editor]
url: https://docs.python.org/3/library/dataclasses.html
---
# dataclasses — Data Classes（标准库文档）

值得读：`Edit` 能写成"一个值"而不是"一个命令对象"，全靠这一页里的三个开关。`frozen=True`
让它造出来就不可变，于是它可以安心地躺在撤销栈里被反复引用；自动生成的 `__eq__` 让
`edit.invert().invert() == edit` 成为一条可以直接写进测试的等式；`slots=True` 去掉每个实例的
`__dict__`，在"一次编辑一个对象"的场景下省下可观的内存。读的时候顺带看 `field()` 与
`dataclasses.replace()`——后者是"从一条记录派生出一条改了一两个字段的新记录"的标准写法，
在需要转换（而不是过滤）记录时会用到。
