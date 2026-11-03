%% trellis:begin %%
# 泛型与类型别名：Generic/TypeVar、Clock 别名、Self 与 override
*编码功力（Coding Craft） / 高级写法（Idioms）*

容器类参数化键值类型；把 Clock = Callable[[], X] 之类的别名统一；copy()/__enter__ 返回 Self；模板方法钩子标 @override。

**Requires:** [[domains/python/map/types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]], [[domains/python/map/types.basics|类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束]], [[domains/python/map/types.gradual-typing|渐进类型（gradual typing）、`Any` 与 mypy/pyright 的检查模型]]

## Cards (5)
1. [[craft-generics-and-type-aliases-1-generic-container-bound]]
2. [[craft-generics-and-type-aliases-2-alias-for-injected-clock]]
3. [[craft-generics-and-type-aliases-3-self-type]]
4. [[craft-generics-and-type-aliases-4-override-decorator]]
5. [[craft-generics-and-type-aliases-5-generics-erased-at-runtime]]
%% trellis:end %%

## Notes
