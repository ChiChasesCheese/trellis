# J11 · 结构化并发 `StructuredTaskScope`：让一组线程「同生共死」

> **Java 21 预览（Preview）API。** 用它必须 `javac --release 21 --enable-preview` 编译、`java --enable-preview` 运行。预览意味着**后续版本可不兼容地改**——它确实改了（5.1）。本课代码只在 JDK 21 上能编译。
> 历史：JDK 19、20 孵化 → **21 预览** → 22–24 继续预览 → 25 API 大改 → 26 第六次预览。
> 可运行代码：`examples/J11/`。前置：J10（虚拟线程）；会 `ExecutorService.submit`、`Future.get`、`InterruptedException`。

---

## 1. 先看痛点：「非结构化」的并发，线程像 `goto` 一样到处乱跳

### 1.1 从零讲：结构化编程是什么

早年程序员用 `goto` 随意跳转，读代码的人不知道「执行流从哪来、到哪去」。1968 年 Dijkstra 发表《Go To Statement Considered Harmful》，共识成了**结构化编程**（structured programming）：只用 `if` / `for` / 方法调用，每个代码块**一个入口、一个出口**，块里开始的事在块结束前一定做完。

```java
void f() {
    g();        // g 一定在这里结束，f 才会继续
    h();
}               // f 返回时，g 和 h 都已经完成了
```

单线程里我们天天享受这个保证，一开线程就没了：

```java
void f() {
    new Thread(() -> g()).start();   // g 什么时候结束？f 返回之后？没人知道
}
```

`f()` 返回了 `g()` 可能还在跑；`g()` 抛异常，`f()` 的调用者永远不知道；线程拿着的资源（连接、文件）可能没人关。

### 1.2 Java 8 里具体有多痛

`examples/J11/J11Old.java`：并行做两件事，一件 1500ms 后成功，一件 100ms 后失败：

```java
ExecutorService pool = Executors.newFixedThreadPool(2);
Future<String> a = pool.submit(J11Old::slowOk);     // 1500ms 后成功
Future<String> b = pool.submit(J11Old::fastFail);   // 100ms 后抛异常
try {
    System.out.println(a.get());   // 先等 a
    System.out.println(b.get());
} catch (ExecutionException e) { ... } finally { pool.shutdown(); }
```

输出：

```
  [slowOk 跑完了——白干了，因为 fastFail 早就失败了]
ok
main 终于发现失败: java.lang.IllegalStateException: risk service down
```

四个痛点同时出现：

1. **失败不传播**：`b` 100ms 就失败，`main` 却在 `a.get()` 上傻等了 1.5 秒。
2. **取消不传播**：`b` 失败后 `a` 已没意义，却被允许做完（可能是昂贵的下游调用），得自己写 `a.cancel(true)`。
3. **泄漏**：任何异常路径漏掉 `shutdown()`/`cancel()`，线程和下游请求就成孤儿。
4. **看不清谁是谁的父**：线程 dump 里这两个线程与发起它们的方法毫无关系，排查生产问题很难把线程对回某个请求。

**结构化并发**的主张：「开一组子任务」也成为有入口有出口的代码块——**块结束时所有子任务一定已结束或被取消**，失败可统一处理。

---

## 2. 语法逐条讲

> 以下是 **JDK 21 预览 API**；JDK 25 之后写法完全不同，见 5.1 对照。

