# cd03 · AccountScheduler：一个类里的"能不能用 → 借给谁 → 该借给谁"，练的是接口先行的类设计

> [!tldr]
> - 这题考的是：把"沙盒账号池"设计成一个类，三个方法层层递进——查询可用性、按 id 加锁、按 LRU 自动挑一个可用的
> - 三步套路：先把 `__init__` 的状态字段和三个方法的签名写全（一行都不填实现）→ 用两个 dict 跑通 Part 1/2 → Part 3 只加一个"排序 key"，不建新状态
> - 最值得带走的一个模式：**接口先行**——类设计题里，先把"这个类有几个状态字段、每个方法收什么吐什么"写成骨架并过一遍脑子里的用例，比直接下手写 `__init__` 的 body 更不容易返工

## 1. 题目在说什么（人话版）
Stripe 内部测试环境有一小撮沙盒账号，多个集成任务会借来借去。一个任务可能问"账号 a 现在能用吗"，
可能"把账号 a 锁 10 秒"，也可能懒得指定账号，直接说"随便给我一个能用的"——这时候调度器要挑
**最久没被用过的那个**，让账号池负载均匀，不会总是同一个账号被反复征用。

账号池在一开始就是固定的（构造函数传进来，不会中途新增），这一点很关键：它把这道题从"一条事件流上滚动统计"
的题型，变成了一道**类设计**题——面试官想看的是一份干净的状态（一个 dict 就够）、一套说得清楚的异常策略、
以及从"能不能用" → "帮我锁上" → "帮我选一个"这条清晰的推导链。

三行小例子：
```
ACCOUNTS a b
ACQ a 0 10      -> true     (锁住 a：[0, 10) 这段时间)
ANY 5 10        -> b        (a 还锁着；b 从没被用过，直接选它)
```

## 2. 读题：把文字变成模型
- **实体**：只有"账号"一个实体，用字符串 id 表示。没有用户、没有金额，状态比数据流题目还要少。
- **输入长什么样**：类本身没有"输入"，只有方法调用；命令流版本的 `main()` 才有输入行——第一行
  `ACCOUNTS a b c`（构造顺序，即 LRU 的 tie-break 顺序），后面每行是 `AVAIL/ACQ/ANY` 命令。
- **输出要什么**：三个方法各自返回 `bool` / `bool` / `str|None`；命令流版本把它们分别渲染成
  `true|false` / `true|false` / `<id>|none`，格式在题面里钉死，不用自己猜。
- **状态**：整个类只需要两个 dict——`locked_until[account_id] -> t`（账号解锁的时刻）和
  `last_used[account_id] -> t`（上一次**成功** `acquire` 的时刻）。没有历史记录，没有队列，就两个映射。
- **一句话建模**：这是一个 **围绕两个 dict 的类设计问题**——`is_available` 只读它们，`acquire` 只写它们，
  `acquire_any` 只是"先按一个排序 key 挑一个 id，再调用同一条写入路径"。

> [!note] 为什么选这个数据结构
> 候选方案是"给每个账号维护一个锁事件列表"，但题面已经说死"只关心当前是否被锁、和上次用的时间"，不需要历史，
> 所以两个 dict（值覆盖写）就够，比列表省事也省状态。LRU 的 tie-break 用一个"构造顺序"表（`id -> 下标`）
> 而不是排序 id 字符串，因为题面明确说了顺序来自 `accounts` 参数，不是字母序——这个表在 `__init__` 里建一次，
> 之后 O(1) 查。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行，不写 body**：先把 `__init__` 的参数和要存的字段列出来（哪怕先只写注释），再把三个方法的
   签名和 docstring 抄一遍——"这个方法收什么、吐什么、什么时候抛异常"用一句话写在 docstring 里。此时代码
   跑不起来（`raise NotImplementedError`），但类的骨架已经和题面的三个 Part 一一对应了。
