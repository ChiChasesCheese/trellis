---
id: amz-linux-find-how-it-is-asked
node: amazon.amz-linux-find
type: qa
step: 1
tags: [grown]
---
## Q
Linux find 命令 API（File Search API）要你设计什么？开场先问哪三个澄清问题？

## A
题目：设计一个类似 Linux `find` 的 API，按大小、格式、名字等条件跨目录搜索文件，如「大于 5MB 的文件」「所有 XML 文件」，接口要干净、可扩展。

三个问题：
1. 树是内存对象还是真实磁盘？（决定遍历怎么写，过滤器不变）
2. 条件只有 AND，还是要 OR / NOT？（决定参数列表够不够，还是要可组合的对象树）
3. 返回列表还是边找边处理、符号链接要不要跟随？（决定生成器与环检测）
