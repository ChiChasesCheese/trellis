---
id: assignment-makes-name-local-statically
node: functions.scope-closure
type: qa
source: python-docs
---
## Q
为什么在函数体里给一个名字赋值一次，会让这个名字在整个函数体内都变成局部变量（local variable），即使赋值语句写在使用它之后？

## A
Python 编译函数时会静态扫描整个函数体：只要函数体内任何地方出现了对某个名字的赋值（包括 `+=`、`import`、`for` 循环变量等绑定操作），这个名字在整个函数体内都被划为局部变量，跟赋值语句写在使用之前还是之后无关。所以「先读后赋值」的写法会在运行到读取处时，发现对应的局部变量还没初始化。
