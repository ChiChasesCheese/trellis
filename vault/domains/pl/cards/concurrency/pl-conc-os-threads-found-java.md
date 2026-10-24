---
id: pl-conc-os-threads-found-java
node: concurrency.os-threads
type: qa
step: 2
---
## Q
Java 里的 `Thread`、线程池（`ExecutorService`）和 `Future` 各是什么？从零开始，一个“并发算三个平方并拿结果”是怎么做的？

## A
- **`Thread`**：对一个 OS 线程的封装。`new Thread(任务).start()` 让系统新建线程去执行任务；任务是一个没有返回值的 `Runnable`。`join()` 等它结束。
- **线程池**（`ExecutorService`）：预先创建固定数量的线程，反复接任务，避免每个任务都新建线程。`Executors.newFixedThreadPool(3)` 得到一个 3 线程的池。
- **`Future<T>`**：“将来某个时刻会有结果”的凭据。向线程池 `submit` 一个有返回值的任务（`Callable`），立刻拿到 `Future`；调用 `get()` 会阻塞到结果就绪，任务里抛出的异常会在 `get()` 时重新抛出（包装成 `ExecutionException`）。

最小例子：
```java
ExecutorService ex = Executors.newFixedThreadPool(3);
List<Future<Integer>> fs = new ArrayList<>();
for (int i = 1; i <= 3; i++) { final int k = i; fs.add(ex.submit(() -> k * k)); }
for (Future<Integer> f : fs) System.out.println(f.get());
ex.shutdown();
```
输出：`1`、`4`、`9`。三个任务在池里的线程上并发执行，主线程依次取结果。

注意裸线程的陷阱：
```java
Thread t = new Thread(() -> { throw new IllegalStateException("boom"); });
t.start(); t.join();
System.out.println("main continues");
```
输出：stderr 打印 `Exception in thread "Thread-0" java.lang.IllegalStateException: boom`，随后主线程照常输出 `main continues`。裸线程里的未捕获异常只被打印，调用方收不到；用 `Future` 才能把异常带回来。
