You are triaging a book into a study system. For each section below decide
what it should become, and answer with one JSON object (no prose).

## Corpus
`peps` — PEP：语言特性的设计文档. Sections are archived as markdown under `sources/archive/peps/`
(one file per section id) if you need to read one in full.

## The skeleton it lands on
### python
- `model.names-objects` — 对象模型：名字、对象与数据模型（data model）: 理解变量是对对象的引用而非容器，`id()`/`is` 比较身份、`==` 调用 `__eq__` 比较值，以及小整数与短字符串驻留（interning）为何只是实现细节。
- `model.mutability` — 对象模型：名字、对象与数据模型（data model）: 掌握可变性如何决定函数参数的副作用、`def f(x, acc=[])` 为什么共享状态、tuple 为什么能做字典键，以及 `+=` 在两类对象上的不同行为。
- `model.copy` — 对象模型：名字、对象与数据模型（data model）: 理解 `copy.copy`、切片、`list()` 只复制一层，`copy.deepcopy` 递归复制并处理环，以及什么时候别名反而是想要的。
- `model.dunder-protocols` — 对象模型：名字、对象与数据模型（data model）: 理解解释器如何通过特殊方法实现 `len()`、`for`、`in`、`+`、调用等语法，`__repr__` 与 `__str__` 的分工，以及为什么应实现协议而不是继承内建类型。
- `model.hash-eq` — 对象模型：名字、对象与数据模型（data model）: 掌握相等的对象必须有相同哈希、定义 `__eq__` 会让 `__hash__` 变 None、可哈希对象为何必须不可变，以及自定义类做字典键时的常见错误。
- `model.dict-set-internals` — 对象模型：名字、对象与数据模型（data model）: 理解哈希表如何用哈希值定位槽位并处理冲突（开放寻址、扰动探测）、3.6+ 紧凑 dict 为何保序、装载因子触发扩容，以及平均 O(1) 与最坏 O(n) 的来源。
- `model.sequences` — 对象模型：名字、对象与数据模型（data model）: 区分容器序列与扁平序列、可变与不可变序列，掌握切片对象与 `__getitem__` 的交互、`+=` 的就地语义、`array`/`memoryview` 的零拷贝场景。
- `model.text-bytes` — 对象模型：名字、对象与数据模型（data model）: 理解字符串是 Unicode 码点序列、bytes 是字节序列，编码/解码在 I/O 边界发生，UTF-8 与错误处理策略，以及"Unicode 三明治"原则。
- `model.numbers` — 对象模型：名字、对象与数据模型（data model）: 掌握 int 任意精度、float 是 IEEE 754 双精度导致 `0.1+0.2 != 0.3`、金额为什么用 `Decimal` 或整数分并显式指定舍入，以及 `//` 和 `%` 对负数的定义。
- `functions.first-class` — 函数、闭包与装饰器: 理解函数对象的属性（`__name__`、`__doc__`、`__defaults__`）、把函数当参数与返回值，以及 lambda 只是没有名字的单表达式函数。
- `functions.scope-closure` — 函数、闭包与装饰器: 掌握名字查找顺序 Local→Enclosing→Global→Builtin、闭包如何持有自由变量的 cell、赋值为何让变量变局部（`UnboundLocalError`），以及循环中闭包的迟绑定陷阱。
- `functions.arguments` — 函数、闭包与装饰器: 理解 Python 是"按对象引用传递"、默认值在定义时求值一次、`*` 与 `/` 分隔符的用途，以及解包调用与形参的匹配规则。
- `functions.decorators` — 函数、闭包与装饰器: 理解 `@d` 等价于 `f = d(f)` 且在模块导入时执行、包装函数如何转发参数与返回值、`wraps` 为何要保留元数据，以及叠加多个装饰器的应用顺序。
- `functions.decorator-patterns` — 函数、闭包与装饰器: 掌握三层嵌套的参数化装饰器、用类实现带状态的装饰器、装饰方法时 `self` 的传递，以及缓存/重试/限流装饰器的设计要点与可测试性（注入时钟）。
- `functions.functools` — 函数、闭包与装饰器: 掌握标准库提供的函数工具及其陷阱：`lru_cache` 要求参数可哈希且可能泄漏内存、`partial` 固定参数、`singledispatch` 按第一个参数类型分派。
- `iteration.iterator-protocol` — 迭代器、生成器与上下文管理器: 区分 iterable（能产生迭代器）与 iterator（有状态、一次性），理解 `for` 循环的展开方式，以及为什么迭代器耗尽后要重新获取。
- `iteration.generators` — 迭代器、生成器与上下文管理器: 理解 `yield` 让函数变成生成器工厂、执行在 `next()` 时才推进、生成器表达式与列表推导的内存差异，以及生成器只能消费一次的坑。
- `iteration.yield-from` — 迭代器、生成器与上下文管理器: 掌握 `yield from` 如何委托子生成器并透传值与异常、`send()` 让生成器成为经典协程，以及这套机制为何是 async/await 的前身。
- `iteration.itertools` — 迭代器、生成器与上下文管理器: 掌握用迭代器工具组合出流水线而不物化中间列表，`groupby` 要求先排序，以及 `tee` 的内存代价。
- `iteration.context-managers` — 迭代器、生成器与上下文管理器: 理解 `with` 如何保证 `__exit__` 在异常时也执行、`__exit__` 返回 True 会吞掉异常、用生成器写上下文管理器时 `try/finally` 包住 `yield`，以及 `ExitStack` 管理动态数量的资源。
- `iteration.comprehensions` — 迭代器、生成器与上下文管理器: 掌握推导式有自己的作用域、超过两层控制子表达式应改写为循环、`for/else` 与 `try/else` 的语义，以及何时用 `map/filter`。
- `classes.pythonic-object` — 类、协议与元编程: 掌握一个类应实现的基本协议、`@classmethod` 作为备选构造器、`@staticmethod` 的定位，以及为什么 `__repr__` 应该能重建对象。
- `classes.dataclasses` — 类、协议与元编程: 比较三种数据类构建器的可变性、内存与哈希语义，`frozen=True`、`field(default_factory=)`、`__post_init__` 校验，以及 `__slots__` 省内存并禁止动态属性的代价。
- `classes.attribute-lookup` — 类、协议与元编程: 理解 `obj.x` 的查找顺序（数据描述符→实例 `__dict__`→类→非数据描述符→`__getattr__`），`__getattribute__` 拦截一切的风险，以及惰性属性的实现方式。
- `classes.properties-descriptors` — 类、协议与元编程: 掌握 property 是描述符的特例、数据描述符与非数据描述符的优先级差异、用描述符复用校验逻辑，以及 `__set_name__` 如何拿到属性名。
- `classes.abc-protocols` — 类、协议与元编程: 理解鸭子类型靠行为而非继承、`collections.abc` 的虚拟子类与 `register`、`@abstractmethod` 阻止实例化，以及 Protocol 提供的结构化子类型（structural subtyping）。
- `classes.inheritance-mro` — 类、协议与元编程: 掌握方法解析顺序如何由 C3 算法决定、`super()` 调用的是 MRO 中的下一个而非父类、mixin 的设计约束，以及为何 Fluent Python 建议优先组合。
- `classes.operator-overloading` — 类、协议与元编程: 理解二元运算符的分派规则（先左操作数、返回 `NotImplemented` 再试反向方法）、`__iadd__` 缺省时退化为 `__add__`，以及比较运算符的反射对应关系。
- `classes.metaprogramming` — 类、协议与元编程: 理解类本身是 `type` 的实例、类体执行完后由元类创建类对象、`__init_subclass__` 与类装饰器在多数场景下足以替代元类，以及元类的典型用途（注册、校验、ORM）。
- `memory.refcounting` — 内存管理与垃圾回收: 理解每个对象头部的引用计数如何随赋值/作用域退出增减、归零即释放的确定性，以及引用计数无法处理循环引用的原因。
- `memory.cyclic-gc` — 内存管理与垃圾回收: 掌握 `gc` 模块如何追踪容器对象、通过"试减引用"找出不可达环、分代假设与触发阈值，3.12+ 增量回收的变化，以及 `__del__` 与弱引用在环中的处理。
- `memory.allocator` — 内存管理与垃圾回收: 理解小对象（≤512 字节）走 pymalloc 的三层分配器、大对象走系统 malloc、arena 只有全空才释放导致 RSS 居高不下，以及碎片化的影响。
- `memory.object-size` — 内存管理与垃圾回收: 掌握一个 Python 对象的头部开销、list 的过量分配策略、dict 的键共享，以及百万级小对象为什么该用 `__slots__`、tuple、array 或 NumPy。
- `memory.leaks-tracemalloc` — 内存管理与垃圾回收: 掌握泄漏的常见来源（全局缓存、`lru_cache`、闭包与回调持有、循环引用加 `__del__`、C 扩展），用 `tracemalloc` 快照比对定位分配点，以及分块处理与定期重启 worker 的工程手段。
- `memory.interning-immortal` — 内存管理与垃圾回收: 理解字符串驻留与小整数缓存如何省内存与加速比较，3.12 引入不朽对象让 `None`/`True`/小整数免于引用计数写入，以及这对多核与写时复制（fork）的意义。
- `memory.weakref` — 内存管理与垃圾回收: 掌握弱引用不增加引用计数、对象被回收后弱引用失效，以及用弱引用字典实现不阻止回收的缓存与观察者列表。
- `concurrency.gil` — 并发模型：GIL、线程与进程: 理解 GIL 让同一进程内同一时刻只有一个线程执行字节码、I/O 与部分 C 扩展（NumPy 内核）会释放它、5 ms 切换间隔的含义，以及 GIL 保护的是解释器状态而不是你的数据。
- `concurrency.threads` — 并发模型：GIL、线程与进程: 掌握用线程隐藏阻塞 I/O 的延迟、CPU 密集下多线程反而更慢的原因（GIL 争用）、守护线程的退出语义，以及线程创建的开销。
- `concurrency.locks-races` — 并发模型：GIL、线程与进程: 理解 `x += 1` 不是原子操作、内建容器的单个方法在 GIL 下原子但复合操作不是、死锁的四个条件与锁顺序，以及线程安全的单例/计数器实现。
- `concurrency.queues` — 并发模型：GIL、线程与进程: 掌握线程安全队列的阻塞语义、`join()`/`task_done()`、哨兵值关闭，以及"无共享状态"比加锁更可靠的设计原则。
- `concurrency.multiprocessing` — 并发模型：GIL、线程与进程: 理解进程绕过 GIL 实现真并行、参数与返回值必须可 pickle、fork 在多线程程序中的危险与 3.14 默认 spawn、`shared_memory` 与 `Manager` 的取舍。
- `concurrency.executors` — 并发模型：GIL、线程与进程: 掌握执行器的统一接口、`submit` 返回 Future、`map` 保序而 `as_completed` 先完成先出、异常在 `.result()` 时抛出，以及如何按 I/O 或 CPU 密集选执行器。
- `concurrency.free-threading` — 并发模型：GIL、线程与进程: 理解 `--disable-gil` 构建如何用偏向引用计数与每对象锁替代 GIL、单线程约 1–8% 开销与 C 扩展兼容问题，以及子解释器提供的另一条多核路径。
- `concurrency.choosing` — 并发模型：GIL、线程与进程: 能在面试里用一句话给出结论：阻塞库 + I/O 用线程，CPU 用进程或换成 NumPy/DuckDB，高并发 I/O 且有 async 库用 asyncio，并说出每种选择的代价。
- `asyncio.event-loop` — asyncio 异步编程: 理解事件循环维护就绪队列与 I/O 选择器（selectors）、协程在 `await` 处让出、CPU 密集代码会卡住整个循环，以及 `asyncio.run()` 创建并关闭循环。
- `asyncio.coroutines-tasks` — asyncio 异步编程: 掌握 `async def` 返回的协程必须被 await 或包成 Task 才会执行、`create_task` 立即调度、忘记 await 的"从未被等待"警告，以及 Task 是 Future 的子类。
- `asyncio.futures` — asyncio 异步编程: 理解 Future 表示尚未完成的结果、`set_result`/`set_exception` 唤醒等待者、`add_done_callback`，以及 `run_in_executor` 如何把线程结果桥接成 Future。
- `asyncio.gather-wait-timeout` — asyncio 异步编程: 掌握 `gather` 保序返回且默认第一个异常传播、`return_exceptions=True` 收集异常、`wait_for` 超时会取消任务，以及 3.11 `TaskGroup` 的结构化并发与异常组。
- `asyncio.cancellation` — asyncio 异步编程: 理解 `task.cancel()` 在下一次 await 处注入 `CancelledError`、`finally` 中的清理、`asyncio.shield` 保护关键段，以及取消被吞掉的常见 bug。
- `asyncio.sync-primitives` — asyncio 异步编程: 掌握 `asyncio.Semaphore` 限制在途请求数、`asyncio.Queue` 做异步生产者-消费者、异步锁与线程锁的区别，以及为什么单线程仍需要锁（跨 await 的临界区）。
- `asyncio.blocking-and-threads` — asyncio 异步编程: 理解同步阻塞库会冻结事件循环、把它丢到线程池的两种 API、从线程回到事件循环的线程安全方式，以及 CPU 密集任务应交给进程池。
- `asyncio.debugging` — asyncio 异步编程: 能诊断"程序没有输出"的典型原因：协程未被 await、`gather` 未 await、事件循环嵌套（Jupyter）、异常留在未取回的 Task 里，以及 debug 模式与慢回调告警。
- `asyncio.streams-protocols` — asyncio 异步编程: 理解高层 `open_connection`/`StreamReader` 与低层 Protocol 回调的分工、背压与 `drain()`，以及分页拉取 API 时并发限流与重试的组合模式。
- `runtime.compile-bytecode` — 解释器与执行模型: 理解 CPython 先编译为字节码再解释执行、`__pycache__` 按源码时间戳/哈希失效、`dis` 如何用于解释性能差异，以及"Python 是解释型语言"这句话的准确含义。
- `runtime.frames-eval` — 解释器与执行模型: 掌握每次函数调用创建帧对象、`sys.setrecursionlimit` 与栈溢出、生成器为何能挂起（帧被保留），以及 3.11 帧对象的惰性创建优化。
- `runtime.adaptive-jit` — 解释器与执行模型: 理解 3.11 起的特化（specializing）字节码如何按运行时类型内联快速路径，3.13 的 copy-and-patch JIT 处于实验阶段，以及这对"Python 慢"的回答意味着什么。
- `runtime.import-system` — 解释器与执行模型: 掌握模块只执行一次并缓存于 `sys.modules`、`__init__.py` 与命名空间包、相对导入，以及循环导入的成因与三种解法。
- `runtime.exceptions` — 解释器与执行模型: 掌握 `BaseException` 与 `Exception` 的分界（`KeyboardInterrupt`/`SystemExit`）、`raise ... from`、`else` 块的用途、EAFP 风格，以及 3.11 `ExceptionGroup` 与 `except*`。
- `runtime.namespaces-execution` — 解释器与执行模型: 理解模块、类体、函数体各自的命名空间与执行时机、类体是在类创建时执行的代码块，以及 `exec`/`eval` 为何只用于开发工具。
- `runtime.stdlib-map` — 解释器与执行模型: 建立"该去哪个模块找"的索引：`deque`/`Counter`/`defaultdict`、堆与二分、时区感知的 datetime、pickle 的安全边界与 `copyreg`、logging 的层级与处理器。
- `types.basics` — 类型提示与静态检查: 掌握注解只是元数据、`list[int]` 与 `List[int]`、`X | None` 语法，以及"类型提示不会让错误的调用失败"这一常被问到的事实。
- `types.gradual-typing` — 类型提示与静态检查: 理解 `Any` 与所有类型兼容、检查器如何推断与缩窄（narrowing）、`TYPE_CHECKING` 避免循环导入，以及 `# type: ignore` 的代价。
- `types.protocols-generics` — 类型提示与静态检查: 掌握结构化子类型如何给鸭子类型加静态检查、`TypeVar` 约束与协变/逆变、3.12 `class Box[T]` 语法，以及装饰器签名保真需要 `ParamSpec`。
- `types.typeddict-literal` — 类型提示与静态检查: 掌握给 JSON 形字典加结构、用 `Literal` 限定取值、`NewType` 区分同底类型的 id，以及 dataclass 字段注解如何被读取。
- `performance.profiling` — 性能与数据处理: 掌握微基准与整体剖析的区别、`cProfile` 的函数级开销、`py-spy` 类采样器对生产进程的低侵入，以及用 `tracemalloc`/`memray` 看内存。
- `performance.containers` — 性能与数据处理: 能说出 list 头部插入 O(n)、`in` 在 list 与 set 上的差异、dict 查找的常数因子、`deque` 两端 O(1)，以及排序（Timsort）稳定且利用已有序段。
- `performance.numpy-vectorization` — 性能与数据处理: 理解向量化把循环下推到 C、连续内存与缓存友好、切片是视图而非拷贝、广播规则，以及为什么 Python 层 `for` 循环比向量化慢一到两个量级。
- `performance.pandas-at-scale` — 性能与数据处理: 掌握 `read_csv(chunksize=, usecols=, dtype=)` 控制内存、分块聚合再合并的 map-reduce 形态、`merge_asof` 做时间对齐、`validate=` 抓重复键，以及 2.x 写时复制（Copy-on-Write）对 `SettingWithCopy` 的影响。
- `performance.compiling` — 性能与数据处理: 理解把热点编译为 C 的三条路径与各自的代价、NumPy/Numba 释放 GIL 的条件，以及"把计算推给 DuckDB/SQL 引擎"往往比优化 Python 循环更划算。
- `performance.less-ram` — 性能与数据处理: 掌握流式处理代替物化、同质数据用 `array`/NumPy 代替 list 的对象开销、`memoryview` 零拷贝切片，以及概率数据结构（布隆过滤器）的适用场景。
- `engineering.robustness` — 工程实践：健壮性、测试与交付: 掌握把 `try` 缩到最小、为库定义根异常隔离调用方、异常变量在块外消失、`assert` 只用于内部假设，以及用 `warnings` 做迁移。
- `engineering.testing` — 工程实践：健壮性、测试与交付: 掌握用 fixture 隔离状态、`parametrize` 覆盖边界、`patch` 的作用域与 autospec、把时间与 I/O 作为参数注入以获得确定性测试，以及浮点比较用 `approx`。
- `engineering.money-time` — 工程实践：健壮性、测试与交付: 能解释为什么金额绝不 float 累加、`Decimal(str(x))` 与 `Decimal(x)` 的区别、`ROUND_HALF_UP` 显式指定，以及 naive 与 aware datetime 混用会抛错。
- `engineering.packaging-env` — 工程实践：健壮性、测试与交付: 掌握隔离环境为何必要、`pyproject.toml` 作为单一配置源、锁文件保证可复现，以及 `python -m` 运行模块的好处。
- `engineering.serialization` — 工程实践：健壮性、测试与交付: 理解 pickle 可执行任意代码故不可反序列化不可信数据、类改名后旧 pickle 失效的处理、json 与 Decimal/datetime 的自定义编码。
- `engineering.logging-config` — 工程实践：健壮性、测试与交付: 掌握 logger 的层级传播、每个模块 `getLogger(__name__)`、处理器与格式器分离、在库里不配置根 logger，以及配置从环境变量/文件读取的模式。

