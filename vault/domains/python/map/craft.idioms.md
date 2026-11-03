%% trellis:begin %%
# 高级写法（Idioms）
*编码功力（Coding Craft）*

真实代码里的 Python 用法：底层做了什么、朴素写法的代价、什么时候不该用。

## Topics
- [[domains/python/map/craft.idioms.frozen-value-objects|不可变值对象（frozen + slots dataclass as value object）]]
- [[domains/python/map/craft.idioms.exception-family|异常家族：基类 + 多重继承 + 携带数据（typed errors）]]
- [[domains/python/map/craft.idioms.protocol-callable-abc|策略接口三选一：Callable / Protocol / ABC]]
- [[domains/python/map/craft.idioms.validated-construction|构造即校验与规范化（__post_init__ + object.__setattr__）]]
- [[domains/python/map/craft.idioms.read-only-views-and-snapshots|只读视图与快照返回（MappingProxyType / tuple / frozenset）]]
- [[domains/python/map/craft.idioms.context-managers-for-invariants|上下文管理器守不变量：@contextmanager 与 ExitStack]]
- [[domains/python/map/craft.idioms.heapq-tuple-ordering|heapq 的元组序与 tie-break：计数器、负号、dataclass(order=True)]]
- [[domains/python/map/craft.idioms.event-wait-and-handoff|Event / Condition 的惯用法：中断式睡眠、结果交接、截止时间]]
- [[domains/python/map/craft.idioms.money-types|金额类型选型：整数分 / 基点 / Decimal / Fraction]]
- [[domains/python/map/craft.idioms.round-once-at-the-boundary|取整点：Decimal.quantize、ROUND_HALF_EVEN 与整数四舍五入]]
- [[domains/python/map/craft.idioms.time-types|时间类型选型：monotonic / aware datetime / 整数时间戳]]
- [[domains/python/map/craft.idioms.match-structural|结构化模式匹配：对 dataclass 与枚举的 match / case]]
- [[domains/python/map/craft.idioms.exhaustive-match-assert-never|穷尽性：match 加 assert_never（解法没用，应该用）]]
- [[domains/python/map/craft.idioms.replace-for-state-change|用 dataclasses.replace 整体替换，而不是原地改（immutable record swap）]]
- [[domains/python/map/craft.idioms.decorators-for-cross-cutting-locks|装饰器做横切关注点：@_synchronized / @_op 与 functools.wraps]]
- [[domains/python/map/craft.idioms.bisect-sorted-lists|bisect 与有序列表：floor/ceiling、key=、只查邻居]]
- [[domains/python/map/craft.idioms.generators-lazy-traversal|生成器管线与显式栈：惰性遍历 + pairwise / islice]]
- [[domains/python/map/craft.idioms.default-forms|省掉标志变量：next(…, None) / min(default=) / for-else / 海象运算符]]
- [[domains/python/map/craft.idioms.closure-factory-policies|闭包工厂做策略（closure factory）]]
- [[domains/python/map/craft.idioms.enum-behaviour|Enum 的行为：IntEnum 排序、属性、StrEnum 与生命周期顺序]]
- [[domains/python/map/craft.idioms.id-generation|ID 生成：itertools.count、next 与生成器表达式的陷阱]]
- [[domains/python/map/craft.idioms.dunder-protocols-that-pay|值得写的特殊方法：__bool__ / __len__ / __contains__ / __and__ / __call__ / __enter__]]
- [[domains/python/map/craft.idioms.sentinels|哨兵值：object()、math.inf、毒丸与「None 是合法值」]]
- [[domains/python/map/craft.idioms.dispatch-tables|数据驱动的分派表：operator 表、方向表、转换表]]
- [[domains/python/map/craft.idioms.bounded-deque|deque(maxlen) 做有界历史；list 头部删除是 O(n)]]
- [[domains/python/map/craft.idioms.copy-in-copy-out|边界拷贝：进来拷、出去拷（deepcopy / tuple / 回放式 copy）]]
- [[domains/python/map/craft.idioms.memoize-on-frozen|记忆化：lru_cache 要求参数可哈希、结果不可变]]
- [[domains/python/map/craft.idioms.kw-only-positional-only|参数形态：仅位置 `/`、仅关键字 `*`、kw_only dataclass]]
- [[domains/python/map/craft.idioms.slots-and-memory|__slots__ 与 slots=True：该用在哪、不能用在哪]]
- [[domains/python/map/craft.idioms.namedtuple-for-keys|NamedTuple 做复合键与轻量返回值]]
- [[domains/python/map/craft.idioms.literal-and-closed-sets|封闭取值集：Literal / Enum / StrEnum 的选型]]
- [[domains/python/map/craft.idioms.generics-and-type-aliases|泛型与类型别名：Generic/TypeVar、Clock 别名、Self 与 override]]
- [[domains/python/map/craft.idioms.descriptors-where-they-earn|描述符：什么时候值得（共享字段规则），什么时候不值得]]
- [[domains/python/map/craft.idioms.init-subclass-registry|__init_subclass__ 注册表 vs 手写 dict（create_cache 的取舍）]]
%% trellis:end %%

## Notes
