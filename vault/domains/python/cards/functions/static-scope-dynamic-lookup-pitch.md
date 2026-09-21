---
id: static-scope-dynamic-lookup-pitch
node: functions.scope-closure
type: qa
source: python-docs
---
## Q
60 秒内讲清楚：为什么说 Python 的作用域是「静态确定、动态查找」？

## A
「静态确定」指一个名字属于 local、enclosing 还是 global 作用域，在编译函数体时就分析好了，只看代码文本里有没有对它赋值，与运行时走哪条分支无关；「动态查找」指真正沿 LEGB 链条到某个命名空间里取值，是在函数被调用、那行代码真正执行时才发生的。这也是为什么只要调用发生在某次全局变量重新赋值之后，函数内部仍能看到更新后的新值。
