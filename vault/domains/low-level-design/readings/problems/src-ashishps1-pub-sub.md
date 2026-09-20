---
nodes: [problems.components.pub-sub]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/pub-sub-system.md
---
# awesome-low-level-design — Designing a Pub-Sub System

值得读：这道题在面试里被念出来的**标准版题面**（六条需求：多发布者多订阅者、按主题投递、
实时送达、线程安全、可扩展），配一张 UML 和六种语言的实现，用来对齐"面试官脑子里的题面"最省事。
它的 Python 版把 `PubSubService` 写成 `__new__` 单例，`Topic` 只有 `add_subscriber` / `broadcast`
两个方法、转身把回调丢进 `ThreadPoolExecutor`——于是同一主题的顺序无从保证、积压量不可观测、
消息投完即丢，第 2 关以后的问题（重放、迟到订阅、慢订阅者隔离）它一个也答不了。本题解用
"共享保留日志 + 每订阅者游标"取代即时广播，用模块级实例取代 `__new__` 单例，理由都在
"关键设计决策"里。
