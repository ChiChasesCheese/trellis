%% trellis:begin %%
# CPython InternalDocs：解释器、编译器、GC 与运行时对象

CPython core developers · free-online · [[Python MOC|Python]]
[Home ↗](https://github.com/python/cpython/tree/main/InternalDocs)

16 sections · 13 readings · 81 cards · 16/79 leaves reached

## Outline
- CPython InternalDocs — *skipped*
- Source Code Structure — *skipped*
- Guide to the Parser — *skipped*
- **Compiler Design** — [[cpy-compiler-pipeline|编译流水线：从源码到字节码经过了几道工序]] → [[runtime.compile-bytecode|从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存]] · 6 cards
- **Code Objects** — [[cpy-code-objects|代码对象：字节码之外还带着什么]] → [[runtime.compile-bytecode|从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存]], [[runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]] · 12 cards
- **Generators** — [[cpy-generators-internals|生成器对象怎么把一次函数调用变成可以反复挂起的执行]] → [[iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]], [[iteration.yield-from|`yield from` 与生成器的 `send`/`throw`/`close`]], [[runtime.frames-eval|求值循环与帧：调用栈、递归限制与尾调用]] · 12 cards
- **Frames** — [[cpy-frames-internals|帧（Frame）的内存布局与 3.11 的惰性创建优化]] → [[runtime.frames-eval|求值循环与帧：调用栈、递归限制与尾调用]] · 6 cards
- **The Bytecode Interpreter** — [[cpy-bytecode-interpreter|字节码解释器：栈机、调用栈重构与自适应特化]] → [[runtime.adaptive-jit|自适应解释器（PEP 659）与实验性 JIT（PEP 744）]], [[runtime.frames-eval|求值循环与帧：调用栈、递归限制与尾调用]] · 12 cards
- **The JIT** — [[cpy-jit-tier2|分层执行：从追踪记录到 copy-and-patch JIT]] → [[runtime.adaptive-jit|自适应解释器（PEP 659）与实验性 JIT（PEP 744）]] · 6 cards
- **Garbage Collector Design** — [[cpy-gc-design|循环垃圾回收器：分代、可达性扫描与销毁顺序]] → [[memory.cyclic-gc|循环垃圾回收：分代（generations）、阈值与增量回收]], [[memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]] · 10 cards
- **Exception Handling** — [[cpy-exception-table|零成本异常处理：try 不抛异常时到底付了多少代价]] → [[runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]] · 6 cards
- **Quiescent-State Based Reclamation** — [[cpy-qsbr-reclaim|自由线程构建里，读操作为什么能不加锁]] → [[concurrency.free-threading|自由线程（PEP 703，3.13 实验版）与子解释器（PEP 734）]]
- **String Interning** — [[cpy-string-interning|字符串驻留与不朽对象：is 比较为什么能又快又准]] → [[memory.interning-immortal|驻留（interning）与不朽对象（immortal objects，PEP 683）]], [[model.names-objects|名字绑定、对象身份与 `is` vs `==`]] · 12 cards
- **asyncio** — [[cpy-asyncio-internals|异步生成器为什么会漏跑 finally，以及 Task 是怎么被追踪的]] → [[asyncio.debugging|常见 bug 与调试：漏 `await`、循环已在运行、异常被吞、`PYTHONASYNCIODEBUG`]], [[asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]] · 12 cards
- **List Sort Algorithm (Timsort)** — [[cpy-timsort|Timsort：为什么 list.sort() 对“已经有点顺序”的数据特别快]] → [[performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]] · 6 cards
- **Dict Implementation Notes** — [[cpy-dict-notes|dict 的键值分离设计：为什么同一个类的实例能共享一张键表]] → [[model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[memory.object-size|对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销]] · 11 cards

## Leaves this corpus never reached (63)
Your reading list: the map says these exist and the book does not teach them.
- [[model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]] — 掌握可变性如何决定函数参数的副作用、`def f(x, acc=[])` 为什么共享状态、tuple 为什么能做字典键，以及 `+=` 在两类对象上的不同行为。
- [[model.copy|浅拷贝、深拷贝与切片复制]] — 理解 `copy.copy`、切片、`list()` 只复制一层，`copy.deepcopy` 递归复制并处理环，以及什么时候别名反而是想要的。
- [[model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]] — 理解解释器如何通过特殊方法实现 `len()`、`for`、`in`、`+`、调用等语法，`__repr__` 与 `__str__` 的分工，以及为什么应实现协议而不是继承内建类型。
- [[model.hash-eq|`__hash__` 与 `__eq__` 的契约]] — 掌握相等的对象必须有相同哈希、定义 `__eq__` 会让 `__hash__` 变 None、可哈希对象为何必须不可变，以及自定义类做字典键时的常见错误。
- [[model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]] — 区分容器序列与扁平序列、可变与不可变序列，掌握切片对象与 `__getitem__` 的交互、`+=` 的就地语义、`array`/`memoryview` 的零拷贝场景。
- [[model.text-bytes|str 与 bytes：Unicode、编码与解码]] — 理解字符串是 Unicode 码点序列、bytes 是字节序列，编码/解码在 I/O 边界发生，UTF-8 与错误处理策略，以及"Unicode 三明治"原则。
- [[model.numbers|数值：int 大整数、float 精度与 Decimal]] — 掌握 int 任意精度、float 是 IEEE 754 双精度导致 `0.1+0.2 != 0.3`、金额为什么用 `Decimal` 或整数分并显式指定舍入，以及 `//` 和 `%` 对负数的定义。
- [[functions.first-class|一等函数：作为对象传递、高阶函数与 lambda]] — 理解函数对象的属性（`__name__`、`__doc__`、`__defaults__`）、把函数当参数与返回值，以及 lambda 只是没有名字的单表达式函数。
- [[functions.scope-closure|作用域（LEGB）、闭包与 `nonlocal`]] — 掌握名字查找顺序 Local→Enclosing→Global→Builtin、闭包如何持有自由变量的 cell、赋值为何让变量变局部（`UnboundLocalError`），以及循环中闭包的迟绑定陷阱。
- [[functions.arguments|参数传递：`*args`/`**kwargs`、仅关键字与仅位置参数、默认值求值时机]] — 理解 Python 是"按对象引用传递"、默认值在定义时求值一次、`*` 与 `/` 分隔符的用途，以及解包调用与形参的匹配规则。
- [[functions.decorators|装饰器：`@` 语法糖、`functools.wraps` 与执行时机]] — 理解 `@d` 等价于 `f = d(f)` 且在模块导入时执行、包装函数如何转发参数与返回值、`wraps` 为何要保留元数据，以及叠加多个装饰器的应用顺序。
- [[functions.decorator-patterns|带参数的装饰器、类装饰器与常见实例（retry、memoize、timing、rate limit）]] — 掌握三层嵌套的参数化装饰器、用类实现带状态的装饰器、装饰方法时 `self` 的传递，以及缓存/重试/限流装饰器的设计要点与可测试性（注入时钟）。
- [[functions.functools|`functools`：`lru_cache`、`partial`、`singledispatch`、`cached_property`]] — 掌握标准库提供的函数工具及其陷阱：`lru_cache` 要求参数可哈希且可能泄漏内存、`partial` 固定参数、`singledispatch` 按第一个参数类型分派。
- [[iteration.iterator-protocol|可迭代对象与迭代器：`__iter__`、`__next__`、`StopIteration`]] — 区分 iterable（能产生迭代器）与 iterator（有状态、一次性），理解 `for` 循环的展开方式，以及为什么迭代器耗尽后要重新获取。
- [[iteration.itertools|`itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`]] — 掌握用迭代器工具组合出流水线而不物化中间列表，`groupby` 要求先排序，以及 `tee` 的内存代价。
- [[iteration.context-managers|上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`]] — 理解 `with` 如何保证 `__exit__` 在异常时也执行、`__exit__` 返回 True 会吞掉异常、用生成器写上下文管理器时 `try/finally` 包住 `yield`，以及 `ExitStack` 管理动态数量的资源。
- [[iteration.comprehensions|推导式与 `else` 块：可读性边界与作用域]] — 掌握推导式有自己的作用域、超过两层控制子表达式应改写为循环、`for/else` 与 `try/else` 的语义，以及何时用 `map/filter`。
- [[iteration.pattern-matching|结构化模式匹配：`match`/`case`、捕获、守卫与类模式]] — 理解 3.10 的 `match` 不是 switch：模式会解构序列、映射与类实例并绑定名字，`case _` 兜底、`if` 守卫、`__match_args__` 决定位置模式，以及什么时候一串 `if` 反而更清楚。
- [[classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]] — 掌握一个类应实现的基本协议、`@classmethod` 作为备选构造器、`@staticmethod` 的定位，以及为什么 `__repr__` 应该能重建对象。
- [[classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]] — 比较三种数据类构建器的可变性、内存与哈希语义，`frozen=True`、`field(default_factory=)`、`__post_init__` 校验，以及 `__slots__` 省内存并禁止动态属性的代价。
- [[classes.attribute-lookup|属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`]] — 理解 `obj.x` 的查找顺序（数据描述符→实例 `__dict__`→类→非数据描述符→`__getattr__`），`__getattribute__` 拦截一切的风险，以及惰性属性的实现方式。
- [[classes.properties-descriptors|`property` 与描述符协议（`__get__`/`__set__`/`__set_name__`）]] — 掌握 property 是描述符的特例、数据描述符与非数据描述符的优先级差异、用描述符复用校验逻辑，以及 `__set_name__` 如何拿到属性名。
- [[classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]] — 理解鸭子类型靠行为而非继承、`collections.abc` 的虚拟子类与 `register`、`@abstractmethod` 阻止实例化，以及 Protocol 提供的结构化子类型（structural subtyping）。
- [[classes.inheritance-mro|继承、多重继承、MRO（C3 线性化）与 `super()`]] — 掌握方法解析顺序如何由 C3 算法决定、`super()` 调用的是 MRO 中的下一个而非父类、mixin 的设计约束，以及为何 Fluent Python 建议优先组合。
- [[classes.operator-overloading|运算符重载：`__add__`/`__radd__`、就地运算符与比较运算]] — 理解二元运算符的分派规则（先左操作数、返回 `NotImplemented` 再试反向方法）、`__iadd__` 缺省时退化为 `__add__`，以及比较运算符的反射对应关系。
- [[classes.metaprogramming|类装饰器、`__init_subclass__` 与元类（metaclass）]] — 理解类本身是 `type` 的实例、类体执行完后由元类创建类对象、`__init_subclass__` 与类装饰器在多数场景下足以替代元类，以及元类的典型用途（注册、校验、ORM）。
- [[classes.enums|枚举（Enum）：`Enum`/`IntEnum`/`StrEnum`/`Flag`、`auto()` 与唯一性]] — 理解枚举成员是类属性求值后由元类替换成的单例、`auto()` 与 `_generate_next_value_` 的取值规则、`@unique` 与别名、`Flag` 的位运算组合，以及什么时候该用 `StrEnum`/`IntEnum` 而不是裸常量。
- [[memory.allocator|pymalloc：arena / pool / block 与为何内存不还给操作系统]] — 理解小对象（≤512 字节）走 pymalloc 的三层分配器、大对象走系统 malloc、arena 只有全空才释放导致 RSS 居高不下，以及碎片化的影响。
- [[memory.leaks-tracemalloc|长驻进程的内存泄漏：来源、`tracemalloc` 与 `gc.get_referrers`]] — 掌握泄漏的常见来源（全局缓存、`lru_cache`、闭包与回调持有、循环引用加 `__del__`、C 扩展），用 `tracemalloc` 快照比对定位分配点，以及分块处理与定期重启 worker 的工程手段。
- [[memory.weakref|弱引用：`weakref`、`WeakValueDictionary` 与缓存]] — 掌握弱引用不增加引用计数、对象被回收后弱引用失效，以及用弱引用字典实现不阻止回收的缓存与观察者列表。
- [[concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]] — 理解 GIL 让同一进程内同一时刻只有一个线程执行字节码、I/O 与部分 C 扩展（NumPy 内核）会释放它、5 ms 切换间隔的含义，以及 GIL 保护的是解释器状态而不是你的数据。
- [[concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]] — 掌握用线程隐藏阻塞 I/O 的延迟、CPU 密集下多线程反而更慢的原因（GIL 争用）、守护线程的退出语义，以及线程创建的开销。
- [[concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]] — 理解 `x += 1` 不是原子操作、内建容器的单个方法在 GIL 下原子但复合操作不是、死锁的四个条件与锁顺序，以及线程安全的单例/计数器实现。
- [[concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]] — 掌握线程安全队列的阻塞语义、`join()`/`task_done()`、哨兵值关闭，以及"无共享状态"比加锁更可靠的设计原则。
- [[concurrency.multiprocessing|多进程：`multiprocessing`、fork vs spawn、pickle 边界与共享内存]] — 理解进程绕过 GIL 实现真并行、参数与返回值必须可 pickle、fork 在多线程程序中的危险与 3.14 起 POSIX 默认 forkserver（Windows/macOS 仍是 spawn）、`shared_memory` 与 `Manager` 的取舍。
- [[concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]] — 掌握执行器的统一接口、`submit` 返回 Future、`map` 保序而 `as_completed` 先完成先出、异常在 `.result()` 时抛出，以及如何按 I/O 或 CPU 密集选执行器。
- [[concurrency.choosing|选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树]] — 能在面试里用一句话给出结论：阻塞库 + I/O 用线程，CPU 用进程或换成 NumPy/DuckDB，高并发 I/O 且有 async 库用 asyncio，并说出每种选择的代价。
- [[asyncio.event-loop|事件循环：单线程协作式多任务如何工作]] — 理解事件循环维护就绪队列与 I/O 选择器（selectors）、协程在 `await` 处让出、CPU 密集代码会卡住整个循环，以及 `asyncio.run()` 创建并关闭循环。
- [[asyncio.futures|Future：可等待的占位符与回调]] — 理解 Future 表示尚未完成的结果、`set_result`/`set_exception` 唤醒等待者、`add_done_callback`，以及 `run_in_executor` 如何把线程结果桥接成 Future。
- [[asyncio.gather-wait-timeout|并发组合：`gather`、`wait`、`wait_for`、`timeout` 与 `TaskGroup`]] — 掌握 `gather` 保序返回且默认第一个异常传播、`return_exceptions=True` 收集异常、`wait_for` 超时会取消任务，以及 3.11 `TaskGroup` 的结构化并发与异常组。
- [[asyncio.cancellation|取消：`CancelledError`、清理与不可取消的边界]] — 理解 `task.cancel()` 在下一次 await 处注入 `CancelledError`、`finally` 中的清理、`asyncio.shield` 保护关键段，以及取消被吞掉的常见 bug。
- [[asyncio.sync-primitives|异步同步原语与限流：`Semaphore`、`Lock`、`Queue`]] — 掌握 `asyncio.Semaphore` 限制在途请求数、`asyncio.Queue` 做异步生产者-消费者、异步锁与线程锁的区别，以及为什么单线程仍需要锁（跨 await 的临界区）。
- [[asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]] — 理解同步阻塞库会冻结事件循环、把它丢到线程池的两种 API、从线程回到事件循环的线程安全方式，以及 CPU 密集任务应交给进程池。
- [[asyncio.streams-protocols|网络层：Streams、Transports/Protocols 与 aiohttp 类客户端的用法]] — 理解高层 `open_connection`/`StreamReader` 与低层 Protocol 回调的分工、背压与 `drain()`，以及分页拉取 API 时并发限流与重试的组合模式。
- [[asyncio.contextvars|上下文变量（contextvars）：为什么线程局部存储在 `await` 之间会失效]] — 理解 `ContextVar` 按任务隔离而不是按线程隔离、每个 Task 在创建时复制当前 Context、`decimal` 上下文与追踪 ID 如何借此跨 await 传播，以及 `threading.local` 在 asyncio 里为何出错。
- [[runtime.import-system|导入系统：模块对象、`sys.modules`、包与循环导入]] — 掌握模块只执行一次并缓存于 `sys.modules`、`__init__.py` 与命名空间包、相对导入，以及循环导入的成因与三种解法。
- [[runtime.namespaces-execution|执行模型：命名空间、`global`、代码块与 `exec`/`eval` 的风险]] — 理解模块、类体、函数体各自的命名空间与执行时机、类体是在类创建时执行的代码块，以及 `exec`/`eval` 为何只用于开发工具。
- [[runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]] — 建立"该去哪个模块找"的索引：`deque`/`Counter`/`defaultdict`、堆与二分、时区感知的 datetime、pickle 的安全边界与 `copyreg`、logging 的层级与处理器。
- [[types.basics|类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束]] — 掌握注解只是元数据、`list[int]` 与 `List[int]`、`X | None` 语法，以及"类型提示不会让错误的调用失败"这一常被问到的事实。
- [[types.gradual-typing|渐进类型（gradual typing）、`Any` 与 mypy/pyright 的检查模型]] — 理解 `Any` 与所有类型兼容、检查器如何推断与缩窄（narrowing）、`TYPE_CHECKING` 避免循环导入，以及 `# type: ignore` 的代价。
- [[types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]] — 掌握结构化子类型如何给鸭子类型加静态检查、`TypeVar` 约束与协变/逆变、3.12 `class Box[T]` 语法，以及装饰器签名保真需要 `ParamSpec`。
- [[types.typeddict-literal|`TypedDict`、`Literal`、`NewType` 与 dataclass 注解]] — 掌握给 JSON 形字典加结构、用 `Literal` 限定取值、`NewType` 区分同底类型的 id，以及 dataclass 字段注解如何被读取。
- [[performance.profiling|先测量：`timeit`、`cProfile`、采样剖析器与内存剖析]] — 掌握微基准与整体剖析的区别、`cProfile` 的函数级开销、`py-spy` 类采样器对生产进程的低侵入，以及用 `tracemalloc`/`memray` 看内存。
- [[performance.numpy-vectorization|NumPy 向量化与内存布局：ndarray、广播、连续内存与视图]] — 理解向量化把循环下推到 C、连续内存与缓存友好、切片是视图而非拷贝、广播规则，以及为什么 Python 层 `for` 循环比向量化慢一到两个量级。
- [[performance.pandas-at-scale|pandas 大表：分块读取、dtype 与 category、`groupby` 与合并、写时复制]] — 掌握 `read_csv(chunksize=, usecols=, dtype=)` 控制内存、分块聚合再合并的 map-reduce 形态、`merge_asof` 做时间对齐、`validate=` 抓重复键，以及 2.x 写时复制（Copy-on-Write）对 `SettingWithCopy` 的影响。
- [[performance.compiling|编译与本地扩展：Cython、Numba、`ctypes` 与何时换引擎]] — 理解把热点编译为 C 的三条路径与各自的代价、NumPy/Numba 释放 GIL 的条件，以及"把计算推给 DuckDB/SQL 引擎"往往比优化 Python 循环更划算。
- [[performance.less-ram|省内存：生成器、`array`、`memoryview`、`__slots__` 与稀疏结构]] — 掌握流式处理代替物化、同质数据用 `array`/NumPy 代替 list 的对象开销、`memoryview` 零拷贝切片，以及概率数据结构（布隆过滤器）的适用场景。
- [[engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]] — 掌握把 `try` 缩到最小、为库定义根异常隔离调用方、异常变量在块外消失、`assert` 只用于内部假设，以及用 `warnings` 做迁移。
- [[engineering.testing|测试：pytest 夹具与参数化、`unittest.mock`、注入时钟与依赖]] — 掌握用 fixture 隔离状态、`parametrize` 覆盖边界、`patch` 的作用域与 autospec、把时间与 I/O 作为参数注入以获得确定性测试，以及浮点比较用 `approx`。
- [[engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]] — 能解释为什么金额绝不 float 累加、`Decimal(str(x))` 与 `Decimal(x)` 的区别、`ROUND_HALF_UP` 显式指定，以及 naive 与 aware datetime 混用会抛错。
- [[engineering.packaging-env|依赖与环境：虚拟环境、`pyproject.toml`、锁文件与 uv/pip]] — 掌握隔离环境为何必要、`pyproject.toml` 作为单一配置源、锁文件保证可复现，以及 `python -m` 运行模块的好处。
- [[engineering.serialization|序列化：`json`、`pickle` 的安全与版本、`copyreg` 与 dataclass 的转换]] — 理解 pickle 可执行任意代码故不可反序列化不可信数据、类改名后旧 pickle 失效的处理、json 与 Decimal/datetime 的自定义编码。
- [[engineering.logging-config|日志与配置：logging 层级、处理器与格式、结构化日志、环境变量配置]] — 掌握 logger 的层级传播、每个模块 `getLogger(__name__)`、处理器与格式器分离、在库里不配置根 logger，以及配置从环境变量/文件读取的模式。
%% trellis:end %%

## Notes
