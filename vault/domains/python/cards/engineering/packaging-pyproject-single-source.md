---
id: packaging-pyproject-single-source
node: engineering.packaging-env
type: qa
tags: [grown]
---
## Q
`pyproject.toml` 作为项目的「单一配置源」（single source of truth）具体统一了哪些原本分散的配置？

## A
在 `pyproject.toml` 出现之前，一个 Python 项目的构建依赖、包元数据（名称、版本、依赖列表）、以及各类工具（如格式化器、类型检查器、测试框架）的配置往往分散在 `setup.py`、`setup.cfg`、`requirements.txt` 及各工具各自的配置文件里。`pyproject.toml` 用统一的 TOML 格式把「用什么工具构建」（`[build-system]`）、「项目元数据与运行时依赖」（`[project]`）和「各工具自己的配置」（`[tool.xxx]`）都放进同一个文件，减少了配置文件数量和相互不一致的风险。
