---
id: test-pytest-fixture-scope-yield-teardown
node: engineering.testing
type: qa
---
## Q
一个测试套件要先启动一个很慢的被测服务（每次约 20 秒），每个测试再各自开一个客户端连接。用 pytest fixture（夹具）怎么写？`scope` 有哪几种，`yield` 之后的清理代码在什么时候、按什么顺序执行？

## A
**写法：服务用大作用域，客户端用默认的函数作用域，客户端依赖服务。**

```python
@pytest.fixture(scope="module")
def server():
    proc = start_server()        # 只在本模块第一次用到时启动
    yield proc                   # yield 之前是准备，之后是清理
    proc.terminate()

@pytest.fixture                  # 默认 scope="function"
def client(server):              # fixture 可以依赖别的 fixture
    c = connect(server)
    yield c
    c.close()
```

- **五种作用域（scope）：** `function`（默认，每个测试一份）、`class`、`module`、`package`、`session`（整次运行一份）。作用域越大，创建次数越少，但测试之间共享的状态越多。
- **清理一定会执行：** 测试断言失败或抛异常，`yield` 之后的代码照样运行。但如果 fixture 在 `yield` **之前**就抛了异常，它自己的清理不会执行，所以准备步骤多时要逐个加 `request.addfinalizer` 或在 `yield` 前用 `try`。
- **清理顺序是后进先出（LIFO）：** 先建的后拆。上例里是「关客户端 → 停服务」，`pytest --setup-show` 能把 SETUP / TEARDOWN 的顺序打印出来。
- **作用域只能往大的依赖：** `session` 的 fixture 不能依赖 `function` 的 fixture，否则 pytest 报 `ScopeMismatch`。
- **代价：** 大作用域的对象被多个测试共享，一个测试改了它的状态会污染后面的测试。常见做法是「贵的资源放大作用域，每个测试再用一个函数作用域的 fixture 把状态重置干净」。
