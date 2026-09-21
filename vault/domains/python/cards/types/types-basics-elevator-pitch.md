---
id: types-basics-elevator-pitch
node: types.basics
type: qa
source: python-docs
---
## Q
60 秒内怎么跟面试官讲清楚 Python 的类型提示（type hint）是什么？

## A
三句话：①类型提示只是函数签名和变量声明上的元数据，存进 `__annotations__`，解释器本身完全不检查、不强制；②真正的类型检查由外部工具（mypy、pyright）在开发阶段做静态分析（static analysis）完成，和运行时无关；③正因为零运行时成本，才能在存量代码里逐步补充注解（渐进类型化，gradual typing），不用一次性全部标完。
