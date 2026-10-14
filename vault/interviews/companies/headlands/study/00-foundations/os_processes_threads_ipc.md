# 基础课 · 操作系统基础：进程、线程、调度、系统调用、进程间通信（IPC）

> 写法说明见 `study/TEXTBOOK.md`。配套代码：[`examples/IpcDemo.java`](examples/IpcDemo.java)（系统调用开销、线程切换往返时间、内存映射文件、**一个跑在共享内存上的 SPSC 环形缓冲**，含跨两个 JVM 进程的版本）。
> 前置：[cpu_cache_locality](cpu_cache_locality.md)（缓存一致性、伪共享）。
> 被谁引用：`hc02`/`hc03`/`hc04` 讲义里的「线程、可见性、虚拟线程」小节只讲了到 Java 层，本章补上操作系统层；`hc04` 的环形缓冲在这里被升级成跨进程版本。
> JD 关联：Headlands 的 JD 写了 Linux。本章默认讲 Linux 语义；本机是 macOS，凡是实测数字与 Linux 可能不同的地方都会注明。
> **运行方式**：`java` 要加 `--enable-preview --enable-native-access=ALL-UNNAMED`（`java.lang.foreign` 在 JDK 21 是预览 API，见第 6.3 节）。

---

## 0. 这一章在讲什么

写 Java 的人平时看不到操作系统，但性能问题常常出在它那里：

* 为什么线程之间传一个消息要 2–3 微秒，有时又只要 90 纳秒？
* 一次读文件、发网络包到底发生了什么？为什么叫"系统调用"，为什么贵？
* 两个进程想高速通信，选管道、socket 还是共享内存？
* 交易系统里常说的"共享内存 + SPSC 环形缓冲"到底是什么，怎么写，为什么快？

本章顺序：进程与线程 → 虚拟内存 → 调度与上下文切换 → 系统调用 → IPC 全家桶 → 内存映射 → SPSC 环形缓冲（含完整代码与实测）。

---

## 1. 程序、进程、线程

### 1.1 是什么

* **程序**（program）：磁盘上的可执行文件。
* **进程**（process）：一个**正在运行的程序**，操作系统给它一整套资源：独立的**虚拟地址空间**、打开的文件描述符、环境变量、至少一个线程。
* **线程**（thread）：进程里的一条**执行流**。同一进程的线程**共享**地址空间（堆、全局变量、打开的文件），但各自有自己的**栈**和寄存器。

```text
进程 A                                   进程 B
┌─────────────────────────────┐        ┌─────────────────────────────┐
│ 虚拟地址空间 (私有)          │        │ 虚拟地址空间 (私有)          │
│  ┌─────────────────────┐    │        │                             │
│  │ 代码 (text)          │    │        │          …                  │
│  │ 全局数据             │    │        └─────────────────────────────┘
│  │ 堆 (heap)  ← 线程共享 │    │
│  ├─────────────────────┤    │        进程之间默认互相看不见对方的内存
│  │ 线程1 栈 │ 线程2 栈   │    │        要通信必须经过内核 → IPC (第 6 节)
│  └─────────────────────┘    │
│ 文件描述符表 (线程共享)       │
└─────────────────────────────┘
```

### 1.2 为什么需要两个层次

* **进程提供隔离**：一个进程崩溃（段错误、`OutOfMemoryError`）不会拖垮别的进程；内存互相看不见，更安全。代价：创建贵、通信贵、上下文切换贵。
* **线程提供轻量并发**：同一份数据直接共享，通信就是读写同一块内存；创建和切换更便宜。代价：没有隔离，一个线程的 bug 可以破坏整个进程；共享数据必须同步（锁、可见性、内存序）。

| | 进程 | 线程 |
|---|---|---|
| 地址空间 | 各自独立 | 同进程共享 |
| 创建开销 | 大（Linux 的 `fork` + 写时复制页表） | 小（`clone` 共享地址空间） |
| 通信方式 | IPC：管道、socket、共享内存…… | 直接读写共享内存（需同步） |
| 崩溃影响 | 只影响自己 | 整个进程陪葬 |
| 上下文切换 | 要切换页表（地址空间），TLB 失效 | 同进程内不用切页表，更便宜 |

### 1.3 Linux 里线程其实也是"任务"

Linux 内核里进程和线程都叫 **task**。线程是用 `clone(CLONE_VM | CLONE_FILES | …)` 创建的、**与创建者共享地址空间**的 task。`ps -eLf` 能看到每个线程；`top -H` 按线程显示。

### 1.4 Java 里的对应关系

* 一个 JVM = 一个进程。你在 `java -jar` 之后用 `ps` 看到的就是它。
* **平台线程**（`new Thread(...)`，或线程池里的线程）与内核线程 **1:1**（JEP 444 原文：平台线程 "typically maps 1:1 to a kernel thread"）。每个都有自己的内核栈和 Java 栈（默认约 1 MB，`-Xss` 调整），所以几千个就是极限。
* **虚拟线程**（JDK 21 正式）：由 JVM 自己调度、挂在少量平台线程（称为**载体 carrier**）上的轻量线程。遇到阻塞 I/O 时，虚拟线程让出载体，让别的虚拟线程跑。适合"大量、等待居多"的任务，**不**适合 CPU 密集（hc03 步骤 8）。详细对比见 [networking_basics](networking_basics.md) 第 9 节。

---

## 2. 虚拟内存（一页纸版本）

### 2.1 是什么

每个进程以为自己独占一大片连续的地址空间（64 位下巨大）。但这些**虚拟地址**并不直接对应物理内存；CPU 里的 **MMU**（内存管理单元）借助内核维护的**页表**（page table），把虚拟地址翻译成物理地址。翻译的单位是**页**（page）：x86-64 Linux 默认 4 KB，**本机 macOS（Apple 芯片）是 16 KB**（`sysctl hw.pagesize` = 16384）。

```text
进程的虚拟地址               页表                    物理内存
 0x1000 ─ 页 A  ───────▶  A → 物理帧 7   ───────▶  [帧 7]
 0x2000 ─ 页 B  ───────▶  B → 物理帧 2   ───────▶  [帧 2]
 0x3000 ─ 页 C  ───────▶  C → (不在内存，在磁盘/文件里)  → 访问时触发"缺页"
```

