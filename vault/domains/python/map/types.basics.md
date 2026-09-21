%% trellis:begin %%
# 类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束
*类型提示与静态检查*

掌握注解只是元数据、`list[int]` 与 `List[int]`、`X | None` 语法，以及"类型提示不会让错误的调用失败"这一常被问到的事实。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/types.gradual-typing|渐进类型（gradual typing）、`Any` 与 mypy/pyright 的检查模型]], [[domains/python/map/types.typeddict-literal|`TypedDict`、`Literal`、`NewType` 与 dataclass 注解]]

## Readings
- [[fluent-08-type-hints-functions|Fluent Python 2e · 第 8 章 函数中的类型提示]]
- [[peps-pep484-type-hints|PEP 484：类型提示（Type Hints）的奠基文档]]
- [[peps-pep526-variable-annotations|PEP 526：变量注解语法]]
- [[pydocs-annotations-best-practices|注解（Annotations）最佳实践]]
- [[pydocs-builtin-types|内建类型（Built-in Types）完整参考]]
- [[pydocs-compound-statements|复合语句语法参考：with / try / 泛型参数]]
- [[pydocs-typing-module|typing 模块：类型提示完整参考]]

## Drills
- [[types-type-a-decorator-and-a-protocol|Drill：给装饰器标注 `ParamSpec`，给鸭子类型参数写 `Protocol`]]

## Cards (6)
1. [[types-basics-annotations-are-metadata]]
2. [[types-basics-bad-call-fails-downstream]]
3. [[types-basics-elevator-pitch]]
4. [[types-basics-optional-vs-default-arg]]
5. [[types-basics-pep585-builtin-generics]]
6. [[types-basics-runtime-isinstance-union]]
%% trellis:end %%

## Notes
