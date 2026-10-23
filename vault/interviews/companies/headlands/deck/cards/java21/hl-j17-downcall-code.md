---
id: hl-j17-downcall-code
node: java21.j17-ffm-api
type: qa
step: 12
---
## Q
写出用 FFM 调 C 的 `strlen`（`size_t strlen(const char*)`）的完整代码，包括传入字符串。

## A
```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
        linker.defaultLookup().find("strlen").orElseThrow(),
        FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));
try (Arena arena = Arena.ofConfined()) {
    MemorySegment cStr = arena.allocateUtf8String("AAPL.O");
    long len = (long) strlen.invokeExact(cStr);       // 6
}
```
- `downcall`：Java 调 C。`FunctionDescriptor.of(返回类型, 参数类型...)` 描述 C 签名，得到 `MethodHandle`。
- `allocateUtf8String`（JDK 21 名字）把 Java 字符串复制成以 `\0` 结尾的 C 字符串。
- 不用写一行 C 代码。