### 2.2 为什么需要它

1. **隔离**：每个进程的页表不同，进程 A 的地址 0x1000 和进程 B 的地址 0x1000 指向不同的物理页。
2. **按需分配**：`malloc` 一大块只是登记，真正用到某一页才分配物理页（**缺页中断 page fault**）。
3. **映射文件**：把文件的某个范围当成内存的一段（第 6 节 `mmap`）。
4. **共享**：两个进程的页表可以把不同的虚拟地址指向同一个物理页——这就是**共享内存**的原理。

### 2.3 代价：TLB 与缺页

* 每次访存都查页表太慢，所以 CPU 有 **TLB**（Translation Lookaside Buffer，页表缓存）。TLB 未命中要走页表（几十到上百周期）。进程切换（换页表）会使 TLB 失效（或者靠 ASID/PCID 标签避免全部清空）。
* **缺页**：访问还没映射的页，CPU 陷入内核，内核分配物理页（minor fault，微秒级）或从磁盘读（major fault，毫秒级）。第一次访问新分配/新映射内存时会触发——低延迟系统常常在启动时就把热内存"摸一遍"（pre-touch）。
* **大页（huge pages）**：页变大（Linux 2 MB / 1 GB），同样的 TLB 条目覆盖更多内存，TLB 未命中大幅减少。JVM 参数 `-XX:+UseTransparentHugePages` / `-XX:+UseLargePages` 与此相关，交易系统里常见。

---

## 3. 调度（scheduling）与上下文切换（context switch）

### 3.1 是什么

机器只有 N 个核，但有成百上千个可运行的线程。**调度器**（scheduler）决定"现在哪个核运行哪个线程、运行多久"。

线程的状态：

```text
          ┌───────────── 被调度器选中 ──────────────┐
          │                                        ▼
     ┌─────────┐   时间片用完 / 被更高优先级抢占   ┌─────────┐
     │ 就绪     │ ◀──────────────────────────────── │ 运行中   │
     │ runnable │                                   │ running │
     └─────────┘                                    └─────────┘
          ▲                                           │    │
          │ I/O 完成、锁被释放、被 unpark、sleep 到期    │    │ 等待 I/O、等锁、
          │                                           │    │ park、sleep
          │             ┌─────────┐                   │    │
          └──────────── │ 阻塞     │ ◀─────────────────┘    │
                        │ blocked │ ◀──────────────────────┘
                        └─────────┘
```

Java 的 `Thread.State`（`RUNNABLE`、`BLOCKED`、`WAITING`、`TIMED_WAITING`）与它大致对应：`RUNNABLE` 包括"在运行"和"就绪"两者（以及在内核里阻塞读 socket 的线程）。

### 3.2 调度的几个关键概念

* **时间片**（time slice / quantum）：一个线程连续运行的最长时间，量级是毫秒。
* **抢占**（preemption）：时钟中断到来时，内核可以把正在跑的线程踢下去换别人。**非自愿切换**。
* **自愿切换**：线程自己阻塞（等 I/O、锁、`park`）。
* **优先级与公平**：Linux 的主流调度器是 **CFS**（Completely Fair Scheduler，2.6.23 起，用红黑树按"已用 CPU 时间"排队，见 [ordered_maps_trees](ordered_maps_trees.md)）；6.6 版内核起换成 **EEVDF**。实时任务有 `SCHED_FIFO` / `SCHED_RR`。
* **CPU 亲和性（affinity）/ 绑核**：限制线程只在指定的核上跑（`taskset -c 3 java ...`，或 `sched_setaffinity`）。低延迟系统会：(1) 隔离出专用核（内核参数 `isolcpus`、`nohz_full`），(2) 把热线程绑上去，(3) 线程在核上**忙等（busy-spin）**，不阻塞、不让出。这样没有调度延迟、缓存始终是热的。Java 标准库没有绑核 API，常用 OpenHFT 的 Java-Thread-Affinity 库（走 JNA 调 `sched_setaffinity`）。

### 3.3 上下文切换：切换一次要做什么，为什么贵

**上下文切换**：把当前线程的寄存器、程序计数器、栈指针等"现场"保存起来，载入另一个线程的现场。

* **直接成本**：进内核、保存/恢复寄存器、调度器选下一个线程、（如果换进程）切换页表。量级约 **1–几微秒**。
* **间接成本（常常更大）**：新线程的数据不在 CPU 缓存里，之前热的缓存/TLB/分支预测器被"污染"了，要重新预热。（Li, Ding, Shen, *Quantifying the Cost of Context Switch*, ExpCS 2007 专门量化了这部分。）
* 如果线程是从别的核醒来，还可能迁移核心，缓存全是冷的。

### 3.4 本机实测：阻塞交接 vs 忙等交接

`IpcDemo` 第 2 部分：两个线程来回"乒乓"传一个标志位。

* **park/unpark 版**：对方没轮到时调用 `LockSupport.park()` 睡眠，轮到时由对方 `unpark` 唤醒。睡眠 = 让出 CPU，唤醒 = 内核把线程重新放回就绪队列并调度。
* **忙等版**：双方都在循环里读标志位（`Thread.onSpinWait()` 提示 CPU 这是自旋），从不睡眠。

真实输出（20 万个往返）：

```text
park/unpark round trip:     3099 ns
busy-spin round trip  :       85 ns
```

* 一个往返包含两次交接，所以 park/unpark 每次交接约 **1.5 µs**；忙等每次交接约 **40 ns**——差 **36 倍**。（另一次运行是 2529 ns / 90 ns，量级一致。）
* 忙等快，是因为这两个线程一直占着核，缓存是热的，交接只是一个缓存行在两个核之间传一下（约几十 ns，见 cpu_cache 第 7 节）。
* 代价：忙等**烧满一个核**。所以只有在你能奢侈地为每个热线程分配专属核的系统（交易系统）才用；通用服务不这么干。

这就是为什么 HFT 系统常常"一个线程一个核，线程里是 `while (true) { poll(); }`"。

---

## 4. 系统调用（system call）

### 4.1 是什么

用户程序不能直接操作硬件或别的进程的内存。CPU 有两种特权级：**用户态**（user mode，受限）和**内核态**（kernel mode，什么都能干）。程序想读文件、发网络包、分配大块内存、创建线程，必须请求内核代劳，这个请求就是**系统调用**。

