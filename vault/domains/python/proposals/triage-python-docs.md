You are triaging a book into a study system. For each section below decide
what it should become, and answer with one JSON object (no prose).

## Corpus
`python-docs` — Python 官方文档：数据模型、HOWTO 与标准库. Sections are archived as markdown under `sources/archive/python-docs/`
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
- `01-datamodel` (L1) 3. Data model
  > # 3. Data model[¶](#data-model) ## 3.1. Objects, values and types[¶](#objects-values-and-types) *Objects* are Python’s abstraction for data. All data in a Pytho…
- `02-executionmodel` (L1) 4. Execution model
  > # 4. Execution model[¶](#execution-model) ## 4.1. Structure of a program[¶](#structure-of-a-program) A Python program is constructed from code blocks. A *block*…
- `03-import` (L1) 5. The import system
  > # 5. The import system[¶](#the-import-system) Python code in one [module](../glossary.html#term-module) gains access to the code in another module by the proces…
- `04-compound-stmts` (L1) 8. Compound statements
  > # 8. Compound statements[¶](#compound-statements) Compound statements contain (groups of) other statements; they affect or control the execution of those other …
- `05-descriptor` (L1) Descriptor Guide
  > # [Descriptor Guide](#id1)[¶](#descriptor-guide) - Author: - Raymond Hettinger - Contact: - <python at rcn dot com> [Descriptors](../glossary.html#term-descript…
- `06-a-conceptual-overview-of-asyncio` (L1) A Conceptual Overview of asyncio
  > # A Conceptual Overview of `asyncio`[¶](#a-conceptual-overview-of-asyncio) This [HOWTO](index.html#how-tos) article seeks to help you build a sturdy mental mode…
- `07-free-threading-python` (L1) Python support for free threading
  > # Python support for free threading[¶](#python-support-for-free-threading) Starting with the 3.13 release, CPython has support for a build of Python called [fre…
- `08-mro` (L1) The Python 2.3 Method Resolution Order
  > # The Python 2.3 Method Resolution Order[¶](#the-python-2-3-method-resolution-order) Note This is a historical document, provided as an appendix to the official…
- `09-sorting` (L1) Sorting Techniques
  > # Sorting Techniques[¶](#sorting-techniques) - Author: - Andrew Dalke and Raymond Hettinger Python lists have a built-in [`list.sort()`](../builtins/stdtypes.ht…
- `10-functional` (L1) Functional Programming HOWTO
  > # Functional Programming HOWTO[¶](#functional-programming-howto) - Author: - A. M. Kuchling - Release: - 0.32 In this document, we’ll take a tour of Python’s fe…
- `11-unicode` (L1) Unicode HOWTO
  > # Unicode HOWTO[¶](#unicode-howto) - Release: - 1.12 This HOWTO discusses Python’s support for the Unicode specification for representing textual data, and expl…
- `12-annotations` (L1) Annotations Best Practices
  > # Annotations Best Practices[¶](#annotations-best-practices) - author: - Larry Hastings ## Accessing The Annotations Dict Of An Object In Python 3.10 And Newer[…
- `13-logging` (L1) Logging HOWTO
  > # Logging HOWTO[¶](#logging-howto) - Author: - Vinay Sajip <vinay_sajip at red-dove dot com> This page contains tutorial information. For links to reference inf…
- `14-enum` (L1) Enum HOWTO
  > # Enum HOWTO[¶](#enum-howto) An [`Enum`](../library/enum.html#enum.Enum) is a set of symbolic names bound to unique values. They are similar to global variables…
- `15-classes` (L1) 9. Classes
  > # 9. Classes[¶](#classes) Classes provide a means of bundling data and functionality together. Creating a new class creates a new *type* of object, allowing new…
- `16-errors` (L1) 8. Errors and Exceptions
  > # 8. Errors and Exceptions[¶](#errors-and-exceptions) Until now error messages haven’t been more than mentioned, but if you have tried out the examples you have…
- `17-datastructures` (L1) 5. Data Structures
  > # 5. Data Structures[¶](#data-structures) This chapter describes some things you’ve learned about already in more detail, and adds some new things as well. ## 5…
