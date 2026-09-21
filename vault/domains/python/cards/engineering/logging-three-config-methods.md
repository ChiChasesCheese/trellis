---
id: logging-three-config-methods
node: engineering.logging-config
type: qa
source: python-docs
---
## Q
logging 支持哪三种配置方式？为什么生产环境常用「把配置写成一份字典（或从配置文件/环境变量拼出这份字典）再传给 `logging.config.dictConfig()`」这种方式，而不是把创建 logger/handler/formatter 的 Python 代码散落在各处？

## A
三种方式：① 直接用 Python 代码显式调用 `getLogger()`/`addHandler()`/`setFormatter()` 等方法搭建；② 写一份配置文件用 `logging.config.fileConfig()` 加载；③ 构造一份配置字典传给 `logging.config.dictConfig()`。用 `dictConfig` 的好处是配置和代码分离：这份字典可以整个从外部文件或环境变量（比如按部署环境切换日志级别、日志文件路径）拼装出来，改配置不需要改代码、不需要重新发布，而且所有 logger/handler/formatter 的搭建逻辑集中在一处，不会随着代码库长大而散落在各个模块的顶部。