```text
用户态                            内核态
┌──────────────────┐
│ 你的 Java 代码     │
│   FileChannel.read│
│   ↓ JNI/JVM 内部   │
│ libc: read(fd,…)  │
│   ↓               │
│ 执行 syscall 指令  │ ─────▶  ┌────────────────────────┐
│ (x86-64: syscall   │          │ 保存用户寄存器、切到内核栈  │
│  ARM64: svc)       │          │ 查系统调用表 → sys_read    │
│                    │          │ 检查参数、权限，真正干活    │
│ 拿到返回值，继续   │ ◀─────  │ 恢复用户寄存器，返回用户态  │
└──────────────────┘          └────────────────────────┘
```

### 4.2 为什么贵

1. **模式切换**：陷入内核再返回，几十到上百个周期。
2. **安全缓解措施**：2018 年的 Meltdown/Spectre 之后，Linux 默认在进出内核时切换页表（KPTI）、清除分支预测状态，把一次系统调用的代价抬高了。（Brendan Gregg 在博客里实测过 KPTI 的影响。）
3. **缓存污染**：内核代码和数据会挤掉用户程序的缓存。
4. **本身要做的事**：读文件要查页缓存、可能阻塞；网络发送要走协议栈。

### 4.3 本机实测

`IpcDemo` 第 1 部分：用 Java 21 的 FFM API（`java.lang.foreign`，第 6.3 节）直接调 libc 的 `write(fd, buf, 1)`，往 `/dev/null` 写 1 字节——这是**最轻的一类**系统调用（内核几乎不做事）。对照组：调一个**不进内核**的 libc 函数 `abs`，用来扣除 FFM 自身的调用开销。

```text
write(fd,buf,1): 622 ns per call   |   abs() (no kernel entry, same FFM overhead): 4.1 ns
```

* 一次最轻的系统调用约 **600 ns**（本机 macOS）；同样的 FFM 调用不进内核只要 4 ns。进内核本身的成本约是普通函数调用的 **150 倍**。
* macOS 的系统调用比 Linux 慢；Linux 上最轻的系统调用通常在 100–几百 ns 量级，受 KPTI 等缓解措施影响很大。**面试里说"几百纳秒到一微秒"最稳妥。**
* 不进内核的捷径：Linux 的 **vDSO** 把 `clock_gettime`、`gettimeofday` 映射成用户态可直接调用的代码，所以 `System.nanoTime()` 在 Linux 上约 20 ns，不是真的陷入内核。

### 4.4 对设计的影响

* **减少系统调用次数**：批量读写（一次 `read` 64 KB 而不是 64 次 1 KB）；`BufferedOutputStream`；用 `writev`/`readv` 聚集；NIO 的 `Selector` 一次问许多连接。
* **绕过内核**：共享内存（第 7 节）读写不需要系统调用；内核旁路网络（见 [networking_basics](networking_basics.md) 第 7 节）。
* **观察工具**：`strace -c -f -p <pid>`（统计系统调用次数和时间）、`perf trace`、`strace -T`（每次调用耗时）；macOS 用 `dtruss`。Gregg 的《Systems Performance》第 5 章（Applications）与第 4 章（Observability Tools）有完整用法。

---

## 5. 进程间通信（IPC）总览

### 5.1 问题

两个进程各有私有地址空间。进程 A 想把一批数据交给进程 B（比如行情解码进程把消息交给策略进程），怎么做？每一种方式都在**延迟、吞吐、复杂度、跨机能力**之间取舍。

### 5.2 方案一览

| 方式 | 数据怎么走 | 每条消息的系统调用 | 拷贝次数 | 跨机器 | 一句话 |
|---|---|---|---|---|---|
| **管道 pipe / FIFO** | 写进程 → 内核缓冲 → 读进程 | 写 1 次 + 读 1 次 | 2 | 否 | 最简单，字节流，Shell 里的 `\|` |
| **Unix 域套接字** | 同上，走 socket API | 写 1 + 读 1 | 2 | 否 | 同机 socket，可传文件描述符，比 TCP 回环省协议栈 |
| **TCP/UDP 回环 / 网络** | 走完整网络协议栈 | 写 1 + 读 1 | 2+ | **是** | 通用，最慢，但同一套代码能跨机器 |
| **消息队列**（POSIX `mq_*` / System V） | 内核里的有界消息队列 | 1 + 1 | 2 | 否 | 保留消息边界、可按优先级；用得较少 |
| **共享内存**（`mmap` / `shm_open`） | 两个进程的页表指向同一块物理页 | **0（建立之后）** | **0** | 否 | 最快；同步要自己做 |
| **信号 signal** | 内核向进程发一个小信号 | | | 否 | 只能传"事件"，不能传数据 |
| **文件 + 轮询** | 写文件、读文件（经页缓存） | 多 | 2 | 否（除网络文件系统） | 笨，但简单、可持久化 |

### 5.3 图解：管道要拷贝两次，共享内存零拷贝

```text
管道 / socket：

  进程 A 的缓冲区 ──write()──▶ [内核缓冲区] ──read()──▶ 进程 B 的缓冲区
                    拷贝 1        (两次 syscall)  拷贝 2

共享内存：

  进程 A 的页表 ─┐
                 ├──▶ [同一块物理内存页] ◀──┤
  进程 B 的页表 ─┘                           A 写，B 读：不经过内核，没有系统调用，没有拷贝
```

### 5.4 Java 里怎么用

* **子进程的标准输入输出（管道）**：

  ```java
  import java.io.*;

  public class PipeToSort {
      public static void main(String[] args) throws Exception {
          Process p = new ProcessBuilder("sort").start();            // 启动子进程，三个管道：stdin/stdout/stderr
          try (Writer w = new OutputStreamWriter(p.getOutputStream())) {
              w.write("pear\napple\nfig\n");                          // 写进子进程的 stdin（内核管道）
          }
          try (BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
              r.lines().forEach(System.out::println);                 // apple fig pear
          }
          p.waitFor();
      }
  }
  ```

  注意 `java.nio.channels.Pipe` **只能在同一个 JVM 内**使用，不是进程间的管道。
