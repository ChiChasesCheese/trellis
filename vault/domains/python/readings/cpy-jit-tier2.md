---
nodes:
- runtime.adaptive-jit
title: 分层执行：从追踪记录到 copy-and-patch JIT
corpus: cpython-internals
section: 009-the-jit
url: https://github.com/python/cpython/tree/main/InternalDocs
tags:
- canonical
---

# 分层执行：从追踪记录到 copy-and-patch JIT

在“逐指令特化”（tier 1）之上，CPython 还有一层实验性的 JIT（tier 2）：某段循环被判定“热”之后，解释器切到追踪模式，把连续执行的字节码翻译成更细粒度的微操作（micro-ops/uops）序列并加以优化，生成一个执行器（executor）；如果编译时开启了完整 JIT（`--enable-experimental-jit`），这段 uops 还会用 copy-and-patch 技术（用预先编译好的代码片段“stencil”在运行时拼接、填充具体信息）直接生成机器码，跳过解释开销。读这篇的价值是知道“Python 3.13 有实验性 JIT”这句话具体指什么阶段、以及它和一般语言的 JIT（如 V8 的分层编译）思路的相似与不同——它仍处于实验阶段，面试里被问到时可以准确地说“基于 copy-and-patch，处于早期、默认不开启”，而不是笼统地说“Python 出 JIT 了”。
