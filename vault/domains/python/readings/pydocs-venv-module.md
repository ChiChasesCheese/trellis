---
nodes:
- engineering.packaging-env
title: venv 模块：虚拟环境
corpus: python-docs
section: 67-venv
url: https://docs.python.org/3/library/venv.html
tags:
- canonical
---

# venv 模块：虚拟环境

venv 是 Python 官方自带的虚拟环境工具，命令行一步创建一个独立的 Python 环境，有自己的 site-packages 目录，和系统全局的包互不干扰，这是为什么每个项目都该有独立虚拟环境的官方实现基础，避免了不同项目对同一个包要求不同版本时互相冲突。文档讲了虚拟环境的工作原理：并不是真的复制一份完整的 Python 解释器，而是通过一套符号链接（或 Windows 上的拷贝）加上 pyvenv.cfg 配置文件，让解释器在启动时优先从虚拟环境目录查找包。文末给出了通过继承 EnvBuilder 类自定义虚拟环境创建流程的例子，比如创建后自动安装一批固定的包。这是理解 pip install 到底把包装到哪里去了、以及为什么忘记激活虚拟环境导致装错地方这类问题根因的基础文档。
