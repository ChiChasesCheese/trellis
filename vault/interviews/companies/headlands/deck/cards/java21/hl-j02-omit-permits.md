---
id: hl-j02-omit-permits
node: java21.j02-sealed
type: qa
step: 6
---
## Q
`sealed` 类型什么时候可以省略 `permits`？省略后名单怎么确定？

## A
**子类与父类在同一个 `.java` 文件里**时可以省略：编译器自动把同文件里直接继承它的类当作许可名单。

子类分散在多个文件时必须写 `permits`。即使可以省略，显式写出更易读。
