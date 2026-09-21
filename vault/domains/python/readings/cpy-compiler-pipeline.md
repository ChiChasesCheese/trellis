---
nodes:
- runtime.compile-bytecode
title: 编译流水线：从源码到字节码经过了几道工序
corpus: cpython-internals
section: 004-compiler-design
url: https://github.com/python/cpython/blob/main/InternalDocs/compiler.md
tags:
- canonical
---

# 编译流水线：从源码到字节码经过了几道工序

这篇讲的是 CPython 编译器的完整流水线：源码先被词法分析、再由 PEG 语法解析成抽象语法树（AST，用 ASDL 描述节点结构），接着 `_PySymtable_Build` 生成符号表确定每个名字的作用域，然后 AST 被转换成一串伪指令，再构造控制流图（CFG）并做窥孔优化，最后汇编成真正的字节码，打包进一个 `PyCodeObject`。读它的价值不是记住这些 C 函数名，而是把“Python 是解释型语言”这句面试常问的话说准确：CPython 并不是逐行扫源码执行，而是先跑一条完整的编译流水线产出字节码，运行时执行的其实是字节码解释器（ceval.c），这也是为什么同一份 `.py` 文件反复运行会被缓存为字节码、以及为什么语法错误在“编译”阶段就会报出来而不是运行到那一行才报。跳过流水线中间的 C 结构体和宏细节，只需要建立“源码→AST→CFG→字节码”这条主线的心智模型。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/python/cpython/blob/main/InternalDocs/compiler.md)

## Archived copy
![[cpy-compiler-pipeline-clip]]
%% trellis:end %%
