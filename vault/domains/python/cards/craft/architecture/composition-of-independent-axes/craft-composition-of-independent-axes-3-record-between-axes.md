---
id: craft-composition-of-independent-axes-3-record-between-axes
node: craft.architecture.composition-of-independent-axes
type: qa
step: 3
---
## Q
**独立变化轴的组合 · 日志框架里格式化、阈值、过滤器怎么互不干扰**｜架构

日志要支持：人读的文本和机器读的 JSON 两种格式；控制台只要 INFO 以上、审计文件要 DEBUG 全收但只要支付模块；每个输出各有自己的规则。如果这些都写在 logger 里，每加一种输出就要改 logger。几条轴之间怎么连接？

## A
**要点。** 三条轴：格式化器（怎么变成一行）、阈值与过滤器（要不要）、输出处理器（写到哪）。它们之间唯一共享的是冻结的 `LogRecord`：一次日志事件的完整快照，可以安全交给任意多个处理器、跨线程传递，处理器永远不需要回头问 logger 任何事。每个处理器自己持有阈值、格式化器、过滤器。

```python
class Level(IntEnum):
    DEBUG = 10; INFO = 20; ERROR = 40

@dataclass(frozen=True)
class Record:                               # 三条轴之间唯一的共享对象
    name: str
    level: Level
    message: str

class TextFormatter:
    def format(self, r: Record) -> str: return f"[{r.level.name}] {r.name}: {r.message}"
class JsonFormatter:
    def format(self, r: Record) -> str: return json.dumps({"lvl": r.level.name, "msg": r.message}, ensure_ascii=False)

class Handler:                              # 阈值、格式化器、过滤器都归它自己
    def __init__(self, out, level=Level.DEBUG, fmt=None, filters=()):
        self.out, self.level, self.fmt, self.filters = out, level, fmt or TextFormatter(), filters
    def handle(self, r: Record) -> bool:
        if r.level < self.level or not all(f(r) for f in self.filters):
            return False
        self.out.write(self.fmt.format(r) + "\n")    # 格式化是纯计算，写出才需要锁
        return True

console, audit = io.StringIO(), io.StringIO()
handlers = [
    Handler(console, Level.INFO),                                         # 人读，INFO 及以上
    Handler(audit, Level.DEBUG, JsonFormatter(), [lambda r: r.name == "pay"]),   # 机器读，只要 pay 的日志
]
for r in (Record("pay", Level.DEBUG, "开始扣款"), Record("pay", Level.ERROR, "扣款失败"), Record("ui", Level.INFO, "点击")):
    print(r.message, "->", [h.handle(r) for h in handlers])
print("console:", console.getvalue().splitlines())
print("audit  :", audit.getvalue().splitlines())
```

两个处理器：控制台（INFO 起，文本）；审计（DEBUG 起，JSON，只要名字是 `pay`）。三条记录，实际输出：

```
开始扣款 -> [False, True]
扣款失败 -> [True, True]
点击 -> [True, False]
console: ['[ERROR] pay: 扣款失败', '[INFO] ui: 点击']
audit  : ['{"lvl": "DEBUG", "msg": "开始扣款"}', '{"lvl": "ERROR", "msg": "扣款失败"}']
```

**为什么。** 记录冻结，所以格式化可以放在锁外，只有真正写出的一步才需要加锁：锁保护的是「一行不被另一行插进来」，不是 CPU 时间。过滤器只是一个函数，不需要类。

**易错。** 格式化器如果需要的信息记录里没有，就别让它回头查 logger：应该在构造记录时就带上（线程名、上下文）。
