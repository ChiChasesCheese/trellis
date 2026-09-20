---
nodes: [quality.fitness-functions]
url: https://www.archunit.org/userguide/html/000_Index.html
---
# ArchUnit User Guide

值得读：这是"用代码检查代码库结构"这件事写得最完整的一份参考——分层架构规则、包之间的依赖方向、循环依赖检测，全部以可执行、
能跑进 CI 的断言形式给出。虽然是 Java 工具，但规则的形状和 `quality-fitness-function-import-direction`、
`quality-fitness-function-positive-control` 两张卡完全对应：一条"domain 不能 import infrastructure"的规则如何被表达成一个
可以失败、可以挡住合并的测试，读它能补上这套断言除了 import 方向之外还能检查到什么粒度（命名约定、注解、包内可见性）。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.archunit.org/userguide/html/000_Index.html)

## Archived copy
![[archunit-fitness-functions-clip]]
%% trellis:end %%
