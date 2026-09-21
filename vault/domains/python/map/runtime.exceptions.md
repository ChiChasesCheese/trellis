%% trellis:begin %%
# 异常：层次结构、`try/except/else/finally`、链式异常与异常组
*解释器与执行模型*

掌握 `BaseException` 与 `Exception` 的分界（`KeyboardInterrupt`/`SystemExit`）、`raise ... from`、`else` 块的用途、EAFP 风格，以及 3.11 `ExceptionGroup` 与 `except*`。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]]

## Readings
- [[cpy-code-objects|代码对象：字节码之外还带着什么]]
- [[cpy-exception-table|零成本异常处理：try 不抛异常时到底付了多少代价]]
- [[effective-10-robustness|Effective Python 3e · 第 10 章 健壮性]]
- [[peps-pep3134-exception-chaining|PEP 3134：异常链与内嵌回溯]]
- [[peps-pep654-exception-groups|PEP 654：异常组与 except*]]
- [[pydocs-builtin-exceptions|内建异常完整参考]]
- [[pydocs-compound-statements|复合语句语法参考：with / try / 泛型参数]]
- [[pydocs-tutorial-errors|Python 教程第 8 章：错误与异常]]

## Drills
- [[runtime-explain-the-traceback-and-the-import-cycle|Drill：解释一个循环导入报错，再解释一个「异常被吞掉」的 traceback]]

## Cards (6)
1. [[else-clause-scopes-exception-handling]]
2. [[except-as-name-deleted-to-break-refcycle]]
3. [[except-star-wraps-into-exceptiongroup]]
4. [[exception-table-lookup-and-propagation]]
5. [[finally-return-swallows-exception]]
6. [[zero-cost-exception-handling]]
%% trellis:end %%

## Notes
