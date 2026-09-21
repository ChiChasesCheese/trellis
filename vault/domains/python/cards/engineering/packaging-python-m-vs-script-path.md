---
id: packaging-python-m-vs-script-path
node: engineering.packaging-env
type: qa
tags: [grown]
---
## Q
用 `python -m 模块名` 运行一个模块，和直接用 `python 路径/文件.py` 运行同一个文件，在依赖解析上有什么关键差异？

## A
`python -m` 会先把该模块所在的包按正常的导入机制（import machinery）定位并加载，模块内部用的相对导入（relative import）和包内路径解析能正确工作，且会把当前工作目录（而不是脚本所在目录）加入 `sys.path`；直接用文件路径运行时，Python 只是把该文件当作独立脚本执行，它所在目录会被当作顶层，包内的相对导入常常因此失败。因此运行属于某个包的模块（例如 `python -m mypkg.cli`），应优先用 `-m` 而不是直接给文件路径。