* **Unix 域套接字**（Java 16+，JEP 380）：

  ```java
  import java.net.*;
  import java.nio.channels.*;
  import java.nio.file.*;

  public class UdsServer {
      public static void main(String[] args) throws Exception {
          Path sock = Path.of("/tmp/demo.sock");
          Files.deleteIfExists(sock);
          try (ServerSocketChannel server = ServerSocketChannel.open(StandardProtocolFamily.UNIX)) {
              server.bind(UnixDomainSocketAddress.of(sock));         // 绑定到文件系统路径
              System.out.println("listening on " + sock);
          }
          Files.deleteIfExists(sock);
      }
  }
  ```

  客户端用 `SocketChannel.open(UnixDomainSocketAddress.of(sock))` 连接。API 与 TCP 的 `SocketChannel` 完全相同。
* **TCP/UDP**：见 [networking_basics](networking_basics.md)。
* **共享内存**：Java 没有直接的 `shm_open`，做法是**映射同一个文件**。Linux 上把文件放在 `/dev/shm`（内存文件系统 tmpfs）里，映射它就是纯内存共享，没有磁盘写回。见第 6 节。
* **消息队列**：Java 里很少用 OS 级别的；业界做法是库：Aeron（UDP/IPC）、Chronicle Queue（映射文件）、Agrona（共享内存数据结构）。

### 5.5 怎么选

* 通用、需要跨机器、延迟要求宽松 → TCP（或 gRPC 之类）。
* 同机、简单、吞吐不极端 → Unix 域套接字或管道。
* 同机、延迟 / 吞吐极端敏感（交易系统的行情→策略→网关的进程间通道）→ **共享内存 + 无锁环形缓冲**。
* 要把消息持久化（崩溃后能重放） → 内存映射文件（Chronicle Queue、Aeron Archive 的思路）。

---

## 6. 内存映射文件（memory-mapped file，`mmap`）

### 6.1 是什么

`mmap` 让内核把**一个文件的某个范围**映射到进程的虚拟地址空间。之后读写这段内存，等价于读写文件，但不需要 `read`/`write` 系统调用。

```text
磁盘上的文件
   │  (内核页缓存 page cache：文件内容缓存在内存里)
   ▼
┌─────────────┐        进程 A 的虚拟地址 0x7f00_0000 ──┐
│ 页缓存的物理页 │ ◀──────────────────────────────────────┤  页表指向同一些物理页
└─────────────┘        进程 B 的虚拟地址 0x7e10_0000 ──┘
```

要点：

* 内核的页缓存本来就在内存里。`mmap` 只是让你的页表**直接指向**那些页，省掉了 `read()` 的"从页缓存拷贝到用户缓冲区"。
* **按需加载**：映射时不读数据；第一次访问某页时触发缺页，内核才把它读进来。
* **共享映射**（`MAP_SHARED`）：多个进程映射同一个文件，看到同一份内存——这是共享内存的实现方式。你写的字节，对方立刻读得到（无需系统调用），内核在后台异步把脏页写回磁盘。
* **持久性**：进程崩溃，数据还在（已经在内核页缓存里，之后会落盘）。**机器断电**则可能丢未写回的页，需要 `msync`/`force()` 强制刷盘（再配合 `fsync`）。

### 6.2 Java 方式一：`MappedByteBuffer`（传统，稳定 API）

```java
import java.io.IOException;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class ClassicMap {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("/tmp/classic-map.bin");
        try (FileChannel ch = FileChannel.open(p, StandardOpenOption.CREATE, StandardOpenOption.READ, StandardOpenOption.WRITE)) {
            MappedByteBuffer mb = ch.map(FileChannel.MapMode.READ_WRITE, 0, 4096);
            mb.order(ByteOrder.nativeOrder());       // 默认是大端！与 C/FFM 共享数据时要对齐字节序
            mb.putLong(0, 0xCAFEBABEL);              // 绝对写，不影响 position
            mb.force();                               // msync：请求内核把脏页写回设备
            System.out.println(Long.toHexString(mb.getLong(0)));
        }
    }
}
```

限制和坑：

* **每次映射最大 2 GB**（`Integer.MAX_VALUE`，`ByteBuffer` 用 `int` 索引）。
* **没有确定性的取消映射**：映射存在，直到 `MappedByteBuffer` 对象被 GC 回收。想立刻释放没有公开 API。
* **字节序默认大端**（`ByteOrder.BIG_ENDIAN`），而 x86/ARM 的本地字节序是小端。`IpcDemo` 里我踩过这个坑：用 `MappedByteBuffer` 写 `0xCAFEBABEL`，再用 FFM 的 `ValueLayout.JAVA_LONG`（本地字节序）读，读到的是 `0xBEBAFECA00000000`。必须 `mb.order(ByteOrder.nativeOrder())`。
* 访问映射区时如果底层文件被别的进程截断，会导致 JVM 崩溃（`SIGBUS`）或抛 `InternalError`。

### 6.3 Java 方式二：FFM API（`java.lang.foreign`，JDK 21 为**预览**，JEP 442）

FFM = Foreign Function & Memory API，Project Panama 的成果，JDK 22 正式（JEP 454）。JDK 21 里是第三次预览，编译和运行都需要 `--enable-preview`：

```java
import java.io.IOException;
import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class FfmMap {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("/tmp/ffm-map.bin");
        try (FileChannel ch = FileChannel.open(p, StandardOpenOption.CREATE, StandardOpenOption.READ, StandardOpenOption.WRITE);
             Arena arena = Arena.ofShared()) {                              // Arena 管理生命周期；close 时确定性地取消映射
            MemorySegment seg = ch.map(FileChannel.MapMode.READ_WRITE, 0, 1L << 20, arena);   // 1 MB，大小用 long
            seg.set(ValueLayout.JAVA_LONG, 0, 42L);                         // 偏移 0 写一个 long（本地字节序）
            seg.set(ValueLayout.JAVA_INT, 8, 7);
            System.out.println(seg.get(ValueLayout.JAVA_LONG, 0) + " " + seg.get(ValueLayout.JAVA_INT, 8));
        }                                                                   // 这里 seg 被取消映射，再访问会抛异常
    }
}
```

相比传统方式的改进：

