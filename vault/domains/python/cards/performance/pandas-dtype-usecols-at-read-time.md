---
id: pandas-dtype-usecols-at-read-time
node: performance.pandas-at-scale
type: qa
tags: [grown]
---
## Q
为什么要在 `pd.read_csv(dtype=..., usecols=...)` 阶段就指定列和类型，而不是等整张表读进来之后再用 `astype()` 转换、再删掉不用的列？

## A
`read_csv` 默认按启发式猜类型，数值列常被猜成 8 字节的 `int64`/`float64`，字符串列整列存成 Python 对象指针，比必要的开销大；读完整表再转换，峰值内存早已按最宽类型、全部列吃满一次，之后缩小也救不回那个峰值。`usecols=` 让不需要的列压根不被解析物化，`dtype=` 让每列一开始就按最省内存的类型分配，两者都在峰值出现前把峰值压低。