### 2.1 骨架

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {   // 1. 开一个作用域
    Subtask<String>  quote = scope.fork(() -> fetchQuote());      // 2. fork：每个子任务一个（默认虚拟）线程
    Subtask<Integer> limit = scope.fork(() -> fetchLimit());

    scope.join()              // 3. 等所有子任务结束，或者策略决定提前结束
         .throwIfFailed();    // 4. 按策略检查结果（这里：有失败就抛）

    use(quote.get(), limit.get());   // 5. join 之后才能 get
}                                    // 6. 退出块：close() 保证所有子线程已结束
```

逐项：

| 元素 | 含义 |
|---|---|
| `StructuredTaskScope<T>` | 作用域基类。**策略（policy）由子类决定**：什么时候算「整体完成」、失败怎么处理。 |
| `ShutdownOnFailure` | 内置策略 1：**任何子任务失败 → 取消其余子任务**。用于「全部成功才有意义」（如下单前检查）。 |
| `ShutdownOnSuccess<T>` | 内置策略 2：**第一个成功 → 取消其余**。用于「谁先回用谁」（对冲请求、多个数据源择一）。 |
| `fork(Callable<? extends U>)` | 在作用域里启动一个子任务，返回 `Subtask<U>`。**不是 `Future`**。 |
| `join()` | 阻塞，等所有子任务完成（或被 shutdown）。可被中断。必须在 `get` 前调用。 |
| `joinUntil(Instant deadline)` | 带截止时间的 `join`，超时抛 `TimeoutException` 并 shutdown。 |
| `shutdown()` | 主动取消：中断所有还没结束的子线程。策略内部在需要时自动调用。 |
| `close()` | 由 `try-with-resources` 调用：`shutdown`（如果还没）并**等待所有子线程结束**。 |
| `Subtask.get()` / `.exception()` / `.state()` | 取结果 / 取异常 / 状态（`UNAVAILABLE`、`SUCCESS`、`FAILED`）。 |

构造器：`new StructuredTaskScope.ShutdownOnFailure()`（虚拟线程）或 `(String name, ThreadFactory factory)`（起名并指定线程工厂；`name` 出现在线程 dump 里）。

### 2.2 规则（违反会抛异常）

* **只有创建作用域的线程（owner）才能 `fork`/`join`/`close`**，否则 `WrongThreadException`。
* 在 `join()` 之前调用 `subtask.get()` → `IllegalStateException`。
* **不 `join` 就退出块**，或作用域嵌套时**不按顺序关闭** → `StructureViolationException`。
* `ShutdownOnFailure.throwIfFailed()`：第一个失败子任务的异常包成 `ExecutionException` 抛出；`throwIfFailed(Function)` 可映射成自己的异常类型。
* `ShutdownOnSuccess.result()`：返回第一个成功的结果；全部失败则抛 `ExecutionException`。

### 2.3 自定义策略

继承 `StructuredTaskScope<T>`，重写 `handleComplete(Subtask)`：每个子任务结束时调用一次，你在里面决定收集结果、记录失败、是否 `shutdown()`。见例 4。

---

## 3. 编译器和 JVM 到底做了什么

编译器只做一件事：看到预览 API，要求 `--enable-preview`，并在 class 文件打上「依赖预览」标记——**用预览编出的类必须带 `--enable-preview` 运行，且只能在同一大版本的 JVM 上运行**。

运行时：

1. **线程容器**（thread container）：每个 scope 内部有个容器，记录它 fork 出的所有线程；`close()` 就是等容器里的线程全终止。
2. **父子关系可见**：线程 dump（`jcmd <pid> Thread.dump_to_file -format=json`）能显示线程属于哪个作用域（名字即构造器第一个参数），解决 1.2 的痛点 4。
3. **取消 = 中断**：`shutdown()` 对每个存活子线程 `interrupt()`。取消是**协作式**的——子任务要在阻塞调用（`sleep`、`BlockingQueue.take`、socket 读）上响应中断，或自己轮询 `Thread.interrupted()`；纯 CPU 循环取消不掉。
4. **作用域值继承**：子线程自动继承父线程当前的 `ScopedValue` 绑定（J12），设计时就是一对。
5. **嵌套结构被检查**：JVM 记录线程上「当前打开的作用域栈」，关闭顺序不对就抛 `StructureViolationException`——「结构化」在这里被强制执行。

---

## 4. 三个例子（由浅入深）+ 一个自定义策略

### 例 1：最简单——两个都成功才算成功（`J11Ex1.java`）

见 2.1 骨架。输出：

```
quote = AAPL 189.50, limit = 10000
```

对比 `J11Old`：没有线程池要关、没有 `Future` 要按序 get；两个子任务的生命周期被 `try` 块框住。

### 例 2：进阶——谁先回用谁（`J11Ex2.java`）

向三个交易所查同一个东西，延迟分别 300 / 80 / 500 ms，用 `ShutdownOnSuccess`：

```java
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> query("NYSE", 300));
    scope.fork(() -> query("NASDAQ", 80));
    scope.fork(() -> query("ARCA", 500));
    String first = scope.join().result();
}
```

输出：

```
拿到: NASDAQ 先回
  [ARCA 被取消(InterruptedException)]
  [NYSE 被取消(InterruptedException)]
离开 try 块时，三个子线程一定都已结束
```

重点是最后一行：第一个结果一到，另两个就被中断；`try` 块结束（`close()` 等待之后）三个线程**确定**都结束了，无需自己 `awaitTermination`。

### 例 3：贴近真实——下单前并行检查 + 整体截止时间（`J11Ex3.java`）

下单前并行取三样：行情（`quote`）、风控额度（`risk`）、合约参考数据（`refdata`）。要求任一失败则整个检查失败并取消其他，整体最多等一个 deadline。

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure("pretrade", Thread.ofVirtual().factory())) {
    Subtask<Quote>      q = scope.fork(() -> slow("quote",   quoteMs, new Quote(18950, 18951), false));
    Subtask<Limit>      l = scope.fork(() -> slow("risk ",   100,     new Limit(500), riskFails));
    Subtask<Instrument> i = scope.fork(() -> slow("refdata", 50,      new Instrument("AAPL", 1), false));
    scope.joinUntil(Instant.now().plus(deadline)).throwIfFailed();
    return new PreTrade(q.get(), l.get(), i.get());
}
```

