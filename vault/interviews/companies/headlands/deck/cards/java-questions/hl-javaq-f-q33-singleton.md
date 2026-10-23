---
id: hl-javaq-f-q33-singleton
node: java-questions.f-concurrency
type: qa
step: 28
---
## Q
写出线程安全的惰性单例：正确的 DCL 写法，以及更干净的 Holder 写法。

## A
正确 DCL（`inst` 必须 `volatile`）：
```java
private static volatile Foo inst;
static Foo get() {
    if (inst == null) synchronized (L) {
        if (inst == null) inst = new Foo();
    }
    return inst;
}
```
最干净是不用 DCL：**静态内部类持有者**（类初始化由 JVM 保证线程安全且惰性）：
```java
class Holder { static final Foo INSTANCE = new Foo(); }
```
也可用枚举单例。这类重排 bug 在 arm64 / x86 + JIT 下不易稳定复现，讲清机制即可，不必现场演示。
