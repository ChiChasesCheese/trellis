---
id: test-pytest-custom-markers-strict
node: engineering.testing
type: qa
---
## Q
团队想把测试分成 `smoke`（每次提交跑）、`nightly`（每晚跑）、`gpu`（需要专用硬件）三类，用自定义标记（marker）实现。标记怎么注册？为什么一定要开 `--strict-markers`？怎么给整个模块或某一个参数组合打标记？

## A
**在配置里登记标记，开 `--strict-markers` 让拼错的标记直接报错，再用 `-m` 按标记选套件。**

```ini
# pytest.ini
[pytest]
addopts = --strict-markers
markers =
    smoke: 每次提交都跑的快速测试
    nightly: 只在夜间全量回归里跑
    gpu: 需要 GPU 机器
```

```python
pytestmark = pytest.mark.nightly             # 整个模块都打上

@pytest.mark.parametrize("batch", [
    1, 8,
    pytest.param(256, marks=pytest.mark.gpu),  # 只给这一组参数打标记
])
def test_throughput(batch): ...
```

- **为什么要 strict：** 不开时，`@pytest.mark.slwo`（拼错）只产生一条警告，测试照样跑，但 `-m "not slow"` 选不掉它，夜间才跑的慢测试就混进了提交检查。开了以后拼错直接在收集阶段报错，报错信息是 `'slwo' not found in markers configuration option`。
- **注册的另一个好处：** `pytest --markers` 列出所有标记和说明，新人知道有哪些分类。
- **三种打法：** 装饰器打在函数或类上；模块级变量 `pytestmark` 作用于整个文件；`pytest.param(..., marks=...)` 只作用于一个参数组合。
- **CI 里怎么用：** 提交检查 `pytest -m smoke`，夜间 `pytest -m "not gpu"`，GPU 机器上 `pytest -m gpu`。标记也能在钩子里读：`item.get_closest_marker("gpu")`。
- **约束：** 标记只是标签，它不会自己跳过测试。「没加选项就跳过 slow」这类行为要靠 `pytest_collection_modifyitems` 钩子实现。
