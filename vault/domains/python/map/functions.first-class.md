%% trellis:begin %%
# 一等函数：作为对象传递、高阶函数与 lambda
*函数、闭包与装饰器*

理解函数对象的属性（`__name__`、`__doc__`、`__defaults__`）、把函数当参数与返回值，以及 lambda 只是没有名字的单表达式函数。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/craft.patterns.dry-run-on-a-copy|在副本上试运行：预测与实际共用同一份逻辑]], [[domains/python/map/craft.patterns.rule-chain-pipeline|规则链/流水线：统一接口，引擎只负责按序跑]], [[domains/python/map/craft.patterns.policy-seam|策略接缝：把会变的规则做成注入的纯函数/对象]], [[domains/python/map/craft.idioms.protocol-callable-abc|策略接口三选一：Callable / Protocol / ABC]], [[domains/python/map/craft.idioms.default-forms|省掉标志变量：next(…, None) / min(default=) / for-else / 海象运算符]], [[domains/python/map/craft.idioms.closure-factory-policies|闭包工厂做策略（closure factory）]], [[domains/python/map/craft.idioms.dispatch-tables|数据驱动的分派表：operator 表、方向表、转换表]], [[domains/python/map/craft.architecture.functional-core-imperative-shell|函数式核心 + 命令式外壳（functional core, imperative shell）]], [[domains/python/map/craft.architecture.interface-only-when-earned|接口是挣来的：什么时候不抽象]], [[domains/python/map/craft.architecture.extension-points-worth-paying-for|扩展点值得付费的地方：数据代替代码、从第一天就预留的字段]]

## Readings
- [[fluent-07-first-class-functions|Fluent Python 2e · 第 7 章 一等函数]]
- [[fluent-10-design-patterns-functions|Fluent Python 2e · 第 10 章 一等函数实现的设计模式]]
- [[pydocs-functional-howto|函数式编程 HOWTO]]
- [[pydocs-programming-faq|编程 FAQ：作用域、参数与可变性高频坑]]

## Cards (6)
1. [[closure-vs-callable-object-tradeoff]]
2. [[first-class-functions-60s-pitch]]
3. [[function-object-introspection-attrs]]
4. [[functions-as-first-class-objects]]
5. [[lambda-refactor-rule]]
6. [[lambda-vs-def-when]]
%% trellis:end %%

## Notes
