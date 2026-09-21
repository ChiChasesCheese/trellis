---
id: venv-detect-sys-prefix-vs-env-var
node: engineering.packaging-env
type: qa
source: python-docs
---
## Q
在代码里判断「当前解释器是否运行在虚拟环境中」，为什么应该比较 `sys.prefix != sys.base_prefix`，而不是检查 `VIRTUAL_ENV` 环境变量是否存在？

## A
`VIRTUAL_ENV` 只在虚拟环境被显式「激活」（activate，即运行了激活脚本）后才会被设置，但激活并不是使用虚拟环境的必要步骤——直接用虚拟环境里 Python 解释器的完整路径运行代码同样有效且不会设置这个变量，所以它不可靠。运行中的解释器里，`sys.prefix` 和 `sys.exec_prefix` 始终指向当前使用的环境目录，`sys.base_prefix` 则指向创建该环境所用的基础 Python；只要两者不同，就说明当前解释器确实运行在虚拟环境里，这个判断与是否激活无关，因此更可靠。
