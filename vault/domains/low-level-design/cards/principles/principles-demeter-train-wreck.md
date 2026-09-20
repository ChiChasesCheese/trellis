---
id: principles-demeter-train-wreck
node: principles.coupling
type: qa
step: 2
---
## Q
什么是迪米特法则（Law of Demeter）的违反？为什么这种写法被叫作 train wreck（火车相撞）？

## A
迪米特法则说：一个方法只应该跟自己的"朋友"打交道——只调用这几类对象的方法：它自己这个类上的方法、传进来的参数对象的方法、自己在方法内部创建或直接持有的对象的方法。

`a.get_b().get_c().get_d().do_it()` 这种写法之所以叫 train wreck，是因为每一个点号后面都像一节火车车厢，一节接一节地追下去——调用方需要知道 `b` 有一个 `c`、`c` 又有一个 `d`，这条链暴露了每一层中间对象的内部结构，`b` 或 `c` 内部换一种实现，最末端的调用方就要跟着改。
