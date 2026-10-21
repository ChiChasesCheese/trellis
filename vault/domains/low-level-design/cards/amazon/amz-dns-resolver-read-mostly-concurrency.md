---
id: amz-dns-resolver-read-mostly-concurrency
node: amazon.amz-dns-resolver
type: qa
step: 5
tags: [grown]
---
## Q
在 DNS 解析器设计里，读远多于写时，缓存的并发怎么处理？同一个域名同时未命中怎么办？

## A
三个选项：整个缓存一把互斥锁（简单，但读也互相排队）；读写锁（读并行，Python 标准库没有）；写时复制（copy-on-write）——写者复制整个字典、改完后原子替换引用，读者拿到引用就无锁读，适合写少的场景，代价是每次写 O(n)。同名并发未命中时，让第一个请求去问上游，其余等同一个结果（single-flight），否则上游被打 N 次。
