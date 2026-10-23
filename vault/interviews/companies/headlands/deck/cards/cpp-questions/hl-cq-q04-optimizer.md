---
id: hl-cq-q04-optimizer
node: cpp-questions.a-why-fast
type: qa
step: 20
---
## Q
面试题：`-O2` 下优化器实际做了什么？你怎么验证？
What does the optimizer actually do at `-O2`? How would you verify it?

## A
一句话：内联、常量折叠、死代码删除、循环优化（展开、向量化、把循环改写成闭式）、去虚化、复制省略。

验证方法：**读汇编（`-S`）或测量**，不要凭感觉。

什么会挡住优化器：
- 跨翻译单元的调用（没开 LTO）；
- 通过基类指针的虚调用（类型未知）；
- 指针别名（两个指针可能指向同一块内存，不敢重排）；
- `volatile`；
- 异常路径。
