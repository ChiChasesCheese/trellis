---
id: intenum-strenum-vs-flag-when-to-use
node: classes.enums
type: qa
source: python-docs
---
## Q
什么时候该用 `IntEnum`/`StrEnum` 而不是裸的整数/字符串常量？什么时候又该用 `Flag`/`IntFlag` 而不是普通 `Enum`？

## A
`IntEnum`/`StrEnum` 本身就是 `int`/`str` 的子类，能直接参与需要真正整数/字符串的场景（比如当数组下标、和外部 API 的整数状态码互相比较），同时还带上枚举名字带来的可读 `repr()` 和类型分组——比裸常量多了自文档性，又不像普通 `Enum` 那样完全不能和 `int`/`str` 混用。`Flag`/`IntFlag` 用在「需要用位运算把多个选项组合成一个值」的场景（比如权限位 `R|W|X`）：普通 `Enum` 的成员之间没有位运算意义，`Flag` 系列的值天然是 2 的幂，`|`、`&`、`^`、`~` 运算后仍然是同一个枚举类型的合法成员，还能对组合值做遍历还原出各个位。
