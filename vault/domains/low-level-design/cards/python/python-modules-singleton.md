---
id: python-modules-singleton
node: python.modules
type: qa
step: 1
tags: [grown]
---
## Q
为什么一个定义在模块顶层的对象（比如 `_registry = {}` 或 `client = APIClient()`）天然就是单例（singleton），不需要写 Singleton 设计模式？

## A
一个模块在一个进程里**只会被真正执行一次**——第一次 `import` 时 Python 执行模块体并把结果对象缓存进 `sys.modules`，之后任何地方再 `import` 同一个模块名，拿到的都是 `sys.modules` 里的同一个模块对象，模块顶层定义的名字自然也是同一份。这就是为什么 Python 里实现单例最地道的方式是“把它做成一个模块级对象”，而不是写一个带 `__new__` 拦截、加锁的 Singleton 类。
