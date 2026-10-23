---
id: hl-cache-qa-cache-line-use
node: foundations.cpu-cache-locality
type: qa
step: 35
---
## Q
追问：什么是缓存行？你怎么利用它？

## A
推荐答法：「CPU 和内存之间搬运数据的最小单位，x86 通常 64 字节，Apple 芯片 128。读一个字节会读进整行，所以相邻数据免费。」

利用：
- 顺序访问；
- 热字段挨在一起；
- 内层循环走连续的那一维。

反过来要避免两个线程写同一行里的不同变量。
