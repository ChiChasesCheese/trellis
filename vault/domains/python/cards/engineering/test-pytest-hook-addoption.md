---
id: test-pytest-hook-addoption
node: engineering.testing
type: qa
---
## Q
同一套测试要能对不同的后端跑：`pytest --device=cpu` 或 `pytest --device=gpu`，并且测试里能拿到这个值。pytest 里怎么加一个自定义命令行选项？钩子（hook）是什么？

## A
**钩子是 pytest 在固定时刻调用的、名字以 `pytest_` 开头的函数；你在 `conftest.py` 或插件里定义同名函数，pytest 就会在那个时刻调用它。加选项用 `pytest_addoption`，读选项用 `config.getoption`。**

```python
# 根目录 conftest.py
def pytest_addoption(parser):
    parser.addoption("--device", default="cpu", choices=["cpu", "gpu"],
                     help="测试针对哪个后端")

@pytest.fixture(scope="session")
def device(pytestconfig):            # 内置 fixture，等于 request.config
    return pytestconfig.getoption("device")

def test_matmul(device):
    run_on(device)
```

- **必须放在根 `conftest.py`（或插件里）：** 命令行在收集测试之前就要解析，子目录里的 `conftest.py` 加载得太晚，在那里定义 `pytest_addoption` 可能不生效。
- **`choices` 和 `default`：** 让拼错的值在启动时就报错，而不是跑到一半才发现。`pytest --help` 会把 `help` 文本列在自定义选项里。
- **读取的三个入口：** fixture 里用 `pytestconfig.getoption("device")` 或 `request.config.getoption(...)`；钩子里用传进来的 `config`；测试项上用 `item.config`。
- **常见用途：** 选择被测后端或硬件、指定被测构建的路径（`--build=/path/to/artifact`）、打开慢测试（`--run-slow`）、设置结果上传地址。
- **钩子的整体图景：** pytest 本身就是一组插件，通过几十个钩子串起来：启动时的 `pytest_configure`，收集阶段的 `pytest_collection_modifyitems`，每个测试的 `pytest_runtest_setup` / `call` / `teardown`，报告阶段的 `pytest_runtest_makereport` 和 `pytest_terminal_summary`。写 `conftest.py` 就是在给自己的项目写本地插件。
