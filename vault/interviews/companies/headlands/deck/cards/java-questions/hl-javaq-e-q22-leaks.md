---
id: hl-javaq-e-q22-leaks
node: java-questions.e-jit-gc
type: qa
step: 18
---
## Q
Java 里的"内存泄漏"是什么意思？常见成因有哪些？分代假说什么时候失效？
What's a Java memory leak? What's the generational hypothesis and when does it fail?

## A
- **Java 的泄漏**：对象不再需要，但仍然**可达**（GC 根能引用到）。
- **常见成因**：静态集合 / 缓存、监听器未注销、`ThreadLocal`、无上限的缓存。
- **分代假说失效**：缓存或大量**中等寿命**的对象 → 晋升多，老年代压力大。
