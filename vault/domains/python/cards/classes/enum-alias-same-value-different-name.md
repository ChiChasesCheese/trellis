---
id: enum-alias-same-value-different-name
node: classes.enums
type: qa
source: python-docs
---
## Q
同一个枚举类里可以有两个名字对应同一个值吗？这两个名字是什么关系，`list(SomeEnum)` 会把它们都列出来吗？

## A
可以。按值排在后面定义的那个名字会成为先定义的那个成员的「别名（alias）」，而不是独立的新成员——按值查（`SomeEnum(值)`）和按别名查（`SomeEnum.别名名`）都会返回同一个（先定义的）成员对象。但反过来，两个成员不能重名（`TypeError`）。遍历枚举（`list(SomeEnum)` 或 `for m in SomeEnum`）只会给出规范成员，不包含别名；要看到全部名字（含别名），需要读 `SomeEnum.__members__` 这个只读的有序映射。