## Sections
- `01-pep-0703` (L1) PEP 703 – Making the Global Interpreter Lock Optional in CPython | peps.python.org
  > # PEP 703 – Making the Global Interpreter Lock Optional in CPython - Author: - Sam Gross <colesbury at gmail.com> - Sponsor: - Łukasz Langa <lukasz at python.or…
- `02-pep-0734` (L1) PEP 734 – Multiple Interpreters in the Stdlib | peps.python.org
  > # PEP 734 – Multiple Interpreters in the Stdlib - Author: - Eric Snow <ericsnowcurrently at gmail.com> - Discussions-To: - [Discourse thread](https://discuss.py…
- `03-pep-0683` (L1) PEP 683 – Immortal Objects, Using a Fixed Refcount | peps.python.org
  > # PEP 683 – Immortal Objects, Using a Fixed Refcount - Author: - Eric Snow <ericsnowcurrently at gmail.com>, Eddie Elizondo <eduardo.elizondorueda at gmail.com>…
- `04-pep-0659` (L1) PEP 659 – Specializing Adaptive Interpreter | peps.python.org
  > # PEP 659 – Specializing Adaptive Interpreter - Author: - Mark Shannon <mark at hotpy.org> - Status: - Final - Type: - Informational - Created: - 13-Apr-2021 - …
