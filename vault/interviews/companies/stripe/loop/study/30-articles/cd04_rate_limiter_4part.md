# cd04 · Rate Limiter (4-part)：一个限流器四次加固，练的是"从能跑到能上线"的叠加思路

> [!tldr]
> - 这题考的是：把一个"能跑但会炸"的限流器，用四个 part 分别加固成内存有界、行为确定、并发安全的
>   生产版本——不是四个新算法，是同一份代码的四次体检
> - 三步套路：先写最朴素的"扫全部历史"版本证明规则本身对 → 把"扫全部历史"换成"只留还在窗口里的"
>   → 把隐藏在题面缝隙里的未定义行为一条条钉死，最后拿一把锁把整个决策过程包起来
> - 最值得带走的一个模式：**滑动窗口日志（deque）的内存有界性是"拒绝的请求从不入账" + "每次调用都
>   先裁剪过期项"两条规则一起保证的，缺一不可**——这个证明本身就是这题的考点，不只是代码

## 1. 题目在说什么（人话版）
Stripe 的每个 API key 都有限流。这题不问你"用哪个限流算法"（那是另一道题 `q23_rate_limiter` 的
考法：滑动窗口、加权、token bucket 换着考），而是问你："给你一个能跑的限流器，怎么一步步把它做成
你敢部署到生产的样子？" 四关分别是：先做对（Part 1），再做到不漏内存（Part 2），再把"如果时钟回拨
了怎么办"这类没写在题面里的问题一个个问清楚并钉死（Part 3），最后保证多线程同时打过来时结果依然
精确（Part 4）。

小例子（Part 1，`limit=3, window_s=1`，`t` 是毫秒）：
```
allow("u", 0)    -> True    # 第 1 次
allow("u", 100)  -> True    # 第 2 次
allow("u", 200)  -> True    # 第 3 次，到限额了
allow("u", 300)  -> False   # 窗口 (-700, 300] 里已经有 3 次，拒绝
allow("u", 1000) -> True    # 窗口滑到 (0, 1000]，t=0 那次被甩出窗口，又有了 1 个名额
```

## 2. 读题：把文字变成模型
- **实体**：`client_id`（谁在请求）、`t`（请求发生的时间，毫秒）。没有别的业务字段——这题的复杂度
  不在"数据长什么样"，而在"同一份状态在不同压力下怎么维持正确"。
- **输入长什么样**：这题不是"一批数据一次性喂进来"，而是一个类的方法调用序列（`allow`/`evict_idle`
  /`log_size`），外加一层薄的命令流协议（`LIMIT`/`ALLOW`/`CLEANUP`）给 `main()` 用。先把类的行为
  想清楚，命令流只是把类包了一层文本 I/O。
- **输出要什么**：`allow` 返回 `True`/`False`；`evict_idle` 返回清理掉的 client 数；`log_size` 返回
  当前还留着的时间戳数量（这是专门为了让 Part 2 的内存上界可以被**直接断言**而加的方法，不是产品
  需求，面试里要主动说明这一点）。
- **状态**：每个 client 一份"还在窗口里的允许时间戳"列表 + 一份"这个 client 上次看到的时间戳"（给
  Part 3 的回拨钳位用）。这决定了核心数据结构是 `dict[client_id] -> deque[int]`。
- **一句话建模**：这是一个**每个 key 维护一条滑动窗口日志（deque），四个 part 依次收紧"这条日志该
  多大、该怎么处理边界、该怎么在并发下保持正确"**的加固问题。

> [!note] 为什么选 deque 而不是继续用 list
> Part 1 用无界 `list` 记录"这个 client 允许过的所有请求"也能算对——`allow` 就是数一遍窗口里有几条。
> 但这样内存和每次调用的耗时都随请求总数无限增长。换成 `deque` 之后，"拒绝的请求不入账" +
> "每次调用先从左边弹出过期项"两条规则加在一起，能把 deque 长度死死摁在 `limit` 以内——这不是"用了
> deque 所以更快"这么简单，是这个组合本身构成了一个可以现场证明的内存上界，Part 2 要的就是这个证明，
> 不只是代码能跑。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：先写 `class RateLimiter` 的四个方法签名和 `__init__`，`allow` 里先用最笨的办法——
   一个 `list` 记时间戳，每次线性扫一遍数窗口里有几条。这一步的目的不是最终代码，是先把"窗口边界
   到底怎么定义"（左开右闭 `(t-window_ms, t]`）用这版代码跑通题面给的三个 worked example，把规则
   钉死再谈优化。
