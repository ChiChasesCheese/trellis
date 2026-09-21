---
id: module-namespace-created-on-first-import-and-main
node: runtime.namespaces-execution
type: qa
source: python-docs
---
## Q
一个模块的命名空间是什么时候被创建的？作为脚本直接运行的模块，它的模块名是什么？

## A
模块命名空间在这个模块第一次被 import 时自动创建，对应它的顶层代码块开始执行。如果一个脚本是直接从命令行运行的（而不是被别的模块 import），它的模块名固定是 `__main__`，而不是文件名——这正是 `if __name__ == "__main__":` 能区分「被直接运行」还是「被当作模块导入」的原因。
