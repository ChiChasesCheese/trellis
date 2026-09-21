---
title: array — Efficient arrays of numeric values
corpus: python-docs
section: 59-array
level: 1
locator: https://docs.python.org/3/library/array.html
license: free-online
fetched: '2026-09-21'
---

# `array` — Efficient arrays of numeric values[¶](#module-array)

This module defines an object type which can compactly represent an array of
basic values: characters, integers, floating-point numbers.  Arrays are mutable [sequence](../glossary.html#term-sequence)
types and behave very much like lists, except that the type of objects stored in
them is constrained.  The type is specified at object creation time by using a
*type code*, which is a single character.  The following type codes are
defined:

| Type code | C Type | Python Type | Minimum size in bytes | Notes | 
|---|---|---|---|---|
| `'b'` | signed char | int | 1 |  | 
| `'B'` | unsigned char | int | 1 |  | 
| `'u'` | wchar_t | Unicode character | 2 | (1) | 
| `'w'` | Py_UCS4 | Unicode character | 4 | (2) | 
| `'h'` | signed short | int | 2 |  | 
| `'H'` | unsigned short | int | 2 |  | 
| `'i'` | signed int | int | 2 |  | 
| `'I'` | unsigned int | int | 2 |  | 
| `'l'` | signed long | int | 4 |  | 
| `'L'` | unsigned long | int | 4 |  | 
| `'q'` | signed long long | int | 8 |  | 
| `'Q'` | unsigned long long | int | 8 |  | 
| `'f'` | float | float | 4 |  | 
| `'d'` | double | float | 8 |  | 

Notes:

1. It can be 16 bits or 32 bits depending on the platform. Changed in version 3.9: `array('u')` now uses`wchar_t` as C type instead of deprecated`Py_UNICODE` . This change doesn’t affect its behavior because`Py_UNICODE` is alias of`wchar_t` since Python 3.3.Deprecated since version 3.3, will be removed in version 3.16: Please migrate to `'w'` typecode.
2. Added in version 3.13.

See also

The [ctypes](ctypes.html#ctypes-fundamental-data-types) and
[struct](struct.html#format-characters) modules,
as well as third-party modules like [numpy](https://numpy.org/doc/stable/reference/arrays.interface.html#object.__array_interface__),
use similar – but slightly different – type codes.

The actual representation of values is determined by the machine architecture
(strictly speaking, by the C implementation).  The actual size can be accessed
through the [`array.itemsize`](#array.array.itemsize) attribute.

The module defines the following item:

- 
array.typecodes[¶](#array.typecodes)
- A string with all available type codes.

The module defines the following type:

- 
*class* array.array(*typecode* [,*initializer* ])[¶](#array.array)
- A new array whose items are restricted by *typecode* , and initialized
from the optional*initializer* value, which must be a[`bytes`](../builtins/stdtypes.html#bytes) or[`bytearray`](../builtins/stdtypes.html#bytearray) object, a Unicode string, or iterable over elements
of the appropriate type.If given a [`bytes`](../builtins/stdtypes.html#bytes) or[`bytearray`](../builtins/stdtypes.html#bytearray) object, the initializer
is passed to the new array’s[`frombytes()`](#array.array.frombytes) method;
if given a Unicode string, the initializer is passed to the[`fromunicode()`](#array.array.fromunicode) method;
otherwise, the initializer’s iterator is passed to the[`extend()`](#array.array.extend) method
to add initial items to the array.Array objects support the ordinary [mutable](../builtins/stdtypes.html#typesseq-mutable)[sequence](../glossary.html#term-sequence) operations of indexing, slicing,
concatenation, and multiplication.  When using slice assignment, the assigned
value must be an array object with the same type code; in all other cases,[`TypeError`](../builtins/exceptions.html#TypeError) is raised. Array objects also implement the buffer interface,
and may be used wherever[bytes-like objects](../glossary.html#term-bytes-like-object) are supported.Arrays are [generic](typing.html#generics) over the type of their contents.Raises an [auditing event](sys.html#auditing)`array.__new__` with arguments`typecode` ,`initializer` .
  - 
typecode[¶](#array.array.typecode)
  - The typecode character used to create the array.
 
  - 
itemsize[¶](#array.array.itemsize)
  - The length in bytes of one array item in the internal representation.
 
  - 
append(*value* ,*/* )[¶](#array.array.append)
  - Append a new item with the specified value to the end of the array.
 
  - 
buffer_info()[¶](#array.array.buffer_info)
  - Return a tuple `(address, length)` giving the current memory address and the
length in elements of the buffer used to hold array’s contents.  The size of the
memory buffer in bytes can be computed as```
array.buffer_info()[1] *
array.itemsize
```
.  This is occasionally useful when working with low-level (and
inherently unsafe) I/O interfaces that require memory addresses, such as certain`ioctl()` operations.  The returned numbers are valid as long as the array
exists and no length-changing operations are applied to it.Note When using array objects from code written in C or C++ (the only way to effectively make use of this information), it makes more sense to use the buffer interface supported by array objects. This method is maintained for backward compatibility and should be avoided in new code. The buffer interface is documented in [Buffer Protocol](../c-api/buffer.html#bufferobjects) .
 
  - 
byteswap()[¶](#array.array.byteswap)
  - “Byteswap” all items of the array. This is only supported for values which are 1, 2, 4, or 8 bytes in size; for other types of values, [`RuntimeError`](../builtins/exceptions.html#RuntimeError) is
raised.  It is useful when reading data from a file written on a machine with a
different byte order.
 
  - 
count(*value* ,*/* )[¶](#array.array.count)
  - Return the number of occurrences of *value* in the array.
 
  - 
extend(*iterable* ,*/* )[¶](#array.array.extend)
  - Append items from *iterable* to the end of the array.  If*iterable* is another
array, it must have*exactly* the same type code; if not,[`TypeError`](../builtins/exceptions.html#TypeError) will
be raised.  If*iterable* is not an array, it must be iterable and its elements
must be the right type to be appended to the array.
 
  - 
frombytes(*buffer* ,*/* )[¶](#array.array.frombytes)
  - Appends items from the [bytes-like object](../glossary.html#term-bytes-like-object) , interpreting
its content as an array of machine values (as if it had been read
from a file using the[`fromfile()`](#array.array.fromfile) method).Added in version 3.2: `fromstring()` is renamed to`frombytes()` for clarity.
 
  - 
fromfile(*f* ,*n* ,*/* )[¶](#array.array.fromfile)
  - Read *n* items (as machine values) from the[file object](../glossary.html#term-file-object)*f* and append
them to the end of the array.  If less than*n* items are available,[`EOFError`](../builtins/exceptions.html#EOFError) is raised, but the items that were available are still
inserted into the array.
 
  - 
fromlist(*list* ,*/* )[¶](#array.array.fromlist)
  - Append items from the list. This is equivalent to ```
for x in list:
a.append(x)
```
except that if there is a type error, the array is unchanged.
 
  - 
fromunicode(*ustr* ,*/* )[¶](#array.array.fromunicode)
  - Extends this array with data from the given Unicode string. The array must have type code `'u'` or`'w'` ; otherwise a[`ValueError`](../builtins/exceptions.html#ValueError) is raised.
Use`array.frombytes(unicodestring.encode(enc))` to append Unicode data to an
array of some other type.
 
  - 
index(*value* [,*start* [,*stop* ]])[¶](#array.array.index)
  - Return the smallest *i* such that*i* is the index of the first occurrence of*value* in the array.  The optional arguments*start* and*stop* can be
specified to search for*value* within a subsection of the array.  Raise[`ValueError`](../builtins/exceptions.html#ValueError) if*value* is not found.Changed in version 3.10: Added optional *start* and*stop* parameters.
 
  - 
insert(*index* ,*value* ,*/* )[¶](#array.array.insert)
  - Insert a new item *value* in the array before position*index* . Negative
values are treated as being relative to the end of the array.
 
  - 
pop(*index=-1* ,*/* )[¶](#array.array.pop)
  - Removes the item with the index *i* from the array and returns it. The optional
argument defaults to`-1` , so that by default the last item is removed and
returned.
 
  - 
remove(*value* ,*/* )[¶](#array.array.remove)
  - Remove the first occurrence of *value* from the array.
 
  - 
clear()[¶](#array.array.clear)
  - Remove all elements from the array. Added in version 3.13.
 
  - 
reverse()[¶](#array.array.reverse)
  - Reverse the order of the items in the array.
 
  - 
tobytes()[¶](#array.array.tobytes)
  - Convert the array to an array of machine values and return the bytes representation (the same sequence of bytes that would be written to a file by the [`tofile()`](#array.array.tofile) method.)Added in version 3.2: `tostring()` is renamed to`tobytes()` for clarity.
 
  - 
tofile(*f* ,*/* )[¶](#array.array.tofile)
  - Write all items (as machine values) to the [file object](../glossary.html#term-file-object)*f* .
 
  - 
tolist()[¶](#array.array.tolist)
  - Convert the array to an ordinary list with the same items.
 
  - 
tounicode()[¶](#array.array.tounicode)
  - Convert the array to a Unicode string. The array must have a type `'u'` or`'w'` ;
otherwise a[`ValueError`](../builtins/exceptions.html#ValueError) is raised. Use`array.tobytes().decode(enc)` to
obtain a Unicode string from an array of some other type.
- 
typecode

The string representation of array objects has the form
`array(typecode, initializer)`.
The *initializer* is omitted if the array is empty, otherwise it is
a Unicode string if the *typecode* is `'u'` or `'w'`, otherwise it is
a list of numbers.
The string representation is guaranteed to be able to be converted back to an
array with the same type and value using [`eval()`](../builtins/functions.html#eval), so long as the
[`array`](#array.array) class has been imported using `from array import array`.
Variables `inf` and `nan` must also be defined if it contains
corresponding floating-point values.
Examples:

```
array('l')
array('w', 'hello \u2641')
array('l', [1, 2, 3, 4, 5])
array('d', [1.0, 2.0, 3.14, -inf, nan])
```