- `05-pep-0744` (L1) PEP 744 – JIT Compilation | peps.python.org
  > # PEP 744 – JIT Compilation - Author: - Brandt Bucher <brandt at python.org>, Savannah Ostrowski <savannah at python.org> - Discussions-To: - [Discourse thread]…
- `06-pep-0492` (L1) PEP 492 – Coroutines with async and await syntax | peps.python.org
  > # PEP 492 – Coroutines with async and await syntax - Author: - Yury Selivanov <yury at edgedb.com> - Discussions-To: - [Python-Dev list](https://mail.python.org…
- `07-pep-0380` (L1) PEP 380 – Syntax for Delegating to a Subgenerator | peps.python.org
  > # PEP 380 – Syntax for Delegating to a Subgenerator - Author: - Gregory Ewing <greg.ewing at canterbury.ac.nz> - Status: - Final - Type: - Standards Track - Cre…
- `08-pep-0342` (L1) PEP 342 – Coroutines via Enhanced Generators | peps.python.org
  > # PEP 342 – Coroutines via Enhanced Generators - Author: - Guido van Rossum, Phillip J. Eby - Status: - Final - Type: - Standards Track - Created: - 10-May-2005…
- `09-pep-0343` (L1) PEP 343 – The “with” Statement | peps.python.org
  > # PEP 343 – The “with” Statement - Author: - Guido van Rossum, Alyssa Coghlan - Status: - Final - Type: - Standards Track - Created: - 13-May-2005 - Python-Vers…
