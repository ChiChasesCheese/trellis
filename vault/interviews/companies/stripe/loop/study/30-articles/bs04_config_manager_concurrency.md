# bs04 · confmgr：缓存踩踏 + reload 后读到旧值，练"先让并发 bug 稳定复现，再谈定位"

> [!tldr]
> - 这轮考的不是"你能不能一眼看出锁加在哪"，是能不能先**把一个并发 bug 变成确定性复现**，再用
>   跟单线程题一样的"读断言 → 假设 → 验证"套路去定位
> - 三步套路：确认失败测试是不是"用 `Barrier`/足够长的 `sleep` 强制出来的确定性失败"（不是靠
>   运气）→ 读失败断言判断是"竞态"还是"该重置没重置" → 数清楚"锁住的是哪一段代码"和"哪个字段
>   该在哪个时机重置"
> - 最值得带走的一个信号：**"两个分别加锁的操作拼在一起" ≠ "一个加锁的操作"**——中间那段没锁的
>   缝隙，就是竞态活着的地方

## 1. 题目在说什么
`confmgr` 是一个线程安全的分层配置管理器：`get(key)` 按 defaults < file < env < 运行时 override
的优先级合并四层，结果放进一个 TTL 缓存里避免每次都重新查四层；`reload()` 可以在不重启进程的情况
下重新读 file/env 两层。它被设计成"多个线程同时调 `get()`，另一个后台线程定时调 `reload()`"这种
场景。两条 issue：

```
Bug report 1 — 并发下同一个 cache key 被解析了不止一次
> 两个线程同时对同一个还没缓存过的 key 调用 cache.get_or_compute("k", factory)，
> factory 耗时足够长，两个线程"几乎肯定"都会看到 miss。期望 factory 只跑一次，
> 实际是每个先到的线程都跑了一次。

Bug report 2 — reload() 之后 get() 还是返回旧值，直到 TTL 自然过期
> get(key) 让它进缓存，改配置文件，调 reload()，TTL 还没到就再 get() 同一个 key，
> 期望拿到新值，实际拿到 reload 之前的值。
```

Bug 1 是竞态，Bug 2 是"该重置没重置"——两者都属于 `LOOP_GUIDE.md` §4 里明确点名的并发 bug 家族。

## 2. 读库：3 分钟摸清结构
1. **README 的 Layout**：`layers.py`（两个无状态的纯函数装载器）→ `cache.py` 的 `TTLCache`
   （`get`/`set`/`invalidate`/`get_or_compute`）→ `manager.py` 的 `ConfigManager`（把四层 +
   `TTLCache` 粘成一个 `get()`/`reload()` API）。
2. **一次 `get()` 的路径**：`ConfigManager.get` → `TTLCache.get_or_compute` → 缓存没命中才走
   `ConfigManager._resolve`（依次查 overrides → env → file → defaults）。`reload()` 是独立
   路径：只重新读 file/env 两层。
3. **跑测试**：`python -m pytest tests -q`，25 个测试，2 红——分布在 `test_cache.py`（并发那个）
   和 `test_manager.py`（reload 那个）。

## 3. 下手顺序（面试里就按这个来）
1. **先确认失败测试是不是"确定性"的，不是"偶尔"的**：读
   `test_get_or_compute_calls_factory_at_most_once_under_concurrent_misses` 的代码，会看到
   `factory` 里有一个 `time.sleep(0.2)`（远大于任何调度抖动），加上一个 `threading.Barrier(2)`
   逼两个线程同时开始——这是**故意设计成每次跑都必现**的，不是"运气不好才复现"。这一步很重要：
   如果你怀疑一个并发测试是 flaky 的，先看它有没有 `Barrier`/够长的 `sleep`/`Event` 这类同步
   原语，有就说明作者已经替你把不确定性去掉了，不需要重复跑几十次去赌。
2. **读失败断言，判断是竞态还是状态残留**：`AssertionError: factory should run exactly once
   per miss, ran 2 time(s)` —— 这是"本该只发生一次的副作用发生了多次"，典型竞态信号。
   `assert 'hi' == 'bonjour'` —— 这是"该更新的没更新"，典型状态残留信号。
