# J12 · `ScopedValue`：不可变、有生命周期的「隐式参数」，替代 `ThreadLocal`

> **Java 21 预览（Preview）API。** 编译 `javac --release 21 --enable-preview`，运行 `java --enable-preview`。
> 历史：JDK 20 孵化 → **21 预览** → 22–24 继续预览 → **JDK 25 转正**，是预览特性里最早毕业的。JDK 21 写法与 25 最终版有出入，见 5.1。
> 可运行代码：`examples/J12/`。前置：线程、`ThreadLocal` 的大概用法（第 1 节从零讲）；建议先读 J10、J11。

---

## 1. 先看痛点：`ThreadLocal` 能用，但有三个结构性毛病

### 1.1 从零讲：为什么需要「隐式参数」

一个下单请求要经过十几层方法：`controller → service → risk → pricing → audit → logger`。最底层的 `logger` 想打出**当前请求的 traceId 和账户号**。办法一：每个方法加个 `RequestContext ctx` 参数一路传——十几个签名全被污染，第三方回调接口更改不了。办法二：放进「线程私有的全局变量」，谁需要谁取——这就是 `ThreadLocal`：

```java
static final ThreadLocal<String> USER = new ThreadLocal<>();
USER.set("alice");     // 存到「当前线程」自己的小表里
USER.get();            // 从「当前线程」的小表里取；别的线程取不到这个值
```

内部：每个 `Thread` 里有张 `ThreadLocalMap`，`ThreadLocal` 对象只是 key，所以「每线程一份」。

### 1.2 三个毛病（`examples/J12/J12Old.java`）

```java
static final ThreadLocal<String> USER = new ThreadLocal<>();
static void handle(String user, boolean cleanup) {
    USER.set(user);
    try { ... } finally { if (cleanup) USER.remove(); }
}
```

输出：

```
pool-1-thread-1 处理 alice，USER=alice
下一个请求(未 set)读到 USER=alice          <- 毛病 1
子线程读到 USER=null                        <- 毛病 2
主线程现在 USER=mallory                     <- 毛病 3
```

1. **生命周期不受控 → 泄漏、串号**：`set` 后值活到线程死或手动 `remove()`。线程池复用线程，请求 A 忘了 `remove` 的值请求 B 在同一线程上读到——**在交易系统里就是「用了别人的账户」**。
2. **不跨线程**：新线程读到 `null`。用 `InheritableThreadLocal` 则建线程时把整张表**复制**给孩子，线程多时复制成本和内存很大；线程池里的线程也不是你的任务创建的，继承不到。
3. **可变，随处可改**：拿到 `ThreadLocal` 引用的代码都能 `set`，读代码的人答不出「这个值是谁在什么时候改的」。

虚拟线程（J10）放大了毛病 1、2：线程数从几百变几百万，每个线程一张 `ThreadLocalMap`，`InheritableThreadLocal` 每次 fork 复制一遍。

---

## 2. 语法逐条讲

> 以下是 **JDK 21 预览 API**。

### 2.1 声明、绑定、读取

```java
static final ScopedValue<String> USER = ScopedValue.newInstance();      // 钥匙；static final

ScopedValue.where(USER, "alice").run(() -> {     // 只在这个 lambda 执行期间，USER 绑定为 "alice"
    System.out.println(USER.get());              // alice
    deep();                                      // deep() 里同样能 USER.get()，不需要参数
});                                              // lambda 一结束，绑定自动消失
```

逐项：

| 元素 | 含义 |
|---|---|
| `ScopedValue<T>` | 钥匙，不装值。值只存在于「绑定」里。通常 `static final`。 |
| `ScopedValue.where(key, value)` | 返回一个 `Carrier`（"携带者"），表示「准备好绑定 key=value」，还没生效。 |
| `Carrier.where(key2, value2)` | 链式再绑一个：`where(A, a).where(B, b).run(...)`。 |
| `Carrier.run(Runnable)` | 绑定生效，执行 lambda，结束自动解绑。无返回值。 |
| `Carrier.call(Callable<R>)` | 同上，有返回值，可抛受检异常。 |
| `Carrier.get(Supplier<R>)` | JDK 21 里还有的变体，有返回值，不抛受检异常。 |
| `ScopedValue.runWhere / callWhere / getWhere(key, v, ...)` | JDK 21 的静态快捷方式（单个绑定），等价于 `where(key, v).run/call/get(...)`。**JDK 24 起 `callWhere`/`runWhere` 被移除**，见 5.1。 |
| `key.get()` | 取当前绑定的值；**未绑定则抛 `NoSuchElementException`**。 |
| `key.isBound()` | 当前线程现在有没有绑定。 |
| `key.orElse(default)` / `orElseThrow(Supplier)` | 未绑定时给默认值 / 抛自定义异常。 |

### 2.2 它没有的东西：`set`

**ScopedValue 不可变，没有 `set`。** 想「改值」只能用新值开一个内层 `where(...).run(...)`，内层看到新值，出来自动还原（例 2）。这直接消灭毛病 3：某范围内值是什么，从缩进结构就看得出。

