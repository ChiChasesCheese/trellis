%% trellis:begin %%
# 结构化模式匹配：`match`/`case`、捕获、守卫与类模式
*迭代器、生成器与上下文管理器*

理解 3.10 的 `match` 不是 switch：模式会解构序列、映射与类实例并绑定名字，`case _` 兜底、`if` 守卫、`__match_args__` 决定位置模式，以及什么时候一串 `if` 反而更清楚。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/craft.patterns.recursive-descent-parsing|递归下降解析：优先级 = 调用层次，分词与求值分离]], [[domains/python/map/craft.idioms.match-structural|结构化模式匹配：对 dataclass 与枚举的 match / case]], [[domains/python/map/craft.idioms.exhaustive-match-assert-never|穷尽性：match 加 assert_never（解法没用，应该用）]]

## Readings
- [[peps-pattern-matching-tutorial|PEP 636：结构化模式匹配教程]]

## Cards (6)
1. [[bare-name-in-pattern-always-captures]]
2. [[guard-checked-after-bind-fallthrough-keeps-bindings]]
3. [[match-args-defines-positional-pattern-order]]
4. [[match-is-not-a-switch-statement]]
5. [[match-tries-patterns-top-to-bottom-first-wins]]
6. [[or-pattern-alternatives-must-bind-same-names]]
%% trellis:end %%

## Notes
