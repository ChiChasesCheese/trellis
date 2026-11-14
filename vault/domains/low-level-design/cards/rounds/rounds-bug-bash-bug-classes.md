---
id: rounds-bug-bash-bug-classes
node: rounds.bug-bash
type: qa
step: 2
---
## Q
在陌生的 Python 代码里找缺陷，要按哪几类逐一扫？每一类在代码里长什么样、怎么快速确认？

## A
**按类扫，比"凭感觉找"覆盖得全。** 每类记住两三个长相和一个确认办法。

- **差一错误（off-by-one）：**
  - 长相：`range(1, n)` 漏了下标 0；`range(len(a) - 1, 0, -1)` 倒序漏了第一个；`<` 和 `<=` 用反；切片 `a[:n-1]`。
  - 确认：用长度 0、1、2 的输入手推。
- **共享可变状态（shared mutable state）：**
  - 长相：可变默认参数 `def f(x, acc=[])`，默认值只在定义时创建一次，所有调用共用；类属性 `items = []` 被所有实例共享；函数返回内部列表，调用方一改就改了内部状态。
  - 确认：同一函数调两次，看第二次结果是否带着第一次的东西。
- **资源泄漏（resource leak）：**
  - 长相：`f = open(p)` 没有 `with`；数据库连接、套接字、线程池没有关闭；异常路径上跳过了关闭。
  - 确认：`python -X dev` 或 `-W error::ResourceWarning` 会把未关闭的文件报出来。
- **吞异常（exception swallowing）：**
  - 长相：`except Exception: pass`、`except: continue`、出错就返回 0 或空列表。裸 `except:` 还会接住 `KeyboardInterrupt` 和 `SystemExit`。
  - 确认：搜 `except`，每一处问"出错后调用方知道吗？"
- **时间与时区：**
  - 长相：不带时区的时间（naive）和带时区的时间（aware）比较，抛 `TypeError`；`datetime.utcnow()` 返回不带时区的时间，3.12 起已弃用；用 `time.time()` 算耗时，系统校时会让它跳变，应用 `time.monotonic()`；带不同时区偏移的时间字符串按字典序排序。
  - 确认：用跨午夜、跨夏令时、带 `+08:00` 的样例跑。
- **浮点相等：**
  - 长相：`0.1 + 0.2 == 0.3` 为 `False`；金额用 `float` 累加。
  - 确认：改成 `math.isclose(a, b, rel_tol=1e-9)`；金额用 `Decimal` 或整数分。
- **并发：**
  - 长相：多线程里 `count += 1`，读、加、写三步之间可能切换线程，即使有全局解释器锁（GIL）也会丢更新；先检查后操作（`if k not in d: d[k] = ...`）；遍历字典时另一个线程在改；`lock.acquire()` 后异常导致没释放。
  - 确认：用 `with lock:`；把线程数调到 8、循环跑 1,000 次放大问题。