3. **对竞态类：数清楚"哪几行代码之间没有锁"**：读 `get_or_compute`，发现它是
   `self.get(key)`（自己加锁解锁）→（不加锁的 `factory()`）→ `self.set(key, ...)`（自己加锁
   解锁）三段拼起来的——**两个独立加锁的操作 ≠ 一个加锁的操作**，中间这段没锁的空隙就是两个线程
   都能看到"miss"的地方。
4. **对状态残留类：用一个不涉及缓存的测试排除嫌疑**：`test_reload_replaces_env_layer_contents`
   直接读 `mgr._env_layer`，绕开 `get()`/缓存，这条测试是绿的——说明 `reload()` 本身确实把
   layer 数据换成新的了，问题出在"layer 换了之后，缓存没有跟着失效"这一步。
5. **假设，然后验证**：竞态类的假设可以直接从"读代码数出没锁的缝隙"得出，不需要额外打印；状态
   残留类同理——`reload()` 里搜一下有没有调用 `self._cache.clear()`，没有就是缺的那一步。
6. **最小修复 + 回归**：这题两个 bug 分别是"把三段拼接改成一次加锁"和"加一行 `cache.clear()`"，
   改完重跑全部 25 个，再把整个套件**连续跑几十次**确认不是"改完这次凑巧过了"。

## 4. 调试工具怎么用
并发 bug 的调试工具跟单线程题不太一样，pdb 命令表见
`loop/rounds/04_bug_squash/DEBUG_101.md`，这里只说这道题该怎么用——`pdb` 在多线程场景下并不
好用（断点会让其中一个线程停下但另一个线程照样跑），更有效的手段是：

- **先看测试怎么强制复现，再决定要不要自己加断点**：这道题的失败测试已经用 `Barrier` + 足够长
  的 `sleep` 把交错方式钉死了，读测试代码本身就是最快的"复现路径"，不需要你自己再想办法制造
  竞态。
- **`print` 到 stderr，标注线程名**：如果需要看两个线程各自的执行顺序，
  `print(f"{threading.current_thread().name} {...}", file=sys.stderr)` 比断点更实用——断点会
  改变调度时机，反而可能让原本必现的竞态变得不必现。
- 改完用 `pytest tests -q --lf` 先看两个失败的是否变绿，再用一个循环把整个套件连续跑
  20 遍（`for i in $(seq 20); do pytest tests -q || break; done`），确认修复后不是"偶尔通过"。

## 5. 本题两个 bug 的排查实录

**Bug 1 — `get_or_compute` 是两个分别加锁的操作拼起来的（竞态/缓存踩踏）**
- 现象：`test_get_or_compute_calls_factory_at_most_once_under_concurrent_misses` 报
  `factory` 跑了 2 次而不是 1 次。
- 定位路径：读测试的 docstring，先搞清楚 `Barrier(2)` + `sleep(0.2)` 是为了让两个线程"确实"
  同时看到 miss，不是巧合。再读 `get_or_compute`：`self.get(key)`（拿锁、查、放锁）→
  没加锁的 `factory()` → `self.set(key, value)`（拿锁、写、放锁）。两个线程都在第一步看到
  `None`（都还没人写过），都往下走到 `factory()`，都各自睡 0.2 秒，最后各自 `set` 一次——`
  factory` 因此被调用了两次。
- 根因分类：**竞态（check-then-act 被拆成了两次独立的加锁操作）**——`self._lock` 本身没写错，
  问题是它保护的范围太窄，"检查"和"写入"之间空出了一段没有锁的时间。
- 修复：把"查缓存、miss 就调 factory、把结果存回去"这一整段收进**同一次** `with self._lock:`，
  让第二个线程进来时能看到第一个线程已经算好并存下的结果，不用重复调用 `factory`。

**Bug 2 — `reload()` 换了 layer 数据，但没让缓存失效（跨调用残留状态）**
- 现象：`test_reload_picks_up_new_file_contents_immediately` 报 `'hi' == 'bonjour'` 失败——
  拿到的是旧值。
