---
id: pandas-category-dtype-groupby
node: performance.pandas-at-scale
type: qa
tags: [grown]
---
## Q
把取值范围很小的字符串列（比如「国家代码」）转成 `category` dtype，为什么既省内存又能让 `groupby` 更快？

## A
`category` dtype 底层是字典编码（dictionary encoding）：只存一份唯一值列表（categories），每行只存一个指向该列表的小整数编码，而不是像 `object` dtype 那样每行各自存一份 Python 字符串对象，哪怕值重复也各占内存。`groupby` 按这一列分组时比较的是小整数而非逐字符比较字符串，既省内存也让哈希与比较更快。
