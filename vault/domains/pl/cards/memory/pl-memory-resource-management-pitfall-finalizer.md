---
id: pl-memory-resource-management-pitfall-finalizer
node: memory.resource-management
type: qa
step: 9
---
## Q
为什么不能靠终结器（finalizer）来释放资源？Go 和 Java 里这个陷阱具体是什么样？

## A
终结器是对象被 GC 回收「之后」才运行的回调。三个问题：
1. **不保证运行**：程序退出时通常不会为还没回收的对象运行终结器。
2. **时机不可控**：堆里内存充裕时，GC 可能很久不运行，而文件描述符早就耗尽了。
3. **在垃圾回收线程里运行**：可能引起竞争、复活对象、拖慢回收。

```go
t := &T{1}
runtime.SetFinalizer(t, func(t *T) { fmt.Println("finalized") })
t = nil
fmt.Println("exit")
```

```java
@Override protected void finalize() { System.out.println("finalized"); }
public static void main(String[] a) { new Fin(); System.out.println("exit"); }
```

两段程序的实测输出都只有：

```console
exit
```

`finalized` 从未出现。Java 编译时还会警告 `finalize() in Object has been deprecated and marked for removal`。

另一个与资源管理相关的 Go 陷阱是循环里的 `defer`：

```go
for i := 0; i < 3; i++ {
	f, _ := os.CreateTemp("", "x")
	defer f.Close()          // runs when the function returns, not per iteration
}
```

三个文件会一直打开到函数结束。处理一万个文件的循环，可能在第一千个时就耗尽文件描述符。修复：把循环体提成函数，让 `defer` 在每次调用结束时执行。

对策：终结器和清理器（Java 的 `Cleaner`、Go 的 `runtime.AddCleanup`）只当作泄漏的最后一道保险，并配合日志，发现被触发就说明有地方漏了正常的关闭。
