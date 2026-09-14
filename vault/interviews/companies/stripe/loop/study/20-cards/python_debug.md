# 卡片 · Python 调试（Bug Squash 轮）

> 配套长文：`loop/rounds/04_bug_squash/DEBUG_101.md`（从零讲起，含真跑出来的 pdb 实录）。
> 格式：`| Q | A | 来源 |`。来源为 `stdlib` / `pytest` 的表示可在官方文档核实；其余标出处。

## pdb 基本操作

| Q | A | 来源 |
|---|---|---|
| 怎么在一行代码处停下来，不用 import 任何东西？ | 写 `breakpoint()`（Python 3.7+，PEP 553）。等价的老写法是 `import pdb; pdb.set_trace()` | stdlib |
| 不改代码，怎么让测试一失败就进调试器？ | `pytest <路径> --pdb`，进入 post-mortem：崩溃后现场还在，直接查变量 | pytest |
| pdb 里 `l` 和 `ll` 的区别？ | `l` 看当前行前后几行；`ll`（longlist）打印**整个当前函数**，找上下文用 `ll` | stdlib |
| `n` 和 `s` 的区别？ | `n`(next) 执行下一行**不进入**被调函数；`s`(step) **进入**被调函数第一行 | stdlib |
| 想一路跑到当前函数返回，用什么？ | `r`(return) | stdlib |
| 怎么打印当前函数的全部参数？ | `a`(args)，比逐个 `p` 快 | stdlib |
| 异常在最里层抛出，但我怀疑上层传错了值，怎么办？ | `u`(up) 往调用栈上走一层，每层用 `a` 打参数，找"值从哪层开始就不对" | stdlib |
| pdb 里 `p` 和 `pp` 选哪个？ | 短值 `p`；字典/列表等长数据 `pp`（pretty print，会换行排版） | stdlib |
| pdb 里怎么看现在的调用栈？ | `w`(where)，输出跟 traceback 一样但是"活"的 | stdlib |
| 在 pdb 里按 `u` 之后 `p node` 报 `NameError`，为什么？ | 很可能上一层是生成器表达式 `<genexpr>` 帧，它只有自己的循环变量，外层名字不在作用域。**再按一次 `u`** | 本仓库 bs01 实测 |

## 读 traceback

| Q | A | 来源 |
|---|---|---|
| traceback 从哪头读？ | **从下往上**。最后一行是异常类型+消息，上面是调用栈（下=最里层，上=最外层） | stdlib |
| traceback 里哪两行最重要？ | ① 最后一行（异常本身）② 倒数第一个属于**被测库**的帧（异常发生位置）。中间多是路过 | 本仓库 DEBUG_101 |
| 同一行代码在栈里出现两次，是递归吗？ | 未必。生成器表达式 `(f(x) for x in xs)` 有**独立栈帧**，会看到外层和 `<genexpr>` 各一次 | 本仓库 bs01 实测 |
| `Failed: DID NOT RAISE LookupError` 怎么读？ | 没有异常栈，因为问题是"**该抛的没抛**"。去测试文件看期望条件，再去被测代码找那个判断 | 本仓库 bs01 实测 |
| 想让 traceback 更短/更长？ | `--tb=long/short/line/no`，日常用 `short`，一次挂几十个先用 `line` | pytest |

## 探查陌生对象

| Q | A | 来源 |
|---|---|---|
| 怎么看一个陌生对象有哪些某类方法？ | `p [m for m in dir(obj) if m.startswith("visit_")]` —— `dir()` 加筛选，这一轮最值钱的套路 | 本仓库 bs01 实测 |
| 怎么看实例的所有字段和当前值？ | `p vars(obj)`（等价 `obj.__dict__`） | stdlib |
| 怎么看这个类继承自谁？ | `p type(x).__mro__` | stdlib |
| 怎么确认一个对象到底是什么类型？ | `p type(x).__name__`（比 `p x` 更直接，`__repr__` 可能骗人） | stdlib |

## pytest 开关

| Q | A | 来源 |
|---|---|---|
| 改一行验一次，最快的命令是？ | `pytest <目录> --lf --tb=short`（`--lf` = last failed，只跑上次红的） | pytest |
| 一次挂很多想逐个击破？ | `-x`：第一个失败就停 | pytest |
| 我的 `print` 为什么没显示？ | pytest 默认捕获 stdout，加 `-s` 关掉捕获 | pytest |
| 只想跑某个 part 的测试？ | `-k "part2"`，按测试名关键词筛 | pytest |
| 本仓库跑 pytest 有什么特别注意？ | `pytest.ini` 已带 `-q`，命令行**别再加 `-q`**，会吞掉汇总行 | 本仓库 CONVENTIONS |

## print 调试