### 2.3 嵌套是遮蔽，不是覆盖

```java
where(USER, "alice").run(() -> {
    where(USER, "admin").run(() -> { /* 这里 USER = admin */ });
    /* 回到这里 USER = alice */
});
```

### 2.4 跨线程：只有结构化并发会继承

* 在 `StructuredTaskScope`（J11）里 `fork` 的子线程，**自动继承**父线程 fork 时刻的所有 ScopedValue 绑定（例 3）。
* 普通 `new Thread`、`Thread.ofVirtual().start`、`ExecutorService.submit` 的任务**不继承**（例 3 的「野线程」读不到）。因为只有结构化并发能保证「子线程一定在父绑定范围结束前结束」，否则子线程可能在父已解绑后还在读。

---

## 3. 编译器和 JVM 到底做了什么

编译器：识别预览 API，要求 `--enable-preview`，无新语法。

运行时（设计概括，具体数据结构是 JDK 内部实现细节，可能变化）：

1. **绑定是不可变的链式结构**：线程里保存的是指向「当前绑定快照」的引用，不是可变表。`where(...).run(...)` 进入 lambda 前把新绑定接在旧快照后形成新快照，退出时恢复旧引用。快照不可变，所以**继承给子线程只是复制一个引用**，不复制数据——比 `InheritableThreadLocal` 便宜的根本原因。
2. **生命周期绑定在调用栈上**：绑定 = 一次 `run`/`call` 的执行期，清理就是方法返回，不存在「忘了清理」。
3. **读取很快**：`get()` 有专门的缓存和位图优化，成本与 `ThreadLocal` 相当甚至更低。
4. **子线程继承靠 `StructuredTaskScope`**：`fork` 时把当前绑定快照交给新线程。「scope 关闭前子线程必结束」与「绑定在父代码块内有效」是同一件事的两面。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——声明、绑定、读取（`J12Ex1.java`）

输出：

```
绑定前 isBound=false, orElse=<anonymous>
绑定前 get() -> NoSuchElementException
块内 isBound=true
  deep() 读到 USER=alice
块外 isBound=false
```

没有 `try/finally`，块外自动回到未绑定（对比 `J12Old` 的毛病 1）。

### 例 2：进阶——嵌套、多绑定、有返回值（`J12Ex2.java`）

```java
ScopedValue.where(USER, "alice").where(DEPTH, 1).run(() -> {
    System.out.println("外层: " + describe());
    ScopedValue.where(USER, "admin-on-behalf-of-alice").where(DEPTH, 2).run(() ->
            System.out.println("内层: " + describe()));
    System.out.println("还原: " + describe());
});
String r  = ScopedValue.where(USER, "carol").call(() -> USER.get().toUpperCase());
String r2 = ScopedValue.getWhere(USER, "dave", () -> USER.get() + "!");
```

输出：

```
外层: alice@depth1
内层: admin-on-behalf-of-alice@depth2
还原: alice@depth1
call -> CAROL, getWhere -> dave!
```

重点是「还原」那行：`ThreadLocal` 要自己写 `old = USER.get(); try { USER.set(x); ... } finally { USER.set(old); }`。

### 例 3：贴近真实——请求上下文传给结构化并发的子任务（`J12Ex3.java`）

```java
record RequestContext(String traceId, String account) {}
static final ScopedValue<RequestContext> CTX = ScopedValue.newInstance();

static void log(String msg) {                // 深层方法：不接受上下文参数，却知道自己在服务哪个请求
    var c = CTX.isBound() ? CTX.get() : null;
    ...
}

static void handleOrder() throws Exception {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Subtask<Long> q = scope.fork(J12Ex3::fetchQuote);   // 子线程自动继承 CTX
        Subtask<Long> l = scope.fork(J12Ex3::fetchLimit);
        scope.join().throwIfFailed();
    }
}

ScopedValue.where(CTX, new RequestContext("t-001", "ACC-7")).call(() -> { handleOrder(); ...; return null; });
```

输出：

```
[t-001/ACC-7] 开始处理订单 
[t-001/ACC-7] 取额度
[t-001/ACC-7] 取行情
[t-001/ACC-7] 行情=18950 额度=500 
[<无上下文>] (野线程) 我能看到上下文吗？ 
[t-002/ACC-9] 开始处理订单 
...
```

* `取额度`/`取行情` 在两个 fork 的虚拟线程里打印，仍带 `t-001/ACC-7`——继承生效。
* `(野线程)` 用 `Thread.ofVirtual().start` 开，打出 `<无上下文>`——不继承。
* 第二个请求 `t-002/ACC-9` 与第一个不串号：绑定随 `call` 返回消失。

---

## 5. 坑与限制

### 5.1 预览 API：后续版本改了什么（面试要能说清）

