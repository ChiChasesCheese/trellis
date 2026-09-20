---
nodes: [problems.realtime.online-judge]
url: https://icpc.io/problem-package-format/spec/legacy-icpc.html
---
# ICPC / Kattis — Problem Package Format (legacy-icpc spec)

值得读：ICPC 官方题目包格式规范，规定测试数据按 `data/sample`（公开样例）与
`data/secret`（隐藏测试）分离，并要求输入校验器（input validator）对每份输入执行校验，
退出码 42/43 分别表示成功/失败。本题解的「核心实体与 API」和「深入探讨」第 4 节直接采用
了这个划分作为测试用例存储结构的设计依据，而不是自己凭空发明一套命名和校验约定。
