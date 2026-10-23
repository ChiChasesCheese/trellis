---
id: hl-javaq-e-q19-megamorphic
node: java-questions.e-jit-gc
type: qa
step: 6
---
## Q
接口调用点分别见到 1 种、2 种、3 种实现类时，JIT 生成什么代码？稳态每次调用耗时各约多少？

## A
- **1 种实现**（CHA）：直接内联 `Sq.area`，无需检查；耗时约 **0.27–0.38 ns/次**。
- **2 种见过**（bimorphic）：`if (s.class == Sq) {内联Sq} else if (s.class == Tri) {内联Tri} else {去优化或虚调用}`；约 **0.34–0.36 ns/次**。
- **≥3 种**（megamorphic）：通过 itable / vtable 间接调用，不内联，每次一次间接跳转且无法跨调用优化；约 **0.9 → 1.35 ns/次**，约慢 4 倍。
- 在 `PrintInlining` 里能看到：`inline (hot)` 表示内联；`virtual call` 表示没内联（见过的类型太多）；`no static binding` 同理。
