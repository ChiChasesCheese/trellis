---
id: pl-conc-memmodel-pitfall-visibility
node: concurrency.atomics-memory-models
type: qa
step: 9
---
## Q
Java 里用一个普通的 `boolean` 字段让另一个线程停止循环，为什么可能永远停不下来？为什么双重检查锁定（double-checked locking）也依赖 `volatile`？

## A
```java
static boolean stop = false;            // not volatile
Thread w = new Thread(() -> { long n = 0; while (!stop) n++; });
w.setDaemon(true); w.start();
Thread.sleep(200);
stop = true;
w.join(1000);
System.out.println(w.isAlive() ? "STILL RUNNING after 1s" : "exited");
```
输出：`plain flag: worker STILL RUNNING after 1s`。把字段改成 `volatile boolean` 后，同样的代码输出 `exited`（JDK 25 实测）。

原因：循环体里没有任何同步，JIT 编译器有权认为「`stop` 在这个线程里没人改」，把读取提到循环外，变成 `if (!stop) while (true) n++;`。这在单线程语义里完全合法，写线程的 `stop = true` 对这个线程永远不可见。`volatile` 禁止这种优化，并规定每次读都要看到最新的写。

另一个经典陷阱是双重检查锁定的单例：
```java
private static Singleton instance;           // must be volatile
static Singleton get() {
    if (instance == null) {
        synchronized (Singleton.class) {
            if (instance == null) instance = new Singleton();
        }
    }
    return instance;
}
```
`new Singleton()` 包含「分配内存、执行构造函数、把引用赋给 `instance`」三步，可能被重排成先赋引用、后构造。另一个线程在第一个 `if` 看到非空的 `instance`，拿到的是**还没构造完的对象**。声明为 `volatile` 才能禁止这种重排。

Go 里同样要避免用普通变量做标志：用 `atomic.Bool` 或通道；`go run -race` 会报告这类数据竞争。
