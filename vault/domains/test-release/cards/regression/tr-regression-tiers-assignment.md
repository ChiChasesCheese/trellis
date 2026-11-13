---
id: tr-regression-tiers-assignment
node: regression.tiers
type: qa
step: 3
---
## Q
一条测试应该放进哪一档？在 pytest 里怎么把测试分档并让不同流水线跑不同的档？

## A
**分配依据**，按顺序考虑：
- **运行时间**：单条超过档的预算就不能放进去，例如一条 20 分钟的测试不能进提交前。
- **稳定性**：flaky 率高的测试不进提交前，否则会频繁挡住无辜的改动；先修稳再晋升。
- **资源**：需要稀缺硬件（多节点、专用加速卡）的测试放提交后或夜间，避免每个改动都去排队。
- **信号价值**：最常抓到回归、覆盖最核心路径的测试尽量往前放，越早发现越便宜。
- **与改动的关系**：只在特定模块改动时才有意义的测试，可以用测试选择只在相关改动时进提交前。

**pytest 里的做法**：用标记（marker）分档，在 `pyproject.toml` 里注册，防止拼错：

```toml
[tool.pytest.ini_options]
markers = ["smoke", "presubmit", "nightly", "release", "hw: needs real hardware"]
addopts = "--strict-markers"
```

```python
@pytest.mark.smoke
def test_server_starts_and_answers(): ...

@pytest.mark.nightly
@pytest.mark.hw
def test_full_config_matrix(): ...
```

流水线按档选择：`pytest -m smoke`、`pytest -m "presubmit and not hw"`、`pytest -m "nightly or release"`。再配合 pytest-timeout 的 `--timeout=60` 给每条测试设上限，超时直接失败，防止一条卡死的测试吃掉整档预算。
