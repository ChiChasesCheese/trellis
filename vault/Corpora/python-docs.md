%% trellis:begin %%
# Python 官方文档：数据模型、HOWTO 与标准库

Python Software Foundation · free-online · [[Python MOC|Python]]
[Home ↗](https://docs.python.org/3/)

66 sections · 66 readings · 339 cards · 71/79 leaves reached

## Outline
- **3. Data model** — [[py-pydocs-data-model|数据模型（Data Model）参考]] → [[model.names-objects|名字绑定、对象身份与 `is` vs `==`]], [[model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]], [[model.numbers|数值：int 大整数、float 精度与 Decimal]], [[model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]], [[model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]], [[model.hash-eq|`__hash__` 与 `__eq__` 的契约]], [[classes.operator-overloading|运算符重载：`__add__`/`__radd__`、就地运算符与比较运算]], [[iteration.context-managers|上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`]], [[memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]], [[classes.metaprogramming|类装饰器、`__init_subclass__` 与元类（metaclass）]] · 48 cards
- **4. Execution model** — [[pydocs-execution-model|执行模型：命名空间与作用域]] → [[functions.scope-closure|作用域（LEGB）、闭包与 `nonlocal`]], [[runtime.namespaces-execution|执行模型：命名空间、`global`、代码块与 `exec`/`eval` 的风险]] · 12 cards
- **5. The import system** — [[pydocs-import-system|导入系统（import system）完整机制]] → [[runtime.import-system|导入系统：模块对象、`sys.modules`、包与循环导入]] · 6 cards
- **8. Compound statements** — [[pydocs-compound-statements|复合语句语法参考：with / try / 泛型参数]] → [[iteration.context-managers|上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`]], [[runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]], [[types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]], [[types.basics|类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束]] · 18 cards
- **Descriptor Guide** — [[pydocs-descriptor-guide|描述符指南（Descriptor Guide）]] → [[classes.properties-descriptors|`property` 与描述符协议（`__get__`/`__set__`/`__set_name__`）]], [[classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]], [[classes.attribute-lookup|属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`]] · 18 cards
- **A Conceptual Overview of asyncio** — [[pydocs-asyncio-overview|asyncio 概念全景：事件循环、协程与 Future]] → [[asyncio.event-loop|事件循环：单线程协作式多任务如何工作]], [[asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]], [[asyncio.futures|Future：可等待的占位符与回调]] · 11 cards
- **Python support for free threading** — [[pydocs-free-threading|自由线程 Python（无 GIL 构建）]] → [[concurrency.free-threading|自由线程（PEP 703，3.13 实验版）与子解释器（PEP 734）]], [[memory.interning-immortal|驻留（interning）与不朽对象（immortal objects，PEP 683）]] · 6 cards
- **The Python 2.3 Method Resolution Order** — [[pydocs-mro-c3|方法解析顺序（MRO）：C3 算法]] → [[classes.inheritance-mro|继承、多重继承、MRO（C3 线性化）与 `super()`]] · 6 cards
- **Sorting Techniques** — [[pydocs-sorting-howto|排序技巧（Sorting Techniques）]] → [[performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]]
- **Functional Programming HOWTO** — [[pydocs-functional-howto|函数式编程 HOWTO]] → [[iteration.iterator-protocol|可迭代对象与迭代器：`__iter__`、`__next__`、`StopIteration`]], [[iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]], [[iteration.itertools|`itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`]], [[functions.functools|`functools`：`lru_cache`、`partial`、`singledispatch`、`cached_property`]], [[functions.first-class|一等函数：作为对象传递、高阶函数与 lambda]] · 24 cards
- **Unicode HOWTO** — [[pydocs-unicode-howto|Unicode HOWTO：字符串与字节的边界]] → [[model.text-bytes|str 与 bytes：Unicode、编码与解码]] · 6 cards
- **Annotations Best Practices** — [[pydocs-annotations-best-practices|注解（Annotations）最佳实践]] → [[types.basics|类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束]] · 6 cards
- **Logging HOWTO** — [[pydocs-logging-howto|日志 HOWTO：从基础用法到多模块配置]] → [[engineering.logging-config|日志与配置：logging 层级、处理器与格式、结构化日志、环境变量配置]] · 6 cards
- **Enum HOWTO** — [[pydocs-enum-howto|Enum HOWTO：枚举成员是类的单例实例]] → [[classes.enums|枚举（Enum）：`Enum`/`IntEnum`/`StrEnum`/`Flag`、`auto()` 与唯一性]] · 7 cards
- **9. Classes** — [[pydocs-tutorial-classes|Python 教程第 9 章：类]] → [[classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]], [[functions.scope-closure|作用域（LEGB）、闭包与 `nonlocal`]], [[classes.inheritance-mro|继承、多重继承、MRO（C3 线性化）与 `super()`]], [[classes.attribute-lookup|属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`]] · 24 cards
- **8. Errors and Exceptions** — [[pydocs-tutorial-errors|Python 教程第 8 章：错误与异常]] → [[runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]
- **5. Data Structures** — [[pydocs-tutorial-datastructures|Python 教程第 5 章：数据结构]] → [[iteration.comprehensions|推导式与 `else` 块：可读性边界与作用域]], [[model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]], [[performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]] · 11 cards
- **6. Modules** — [[pydocs-tutorial-modules|Python 教程第 6 章：模块]] → [[runtime.import-system|导入系统：模块对象、`sys.modules`、包与循环导入]], [[runtime.compile-bytecode|从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存]] · 6 cards
- **15. Floating-Point Arithmetic: Issues and Limitations** — [[pydocs-floating-point-issues|浮点数运算：问题与限制]] → [[model.numbers|数值：int 大整数、float 精度与 Decimal]] · 6 cards
- **Design and History FAQ** — [[pydocs-design-faq|设计与历史 FAQ：CPython 内部实现精选问答]] → [[model.numbers|数值：int 大整数、float 精度与 Decimal]], [[memory.allocator|pymalloc：arena / pool / block 与为何内存不还给操作系统]], [[memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]], [[memory.cyclic-gc|循环垃圾回收：分代（generations）、阈值与增量回收]], [[model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[memory.object-size|对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销]] · 11 cards
- **Programming FAQ** — [[pydocs-programming-faq|编程 FAQ：作用域、参数与可变性高频坑]] → [[functions.scope-closure|作用域（LEGB）、闭包与 `nonlocal`]], [[functions.arguments|参数传递：`*args`/`**kwargs`、仅关键字与仅位置参数、默认值求值时机]], [[model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]], [[model.copy|浅拷贝、深拷贝与切片复制]], [[functions.first-class|一等函数：作为对象传递、高阶函数与 lambda]], [[model.numbers|数值：int 大整数、float 精度与 Decimal]] · 36 cards
- **threading — Thread-based parallelism** — [[pydocs-threading-module|threading 模块：线程、锁与同步原语]] → [[concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]], [[concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]] · 16 cards
- **multiprocessing — Process-based parallelism** — [[pydocs-multiprocessing-module|multiprocessing 模块：绕开 GIL 的真并行]] → [[concurrency.multiprocessing|多进程：`multiprocessing`、fork vs spawn、pickle 边界与共享内存]] · 6 cards
- **concurrent.futures — Launching parallel tasks** — [[pydocs-concurrent-futures|concurrent.futures：线程池与进程池的统一接口]] → [[concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]] · 6 cards
- **queue — A synchronized queue class** — [[pydocs-queue-module|queue 模块：线程安全队列]] → [[concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]] · 5 cards
- **contextvars — Context Variables** — [[pydocs-contextvars|contextvars：按任务隔离的上下文变量]] → [[asyncio.contextvars|上下文变量（contextvars）：为什么线程局部存储在 `await` 之间会失效]] · 6 cards
- **concurrent.interpreters — Multiple interpreters in the same process** — [[pydocs-concurrent-interpreters|concurrent.interpreters：子解释器提供的另一条多核路径]] → [[concurrency.free-threading|自由线程（PEP 703，3.13 实验版）与子解释器（PEP 734）]] · 6 cards
- **Coroutines and tasks** — [[pydocs-asyncio-coroutines-tasks|asyncio：协程与任务完整参考]] → [[asyncio.coroutines-tasks|协程、`await` 与 `Task`：调用协程函数只得到协程对象]], [[asyncio.cancellation|取消：`CancelledError`、清理与不可取消的边界]], [[asyncio.gather-wait-timeout|并发组合：`gather`、`wait`、`wait_for`、`timeout` 与 `TaskGroup`]], [[asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]] · 18 cards
- **Event loop** — [[pydocs-asyncio-eventloop-ref|asyncio 事件循环底层 API 参考]] → [[asyncio.event-loop|事件循环：单线程协作式多任务如何工作]], [[asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]] · 11 cards
- **Futures** — [[pydocs-asyncio-futures|asyncio Future 对象参考]] → [[asyncio.futures|Future：可等待的占位符与回调]] · 6 cards
- **Synchronization Primitives** — [[pydocs-asyncio-sync-primitives|asyncio 同步原语：Lock / Semaphore / Event / Barrier]] → [[asyncio.sync-primitives|异步同步原语与限流：`Semaphore`、`Lock`、`Queue`]] · 6 cards
- **Queues** — [[pydocs-asyncio-queues|asyncio.Queue：异步生产者消费者队列]] → [[asyncio.sync-primitives|异步同步原语与限流：`Semaphore`、`Lock`、`Queue`]] · 6 cards
- **Developing with asyncio** — [[pydocs-asyncio-dev-practices|asyncio 开发实践与调试]] → [[asyncio.debugging|常见 bug 与调试：漏 `await`、循环已在运行、异常被吞、`PYTHONASYNCIODEBUG`]], [[asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]] · 6 cards
- **Runners** — [[pydocs-asyncio-runners|asyncio.run() 与 Runner]] → [[asyncio.event-loop|事件循环：单线程协作式多任务如何工作]] · 5 cards
- **Streams** — [[pydocs-asyncio-streams|asyncio Streams：高层网络 I/O]] → [[asyncio.streams-protocols|网络层：Streams、Transports/Protocols 与 aiohttp 类客户端的用法]] · 6 cards
- **Transports and Protocols** — [[pydocs-asyncio-transports-protocols|asyncio Transports 与 Protocols：底层网络 API]] → [[asyncio.streams-protocols|网络层：Streams、Transports/Protocols 与 aiohttp 类客户端的用法]] · 6 cards
- **asyncio and free-threaded Python** — [[pydocs-asyncio-free-threading|asyncio 与自由线程 Python]] → [[concurrency.free-threading|自由线程（PEP 703，3.13 实验版）与子解释器（PEP 734）]], [[asyncio.blocking-and-threads|阻塞调用与线程的交界：`to_thread`、`run_in_executor`、`run_coroutine_threadsafe`]] · 12 cards
- **gc — Garbage Collector interface** — [[pydocs-gc-module|gc 模块：垃圾回收器接口]] → [[memory.cyclic-gc|循环垃圾回收：分代（generations）、阈值与增量回收]]
- **weakref — Weak references** — [[pydocs-weakref-module|weakref 模块：弱引用]] → [[memory.weakref|弱引用：`weakref`、`WeakValueDictionary` 与缓存]] · 5 cards
- **copy — Shallow and deep copy operations** — [[pydocs-copy-module|copy 模块：浅拷贝与深拷贝]] → [[model.copy|浅拷贝、深拷贝与切片复制]] · 6 cards
- **sys — System-specific parameters and functions** — [[pydocs-sys-module|sys 模块：解释器内部状态入口]] → [[runtime.frames-eval|求值循环与帧：调用栈、递归限制与尾调用]], [[memory.interning-immortal|驻留（interning）与不朽对象（immortal objects，PEP 683）]], [[memory.object-size|对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销]], [[runtime.import-system|导入系统：模块对象、`sys.modules`、包与循环导入]] · 6 cards
- **tracemalloc — Trace memory allocations** — [[pydocs-tracemalloc|tracemalloc：追踪内存分配]] → [[memory.leaks-tracemalloc|长驻进程的内存泄漏：来源、`tracemalloc` 与 `gc.get_referrers`]] · 5 cards
- **functools — Higher-order functions and operations on callable objects** — [[pydocs-functools-module|functools 模块：高阶函数工具箱]] → [[functions.functools|`functools`：`lru_cache`、`partial`、`singledispatch`、`cached_property`]], [[functions.decorators|装饰器：`@` 语法糖、`functools.wraps` 与执行时机]] · 12 cards
- **itertools — Functions creating iterators for efficient looping** — [[pydocs-itertools-module|itertools 模块：惰性迭代器工具]] → [[iteration.itertools|`itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`]] · 6 cards
- **contextlib — Utilities for with-statement contexts** — [[pydocs-contextlib-module|contextlib 模块：上下文管理器工具箱]] → [[iteration.context-managers|上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`]] · 6 cards
- **dataclasses — Data Classes** — [[pydocs-dataclasses-module|dataclasses 模块：数据类完整参考]] → [[classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]] · 7 cards
- **collections — Container datatypes** — [[pydocs-collections-module|collections 模块：专用容器数据类型]] → [[runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]], [[performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]] · 6 cards
- **collections.abc — Abstract Base Classes for Containers** — [[pydocs-collections-abc|collections.abc：容器的抽象基类]] → [[classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]] · 7 cards
- **abc — Abstract Base Classes** — [[pydocs-abc-module|abc 模块：抽象基类机制]] → [[classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]] · 7 cards
- **typing — Support for type hints** — [[pydocs-typing-module|typing 模块：类型提示完整参考]] → [[types.basics|类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束]], [[types.gradual-typing|渐进类型（gradual typing）、`Any` 与 mypy/pyright 的检查模型]], [[types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]], [[types.typeddict-literal|`TypedDict`、`Literal`、`NewType` 与 dataclass 注解]] · 23 cards
- **Built-in Exceptions** — [[pydocs-builtin-exceptions|内建异常完整参考]] → [[runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]
- **decimal — Decimal fixed-point and floating-point arithmetic** — [[pydocs-decimal-module|decimal 模块：精确十进制运算]] → [[model.numbers|数值：int 大整数、float 精度与 Decimal]], [[engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]] · 12 cards
- **datetime — Basic date and time types** — [[pydocs-datetime-module|datetime 模块：日期时间完整参考]] → [[engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]], [[runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]] · 12 cards
- **pickle — Python object serialization** — [[pydocs-pickle-module|pickle 模块：Python 对象序列化]] → [[engineering.serialization|序列化：`json`、`pickle` 的安全与版本、`copyreg` 与 dataclass 的转换]], [[runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]] · 12 cards
- **json — JSON encoder and decoder** — [[pydocs-json-module|json 模块：JSON 编解码]] → [[engineering.serialization|序列化：`json`、`pickle` 的安全与版本、`copyreg` 与 dataclass 的转换]] · 6 cards
- **heapq — Heap queue algorithm** — [[pydocs-heapq-module|heapq 模块：堆队列算法]] → [[runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]] · 6 cards
- **bisect — Array bisection algorithm** — [[pydocs-bisect-module|bisect 模块：有序数组二分查找]] → [[runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]] · 6 cards
- **array — Efficient arrays of numeric values** — [[pydocs-array-module|array 模块：紧凑数值数组]] → [[performance.less-ram|省内存：生成器、`array`、`memoryview`、`__slots__` 与稀疏结构]], [[model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]] · 12 cards
- **Built-in Types** — [[pydocs-builtin-types|内建类型（Built-in Types）完整参考]] → [[model.numbers|数值：int 大整数、float 精度与 Decimal]], [[model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]], [[model.text-bytes|str 与 bytes：Unicode、编码与解码]], [[model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[types.basics|类型提示基础：`Optional`、`Union`/`|`、泛型容器与运行时零约束]] · 24 cards
- **dis — Disassembler for Python bytecode** — [[pydocs-dis-module|dis 模块：字节码反汇编]] → [[runtime.compile-bytecode|从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存]]
- **timeit — Measure execution time of small code snippets** — [[pydocs-timeit-module|timeit 模块：微基准测试]] → [[performance.profiling|先测量：`timeit`、`cProfile`、采样剖析器与内存剖析]] · 6 cards
- **The Python Profilers** — [[pydocs-profilers|Python Profilers：cProfile 与 profile]] → [[performance.profiling|先测量：`timeit`、`cProfile`、采样剖析器与内存剖析]] · 6 cards
- **unittest.mock — mock object library** — [[pydocs-unittest-mock|unittest.mock：模拟对象库]] → [[engineering.testing|测试：pytest 夹具与参数化、`unittest.mock`、注入时钟与依赖]] · 5 cards
- **logging — Logging facility for Python** — [[pydocs-logging-module-ref|logging 模块：完整 API 参考]] → [[engineering.logging-config|日志与配置：logging 层级、处理器与格式、结构化日志、环境变量配置]] · 6 cards
- **warnings — Warning control** — [[pydocs-warnings-module|warnings 模块：警告控制]] → [[engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]] · 7 cards
- **venv — Creation of virtual environments** — [[pydocs-venv-module|venv 模块：虚拟环境]] → [[engineering.packaging-env|依赖与环境：虚拟环境、`pyproject.toml`、锁文件与 uv/pip]] · 3 cards

## Leaves this corpus never reached (8)
Your reading list: the map says these exist and the book does not teach them.
- [[functions.decorator-patterns|带参数的装饰器、类装饰器与常见实例（retry、memoize、timing、rate limit）]] — 掌握三层嵌套的参数化装饰器、用类实现带状态的装饰器、装饰方法时 `self` 的传递，以及缓存/重试/限流装饰器的设计要点与可测试性（注入时钟）。
- [[iteration.yield-from|`yield from` 与生成器的 `send`/`throw`/`close`]] — 掌握 `yield from` 如何委托子生成器并透传值与异常、`send()` 让生成器成为经典协程，以及这套机制为何是 async/await 的前身。
- [[iteration.pattern-matching|结构化模式匹配：`match`/`case`、捕获、守卫与类模式]] — 理解 3.10 的 `match` 不是 switch：模式会解构序列、映射与类实例并绑定名字，`case _` 兜底、`if` 守卫、`__match_args__` 决定位置模式，以及什么时候一串 `if` 反而更清楚。
- [[concurrency.choosing|选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树]] — 能在面试里用一句话给出结论：阻塞库 + I/O 用线程，CPU 用进程或换成 NumPy/DuckDB，高并发 I/O 且有 async 库用 asyncio，并说出每种选择的代价。
- [[runtime.adaptive-jit|自适应解释器（PEP 659）与实验性 JIT（PEP 744）]] — 理解 3.11 起的特化（specializing）字节码如何按运行时类型内联快速路径，3.13 的 copy-and-patch JIT 处于实验阶段，以及这对"Python 慢"的回答意味着什么。
- [[performance.numpy-vectorization|NumPy 向量化与内存布局：ndarray、广播、连续内存与视图]] — 理解向量化把循环下推到 C、连续内存与缓存友好、切片是视图而非拷贝、广播规则，以及为什么 Python 层 `for` 循环比向量化慢一到两个量级。
- [[performance.pandas-at-scale|pandas 大表：分块读取、dtype 与 category、`groupby` 与合并、写时复制]] — 掌握 `read_csv(chunksize=, usecols=, dtype=)` 控制内存、分块聚合再合并的 map-reduce 形态、`merge_asof` 做时间对齐、`validate=` 抓重复键，以及 2.x 写时复制（Copy-on-Write）对 `SettingWithCopy` 的影响。
- [[performance.compiling|编译与本地扩展：Cython、Numba、`ctypes` 与何时换引擎]] — 理解把热点编译为 C 的三条路径与各自的代价、NumPy/Numba 释放 GIL 的条件，以及"把计算推给 DuckDB/SQL 引擎"往往比优化 Python 循环更划算。
%% trellis:end %%

## Notes