- `10-pep-0318` (L1) PEP 318 – Decorators for Functions and Methods | peps.python.org
  > # PEP 318 – Decorators for Functions and Methods - Author: - Kevin D. Smith <Kevin.Smith at theMorgue.org>, Jim J. Jewett, Skip Montanaro, Anthony Baxter - Stat…
- `11-pep-3148` (L1) PEP 3148 – futures - execute computations asynchronously | peps.python.org
  > # PEP 3148 – futures - execute computations asynchronously - Author: - Brian Quinlan <brian at sweetapp.com> - Status: - Final - Type: - Standards Track - Creat…
- `12-pep-0557` (L1) PEP 557 – Data Classes | peps.python.org
  > # PEP 557 – Data Classes - Author: - Eric V. Smith <eric at trueblade.com> - Status: - Final - Type: - Standards Track - Created: - 02-Jun-2017 - Python-Version…
- `13-pep-0484` (L1) PEP 484 – Type Hints | peps.python.org
  > # PEP 484 – Type Hints - Author: - Guido van Rossum <guido at python.org>, Jukka Lehtosalo <jukka.lehtosalo at iki.fi>, Łukasz Langa <lukasz at python.org> - BD…
- `14-pep-0544` (L1) PEP 544 – Protocols: Structural subtyping (static duck typing) | peps.python.org
  > # PEP 544 – Protocols: Structural subtyping (static duck typing) - Author: - Ivan Levkivskyi <levkivskyi at gmail.com>, Jukka Lehtosalo <jukka.lehtosalo at iki.…
