---
id: pl-foundations-tradeoff-axes-found-gc
node: foundations.tradeoff-axes
type: qa
step: 3
---
## Q
垃圾回收（garbage collection，GC）是什么？它为 Go、Java、Python 的使用者换来什么、拿走什么？

## A
GC 是运行时的一个组件，自动找出程序再也用不到的对象并回收内存。判断「用不到」的依据是可达性：从根（栈上的变量、全局变量）出发，沿引用能走到的对象是活的，走不到的就是垃圾。程序员不需要、也不能手动释放。

```java
Object o = new Object();
WeakReference<Object> w = new WeakReference<>(o);   // 弱引用：不阻止回收
System.out.println(w.get() != null);   // true
o = null;                              // 对象不再可达
System.gc();                           // 建议运行一次 GC
Thread.sleep(100);
System.out.println(w.get() != null);   // false
```

实际输出 `true` 然后 `false`：`o = null` 之后对象没有强引用，GC 回收了它，弱引用被清空。

换来的是：不会出现释放后使用、重复释放，内存管理的心智负担几乎为零，循环引用也不是问题。拿走的是：回收的时机由运行时决定，需要额外的 CPU 和内存（堆通常要预留余量），GC 工作时可能造成延迟波动。Go 和 Java 使用追踪式 GC，Python 以引用计数为主；Rust 与此不同，没有 GC，靠所有权在编译期决定何时释放；C++ 也没有 GC，靠 RAII（对象离开作用域时析构函数自动释放资源）在固定时刻释放，但是否用对由程序员负责。
