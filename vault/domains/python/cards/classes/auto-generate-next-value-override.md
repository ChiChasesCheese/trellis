---
id: auto-generate-next-value-override
node: classes.enums
type: qa
source: python-docs
---
## Q
`auto()` 生成的具体取值是由谁决定的？默认是什么规则，能不能改成用成员名字本身当值？

## A
`auto()` 的取值由类上的 `_generate_next_value_()` 决定，默认实现是『从 1 开始、按声明顺序依次递增的整数』。想改变这个规则（比如让每个成员的值就是它自己的名字字符串），可以在枚举类里重写 `_generate_next_value_(name, start, count, last_values)`，让它返回 `name` 而不是递增整数——唯一的硬性要求是这个重写必须写在所有用到 `auto()` 的成员声明之前，因为 Python 按顺序执行类体，晚定义的重写对前面已经用了 `auto()` 的成员不生效。
