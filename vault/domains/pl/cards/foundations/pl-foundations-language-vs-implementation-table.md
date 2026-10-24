---
id: pl-foundations-language-vs-implementation-table
node: foundations.language-vs-implementation
type: qa
step: 5
---
## Q
C++、Go、Java、Rust、Python 各自怎样定义「语言是什么」？这种定义方式换来什么，又付出什么？

## A
| 语言 | 定义方式与主要实现 | 换来 | 代价 |
|---|---|---|---|
| Go | 语言规范加官方实现 `gc`，另有 gccgo、TinyGo | 规范精确，官方实现占绝对主导，演进可控 | 替代实现的生态很小，TinyGo 等只支持子集 |
| C++ | ISO 标准（委员会每三年出一版）；GCC、Clang、MSVC 三大实现并存 | 没有单一厂商控制，多平台多编译器竞争，标准把「不规定」也白纸黑字写出来（未定义、未指明、实现定义行为） | 标准落地比发布晚，各编译器、各标准库（libstdc++、libc++、MSVC STL）支持进度和 ABI（二进制接口约定）不一致，同一份代码换编译器可能行为不同 |
| Java | JLS 加 JVMS 两份规范，TCK 认证；HotSpot、GraalVM、OpenJ9 | 多厂商竞争，同一字节码可以换虚拟机；Kotlin、Scala 共享 JVM | 规范和测试要长期维护，新特性走 JEP，节奏慢 |
| Rust | `rustc` 即标准，Rust Reference 说明性文档 | 演进快，没有实现分歧 | 替代实现（`gccrs`、`mrustc`）追赶困难，安全认证领域缺正式规范 |
| Python | Language Reference 加参考实现 CPython，PEP 流程 | 创新快，C 扩展生态极大 | C 扩展接口绑定 CPython 内部结构，PyPy 等实现兼容 NumPy 之类扩展很吃力 |

背后的逻辑：「规范加认证」是 Java 为企业客户设计的：企业要避免被单一厂商锁定，所以 Sun 把语言和机器都写成合同。「参考实现即标准」是社区驱动语言的自然选择：先有一个好用的实现，规范是后来才补的文档。这两条路的代价对称：前者演进慢，后者生态耦合重。C++ 属于前一类里最彻底的一例：它只规定源码语义，不规定二进制，也没有统一的认证测试，委员会因此宁可把难以统一的行为留空（未定义行为，UB），让各编译器自由优化，代价就是可移植性要程序员自己守。判断一个看似语言级的限制（如 GIL、小整数缓存）是不是实现细节，办法是看规范有没有承诺它。
