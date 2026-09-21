%% trellis:begin %%
# 解释器与执行模型

源码如何变成字节码并被求值：编译、代码对象与帧、导入系统、异常机制，以及 3.11+ 自适应解释器与 JIT 带来的变化。

## Topics
- [[domains/python/map/runtime.compile-bytecode|从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存]]
- [[domains/python/map/runtime.frames-eval|求值循环与帧：调用栈、递归限制与尾调用]]
- [[domains/python/map/runtime.adaptive-jit|自适应解释器（PEP 659）与实验性 JIT（PEP 744）]]
- [[domains/python/map/runtime.import-system|导入系统：模块对象、`sys.modules`、包与循环导入]]
- [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]
- [[domains/python/map/runtime.namespaces-execution|执行模型：命名空间、`global`、代码块与 `exec`/`eval` 的风险]]
- [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]]
%% trellis:end %%

## Notes
