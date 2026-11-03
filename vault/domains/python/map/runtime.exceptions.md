%% trellis:begin %%
# 异常：层次结构、`try/except/else/finally`、链式异常与异常组
*解释器与执行模型*

掌握 `BaseException` 与 `Exception` 的分界（`KeyboardInterrupt`/`SystemExit`）、`raise ... from`、`else` 块的用途、EAFP 风格，以及 3.11 `ExceptionGroup` 与 `except*`。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]], [[domains/python/map/craft.patterns.validate-then-commit|先校验后提交：失败不留痕迹（validate-then-commit）]], [[domains/python/map/craft.patterns.transition-table-state-machine|转移表状态机：把「哪个状态能去哪」写成数据（State machine as a table）]], [[domains/python/map/craft.patterns.saga-idempotent-compensation|Saga 与幂等补偿：反向撤销，补偿不能失败也不能重复生效]], [[domains/python/map/craft.patterns.retry-backoff-dead-letter|重试、退避与死信：可靠性写一份，渠道只管怎么发]], [[domains/python/map/craft.idioms.exception-family|异常家族：基类 + 多重继承 + 携带数据（typed errors）]], [[domains/python/map/craft.idioms.validated-construction|构造即校验与规范化（__post_init__ + object.__setattr__）]], [[domains/python/map/craft.architecture.error-boundaries-and-failure-taxonomy|错误边界与失败分类：哪些吞、哪些抛、哪些变成值]], [[domains/python/map/craft.architecture.order-side-effects-by-reversibility|按可逆性给副作用排序：先做会失败的、可回滚的，最后做不可撤销的]]

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
