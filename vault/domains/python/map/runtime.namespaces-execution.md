%% trellis:begin %%
# 执行模型：命名空间、`global`、代码块与 `exec`/`eval` 的风险
*解释器与执行模型*

理解模块、类体、函数体各自的命名空间与执行时机、类体是在类创建时执行的代码块，以及 `exec`/`eval` 为何只用于开发工具。

**Requires:** [[domains/python/map/functions.scope-closure|作用域（LEGB）、闭包与 `nonlocal`]]

## Readings
- [[pydocs-execution-model|执行模型：命名空间与作用域]]

## Cards (6)
1. [[builtins-namespace-lookup-via-dunder]]
2. [[class-body-namespace-becomes-dict]]
3. [[comprehension-in-class-body-cannot-see-class-scope]]
4. [[exec-eval-skip-enclosing-closure-scope]]
5. [[free-variable-resolved-at-call-time]]
6. [[module-namespace-created-on-first-import-and-main]]
%% trellis:end %%

## Notes
