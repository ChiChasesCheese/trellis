---
nodes:
- classes.enums
title: Enum HOWTO：枚举成员是类的单例实例
corpus: python-docs
section: 14-enum
url: https://docs.python.org/3/howto/enum.html
tags:
- canonical
---

# Enum HOWTO：枚举成员是类的单例实例

Enum HOWTO 是标准库枚举的完整说明：从最基础的 `class Color(Enum)` 到 `IntEnum`、`StrEnum`（3.11 起）、`Flag`/`IntFlag` 的位运算组合，再到 `auto()` 的取值规则、`@unique` 对别名的约束、成员迭代顺序按定义顺序、pickle 与 dataclass 混用。读它抓住一个机制：类体里的赋值在元类 `EnumType` 里被拦截，每个成员被替换成该类的一个单例实例，所以 `Color.RED is Color.RED`、成员可比较身份但默认不可比较大小；`IntEnum` 之所以能和整数互换，是因为它同时继承 `int`。带走三点：`auto()` 的默认值是从 1 起的递增整数，`StrEnum` 里则是小写成员名；值相同的成员是别名而不是新成员；`Flag` 的组合值（`Color.RED | Color.BLUE`）是运行时合成的伪成员。面试里用它回答「为什么不用模块级常量」：类型检查、穷举性、`__repr__` 可读性与 `match` 里的类模式。
