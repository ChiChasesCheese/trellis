%% trellis:begin %%
# 穷尽性：match 加 assert_never（解法没用，应该用）
*编码功力（Coding Craft） / 高级写法（Idioms）*

所有 match/if-elif 都没有穷尽性保护；加一个新枚举成员时，漏处理的分支会静默通过。

**Requires:** [[domains/python/map/iteration.pattern-matching|结构化模式匹配：`match`/`case`、捕获、守卫与类模式]], [[domains/python/map/types.gradual-typing|渐进类型（gradual typing）、`Any` 与 mypy/pyright 的检查模型]]

## Cards (4)
1. [[craft-exhaustive-match-assert-never-1-silent-fallthrough]]
2. [[craft-exhaustive-match-assert-never-2-default-is-a-bug]]
3. [[craft-exhaustive-match-assert-never-3-if-chain-and-test-net]]
4. [[craft-exhaustive-match-assert-never-4-scales-unknown-variant]]
%% trellis:end %%

## Notes
