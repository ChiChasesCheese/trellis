---
nodes: [python.data-model]
url: https://docs.python.org/3/reference/datamodel.html
---
# 3. Data model

值得读：官方语言参考里 `__eq__`/`__hash__`/`__repr__` 与排序、容器协议那几节，是
`python-data-model-hash-eq-contract`、`python-data-model-eq-disables-hash` 两张卡的第一手依据——"重写 `__eq__`
会让默认 `__hash__` 失效"这条契约不是约定俗成，而是数据模型里写死的规则，读它能补上为什么，以及容器协议还牵连了哪些方法。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/reference/datamodel.html)
%% trellis:end %%
