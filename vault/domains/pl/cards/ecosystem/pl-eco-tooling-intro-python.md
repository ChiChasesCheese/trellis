---
id: pl-eco-tooling-intro-python
node: ecosystem.tooling
type: qa
step: 5
---
## Q
Python 的工具链里 black、ruff、mypy/pyright 和 pytest 各是什么？为什么 ruff 的出现让这个生态向统一靠拢？

## A
**历史**：Python 标准库只有 `unittest` 和 `venv`，格式化与检查全靠第三方，长期并存：格式化用 `black` 或 `autopep8`，检查用 `flake8`、`pylint`，排序导入用 `isort`，每个工具各有配置。

**今天常见的组合**：
- **`black`**：“不可协商”风格的格式化器，几乎不可配置，类似 `gofmt` 的理念。
- **`ruff`**：用 Rust 写的 linter 兼格式化器，一个工具取代 `flake8`、`isort`、`black`、`pyupgrade` 等几十个，速度快一到两个数量级。配置写在 `pyproject.toml` 里。真实输出：对一段有问题的代码，它报 `F401 os imported but unused`、`E722 Do not use bare except`、`B006 Do not use mutable data structures for argument defaults`，并用 `ruff format --diff` 显示该怎样排版。
- **类型检查器**：`mypy`、`pyright`。Python 的类型注解默认不检查，必须运行它们才有效。
- **`pytest`**：事实标准测试框架。测试就是以 `test_` 开头的普通函数，用裸 `assert` 断言，失败时自动展示表达式各部分的值；`fixture` 做依赖注入。

**统一趋势**：ruff 和 uv 都来自同一家公司（Astral），都用 Rust 重写，目的是把“多个工具、多份配置”收拢成“一个快速工具”。这条路径和 Go 把工具链收进官方是殊途同归：区别在于 Python 是由社区的一个项目事实上完成的，而不是语言团队。

**要记住的一点**：Python 的工具链长期是“拼装”的，所以第一件事是在 `pyproject.toml` 里把检查、格式、类型、测试的命令和版本固定下来。
