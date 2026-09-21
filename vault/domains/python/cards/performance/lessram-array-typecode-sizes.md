---
id: lessram-array-typecode-sizes
node: performance.less-ram
type: cloze
source: python-docs
---
`array` 模块里，类型码 {{c1::'b'}} 对应 1 字节的 signed char，{{c2::'q'}} 对应 8 字节的 signed long long，{{c3::'d'}} 对应 8 字节的 double；每种类型码的实际字节数是平台相关的最小值，准确大小要看数组对象的 `itemsize` 属性，不能只凭类型码猜。
