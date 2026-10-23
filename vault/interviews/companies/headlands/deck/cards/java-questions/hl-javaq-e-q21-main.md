---
id: hl-javaq-e-q21-main
node: java-questions.e-jit-gc
type: qa
step: 12
---
## Q
什么是去优化（deoptimisation）？举例说明 JVM 什么时候会扔掉编译好的代码。
What is deoptimisation? Give an example of when the JVM throws away compiled code.

## A
一句话：JIT 为了快会做**投机**（只见过一种类型、某分支从没走过、没有第二个实现类）；假设被破坏时，JVM 在 **uncommon trap** 处把执行**回退到解释器**，并作废编译版本（日志里 `made not entrant`），之后重新 profile 再编译。

触发例：
1. 类加载使 CHA 的"只有一个实现"失效。
2. 类型 profile 变化（见到新类型）。
3. 从没走过的分支被走到（`unstable_if`）。
4. 空指针 / 除零等"不应发生"的路径发生。
