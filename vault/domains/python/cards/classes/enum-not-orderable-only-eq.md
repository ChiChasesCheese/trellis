---
id: enum-not-orderable-only-eq
node: classes.enums
type: qa
source: python-docs
---
## Q
普通 `Enum`（不是 `IntEnum`）的成员之间能不能用 `<`、`>` 比较大小？能不能用 `==` 判断相等？

## A
不能排序：`Color.RED < Color.BLUE` 直接抛 `TypeError`，因为普通枚举成员不是数字，不携带『大小』这个语义，只是一组带名字的独立符号。但可以判断相等：`==`/`!=` 是支持的，且和其它非本枚举类型的值比较（包括数值上相等的整数）恒为不相等——这一点被 `IntEnum` 故意打破了，是普通 `Enum` 和 `IntEnum` 最核心的行为差异之一。