- `15-pep-0526` (L1) PEP 526 – Syntax for Variable Annotations | peps.python.org
  > # PEP 526 – Syntax for Variable Annotations - Author: - Ryan Gonzalez <rymg19 at gmail.com>, Philip House <phouse512 at gmail.com>, Ivan Levkivskyi <levkivskyi …
- `16-pep-0612` (L1) PEP 612 – Parameter Specification Variables | peps.python.org
  > # PEP 612 – Parameter Specification Variables - Author: - Mark Mendoza <mendoza.mark.a at gmail.com> - Sponsor: - Guido van Rossum <guido at python.org> - BDFL-…
- `17-pep-0695` (L1) PEP 695 – Type Parameter Syntax | peps.python.org
  > # PEP 695 – Type Parameter Syntax - Author: - Eric Traut <erictr at microsoft.com> - Sponsor: - Guido van Rossum <guido at python.org> - Discussions-To: - [Typi…
- `18-pep-0649` (L1) PEP 649 – Deferred Evaluation Of Annotations Using Descriptors | peps.python.org
  > # PEP 649 – Deferred Evaluation Of Annotations Using Descriptors - Author: - Larry Hastings <larry at hastings.org> - Discussions-To: - [Discourse thread](https…
- `19-pep-3119` (L1) PEP 3119 – Introducing Abstract Base Classes | peps.python.org
  > # PEP 3119 – Introducing Abstract Base Classes - Author: - Guido van Rossum <guido at python.org>, Talin <viridia at gmail.com> - Status: - Final - Type: - Stan…