2. **Part 1 最小可用**：`count = 有多少条记录落在 (t-window_ms, t]` `if count < limit: 记录并返回
   True else 返回 False`。这一步就是把"限流"这个词翻译成一行比较。
3. **Part 2 叠加**：把 `list` 换成 `deque`，在 `allow` **和** `evict_idle` 里都先做"从左边弹出
   `<= t - window_ms` 的项"这一步，再做业务判断。`evict_idle` 复用同一套裁剪逻辑，裁剪完为空就把
   这个 client 整个从字典里删掉——这是第二个内存泄漏点（"曾经来过但再也不来的 client 永远占着一个
   字典项"），跟"单个 client 的日志无限增长"是两个独立的洞，题面专门分开点名，写的时候也分两步说。
4. **Part 3 叠加**：不写新的数据结构，只是在 `allow` 最前面插一步"把这次的 `t` 换算成 `effective_t`
   "（跟这个 client 上次看到的 `t` 取较大值），后面所有逻辑（含 Part 1/2 的窗口判断和裁剪）原封不动
   地用 `effective_t`。`limit == 0`、空字符串 client_id、超大 `t` 这几个不需要新代码，只需要在心里
   过一遍"现有逻辑会不会已经处理对了"——大部分时候答案是"对，因为字典和比较运算本来就支持这些值"。
5. **Part 4 叠加**：把 `allow`、`evict_idle`、`log_size` 三个方法体分别包进同一把 `threading.Lock`。
   不用改任何判断逻辑，只是把"读日志、裁剪、数数、决定、写回"这一整段变成一个原子操作。
6. **收尾**：三个 worked example 逐字跑一遍；把 `main()`/命令流协议补上，跑一遍空输入和格式错误行；
   检查有没有漏加锁的方法。

## 4. 代码怎么组织
```
class RateLimiter:
    __init__(limit, window_s)          # 存 limit、window_ms、_log dict、_last_seen dict、_lock
    _effective_t(client_id, t)         # Part 3 的回拨钳位，一个私有 helper
    allow(client_id, t)                # 钳位 -> 裁剪过期项 -> 判断 -> 记录，全程加锁
    evict_idle(now)                    # 对每个 client 裁剪 + 空则整体删除，全程加锁
    log_size(client_id)                # 纯读取，给测试断言内存上界用

run_commands(lines) -> list[str]        # 解析 LIMIT/ALLOW/CLEANUP 命令流，调用上面的类
main(stdin, stdout)                     # 只做 I/O
```
拆分原则：**类只对外暴露"业务动作"，不对外暴露内部数据结构**；`_effective_t` 单独抽出来，是因为它
在 `allow` 里被调用，将来如果 `evict_idle` 也要考虑回拨（本题不需要），改动只发生在一个地方。命令流
解析（`run_commands`）完全不知道类内部怎么存数据，这样"如果限流器要换成 Redis 实现"时，改动只发生在
类内部，`main()` 和命令流协议原封不动——这是这份代码在面试里最值得主动指出的一点。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：钳位 -> 裁剪 -> 判断 -> 加锁。省略 evict_idle/log_size 与命令流解析。
class RateLimiter:
    def __init__(self, limit: int, window_s: int) -> None:
        self.limit = limit
        self.window_ms = window_s * 1000
        self._log: dict[str, deque[int]] = {}       # client -> 还在窗口里的允许时间戳
        self._last_seen: dict[str, int] = {}         # client -> 上次看到的 t，给回拨钳位用
        self._lock = threading.Lock()

    def _effective_t(self, client_id: str, t: int) -> int:
        # Part 3: t 比这个 client 上次见过的还小 -> 钳位到上次的值，不抛异常
        last = self._last_seen.get(client_id)
        return t if last is None or t >= last else last

    def allow(self, client_id: str, t: int) -> bool:
        with self._lock:                              # Part 4: 整段临界区一把锁
            eff_t = self._effective_t(client_id, t)
            self._last_seen[client_id] = eff_t
            dq = self._log.setdefault(client_id, deque())
            cutoff = eff_t - self.window_ms
            while dq and dq[0] <= cutoff:              # Part 2: 每次调用先裁剪过期项
                dq.popleft()
            if self.limit <= 0 or len(dq) >= self.limit:
                return False                            # 拒绝的请求从不入账
            dq.append(eff_t)
            return True
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：`t` 是毫秒还是秒？窗口边界是左开右闭还是两头都闭？」——这题的踩坑点几乎
  全是"单位"和"边界"，开口先问比写完再改省时间。
