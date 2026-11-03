%% trellis:begin %%
# 值得写的特殊方法：__bool__ / __len__ / __contains__ / __and__ / __call__ / __enter__
*编码功力（Coding Craft） / 高级写法（Idioms）*

只在它让调用点更自然或让升级无感时才写：Decision 的 __bool__、Filter 的 & | ~、观察者的 __call__。

**Requires:** [[domains/python/map/model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]], [[domains/python/map/classes.operator-overloading|运算符重载：`__add__`/`__radd__`、就地运算符与比较运算]], [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]]

## Cards (6)
1. [[craft-dunder-protocols-that-pay-1-bool-keeps-old-callers-working]]
2. [[craft-dunder-protocols-that-pay-2-operators-for-composition]]
3. [[craft-dunder-protocols-that-pay-3-call-makes-objects-observers]]
4. [[craft-dunder-protocols-that-pay-4-container-protocols]]
5. [[craft-dunder-protocols-that-pay-5-container-semantics-cost]]
6. [[craft-dunder-protocols-that-pay-6-which-dunders-pay]]
%% trellis:end %%

## Notes
