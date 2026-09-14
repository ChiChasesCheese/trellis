# od03 · Transactional KV Store：嵌套事务栈，练的是"first-touch snapshotting"

> [!tldr]
> - 这题考的是：一个支持嵌套事务的内存 KV store——`begin`/`commit`/`rollback` 的作用域语义，是 MVCC 的一个玩具版本
> - 三步套路：先做无事务的直接读写 → Part 2 用一个"覆盖帧栈"实现嵌套事务（每层只记自己的写）→ Part 3 用 `threading.local()` 给每个线程一份独立的栈
> - 最值得带走的一个模式：**每层事务只记录自己碰过的 key 的新值，不需要额外的 undo-log**——因为"这一层的帧"本身就是"进入这层之后的全部修改"，`rollback` 直接丢弃整个帧就够了

## 类设计先定契约
```python
class TransactionalKVStore:
    def get(self, key: str) -> int | None: ...
    def put(self, key: str, value: int) -> None: ...
    def delete(self, key: str) -> None: ...
    def begin(self) -> None: ...       # 开启一层（可能嵌套的）事务作用域
    def commit(self) -> bool: ...      # 没有活跃事务返回 False，不抛异常
    def rollback(self) -> bool: ...    # 同上
```
**不变量（写代码前先想清楚）**：
1. 没有 `begin()` 时，`put`/`delete`/`get` 直接读写全局状态；`commit`/`rollback` 返回 `False`。
2. `begin()` 内的写操作，对同一事务、同一线程内更晚的读立即可见，但不影响全局状态，也不影响其他线程。
3. `commit()` 把最内层事务的修改合并进**上一层**（不是直接落到全局），只有最外层的 `commit()` 才真正
   写入全局状态——N 层嵌套需要 N 次 `commit()` 才能持久化。
4. `rollback()` 只撤销最内层事务自己做的修改，回到该层 `begin()` 之前的状态。
5. `delete` 之后再 `get` 和"从未存在"不可区分，都是 `None`。

## 1. 题目在说什么（人话版）
一个内存 KV store 支持嵌套事务：`begin()` 开一层作用域，这一层里的 `put`/`delete` 只在这一层和更深
层可见；`commit()` 把这层的修改并入上一层（外层事务或全局状态）；`rollback()` 把这层的修改整体丢弃。
Part 3 让多个线程各自拥有独立的事务栈，互不干扰，直到某个线程真正 `commit` 到全局。

三行小例子：
```
put(a,1); begin(); put(a,2); get(a)   -> 2 (读到本层的写)
begin(); delete(a); get(a)             -> None (更内层看到自己的删除)
rollback(); get(a)                     -> 2 (回到上一层的状态)
```

## 2. 读题：把文字变成模型
- **实体**：全局状态（`dict[str,int]`）、每层事务的"覆盖帧"（这一层自己碰过的 key 极其新值）。
- **输入长什么样**：`main()` 命令流 `GET/PUT/DELETE/BEGIN/COMMIT/ROLLBACK`。
- **输出要什么**：`GET` 输出值或 `None`；`COMMIT`/`ROLLBACK` 输出 `True`/`False`；其余无输出。
- **状态**：一个全局字典 + 一个"帧栈"（每个元素是一层事务自己的写记录，用一个哨兵值表示"这个 key
  被删除了"）；Part 3 里这个帧栈要按线程隔离。
- **一句话建模**：这是一个 **按嵌套深度叠加的覆盖层**——读操作从最内层往外找第一个命中的记录，
  `commit` 把最内层合并进上一层,`rollback` 直接丢弃最内层。

> [!note] 为什么选这个数据结构
> 不需要为每个 key 维护"历史值列表"（undo-log 式），因为一层事务帧本身就是"进入这层之后所有写操作
> 的最终结果"——同一 key 在这层内被反复 `put`/`delete`，帧里只留最后一次的值,`rollback` 时整层丢弃
> 就自动撤销了这个 key 在这层的全部修改，不需要逐次撤销。这正是"first-touch snapshotting"的意义：
> 帧只关心"这个 key 在这层的最终状态"，不关心它在这层被改了几次。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：先写 `__init__` 的字段（全局字典、帧栈），六个方法签名和 docstring 过一遍——尤其是
   `commit`/`rollback` 在"无活跃事务"时返回 `False` 而不是抛异常，这个契约要先写清楚。
2. **Part 1 最小可用**：不涉及帧栈，`get`/`put`/`delete` 直接操作全局字典；`begin`/`commit`/`rollback`
   先只处理"没有事务"的退化情况。
3. **Part 2 叠加**：`begin()` 往栈里 push 一个空字典（帧）；`put`/`delete` 有帧就写最内层帧（用哨兵
   值表示删除），没帧才落全局；`get` 从最内层帧开始由内向外找,都没有才查全局；`commit()` 弹出最内层
   帧，有上一层就 `dict.update` 合并进去，没有就真正写入全局；`rollback()` 直接弹出丢弃最内层帧。
4. **Part 3 叠加**：把帧栈从"实例的一个属性"换成 `threading.local()`，让每个线程拿到自己独立的栈；
   全局字典的读写包一把锁,保证跨线程的最终提交是原子的。
5. **收尾**：用来源原文给的嵌套例子逐步手算验证；`commit`/`rollback` 在无事务时不抛异常这条边界要
   显式测。

