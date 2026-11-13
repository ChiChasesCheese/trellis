---
id: test-pytest-fixture-factory-request
node: engineering.testing
type: qa
---
## Q
一个测试要创建三个配置不同的任务对象，而且每个都必须在测试结束后删掉。一个普通 fixture 只能返回一个值，怎么办？`request` 这个内置 fixture 能拿到什么？

## A
**用「工厂 fixture（factory as fixture）」：fixture 返回一个创建函数，函数每被调一次就记下创建的对象，测试结束时统一清理。**

```python
@pytest.fixture
def make_job(tmp_path):
    created = []
    def _make(name, retries=0):
        job = Job(name, workdir=tmp_path / name, retries=retries)
        created.append(job)
        return job
    yield _make
    for job in reversed(created):   # 后建的先删
        job.delete()

def test_retry_order(make_job):
    a, b = make_job("a"), make_job("b", retries=2)
    ...
```

- **为什么不用三个 fixture：** 数量和参数由测试决定，写死成三个 fixture 既不灵活也会重复。工厂把「怎么建、怎么清」集中在一处，测试只表达「我要什么」。
- **组合（composition）：** fixture 可以依赖别的 fixture（上例依赖 `tmp_path`），小 fixture 拼成大 fixture，比一个巨型 `setup` 函数更容易复用。
- **`request` 能拿到的东西：** `request.node`（当前测试项，可读它的名字和标记）、`request.config`（命令行选项和配置）、`request.param`（参数化 fixture 当前的参数）、`request.addfinalizer(fn)`（注册清理函数，和 `yield` 等价，可以注册多个）、`request.getfixturevalue("name")`（运行时按名字取另一个 fixture）。
- **常见用法：** 根据测试上的标记决定准备什么，比如 `request.node.get_closest_marker("gpu")` 存在时才去申请一块 GPU。
