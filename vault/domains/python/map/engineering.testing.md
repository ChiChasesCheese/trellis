%% trellis:begin %%
# 测试：pytest 夹具与参数化、`unittest.mock`、注入时钟与依赖
*工程实践：健壮性、测试与交付*

掌握用 fixture 隔离状态、`parametrize` 覆盖边界、`patch` 的作用域与 autospec、把时间与 I/O 作为参数注入以获得确定性测试，以及浮点比较用 `approx`。

**Unlocks:** [[domains/python/map/craft.patterns.injected-clock-three-forms|注入时钟的三种形态：Clock 参数 / 时间戳参数 / tick 步进]], [[domains/python/map/craft.patterns.lazy-expiry-settle-on-access|惰性过期：每次访问先结清，不起后台线程（settle on access）]], [[domains/python/map/craft.patterns.conservation-invariant-reconcile|守恒不变量与对账：总和恒为零、钞票守恒、缓存可核对]], [[domains/python/map/craft.architecture.functional-core-imperative-shell|函数式核心 + 命令式外壳（functional core, imperative shell）]], [[domains/python/map/craft.architecture.seams-for-testing|测试接缝：时钟、文件系统、sleep、可观测计数器]], [[domains/python/map/craft.architecture.observability-as-design|可观测性是设计的一部分：丢弃必须计数，状态变化必须留痕]]

## Readings
- [[effective-13-testing-debugging|Effective Python 3e · 第 13 章 测试与调试]]
- [[pydocs-unittest-mock|unittest.mock：模拟对象库]]

## Drills
- [[engineering-harden-a-payment-script|Drill：把一段收款脚本改成生产可用的版本]]

## Cards (7)
1. [[test-mock-assert-called-once-vs-any-call]]
2. [[test-mock-autospec-catches-typo]]
3. [[test-mock-decorator-context-manager-restore]]
4. [[test-mock-side-effect-vs-return-value]]
5. [[test-mock-where-to-patch]]
6. [[test-pytest-fixture-isolation]]
7. [[test-pytest-parametrize-boundary]]
%% trellis:end %%

## Notes
