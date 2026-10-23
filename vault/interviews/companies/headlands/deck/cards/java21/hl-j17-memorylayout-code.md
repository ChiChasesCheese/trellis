---
id: hl-j17-memorylayout-code
node: java21.j17-ffm-api
type: qa
step: 9
---
## Q
用 `MemoryLayout` 声明 `struct Fill { long id; long px; int qty; pad }`，取得 `px` 偏移和读写句柄，再声明 100 万个 `FILL` 的数组布局。

## A
```java
static final StructLayout FILL = MemoryLayout.structLayout(
        ValueLayout.JAVA_LONG.withName("id"),
        ValueLayout.JAVA_LONG.withName("px"),
        ValueLayout.JAVA_INT.withName("qty"),
        MemoryLayout.paddingLayout(4));          // 补到 8 的倍数
FILL.byteSize();                                  // 24
FILL.byteOffset(PathElement.groupElement("px"));  // 8，JDK 替你算
VarHandle PX = FILL.varHandle(PathElement.groupElement("px"));
SequenceLayout POOL = MemoryLayout.sequenceLayout(1_000_000, FILL);
```
`structLayout` 像 C 的 `struct`，`sequenceLayout(n, elem)` 像 C 的数组，`paddingLayout` 是显式填充。结果：`byteSize = 24`、`offset(px) = 8`、`offset(qty) = 16`、`alignment = 8`。用声明代替魔法数字。
