---
id: hl-javaq-e-q19-say60
node: java-questions.e-jit-gc
type: qa
step: 28
---
## Q
用英文 60 秒回答：What is inlining and why is it "the mother of all optimisations"? How does the JIT inline virtual calls?

## A
结构：内联消除调用开销并打开其他优化 → 虚调用靠 CHA 加类型 profile → 单态、双态内联，三种以上变 megamorphic → 实测 0.3 对 1.35 ns → 方法大小阈值。

> "Inlining removes call overhead but more importantly it opens up other optimisations - once the callee's body is in the caller, the JIT can propagate constants, eliminate allocations by escape analysis, and hoist checks out of loops. For virtual and interface calls, HotSpot uses class-hierarchy analysis and the type profile: if only one implementation is loaded it inlines directly, and if the call site has seen one or two receiver types it inlines with a type check. With three or more it goes megamorphic and does a table dispatch. I measured that: about 0.3 ns per call with one or two implementations and about 1.35 ns with three. Methods also have to be small enough: 35 bytecodes when cold, 325 when hot, by default."
