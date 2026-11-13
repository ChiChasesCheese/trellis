---
id: test-pytest-hook-makereport
node: engineering.testing
type: qa
---
## Q
测试失败时，希望自动把被测服务的最后 50 行日志附到报告中，并在整次运行结束时打印一行汇总（多少个测试超过 10 秒）。用哪些报告钩子？「包装钩子（wrapper）」是什么？

## A
**每个测试的结果由 `pytest_runtest_makereport` 生成；用包装钩子拿到 pytest 生成的报告对象再加工。整次运行结束时用 `pytest_terminal_summary` 输出汇总。**

```python
@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    rep = yield                         # 先让 pytest 生成报告
    if rep.when == "call" and rep.failed:
        rep.sections.append(("server log", tail_server_log(50)))
    if rep.when == "call" and rep.duration > 10:
        item.config.stash.setdefault(SLOW, []).append(item.nodeid)
    return rep

def pytest_terminal_summary(terminalreporter, config):
    slow = config.stash.get(SLOW, [])
    terminalreporter.write_line(f"{len(slow)} 个测试超过 10 秒")
```

（`SLOW = pytest.StashKey[list]()` 定义在模块顶部。）

- **包装钩子：** `yield` 之前的代码在其他实现之前运行，`yield` 把控制交给它们，返回值就是它们生成的结果，你改完再 `return`。这是「在别人的结果上加东西」的标准写法。旧写法是 `hookwrapper=True`，`outcome = yield` 再 `outcome.get_result()`。
- **`rep.when`：** 每个测试会生成三份报告：`setup`、`call`、`teardown`。只关心测试体本身就判断 `when == "call"`；准备阶段失败时 `setup` 那份是 failed。
- **`rep.sections`：** 追加的段落会作为单独一节出现在终端的失败详情里。要让 CI 的 XML 报告中也有，另用 `record_property` 或把日志写成构建产物（artifact）。
- **跨测试保存数据：** 用 `config.stash` 或 `item.stash`，比给对象随手加属性安全。
- **插件的两种形态：** 写在 `conftest.py` 里只对本项目生效；做成安装包并在 `pyproject.toml` 里登记 `pytest11` 入口点（entry point），装上就对任何项目生效。`-p no:name` 可以禁用某个插件。
