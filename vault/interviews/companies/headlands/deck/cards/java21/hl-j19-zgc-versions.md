---
id: hl-j19-zgc-versions
node: java21.j19-runtime-zgc-jit
type: qa
step: 10
---
## Q
分代 ZGC 在 JDK 21、23、24 各是什么状态？

## A
- **JDK 21**：分代 ZGC 正式，需 `-XX:+UseZGC -XX:+ZGenerational`；
- **JDK 23**：`-XX:+UseZGC` 默认就是分代，`-XX:-ZGenerational` 触发弃用警告；
- **JDK 24**：彻底移除非分代模式，`ZGenerational` 选项被废弃（设了只会警告）。

JFR 自 JDK 11 起开源可用。
