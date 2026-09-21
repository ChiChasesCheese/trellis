---
id: parameterized-decorator-three-layers
node: functions.decorator-patterns
type: qa
tags: [grown]
---
## Q
写一个「带参数的装饰器」（比如 `@retry(times=3)`）为什么通常要嵌套三层函数？每一层各自负责什么？

## A
最外层函数接收装饰器自己的参数（如 `times=3`），返回真正的装饰器；中间层（真正的装饰器）接收被装饰的函数 `func`，返回包装函数；最内层的包装函数 `wrapper(*args, **kwargs)` 在被调用时执行真正的逻辑（比如重试循环），再转发参数调用原始 `func`。三层缺一不可：不带参数的装饰器只需要中间层+最内层两层，一旦要在 `@` 后面传参数，就必须多包一层先接收这些参数。
