%% trellis:begin %%
# 不可变值对象（frozen + slots dataclass as value object）
*编码功力（Coding Craft） / 高级写法（Idioms）*

事件、配置、快照、键都写成 @dataclass(frozen=True, slots=True)：免费得到 ==、hash 和只读。

**Requires:** [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]], [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]], [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]]

## Cards (5)
1. [[craft-frozen-value-objects-1-fingerprint-by-value]]
2. [[craft-frozen-value-objects-2-not-deep]]
3. [[craft-frozen-value-objects-3-eq-hash-slots]]
4. [[craft-frozen-value-objects-4-across-problems]]
5. [[craft-frozen-value-objects-5-scales]]
%% trellis:end %%

## Notes
