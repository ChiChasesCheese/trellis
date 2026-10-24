---
id: pl-eco-packages-intro-python
node: ecosystem.package-managers
type: qa
step: 6
---
## Q
Python 的 pip、uv 和虚拟环境（virtual environment）是什么？为什么一个环境里每个包只能有一个版本，解析器怎样回溯？

## A
**虚拟环境**：一个独立的目录，里面有自己的 Python 解释器链接和自己的 `site-packages`（安装第三方包的位置）。每个项目一个环境，避免项目之间相互污染，也避免污染系统 Python。

**pip 与 uv**：`pip` 是官方安装器。`uv` 是新一代工具，用 Rust 写，速度快得多，一并管理虚拟环境、Python 版本、依赖解析和锁文件（`uv.lock`）。项目依赖写在 `pyproject.toml` 里。

**一个环境一个版本**：`import requests` 只会找到 `site-packages` 里那一份，所以同一个环境里每个包最多一个版本。解析器必须找到**对所有约束都成立的一个版本**，找不到就失败。

**解析器与回溯**：它按约束求解。如果最新版本冲突，就回溯尝试更旧的版本，直到满足或穷尽。真实例子：`uv add "urllib3==1.20" "requests>=2.0"`，最新的 `requests` 要求 `urllib3>=1.21.1`，不满足，解析器回溯，**悄悄**选了 `requests==2.15.1`（一个很旧的版本）。

约束不可能满足时它会报错并解释原因：

```
your project depends on requests>=2.32 and urllib3==1.20,
we can conclude that your project's requirements are unsatisfiable.
```

**其他要点**：
- 二进制包叫 wheel，按平台预编译；没有 wheel 时要现场编译，需要编译器。
- 构建后端与 `pyproject.toml` 把「怎么构建包」从 `setup.py` 脚本里解耦。
- 应用提交 `uv.lock`；库在 `pyproject.toml` 里写宽松范围。

**要记住的一点**：Python 的单版本规则让类型和行为一致，代价是依赖冲突没有缓冲，只能靠解析器找交集。