- `18-modules` (L1) 6. Modules
  > # 6. Modules[¶](#modules) If you quit from the Python interpreter and enter it again, the definitions you have made (functions and variables) are lost. Therefor…
- `19-floatingpoint` (L1) 15. Floating-Point Arithmetic: Issues and Limitations
  > # 15. Floating-Point Arithmetic: Issues and Limitations[¶](#floating-point-arithmetic-issues-and-limitations) Floating-point numbers are represented in computer…
- `20-design` (L1) Design and History FAQ
  > # [Design and History FAQ](#id2)[¶](#design-and-history-faq) ## [Why does Python use indentation for grouping of statements?](#id3)[¶](#why-does-python-use-inde…
- `21-programming` (L1) Programming FAQ
  > # [Programming FAQ](#id2)[¶](#programming-faq) ## [General questions](#id3)[¶](#general-questions) ### [Is there a source code-level debugger with breakpoints a…
- `22-threading` (L1) threading — Thread-based parallelism
  > # `threading` — Thread-based parallelism[¶](#module-threading) **Source code:** [Lib/threading.py](https://github.com/python/cpython/tree/3.14/Lib/threading.py)…
- `23-multiprocessing` (L1) multiprocessing — Process-based parallelism
  > # `multiprocessing` — Process-based parallelism[¶](#module-multiprocessing) **Source code:** [Lib/multiprocessing/](https://github.com/python/cpython/tree/3.14/…
- `24-concurrent-futures` (L1) concurrent.futures — Launching parallel tasks
  > # `concurrent.futures` — Launching parallel tasks[¶](#module-concurrent.futures) Added in version 3.2. **Source code:** [Lib/concurrent/futures/thread.py](https…
- `25-queue` (L1) queue — A synchronized queue class
  > # `queue` — A synchronized queue class[¶](#module-queue) **Source code:** [Lib/queue.py](https://github.com/python/cpython/tree/3.14/Lib/queue.py) The `queue` m…
- `26-contextvars` (L1) contextvars — Context Variables
  > # `contextvars` — Context Variables[¶](#module-contextvars) This module provides APIs to manage, store, and access context-local state. The [`ContextVar`](#cont…
- `27-concurrent-interpreters` (L1) concurrent.interpreters — Multiple interpreters in the same process
  > # `concurrent.interpreters` — Multiple interpreters in the same process[¶](#module-concurrent.interpreters) Added in version 3.14. **Source code:** [Lib/concurr…
- `28-asyncio-task` (L1) Coroutines and tasks
  > # Coroutines and tasks[¶](#coroutines-and-tasks) This section outlines high-level asyncio APIs to work with coroutines and Tasks. ## [Coroutines](#id2)[¶](#coro…
- `29-asyncio-eventloop` (L1) Event loop
  > # Event loop[¶](#event-loop) **Source code:** [Lib/asyncio/events.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/events.py), [Lib/asyncio/base_even…
- `30-asyncio-future` (L1) Futures
  > # Futures[¶](#futures) **Source code:** [Lib/asyncio/futures.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/futures.py), [Lib/asyncio/base_futures.…
- `31-asyncio-sync` (L1) Synchronization Primitives
  > # Synchronization Primitives[¶](#synchronization-primitives) **Source code:** [Lib/asyncio/locks.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/loc…
- `32-asyncio-queue` (L1) Queues
  > # Queues[¶](#queues) **Source code:** [Lib/asyncio/queues.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/queues.py) asyncio queues are designed to …
- `33-asyncio-dev` (L1) Developing with asyncio
  > # Developing with asyncio[¶](#developing-with-asyncio) Asynchronous programming is different from classic “sequential” programming. This page lists common mista…
- `34-asyncio-runner` (L1) Runners
  > # Runners[¶](#runners) **Source code:** [Lib/asyncio/runners.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/runners.py) This section outlines high-…
- `36-asyncio-stream` (L1) Streams
  > # Streams[¶](#streams) **Source code:** [Lib/asyncio/streams.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/streams.py) Streams are high-level asyn…
