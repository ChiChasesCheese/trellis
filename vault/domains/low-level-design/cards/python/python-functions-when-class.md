---
id: python-functions-when-class
node: python.first-class-functions
type: qa
step: 6
tags: [grown]
---
## Q
什么情况下即使 Python 支持一等函数，用类实现 Strategy/Command 仍然更好？

## A
当这个“策略”需要**携带并维护自己的状态**（不只是无状态计算，例如一个需要累计统计的定价策略）、需要**多个协作方法**（不止一个抽象操作）、或者需要参与 `isinstance` 检查/继承体系（比如要被序列化、要暴露多个可覆盖的钩子方法）时，一个类比一个闭包更清楚：状态是显式的实例属性，不是靠嵌套函数的自由变量隐藏起来的。
