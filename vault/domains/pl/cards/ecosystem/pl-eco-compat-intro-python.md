---
id: pl-eco-compat-intro-python
node: ecosystem.compatibility
type: qa
step: 5
---
## Q
Python 2 到 3 的迁移是怎么回事？今天的弃用政策与“删除死电池”（dead batteries）又是什么？

## A
**Python 2 → 3（2008 至 2020）**：Python 3 一次性修复了早期设计里的根本问题，最大的是文本模型：`str` 与 `bytes` 严格分离、字符串默认 Unicode；还有整数除法、`print` 变成函数、迭代器代替列表等。这些改变**不能向后兼容**，3.x 不能运行 2.x 代码。

**后果**：迁移用了十几年。很多库要同时支持 2 和 3（用 `six` 之类的兼容层），应用等库，库等应用，生态被卡住。2.7 在 2020 年 1 月 1 日结束维护。教训被广泛引用：**大爆炸式的破坏很贵**；现在 Python 团队明确表示不会再做 Python 4 式的断裂。

**现在的做法：持续、小步、有预告**。弃用流程大致是：某个功能先发出 `DeprecationWarning`，至少经过两个版本之后才删除（PEP 387）。并且每年一个版本，节奏固定。

**“死电池”清理**：Python 号称“电池齐全”，标准库里有很多过时的模块。3.12 删除了 `distutils` 和 `imp`（PEP 632 等），3.13 按 PEP 594 删除了一批更老的模块。真实结果：

```
python3 -c "import distutils"   # ModuleNotFoundError: No module named 'distutils'
python3 -c "import imp"         # ModuleNotFoundError: No module named 'imp'
```

依赖它们的老脚本升级 Python 后直接失败。

**要点**：
1. Python 的兼容性比 Java、Go 弱得多：次版本升级就可能破坏代码，所以必须关注弃用警告。
2. 因此项目要在 CI 里用 `-W error::DeprecationWarning` 把弃用警告当错误，提前发现。

**要记住的一点**：Python 从“一次大断裂”改成“年年小断裂”，让每次升级成本可控。
