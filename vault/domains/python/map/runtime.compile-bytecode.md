%% trellis:begin %%
# 从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存
*解释器与执行模型*

理解 CPython 先编译为字节码再解释执行、`__pycache__` 按源码时间戳/哈希失效、`dis` 如何用于解释性能差异，以及"Python 是解释型语言"这句话的准确含义。

**Unlocks:** [[domains/python/map/runtime.frames-eval|求值循环与帧：调用栈、递归限制与尾调用]], [[domains/python/map/runtime.import-system|导入系统：模块对象、`sys.modules`、包与循环导入]]

## Readings
- [[cpy-code-objects|代码对象：字节码之外还带着什么]]
- [[cpy-compiler-pipeline|编译流水线：从源码到字节码经过了几道工序]]
- [[cpyint-01-compiler-lexing-parsing|CPython Internals · 编译器：词法分析与语法分析]]
- [[effective-11-performance|Effective Python 3e · 第 11 章 性能]]
- [[pydocs-dis-module|dis 模块：字节码反汇编]]
- [[pydocs-tutorial-modules|Python 教程第 6 章：模块]]

## Drills
- [[runtime-explain-the-traceback-and-the-import-cycle|Drill：解释一个循环导入报错，再解释一个「异常被吞掉」的 traceback]]

## Cards (6)
1. [[code-object-composition]]
2. [[compile-pipeline-stages]]
3. [[interpreted-language-dis-soundbite]]
4. [[pyc-cache-invalidation]]
5. [[pyc-cross-version-coexist]]
6. [[pyc-speeds-loading-not-execution]]
%% trellis:end %%

## Notes
