%% trellis:begin %%
# 递归下降解析：优先级 = 调用层次，分词与求值分离
*编码功力（Coding Craft） / 跨题模式（Patterns）*

词法（正则切 token）→ 语法（每个优先级一个函数，低优先级先调用）→ 语法树（frozen 节点）→ 求值。

**Requires:** [[domains/python/map/iteration.pattern-matching|结构化模式匹配：`match`/`case`、捕获、守卫与类模式]], [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]

## Cards (5)
1. [[craft-recursive-descent-parsing-1-precedence-is-call-depth]]
2. [[craft-recursive-descent-parsing-2-tokenizer-regex]]
3. [[craft-recursive-descent-parsing-3-loop-for-associativity]]
4. [[craft-recursive-descent-parsing-4-errors-and-leftovers]]
5. [[craft-recursive-descent-parsing-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