2. **Part 1 最小可用**：填 `is_available`——查 id 合法性（不合法 `KeyError`），查 `locked_until`，
   `t >= end` 就是可用。立刻拿题面样例的几个边界点（锁的起点、终点前一秒、终点）手动跑一遍。
3. **Part 2 叠加**：`acquire` 先检查 `duration <= 0`（这一步在检查 id 之前，因为它是纯参数校验，不需要碰状态），
   再调用刚写好的 `is_available` 判断能不能锁，能锁就写两个 dict。
4. **Part 3 叠加**：`acquire_any` 不新建任何状态——先用 `is_available` 过滤出候选，按"没用过的排前面、
   用过的按 `last_used` 升序，同分按构造顺序"这个 key 选一个，然后**复用 Part 2 里写状态的那两行**去锁它。
5. **收尾**：把命令流的 `main()`/`run_commands` 包一层——它只做"解析一行、调类方法、把结果/异常渲染成一行输出"，
   不应该有任何业务判断跑到这一层来。

## 4. 代码怎么组织
接口先行是这题的核心方法论，具体到代码上，就是**在填任何一行实现之前，先把这份骨架写出来**：
```python
class AccountScheduler:
    def __init__(self, accounts: list[str]) -> None: ...      # 存哪些状态？
    def is_available(self, account_id: str, t: int) -> bool: ...
    def acquire(self, account_id: str, t: int, duration: int) -> bool: ...
    def acquire_any(self, t: int, duration: int) -> str | None: ...
```
写这份骨架时问自己两个问题："每个方法的输入输出类型是什么"（决定了签名和 docstring）、
"这个方法会不会修改状态、修改哪个字段"（决定了 `__init__` 里到底要几个字段）。这道题的答案很干净：
只读的方法（`is_available`）不动状态，只写的路径（一次成功的锁）只动 `locked_until` / `last_used` 这两行，
于是自然而然地把这两行提成一个私有方法 `_lock`，`acquire` 和 `acquire_any` 末尾都调它——**后一个 Part
复用前一个 Part 的写状态逻辑**，而不是各写一份。命令流解析（`run_commands`/`main`）完全在类外面，
只做"读一行 → 调方法 → 把返回值或异常渲成一行字符串"，这样类本身可以脱离 stdin/stdout 单独单测，
也是这题告诉你的一个更通用的道理：**类设计题里，I/O 层和业务类要分开，业务类不知道自己在被命令行调用还是被单测调用**。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：状态字段 → 三个方法 → 共用的写入路径。省略参数解析、main() 的行级 try/except。
class AccountScheduler:
    def __init__(self, accounts: list[str]) -> None:
        self._order = {aid: i for i, aid in enumerate(accounts)}   # id -> 构造顺序，LRU tie-break
        self.locked_until: dict[str, int] = {}   # account_id -> 解锁时刻（独占区间右端点）
        self.last_used: dict[str, int] = {}      # account_id -> 上一次成功 acquire 的时刻

    def _lock(self, account_id, t, duration):    # acquire / acquire_any 共用的写入路径
        self.locked_until[account_id] = t + duration
        self.last_used[account_id] = t

    def is_available(self, account_id, t):
        if account_id not in self._order:
            raise KeyError(account_id)
        end = self.locked_until.get(account_id)
        return end is None or t >= end            # 没锁过，或锁的右端点已经到了

    def acquire(self, account_id, t, duration):
        if duration <= 0:
            raise ValueError("duration must be > 0")   # 先校验参数，不碰状态
        if not self.is_available(account_id, t):       # 顺带做了 id 合法性检查
            return False
        self._lock(account_id, t, duration)
        return True

    def acquire_any(self, t, duration):
        if duration <= 0:
            raise ValueError("duration must be > 0")
        candidates = [a for a in self._order if self.is_available(a, t)]
        if not candidates:
            return None
        key = lambda a: (a in self.last_used, self.last_used.get(a, 0), self._order[a])
        chosen = min(candidates, key=key)          # 没用过的排前面，其次最久没用，再其次构造顺序
        self._lock(chosen, t, duration)
        return chosen
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认一下：锁的区间是 `[t, t+duration)`，右端点是独占的，也就是 `t+duration` 那一刻账号已经
  空出来了；如果定义不同我改一处判断。」