| | `MappedByteBuffer` | FFM `MemorySegment` |
|---|---|---|
| 最大映射大小 | 2 GB | `long`，可达 TB 级 |
| 取消映射 | 靠 GC，不确定 | `Arena.close()`，确定性 |
| 字节序 | 默认大端，需手动设 | 本地字节序（`ValueLayout.JAVA_LONG`）；大端要显式用 `withOrder` |
| 越界/已释放访问 | 越界检查；已释放 UB 风险 | 越界检查 + 时间安全检查（已释放抛异常） |
| 状态 | 稳定 | JDK 21 预览，JDK 22 正式 |

`Arena.ofConfined()` 只允许创建它的线程访问；`Arena.ofShared()` 允许多线程。**跨进程共享内存**的 `MemorySegment` 通常用 `ofShared()` 映射同一个文件。

### 6.4 `IpcDemo` 第 3 部分的输出

```text
read through FFM mapping: 0xCAFEBABE, segment size 4096
read through read(2) path: 0xCAFEBABE and 42
```

先用 `MappedByteBuffer` 写，再用 FFM 映射读到同一个值（对齐字节序之后），最后用普通的 `FileChannel.read` 也能读到——证明三条路径看到的是同一份页缓存。

### 6.5 共享内存的难点：同步和内存序

两个进程读写同一块内存，没有锁。怎么保证 B 读到的是 A 已经写完的完整数据？这就是下一节环形缓冲要解决的问题。

---

## 7. SPSC 环形缓冲（single-producer single-consumer ring buffer）

### 7.1 是什么

* **环形缓冲**：一个固定大小的数组，当作首尾相连的环使用。写满末尾后回到开头。hc04 讲义第 2.1 节讲过同样的结构。
* **SPSC**：只有**一个生产者**线程（进程）写，**一个消费者**线程（进程）读。
* 放在**共享内存**里：生产者和消费者可以是两个不同的进程。

### 7.2 为什么需要它

用 `ArrayBlockingQueue` 或 `LinkedBlockingQueue` 在线程之间传消息，每次 `put`/`take` 要加锁（`ReentrantLock`），有竞争时会阻塞（park/unpark，上节实测约 1.5 µs/次交接），还要分配节点（`LinkedBlockingQueue`）。跨进程则根本不能用它们。

**只有一个生产者和一个消费者**这个约束，让我们可以做到**完全无锁、无 CAS、无系统调用**：

* 只有生产者修改 `tail`（写位置）和槽位内容；
* 只有消费者修改 `head`（读位置）；
* 每个变量**只有一个写者**——不需要原子读改写，只需要保证**可见性与顺序**。

### 7.3 内存布局

```text
共享内存（一个映射文件）：

偏移 0                 128                256                                        256 + 8×容量
 ┌────────────────────┬────────────────────┬────────┬────────┬────────┬─────────┬────────┐
 │ head (8 B) + 填充   │ tail (8 B) + 填充   │ slot 0 │ slot 1 │ slot 2 │  ...    │ slot N-1│
 │ 消费者写            │ 生产者写            │        │        │        │         │        │
 └────────────────────┴────────────────────┴────────┴────────┴────────┴─────────┴────────┘
        ↑ 独占缓存行（本机 128 B，所以间隔 128）：避免 head 和 tail 伪共享

容量 N 是 2 的幂；槽位下标 = 序号 & (N - 1)  （和取模等价，但快）
```

### 7.4 算法（序号"只增不减"）

`head` 和 `tail` 都是**一直增加的序号**（long），不会回绕到 0；槽位是 `序号 & (N-1)`。

```text
元素个数 = tail - head
空：  tail == head
满：  tail - head == N

生产者 offer(v):
    t = tail                              （我是唯一的写者，直接读）
    如果 t - head == N：满了，返回 false
    slot[t & mask] = v                    ① 先写数据
    tail = t + 1       (release 写)       ② 再发布：让消费者能看见这个新元素

消费者 poll():
    h = head
    如果 h == tail (acquire 读)：空，返回"没有"
    v = slot[h & mask]                    ③ 读数据
    head = h + 1       (release 写)       ④ 释放槽位：让生产者能重用
```

**为什么用序号而不用下标回绕？**如果 `head`/`tail` 存的是下标（0..N-1），`head == tail` 既可能表示"空"也可能表示"满"，需要额外留一个空槽或加计数器。用只增的序号，空和满一眼区分（相等 vs 差 N）。64 位序号每秒 10 亿条也要几百年才会溢出。

### 7.5 关键：内存序（memory ordering）

这是正确性的核心。假设生产者先写数据 ①，再更新 `tail` ②。如果消费者看到了新的 `tail`，但**看不到**数据 ①（因为硬件或编译器把 ① 和 ② 的顺序重排了，或者数据还在生产者核心的写缓冲里没出来），消费者就会读到垃圾。

解决：用 Java 的 `VarHandle`（`java.lang.invoke`）提供的**有序访问模式**：

* **`setRelease`**（释放写）：保证"在它之前的所有写，对于另一个线程在看到这次写之后，都可见"。
* **`getAcquire`**（获取读）：保证"在它之后的所有读，不会被重排到它之前"。

配对：生产者的 `setRelease(tail)`（②）与消费者的 `getAcquire(tail)` 构成 *synchronizes-with* 关系：消费者看到新 `tail` 时，生产者在此之前对槽位的写一定可见。对称地，消费者的 `setRelease(head)`（④）与生产者的 `getAcquire(head)` 保证消费者读完槽位（③）之后生产者才能覆盖它。

x86 的内存模型（TSO）本来就禁止"写-写重排"，所以不少人在 x86 上不加屏障也"碰巧能跑"；但 ARM（包括 Apple 芯片、AWS Graviton）的内存模型很弱，会出真 bug。而且即使在 x86，**JIT 编译器**也可能把普通读写重排或把读提到循环外。所以一定要用有序访问。Doug Lea 的 "Using JDK 9 Memory Order Modes"（gee.cs.oswego.edu/dl/html/j9mm.html）是这些模式的权威指南。

> **关于"跨进程"的诚实说明**：Java 内存模型（JMM）形式上只定义同一个 JVM 里的线程之间的 happens-before。两个不同 JVM 进程通过共享内存通信，JMM 并不覆盖。实践中这么做是可行的——`VarHandle` 的 release/acquire 会编译成真正的 CPU 屏障指令，缓存一致性硬件对不同进程的核一视同仁——这也是 Aeron、Chronicle Queue 的做法，但它依赖的是硬件内存模型加 JIT 实现，不是 JMM 的形式保证。

