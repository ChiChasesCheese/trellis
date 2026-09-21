---
id: specialization-rewrite-mechanism
node: runtime.adaptive-jit
type: qa
source: cpython-internals
---
## Q
CPython 3.11 起的「自适应特化」（specializing adaptive interpreter，PEP 659）具体怎么让一条字节码指令变快？

## A
每条可特化的指令族（family）里有一条「自适应」（adaptive）版本，自带一个内联缓存（inline cache）计数器。执行到一定次数后会调用对应的 `_Py_Specialize_XXX` 函数，把这条指令就地改写成针对这次实际遇到的类型/值定制的「特化」（specialized）版本——例如 `LOAD_GLOBAL` 可被特化成读模块全局变量的 `LOAD_GLOBAL_MODULE` 或读内置名字的 `LOAD_GLOBAL_BUILTIN`。特化版本靠内联缓存里的守卫条件（如字典版本号）快速验证假设仍成立，成立就跳过通用逻辑直接执行。
