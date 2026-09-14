---
id: auto-resume-trigger-and-cost-control
node: warehouse.auto-suspend-resume
type: qa
source: snowflake-docs
---
## Q
虚拟仓库（virtual warehouse）的 auto-resume（自动恢复）在什么条件下触发？什么时候应该故意关掉它？

## A
默认开启：当会话提交了需要仓库的语句，且该仓库是该会话的当前仓库时，Snowflake 会自动恢复这个已挂起的仓库（可能因资源准备有短暂延迟）。若成本和访问都不是问题，开启它可保证需要时仓库自动启动；若想控制成本或限制谁能使用某个仓库，应关闭 auto-resume，只在需要时手动恢复，这样任何人的一条查询都无法悄悄把它拉起来计费。
