---
id: pl-conc-locks-found-mutex
node: concurrency.locks-shared-memory
type: qa
step: 2
---
## Q
Java 的 `synchronized`、Go 的 `sync.Mutex`、Python 的 `threading.Lock` 怎么保护一个共享计数器？加锁解锁的基本流程和“保证一定解锁”的写法是什么？

## A
三者本质一样：一把互斥锁，同一时刻只有一个线程能持有，其他线程在 `lock` 处等待，持有者释放后才轮到下一个。临界区就是“持锁期间执行的代码”。

**Java**：`synchronized (obj) { ... }` 把任意对象当锁，进入块时加锁，**离开块时（包括抛异常）自动释放**：
```java
static final Object lock = new Object();
static int locked = 0;
// 4 threads, each:
for (int j = 0; j < 1_000_000; j++) synchronized (lock) { locked++; }
```
输出：`synchronized: 4000000`。（去掉 `synchronized` 得到 `1050193`，丢了大量更新。）

**Go**：`sync.Mutex` 有 `Lock()` 和 `Unlock()`，惯用写法是加锁后立刻 `defer mu.Unlock()`，保证函数返回时无论如何都会释放：
```go
var mu sync.Mutex
var n int
// 4 goroutines, each:
for j := 0; j < 1_000_000; j++ { mu.Lock(); n++; mu.Unlock() }
```
输出：`sync.Mutex: 4000000`。

**Python**：`threading.Lock` 配合 `with`，进入时 `acquire`，离开时 `release`：
```python
lock = threading.Lock()
with lock:
    n += 1
```
**为什么必须保证释放**：忘了解锁（尤其是在异常路径上）会让所有等待者永远卡住。所以三种语言都提供了“绑定到作用域”的写法：Java 的块、Go 的 `defer`、Python 的 `with`。

**锁保护的是“不变量”**：`n++` 是读、加、写三步，两个线程交错会丢更新；锁保证这三步不被打断。但锁只有在**所有**访问该数据的代码都用同一把锁时才有用，漏掉一处就等于没锁。
