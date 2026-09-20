---
nodes: [problems.components.logger]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/logging-framework
---
# lld-python — logging-framework

值得读：自由来源里唯一原生 Python、带 pytest 套件和 mermaid 图的实现。它有两个判断和本题解一致，
值得先看一遍：一是**责任链在日志里必须去掉"接住就停"这条规则**（它把这一点单独写了一节），
二是**格式化器要和目的地分开**，否则会长出 `JsonFileHandler` 这类乘积式的类。它的多目的地是靠
handler 的 `next` 指针串成一条链、没有 logger 层级，配置集中在一个双重检查锁的单例注册表里；
本题解换成"logger 持有 handler 元组 + 按点分名字成树、记录沿祖先链向上"，并把它列为后续的
异步写入（队列、排空、丢弃计数）和按大小滚动补成了第 3、4 关的硬要求。
