---
id: fluency-style-formatter-linter
node: fluency.style
type: qa
step: 2
---
## Q
代码评审里一半的评论是空格、引号、换行位置。团队应该怎么让这些争论消失？格式化器（formatter）、linter 和类型检查器各管什么？

## A
**格式交给工具，评审只谈设计**

- **格式化器**：自动把代码改写成统一样子（`ruff format`、`black`）；引号、空格、换行、尾逗号不再是评审话题；风格选择不可商量，换来的是零争论；
- **linter**：静态检查可能出错的写法（`ruff check`、`flake8`、`pylint`）；未用的导入、遮蔽内置名、可变默认参数、裸 `except:`、`== None` 都会被指出；
- **类型检查器**：检查类型对不对（`mypy`、`pyright`），这是第三种工具，不要和 linter 混为一谈；
- **配置进仓库**：规则写在 `pyproject.toml`，本地和 CI 跑同一份；CI 里用 `ruff format --check` 和 `ruff check`，不通过就不合并；
- **选规则看收益**：先开会抓真 bug 的（`F` 未定义或未用名、`B` 常见陷阱、`A` 遮蔽内置、`E7` 比较写法）；纯排版的规则交给格式化器；
- **团队没有约定时的默认**：PEP 8 加 `ruff`；面试里也一样，字写成标准样子，评审者的注意力才会放在逻辑上。

```python
# 格式化前
x = {  'a':1,
  'b' :2 }
def f( a,b ):
    return a+b

# ruff format 之后
x = {"a": 1, "b": 2}


def f(a, b):
    return a + b
```

<details class="pt"><summary>延伸</summary>

格式化器一旦引入，第一次提交会改动整个仓库；把它单独做成一个提交，并把该提交的哈希写进 `.git-blame-ignore-revs`，`git blame` 就不会把每一行都算到格式化提交头上。

</details>

**知识点：**命名与风格规范（Naming, Style & Linters）