| Q | A | 来源 |
|---|---|---|
| 调试输出该往哪打？ | **stderr**：`print(..., file=sys.stderr)`。stdout 是要被逐字节比对的答案，打脏了就算错 | 本仓库 CONVENTIONS |
| 怎么少写一半 print 的字？ | f-string 的 `=` 语法：`print(f"{x=} {y=}")` 打成 `x=3 y=4`，变量名自动带上（3.8+） | stdlib |
| print 和断点各适合什么？ | print 适合看**循环里值怎么变**；断点适合在**一个点**上把周围翻个底朝天。互补，不是二选一 | 本仓库 DEBUG_101 |

## 会咬人的 Python 机制

| Q | A | 来源 |
|---|---|---|
| `def f(x, acc=[])` 有什么问题？ | 默认值只求值一次，`acc` 在**所有调用间共享**，第二次调用带着上次的数据 | stdlib |
| 单跑一个测试绿、连着跑就红，第一嫌疑是什么？ | **跨调用残留状态**：实例字段该在 `reset()`/`__init__` 清而没清 | LOOP_GUIDE §4 |
| `[lambda: i for i in range(3)]` 三个 lambda 返回什么？ | 全返回 `2`。闭包**晚绑定**：调用时才查 `i`，那时循环已结束 | stdlib |
| 什么时候能用 `is`？ | 只跟 `None` / `True` / `False` 比。小整数和短字符串被缓存，`is` 有时"碰巧"对，靠不住 | stdlib |
| `d2 = dict(d1)` 之后改 `d2` 会影响 `d1` 吗？ | 顶层不会，**嵌套的 list/dict 会**——这是浅拷贝。要断开用 `copy.deepcopy` | stdlib |
| 同一个生成器 `for` 两次，第二次拿到什么？ | 空。生成器只能迭代一次，要多次用就 `list()` 固化 | stdlib |
| 排序结果"差不多对"，只有某些用例红，查什么？ | `sorted` 的 **key / tie-break 写错**——只在键相同时才暴露 | LOOP_GUIDE §4 |
| `TypeError: list indices must be integers` 常见成因？ | 用了 `/` 而不是 `//`。`/` 永远返回 float | stdlib |
| 结果不对但一个报错都没有，查什么？ | 异常被吞：`except Exception: pass`，或 `gather(..., return_exceptions=True)` 后没检查返回值 | 本仓库 DEBUG_101 |
| Bug Squash 进场先按哪几类猜？ | 逻辑错误 · off-by-one · 符号反转 · 跨调用残留状态 · 排序用错 comparator | leonstaff 2026-08-13 |

## 并发（bs04 / bs05）

| Q | A | 来源 |
|---|---|---|
| GIL 能保证 `if k not in d: d[k] = v` 是原子的吗？ | **不能**。GIL 只保证单条字节码原子，这是两步，中间可被打断——典型 check-then-act 竞态 | stdlib |
| `await` 在并发上意味着什么？ | 它是**让出点**：协程可能在这里被挂起，别的协程会跑。`await` 前读到的共享状态，`await` 后可能已变 | stdlib |
| `asyncio.gather` 返回值的顺序是？ | **传入顺序**，不是完成顺序。当成完成顺序就错 | stdlib |
| `gather(..., return_exceptions=True)` 的陷阱？ | 异常变成返回列表里的一个对象，不再抛出。不逐个 `isinstance(r, Exception)` 检查就会被当成正常结果统计 | stdlib |
| 同一线程二次 `lock.acquire()` 会怎样？ | 直接死锁。`threading.Lock` **不可重入**，递归场景要用 `RLock` | stdlib |
| 并发 bug 的失败测试怎么写才算合格？ | 必须**确定性复现**（100% 红）。用 `threading.Barrier` / `Event` / 注入 sleep 点强制交错，不能写成偶发 flaky | 本仓库 bs04/bs05 AC |

## 这一轮的元知识

| Q | A | 来源 |
|---|---|---|
| 拿到题第一件事做什么？ | **先跑失败测试**，亲眼确认错误长什么样，再读代码。"跳过这步直接读代码，是有经验的工程师不会犯的错" | leonstaff 2026-08-13 |
| 面试官这一轮主要在评什么？ | 不是"修没修好"——"solving the bug isn't the primary objective"，评的是独立调试能力、方法论、沟通 | Stripe 员工（Blind） |
| 强表现的标准动作是哪五个？ | 读入口 → 早下断点 → 说出假设 → 验证 → 精准最小修复 | Blind bxonqpkp |
| 一轮通常几个 bug？ | 2026 年三份材料都说 **2–3 个**（其中两份是搜索摘要）；老证据说 1 主 + follow-up。按 2–3 准备 | discovery/2026-09 |
| 这一轮能用 AI 助手吗？ | **明确禁止**（除 AI Programming Exercise 外的所有轮都禁） | leonstaff 2026-08-13 |
| 挂点第一名是什么？ | 只用 print、不会 debugger | LOOP_GUIDE §4 |
| Python 版 Bug Squash 的通过率？ | Stripe 员工 2022 年说 **"<10%"** | LOOP_GUIDE §4 |
| 修完一个 bug 之后该做什么？ | 主动问"要我继续找下一个吗"，并加一个回归测试锁住行为 | 本仓库 DEBUG_101 |
