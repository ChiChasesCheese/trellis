---
id: leetcode-c-openssl-rsa-modexp-application
node: topics.uncategorised
type: qa
anki: 1787361364897
tags: [algorithm::constant-time-arithmetic, algorithm::modular-exponentiation, algorithm::montgomery-reduction, application, case, case::openssl-rsa-modexp, category::runtimes-os, chapter::05, chapter::09, chapter::13, leetcode, system::openssl]
---
## Q
OpenSSL RSA 模幂为什么同时需要 binary/window exponentiation、Montgomery reduction 和 constant-time 实现？

## A
快速幂减少乘法次数；Montgomery reduction 降低反复 mod 大整数的成本；constant-time 路径避免 secret exponent 通过分支或查表时序泄露。三者分别解决算法量、算术常数和安全边界。

**Evidence**

OpenSSL 官方 BN API 与 bn_exp.c 区分 Montgomery 和 constant-time modular exponentiation paths。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FOpenSSL%20RSA%EF%BC%9A%E6%A8%A1%E5%B9%82%E3%80%81Montgomery%20Reduction%20%E4%B8%8E%E5%B8%B8%E6%95%B0%E6%97%B6%E9%97%B4)
