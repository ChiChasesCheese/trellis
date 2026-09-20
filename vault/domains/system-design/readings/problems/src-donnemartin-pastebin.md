---
nodes: [problems.foundations.pastebin]
url: https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md
tags: [reference]
---
# Design Pastebin.com (or Bit.ly)

值得读：CC-BY 授权的开源模板，给出了"元数据表 + 对象存储分离、按 DAU 估算读写 QPS"这套
最基本的骨架，容量估算部分用了单一平均粘贴大小（约 1.27KB/条）做整体估算。本题解沿用了
它"内容和元数据分开存"的骨架，但认为按单一平均值估算会掩盖大文件对字节总量的主导作用，
因此改用条数分桶（片段/日志/大文件三档）重新推导存储量，并补充了它完全没有涉及的隐私
（去重旁路）、阅后即焚、私有 id 熵这三个维度。
