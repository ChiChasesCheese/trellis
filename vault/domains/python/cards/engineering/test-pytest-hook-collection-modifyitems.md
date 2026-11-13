---
id: test-pytest-hook-collection-modifyitems
node: engineering.testing
type: qa
---
## Q
要求：标了 `slow` 的测试默认跳过，只有加 `--run-slow` 才跑；另外希望 `smoke` 测试总是排在最前面跑。用哪个钩子实现？它能对收集到的测试做哪些事？

## A
**用 `pytest_collection_modifyitems(config, items)`：收集完成、开始运行之前调用一次，`items` 是全部测试项的列表，你可以给它们加标记、排序或删掉一部分。**

```python
def pytest_addoption(parser):
    parser.addoption("--run-slow", action="store_true")

def pytest_collection_modifyitems(config, items):
    items.sort(key=lambda it: it.get_closest_marker("smoke") is None)  # smoke 先跑
    if config.getoption("--run-slow"):
        return
    skip_slow = pytest.mark.skip(reason="需要 --run-slow")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
```

- **能做的四件事：** 给测试加标记（上例加 `skip`）；原地重排 `items`（`sort` 是稳定的，其余顺序不变）；删除测试（从 `items` 里移除，并调用 `config.hook.pytest_deselected(items=removed)` 让报告中显示为 deselected）；读取每个测试的信息（`item.nodeid`、`item.get_closest_marker`、`item.keywords`）做统计。
- **为什么用 skip 而不是直接删：** 加 skip 的测试仍出现在报告中，带着原因，大家知道它存在、为什么没跑；直接删掉就悄无声息。
- **必须原地修改：** 改的是传进来的 `items` 列表本身，给它重新赋值不会生效。
- **典型用途：** 按命令行开关跳过一类测试、把历史最慢的测试放前面让并行更均衡、按改动文件只保留相关测试（测试选择，test selection）、为没打任何分层标记的测试统一补上默认标记。
- **注意执行时机：** 它在 `-k` / `-m` 过滤之前还是之后取决于插件顺序；需要确定先后时用 `@pytest.hookimpl(tryfirst=True)` 或 `trylast=True`。
