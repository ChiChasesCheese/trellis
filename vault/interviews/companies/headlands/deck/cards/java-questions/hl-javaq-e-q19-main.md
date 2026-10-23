---
id: hl-javaq-e-q19-main
node: java-questions.e-jit-gc
type: qa
step: 5
---
## Q
什么是内联（inlining）？为什么说它是"优化之母"？JIT 怎么内联虚调用？
What is inlining and why is it "the mother of all optimisations"? How does the JIT inline virtual calls?

## A
一句话：内联把被调方法的代码拷进调用者，消除调用开销，并让后续优化（常量传播、逃逸分析、循环优化）能**跨方法**工作。

虚调用 / 接口调用靠 **类层次分析**（CHA，class hierarchy analysis）+ **类型 profile**：
- 只有一个实现 → 直接内联（带"类层次没变"的依赖，之后加载新实现类就失效并去优化）。
- 调用点见过 1–2 种类型 → 类型检查 + 内联（bimorphic）。
- 见过 ≥3 种（megamorphic）→ 退回虚表 / 接口表调用，不内联。
