---
nodes: [problems.foundations.auth-service]
url: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
tags: [reference]
---
# Password Storage Cheat Sheet

值得读：OWASP 官方密码存储指南，给出 Argon2id 的具体基线参数（最低 19 MiB 内存、
迭代次数 2、并行度 1），以及 bcrypt（cost ≥ 10，72 字节输入截断）、scrypt、PBKDF2
（FIPS-140 场景，HMAC-SHA256 + 至少 60 万次迭代）作为不同约束下的备选，并建议把
工作因子调到一个具体的耗时区间内。本题解「深入探讨」第 1 节直接采用 Argon2id 基线，
并补充了这篇文章没有给出的部分——把耗时参数和峰值登录 QPS 联立，算出需要多少 CPU
核心，而不是停留在"应该多慢"这个定性建议。
