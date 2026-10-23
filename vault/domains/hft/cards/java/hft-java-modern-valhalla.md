---
id: hft-java-modern-valhalla
node: java.modern
type: qa
step: 4
---
## Q
Project Valhalla 的值类（value class）要解决什么问题？

## A
问题：Java 的对象都带对象头，并且通过引用访问；`Point[]` 其实是指针数组，对象散落在堆里，既占内存又不利于缓存。

**值类**是没有“身份”（identity）的类。因为不需要身份，JVM 可以把它**扁平化**（flatten）：`Point[]` 直接连续存放 `x`、`y` 字段，没有对象头、没有间接引用，局部变量甚至可以放在寄存器里。效果是内存布局像 `int` 一样紧凑，但仍保留类的抽象。

例：`record Point(int x, int y)` 作为普通对象，12 字节头加 8 字节字段对齐成 24 字节，数组里再加一个 4 字节引用，共约 28 字节；扁平化后每个只要 8 字节，约小 3.5 倍。Money、Price 这类小型数据，可以 100 万个连续存放，既缓存友好又减少 GC 压力。

状态：这是仍在推进中的长期项目，是否可用要看具体的 JDK 版本，不能当作已经可用的特性。
