# 前置课 02 · 并发基础：线程、锁、条件变量、原子性、竞态、死锁、GIL

> 目标：JD 明确写"并发 1/6"，但 `../../catalog/skills_matrix.md` S10 显示 5/9 道 OOD 题有并发追问——**面试考的不是并发理论，是"能不能把一个单线程正确的类改成线程安全的，并说清为什么"**。这篇是 `../00-essentials/04-class-design-and-concurrency.md` §6/§7 的背景知识；具体到 kit 题目的做法在那篇里，这篇只讲概念本身。

---

## 1. 线程（Thread）：面试语境下的最小心智模型

一个进程内可以有多个线程，**共享同一份内存**（堆上的对象、模块级变量），但各自有独立的调用栈和程序计数器。Java 里你熟悉的 `Thread`/`Runnable`/`ExecutorService`，Python 对应 `threading.Thread`/`concurrent.futures.ThreadPoolExecutor`。

**面试里怎么说**："Multiple threads share the same heap, so any mutable state one thread writes is visible to another — that's exactly the source of the bug, not a feature that needs extra plumbing to enable."

**Snowflake 面试里几乎不会真的要求你写 `Thread` 的创建/join——考点永远是"给定一个类，怎么让它在多线程下正确"，不是"怎么起线程"。**

---

## 2. 锁（Lock）：用来保护什么，不是用来"防止并发"

锁保护的是**不变量**，不是"这段代码"。拿到锁只意味着"当前没有其他持锁者在修改被保护的状态"，不意味着代码本身变快或变安全——锁只解决**互斥**，不解决逻辑错误。

```python
import threading
lock = threading.Lock()
with lock:                 # 面试里永远用 with，不要手写 acquire/release
    shared_counter += 1
```

**最小锁原则**（详见 `../00-essentials/04-class-design-and-concurrency.md` §6②）：锁的范围应该恰好覆盖"读取-判断-写入"这个必须原子发生的序列，不多不少。锁范围过大会牺牲并发度（这也是"分段锁"存在的原因）；锁范围过小会让不变量在锁释放的间隙被破坏。

**易错**：`with lock1: with lock2:` 和 `with lock2: with lock1:` 在两个线程里分别出现，就是死锁的经典成因（见 §6）。

---

## 3. 条件变量（Condition Variable）：等待某个条件成立

`threading.Condition` 让一个线程可以"释放锁并睡眠，直到别的线程通知条件可能已经成立"，而不是自己不停地加锁检查（忙等，浪费 CPU）。

```python
cond = threading.Condition()
def consumer():
    with cond:
        while not queue:            # 用 while 不用 if：被唤醒后条件可能又变了
            cond.wait()
        item = queue.pop()

def producer(item):
    with cond:
        queue.append(item)
        cond.notify()               # 唤醒一个等待者；notify_all() 唤醒全部
```

**本 kit 目前没有题目直接考条件变量**，但 `od09`（队列服务）如果被追问"`dequeue()` 队列为空时要不要阻塞等待"，这就是条件变量的使用场景——面试里说清"我会用 `Condition` 让消费者线程睡眠，而不是自旋轮询"即可，不一定要求写全。

**易错**：永远用 `while` 检查条件，不用 `if`——"虚假唤醒"（spurious wakeup）和"被唤醒时条件已经被别的消费者线程抢先满足"都要求重新检查条件，而不是假设醒来就一定能继续。

---

## 4. 原子性（Atomicity）与竞态条件（Race Condition）

**原子操作**：从其他线程的视角看，要么完全没发生，要么完全发生了，不会观察到"发生了一半"的中间状态。

**竞态条件**：两个或以上线程访问共享状态，至少一个在写，且没有同步机制保证顺序，导致结果依赖于线程调度的时序——**这是面试问"how would you make this thread-safe"时真正要考的东西**。

```python
# 竞态条件的经典例子：这一行代码在字节码层面不是一次操作
counter += 1
# 实际是三步：读 counter → 加 1 → 写回 counter
# 两个线程交错执行，可能都读到同一个旧值，最终少加了一次
```

