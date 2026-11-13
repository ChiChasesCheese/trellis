---
id: tr-test-infra-framework-architecture-pytest
node: test-infra.framework-architecture
type: qa
step: 2
---
## Q
用 pytest 搭一个分层的测试框架时，资源、驱动、测试逻辑、报告这几层分别用 pytest 的什么机制实现？

## A
- **资源层 → fixture**：用 `@pytest.fixture(scope="session")` 管理贵的资源（申请设备、启动服务），`yield` 之前准备、之后清理；清理写在 `yield` 之后，测试失败也会执行。
- **驱动层 → 普通 Python 类**：由 fixture 构造并注入测试，测试只拿到 `client`，看不到端口和进程。
- **测试逻辑 → 测试函数 + `parametrize`**：同一逻辑跑多组输入或多种配置。
- **选择与分档 → marker**：`@pytest.mark.hardware`、`@pytest.mark.nightly`，配合 `-m "not hardware"` 选择；在 `pytest.ini` 的 `markers` 里登记，并开 `--strict-markers` 防止拼错。
- **报告与扩展 → 插件钩子（hook）**：`conftest.py` 或独立插件里实现 `pytest_addoption`（加命令行参数，如 `--target=sim`）、`pytest_collection_modifyitems`（按资源过滤用例）、`pytest_runtest_makereport`（失败时收集日志附件）。报告用 `--junitxml=report.xml`。

```python
def pytest_addoption(parser):
    parser.addoption("--target", default="sim")   # sim 或 hw

@pytest.fixture(scope="session")
def server(request):
    target = request.config.getoption("--target")
    srv = launch_server(target)        # 资源层：申请设备并启动
    yield srv
    srv.shutdown()                     # 失败也会执行

@pytest.fixture
def client(server):
    return InferenceClient(server.url, timeout=30)   # 驱动层

@pytest.mark.parametrize("n", [1, 16, 512])
def test_returns_n_tokens(client, n):
    assert len(client.generate("hi", max_tokens=n).tokens) == n
```

`max_tokens` 是最多生成多少个 token；token 是模型处理文字的最小单位，约等于一个词或词的一部分。同一套用例用 `--target=hw` 就能在真机上跑，测试函数不改。