### 7.6 优化：缓存对方的序号

生产者每次 `offer` 都读 `head` 来判断是否满，这是一次对"消费者正在写的缓存行"的读，会触发缓存行在两个核之间传递（乒乓）。优化：生产者**本地缓存**上次看到的 `head`（`cachedHead`），只有当"按缓存值看起来满了"时才真正重新读 `head`。消费者对 `tail` 同样处理（`cachedTail`）。这样多数时候一次共享内存读都不需要。

### 7.7 完整代码（`IpcDemo.SpscRing`，可编译）

```java
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;
import java.lang.invoke.VarHandle;

public final class SpscRing {
    // JDK 21: ValueLayout.varHandle() 的坐标只有 (MemorySegment)
    static final VarHandle LONG = ValueLayout.JAVA_LONG.varHandle();
    static final int HEADER = 256;                       // head 在 [0,128)，tail 在 [128,256)，槽位从 256 开始
    final MemorySegment headSeg, tailSeg, slots;
    final int capacity, mask;
    long cachedHead, cachedTail;                         // 对方序号的本地缓存（各只被一方使用）

    public SpscRing(MemorySegment mem, int capacity) {
        if (Integer.bitCount(capacity) != 1) throw new IllegalArgumentException("capacity must be a power of two");
        this.capacity = capacity;
        this.mask = capacity - 1;
        this.headSeg = mem.asSlice(0, 8);
        this.tailSeg = mem.asSlice(128, 8);
        this.slots = mem.asSlice(HEADER, (long) capacity * 8);
    }

    public static long bytesFor(int capacity) { return HEADER + (long) capacity * 8; }

    /** 生产者调用。满了返回 false。 */
    public boolean offer(long v) {
        long tail = (long) LONG.get(tailSeg);                         // 我是 tail 的唯一写者：普通读
        if (tail - cachedHead == capacity) {                          // 按缓存值看是满的：刷新
            cachedHead = (long) LONG.getAcquire(headSeg);
            if (tail - cachedHead == capacity) return false;
        }
        slots.set(ValueLayout.JAVA_LONG, (tail & mask) * 8, v);       // ① 先写数据
        LONG.setRelease(tailSeg, tail + 1);                           // ② 再发布（release）
        return true;
    }

    /** 消费者调用。空了返回 Long.MIN_VALUE。 */
    public long poll() {
        long head = (long) LONG.get(headSeg);
        if (head == cachedTail) {                                     // 按缓存值看是空的：刷新
            cachedTail = (long) LONG.getAcquire(tailSeg);             // acquire：与生产者的 release 配对
            if (head == cachedTail) return Long.MIN_VALUE;
        }
        long v = slots.get(ValueLayout.JAVA_LONG, (head & mask) * 8); // ③ 读数据
        LONG.setRelease(headSeg, head + 1);                           // ④ 释放槽位
        return v;
    }
}
```

要点逐行：

* `mem.asSlice(0, 8)` 把 `head` 所在的 8 字节单独切成一个小 `MemorySegment`，因为 JDK 21 的 `VarHandle` 只接受 `MemorySegment` 一个坐标（JDK 22 起加了偏移坐标）。
* `head` 和 `tail` 相隔 128 字节：本机缓存行 128 字节，两个计数器不在同一行，避免第 7 节（cpu_cache）的伪共享。
* 返回值用 `Long.MIN_VALUE` 当"空"哨兵，所以消息不能取这个值。真实系统会返回布尔值并通过别的方式给出消息，或者用变长消息帧（Agrona 的 `OneToOneRingBuffer` 就是带长度头的变长消息）。
* 容量是 2 的幂，`& mask` 代替 `%`。

### 7.8 用 `IpcDemo` 测它

在一个 JVM 里，用两个线程，映射一个临时文件，传 2000 万个 `long`，对比 `ArrayBlockingQueue<Long>`（容量相同）。真实输出（5 次，原文）：

```text
run 0: mmap SPSC ring     : 0.24 s -> 84.5 M msgs/s
run 0: ArrayBlockingQueue : 2.17 s -> 9.2 M msgs/s
run 1: mmap SPSC ring     : 0.27 s -> 74.3 M msgs/s
run 1: ArrayBlockingQueue : 2.86 s -> 7.0 M msgs/s
run 2: mmap SPSC ring     : 0.27 s -> 74.2 M msgs/s
run 2: ArrayBlockingQueue : 2.71 s -> 7.4 M msgs/s
run 3: mmap SPSC ring     : 0.25 s -> 78.9 M msgs/s
run 3: ArrayBlockingQueue : 2.62 s -> 7.6 M msgs/s
run 4: mmap SPSC ring     : 0.25 s -> 80.2 M msgs/s
run 4: ArrayBlockingQueue : 3.04 s -> 6.6 M msgs/s
```

环形缓冲约 **10 倍**吞吐（每条约 12 ns 对约 130 ns）。别的时间运行同一个程序，环形缓冲吞吐曾落在 27–50 M msgs/s（这台机器的核心类型不同、系统负载不同，吞吐上下浮动 2–3 倍），`ArrayBlockingQueue` 稳定在 5–9 M msgs/s；一次孤立的运行还出现过 313 M msgs/s，我没找到原因，请忽略。**倍数方向稳定，绝对数字不稳定。**

### 7.9 跨两个 JVM 进程

`IpcDemo` 可以分别启动消费者和生产者两个进程，映射同一个文件（先启动消费者，等一秒再启动生产者）：

```text
java --enable-preview --enable-native-access=ALL-UNNAMED IpcDemo consumer /tmp/ring.bin 50000000 &
java --enable-preview --enable-native-access=ALL-UNNAMED IpcDemo producer /tmp/ring.bin 50000000
```

三次真实输出：

```text
[pid 98701] producer wrote 50000000 msgs in 0.89 s
[pid 98698] consumer read 50000000 msgs in order, 56.1 M msgs/s
[pid 98711] producer wrote 50000000 msgs in 0.46 s
[pid 98709] consumer read 50000000 msgs in order, 109.5 M msgs/s
[pid 98728] producer wrote 50000000 msgs in 0.37 s
[pid 98724] consumer read 50000000 msgs in order, 136.4 M msgs/s
```

