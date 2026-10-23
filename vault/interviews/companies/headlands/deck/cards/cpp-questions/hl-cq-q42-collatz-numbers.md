---
id: hl-cq-q42-collatz-numbers
node: cpp-questions.j-cross-language
type: qa
step: 18
---
## Q
对 1 到 300000 的所有数求 Collatz 序列步数总和（结果 35669725），C++ 和 Python 各多久？为什么 Python 慢？NumPy 为什么快？

## A
- C++：约 **24–34 ms**；Python：约 **857 ms**，约慢 **30 倍**。
- Python 慢的原因：每个值都是带引用计数的对象；每次 `+` 都要查类型分派；CPython 默认没有 JIT；GIL 阻止多线程并行。
- NumPy 快：把循环交给 C，在连续的有类型数组上用编译后的代码（带 SIMD）运算，避免每个元素一个 Python 对象。
