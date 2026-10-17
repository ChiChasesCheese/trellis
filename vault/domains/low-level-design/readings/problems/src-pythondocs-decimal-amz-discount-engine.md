---
nodes: [amazon.amz-discount-engine]
url: https://docs.python.org/3/library/decimal.html
---
# decimal — Decimal fixed point and floating point arithmetic
值得读：Python 官方文档，讲十进制精确算术与舍入模式（`ROUND_HALF_UP` 等），开头就用 `0.1 + 0.2` 对比 float 与 Decimal。只用它做「价格字符串 → 分」的一次精确转换，其余全部用整数运算，就不必每一步都想舍入模式；面试官要求多币种或任意精度时，才把金额类型换成 Decimal。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/decimal.html)
%% trellis:end %%
