---
id: closure-vs-callable-object-tradeoff
node: functions.first-class
type: qa
source: python-docs
---
## Q
要实现「返回一个记住了 a、b 的函数 f(x)=a*x+b」这种高阶函数（higher-order function），用嵌套函数（闭包）写法和用实现 `__call__` 的可调用对象（callable object）写法相比，各有什么代价？

## A
闭包（嵌套函数）写法更短、调用更快；可调用对象（定义 `__call__` 的类）稍慢、代码更长，但状态以实例属性形式显式暴露，且同类高阶函数可以通过继承共享参数签名——子类只需重写 `__call__` 里的计算式即可换一种行为。
