---
id: hl-j17-valuelayout
node: java21.j17-ffm-api
type: qa
step: 8
---
## Q
`ValueLayout` 描述什么？`JAVA_LONG` 对偏移有什么要求，不对齐怎么办？

## A
`ValueLayout` 描述「这个位置是什么类型」：`JAVA_LONG`、`JAVA_INT`、`JAVA_DOUBLE`、`JAVA_BYTE`、`ADDRESS`（指针）等。

`JAVA_LONG` 要求偏移是 **8 的倍数**（对齐）；在不 8 字节对齐的偏移访问抛 `IllegalArgumentException`。不对齐访问用 `JAVA_LONG_UNALIGNED`。
