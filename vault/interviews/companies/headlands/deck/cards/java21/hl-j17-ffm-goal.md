---
id: hl-j17-ffm-goal
node: java21.j17-ffm-api
type: qa
step: 2
---
## Q
Foreign Function & Memory API（FFM）要解决什么问题？它的两个目标分别取代什么？

## A
目标一：**既要堆外内存的好处，又要 Java 级别的安全**（边界检查、生命周期检查），取代 `ByteBuffer.allocateDirect` 和 `sun.misc.Unsafe` 这类手段。

目标二：**取代 JNI**（Java Native Interface）调 C 函数。JNI 要写 C 代码、生成头文件、编译成 `.so`、处理平台差异，繁琐易错；FFM 不用写一行 C 代码。
