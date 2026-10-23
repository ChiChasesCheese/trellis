---
id: hl-javaq-e-q18-thresholds-osr
node: java-questions.e-jit-gc
type: qa
step: 2
---
## Q
分层编译的默认阈值参数有哪些？OSR（栈上替换）解决什么问题、靠什么计数、在什么时候切换？

## A
- **默认阈值**（运行时会按编译队列长度动态缩放）：`Tier3CompileThreshold=2000`、`Tier4InvocationThreshold=5000`、`Tier4CompileThreshold=15000`、`TieredStopAtLevel=4`。
- **OSR**（on-stack replacement）：`main` 里只调用一次的长循环没有"调用次数"可数，所以靠**回边计数**（back-edge counter）；达到阈值后在**循环迭代之间**把解释器栈帧换成编译版本。
- 编译线程会和业务线程**抢 CPU**，核数少的容器里会放大预热期延迟（常见经验）。
