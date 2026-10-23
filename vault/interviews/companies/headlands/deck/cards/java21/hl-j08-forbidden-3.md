---
id: hl-j08-forbidden-3
node: java21.j08-var
type: qa
step: 7
---
## Q
`var` 能不能用于字段、方法返回类型、方法参数？它的适用范围一句话怎么说？

## A
都**不能**，报 `'var' is not allowed here`：
- 字段：`var field = 1;`
- 方法返回类型：`static var g()`
- 方法参数：`void h(var p)`

一句话：`var` 只用于**局部变量**，且右边必须自带足够的类型信息。
