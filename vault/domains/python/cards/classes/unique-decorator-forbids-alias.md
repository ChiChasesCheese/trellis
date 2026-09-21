---
id: unique-decorator-forbids-alias
node: classes.enums
type: qa
source: python-docs
---
## Q
如果不希望一个枚举类里出现「同值不同名」的别名，有什么办法在定义时就拦住？

## A
给枚举类加上 `@unique` 装饰器（来自 `enum` 模块）。一旦类体里出现两个成员值相同（也就是本会形成别名的情况），`@unique` 会在类创建时直接抛出 `ValueError`，把『不同名字必须对应不同值』当成硬性约束，而不是默默允许并把后者变成别名。
