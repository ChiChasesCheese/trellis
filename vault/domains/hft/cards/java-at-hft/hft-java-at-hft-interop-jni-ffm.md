---
id: hft-java-at-hft-interop-jni-ffm
node: java-at-hft.interop
type: qa
step: 3
---
## Q
Java 调用 C/C++ 本地代码时，JNI 和 FFM API 有什么区别？

## A
**JNI**（Java Native Interface）：要声明 `native` 方法，用 `javac -h` 生成头文件，写 C 胶水代码，编译成 `.so`，平台相关，写错了会直接崩进程。
**FFM API**（Foreign Function & Memory，JDK 22 正式）：全部用 Java 描述——用 `Linker` 和 `FunctionDescriptor` 描述 C 函数的签名，得到一个 `MethodHandle` 直接调用，不需要 C 胶水代码；还能用 `MemorySegment` 把堆外内存的地址直接传给 C，零拷贝。运行时由 JVM 生成调用桩，调用开销与 JNI 同量级或更低。

共同点：每次跨边界都有固定开销（几十纳秒量级），且本地代码里的逻辑无法被 JIT 内联优化；签名写错都可能崩进程，所以调用本地函数是“受限操作”，需要 `--enable-native-access`。
