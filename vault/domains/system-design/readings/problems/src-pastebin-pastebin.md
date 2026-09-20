---
nodes: [problems.foundations.pastebin]
url: https://pastebin.com/doc_api
tags: [reference]
---
# Pastebin.com API 文档

值得读：真实产品的一手文档，给出了可见性分级（公开 / 不可列出，上限 25 条 / 私有，上限 10
条）和九档到期时间预设（10 分钟到 1 年，或永不过期）——本题解的 `visibility` 枚举和
`expires_in` 预设直接参照了这个真实产品的划分。不同于本题解的地方：Pastebin.com 的具体
大小限制（免费 512KB / 付费 10MB）是账户等级驱动的产品定价策略，本题解没有照搬这两个数字，
而是按自己的容量估算重新推导了 4KB 内联阈值和 1MB/25MB 的匿名/认证上限。
