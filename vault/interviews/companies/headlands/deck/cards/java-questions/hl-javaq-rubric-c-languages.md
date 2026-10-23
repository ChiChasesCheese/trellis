---
id: hl-javaq-rubric-c-languages
node: java-questions.rubric
type: qa
step: 6
---
## Q
回答"Java 对 Python、智能指针、未定义行为、泛型 vs 模板"这类语言对比与所有权问题，强、一般、弱的答案各有什么特征？

## A
- **强**：Java vs Python——静态 / 动态、JIT / 解释、GIL、整数语义（回绕 vs 大整数、`/` 与 `%` 对负数的差异），并给选型。智能指针——Java 没有所有权，GC 做可达性，`WeakReference` ≈ `weak_ptr`，RAII ≈ try-with-resources，`finalize` 被弃用，`Cleaner` 无时机保证。泛型——擦除 → 装箱 → 内存与缓存代价，Valhalla 是动机但 21 还没有。
- **一般**：答对表面（"Java 有 GC 所以不用智能指针"），但不提非内存资源要显式关闭；泛型只说"编译期检查"。
- **弱**：说"Java 的引用就是 C++ 指针"；"Java 对象按引用传递"（应为**引用按值传递**）；不知道循环引用在 GC 下不是问题。