5000 万条消息，**两个独立的 OS 进程**，消费者校验了每一条都按顺序到达（`out of order` 检查通过）。每次 56–136 M msgs/s，波动来自两个进程被调度到哪两个核。也许让你惊讶：跨进程并不比同进程两线程更慢——因为两者的数据路径一样：缓存行在两个核之间传，进程边界并不介入。

### 7.10 真实世界里的同类东西

* **Agrona**（Real Logic）的 `OneToOneRingBuffer` / `ManyToOneRingBuffer`：就是变长消息版的共享内存环形缓冲。
* **Aeron** 的 IPC 通道：同机进程之间通过映射文件里的日志缓冲区通信，延迟在百纳秒量级。
* **Chronicle Queue**：映射文件上的追加日志，既是 IPC 又是持久化日志。
* **LMAX Disruptor**：同一 JVM 内线程间的环形缓冲（有序号、等待策略、缓存行填充），论文：Thompson 等 2011。
* **Linux io_uring**（Jens Axboe）：内核与用户态之间的提交队列（SQ）和完成队列（CQ）是**映射在共享内存里的 SPSC 环形缓冲**——用户态写 SQ、内核读；内核写 CQ、用户态读，从而省掉每次 I/O 的系统调用。

### 7.11 生产环境还要考虑的

* **多生产者 / 多消费者**：需要 CAS 争抢序号（MPSC、MPMC），复杂得多；常见做法是 N 个 SPSC 环（每个生产者一个）由一个消费者轮询。
* **变长消息**：每条消息带长度头，处理环尾回绕（填充消息）。
* **崩溃恢复**：进程崩溃后文件里留着旧的 `head`/`tail`；要有魔数、版本号、清理策略。
* **背压**：满了怎么办——丢弃、自旋等待、返回错误？
* **页预热**：第一次访问映射页会缺页；启动时先写一遍。
* **放 tmpfs**：Linux 上把文件放 `/dev/shm`，避免磁盘写回干扰。

---

## 8. 常见误区

1. **「线程比进程快，所以都用线程」。**线程没有隔离，一个 bug 全死；多个进程组成的流水线（行情进程、策略进程、网关进程）可以独立重启、独立崩溃。选择是工程取舍。
2. **「系统调用就是函数调用」。**差约 150 倍（第 4.3 节）。热路径上的每个 `System.currentTimeMillis()`、日志写入、小文件读写都要审视是否进内核。
3. **「锁的开销就是几十纳秒」。**无竞争时是，有竞争时会 park 睡眠，一次交接 1–几微秒，还带来调度抖动。
4. **「`mmap` 一定比 `read` 快」。**它省去一次拷贝，但引入缺页（首次访问）、TLB 压力，并且 I/O 错误以信号形式出现。对大文件的顺序读，`read` + 预读常常不输 `mmap`。`mmap` 的最大价值是**零系统调用地随机访问**和**进程间共享**。
5. **「共享内存里直接写普通变量就行」。**没有有序访问就没有可见性/顺序保证（第 7.5 节）。
6. **「`MappedByteBuffer` 默认和 C 结构体兼容」。**默认大端；与 C/FFM 共享要 `order(nativeOrder())`。
7. **「忙等是浪费」。**在低延迟系统里，把一个核专门用来忙等，是用 CPU 换延迟的有意设计。在通用服务器上则是浪费。

---

## 9. 面试追问预演

**Q1：进程和线程的区别？**
答：「进程有独立的虚拟地址空间，提供隔离，创建和切换成本高；线程共享所属进程的地址空间，只有各自的栈和寄存器，创建和切换便宜，但共享数据需要同步，一个线程出错会拖垮整个进程。Linux 内核里两者都是 task，线程是共享地址空间的 task。Java 平台线程和内核线程 1:1；JDK 21 的虚拟线程是 JVM 调度的用户态线程。」

**Q2：上下文切换为什么贵？**
答：「直接成本是进内核、存取寄存器、调度，约一到几微秒；更大的是间接成本：缓存、TLB、分支预测器被新线程污染，要重新预热；跨核醒来缓存全冷。我实测过阻塞式交接 park/unpark 往返约 2.5–3 µs，忙等往返约 90 ns，所以低延迟系统把热线程绑核自旋。」

**Q3：什么是系统调用，为什么要尽量少？**
答：「用户态程序通过 syscall 指令请求内核服务，要切模式、保存恢复寄存器、校验参数，在有 Meltdown 缓解的内核上还要切页表，加上缓存污染。我在 macOS 上测一次最轻的 `write` 约 600 ns，不进内核的 libc 调用只要几 ns。优化办法：批量、聚集 I/O、`Selector`、共享内存、内核旁路。」

**Q4：同机两个进程要传高频小消息，怎么设计？**
答：「共享内存加 SPSC 环形缓冲。映射同一个文件（Linux 放 `/dev/shm`）。head 和 tail 各占一条缓存行避免伪共享，序号只增不减，槽位用 `序号 & mask`。生产者先写数据，再用 release 写 tail；消费者 acquire 读 tail，读数据，再 release 写 head。每个变量单写者，无锁无 CAS。Java 里用 FFM 的 `MemorySegment` 加 `VarHandle`，我测过两个进程传 5000 万条，每秒几千万到上亿条。」

**Q5：为什么用 release/acquire 而不是 volatile？**
答：「volatile 是顺序一致（sequentially consistent），在 x86 上写要带 `lock` 前缀或 `mfence`，贵；SPSC 只需要 release/acquire 这种较弱的排序，在 x86 上基本是普通 mov，在 ARM 上是 `stlr`/`ldar`，更便宜。」

**Q6：mmap 和 read 的区别？什么时候用 mmap？**
答：「`read` 把页缓存的数据拷贝到用户缓冲区，每次一次系统调用；`mmap` 让页表直接指向页缓存，访问不需要系统调用也没有拷贝，第一次访问触发缺页。适合随机访问大文件、多进程共享、需要持久化的消息日志。要注意字节序、文件截断导致的 SIGBUS、刷盘语义（`force`）。」

---

## 10. 自测题

**Q1（概念）** 进程崩溃会不会影响同一机器上的另一个进程？同一进程里一个线程抛了未捕获异常呢？

