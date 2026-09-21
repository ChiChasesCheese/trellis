%% trellis:begin %%
# 类、协议与元编程

从写出一个"Pythonic 对象"到理解属性查找、描述符、抽象基类与协议、继承与 MRO，直到类装饰器与元类如何在类创建时介入。

## Topics
- [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]]
- [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]
- [[domains/python/map/classes.attribute-lookup|属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`]]
- [[domains/python/map/classes.properties-descriptors|`property` 与描述符协议（`__get__`/`__set__`/`__set_name__`）]]
- [[domains/python/map/classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]]
- [[domains/python/map/classes.inheritance-mro|继承、多重继承、MRO（C3 线性化）与 `super()`]]
- [[domains/python/map/classes.operator-overloading|运算符重载：`__add__`/`__radd__`、就地运算符与比较运算]]
- [[domains/python/map/classes.metaprogramming|类装饰器、`__init_subclass__` 与元类（metaclass）]]
- [[domains/python/map/classes.enums|枚举（Enum）：`Enum`/`IntEnum`/`StrEnum`/`Flag`、`auto()` 与唯一性]]
%% trellis:end %%

## Notes
