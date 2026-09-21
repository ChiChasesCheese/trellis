---
id: accumulate-default-sum-custom-running-max
node: iteration.itertools
type: qa
source: python-docs
---
## Q
`itertools.accumulate([3, 4, 6, 2, 1], max)` 依次产出什么？`accumulate` 不传 `function` 参数时默认做的是什么运算？

## A
依次产出 `3, 4, 6, 6, 6`——每一步都是「到目前为止看到过的最大值」，因为传入的 `function` 是 `max`。`accumulate` 默认（不传 `function`）用的是加法，产出运行总和（running sum），例如 `accumulate([1,2,3,4,5])` 产出 `1, 3, 6, 10, 15`；传入 `initial` 参数还能让输出比输入多一个元素（先产出 initial 本身，再往后累加）。