三个场景的输出：

```
场景 1：全部成功
    - risk  完成
    - quote 完成
    - refdata 完成
  结果: PreTrade[q=Quote[bid=18950, ask=18951], l=Limit[maxQty=500], i=Instrument[symbol=AAPL, tickSize=1]]
场景 2：风控失败(100ms)，行情要 1500ms -> 行情应被取消
    - refdata 完成
    - quote 被取消
  失败: java.lang.IllegalStateException: risk  unavailable
场景 3：行情太慢(3000ms)，deadline 400ms -> 超时并取消
    - refdata 完成
    - risk  完成
    - quote 被取消
  超时: TimeoutException
```

读法：

* 场景 2：风控 100ms 失败 → scope shutdown → 还在 sleep 的行情收到中断 → `main` 立刻拿到 `ExecutionException`，**不用等 1500ms**（`J11Old` 等了 1.5s）。
* 场景 3：`joinUntil` 超时抛 `TimeoutException`，抛出前 scope 已 shutdown，慢的行情被取消。
* 场景 1 的完成顺序由线程调度和 sleep 精度决定，并不固定——**别依赖子任务完成顺序**。

### 例 4：自定义策略——收集全部成功（`J11Ex4Custom.java`）

内置两个策略都是「一个失败/成功就收工」。「尽力从 5 个交易所取价，失败的忽略」要自己写：

```java
static class CollectOk<T> extends StructuredTaskScope<T> {
    private final Queue<T> ok = new ConcurrentLinkedQueue<>();
    private final Queue<Throwable> failed = new ConcurrentLinkedQueue<>();
    @Override protected void handleComplete(Subtask<? extends T> st) {
        switch (st.state()) {
            case SUCCESS -> ok.add(st.get());
            case FAILED  -> failed.add(st.exception());
            case UNAVAILABLE -> throw new IllegalStateException();
        }
    }
    ...
}
```

输出：

```
成功 4 个: [18950, 18951, 18952, 18954]，失败 1 个
```

`handleComplete` 在**子线程**里被调用，收集结果的容器必须线程安全（这里用 `ConcurrentLinkedQueue`）——这是自定义策略比内置难的地方。

---

## 5. 坑与限制

### 5.1 预览 API：后续版本会不兼容地改

* **JDK 21**：`new StructuredTaskScope.ShutdownOnFailure()` / `ShutdownOnSuccess<T>`，`fork` 返回 `Subtask`。本课写法。
* **JDK 25**：作用域改用**静态工厂方法**打开，不再用公有构造器；完成策略由 **`Joiner`** 对象表达。默认 `StructuredTaskScope.open()` 的语义是「全部成功才成功，任一失败则整体失败」；其他策略传 `open(Joiner)`，内置 joiner 有 `anySuccessfulResultOrThrow()`、`allSuccessfulOrThrow()`、`awaitAll()`、`awaitAllSuccessfulOrThrow()`、`allUntil(...)`，也可自己实现 `Joiner`。JDK 21 的 `ShutdownOnFailure` / `ShutdownOnSuccess` 由 `open()` / `Joiner` 取代。
* **JDK 26**：小改——`Joiner.onTimeout()`、`allSuccessfulOrThrow()` 改为返回结果列表、`anySuccessfulResultOrThrow()` 改名 `anySuccessfulOrThrow()`；仍是预览。
* 生产代码用不用，取决于能否接受每次升级 JDK 都改代码；面试重点讲**概念**（子任务生命周期被词法作用域框住、失败/取消统一处理、取消靠中断），不要背 API 细节。

**速查对照（概念映射，非逐字翻译）：**

| 想做的事 | JDK 21（本课） | JDK 25+ |
|---|---|---|
| 全部成功才算成功 | `new ShutdownOnFailure()` + `join().throwIfFailed()` | `StructuredTaskScope.open()` + `join()` |
| 第一个成功就收工 | `new ShutdownOnSuccess<T>()` + `join().result()` | `open(Joiner.anySuccessfulResultOrThrow())`（26 改名 `anySuccessfulOrThrow`） |
| 自定义 | 继承并重写 `handleComplete` | 实现 `Joiner` |

### 5.2 取消依赖中断：不响应中断的子任务取消不掉

`shutdown()` 只是 `interrupt()`。`while (true) { compute(); }` 的子任务永不停；调用不响应中断的库（老式阻塞 I/O）也停不下来。`close()` 会等所有子线程结束，所以这种子任务让 `close()` **一直卡住**。设计子任务要保证可中断。

