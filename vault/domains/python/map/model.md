%% trellis:begin %%
# 对象模型：名字、对象与数据模型（data model）

建立 Python 的核心心智模型：一切皆对象、名字是绑定而非盒子、特殊方法（dunder）把对象接入语言协议，以及 dict/set 这类内建容器在底层如何工作。

## Topics
- [[domains/python/map/model.names-objects|名字绑定、对象身份与 `is` vs `==`]]
- [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]]
- [[domains/python/map/model.copy|浅拷贝、深拷贝与切片复制]]
- [[domains/python/map/model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]]
- [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]]
- [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]]
- [[domains/python/map/model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]]
- [[domains/python/map/model.text-bytes|str 与 bytes：Unicode、编码与解码]]
- [[domains/python/map/model.numbers|数值：int 大整数、float 精度与 Decimal]]
%% trellis:end %%

## Notes