- 定位路径：先看 `test_reload_replaces_env_layer_contents`（绕开缓存直接读 `mgr._env_layer`）
  是绿的——这条测试排除了"`reload()` 没有正确重新读文件/环境变量"这个可能性，把范围缩小到
  "layer 数据换了，但下一次 `get()` 没有感知到"。读 `reload()` 的实现：只调用两个
  `load_*_layer()` 函数换掉 `self._file_layer`/`self._env_layer`，从头到尾没碰
  `self._cache`。
- 根因分类：**跨调用残留状态**——缓存里的旧结果是 `reload()` 之前算出来的，`reload()` 这个
  "应该让状态焕然一新"的方法，忘了清掉一份跟它相关的旧状态（缓存）。
- 修复：一行，`reload()` 结尾加 `self._cache.clear()`。

**一个可迁移的信号**：并发场景下，"某个本该只发生一次的副作用发生了不止一次" → 先怀疑
check-then-act 被拆成了两次独立加锁的操作，去数"检查"和"写入"之间有没有锁；"某个生命周期事件
（reload/reset/close）之后，某个旧状态还在生效" → 去看这个方法有没有漏掉一个"本该跟着清空/重置"
的字段——这条信号在单线程题（`bs03` 的 `Parser.parse()` 忘记重置游标）和这里的并发题
（`reload()` 忘记清缓存）里是同一个根因家族，只是并发场景下更容易被放大成"看起来像竞态"的现象。

## 6. 面试里怎么说
- 看到 `Barrier`/`sleep` 先说清楚它们的作用：「这个测试用 `Barrier(2)` 强制两个线程同时开始，
  `sleep(0.2)` 保证两个线程都会看到 miss——这是让竞态每次都必现的写法，不是巧合，我不会去改动
  这两行。」
- 讲 bug 1 时说清楚"为什么两次加锁不等于一次加锁"：「`get` 和 `set` 各自是安全的，但拼在一起用
  的时候，中间那段没锁的空隙就是竞态活着的地方——修复是把整个检查+计算+写入收进同一次加锁，而
  不是在 `ConfigManager` 那一层再包一把更粗的锁。」
- 讲 bug 2 时说清楚定位依据：「`test_reload_replaces_env_layer_contents` 已经证明 `reload()`
  本身没问题，所以我去找'换完 layer 之后还差什么一步'，而不是怀疑 `_resolve` 的优先级逻辑。」
- 交付时说明验证方式：「两个 bug 分别改了一个方法和加了一行，我把整个套件连续跑了几十遍确认
  不是碰巧一次通过——并发 bug 修完之后光跑一次绿是不够的。」

## 7. 常见跑偏
- **在 `ConfigManager` 那一层再包一把更粗的锁，而不是修 `TTLCache.get_or_compute` 本身**：这样
  能让这个测试过，但 `TTLCache` 本来是设计成"自己就该是线程安全的"，只在一个调用方那里打补丁，
  下一个用到 `TTLCache` 的地方还是会踩同样的坑。
- **用缩短 TTL 来"修" bug 2**：让这一条测试的具体数字凑巧过了，但"reload 之后要等自然过期"这个
  根本问题对任何比这个 TTL 长的场景依然成立——没有修到缺陷本身。
- **把 `_resolve` 的四层优先级逻辑或者 `_overrides_lock`/`_cache` 的锁拆分重新设计一遍**：两个
  bug 都不在这里，属于"看到并发代码就想全部重新加锁"的过度反应。

## 8. 真实库对应 + 延伸练习
这两个 bug 没有对应到某个具体编号的上游 issue，但都是极常见的真实 bug **模式**：
"memoization 的 check-then-act 没有被一次锁完整覆盖"（缓存踩踏/dog-piling）和"生命周期方法忘记
连带重置相关状态"，在连接池、内存缓存、单例初始化这类代码里反复出现。

延伸练习：`python3 loop/mock.py start bs04` → `test` → `ref`。练完之后可以自己动手做一次
"制造确定性并发复现"的练习——挑一段自己写过的、"理论上有竞态但很少实际触发"的代码，试着用
`threading.Barrier` 卡住多个线程的起跑点、用一个足够长的 `sleep` 撑大竞态窗口，把它从"偶尔失败"
变成"每次都失败"，这是本题真正想教会你的技能，比记住这两个具体 bug 更有用。
