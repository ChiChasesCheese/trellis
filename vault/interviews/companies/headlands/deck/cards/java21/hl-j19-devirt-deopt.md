---
id: hl-j19-devirt-deopt
node: java21.j19-runtime-zgc-jit
type: qa
step: 23
---
## Q
JIT 怎么优化 `list.get(i)` 这样的虚调用？什么情况下会触发去优化（deoptimization）？

## A
运行时 99% 的调用点只见到 `ArrayList`，JIT 据剖析数据做**投机**（speculation）：直接内联 `ArrayList.get`，前面放一个「类型真是 ArrayList 吗」的检查（去虚化）。

以后真来了别的类型，检查失败 → **uncommon trap** → **去优化**：丢掉编译代码，退回解释器，重新收集数据再编译。这是 `made not entrant` 的另一个来源。

所以多态调用点（一个调用点出现 **3 种以上类型**）成了真正的虚调用，无法内联；热路径要保持行为稳定、调用点单态。
