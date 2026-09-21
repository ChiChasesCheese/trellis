%% trellis:begin %%
# 渐进类型（gradual typing）、`Any` 与 mypy/pyright 的检查模型
*类型提示与静态检查*

理解 `Any` 与所有类型兼容、检查器如何推断与缩窄（narrowing）、`TYPE_CHECKING` 避免循环导入，以及 `# type: ignore` 的代价。

**Requires:** [[domains/python/map/types.basics|类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束]]

**Unlocks:** [[domains/python/map/types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]]

## Readings
- [[effective-14-collaboration|Effective Python 3e · 第 14 章 协作]]
- [[fluent-08-type-hints-functions|Fluent Python 2e · 第 8 章 函数中的类型提示]]
- [[peps-pep484-type-hints|PEP 484：类型提示（Type Hints）的奠基文档]]
- [[peps-pep649-deferred-annotations|PEP 649：注解的延迟求值]]
- [[pydocs-typing-module|typing 模块：类型提示完整参考]]

## Drills
- [[types-type-a-decorator-and-a-protocol|Drill：给装饰器标注 `ParamSpec`，给鸭子类型参数写 `Protocol`]]

## Cards (5)
1. [[types-gradual-any-vs-object]]
2. [[types-gradual-implicit-any]]
3. [[types-gradual-narrowing-isinstance]]
4. [[types-gradual-type-checking-const]]
5. [[types-gradual-type-ignore-cost]]
%% trellis:end %%

## Notes