- `37-asyncio-protocol` (L1) Transports and Protocols
  > # Transports and Protocols[¶](#transports-and-protocols) Preface Transports and Protocols are used by the **low-level** event loop APIs such as [`loop.create_co…
- `38-asyncio-threading` (L1) asyncio and free-threaded Python
  > # asyncio and free-threaded Python[¶](#asyncio-and-free-threaded-python) asyncio uses an event loop as a scheduler to enable highly efficient concurrency by swi…
- `39-gc` (L1) gc — Garbage Collector interface
  > # `gc` — Garbage Collector interface[¶](#module-gc) This module provides an interface to the optional garbage collector. It provides the ability to disable the …
- `40-weakref` (L1) weakref — Weak references
  > # `weakref` — Weak references[¶](#module-weakref) **Source code:** [Lib/weakref.py](https://github.com/python/cpython/tree/3.14/Lib/weakref.py) The `weakref` mo…
- `41-copy` (L1) copy — Shallow and deep copy operations
  > # `copy` — Shallow and deep copy operations[¶](#module-copy) **Source code:** [Lib/copy.py](https://github.com/python/cpython/tree/3.14/Lib/copy.py) Assignment …
- `42-sys` (L1) sys — System-specific parameters and functions
  > # `sys` — System-specific parameters and functions[¶](#module-sys) This module provides access to some variables used or maintained by the interpreter and to fu…
- `43-tracemalloc` (L1) tracemalloc — Trace memory allocations
  > # `tracemalloc` — Trace memory allocations[¶](#module-tracemalloc) Added in version 3.4. **Source code:** [Lib/tracemalloc.py](https://github.com/python/cpython…
- `44-functools` (L1) functools — Higher-order functions and operations on callable objects
  > # `functools` — Higher-order functions and operations on callable objects[¶](#module-functools) **Source code:** [Lib/functools.py](https://github.com/python/cp…
- `45-itertools` (L1) itertools — Functions creating iterators for efficient looping
  > # `itertools` — Functions creating iterators for efficient looping[¶](#module-itertools) This module implements a number of [iterator](../glossary.html#term-ite…
- `46-contextlib` (L1) contextlib — Utilities for with-statement contexts
  > # `contextlib` — Utilities for `with`-statement contexts[¶](#module-contextlib) **Source code:** [Lib/contextlib.py](https://github.com/python/cpython/tree/3.14…
- `47-dataclasses` (L1) dataclasses — Data Classes
  > # `dataclasses` — Data Classes[¶](#module-dataclasses) **Source code:** [Lib/dataclasses.py](https://github.com/python/cpython/tree/3.14/Lib/dataclasses.py) Thi…
- `48-collections` (L1) collections — Container datatypes
  > # `collections` — Container datatypes[¶](#module-collections) **Source code:** [Lib/collections/__init__.py](https://github.com/python/cpython/tree/3.14/Lib/col…
- `49-collections-abc` (L1) collections.abc — Abstract Base Classes for Containers
  > # `collections.abc` — Abstract Base Classes for Containers[¶](#module-collections.abc) Added in version 3.3: Formerly, this module was part of the [`collections…
- `50-abc` (L1) abc — Abstract Base Classes
  > # `abc` — Abstract Base Classes[¶](#module-abc) **Source code:** [Lib/abc.py](https://github.com/python/cpython/tree/3.14/Lib/abc.py) This module provides the i…
- `51-typing` (L1) typing — Support for type hints
  > # `typing` — Support for type hints[¶](#typing-support-for-type-hints) Added in version 3.5. **Source code:** [Lib/typing.py](https://github.com/python/cpython/…
- `52-exceptions` (L1) Built-in Exceptions
  > # Built-in Exceptions[¶](#built-in-exceptions) In Python, all exceptions must be instances of a class that derives from [`BaseException`](#BaseException). In a …
- `53-decimal` (L1) decimal — Decimal fixed-point and floating-point arithmetic
  > # `decimal` — Decimal fixed-point and floating-point arithmetic[¶](#module-decimal) **Source code:** [Lib/decimal.py](https://github.com/python/cpython/tree/3.1…
