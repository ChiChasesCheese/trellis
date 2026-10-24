---
id: pl-trends-effects-foundation-algebraic
node: trends.effects
type: qa
step: 4
---
## Q
代数效应（algebraic effect）和处理器（handler）是什么？用一个小例子说明同一段业务代码怎样换不同的处理器。

## A
代数效应把效应拆成两部分：

1. **操作**（operation）：业务代码在需要外部帮助的地方，写下「我要做某件事」，如 `ask("host")`（我需要配置项 `host`）、`abort("bad port")`（我想中止）。业务代码不知道这件事怎么完成。
2. **处理器**（handler）：由外层代码提供，决定每个操作的含义，并可以决定**要不要、何时、用什么值恢复**业务代码继续执行。

业务代码执行到操作时被暂停，把「接下来要做的事」交给处理器（这个剩余的计算叫**续延**，continuation）；处理器可以：恢复一次（普通函数返回）、不恢复（相当于抛异常）、稍后恢复（相当于异步）、多次恢复（相当于非确定性）。因此异常、生成器、异步、状态、读环境，都能用同一套机制表达。

Python 的生成器可以模拟出这个模型：`yield` 就是执行操作，驱动循环就是处理器：

```python
# Ask(key) and Abort(why) are small classes that carry a request
def program():                     # business logic: no I/O, no try/except
    host = yield Ask("host")
    port = yield Ask("port")
    if port == "0":
        yield Abort("bad port")
    return f"{host}:{port}"
```

驱动循环负责把每个请求交给处理器，再把答复送回业务代码；处理器抛出异常就等于「不恢复」：

```python
def run(prog, handler):            # the handler gives each effect a meaning
    gen = prog(); reply = None
    try:
        while True:
            reply = handler(gen.send(reply))
    except StopIteration as done:
        return done.value
    except Exception as e:
        return f"aborted: {e}"
```

用「真实环境」处理器（`host=db, port=5432`）运行，得到 `db:5432`；用「测试环境」处理器（`port=0`）运行同一个 `program`，得到 `aborted: bad port`。业务代码没有改动，没有依赖注入框架，也没有 mock。

这个模拟只有一层、一次性的限制；真正的代数效应由语言实现，可以出现在调用栈任意深处，嵌套的处理器各管各的操作。

好处：

- **业务代码与外部世界解耦**：测试、重放、模拟都只是换处理器；
- **统一**：异常、协程、异步、状态不再是各自的特殊语法；
- **效应出现在类型里时**（Koka），编译器知道哪些函数是纯的。

要记住：代数效应是「可恢复的异常」，处理器就是 `catch` 加上 `resume`。
