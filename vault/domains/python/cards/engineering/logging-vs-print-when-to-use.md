---
id: logging-vs-print-when-to-use
node: engineering.logging-config
type: qa
source: python-docs
---
## Q
命令行脚本给用户看的正常输出该用 `print()`，那什么情况下该改用 `logging` 而不是 `print()`？

## A
`print()` 适合命令行程序面向用户的常规输出；而报告程序正常运行期间发生的事件（用于状态监控或故障排查）应该用 logger 的 `info()`（或需要详细诊断信息时用 `debug()`）。二者的关键差别是：logging 的输出有级别（level）、可以按级别过滤、可以独立配置输出目的地（控制台、文件、远程服务）而不改动业务代码；`print()` 做不到这些，只会无条件写到标准输出，没法在生产环境里按需要开关或改道。
