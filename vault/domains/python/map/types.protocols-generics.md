%% trellis:begin %%
# `Protocol`、`TypeVar`、`ParamSpec` 与泛型类
*类型提示与静态检查*

掌握结构化子类型如何给鸭子类型加静态检查、`TypeVar` 约束与协变/逆变、3.12 `class Box[T]` 语法，以及装饰器签名保真需要 `ParamSpec`。

**Requires:** [[domains/python/map/types.gradual-typing|渐进类型（gradual typing）、`Any` 与 mypy/pyright 的检查模型]], [[domains/python/map/classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]]

## Readings
- [[fluent-15-more-type-hints|Fluent Python 2e · 第 15 章 深入类型提示]]
- [[peps-pep544-protocols|PEP 544：Protocol 与结构化子类型]]
- [[peps-pep612-paramspec|PEP 612：参数规范变量 ParamSpec]]
- [[peps-pep695-type-parameter-syntax|PEP 695：3.12 类型参数新语法]]
- [[pydocs-compound-statements|复合语句语法参考：with / try / 泛型参数]]
- [[pydocs-typing-module|typing 模块：类型提示完整参考]]

## Drills
- [[types-type-a-decorator-and-a-protocol|Drill：给装饰器标注 `ParamSpec`，给鸭子类型参数写 `Protocol`]]

## Cards (6)
1. [[types-protocols-container-variance]]
2. [[types-protocols-paramspec-decorator]]
3. [[types-protocols-py312-generic-class-syntax]]
4. [[types-protocols-runtime-checkable-cost]]
5. [[types-protocols-typevar-bound-vs-constrained]]
6. [[types-protocols-vs-abc]]
%% trellis:end %%

## Notes
