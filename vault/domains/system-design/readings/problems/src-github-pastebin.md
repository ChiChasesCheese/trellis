---
nodes: [problems.foundations.pastebin]
url: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
tags: [reference]
---
# GitHub Docs — About large files on GitHub

值得读：讲的是仓库文件而非 Gist，但给出的分级限制思路（25MiB 浏览器上传 / 50MiB 警告 /
100MiB 硬性拒绝）为"按大小分级处理，而不是设单一阈值"提供了一个可参照的真实产品先例。本
题解借用了这种分级思路来设计内联/对象存储的路由，但具体数字（4KB 内联阈值、1MB/25MB 的
匿名/认证上限）是按自己的容量估算和延迟预算独立推导的，与 GitHub 这里的数字没有对应关系。