### 5.3 忘记 `join()`

fork 后直接 `get()` → `IllegalStateException`；fork 后不 `join` 直接退出块 → `StructureViolationException`。

### 5.4 不要把 `scope` 传给别的线程用

只有 owner 线程能 `fork`；子任务里想再并行，就在子任务里**开自己的新作用域**（嵌套），别用外面那个。

### 5.5 `handleComplete` 里的线程安全

自定义策略的 `handleComplete` 在子线程里并发执行；内置策略用 `AtomicReference` 之类保证安全，自己写时同样要保证。

### 5.6 它不是「并行流」的替代品

并行流是**数据并行**（集合分块算，CPU 密集，用公共 `ForkJoinPool`）；结构化并发是**任务并行**（几个不同的、通常阻塞的调用），一般搭虚拟线程。

### 5.7 把它和虚拟线程配套理解

`fork` 默认就是虚拟线程，「每个子任务一个线程」不贵；换成平台线程工厂就回到 J10 的线程成本问题。

---

## 6. 真实代码里的结构化并发

**`ConcurrentMerge.mergeAll`**：一次性合并 k 路数据流，任一路出错整体失败。

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure("merge-all", Thread.ofVirtual().factory())) {
    for (int i = 0; i < srcs.size(); i++) {
        final int idx = i;
        scope.fork(() -> {
            try { produce(idx, srcs.get(idx), queues.get(idx)); }
            catch (InterruptedException e) { throw e; }                     // 被取消：原样往外抛
            catch (Exception e) { throw new MergeException(idx, e); }       // 真正的失败：带上流编号
            return null;
        });
    }
    var merged = scope.fork(() -> { ... combiner.poll(true) ... return out; });
    scope.join();
    scope.throwIfFailed(e -> e instanceof MergeException me ? me : new MergeException(-1, e));
    return merged.get();
}
```

对照本课：`ShutdownOnFailure`；有名字的 scope + 虚拟线程工厂；`catch (InterruptedException e) { throw e; }` 把「被取消」和「真正失败」分开（取消靠中断，子任务要让中断异常往外传而不是吞掉，5.2）；`throwIfFailed(Function)` 把异常映射成自己的 `MergeException`。动机一句话：离开 try 块时所有子线程一定已结束，不会泄漏。

**`RecursiveSum.sumVirtual`**：每块数组一个子任务，`scope.join().throwIfFailed()` 之后逐个 `p.get()` 合并。这是 `ShutdownOnFailure` 的最简用法，也是「CPU 密集不该用虚拟线程」的反例。

> 这两处和本课一样只能在 JDK 21–24 预览 API 下编译（`--release 21 --enable-preview`）。

---

## 7. 自测题

1. 结构化并发要保证的核心性质是什么？用 Java 8 的 `ExecutorService` 为什么做不到？
2. `ShutdownOnFailure` 与 `ShutdownOnSuccess` 各适合什么场景？各举一个交易系统里的例子。
3. 下面代码有什么错？
   ```java
   try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
       var a = scope.fork(() -> compute());
       System.out.println(a.get());
       scope.join();
   }
   ```
4. 子任务是 `while (true) { x = heavy(x); }`（纯计算，不检查中断）。别的子任务失败后，会发生什么？
5. 这段 JDK 21 代码在 JDK 25 里要怎么改，为什么？（只说思路）

<details><summary>答案</summary>

1. 子任务的生命周期被词法作用域包住：块结束时全部已结束或已取消，失败和取消统一传播。`ExecutorService` 的任务只由池管理，与发起它的代码块无关，没有「块结束必须结束」的约束，取消/异常也不自动传播。
2. `ShutdownOnFailure`：全部必须成功，如下单前 行情 + 风控 + 参考数据 检查。`ShutdownOnSuccess`：谁先回用谁，如同一价格向多个交易所发对冲请求。
3. `join()` 之前调用 `get()`，抛 `IllegalStateException`；应先 `scope.join()` 再 `a.get()`。
4. 不会被取消：`shutdown()` 只是 `interrupt()`，纯计算不响应；`close()` 会等它结束，`try` 块就卡在 `close()` 直到它算完（这里是永远）。循环里要检查 `Thread.currentThread().isInterrupted()`。
5. JDK 25 起不能 `new` 作用域，要 `StructuredTaskScope.open(...)`：`ShutdownOnFailure` 的语义由默认 `open()` 提供，`ShutdownOnSuccess` 由 `open(Joiner.anySuccessfulResultOrThrow())` 提供，自定义策略改成实现 `Joiner`。因为预览 API 允许不兼容改动。

</details>

---

「延伸」J12 作用域值：结构化并发里子线程自动继承的那一对。