- `54-datetime` (L1) datetime — Basic date and time types
  > # `datetime` — Basic date and time types[¶](#module-datetime) **Source code:** [Lib/datetime.py](https://github.com/python/cpython/tree/3.14/Lib/datetime.py) Th…
- `55-pickle` (L1) pickle — Python object serialization
  > # `pickle` — Python object serialization[¶](#module-pickle) **Source code:** [Lib/pickle.py](https://github.com/python/cpython/tree/3.14/Lib/pickle.py) The `pic…
- `56-json` (L1) json — JSON encoder and decoder
  > # `json` — JSON encoder and decoder[¶](#module-json) **Source code:** [Lib/json/__init__.py](https://github.com/python/cpython/tree/3.14/Lib/json/__init__.py) […
- `57-heapq` (L1) heapq — Heap queue algorithm
  > # `heapq` — Heap queue algorithm[¶](#module-heapq) **Source code:** [Lib/heapq.py](https://github.com/python/cpython/tree/3.14/Lib/heapq.py) This module provide…
- `58-bisect` (L1) bisect — Array bisection algorithm
  > # `bisect` — Array bisection algorithm[¶](#module-bisect) **Source code:** [Lib/bisect.py](https://github.com/python/cpython/tree/3.14/Lib/bisect.py) This modul…
- `59-array` (L1) array — Efficient arrays of numeric values
  > # `array` — Efficient arrays of numeric values[¶](#module-array) This module defines an object type which can compactly represent an array of basic values: char…
- `60-stdtypes` (L1) Built-in Types
  > # Built-in Types[¶](#built-in-types) The following sections describe the standard types that are built into the interpreter. The principal built-in types are nu…
- `61-dis` (L1) dis — Disassembler for Python bytecode
  > # `dis` — Disassembler for Python bytecode[¶](#module-dis) **Source code:** [Lib/dis.py](https://github.com/python/cpython/tree/3.14/Lib/dis.py) The `dis` modul…
- `62-timeit` (L1) timeit — Measure execution time of small code snippets
  > # `timeit` — Measure execution time of small code snippets[¶](#module-timeit) **Source code:** [Lib/timeit.py](https://github.com/python/cpython/tree/3.14/Lib/t…
- `63-profile` (L1) The Python Profilers
  > # The Python Profilers[¶](#the-python-profilers) **Source code:** [Lib/profile.py](https://github.com/python/cpython/tree/3.14/Lib/profile.py) and [Lib/pstats.p…
- `64-unittest-mock` (L1) unittest.mock — mock object library
  > # `unittest.mock` — mock object library[¶](#module-unittest.mock) Added in version 3.3. **Source code:** [Lib/unittest/mock.py](https://github.com/python/cpytho…
- `65-logging` (L1) logging — Logging facility for Python
  > # `logging` — Logging facility for Python[¶](#module-logging) **Source code:** [Lib/logging/__init__.py](https://github.com/python/cpython/tree/3.14/Lib/logging…
- `66-warnings` (L1) warnings — Warning control
  > # `warnings` — Warning control[¶](#module-warnings) **Source code:** [Lib/warnings.py](https://github.com/python/cpython/tree/3.14/Lib/warnings.py) Warning mess…
- `67-venv` (L1) venv — Creation of virtual environments
  > # `venv` — Creation of virtual environments[¶](#module-venv) Added in version 3.3. **Source code:** [Lib/venv/](https://github.com/python/cpython/tree/3.14/Lib/…

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
- `slug` must be unique, lowercase-hyphenated, and start with `python-`.
- Be strict: a `skip` costs nothing, a diluted deck costs every review.

## Answer format
{"corpus": "python-docs", "items": [
  {"section": "032-3-4", "verdict": "reading", "nodes": ["producer.acks"],
   "slug": "python-producer-config", "title": "...", "body": "..."},
  {"section": "001-section", "verdict": "skip", "why": "front matter"},
  {"section": "099-x", "verdict": "gap", "proposed_leaf": "ops.tiered-storage", "why": "..."}
]}
