# CODE_GUIDE — confmgr

给第一次读并发 Python 代码的人看的导览。讲代码在做什么、模块怎么互相调用、以及并发代码里最容易想岔的几个点。
**不讲这道题的 bug 在哪** —— 那是练习本身要你去找的东西。

## 数据流

```
                          ┌─────────────────┐
  dict (代码里写死)  ───▶ │                  │
  JSON 文件          ───▶ │   layers.py      │  每层各自的 load_*() 函数，
  os.environ 里一段前缀 ─▶ │  (纯函数，无状态)  │  互不知道对方存在
                          └────────┬─────────┘
                                   │ 四层数据（dict）
                                   ▼
                          ┌──────────────────┐
                          │   manager.py     │  ConfigManager：按优先级
                          │  ConfigManager   │  合并四层，暴露 get()/reload()
                          └────────┬─────────┘
                                   │ get(key) 先问缓存，缓存没有才去查四层
                                   ▼
                          ┌──────────────────┐
                          │    cache.py      │  TTLCache：key -> (value, 过期时间)，
                          │    TTLCache      │  所有读写都要拿 self._lock
                          └──────────────────┘
                                   │
                                   ▼
                          调用方（多个线程同时调 get()）
```

一次 `config.get("timeout")` 调用的路径：`ConfigManager.get` → `TTLCache.get_or_compute` →（缓存
没命中才会走到这一步）`ConfigManager._resolve` → 依次查 overrides → env → file → defaults，返回
第一个命中的层。`reload()` 是另一条独立路径：只重新读 file 层和 env 层（覆盖层和 defaults 层本来
就在内存里，不需要"重新读"）。

## 逐模块

### `layers.py` — 两个装载函数
- `load_file_layer(path)`：读一个 JSON 文件，返回其中的 dict；文件不存在就返回 `{}`（配置文件是
  可选的，机器还没配置过也应该能正常启动）。
- `load_env_layer(prefix)`：遍历 `os.environ`，挑出以 `prefix` 开头的 key，去掉前缀后放进一个
  dict 里返回。
- 这两个函数都是**无状态的纯函数**：给定输入，输出完全确定，不保留任何调用之间的记忆。它们不知道
  `ConfigManager` 的存在，也不知道"这是不是第一次读"——每次调用都是从头读一遍。

### `cache.py` — `TTLCache`
一个"记住结果一段时间"的小工具，被 `ConfigManager` 用来避免每次 `get()` 都重新走一遍四层查找。

- `_store` 是一个普通 dict：`key -> (value, 过期的绝对时间戳)`。
- `get(key)` / `set(key, value)` / `invalidate(key)` / `clear()`：基本的读写操作，每个都在
  `self._lock` 保护下访问 `_store`。
- `get_or_compute(key, factory)`：这是 `ConfigManager.get()` 实际调用的入口——"如果缓存里有就直接
  返回，没有就调 `factory()` 算一个新值、存起来、再返回"。`factory` 在这里就是"去四层里查这个
  key"这件事本身（一个不接受参数的函数，调用时才真正执行查找）。

### `manager.py` — `ConfigManager`
把上面两个模块粘合成一个 API。

- `__init__`：接收 defaults dict、可选的文件路径、可选的环境变量前缀，构造出四层里的其中两层
  （file、env）+ 把另外两层（defaults、overrides）直接存成实例属性；再建一个 `TTLCache`。
- `get(key, default=None)`：调 `self._cache.get_or_compute(key, lambda: self._resolve(key))`。
- `set_override(key, value)` / `clear_override(key)`：改 `self._overrides`（自己有单独的
  `_overrides_lock` 保护），然后把这个 key 的缓存失效掉（`cache.invalidate`），这样下一次
  `get()` 会重新走 `_resolve`，看到最新的 override。
- `reload()`：重新调用 `layers.py` 里那两个装载函数，把 `self._file_layer` / `self._env_layer`
  换成新读到的内容。
- `_resolve(key)`：按 overrides → env → file → defaults 的顺序查一遍，谁先命中用谁；四层都没有
  就返回一个内部哨兵值 `_MISSING`（`get()` 再把它翻译成调用方传的 `default`）。

## 读并发代码时容易误解的地方

这几点不是这道题专属的坑，是读任何 Python 并发代码之前都该先弄清楚的机制。

**1. GIL 不等于"这段代码是原子的"。** CPython 的全局解释器锁（GIL）保证任意时刻只有一个线程在执行
Python 字节码，很多人因此以为"反正同一时间只有一个线程在跑，我的代码肯定不会被打断"。但 GIL 只保证
**单条字节码指令**内部不会被打断，两条语句之间——甚至一条 Python 语句翻译出的多条字节码指令
之间——解释器随时可能把执行权切给另一个线程。`if key not in cache: cache[key] = value` 看起来是
一行代码，但它是"读一次 dict、判断、（可能）写一次 dict"三个独立的字节码操作，中间随时可能插入
另一个线程的完整执行。GIL 保护的是解释器自己的内部状态不被搞坏（不会导致 dict 内部数据结构损坏），
不保护你写的业务逻辑的"读了就一定还是刚才读到的那个值"这种假设。

**2. `with lock:` 保护的是"锁被持有期间"，不是"这个函数名字听起来相关的所有代码"。** 一个方法内部
如果分成两段分别 `with self._lock:`，两段之间没有锁——另一个线程完全可以在两段中间插进来，把状态
改成第一段读到之后、第二段写入之前完全不一样的样子。锁的范围（多大一段代码被同一次 `with` 包住）
和锁本身"有没有加"同样重要。

**3. `threading.Lock` 不可重入。** 同一个线程如果在已经持有某把 `Lock` 的情况下再次 `acquire()`
同一把锁，会直接死锁（自己等自己释放，永远等不到）。需要"同一线程可以重复拿"的场景要用
`threading.RLock`，两者不能随便互换。

**4. 一个方法调另一个"看起来只是读"的方法，不代表两次调用之间状态没变。** 比如某个方法先调用
`self.get(x)`（内部拿了一次锁、读、放锁），再做一些计算，再调用 `self.set(x, ...)`（内部又拿了
一次锁、写、放锁）——这是两次独立的加锁-解锁，而不是一次连续的临界区。两次调用之间，锁是完全释放
的，其他线程可以自由进出。

**5. `threading.Barrier(n)` 是用来做确定性测试的工具，不是业务代码里常见的东西。** 它会让每个
调用 `.wait()` 的线程都阻塞，直到凑够 `n` 个线程一起到达才同时放行——测试用它来强制"两个线程几乎
同时开始做某件事"，让原本依赖操作系统调度、时快时慢的竞争条件变成每次运行都一样的结果，而不是需要
反复运行赌运气。

---
练到第二遍就别再看这份指南了——真实面试现场没有人会给你一张"这个模块负责什么"的说明书。
