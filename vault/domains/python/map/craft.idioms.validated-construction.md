%% trellis:begin %%
# 构造即校验与规范化（__post_init__ + object.__setattr__）
*编码功力（Coding Craft） / 高级写法（Idioms）*

让「存在的实例一定合法」：校验和规范化放进构造，下游不再重复检查。

**Requires:** [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]], [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]], [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]

## Cards (5)
1. [[craft-validated-construction-1-validate-in-post-init]]
2. [[craft-validated-construction-2-copy-then-validate]]
3. [[craft-validated-construction-3-cross-object-invariants]]
4. [[craft-validated-construction-4-across-problems]]
5. [[craft-validated-construction-5-parse-dont-validate]]
%% trellis:end %%

## Notes