<details><summary>答案</summary>

一般不会影响别的进程（地址空间隔离；除非共享了资源并且依赖对方）。同一进程里一个线程抛未捕获的 `Exception`，只终止这个线程（JVM 继续跑，其他线程不受影响）；但如果是 `OutOfMemoryError` 等导致整个 JVM 崩溃，或原生代码段错误（`SIGSEGV`），整个进程退出，所有线程陪葬。

</details>

**Q2（估算）** 一个服务每秒处理 100 万条消息，每条处理要 1 次系统调用（600 ns）。系统调用占多少 CPU？

<details><summary>答案</summary>

10⁶ × 600 ns = 0.6 秒 / 秒 = 一个核的 60%。如果批量处理 100 条才调一次，降到 0.6%。

</details>

**Q3（读代码）** 下面的"发布"有什么问题？

```java
class Box {
    long[] data = new long[8];
    boolean ready;                 // 普通字段
}
// 线程 A：  box.data[0] = 42; box.ready = true;
// 线程 B：  while (!box.ready) { }  System.out.println(box.data[0]);
```

<details><summary>答案</summary>

没有同步：`ready` 不是 `volatile`，B 的循环可能被 JIT 提升成死循环（永远读寄存器里的旧值）；即使 B 看到了 `ready == true`，也不保证看到 `data[0] == 42`（写重排或缓存未同步）。修法：`volatile boolean ready`（volatile 写 happens-before 后续对它的读），或用 `VarHandle.setRelease`/`getAcquire`。

</details>

**Q4（设计）** SPSC 环形缓冲里，为什么 `head` 和 `tail` 要放在不同缓存行？如果放在同一行会发生什么？

<details><summary>答案</summary>

生产者持续写 `tail`，消费者持续写 `head`。同一缓存行里时，每次写都使对方核心的那一行失效，两个核反复把这一行抢来抢去（伪共享），每次访问几十 ns 的跨核通信，吞吐会大幅下降。分开放，各自核心独占自己的行，只在需要读对方序号时才传输（配合缓存对方序号，大多数时候都不需要）。

</details>

**Q5（代码）** 修改 `SpscRing.offer`，让它支持返回"成功/失败"，并让生产者在满的时候自旋等待最多 `n` 次再放弃。

<details><summary>答案</summary>

```java
interface Ring { boolean offer(long v); }               // 例如 SpscRing 实现了它

static boolean offerSpin(Ring ring, long v, int maxSpins) {
    for (int i = 0; i < maxSpins; i++) {
        if (ring.offer(v)) return true;
        Thread.onSpinWait();            // 告诉 CPU 这是自旋循环（x86 上编译成 PAUSE 指令）
    }
    return false;                       // 放弃，调用方决定丢弃或报警（背压）
}
```

`offer` 已经返回 boolean；这里包一层有限自旋。注意不要无限自旋，否则消费者挂了生产者就卡死。

</details>

**Q6（辨析）** 管道、Unix 域套接字、共享内存，哪个延迟最低，为什么？哪个最容易用？

<details><summary>答案</summary>

共享内存延迟最低：建立后读写不需要系统调用，也没有内核拷贝。管道和 Unix 域套接字每条消息两次系统调用、两次拷贝，延迟在微秒级。最容易用的是管道（Shell 的 `|`），其次是 Unix 域套接字（API 与 TCP 相同）；共享内存最难，因为同步、内存序、崩溃恢复都要自己做。

</details>

**Q7（概念）** `MappedByteBuffer.force()` 做了什么？进程崩溃时，已写到映射区但没 `force()` 的数据会丢吗？

<details><summary>答案</summary>

`force()` 对映射区调用 `msync`，请求内核把脏页写到存储设备。写到映射区的数据先落在内核页缓存里，进程崩溃后这些页仍在页缓存中，之后由内核写回，所以**进程崩溃不会丢**。机器断电或内核崩溃才会丢尚未写回的页——要抗断电需要 `force()`（以及保证设备本身的写缓存落盘）。

</details>

---

## 11. 延伸阅读（只列权威来源）

* **Arpaci-Dusseau,《Operating Systems: Three Easy Pieces》（OSTEP，免费在线）**：第 4–5 章（进程与进程 API）、**第 6 章「Mechanism: Limited Direct Execution」**（系统调用与上下文切换的最佳入门）、第 7–9 章（调度）、第 13–23 章（虚拟内存）、第 26–28 章（线程与锁）。
* **Michael Kerrisk,《The Linux Programming Interface》**：第 3 章（系统调用）、第 6 章（进程）、第 24–28 章（进程创建与执行）、**第 44 章（管道和 FIFO）、第 49 章（内存映射）、第 52 章（POSIX 消息队列）、第 54 章（POSIX 共享内存）**。
* **Brendan Gregg,《Systems Performance》第 2 版**：第 3 章「Operating Systems」（系统调用、调度、虚拟内存）、第 6 章「CPUs」、第 7 章「Memory」。
* **Ulrich Drepper, *What Every Programmer Should Know About Memory***：第 4 章虚拟内存（页表、TLB）、第 6.4 节多线程优化。
* **JEP 444: Virtual Threads**；**JEP 442: Foreign Function & Memory API (Third Preview)**（JDK 22 正式化为 JEP 454）；**JEP 380: Unix-Domain Socket Channels**。
* **Java SE 21 API：`java.nio.channels.FileChannel#map`、`java.nio.MappedByteBuffer`、`java.lang.foreign.MemorySegment`、`java.lang.foreign.Arena`、`java.lang.invoke.VarHandle`**（访问模式 `getAcquire/setRelease` 的语义）。
* **Doug Lea, "Using JDK 9 Memory Order Modes"**：release/acquire/opaque/volatile 四种模式的权威指南。
* **Thompson, Farley, Barker, Gee, Stewart, "Disruptor: High performance alternative to bounded queues for exchanging data between concurrent threads", LMAX, 2011**；**Agrona**（github.com/real-logic/agrona）与 **Aeron**（github.com/real-logic/aeron）源码与 wiki。
* **Jens Axboe, "Efficient IO with io_uring"（2019）**：共享内存环形缓冲在内核接口中的应用。
* **Li, Ding, Shen, "Quantifying the Cost of Context Switch", ExpCS 2007**：上下文切换间接成本的实测。