- `20-pep-3134` (L1) PEP 3134 – Exception Chaining and Embedded Tracebacks | peps.python.org
  > # PEP 3134 – Exception Chaining and Embedded Tracebacks - Author: - Ka-Ping Yee - Status: - Final - Type: - Standards Track - Created: - 12-May-2005 - Python-Ve…
- `21-pep-0654` (L1) PEP 654 – Exception Groups and except* | peps.python.org
  > # PEP 654 – Exception Groups and except* - Author: - Irit Katriel <irit at python.org>, Yury Selivanov <yury at edgedb.com>, Guido van Rossum <guido at python.o…
- `22-pep-0572` (L1) PEP 572 – Assignment Expressions | peps.python.org
  > # PEP 572 – Assignment Expressions - Author: - Chris Angelico <rosuav at gmail.com>, Tim Peters <tim.peters at gmail.com>, Guido van Rossum <guido at python.org…
- `23-pep-0636` (L1) PEP 636 – Structural Pattern Matching: Tutorial | peps.python.org
  > # PEP 636 – Structural Pattern Matching: Tutorial - Author: - Daniel F Moisset <dfmoisset at gmail.com> - Sponsor: - Guido van Rossum <guido at python.org> - BD…
- `24-pep-0412` (L1) PEP 412 – Key-Sharing Dictionary | peps.python.org
  > # PEP 412 – Key-Sharing Dictionary - Author: - Mark Shannon <mark at hotpy.org> - Status: - Final - Type: - Standards Track - Created: - 08-Feb-2012 - Python-Ve…
