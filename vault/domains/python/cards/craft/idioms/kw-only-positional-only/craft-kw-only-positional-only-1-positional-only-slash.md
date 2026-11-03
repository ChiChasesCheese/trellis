---
id: craft-kw-only-positional-only-1-positional-only-slash
node: craft.idioms.kw-only-positional-only
type: qa
step: 1
---
## Q
**参数形态 · 日志函数为什么要用 `/` 把前两个参数锁成仅位置**｜写法

`log(level, message, **context)` 允许调用方附带任意业务字段：`log.info("冲突", level="P1")`，这里的 `level` 是业务里的优先级，碰巧与形参同名。会发生什么？函数签名里的 `/` 起什么作用，另外还有什么好处？

## A
**要点。** 一个函数既有具名形参，又有收集任意关键字的 `**context`，两者共用同一个关键字命名空间：调用方的业务字段一旦与形参重名就冲突。`/` 之前的形参是仅位置（positional-only）的：不占用关键字名字，调用方用同名关键字时会被放进 `**context`。这样「形参叫什么」不再是公共接口的一部分，以后可以改名而不破坏调用方。

```python
def log_plain(level: str, message: str, **context: object) -> dict:
    return {"_lvl": level, "_msg": message, **context}

def log(level: str, message: str, /, **context: object) -> dict:
    return {"_lvl": level, "_msg": message, **context}

try:
    log_plain("INFO", "冲突", level="P1")           # 业务字段碰巧也叫 level
except TypeError as e:
    print("TypeError:", e)
print(log("INFO", "冲突", level="P1"))              # 仅位置：形参名不占关键字命名空间

def area(w, h): return w * h
def area2(width, height, /): return width * height
print(area(w=2, h=3))                               # 有人按关键字调用，形参名就成了公共 API
try:
    area2(width=2, height=3)
except TypeError as e:
    print("TypeError:", e)
```

实际输出：

```
TypeError: log_plain() got multiple values for argument 'level'
{'_lvl': 'INFO', '_msg': '冲突', 'level': 'P1'}
6
TypeError: area2() got some positional-only arguments passed as keyword arguments: 'width, height'
```

**为什么。** 第二行里业务字段 `level='P1'` 作为上下文被原样保留，日志本身的级别仍是 `INFO`。方法的 `self` 本来就是仅位置的，`def bind(self, /, **context)` 里写出 `/` 是为了让业务字段 `self` 也能当关键字传入。

**易错。** 只收少数几个形参、没有 `**kwargs` 的函数不用 `/`：它防的是命名空间冲突，没有冲突风险时只是增加噪音。内置的 `len(obj, /)` 用它，是为了保留改形参名的自由。
