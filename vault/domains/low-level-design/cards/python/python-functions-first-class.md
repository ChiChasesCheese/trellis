---
id: python-functions-first-class
node: python.first-class-functions
type: qa
step: 1
tags: [grown]
---
## Q
“函数是一等公民（first-class）”具体让你在设计里少写什么样的类？

## A
函数可以被赋值给变量、存进容器、当参数传递、当返回值返回——凡是**只有一个抽象方法**的接口（Strategy 的 `execute`、Command 的 `run`、Comparator 的 `compare`），在 Java 里需要一个接口加一堆实现类，在 Python 里直接就是一个函数签名：调用方传一个满足该签名的可调用对象（callable）就行，不需要为每种算法各写一个类。