- `25-pep-0567` (L1) PEP 567 – Context Variables | peps.python.org
  > # PEP 567 – Context Variables - Author: - Yury Selivanov <yury at edgedb.com> - Status: - Final - Type: - Standards Track - Created: - 12-Dec-2017 - Python-Vers…

## Verdicts
- `reading` — the section TEACHES one or more leaves. `nodes` lists them;
  `title` is the reading's own title; `body` (100-200 words, in Chinese (简体中文))
  says why to read this section and what to take from it, for someone who
  has never opened the book. A section may serve several leaves; a leaf
  may be served by several sections.
- `gap` — the section clearly belongs to this subject but no leaf fits.
  Name the missing leaf under `proposed_leaf`. A wanted outcome.
- `skip` — front matter, installation walkthroughs, summaries, or anything
  that teaches nothing a leaf should carry.

## Rules
- `nodes` must be leaf ids copied exactly from above.
- `slug` must be unique, lowercase-hyphenated, and start with `peps-`.
- Be strict: a `skip` costs nothing, a diluted deck costs every review.

## Answer format
{"corpus": "peps", "items": [
  {"section": "032-3-4", "verdict": "reading", "nodes": ["producer.acks"],
   "slug": "peps-producer-config", "title": "...", "body": "..."},
  {"section": "001-section", "verdict": "skip", "why": "front matter"},
  {"section": "099-x", "verdict": "gap", "proposed_leaf": "ops.tiered-storage", "why": "..."}
]}
