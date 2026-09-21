---
id: types-gradual-type-ignore-cost
node: types.gradual-typing
type: qa
source: python-docs
---
## Q
`# type: ignore` 注释和 `@no_type_check` 装饰器做的是什么事？它们的代价是什么？

## A
两者都不改变运行时行为——注解本身运行时从不被强制，它们只是告诉静态检查器跳过对这一行/这个函数的类型检查，用来压掉检查器给出的误报（spurious warning）。代价是这段代码此后对真正的类型错误也免疫：如果后续改动在这一行引入了真实的类型 bug，检查器不会再报，只能等运行时出错或靠测试兜底。