- 写 `__init__` 时：「我这里就用两个 dict，一个记解锁时刻，一个记上次使用时刻，没有历史需要保留，所以不用
  列表或队列。」
- 写 `acquire` 时：「`duration <= 0` 我放在最前面校验，因为它是纯参数问题，不需要先查这个账号存不存在——
  两种顺序都说得通，但我选了这个并且会在注释里写清楚，保证所有方法都统一。」
- 写 `acquire_any` 时：「选择逻辑我写成一个排序 key，三层优先级对应题面的三条规则；选完之后我直接复用
  `acquire` 里写状态的那两行，不重复一遍逻辑。」
- 如果面试官追问"现在 `acquire_any` 是不是每次都要扫一遍全部账号，能不能优化到 O(log n)"：先口头确认
  当前规模下 O(pool size) 完全够用，然后讲思路——维护一个按 `last_used` 排序的堆存"已用过的账号"，
  加锁时不真的删堆里的元素，而是靠一个版本号做懒失效，取的时候弹到版本号匹配的元素为止；"没用过的账号"
  单独排队，永远优先出。**先讲清楚这个思路要解决什么问题、数据结构怎么配合，再问面试官要不要现场写**——
  60 分钟的题不主动把一个正确、够用的方案推翻重写。
- 交付时：「三个样例都过了；如果要支持 `release(id)` 提前解锁，我会加一个新方法，但不会去动
  `last_used`——提前释放不等于"被使用过"，这个点我在设计的时候特意留意了。」

## 7. 常见跑偏（方法层面，3 条）
- **没有先写接口就直接填 `__init__` 的 body**：容易一上来就把"排序用的表"和"锁状态"混在一个 dict 里，
  等写到 Part 3 发现要额外记"构造顺序"时才回头改 `__init__`，浪费时间还容易漏改其他方法。先把三个方法的
  签名和状态字段列全，再动手写实现，返工成本低得多。
- **`acquire_any` 重新写一遍加锁逻辑**，而不是调用 `acquire` 已经验证过的写入路径：两份逻辑不同步，后面
  改一处漏一处（比如以后要加"上锁时顺带记一个原子计数器"，只改了一处）。选出账号之后，锁它这件事应该
  只有一条代码路径。
- **把命令流解析里的判断逻辑塞进类的方法里**（比如在 `acquire` 里处理"非法命令行"的情况）：类应该只知道
  "账号 id、时间戳、时长"这几个合法类型的参数，格式错误、动词识别不了这些属于 I/O 层的事，写在 `main()`
  或 `run_commands` 里，不要让业务类关心"我是被命令行调的还是被单测调的"。

## 8. 同族题 / 延伸
- OA 侧：`problems/q26_account_scheduler_lru` 是同一个题面的 OA 变体——动态 `ADD`/`RELEASE`、布尔哨兵
  代替异常、id 字母序代替构造顺序做 tie-break。两题的契约刻意不同，别把 q26 的解法直接搬过来。
- 类设计的同族模式：任何"查询状态 → 修改状态 → 按规则自动挑一个目标去修改状态"的题（比如连接池、
  限流器、会话管理器）都是这道题的换皮版本，核心都是先把状态字段和方法签名想清楚。
- 延伸思考：如果账号池要支持运行时增删（变回 q26 那种 `ADD`），"构造顺序"这个 tie-break 就失去意义了，
  需要换成一个单调递增的"首次注册序号"，而不是死记当前列表的下标——这也是面试官常问的追问之一。
- 练习命令：`python3 loop/mock.py start cd03`
