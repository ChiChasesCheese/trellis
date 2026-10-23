---
id: hl-javaq-e-q21-say60
node: java-questions.e-jit-gc
type: qa
step: 30
---
## Q
用英文 60 秒回答：What is deoptimisation? Give an example of when the JVM throws away compiled code.

## A
结构：JIT 投机并设陷阱 → 假设被破坏就回退解释器并标 not entrant → PrintCompilation 实例（类依次加载）→ 教训：用真实的类型与分支多样性预热。

> "The JIT optimises speculatively - for example 'this call site has only ever seen one class', or 'this branch is never taken' - and puts an uncommon trap on the unlikely path. If the assumption breaks, the JVM deoptimises: it transfers the running frame back to the interpreter, marks the compiled method 'not entrant', and recompiles later with fresh profile data. I watched it with `PrintCompilation`: my hot method was compiled assuming one implementation, and the moment a second and then a third class were loaded the compiled versions were marked 'made not entrant' and rebuilt. The practical lesson for a latency-sensitive service is to warm up with a realistic mix of types and branches, otherwise the first real SELL order or error path pays for a deopt."