**GIL 对这个问题的影响，也是最容易被面试官问懵的地方**：CPython 的全局解释器锁（GIL）保证**同一时刻只有一个线程在执行 Python 字节码**，这确实让**单条字节码指令**（比如一次简单赋值）看起来是原子的。但 `counter += 1` 编译后是**多条字节码**（LOAD、ADD、STORE），GIL 可以在这些指令之间切换线程——**所以复合操作依然不是原子的，GIL 不能替代锁**。

**面试里正确的说法**：
> "The GIL serializes bytecode execution, but a compound operation like `x += 1` spans multiple bytecode instructions, so the GIL can still switch threads in between — I still need a lock around any read-modify-write sequence."

**错误的说法（减分）**："Python 有 GIL 所以不用加锁"——这句话在任何"复合操作"或"多个字段要一起改"的场景下都是错的，`od01` 的"扫描堆 + 标记已执行"、`od03` 的"读全局态 + 判断 + 写全局态"都是复合操作，必须显式加锁。

**GIL 唯一真正省心的场景**：单个内置类型的单一操作（比如一次 `dict[key] = value` 整体赋值、`list.append`）在 CPython 里通常是线程安全的，因为它对应的字节码序列很短且不会被 GIL 切分出可观察的中间状态——但这是**实现细节**，不是语言规范承诺，面试里可以提一句作为"了解 CPython 实现"的加分项，不能当成设计依据。

---

## 5. 死锁（Deadlock）：面试里怎么快速判断"我的设计会不会死锁"

四个必要条件（Coffman conditions）同时满足才会死锁：互斥、持有并等待、不可抢占、循环等待。面试里不需要背这四条，**只需要检查一件事：会不会有两个执行路径以相反顺序获取两把锁？**

```python
# 危险：两个方法用不同顺序拿两把锁
def transfer(a, b, amount):
    with a.lock:
        with b.lock:      # 如果同时有 transfer(b, a, ...) 在跑，顺序相反 → 死锁
            ...
```

**标准解法**：固定获取顺序（比如按对象 id 或 key 排序后总是先锁"更小"的那个），或者干脆避免"同时持有两把锁"的设计（`od02` 的做法：结构锁只在遍历树时短暂持有，找到目标文件后**释放结构锁**再拿文件自己的锁，两把锁不同时持有，天然没有死锁风险）。

**本 kit 里没有需要"同时持有两把锁"的题**——这恰恰是因为好的锁设计（分段、最小化持锁时间）本身就在规避死锁，`../00-essentials/04-class-design-and-concurrency.md` §6 的"分段锁"策略就是这个原则的实践。

---

## 6. 一张对照表：这些概念在 kit 题目里具体是什么

| 概念 | 在哪道题体现 | 具体机制 |
|---|---|---|
| 最小锁 | `od01`（Task Scheduler）| 锁只包住"扫描候选 + 标记已执行"，不包住整个 `add()` |
| 分段锁 | `od02`（文件系统）| 结构锁（树形状）与每文件锁分开，互不阻塞 |
| 线程私有状态（不需要锁）| `od03`（事务 KV）| `threading.local()` 存每线程自己的事务栈 |
| 存储层 CAS/lease（替代长期持锁）| `od05`（Cron Scheduler）| `LeaseStore.try_claim`：原子性的"若未被占用则占用" |
| 竞态窗口 | `od04`（多规则限流器）| "谁先占到这个时刻的配额"必须原子判断+登记 |

详细代码见 `../00-essentials/04-class-design-and-concurrency.md` §2–§6。

---

## 7. 自测

- [ ] 用一句话解释"GIL 让某些操作看起来原子"和"GIL 让所有操作都安全"的区别，并举一个反例
- [ ] 说出死锁的判断捷径（不用背四个条件，说那一句话）
- [ ] 解释 `threading.local()` 为什么不需要加锁，它和"加锁保护共享状态"是同一件事的两种解法吗？
- [ ] 挑 `od01`/`od02`/`od03`/`od04`/`od05` 中一题，口述它的锁策略属于哪一类（最小锁/分段锁/线程私有/CAS-lease）
