---
id: test-pytest-conftest-autouse-override
node: engineering.testing
type: qa
---
## Q
`conftest.py` 是什么？它和普通的 helper 模块有什么不同？`autouse=True` 的 fixture 适合做什么、有什么风险？同名 fixture 在不同目录里怎么覆盖？

## A
**`conftest.py` 是 pytest 自动发现的本地插件文件：放在哪个目录，里面的 fixture 和钩子（hook）就对这个目录及其所有子目录里的测试生效，测试文件不需要 `import` 它。**

- **和 helper 模块的区别：** helper 要显式 `import`；`conftest.py` 由 pytest 在收集时加载，fixture 按名字注入。它还能定义钩子函数（如 `pytest_addoption`），普通模块不行。
- **分层放置：** 根目录的 `conftest.py` 放全局的东西（命令行选项、session 级资源）；`tests/integration/conftest.py` 只放集成测试要的 fixture。
- **覆盖规则：** 子目录（或测试模块里）定义一个同名 fixture，就会遮住上层的那个，离测试越近越优先。下层版本还能把上层同名 fixture 当参数接收，在它的基础上加工。
- **autouse：** 本作用域内每个测试都自动使用，不用写进参数。适合「每个测试都必须做」的事：固定随机种子、清空全局缓存、把环境变量恢复原样。

```python
@pytest.fixture(autouse=True)
def _fixed_seed():
    random.seed(0)
```

- **autouse 的风险：** 读测试代码时看不见它，测试慢了或行为怪了很难想到是它；放在根 `conftest.py` 里会影响所有测试。只用于便宜、无害、每个测试都需要的准备。
- **排查工具：** `pytest --fixtures` 列出当前可用的所有 fixture 及其定义位置；`pytest --setup-show` 显示每个测试实际用了哪些 fixture。
