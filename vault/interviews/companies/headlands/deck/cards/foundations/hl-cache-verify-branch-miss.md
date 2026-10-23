---
id: hl-cache-verify-branch-miss
node: foundations.cpu-cache-locality
type: qa
step: 43
---
## Q
怀疑一段 Java 代码慢是因为分支预测失败，怎么验证？

## A
四步：
1. `perf stat -e branches,branch-misses` 看分支预测失败率；
2. 输入排序（或构造完全可预测的数据）重跑，看时间是否明显下降；
3. 改成无分支写法再比较；
4. 用 JMH 避免被预热、死代码消除误导。

排序后显著变快，基本可确认。
