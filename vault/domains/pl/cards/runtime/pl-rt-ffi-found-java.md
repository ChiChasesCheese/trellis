---
id: pl-rt-ffi-found-java
node: runtime.ffi
type: qa
step: 2
---
## Q
Java 怎样调用 C 函数？JNI 和 FFM API 分别是什么，各有什么问题？
请用调用 C 的 `strlen` 说明基本流程。

## A
**JNI**（Java Native Interface，Java 1.1 起）：在 Java 里把方法声明为 `native`，再写一个 C 函数，函数名按固定规则拼出来（如 `Java_Foo_bar`），用 `javac -h` 生成头文件，编译成动态库，运行时 `System.loadLibrary`。C 代码通过 `JNIEnv*` 才能访问 Java 对象。问题：必须写、编译、分发 C 胶水；容易写错导致 JVM 崩溃；不同平台要各编一份。

**FFM API**（Foreign Function & Memory API，Java 22 起正式，位于 `java.lang.foreign`）：不用写 C 代码，直接在 Java 里描述 C 函数的签名并调用，同时提供受管理的原生内存：
```java
Linker linker = Linker.nativeLinker();
MethodHandle strlen = linker.downcallHandle(
    linker.defaultLookup().find("strlen").orElseThrow(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));
try (Arena arena = Arena.ofConfined()) {
    MemorySegment s = arena.allocateFrom("hello, ffi");  // C string in native memory
    System.out.println((long) strlen.invokeExact(s));
}
```
输出：`10`。

心智模型：
- `Linker` 找到 C 函数的地址（`find("strlen")`），按 `FunctionDescriptor`（返回 long，参数是一个地址）生成一个能调用它的 `MethodHandle`；
- `Arena` 是原生内存的作用域：`try` 结束时里面分配的内存自动释放，避免泄漏和释放后使用；
- `MemorySegment` 是一段带边界检查的原生内存，Java 不会让你越界访问。
首次使用会收到警告，需要显式授权 `--enable-native-access=ALL-UNNAMED`，因为原生访问可能破坏 JVM 的安全保证（“受限方法”）。

FFM 的价值：让 Java 访问原生库的门槛降到接近 Python 的 `ctypes`，同时保持类型化的描述和内存作用域，取代易错的 JNI。