| 版本 | 状态 / 变化 |
|---|---|
| JDK 20 | 孵化（incubator） |
| **JDK 21** | **第一次预览，本课写法。** 有 `runWhere` / `callWhere` / `getWhere` 静态方法，和 `Carrier.run/call/get(Supplier)` |
| JDK 22、23 | 继续预览，小改 |
| JDK 24 | 第四次预览：**`callWhere` 与 `runWhere` 被移除**，API 全"流式"——使用已绑定值的唯一方式是 `Carrier.call` 和 `Carrier.run` |
| **JDK 25** | **转正（final）**：`ScopedValue.orElse` 不再接受 `null` 参数 |

对本课代码的含义：`runWhere(...)`、`callWhere(...)` 在 24 起不能编译，要写成 `ScopedValue.where(KEY, v).run(...)` / `.call(...)`。例 1、例 3 的 `where(...).run/call` 在 JDK 25 仍是标准形式。`Carrier.get(Supplier)` 在后续版本的去向未核对，新代码别依赖它。

### 5.2 它不是 `ThreadLocal` 的完全替代

* 要"**每线程一份、可变、长生命周期**"的东西（每线程复用的缓冲区、非线程安全的 `SimpleDateFormat`），`ThreadLocal` 仍是对的工具。
* `ScopedValue` 解决"**调用链上的只读上下文**"：用户、traceId、事务。
* 更新上下文只能重绑定，"在深层改一个值让上层看到"做不到——那说明你要的是返回值，不是上下文。

### 5.3 普通线程不继承

线程池里 `executor.submit(task)` 的任务在池线程上运行，**看不到**提交者的绑定。用 `StructuredTaskScope`，或在任务里自己重新 `where(...)`。

### 5.4 未绑定的 `get()` 抛异常

用 `isBound()` / `orElse()` 保护，或确保所有入口都绑定过。

### 5.5 值本身要不可变

`ScopedValue` 保证"绑定"不可变，不保证"值对象"不可变。绑一个 `ArrayList` 进去，到处都能改它，等于把毛病 3 请回来。绑 `record` 或不可变对象。

### 5.6 别滥用成"隐藏的全局变量"

隐式参数让依赖看不见。只放真正横切的（身份、追踪、截止时间），业务数据仍用参数。

---

## 6. 真实代码里的 ScopedValue

参考实现里没有直接用 `ScopedValue`，它在这里是「配套理解」的一课。最近的关联点是 J11 的 `ConcurrentMerge.mergeAll`：

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure("merge-all", Thread.ofVirtual().factory())) {
    for (int i = 0; i < srcs.size(); i++) { ... scope.fork(() -> { ... produce(idx, srcs.get(idx), queues.get(idx)); ... }); }
```

若要给每次 `mergeAll` 附一个 traceId，让所有 `produce` 子任务和 `MergeException` 都能带上，最干净的是外面套 `ScopedValue.where(TRACE, id).call(() -> mergeAll(...))`——`fork` 出的所有生产者自动继承，不用改 `produce` 的签名（即例 3 的结构）。

面试问「服务怎么在线程间传 traceId」：老办法 `ThreadLocal`/`MDC`，要处理池线程泄漏和跨线程拷贝；JDK 21 起有预览的 `ScopedValue`，不可变、随块结束自动解绑，结构化并发子线程自动继承；JDK 25 转正。

---

## 7. 自测题

1. 列出 `ThreadLocal` 的三个结构性毛病，并说明 `ScopedValue` 各用什么设计消除它。
2. `ScopedValue.get()` 在未绑定时会怎样？有哪几种安全的读法？
3. 下面输出什么？
   ```java
   static final ScopedValue<Integer> X = ScopedValue.newInstance();
   ScopedValue.where(X, 1).run(() -> {
       ScopedValue.where(X, 2).run(() -> System.out.print(X.get()));
       System.out.print(X.get());
   });
   System.out.print(X.isBound());
   ```
4. 在 `ExecutorService.submit(() -> log("..."))` 里，任务能看到提交者的 `ScopedValue` 绑定吗？在 `StructuredTaskScope.fork` 里呢？为什么有区别？
5. `ScopedValue` 在哪个 JDK 版本转正？JDK 24 把哪些方法移除了？

<details><summary>答案</summary>

1. 生命周期失控/泄漏 → 绑定寿命等于 `run/call` 执行期，返回即消失；不跨线程或继承成本高 → 结构化并发 fork 时继承不可变快照的引用；可变且随处可改 → 没有 `set`，改值只能用内层 `where` 遮蔽。
2. 抛 `NoSuchElementException`。安全读法：`isBound()`、`orElse(默认值)`、`orElseThrow(自定义异常)`。
3. `21false`：内层打印 2，回外层打印 1，块外 `isBound()` 为 false。
4. 不能；`fork` 里可以。`fork` 的子线程一定在 scope 关闭前结束，继承父绑定安全；线程池线程的生命周期不受提交者控制，可能在父已解绑后才运行。
5. JDK 25 转正；JDK 24 移除了 `ScopedValue.callWhere` 和 `runWhere`。

</details>

---

「延伸」J13 未命名变量：`_` 占位符。