## 4. 代码怎么组织
```
TransactionalKVStore.__init__      # 全局字典 + 全局锁 + threading.local() 帧栈
_stack() -> list[dict]              # 取当前线程的帧栈（懒初始化）
get/put/delete(...)                 # 有帧写/读最内层帧，否则落/查全局（全局访问加锁）
begin()/commit()/rollback()         # push/合并弹出/丢弃弹出
main(stdin, stdout)                 # 解析命令流，分发，格式化输出
```
`_stack()` 是整个类唯一"知道帧栈存在 `threading.local()` 里"的地方，其余方法只管"当前帧栈"这个抽象，
这样从单线程版本升级到 Part 3 的多线程版本，只需要改 `_stack()` 的实现，不需要碰六个公开方法的逻辑。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
_DELETED = object()                    # 哨兵：表示这个 key 在本层被删除

class TransactionalKVStore:
    def __init__(self):
        self._global = {}
        self._global_lock = threading.Lock()
        self._local = threading.local()  # 每线程独立的帧栈

    def _stack(self):
        stack = getattr(self._local, "stack", None)
        if stack is None:
            stack = []
            self._local.stack = stack
        return stack

    def get(self, key):
        for frame in reversed(self._stack()):   # 由内向外找第一个命中的帧
            if key in frame:
                v = frame[key]
                return None if v is _DELETED else v
        with self._global_lock:
            return self._global.get(key)

    def put(self, key, value):
        stack = self._stack()
        if stack:
            stack[-1][key] = value               # 只写最内层帧
        else:
            with self._global_lock:
                self._global[key] = value

    def begin(self):
        self._stack().append({})

    def commit(self):
        stack = self._stack()
        if not stack:
            return False
        frame = stack.pop()
        if stack:
            stack[-1].update(frame)              # 合并进上一层，非最外层不落全局
        else:
            with self._global_lock:
                for k, v in frame.items():
                    if v is _DELETED:
                        self._global.pop(k, None)
                    else:
                        self._global[k] = v
        return True

    def rollback(self):
        stack = self._stack()
        if not stack:
            return False
        stack.pop()                              # 整层丢弃，不需要逐次撤销
        return True
```

## 6. 并发追问怎么答
- **同一 key 被两个线程并发 `put` 又 `commit`，最终值是谁的**：last-committer-wins——谁的 `commit`
  把修改写入全局状态发生在后面，谁的值就是最终值；用一把保护"合并进全局状态"这一步的锁保证提交本身
  是原子的，不会出现两个线程同时写导致的数据竞争。
- **first-touch snapshotting 需不需要为同一 key 存多份 undo 记录**：不需要——帧本身就是"这个 key 在
  这一层的最终值"，同一 key 在这层被写 100 次，帧里也只留最后一次的值，`rollback` 整层丢弃即可正确
  撤销全部 100 次写，不需要逐次记录历史。
- **如果要支持跨线程共享同一个嵌套事务，线性一致性还成立吗**：这需要把事务边界的加锁范围扩大到跨越
  多次方法调用（长事务持锁），会带来吞吐下降和潜在死锁问题——可以指出这是一个开放式权衡，没有标准
  答案，但要点明"跨线程共享事务"和"每线程独立事务栈"在锁粒度上的本质区别。

## 7. 常见跑偏（方法层面，3 条）
- **`commit()` 把最内层事务的修改直接落到全局状态**：忘记"只有最外层的 commit 才真正持久化"这条
  规则，嵌套事务的 `commit` 应该合并进上一层帧，用来源给的多层嵌套例子（例3）能直接测出这个坑。
- **`rollback` 试图逐条撤销记录的每一次写（真正的 undo-log）**：不必要地复杂,且容易在"同一 key 被
  反复写"的场景下漏掉撤销顺序；帧本身天然只保留最终值，直接丢弃整个帧就是正确的 rollback。
- **`delete` 用 `del frame[key]` 而不是写入哨兵值**：如果外层帧或全局里已经有这个 key 的旧值，
  `del` 只是让这一帧对这个 key "没有记录"，读操作会继续往外层找到旧值——必须显式写入 `_DELETED`
  哨兵，让"删除"本身成为这一层的一条记录。

## 自测清单
- 无事务时 `commit`/`rollback` 返回 `False`，不抛异常。
- `get` 未 `put` 过的 key 和已 `delete` 的 key 都返回 `None`。
- 事务内 `delete` 一个"外层刚 put 但未提交"的 key，`rollback` 后恢复到外层那次 put 的值。
- 深度 ≥3 的嵌套，每层写不同 key，`rollback` 中间层不影响更外层已做的修改。
- 同一 key 同一事务内反复 `put`/`delete`，`rollback` 只需恢复到进入这个事务之前的值。
- 多线程各自开独立事务、写不相交 key 集合，最终全局状态是所有提交的并集。
- 1e5 次混合操作、嵌套深度不超过操作数，2s 内完成。

## 相关题与 skills id
- skills: **S09**（类设计先定契约，`commit`/`rollback` 布尔返回值 vs 异常的取舍）· **S10**
  （并发正确性：每线程事务栈、first-touch snapshotting、线性一致读）· S11（间接，undo-log 与
  WAL 思路相通）。
- 同族：`od02_in_memory_file_system` 的"结构锁 vs 内容锁分离"和本题"per-thread 栈 vs 全局锁"是同一
  方法论——把"不需要跨线程共享的状态"隔离到线程本地，只在真正需要共享的边界加锁。
- 练习命令：`python3 loop/mock.py start od03`
