---
id: types-typeddict-literal-runtime-permissive
node: types.typeddict-literal
type: qa
source: python-docs
---
## Q
`type Mode = Literal['r', 'rb', 'w', 'wb']` 之后，运行时往标注为 `Mode` 的参数里传一个不在列表里的字符串（比如 `'typo'`）会怎样？

## A
运行时什么也不会发生——`Literal[...]` 在运行时对参数值没有任何约束，任意值都能传进去，只有静态检查器会在 `open_helper('/path', 'typo')` 这类调用上报错。`Literal[...]` 本身也不能被子类化或实例化，它只是一种「值被限定在给定集合内」的注解语法糖。