- 写 Part 1 时：「我先用一个无界的 list 把规则写对，用样例验证窗口边界，之后再谈内存优化——先正确
  后高效。」
- 写 Part 2 时：「client 的 deque 长度不会超过 limit，因为拒绝的请求从不 append，而每次调用都会先
  把过期的弹出去——这两条规则加起来才是内存有界的证明，我加一个 `log_size` 方法方便直接断言这个
  上界。」
- 写 Part 3 时：「时钟回拨我选择钳位而不是抛异常，因为一个限流器自己变成生产事故的源头是最不该发生
  的事；`limit == 0` 是合法配置（比如运营手动掐断某个 key），不是错误输入。」
- 写 Part 4 时：「我先用一把全局锁保证整段临界区原子，这是正确性优先的选择；如果后面测出锁竞争是
  瓶颈，可以升级成 per-client 锁，但那需要额外一把锁保护字典本身的创建/删除，复杂度上升不小，值得
  先测量再决定要不要做。」
- 交付时：「三个样例都过了；并发测试断言的是恰好等于 limit，不是大概率正确，这个我特意用 exact
  assertion 验证过。」

## 7. 常见跑偏（方法层面，3 条）
- **一上来就写"优化版"，跳过朴素版**：Part 2 存在的理由是"先有一个明显正确但会漏内存的版本"，如果
  一开始就写 deque + 裁剪，反而说不清楚"为什么要裁剪"——面试官想看到你先证明规则对，再证明内存有界，
  这是两件事，不要合并成一步。
- **把"未定义行为"当成不用管的边角**：Part 3 的每一条（回拨、`limit=0`、空字符串 id、超大 `t`）都
  是题面故意留的缝——真实面试里这些不会被明确写出来，主动问、主动选一个内部一致的处理方式并说出
  理由，比"代码没崩就算过"值钱得多。
- **加锁加在错误的粒度上**：只在"读"或只在"写"周围加锁，而临界区之间还留有空隙（比如判断和写回
  分成两步、中间没锁住），会让 8 线程并发测试出现"和为 100 但单次运行结果不稳定"这种难以复现的
  bug。加锁要包住"从读到写决定"的整段逻辑，而不是包住某个单独的语句。

## 8. 同族题 / 延伸
- 同一轮里 `q23_rate_limiter` 是这题的"姊妹题"：q23 考的是换着花样加算法（滑动窗口→per-client→
  加权→token bucket），这题考的是把同一个算法做扎实（内存→边界→并发）——两题的"能力项"不同，遇到
  哪个都不要套另一个的解法结构。
- 其他轮：cd06 `suspicious_users_window` 也是"滑动窗口 + 边界钉死"的同一类模型，只是从"限流"换成
  "风控检测"这张皮；ps01 `transaction_stream_levels` 的 Part 2 是这题 Part 1 的简化版。
- 延伸思考：如果要求跨进程/跨机器共享同一份限流预算，内存里的 `deque` + `Lock` 方案就不成立了，
  需要换成 Redis + 原子脚本（Lua）来做分布式的滑动窗口计数——这是"进程内锁"和"分布式协调"两个完全
  不同量级的问题，面试官很可能会追问到这一步。
- 练习命令：`python3 loop/mock.py start cd04`
