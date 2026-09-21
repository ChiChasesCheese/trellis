---
id: robust-warnings-deprecation-migration
node: engineering.robustness
type: qa
source: python-docs
---
## Q
`DeprecationWarning` 默认情况下会不会打印出来？库作者想提醒使用者迁移到新 API，为什么单靠默认行为不够，测试代码该怎么配置？

## A
`DeprecationWarning` 默认被 Python 的警告过滤器忽略，只有当触发它的代码直接写在 `__main__` 模块里时才会显示（3.7 起如此）；也就是说库内部调用已弃用 API 触发的警告，最终用户默认根本看不到。所以测试运行环境应显式开启，例如设置环境变量 `PYTHONWARNINGS=default` 或用 `-W default` 启动解释器，让所有默认被忽略的警告（包括 `DeprecationWarning`）都能在测试时暴露出来，及时发现依赖了废弃接口。
