---
id: decorator-factory-expansion
node: functions.decorators
type: qa
source: python-docs
---
## Q
装饰器可以写成 `@decomaker(argA, argB)` 这种带参数的形式，它展开后等价于什么赋值语句？为什么需要多包一层函数？

## A
等价于 `func = decomaker(argA, argB)(func)`：`@` 后面的部分先作为表达式求值（调用 `decomaker(argA, argB)`），它的返回值才是真正的装饰器，再拿这个返回值去调用被装饰的函数 `func`。这就是为什么「带参数的装饰器」要多包一层函数：外层函数先接收装饰器自己的参数，返回一个只接收 `func` 一个参数的真正装饰器。
