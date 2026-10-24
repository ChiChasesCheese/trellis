---
id: pl-foundations-language-vs-implementation-history-specs
node: foundations.language-vs-implementation
type: qa
step: 9
---
## Q
Java、Go、Rust、Python 的规范和替代实现是怎样发展起来的？今天的趋势是什么？

## A
- Java：1996 年随 JDK 1.0 发布语言规范（JLS）和虚拟机规范（JVMS）。早期 Sun 的实现是唯一选择；2006 到 2007 年 Sun 将 JDK 开源，形成 OpenJDK，从此 HotSpot 之外有了 OpenJ9、GraalVM 等实现。
- Go：2009 年发布时就同时带有 `gc` 和 gccgo 两个编译器，规范因此写得很精确，必须让两个实现表现一致。
- Python：长期只有 CPython；PyPy 在 2000 年代后期成熟，目标是用 JIT 提速；MicroPython 面向单片机，GraalPy 面向 GraalVM。语言变更走 PEP（Python Enhancement Proposal）流程。
- Rust：2015 年发布 1.0 后一直以 `rustc` 为准；安全关键行业（汽车、航空）需要正式规范，于是出现了 Ferrocene 语言规范（FLS）等规范化工作，GCC 也在开发另一个前端 `gccrs`。

趋势：当一门语言进入对可靠性有硬要求的领域，就会逼出正式规范和多个实现，因为认证机构要求能写出「它应当做什么」，而不仅仅是「编译器碰巧做什么」。另一个趋势相反：在同一个实现内部出现可选模式，如 CPython 3.13 的实验性 JIT 和自由线程构建，它们是同一语言下的不同实现配置。
