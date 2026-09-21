---
title: collections.abc — Abstract Base Classes for Containers
source: https://docs.python.org/3/library/collections.abc.html
corpus: python-docs
section: 49-collections-abc
clipped: '2026-09-21'
---

# collections.abc — Abstract Base Classes for Containers

# `collections.abc` — Abstract Base Classes for Containers[¶](#module-collections.abc)

Added in version 3.3: Formerly, this module was part of the [`collections`](collections.html#module-collections) module.

**Source code:** [Lib/_collections_abc.py](https://github.com/python/cpython/tree/3.14/Lib/_collections_abc.py)

This module provides [abstract base classes](../glossary.html#term-abstract-base-class) that
can be used to test whether a class provides a particular interface; for
example, whether it is [hashable](../glossary.html#term-hashable) or whether it is a [mapping](../glossary.html#term-mapping).

An [`issubclass()`](../builtins/functions.html#issubclass) or [`isinstance()`](../builtins/functions.html#isinstance) test for an interface works in one
of three ways.

1. A newly written class can inherit directly from one of the abstract base classes. The class must supply the required abstract methods. The remaining mixin methods come from inheritance and can be overridden if desired. Other methods may be added as needed: class C(Sequence): # Direct inheritance def __init__(self): ... # Extra method not required by the ABC def __getitem__(self, index): ... # Required abstract method def __len__(self): ... # Required abstract method def count(self, value): ... # Optionally override a mixin method >>> issubclass(C, Sequence) True >>> isinstance(C(), Sequence) True
2. Existing classes and built-in classes can be registered as “virtual subclasses” of the ABCs. Those classes should define the full API including all of the abstract methods and all of the mixin methods. This lets users rely on [`issubclass()`](../builtins/functions.html#issubclass) or[`isinstance()`](../builtins/functions.html#isinstance) tests
to determine whether the full interface is supported.  The exception to
this rule is for methods that are automatically inferred from the rest
of the API:class D: # No inheritance def __init__(self): ... # Extra method not required by the ABC def __getitem__(self, index): ... # Abstract method def __len__(self): ... # Abstract method def count(self, value): ... # Mixin method def index(self, value): ... # Mixin method Sequence.register(D) # Register instead of inherit >>> issubclass(D, Sequence) True >>> isinstance(D(), Sequence) True In this example, class `D` does not need to define`__contains__` ,`__iter__` , and`__reversed__` because the[in-operator](../reference/expressions.html#comparisons) , the[iteration](../glossary.html#term-iterable) logic, and the[`reversed()`](../builtins/functions.html#reversed) function automatically fall back to
using`__getitem__` and`__len__` .
3. Some simple interfaces are directly recognizable by the presence of the required methods (unless those methods have been set to [`None`](../builtins/constants.html#None) ):class E: def __iter__(self): ... def __next__(self): ... >>> issubclass(E, Iterable) True >>> isinstance(E(), Iterable) True Complex interfaces do not support this last technique because an interface is more than just the presence of method names. Interfaces specify semantics and relationships between methods that cannot be inferred solely from the presence of specific method names. For example, knowing that a class supplies `__getitem__` ,`__len__` , and`__iter__` is insufficient for distinguishing a[`Sequence`](#collections.abc.Sequence) from
a[`Mapping`](#collections.abc.Mapping) .

Added in version 3.9: These abstract classes now support `[]`. See [Generic Alias Type](../builtins/stdtypes.html#types-genericalias)
and [**PEP 585**](https://peps.python.org/pep-0585/).

## Collections Abstract Base Classes[¶](#collections-abstract-base-classes)

The collections module offers the following [ABCs](../glossary.html#term-abstract-base-class):

| ABC | Inherits from | Abstract Methods | Mixin Methods | 
|---|---|---|---|
| `Container`[\[1\]](#id18) |  | `__contains__` |  | 
| `Hashable`[\[1\]](#id18) |  | `__hash__` |  | 
| `Iterable`[\[1\]](#id18)[\[2\]](#id19) |  | `__iter__` |  | 
| `Iterator`[\[1\]](#id18) | `Iterable` | `__next__` | `__iter__` | 
| `Reversible`[\[1\]](#id18) | `Iterable` | `__reversed__` |  | 
| `Generator`[\[1\]](#id18) | `Iterator` | `send` ,`throw` | `close` ,`__iter__` ,`__next__` | 
| `Sized`[\[1\]](#id18) |  | `__len__` |  | 
| `Callable`[\[1\]](#id18) |  | `__call__` |  | 
| `Collection`[\[1\]](#id18) | [`Sized`](#collections.abc.Sized) ,[`Iterable`](#collections.abc.Iterable) ,`Container` | `__contains__` ,`__iter__` ,`__len__` |  | 
| `Sequence` | [`Reversible`](#collections.abc.Reversible) ,`Collection` | `__getitem__` ,`__len__` | `__contains__` ,`__iter__` ,`__reversed__` ,`index` , and`count` | 
| `MutableSequence` | `Sequence` | `__getitem__` ,`__setitem__` ,`__delitem__` ,`__len__` ,`insert` | Inherited [`Sequence`](#collections.abc.Sequence) methods and`append` ,`clear` ,`reverse` ,`extend` ,`pop` ,`remove` , and`__iadd__` | 
| `ByteString` | `Sequence` | `__getitem__` ,`__len__` | Inherited [`Sequence`](#collections.abc.Sequence) methods | 
| `Set` | `Collection` | `__contains__` ,`__iter__` ,`__len__` | `__le__` ,`__lt__` ,`__eq__` ,`__ne__` ,`__gt__` ,`__ge__` ,`__and__` ,`__or__` ,`__sub__` ,`__rsub__` ,`__xor__` ,`__rxor__` and`isdisjoint` | 
| `MutableSet` | `Set` | `__contains__` ,`__iter__` ,`__len__` ,`add` ,`discard` | Inherited [`Set`](#collections.abc.Set) methods and`clear` ,`pop` ,`remove` ,`__ior__` ,`__iand__` ,`__ixor__` , and`__isub__` | 
| `Mapping` | `Collection` | `__getitem__` ,`__iter__` ,`__len__` | `__contains__` ,`keys` ,`items` ,`values` ,`get` ,`__eq__` , and`__ne__` | 
| `MutableMapping` | `Mapping` | `__getitem__` ,`__setitem__` ,`__delitem__` ,`__iter__` ,`__len__` | Inherited [`Mapping`](#collections.abc.Mapping) methods and`pop` ,`popitem` ,`clear` ,`update` , and`setdefault` | 
| `MappingView` | `Sized` |  | `__init__` ,`__len__` and`__repr__` | 
| `ItemsView` | [`MappingView`](#collections.abc.MappingView) ,`Set` |  | `__contains__` ,`__iter__` | 
| `KeysView` | [`MappingView`](#collections.abc.MappingView) ,`Set` |  | `__contains__` ,`__iter__` | 
| `ValuesView` | [`MappingView`](#collections.abc.MappingView) ,`Collection` |  | `__contains__` ,`__iter__` | 
| `Awaitable`[\[1\]](#id18) |  | `__await__` |  | 
| `Coroutine`[\[1\]](#id18) | `Awaitable` | `send` ,`throw` | `close` | 
| `AsyncIterable`[\[1\]](#id18) |  | `__aiter__` |  | 
| `AsyncIterator`[\[1\]](#id18) | `AsyncIterable` | `__anext__` | `__aiter__` | 
| `AsyncGenerator`[\[1\]](#id18) | `AsyncIterator` | `asend` ,`athrow` | `aclose` ,`__aiter__` ,`__anext__` | 
| `Buffer`[\[1\]](#id18) |  | `__buffer__` |  | 

Footnotes

## Collections Abstract Base Classes – Detailed Descriptions[¶](#collections-abstract-base-classes-detailed-descriptions)

- 
*class* collections.abc.Container[¶](#collections.abc.Container)
- ABC for classes that provide the [`__contains__()`](../reference/datamodel.html#object.__contains__) method.

- 
*class* collections.abc.Hashable[¶](#collections.abc.Hashable)
- ABC for classes that provide the [`__hash__()`](../reference/datamodel.html#object.__hash__) method.

- 
*class* collections.abc.Callable[¶](#collections.abc.Callable)
- ABC for classes that provide the [`__call__()`](../reference/datamodel.html#object.__call__) method.See [Annotating callable objects](typing.html#annotating-callables) for details on how to use`Callable` in type annotations.

- 
*class* collections.abc.Iterable[¶](#collections.abc.Iterable)
- ABC for classes that provide the [`__iter__()`](../builtins/stdtypes.html#container.__iter__) method.Checking `isinstance(obj, Iterable)` detects classes that are registered
as`Iterable` or that have an[`__iter__()`](../builtins/stdtypes.html#container.__iter__) method,
but it does
not detect classes that iterate with the[`__getitem__()`](../reference/datamodel.html#object.__getitem__) method.
The only reliable way to determine whether an object is[iterable](../glossary.html#term-iterable) is to call`iter(obj)` .

- 
*class* collections.abc.Collection[¶](#collections.abc.Collection)
- ABC for sized iterable container classes. Added in version 3.6.

- 
*class* collections.abc.Iterator[¶](#collections.abc.Iterator)
- ABC for classes that provide the [`__iter__()`](../builtins/stdtypes.html#iterator.__iter__) and[`__next__()`](../builtins/stdtypes.html#iterator.__next__) methods.  See also the definition of[iterator](../glossary.html#term-iterator) .

- 
*class* collections.abc.Reversible[¶](#collections.abc.Reversible)
- ABC for iterable classes that also provide the [`__reversed__()`](../reference/datamodel.html#object.__reversed__) method.Added in version 3.6.

- 
*class* collections.abc.Generator[¶](#collections.abc.Generator)
- ABC for [generator](../glossary.html#term-generator) classes that implement the protocol defined in[**PEP 342**](https://peps.python.org/pep-0342/) that extends[iterators](../glossary.html#term-iterator) with the[`send()`](../reference/expressions.html#generator.send) ,[`throw()`](../reference/expressions.html#generator.throw) and[`close()`](../reference/expressions.html#generator.close) methods.See [Annotating generators and coroutines](typing.html#annotating-generators-and-coroutines) for details on using`Generator` in type annotations.Added in version 3.5.

- 
*class* collections.abc.Sequence[¶](#collections.abc.Sequence)
- 
*class* collections.abc.MutableSequence[¶](#collections.abc.MutableSequence)
- 
*class* collections.abc.ByteString[¶](#collections.abc.ByteString)
- ABCs for read-only and mutable [sequences](../glossary.html#term-sequence) .Implementation note: Some of the mixin methods, such as [`__iter__()`](../builtins/stdtypes.html#container.__iter__) ,[`__reversed__()`](../reference/datamodel.html#object.__reversed__) ,
and[`index()`](../builtins/stdtypes.html#sequence.index) make repeated calls to the underlying[`__getitem__()`](../reference/datamodel.html#object.__getitem__) method.
Consequently, if`__getitem__()` is implemented with constant
access speed, the mixin methods will have linear performance;
however, if the underlying method is linear (as it would be with a
linked list), the mixins will have quadratic performance and will
likely need to be overridden.
  - 
index(*value* ,*start=0* ,*stop=None* )[¶](#collections.abc.ByteString.index)
  - Return first index of *value* .Raises [`ValueError`](../builtins/exceptions.html#ValueError) if the value is not present.Supporting the *start* and*stop* arguments is optional, but recommended.Changed in version 3.5: The [`index()`](../builtins/stdtypes.html#sequence.index) method gained support for
the*stop* and*start* arguments.
 Deprecated since version 3.12, will be removed in version 3.17: The `ByteString` ABC has been deprecated.Use `isinstance(obj, collections.abc.Buffer)` to test if`obj` implements the[buffer protocol](../c-api/buffer.html#bufferobjects) at runtime. For use
in type annotations, either use[`Buffer`](#collections.abc.Buffer) or a union that
explicitly specifies the types your code supports (e.g.,`bytes | bytearray | memoryview` ).`ByteString` was originally intended to be an abstract class that
would serve as a supertype of both[`bytes`](../builtins/stdtypes.html#bytes) and[`bytearray`](../builtins/stdtypes.html#bytearray) .
However, since the ABC never had any methods, knowing that an object was
an instance of`ByteString` never actually told you anything
useful about the object. Other common buffer types such as[`memoryview`](../builtins/stdtypes.html#memoryview) were also never understood as subtypes of`ByteString` (either at runtime or by static type checkers).See [**PEP 688**](https://peps.python.org/pep-0688/#current-options) for more details.
- 
index(

- 
*class* collections.abc.Mapping[¶](#collections.abc.Mapping)
- 
*class* collections.abc.MutableMapping[¶](#collections.abc.MutableMapping)
- ABCs for read-only and mutable [mappings](../glossary.html#term-mapping) .

- 
*class* collections.abc.MappingView[¶](#collections.abc.MappingView)
- 
*class* collections.abc.ItemsView[¶](#collections.abc.ItemsView)
- 
*class* collections.abc.KeysView[¶](#collections.abc.KeysView)
- 
*class* collections.abc.ValuesView[¶](#collections.abc.ValuesView)
- ABCs for mapping, items, keys, and values [views](../glossary.html#term-dictionary-view) .

- 
*class* collections.abc.Awaitable[¶](#collections.abc.Awaitable)
- ABC for [awaitable](../glossary.html#term-awaitable) objects, which can be used in[`await`](../reference/expressions.html#await) expressions.  Custom implementations must provide the[`__await__()`](../reference/datamodel.html#object.__await__) method.[Coroutine](../glossary.html#term-coroutine) objects and instances of the[`Coroutine`](#collections.abc.Coroutine) ABC are all instances of this ABC.Note In CPython, generator-based coroutines ( [generators](../glossary.html#term-generator) decorated with[`@types.coroutine`](types.html#types.coroutine) ) are*awaitables* , even though they do not have an[`__await__()`](../reference/datamodel.html#object.__await__) method.
Using`isinstance(gencoro, Awaitable)` for them will return`False` .
Use[`inspect.isawaitable()`](inspect.html#inspect.isawaitable) to detect them.Added in version 3.5.

- 
*class* collections.abc.Coroutine[¶](#collections.abc.Coroutine)
- ABC for [coroutine](../glossary.html#term-coroutine) compatible classes.  These implement the
following methods, defined in[Coroutine Objects](../reference/datamodel.html#coroutine-objects) :[`send()`](../reference/datamodel.html#coroutine.send) ,[`throw()`](../reference/datamodel.html#coroutine.throw) , and[`close()`](../reference/datamodel.html#coroutine.close) .  Custom implementations must also implement[`__await__()`](../reference/datamodel.html#object.__await__) .  All`Coroutine` instances are also
instances of[`Awaitable`](#collections.abc.Awaitable) .Note In CPython, generator-based coroutines ( [generators](../glossary.html#term-generator) decorated with[`@types.coroutine`](types.html#types.coroutine) ) are*awaitables* , even though they do not have an[`__await__()`](../reference/datamodel.html#object.__await__) method.
Using`isinstance(gencoro, Coroutine)` for them will return`False` .
Use[`inspect.isawaitable()`](inspect.html#inspect.isawaitable) to detect them.See [Annotating generators and coroutines](typing.html#annotating-generators-and-coroutines) for details on using`Coroutine` in type annotations.
The variance and order of type parameters correspond to those of[`Generator`](#collections.abc.Generator) .Added in version 3.5.

- 
*class* collections.abc.AsyncIterable[¶](#collections.abc.AsyncIterable)
- ABC for classes that provide an `__aiter__` method.  See also the
definition of[asynchronous iterable](../glossary.html#term-asynchronous-iterable) .Added in version 3.5.

- 
*class* collections.abc.AsyncIterator[¶](#collections.abc.AsyncIterator)
- ABC for classes that provide `__aiter__` and`__anext__` methods.  See also the definition of[asynchronous iterator](../glossary.html#term-asynchronous-iterator) .Added in version 3.5.

- 
*class* collections.abc.AsyncGenerator[¶](#collections.abc.AsyncGenerator)
- ABC for [asynchronous generator](../glossary.html#term-asynchronous-generator) classes that implement the protocol
defined in[**PEP 525**](https://peps.python.org/pep-0525/) and[**PEP 492**](https://peps.python.org/pep-0492/) .See [Annotating generators and coroutines](typing.html#annotating-generators-and-coroutines) for details on using`AsyncGenerator` in type annotations.Added in version 3.6.

- 
*class* collections.abc.Buffer[¶](#collections.abc.Buffer)
- ABC for classes that provide the [`__buffer__()`](../reference/datamodel.html#object.__buffer__) method,
implementing the[buffer protocol](../c-api/buffer.html#bufferobjects) . See[**PEP 688**](https://peps.python.org/pep-0688/) .Added in version 3.12.

## Examples and Recipes[¶](#examples-and-recipes)

ABCs allow us to ask classes or instances if they provide particular functionality, for example:

```
size = None
if isinstance(myvar, collections.abc.Sized):
    size = len(myvar)
```
Several of the ABCs are also useful as mixins that make it easier to develop
classes supporting container APIs.  For example, to write a class supporting
the full [`Set`](#collections.abc.Set) API, it is only necessary to supply the three underlying
abstract methods: [`__contains__()`](../reference/datamodel.html#object.__contains__), [`__iter__()`](../builtins/stdtypes.html#container.__iter__), and
[`__len__()`](../reference/datamodel.html#object.__len__). The ABC supplies the remaining methods such as
`__and__()` and [`isdisjoint()`](../builtins/stdtypes.html#frozenset.isdisjoint):

```
class ListBasedSet(collections.abc.Set):
    ''' Alternate set implementation favoring space over speed
        and not requiring the set elements to be hashable. '''
    def __init__(self, iterable):
        self.elements = lst = []
        for value in iterable:
            if value not in lst:
                lst.append(value)
    def __iter__(self):
        return iter(self.elements)
    def __contains__(self, value):
        return value in self.elements
    def __len__(self):
        return len(self.elements)
s1 = ListBasedSet('abcdef')
s2 = ListBasedSet('defghi')
overlap = s1 & s2            # The __and__() method is supported automatically
```
Notes on using [`Set`](#collections.abc.Set) and [`MutableSet`](#collections.abc.MutableSet) as a mixin:

1. Since some set operations create new sets, the default mixin methods need a way to create new instances from an [iterable](../glossary.html#term-iterable) . The class constructor is
assumed to have a signature in the form`ClassName(iterable)` .
That assumption is factored-out to an internal[`classmethod`](../builtins/functions.html#classmethod) called`_from_iterable()` which calls`cls(iterable)` to produce a new set.
If the[`Set`](#collections.abc.Set) mixin is being used in a class with a different
constructor signature, you will need to override`_from_iterable()` with a classmethod or regular method that can construct new instances from
an iterable argument.
2. To override the comparisons (presumably for speed, as the semantics are fixed), redefine [`__le__()`](../reference/datamodel.html#object.__le__) and[`__ge__()`](../reference/datamodel.html#object.__ge__) ,
then the other operations will automatically follow suit.
3. The [`Set`](#collections.abc.Set) mixin provides a`_hash()` method to compute a hash value
for the set; however,[`__hash__()`](../reference/datamodel.html#object.__hash__) is not defined because not all sets
are[hashable](../glossary.html#term-hashable) or immutable.  To add set hashability using mixins,
inherit from both`Set` and[`Hashable`](#collections.abc.Hashable) , then define`__hash__ = Set._hash` .

See also

- [OrderedSet recipe](https://code.activestate.com/recipes/576694/) for an
example built on[`MutableSet`](#collections.abc.MutableSet) .
- For more about ABCs, see the [`abc`](abc.html#module-abc) module and[**PEP 3119**](https://peps.python.org/pep-3119/) .
