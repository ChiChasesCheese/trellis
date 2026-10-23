---
id: hl-j17-quiz-layout
node: java21.j17-ffm-api
type: qa
step: 23
---
## Q
用 `MemoryLayout` 写 `struct { int side; int qty; long px; }` 的布局，并说出 `px` 的偏移和总大小。

## A
```java
StructLayout L = MemoryLayout.structLayout(
    ValueLayout.JAVA_INT.withName("side"),
    ValueLayout.JAVA_INT.withName("qty"),
    ValueLayout.JAVA_LONG.withName("px"));
```
`px` 偏移 **8**（前两个 `int` 共 8 字节，且正好 8 字节对齐），总大小 **16**，不需要 padding。
