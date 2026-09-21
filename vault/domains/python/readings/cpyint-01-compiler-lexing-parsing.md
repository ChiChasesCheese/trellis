---
nodes: [runtime.compile-bytecode]
url: https://realpython.com/products/cpython-internals-book/
tags: [book, no-archive]
title: CPython Internals · 编译器：词法分析与语法分析
---
# CPython Internals · 编译器：词法分析与语法分析

这一部分讲源码到字节码要经过的几个阶段：分词、语法分析生成 AST、再由编译器把 AST翻译成字节码；理解这条流水线，才能看懂为什么 `.pyc` 缓存的是字节码而不是源码，以及 `dis` 模块看到的到底是哪一层产物。

**读时提取：**
- 源码 → token 流 → AST → 字节码这条流水线的四个阶段各做什么
- `.pyc` 文件缓存的是编译后的字节码，运行时跳过重新编译这一步
- 用 `dis.dis()` 看到的字节码指令和源码语句之间大致如何对应

%% trellis:begin %%
## Source
[Open the original ↗](https://realpython.com/products/cpython-internals-book/)
%% trellis:end %%
