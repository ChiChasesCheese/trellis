---
title: dis — Disassembler for Python bytecode
corpus: python-docs
section: 61-dis
level: 1
locator: https://docs.python.org/3/library/dis.html
license: free-online
fetched: '2026-09-21'
---

# `dis` — Disassembler for Python bytecode[¶](#module-dis)

**Source code:** [Lib/dis.py](https://github.com/python/cpython/tree/3.14/Lib/dis.py)

The `dis` module supports the analysis of CPython [bytecode](../glossary.html#term-bytecode) by
disassembling it. The CPython bytecode which this module takes as an input is
defined in the file `Include/opcode.h` and used by the compiler and the
interpreter.

**CPython implementation detail:** Bytecode is an implementation detail of the CPython interpreter.  No
guarantees are made that bytecode will not be added, removed, or changed
between versions of Python.  Use of this module should not be considered to
work across Python VMs or Python releases.

Changed in version 3.6: Use 2 bytes for each instruction. Previously the number of bytes varied by instruction.

Changed in version 3.10: The argument of jump, exception handling and loop instructions is now the instruction offset rather than the byte offset.

Changed in version 3.11: Some instructions are accompanied by one or more inline cache entries,
which take the form of [`CACHE`](#opcode-CACHE) instructions. These instructions
are hidden by default, but can be shown by passing `show_caches=True` to
any `dis` utility. Furthermore, the interpreter now adapts the
bytecode to specialize it for different runtime conditions. The
adaptive bytecode can be shown by passing `adaptive=True`.

Changed in version 3.12: The argument of a jump is the offset of the target instruction relative
to the instruction that appears immediately after the jump instruction’s
[`CACHE`](#opcode-CACHE) entries.

As a consequence, the presence of the [`CACHE`](#opcode-CACHE) instructions is
transparent for forward jumps but needs to be taken into account when
reasoning about backward jumps.

Changed in version 3.13: The output shows logical labels rather than instruction offsets
for jump targets and exception handlers. The `-O` command line
option and the `show_offsets` argument were added.

Example: Given the function `myfunc()`:

```
def myfunc(alist):
    return len(alist)
```
the following command can be used to display the disassembly of
`myfunc()`:

```
>>> dis.dis(myfunc)
  2           RESUME                   0
  3           LOAD_GLOBAL              1 (len + NULL)
              LOAD_FAST_BORROW         0 (alist)
              CALL                     1
              RETURN_VALUE
```
(The “2” is a line number).

## Command-line interface[¶](#command-line-interface)

The `dis` module can be invoked as a script from the command line:

```
python -m dis [-h] [-C] [-O] [-P] [-S] [infile]
```
The following options are accepted:

- 
-h, --help[¶](#cmdoption-dis-h)
- Display usage and exit.

- 
-C, --show-caches[¶](#cmdoption-dis-C)
- Show inline caches. Added in version 3.13.

- 
-O, --show-offsets[¶](#cmdoption-dis-O)
- Show offsets of instructions. Added in version 3.13.

- 
-P, --show-positions[¶](#cmdoption-dis-P)
- Show positions of instructions in the source code. Added in version 3.14.

- 
-S, --specialized[¶](#cmdoption-dis-S)
- Show specialized bytecode. Added in version 3.14.

If `infile` is specified, its disassembled code will be written to stdout.
Otherwise, disassembly is performed on compiled source code received from stdin.

## Bytecode analysis[¶](#bytecode-analysis)

Added in version 3.4.

The bytecode analysis API allows pieces of Python code to be wrapped in a
[`Bytecode`](#dis.Bytecode) object that provides easy access to details of the compiled
code.

- 
*class* dis.Bytecode(*x* ,*** ,*first_line=None* ,*current_offset=None* ,*show_caches=False* ,*adaptive=False* ,*show_offsets=False* ,*show_positions=False* )[¶](#dis.Bytecode)
- Analyse the bytecode corresponding to a function, generator, asynchronous generator, coroutine, method, string of source code, or a code object (as returned by [`compile()`](../builtins/functions.html#compile) ).This is a convenience wrapper around many of the functions listed below, most notably [`get_instructions()`](#dis.get_instructions) , as iterating over a`Bytecode` instance yields the bytecode operations as[`Instruction`](#dis.Instruction) instances.If *first_line* is not`None` , it indicates the line number that should be
reported for the first source line in the disassembled code.  Otherwise, the
source line information (if any) is taken directly from the disassembled code
object.If *current_offset* is not`None` , it refers to an instruction offset in the
disassembled code. Setting this means[`dis()`](#dis.Bytecode.dis) will display a “current
instruction” marker against the specified opcode.If *show_caches* is`True` ,[`dis()`](#dis.Bytecode.dis) will display inline cache
entries used by the interpreter to specialize the bytecode.If *adaptive* is`True` ,[`dis()`](#dis.Bytecode.dis) will display specialized bytecode
that may be different from the original bytecode.If *show_offsets* is`True` ,[`dis()`](#dis.Bytecode.dis) will include instruction
offsets in the output.If *show_positions* is`True` ,[`dis()`](#dis.Bytecode.dis) will include instruction
source code positions in the output.
  - 
*classmethod* from_traceback(*tb* ,*** ,*show_caches=False* )[¶](#dis.Bytecode.from_traceback)
  - Construct a `Bytecode` instance from the given traceback, setting*current_offset* to the instruction responsible for the exception.
 
  - 
codeobj[¶](#dis.Bytecode.codeobj)
  - The compiled code object.
 
  - 
first_line[¶](#dis.Bytecode.first_line)
  - The first source line of the code object (if available)
 
  - 
dis()[¶](#dis.Bytecode.dis)
  - Return a formatted view of the bytecode operations (the same as printed by [`dis.dis()`](#dis.dis) , but returned as a multi-line string).
 
  - 
info()[¶](#dis.Bytecode.info)
  - Return a formatted multi-line string with detailed information about the code object, like [`code_info()`](#dis.code_info) .
 Changed in version 3.7: This can now handle coroutine and asynchronous generator objects. Changed in version 3.11: Added the *show_caches* and*adaptive* parameters.Changed in version 3.13: Added the *show_offsets* parameterChanged in version 3.14: Added the *show_positions* parameter.
- 

Example:

```
>>> bytecode = dis.Bytecode(myfunc)
>>> for instr in bytecode:
...     print(instr.opname)
...
RESUME
LOAD_GLOBAL
LOAD_FAST_BORROW
CALL
RETURN_VALUE
```
## Analysis functions[¶](#analysis-functions)

The `dis` module also defines the following analysis functions that convert
the input directly to the desired output. They can be useful if only a single
operation is being performed, so the intermediate analysis object isn’t useful:

- 
dis.code_info(*x* )[¶](#dis.code_info)
- Return a formatted multi-line string with detailed code object information for the supplied function, generator, asynchronous generator, coroutine, method, source code string or code object. Note that the exact contents of code info strings are highly implementation dependent and they may change arbitrarily across Python VMs or Python releases. Added in version 3.2. Changed in version 3.7: This can now handle coroutine and asynchronous generator objects.

- 
dis.show_code(*x* ,*** ,*file=None* )[¶](#dis.show_code)
- Print detailed code object information for the supplied function, method, source code string or code object to *file* (or`sys.stdout` if*file* is not specified).This is a convenient shorthand for `print(code_info(x), file=file)` ,
intended for interactive exploration at the interpreter prompt.Added in version 3.2. Changed in version 3.4: Added *file* parameter.

- 
dis.dis(*x=None* ,*** ,*file=None* ,*depth=None* ,*show_caches=False* ,*adaptive=False* ,*show_offsets=False* ,*show_positions=False* )[¶](#dis.dis)
- Disassemble the *x* object.*x* can denote either a module, a class, a
method, a function, a generator, an asynchronous generator, a coroutine,
a code object, a string of source code or a byte sequence of raw bytecode.
For a module, it disassembles all functions. For a class, it disassembles
all methods (including class and static methods). For a code object or
sequence of raw bytecode, it prints one line per bytecode instruction.
It also recursively disassembles nested code objects. These can include
generator expressions, nested functions, the bodies of nested classes,
and the code objects used for[annotation scopes](../reference/executionmodel.html#annotation-scopes) .
Strings are first compiled to code objects with the[`compile()`](../builtins/functions.html#compile) built-in function before being disassembled.  If no object is provided, this
function disassembles the last traceback.The disassembly is written as text to the supplied *file* argument if
provided and to`sys.stdout` otherwise.The maximal depth of recursion is limited by *depth* unless it is`None` .`depth=0` means no recursion.If *show_caches* is`True` , this function will display inline cache
entries used by the interpreter to specialize the bytecode.If *adaptive* is`True` , this function will display specialized bytecode
that may be different from the original bytecode.Changed in version 3.4: Added *file* parameter.Changed in version 3.7: Implemented recursive disassembling and added *depth* parameter.Changed in version 3.7: This can now handle coroutine and asynchronous generator objects. Changed in version 3.11: Added the *show_caches* and*adaptive* parameters.Changed in version 3.13: Added the *show_offsets* parameter.Changed in version 3.14: Added the *show_positions* parameter.

- 
dis.distb(*tb=None* ,*** ,*file=None* ,*show_caches=False* ,*adaptive=False* ,*show_offset=False* ,*show_positions=False* )[¶](#dis.distb)
- Disassemble the top-of-stack function of a traceback, using the last traceback if none was passed. The instruction causing the exception is indicated. The disassembly is written as text to the supplied *file* argument if
provided and to`sys.stdout` otherwise.Changed in version 3.4: Added *file* parameter.Changed in version 3.11: Added the *show_caches* and*adaptive* parameters.Changed in version 3.13: Added the *show_offsets* parameter.Changed in version 3.14: Added the *show_positions* parameter.

- 
dis.disassemble(*code* ,*lasti=-1* ,*** ,*file=None* ,*show_caches=False* ,*adaptive=False* ,*show_offsets=False* ,*show_positions=False* )[¶](#dis.disassemble)
- 
dis.disco(*code* ,*lasti=-1* ,*** ,*file=None* ,*show_caches=False* ,*adaptive=False* ,*show_offsets=False* ,*show_positions=False* )[¶](#dis.disco)
- Disassemble a code object, indicating the last instruction if *lasti* was
provided.  The output is divided in the following columns:
  1. the source code location of the instruction. Complete location information is shown if *show_positions* is true. Otherwise (the default) only the
line number is displayed.
  2. the current instruction, indicated as `-->` ,
  3. a labelled instruction, indicated with `>>` ,
  4. the address of the instruction,
  5. the operation code name,
  6. operation parameters, and
  7. interpretation of the parameters in parentheses.
 The parameter interpretation recognizes local and global variable names, constant values, branch targets, and compare operators. The disassembly is written as text to the supplied *file* argument if
provided and to`sys.stdout` otherwise.Changed in version 3.4: Added *file* parameter.Changed in version 3.11: Added the *show_caches* and*adaptive* parameters.Changed in version 3.13: Added the *show_offsets* parameter.Changed in version 3.14: Added the *show_positions* parameter.

- 
dis.get_instructions(*x* ,*** ,*first_line=None* ,*show_caches=False* ,*adaptive=False* )[¶](#dis.get_instructions)
- Return an iterator over the instructions in the supplied function, method, source code string or code object. The iterator generates a series of [`Instruction`](#dis.Instruction) named tuples giving
the details of each operation in the supplied code.If *first_line* is not`None` , it indicates the line number that should be
reported for the first source line in the disassembled code.  Otherwise, the
source line information (if any) is taken directly from the disassembled code
object.The *adaptive* parameter works as it does in[`dis()`](#module-dis) .Added in version 3.4. Changed in version 3.11: Added the *show_caches* and*adaptive* parameters.Changed in version 3.13: The *show_caches* parameter is deprecated and has no effect. The iterator
generates the[`Instruction`](#dis.Instruction) instances with the*cache_info* field populated (regardless of the value of*show_caches* ) and it no longer
generates separate items for the cache entries.

- 
dis.findlinestarts(*code* )[¶](#dis.findlinestarts)
- This generator function uses the [`co_lines()`](../reference/datamodel.html#codeobject.co_lines) method
of the[code object](../reference/datamodel.html#code-objects)*code* to find the offsets which
are starts of
lines in the source code.  They are generated as`(offset, lineno)` pairs.Changed in version 3.6: Line numbers can be decreasing. Before, they were always increasing. Changed in version 3.10: The [**PEP 626**](https://peps.python.org/pep-0626/)[`co_lines()`](../reference/datamodel.html#codeobject.co_lines) method is used instead of the[`co_firstlineno`](../reference/datamodel.html#codeobject.co_firstlineno) and[`co_lnotab`](../reference/datamodel.html#codeobject.co_lnotab) attributes of the[code object](../reference/datamodel.html#code-objects) .Changed in version 3.13: Line numbers can be `None` for bytecode that does not map to source lines.

- 
dis.findlabels(*code* )[¶](#dis.findlabels)
- Detect all offsets in the raw compiled bytecode string *code* which are jump targets, and
return a list of these offsets.

- 
dis.stack_effect(*opcode* ,*oparg=None* ,*** ,*jump=None* )[¶](#dis.stack_effect)
- Compute the stack effect of *opcode* with argument*oparg* .If the code has a jump target and *jump* is`True` ,`stack_effect()` will return the stack effect of jumping.  If*jump* is`False` ,
it will return the stack effect of not jumping. And if*jump* is`None` (default), it will return the maximal stack effect of both cases.Added in version 3.4. Changed in version 3.8: Added *jump* parameter.Changed in version 3.13: If `oparg` is omitted (or`None` ), the stack effect is now returned
for`oparg=0` . Previously this was an error for opcodes that use their
arg. It is also no longer an error to pass an integer`oparg` when
the`opcode` does not use it; the`oparg` in this case is ignored.

## Python Bytecode Instructions[¶](#python-bytecode-instructions)

The [`get_instructions()`](#dis.get_instructions) function and [`Bytecode`](#dis.Bytecode) class provide
details of bytecode instructions as [`Instruction`](#dis.Instruction) instances:

- 
*class* dis.Instruction[¶](#dis.Instruction)
- Details for a bytecode operation 
  - 
opcode[¶](#dis.Instruction.opcode)
  - numeric code for operation, corresponding to the opcode values listed below and the bytecode values in the [Opcode collections](#opcode-collections) .
 
  - 
opname[¶](#dis.Instruction.opname)
  - human readable name for operation
 
  - 
baseopcode[¶](#dis.Instruction.baseopcode)
  - numeric code for the base operation if operation is specialized; otherwise equal to [`opcode`](#dis.Instruction.opcode)
 
  - 
baseopname[¶](#dis.Instruction.baseopname)
  - human readable name for the base operation if operation is specialized; otherwise equal to [`opname`](#dis.opname)
 
  - 
arg[¶](#dis.Instruction.arg)
  - numeric argument to operation (if any), otherwise `None`
 
  - 
argval[¶](#dis.Instruction.argval)
  - resolved arg value (if any), otherwise `None`
 
  - 
argrepr[¶](#dis.Instruction.argrepr)
  - human readable description of operation argument (if any), otherwise an empty string.
 
  - 
offset[¶](#dis.Instruction.offset)
  - start index of operation within bytecode sequence
 
  - 
start_offset[¶](#dis.Instruction.start_offset)
  - start index of operation within bytecode sequence, including prefixed `EXTENDED_ARG` operations if present; otherwise equal to[`offset`](#dis.Instruction.offset)
 
  - 
cache_offset[¶](#dis.Instruction.cache_offset)
  - start index of the cache entries following the operation
 
  - 
end_offset[¶](#dis.Instruction.end_offset)
  - end index of the cache entries following the operation
 
  - 
starts_line[¶](#dis.Instruction.starts_line)
  - `True` if this opcode starts a source line, otherwise`False`
 
  - 
line_number[¶](#dis.Instruction.line_number)
  - source line number associated with this opcode (if any), otherwise `None`
 
  - 
is_jump_target[¶](#dis.Instruction.is_jump_target)
  - `True` if other code jumps to here, otherwise`False`
 
  - 
jump_target[¶](#dis.Instruction.jump_target)
  - bytecode index of the jump target if this is a jump operation, otherwise `None`
 
  - 
positions[¶](#dis.Instruction.positions)
  - [`dis.Positions`](#dis.Positions) object holding the
start and end locations that are covered by this instruction.
 
  - 
cache_info[¶](#dis.Instruction.cache_info)
  - Information about the cache entries of this instruction, as triplets of the form `(name, size, data)` , where the`name` and`size` describe the cache format and data is the contents
of the cache.`cache_info` is`None` if the instruction does not have
caches.
 Added in version 3.4. Changed in version 3.11: Field `positions` is added.Changed in version 3.13: Changed field `starts_line` .Added fields `start_offset` ,`cache_offset` ,`end_offset` ,`baseopname` ,`baseopcode` ,`jump_target` ,`oparg` ,`line_number` and`cache_info` .
- 
opcode

- 
*class* dis.Positions[¶](#dis.Positions)
- In case the information is not available, some fields might be `None` .
  - 
lineno[¶](#dis.Positions.lineno)
 
  - 
end_lineno[¶](#dis.Positions.end_lineno)
 
  - 
col_offset[¶](#dis.Positions.col_offset)
 
  - 
end_col_offset[¶](#dis.Positions.end_col_offset)
 Added in version 3.11.
- 
lineno

The Python compiler currently generates the following bytecode instructions.

**General instructions**

In the following, We will refer to the interpreter stack as `STACK` and describe
operations on it as if it was a Python list. The top of the stack corresponds to
`STACK[-1]` in this language.

- 
NOP[¶](#opcode-NOP)
- Do nothing code. Used as a placeholder by the bytecode optimizer, and to generate line tracing events.

- 
NOT_TAKEN[¶](#opcode-NOT_TAKEN)
- Do nothing code. Used by the interpreter to record [`BRANCH_LEFT`](sys.monitoring.html#monitoring-event-BRANCH_LEFT) and[`BRANCH_RIGHT`](sys.monitoring.html#monitoring-event-BRANCH_RIGHT) events for[`sys.monitoring`](sys.monitoring.html#module-sys.monitoring) .Added in version 3.14.

- 
POP_ITER[¶](#opcode-POP_ITER)
- Removes the iterator from the top of the stack. Added in version 3.14.

- 
POP_TOP[¶](#opcode-POP_TOP)
- Removes the top-of-stack item: STACK.pop()

- 
END_FOR[¶](#opcode-END_FOR)
- Removes the top-of-stack item. Equivalent to `POP_TOP` .
Used to clean up at the end of loops, hence the name.Added in version 3.12.

- 
END_SEND[¶](#opcode-END_SEND)
- Implements `del STACK[-2]` .
Used to clean up when a generator exits.Added in version 3.12.

- 
COPY(*i* )[¶](#opcode-COPY)
- Push the i-th item to the top of the stack without removing it from its original location: assert i > 0 STACK.append(STACK[-i]) Added in version 3.11.

- 
SWAP(*i* )[¶](#opcode-SWAP)
- Swap the top of the stack with the i-th element: STACK[-i], STACK[-1] = STACK[-1], STACK[-i] Added in version 3.11.

- 
CACHE[¶](#opcode-CACHE)
- Rather than being an actual instruction, this opcode is used to mark extra space for the interpreter to cache useful data directly in the bytecode itself. It is automatically hidden by all `dis` utilities, but can be
viewed with`show_caches=True` .Logically, this space is part of the preceding instruction. Many opcodes expect to be followed by an exact number of caches, and will instruct the interpreter to skip over them at runtime. Populated caches can look like arbitrary instructions, so great care should be taken when reading or modifying raw, adaptive bytecode containing quickened data. Added in version 3.11.

**Unary operations**

Unary operations take the top of the stack, apply the operation, and push the result back on the stack.

- 
UNARY_NEGATIVE[¶](#opcode-UNARY_NEGATIVE)
- Implements `STACK[-1] = -STACK[-1]` .

- 
UNARY_NOT[¶](#opcode-UNARY_NOT)
- Implements `STACK[-1] = not STACK[-1]` .Changed in version 3.13: This instruction now requires an exact [`bool`](../builtins/functions.html#bool) operand.

- 
UNARY_INVERT[¶](#opcode-UNARY_INVERT)
- Implements `STACK[-1] = ~STACK[-1]` .

- 
GET_ITER[¶](#opcode-GET_ITER)
- Implements `STACK[-1] = iter(STACK[-1])` .

- 
GET_YIELD_FROM_ITER[¶](#opcode-GET_YIELD_FROM_ITER)
- If `STACK[-1]` is a[generator iterator](../glossary.html#term-generator-iterator) or[coroutine](../glossary.html#term-coroutine) object
it is left as is.  Otherwise, implements`STACK[-1] = iter(STACK[-1])` .Added in version 3.5.

- 
TO_BOOL[¶](#opcode-TO_BOOL)
- Implements `STACK[-1] = bool(STACK[-1])` .Added in version 3.13.

**Binary and in-place operations**

Binary operations remove the top two items from the stack (`STACK[-1]` and
`STACK[-2]`). They perform the operation, then put the result back on the stack.

In-place operations are like binary operations, but the operation is done in-place
when `STACK[-2]` supports it, and the resulting `STACK[-1]` may be (but does
not have to be) the original `STACK[-2]`.

- 
BINARY_OP(*op* )[¶](#opcode-BINARY_OP)
- Implements the binary and in-place operators (depending on the value of *op* ):rhs = STACK.pop() lhs = STACK.pop() STACK.append(lhs op rhs) Added in version 3.11. Changed in version 3.14: With oparg : `NB_SUBSCR` , implements binary subscript (replaces opcode`BINARY_SUBSCR` )

- 
STORE_SUBSCR[¶](#opcode-STORE_SUBSCR)
- Implements: key = STACK.pop() container = STACK.pop() value = STACK.pop() container[key] = value

- 
DELETE_SUBSCR[¶](#opcode-DELETE_SUBSCR)
- Implements: key = STACK.pop() container = STACK.pop() del container[key]

- 
BINARY_SLICE[¶](#opcode-BINARY_SLICE)
- Implements: end = STACK.pop() start = STACK.pop() container = STACK.pop() STACK.append(container[start:end]) Added in version 3.12.

- 
STORE_SLICE[¶](#opcode-STORE_SLICE)
- Implements: end = STACK.pop() start = STACK.pop() container = STACK.pop() value = STACK.pop() container[start:end] = value Added in version 3.12.

**Coroutine opcodes**

- 
GET_AWAITABLE(*where* )[¶](#opcode-GET_AWAITABLE)
- Implements `STACK[-1] = get_awaitable(STACK[-1])` , where`get_awaitable(o)` returns`o` if`o` is a coroutine object or a generator object with
the[`CO_ITERABLE_COROUTINE`](inspect.html#inspect.CO_ITERABLE_COROUTINE) flag, or resolves`o.__await__` .If the `where` operand is nonzero, it indicates where the instruction
occurs:
  - `1` : After a call to`__aenter__`
  - `2` : After a call to`__aexit__`
 Added in version 3.5. Changed in version 3.11: Previously, this instruction did not have an oparg.

- 
GET_AITER[¶](#opcode-GET_AITER)
- Implements `STACK[-1] = STACK[-1].__aiter__()` .Added in version 3.5. Changed in version 3.7: Returning awaitable objects from `__aiter__` is no longer
supported.

- 
GET_ANEXT[¶](#opcode-GET_ANEXT)
- Implement `STACK.append(get_awaitable(STACK[-1].__anext__()))` to the stack.
See`GET_AWAITABLE` for details about`get_awaitable` .Added in version 3.5.

- 
END_ASYNC_FOR[¶](#opcode-END_ASYNC_FOR)
- Terminates an [`async for`](../reference/compound_stmts.html#async-for) loop.  Handles an exception raised
when awaiting a next item. The stack contains the async iterable in`STACK[-2]` and the raised exception in`STACK[-1]` . Both are popped.
If the exception is not[`StopAsyncIteration`](../builtins/exceptions.html#StopAsyncIteration) , it is re-raised.Added in version 3.8. Changed in version 3.11: Exception representation on the stack now consist of one, not three, items.

- 
CLEANUP_THROW[¶](#opcode-CLEANUP_THROW)
- Handles an exception raised during a [`throw()`](../reference/expressions.html#generator.throw) or[`close()`](../reference/expressions.html#generator.close) call through the current frame.  If`STACK[-1]` is an
instance of[`StopIteration`](../builtins/exceptions.html#StopIteration) , pop three values from the stack and push
its`value` member.  Otherwise, re-raise`STACK[-1]` .Added in version 3.12.

**Miscellaneous opcodes**

- 
SET_ADD(*i* )[¶](#opcode-SET_ADD)
- Implements: item = STACK.pop() set.add(STACK[-i], item) Used to implement set comprehensions.

- 
LIST_APPEND(*i* )[¶](#opcode-LIST_APPEND)
- Implements: item = STACK.pop() list.append(STACK[-i], item) Used to implement list comprehensions.

- 
MAP_ADD(*i* )[¶](#opcode-MAP_ADD)
- Implements: value = STACK.pop() key = STACK.pop() dict.__setitem__(STACK[-i], key, value) Used to implement dict comprehensions. Added in version 3.1. Changed in version 3.8: Map value is `STACK[-1]` and map key is`STACK[-2]` . Before, those
were reversed.

For all of the [`SET_ADD`](#opcode-SET_ADD), [`LIST_APPEND`](#opcode-LIST_APPEND) and [`MAP_ADD`](#opcode-MAP_ADD)
instructions, while the added value or key/value pair is popped off, the
container object remains on the stack so that it is available for further
iterations of the loop.

- 
RETURN_VALUE[¶](#opcode-RETURN_VALUE)
- Returns with `STACK[-1]` to the caller of the function.

- 
YIELD_VALUE[¶](#opcode-YIELD_VALUE)
- Yields `STACK.pop()` from a[generator](../glossary.html#term-generator) .Changed in version 3.11: oparg set to be the stack depth. Changed in version 3.12: oparg set to be the exception block depth, for efficient closing of generators. Changed in version 3.13: oparg is `1` if this instruction is part of a yield-from or await, and`0` otherwise.

- 
SETUP_ANNOTATIONS[¶](#opcode-SETUP_ANNOTATIONS)
- Checks whether `__annotations__` is defined in`locals()` , if not it is
set up to an empty`dict` . This opcode is only emitted if a class
or module body contains[variable annotations](../glossary.html#term-variable-annotation) statically.Added in version 3.6.

- 
POP_EXCEPT[¶](#opcode-POP_EXCEPT)
- Pops a value from the stack, which is used to restore the exception state. Changed in version 3.11: Exception representation on the stack now consist of one, not three, items.

- 
RERAISE[¶](#opcode-RERAISE)
- Re-raises the exception currently on top of the stack. If oparg is non-zero, pops an additional value from the stack which is used to set [`f_lasti`](../reference/datamodel.html#frame.f_lasti) of the current frame.Added in version 3.9. Changed in version 3.11: Exception representation on the stack now consist of one, not three, items.

- 
PUSH_EXC_INFO[¶](#opcode-PUSH_EXC_INFO)
- Pops a value from the stack. Pushes the current exception to the top of the stack. Pushes the value originally popped back to the stack. Used in exception handlers. Added in version 3.11.

- 
CHECK_EXC_MATCH[¶](#opcode-CHECK_EXC_MATCH)
- Performs exception matching for `except` . Tests whether the`STACK[-2]` is an exception matching`STACK[-1]` . Pops`STACK[-1]` and pushes the boolean
result of the test.Added in version 3.11.

- 
CHECK_EG_MATCH[¶](#opcode-CHECK_EG_MATCH)
- Performs exception matching for `except*` . Applies`split(STACK[-1])` on
the exception group representing`STACK[-2]` .In case of a match, pops two items from the stack and pushes the non-matching subgroup ( `None` in case of full match) followed by the
matching subgroup. When there is no match, pops one item (the match
type) and pushes`None` .Added in version 3.11.

- 
WITH_EXCEPT_START[¶](#opcode-WITH_EXCEPT_START)
- Calls the function in position 4 on the stack with arguments (type, val, tb) representing the exception at the top of the stack. Used to implement the call `context_manager.__exit__(*exc_info())` when an exception
has occurred in a[`with`](../reference/compound_stmts.html#with) statement.Added in version 3.9. Changed in version 3.11: The `__exit__` function is in position 4 of the stack rather than 7.
Exception representation on the stack now consist of one, not three, items.

- 
LOAD_COMMON_CONSTANT[¶](#opcode-LOAD_COMMON_CONSTANT)
- Pushes a common constant onto the stack. The interpreter contains a hardcoded list of constants supported by this instruction. Used by the [`assert`](../reference/simple_stmts.html#assert) statement to load[`AssertionError`](../builtins/exceptions.html#AssertionError) .Added in version 3.14.

- 
LOAD_BUILD_CLASS[¶](#opcode-LOAD_BUILD_CLASS)
- Pushes `builtins.__build_class__()` onto the stack.  It is later called
to construct a class.

- 
GET_LEN[¶](#opcode-GET_LEN)
- Perform `STACK.append(len(STACK[-1]))` . Used in[`match`](../reference/compound_stmts.html#match) statements where
comparison with structure of pattern is needed.Added in version 3.10.

- 
MATCH_MAPPING[¶](#opcode-MATCH_MAPPING)
- If `STACK[-1]` is an instance of[`collections.abc.Mapping`](collections.abc.html#collections.abc.Mapping) (or, more
technically: if it has the[`Py_TPFLAGS_MAPPING`](../c-api/typeobj.html#c.Py_TPFLAGS_MAPPING) flag set in its[`tp_flags`](../c-api/typeobj.html#c.PyTypeObject.tp_flags) ), push`True` onto the stack.  Otherwise,
push`False` .Added in version 3.10.

- 
MATCH_SEQUENCE[¶](#opcode-MATCH_SEQUENCE)
- If `STACK[-1]` is an instance of[`collections.abc.Sequence`](collections.abc.html#collections.abc.Sequence) and is*not* an instance
of[`str`](../builtins/stdtypes.html#str) /[`bytes`](../builtins/stdtypes.html#bytes) /[`bytearray`](../builtins/stdtypes.html#bytearray) (or, more technically: if it has
the[`Py_TPFLAGS_SEQUENCE`](../c-api/typeobj.html#c.Py_TPFLAGS_SEQUENCE) flag set in its[`tp_flags`](../c-api/typeobj.html#c.PyTypeObject.tp_flags) ),
push`True` onto the stack.  Otherwise, push`False` .Added in version 3.10.

- 
MATCH_KEYS[¶](#opcode-MATCH_KEYS)
- `STACK[-1]` is a tuple of mapping keys, and`STACK[-2]` is the match subject.
If`STACK[-2]` contains all of the keys in`STACK[-1]` , push a[`tuple`](../builtins/stdtypes.html#tuple) containing the corresponding values. Otherwise, push`None` .Added in version 3.10. Changed in version 3.11: Previously, this instruction also pushed a boolean value indicating success ( `True` ) or failure (`False` ).

- 
STORE_NAME(*namei* )[¶](#opcode-STORE_NAME)
- Implements `name = STACK.pop()` .*namei* is the index of*name* in the attribute[`co_names`](../reference/datamodel.html#codeobject.co_names) of the[code object](../reference/datamodel.html#code-objects) .
The compiler tries to use[`STORE_FAST`](#opcode-STORE_FAST) or[`STORE_GLOBAL`](#opcode-STORE_GLOBAL) if possible.

- 
DELETE_NAME(*namei* )[¶](#opcode-DELETE_NAME)
- Implements `del name` , where*namei* is the index into[`co_names`](../reference/datamodel.html#codeobject.co_names) attribute of the[code object](../reference/datamodel.html#code-objects) .

- 
UNPACK_SEQUENCE(*count* )[¶](#opcode-UNPACK_SEQUENCE)
- Unpacks `STACK[-1]` into*count* individual values, which are put onto the stack
right-to-left. Require there to be exactly*count* values.:assert(len(STACK[-1]) == count) STACK.extend(STACK.pop()[:-count-1:-1])

- 
UNPACK_EX(*counts* )[¶](#opcode-UNPACK_EX)
- Implements assignment with a starred target: Unpacks an iterable in `STACK[-1]` into individual values, where the total number of values can be smaller than the
number of items in the iterable: one of the new values will be a list of all
leftover items.The number of values before and after the list value is limited to 255. The number of values before the list value is encoded in the argument of the opcode. The number of values after the list if any is encoded using an `EXTENDED_ARG` . As a consequence, the argument can be seen as a two bytes values
where the low byte of*counts* is the number of values before the list value, the
high byte of*counts* the number of values after it.The extracted values are put onto the stack right-to-left, i.e. `a, *b, c = d` will be stored after execution as`STACK.extend((a, b, c))` .

- 
STORE_ATTR(*namei* )[¶](#opcode-STORE_ATTR)
- Implements: obj = STACK.pop() value = STACK.pop() obj.name = value where *namei* is the index of name in[`co_names`](../reference/datamodel.html#codeobject.co_names) of the[code object](../reference/datamodel.html#code-objects) .

- 
DELETE_ATTR(*namei* )[¶](#opcode-DELETE_ATTR)
- Implements: obj = STACK.pop() del obj.name where *namei* is the index of name into[`co_names`](../reference/datamodel.html#codeobject.co_names) of the[code object](../reference/datamodel.html#code-objects) .

- 
STORE_GLOBAL(*namei* )[¶](#opcode-STORE_GLOBAL)
- Works as [`STORE_NAME`](#opcode-STORE_NAME) , but stores the name as a global.

- 
DELETE_GLOBAL(*namei* )[¶](#opcode-DELETE_GLOBAL)
- Works as [`DELETE_NAME`](#opcode-DELETE_NAME) , but deletes a global name.

- 
LOAD_CONST(*consti* )[¶](#opcode-LOAD_CONST)
- Pushes `co_consts[consti]` onto the stack.

- 
LOAD_SMALL_INT(*i* )[¶](#opcode-LOAD_SMALL_INT)
- Pushes the integer `i` onto the stack.`i` must be in`range(256)`Added in version 3.14.

- 
LOAD_NAME(*namei* )[¶](#opcode-LOAD_NAME)
- Pushes the value associated with `co_names[namei]` onto the stack.
The name is looked up within the locals, then the globals, then the builtins.

- 
LOAD_LOCALS[¶](#opcode-LOAD_LOCALS)
- Pushes a reference to the locals dictionary onto the stack. This is used to prepare namespace dictionaries for [`LOAD_FROM_DICT_OR_DEREF`](#opcode-LOAD_FROM_DICT_OR_DEREF) and[`LOAD_FROM_DICT_OR_GLOBALS`](#opcode-LOAD_FROM_DICT_OR_GLOBALS) .Added in version 3.12.

- 
LOAD_FROM_DICT_OR_GLOBALS(*i* )[¶](#opcode-LOAD_FROM_DICT_OR_GLOBALS)
- Pops a mapping off the stack and looks up the value for `co_names[namei]` .
If the name is not found there, looks it up in the globals and then the builtins,
similar to[`LOAD_GLOBAL`](#opcode-LOAD_GLOBAL) .
This is used for loading global variables in[annotation scopes](../reference/executionmodel.html#annotation-scopes) within class bodies.Added in version 3.12.

- 
BUILD_TEMPLATE[¶](#opcode-BUILD_TEMPLATE)
- Constructs a new [`Template`](string.templatelib.html#string.templatelib.Template) instance from a tuple
of strings and a tuple of interpolations and pushes the resulting object
onto the stack:interpolations = STACK.pop() strings = STACK.pop() STACK.append(_build_template(strings, interpolations)) Added in version 3.14.

- 
BUILD_INTERPOLATION(*format* )[¶](#opcode-BUILD_INTERPOLATION)
- Constructs a new [`Interpolation`](string.templatelib.html#string.templatelib.Interpolation) instance from a
value and its source expression and pushes the resulting object onto the
stack.If no conversion or format specification is present, `format` is set to`2` .If the low bit of `format` is set, it indicates that the interpolation
contains a format specification.If `format >> 2` is non-zero, it indicates that the interpolation
contains a conversion. The value of`format >> 2` is the conversion type
(`0` for no conversion,`1` for`!s` ,`2` for`!r` , and`3` for`!a` ):conversion = format >> 2 if format & 1: format_spec = STACK.pop() else: format_spec = None expression = STACK.pop() value = STACK.pop() STACK.append(_build_interpolation(value, expression, conversion, format_spec)) Added in version 3.14.

- 
BUILD_TUPLE(*count* )[¶](#opcode-BUILD_TUPLE)
- Creates a tuple consuming *count* items from the stack, and pushes the
resulting tuple onto the stack:if count == 0: value = () else: value = tuple(STACK[-count:]) STACK = STACK[:-count] STACK.append(value)

- 
BUILD_LIST(*count* )[¶](#opcode-BUILD_LIST)
- Works as [`BUILD_TUPLE`](#opcode-BUILD_TUPLE) , but creates a list.

- 
BUILD_SET(*count* )[¶](#opcode-BUILD_SET)
- Works as [`BUILD_TUPLE`](#opcode-BUILD_TUPLE) , but creates a set.

- 
BUILD_MAP(*count* )[¶](#opcode-BUILD_MAP)
- Pushes a new dictionary object onto the stack. Pops `2 * count` items
so that the dictionary holds*count* entries:`{..., STACK[-4]: STACK[-3], STACK[-2]: STACK[-1]}` .Changed in version 3.5: The dictionary is created from stack items instead of creating an empty dictionary pre-sized to hold *count* items.

- 
BUILD_STRING(*count* )[¶](#opcode-BUILD_STRING)
- Concatenates *count* strings from the stack and pushes the resulting string
onto the stack.Added in version 3.6.

- 
LIST_EXTEND(*i* )[¶](#opcode-LIST_EXTEND)
- Implements: seq = STACK.pop() list.extend(STACK[-i], seq) Used to build lists. Added in version 3.9.

- 
SET_UPDATE(*i* )[¶](#opcode-SET_UPDATE)
- Implements: seq = STACK.pop() set.update(STACK[-i], seq) Used to build sets. Added in version 3.9.

- 
DICT_UPDATE(*i* )[¶](#opcode-DICT_UPDATE)
- Implements: map = STACK.pop() dict.update(STACK[-i], map) Used to build dicts. Added in version 3.9.

- 
DICT_MERGE(*i* )[¶](#opcode-DICT_MERGE)
- Like [`DICT_UPDATE`](#opcode-DICT_UPDATE) but raises an exception for duplicate keys.Added in version 3.9.

- 
LOAD_ATTR(*namei* )[¶](#opcode-LOAD_ATTR)
- If the low bit of `namei` is not set, this replaces`STACK[-1]` with`getattr(STACK[-1], co_names[namei>>1])` .If the low bit of `namei` is set, this will attempt to load a method named`co_names[namei>>1]` from the`STACK[-1]` object.`STACK[-1]` is popped.
This bytecode distinguishes two cases: if`STACK[-1]` has a method with the
correct name, the bytecode pushes the unbound method and`STACK[-1]` .`STACK[-1]` will be used as the first argument (`self` ) by[`CALL`](#opcode-CALL) or[`CALL_KW`](#opcode-CALL_KW) when calling the unbound method.
Otherwise,`NULL` and the object returned by
the attribute lookup are pushed.Changed in version 3.12: If the low bit of `namei` is set, then a`NULL` or`self` is
pushed to the stack before the attribute or unbound method respectively.

- 
LOAD_SUPER_ATTR(*namei* )[¶](#opcode-LOAD_SUPER_ATTR)
- This opcode implements [`super()`](../builtins/functions.html#super) , both in its zero-argument and
two-argument forms (e.g.`super().method()` ,`super().attr` and`super(cls, self).method()` ,`super(cls, self).attr` ).It pops three values from the stack (from top of stack down): 
  - `self` : the first argument to the current method
  - `cls` : the class within which the current method was defined
  - the global `super`
 With respect to its argument, it works similarly to [`LOAD_ATTR`](#opcode-LOAD_ATTR) ,
except that`namei` is shifted left by 2 bits instead of 1.The low bit of `namei` signals to attempt a method load, as with[`LOAD_ATTR`](#opcode-LOAD_ATTR) , which results in pushing`NULL` and the loaded method.
When it is unset a single value is pushed to the stack.The second-low bit of `namei` , if set, means that this was a two-argument
call to[`super()`](../builtins/functions.html#super) (unset means zero-argument).Added in version 3.12.

- 
COMPARE_OP(*opname* )[¶](#opcode-COMPARE_OP)
- Performs a Boolean operation. The operation name can be found in `cmp_op[opname >> 5]` . If the fifth-lowest bit of`opname` is set
(`opname & 16` ), the result should be coerced to`bool` .Changed in version 3.13: The fifth-lowest bit of the oparg now indicates a forced conversion to [`bool`](../builtins/functions.html#bool) .

- 
IS_OP(*invert* )[¶](#opcode-IS_OP)
- Performs `is` comparison, or`is not` if`invert` is 1.Added in version 3.9.

- 
CONTAINS_OP(*invert* )[¶](#opcode-CONTAINS_OP)
- Performs `in` comparison, or`not in` if`invert` is 1.Added in version 3.9.

- 
IMPORT_NAME(*namei* )[¶](#opcode-IMPORT_NAME)
- Imports the module `co_names[namei]` .`STACK[-1]` and`STACK[-2]` are
popped and provide the*fromlist* and*level* arguments of[`__import__()`](../builtins/functions.html#import__) .
The module object is pushed onto the stack.  The current namespace is not affected: for a proper import statement, a subsequent[`STORE_FAST`](#opcode-STORE_FAST) instruction
modifies the namespace.

- 
IMPORT_FROM(*namei* )[¶](#opcode-IMPORT_FROM)
- Loads the attribute `co_names[namei]` from the module found in`STACK[-1]` .
The resulting object is pushed onto the stack, to be subsequently stored by a[`STORE_FAST`](#opcode-STORE_FAST) instruction.

- 
JUMP_FORWARD(*delta* )[¶](#opcode-JUMP_FORWARD)
- Increments bytecode counter by *delta* .

- 
JUMP_BACKWARD(*delta* )[¶](#opcode-JUMP_BACKWARD)
- Decrements bytecode counter by *delta* . Checks for interrupts.Added in version 3.11.

- 
JUMP_BACKWARD_NO_INTERRUPT(*delta* )[¶](#opcode-JUMP_BACKWARD_NO_INTERRUPT)
- Decrements bytecode counter by *delta* . Does not check for interrupts.Added in version 3.11.

- 
POP_JUMP_IF_TRUE(*delta* )[¶](#opcode-POP_JUMP_IF_TRUE)
- If `STACK[-1]` is true, increments the bytecode counter by*delta* .`STACK[-1]` is popped.Changed in version 3.11: The oparg is now a relative delta rather than an absolute target. This opcode is a pseudo-instruction, replaced in final bytecode by the directed versions (forward/backward). Changed in version 3.12: This is no longer a pseudo-instruction. Changed in version 3.13: This instruction now requires an exact [`bool`](../builtins/functions.html#bool) operand.

- 
POP_JUMP_IF_FALSE(*delta* )[¶](#opcode-POP_JUMP_IF_FALSE)
- If `STACK[-1]` is false, increments the bytecode counter by*delta* .`STACK[-1]` is popped.Changed in version 3.11: The oparg is now a relative delta rather than an absolute target. This opcode is a pseudo-instruction, replaced in final bytecode by the directed versions (forward/backward). Changed in version 3.12: This is no longer a pseudo-instruction. Changed in version 3.13: This instruction now requires an exact [`bool`](../builtins/functions.html#bool) operand.

- 
POP_JUMP_IF_NOT_NONE(*delta* )[¶](#opcode-POP_JUMP_IF_NOT_NONE)
- If `STACK[-1]` is not`None` , increments the bytecode counter by*delta* .`STACK[-1]` is popped.Added in version 3.11. Changed in version 3.12: This is no longer a pseudo-instruction.

- 
POP_JUMP_IF_NONE(*delta* )[¶](#opcode-POP_JUMP_IF_NONE)
- If `STACK[-1]` is`None` , increments the bytecode counter by*delta* .`STACK[-1]` is popped.Added in version 3.11. Changed in version 3.12: This is no longer a pseudo-instruction.

- 
FOR_ITER(*delta* )[¶](#opcode-FOR_ITER)
- `STACK[-1]` is an[iterator](../glossary.html#term-iterator) .  Call its[`__next__()`](../builtins/stdtypes.html#iterator.__next__) method.
If this yields a new value, push it on the stack (leaving the iterator below
it).  If the iterator indicates it is[exhausted](../glossary.html#term-exhausted) then the byte code counter is
incremented by*delta* .Changed in version 3.12: Up until 3.11 the iterator was popped when it was exhausted.

- 
LOAD_GLOBAL(*namei* )[¶](#opcode-LOAD_GLOBAL)
- Loads the global named `co_names[namei>>1]` onto the stack.Changed in version 3.11: If the low bit of `namei` is set, then a`NULL` is pushed to the
stack before the global variable.

- 
LOAD_FAST(*var_num* )[¶](#opcode-LOAD_FAST)
- Pushes a reference to the local `co_varnames[var_num]` onto the stack.Changed in version 3.12: This opcode is now only used in situations where the local variable is guaranteed to be initialized. It cannot raise [`UnboundLocalError`](../builtins/exceptions.html#UnboundLocalError) .

- 
LOAD_FAST_BORROW(*var_num* )[¶](#opcode-LOAD_FAST_BORROW)
- Pushes a borrowed reference to the local `co_varnames[var_num]` onto the
stack.Added in version 3.14.

- 
LOAD_FAST_LOAD_FAST(*var_nums* )[¶](#opcode-LOAD_FAST_LOAD_FAST)
- Pushes references to `co_varnames[var_nums >> 4]` and`co_varnames[var_nums & 15]` onto the stack.Added in version 3.13.

- 
LOAD_FAST_BORROW_LOAD_FAST_BORROW(*var_nums* )[¶](#opcode-LOAD_FAST_BORROW_LOAD_FAST_BORROW)
- Pushes borrowed references to `co_varnames[var_nums >> 4]` and`co_varnames[var_nums & 15]` onto the stack.Added in version 3.14.

- 
LOAD_FAST_CHECK(*var_num* )[¶](#opcode-LOAD_FAST_CHECK)
- Pushes a reference to the local `co_varnames[var_num]` onto the stack,
raising an[`UnboundLocalError`](../builtins/exceptions.html#UnboundLocalError) if the local variable has not been
initialized.Added in version 3.12.

- 
LOAD_FAST_AND_CLEAR(*var_num* )[¶](#opcode-LOAD_FAST_AND_CLEAR)
- Pushes a reference to the local `co_varnames[var_num]` onto the stack (or
pushes`NULL` onto the stack if the local variable has not been
initialized) and sets`co_varnames[var_num]` to`NULL` .Added in version 3.12.

- 
STORE_FAST(*var_num* )[¶](#opcode-STORE_FAST)
- Stores `STACK.pop()` into the local`co_varnames[var_num]` .

- 
STORE_FAST_STORE_FAST(*var_nums* )[¶](#opcode-STORE_FAST_STORE_FAST)
- Stores `STACK[-1]` into`co_varnames[var_nums >> 4]` and`STACK[-2]` into`co_varnames[var_nums & 15]` .Added in version 3.13.

- 
STORE_FAST_LOAD_FAST(*var_nums* )[¶](#opcode-STORE_FAST_LOAD_FAST)
- Stores `STACK.pop()` into the local`co_varnames[var_nums >> 4]` and pushes a reference to the local`co_varnames[var_nums & 15]` onto the stack.Added in version 3.13.

- 
DELETE_FAST(*var_num* )[¶](#opcode-DELETE_FAST)
- Deletes local `co_varnames[var_num]` .

- 
MAKE_CELL(*i* )[¶](#opcode-MAKE_CELL)
- Creates a new cell in slot `i` .  If that slot is nonempty then
that value is stored into the new cell.Added in version 3.11.

- 
LOAD_DEREF(*i* )[¶](#opcode-LOAD_DEREF)
- Loads the cell contained in slot `i` of the “fast locals” storage.
Pushes a reference to the object the cell contains on the stack.Changed in version 3.11: `i` is no longer offset by the length of[`co_varnames`](../reference/datamodel.html#codeobject.co_varnames) .

- 
LOAD_FROM_DICT_OR_DEREF(*i* )[¶](#opcode-LOAD_FROM_DICT_OR_DEREF)
- Pops a mapping off the stack and looks up the name associated with slot `i` of the “fast locals” storage in this mapping.
If the name is not found there, loads it from the cell contained in
slot`i` , similar to[`LOAD_DEREF`](#opcode-LOAD_DEREF) . This is used for loading[closure variables](../glossary.html#term-closure-variable) in class bodies (which previously used`LOAD_CLASSDEREF` ) and in[annotation scopes](../reference/executionmodel.html#annotation-scopes) within class bodies.Added in version 3.12.

- 
STORE_DEREF(*i* )[¶](#opcode-STORE_DEREF)
- Stores `STACK.pop()` into the cell contained in slot`i` of the “fast locals”
storage.Changed in version 3.11: `i` is no longer offset by the length of[`co_varnames`](../reference/datamodel.html#codeobject.co_varnames) .

- 
DELETE_DEREF(*i* )[¶](#opcode-DELETE_DEREF)
- Empties the cell contained in slot `i` of the “fast locals” storage.
Used by the[`del`](../reference/simple_stmts.html#del) statement.Added in version 3.2. Changed in version 3.11: `i` is no longer offset by the length of[`co_varnames`](../reference/datamodel.html#codeobject.co_varnames) .

- 
COPY_FREE_VARS(*n* )[¶](#opcode-COPY_FREE_VARS)
- Copies the `n`[free (closure) variables](../glossary.html#term-closure-variable) from the closure
into the frame. Removes the need for special code on the caller’s side when calling
closures.Added in version 3.11.

- 
RAISE_VARARGS(*argc* )[¶](#opcode-RAISE_VARARGS)
- Raises an exception using one of the 3 forms of the `raise` statement,
depending on the value of*argc* :
  - 0: `raise` (re-raise previous exception)
  - 1: `raise STACK[-1]` (raise exception instance or type at`STACK[-1]` )
  - 2: `raise STACK[-2] from STACK[-1]` (raise exception instance or type at`STACK[-2]` with`__cause__` set to`STACK[-1]` )

- 
CALL(*argc* )[¶](#opcode-CALL)
- Calls a callable object with the number of arguments specified by `argc` .
On the stack are (in ascending order):
  - The callable
  - `self` or`NULL`
  - The remaining positional arguments
 `argc` is the total of the positional arguments, excluding`self` .`CALL` pops all arguments and the callable object off the stack,
calls the callable object with those arguments, and pushes the return value
returned by the callable object.Added in version 3.11. Changed in version 3.13: The callable now always appears at the same position on the stack. Changed in version 3.13: Calls with keyword arguments are now handled by [`CALL_KW`](#opcode-CALL_KW) .

- 
CALL_KW(*argc* )[¶](#opcode-CALL_KW)
- Calls a callable object with the number of arguments specified by `argc` ,
including one or more named arguments. On the stack are (in ascending order):
  - The callable
  - `self` or`NULL`
  - The remaining positional arguments
  - The named arguments
  - A [`tuple`](../builtins/stdtypes.html#tuple) of keyword argument names
 `argc` is the total of the positional and named arguments, excluding`self` .
The length of the tuple of keyword argument names is the number of named arguments.`CALL_KW` pops all arguments, the keyword names, and the callable object
off the stack, calls the callable object with those arguments, and pushes the
return value returned by the callable object.Added in version 3.13.

- 
CALL_FUNCTION_EX(*flags* )[¶](#opcode-CALL_FUNCTION_EX)
- Calls a callable object with variable set of positional and keyword arguments. If the lowest bit of *flags* is set, the top of the stack
contains a mapping object containing additional keyword arguments.
Before the callable is called, the mapping object and iterable object
are each “unpacked” and their contents passed in as keyword and
positional arguments respectively.`CALL_FUNCTION_EX` pops all arguments and the callable object off the stack,
calls the callable object with those arguments, and pushes the return value
returned by the callable object.Added in version 3.6.

- 
PUSH_NULL[¶](#opcode-PUSH_NULL)
- Pushes a `NULL` to the stack.
Used in the call sequence to match the`NULL` pushed by`LOAD_METHOD` for non-method calls.Added in version 3.11.

- 
MAKE_FUNCTION[¶](#opcode-MAKE_FUNCTION)
- Pushes a new function object on the stack built from the code object at `STACK[-1]` .Changed in version 3.10: Flag value `0x04` is a tuple of strings instead of dictionaryChanged in version 3.11: Qualified name at `STACK[-1]` was removed.Changed in version 3.13: Extra function attributes on the stack, signaled by oparg flags, were removed. They now use [`SET_FUNCTION_ATTRIBUTE`](#opcode-SET_FUNCTION_ATTRIBUTE) .

- 
SET_FUNCTION_ATTRIBUTE(*flag* )[¶](#opcode-SET_FUNCTION_ATTRIBUTE)
- Sets an attribute on a function object. Expects the function at `STACK[-1]` and the attribute value to set at`STACK[-2]` ; consumes both and leaves the
function at`STACK[-1]` . The flag determines which attribute to set:
  - `0x01` a tuple of default values for positional-only and
positional-or-keyword parameters in positional order
  - `0x02` a dictionary of keyword-only parameters’ default values
  - `0x04` a tuple of strings containing parameters’ annotations
  - `0x08` a tuple containing cells for free variables, making a closure
  - `0x10` the[annotate function](../glossary.html#term-annotate-function) for the function object
 Added in version 3.13. Changed in version 3.14: Added `0x10` to indicate the annotate function for the function object.

- 
BUILD_SLICE(*argc* )[¶](#opcode-BUILD_SLICE)
- Pushes a slice object on the stack. *argc* must be 2 or 3.  If it is 2, implements:end = STACK.pop() start = STACK.pop() STACK.append(slice(start, end)) if it is 3, implements: step = STACK.pop() end = STACK.pop() start = STACK.pop() STACK.append(slice(start, end, step)) See the [`slice()`](../builtins/functions.html#slice) built-in function for more information.

- 
EXTENDED_ARG(*ext* )[¶](#opcode-EXTENDED_ARG)
- Prefixes any opcode which has an argument too big to fit into the default one byte. *ext* holds an additional byte which act as higher bits in the argument.
For each opcode, at most three prefixal`EXTENDED_ARG` are allowed, forming
an argument from two-byte to four-byte.

- 
CONVERT_VALUE(*oparg* )[¶](#opcode-CONVERT_VALUE)
- Convert value to a string, depending on `oparg` :value = STACK.pop() result = func(value) STACK.append(result) Used for implementing formatted string literals (f-strings). Added in version 3.13.

- 
FORMAT_SIMPLE[¶](#opcode-FORMAT_SIMPLE)
- Formats the value on top of stack: value = STACK.pop() result = value.__format__("") STACK.append(result) Used for implementing formatted string literals (f-strings). Added in version 3.13.

- 
FORMAT_WITH_SPEC[¶](#opcode-FORMAT_WITH_SPEC)
- Formats the given value with the given format spec: spec = STACK.pop() value = STACK.pop() result = value.__format__(spec) STACK.append(result) Used for implementing formatted string literals (f-strings). Added in version 3.13.

- 
MATCH_CLASS(*count* )[¶](#opcode-MATCH_CLASS)
- `STACK[-1]` is a tuple of keyword attribute names,`STACK[-2]` is the class
being matched against, and`STACK[-3]` is the match subject.*count* is the
number of positional sub-patterns.Pop `STACK[-1]` ,`STACK[-2]` , and`STACK[-3]` . If`STACK[-3]` is an
instance of`STACK[-2]` and has the positional and keyword attributes
required by*count* and`STACK[-1]` , push a tuple of extracted attributes.
Otherwise, push`None` .Added in version 3.10. Changed in version 3.11: Previously, this instruction also pushed a boolean value indicating success ( `True` ) or failure (`False` ).

- 
RESUME(*context* )[¶](#opcode-RESUME)
- A no-op. Performs internal tracing, debugging and optimization checks. The `context` operand consists of two parts. The lowest two bits
indicate where the`RESUME` occurs:
  - `0` The start of a function, which is neither a generator, coroutine
nor an async generator
  - `1` After a`yield` expression
  - `2` After a`yield from` expression
  - `3` After an`await` expression
 The next bit is `1` if the RESUME is at except-depth`1` , and`0` otherwise.Added in version 3.11. Changed in version 3.13: The oparg value changed to include information about except-depth

- 
RETURN_GENERATOR[¶](#opcode-RETURN_GENERATOR)
- Create a generator, coroutine, or async generator from the current frame. Used as first opcode of in code object for the above mentioned callables. Clear the current frame and return the newly created generator. Added in version 3.11.

- 
SEND(*delta* )[¶](#opcode-SEND)
- Equivalent to `STACK[-1] = STACK[-2].send(STACK[-1])` . Used in`yield from` and`await` statements.If the call raises [`StopIteration`](../builtins/exceptions.html#StopIteration) , pop the top value from the stack,
push the exception’s`value` attribute, and increment the bytecode counter
by*delta* .Added in version 3.11.

- 
HAVE_ARGUMENT[¶](#opcode-HAVE_ARGUMENT)
- This is not really an opcode. It identifies the dividing line between opcodes in the range [0,255] which don’t use their argument and those that do ( `< HAVE_ARGUMENT` and`>= HAVE_ARGUMENT` , respectively).If your application uses pseudo instructions or specialized instructions, use the [`hasarg`](#dis.hasarg) collection instead.Changed in version 3.6: Now every instruction has an argument, but opcodes `< HAVE_ARGUMENT` ignore it. Before, only opcodes`>= HAVE_ARGUMENT` had an argument.Changed in version 3.12: Pseudo instructions were added to the `dis` module, and for them
it is not true that comparison with`HAVE_ARGUMENT` indicates whether
they use their arg.Deprecated since version 3.13: Use [`hasarg`](#dis.hasarg) instead.

- 
CALL_INTRINSIC_1[¶](#opcode-CALL_INTRINSIC_1)
- Calls an intrinsic function with one argument. Passes `STACK[-1]` as the
argument and sets`STACK[-1]` to the result. Used to implement
functionality that is not performance critical.The operand determines which intrinsic function is called: Operand Description `INTRINSIC_1_INVALID`Not valid `INTRINSIC_PRINT`Prints the argument to standard out. Used in the REPL. `INTRINSIC_IMPORT_STAR`Performs `import *` for the
named module.`INTRINSIC_STOPITERATION_ERROR`Extracts the return value from a `StopIteration` exception.`INTRINSIC_ASYNC_GEN_WRAP`Wraps an async generator value `INTRINSIC_UNARY_POSITIVE`Performs the unary `+` operation`INTRINSIC_LIST_TO_TUPLE`Converts a list to a tuple `INTRINSIC_TYPEVAR`Creates a [`typing.TypeVar`](typing.html#typing.TypeVar)`INTRINSIC_PARAMSPEC`Creates a [`typing.ParamSpec`](typing.html#typing.ParamSpec)`INTRINSIC_TYPEVARTUPLE`Creates a [`typing.TypeVarTuple`](typing.html#typing.TypeVarTuple)`INTRINSIC_SUBSCRIPT_GENERIC`Returns [`typing.Generic`](typing.html#typing.Generic) subscripted with the argument`INTRINSIC_TYPEALIAS`Creates a [`typing.TypeAliasType`](typing.html#typing.TypeAliasType) ;
used in the[`type`](../reference/simple_stmts.html#type) statement. The argument is a tuple
of the type alias’s name,
type parameters, and value.Added in version 3.12.

- 
CALL_INTRINSIC_2[¶](#opcode-CALL_INTRINSIC_2)
- Calls an intrinsic function with two arguments. Used to implement functionality that is not performance critical: arg2 = STACK.pop() arg1 = STACK.pop() result = intrinsic2(arg1, arg2) STACK.append(result) The operand determines which intrinsic function is called: Operand Description `INTRINSIC_2_INVALID`Not valid `INTRINSIC_PREP_RERAISE_STAR`Calculates the [`ExceptionGroup`](../builtins/exceptions.html#ExceptionGroup) to raise
from a`try-except*` .`INTRINSIC_TYPEVAR_WITH_BOUND`Creates a [`typing.TypeVar`](typing.html#typing.TypeVar) with a bound.`INTRINSIC_TYPEVAR_WITH_CONSTRAINTS`Creates a [`typing.TypeVar`](typing.html#typing.TypeVar) with
constraints.`INTRINSIC_SET_FUNCTION_TYPE_PARAMS`Sets the `__type_params__` attribute of a function.Added in version 3.12.

- 
LOAD_SPECIAL[¶](#opcode-LOAD_SPECIAL)
- Performs special method lookup on `STACK[-1]` .
If`type(STACK[-1]).__xxx__` is a method, leave`type(STACK[-1]).__xxx__; STACK[-1]` on the stack.
If`type(STACK[-1]).__xxx__` is not a method, leave`STACK[-1].__xxx__; NULL` on the stack.Added in version 3.14.

**Pseudo-instructions**

These opcodes do not appear in Python bytecode. They are used by the compiler but are replaced by real opcodes or removed before bytecode is generated.

- 
SETUP_FINALLY(*target* )[¶](#opcode-SETUP_FINALLY)
- Set up an exception handler for the following code block. If an exception occurs, the value stack level is restored to its current state and control is transferred to the exception handler at `target` .

- 
SETUP_CLEANUP(*target* )[¶](#opcode-SETUP_CLEANUP)
- Like `SETUP_FINALLY` , but in case of an exception also pushes the last
instruction (`lasti` ) to the stack so that`RERAISE` can restore it.
If an exception occurs, the value stack level and the last instruction on
the frame are restored to their current state, and control is transferred
to the exception handler at`target` .

- 
SETUP_WITH(*target* )[¶](#opcode-SETUP_WITH)
- Like `SETUP_CLEANUP` , but in case of an exception one more item is popped
from the stack before control is transferred to the exception handler at`target` .This variant is used in [`with`](../reference/compound_stmts.html#with) and[`async with`](../reference/compound_stmts.html#async-with) constructs, which push the return value of the context manager’s[`__enter__()`](../reference/datamodel.html#object.__enter__) or[`__aenter__()`](../reference/datamodel.html#object.__aenter__) to the stack.

- 
POP_BLOCK[¶](#opcode-POP_BLOCK)
- Marks the end of the code block associated with the last `SETUP_FINALLY` ,`SETUP_CLEANUP` or`SETUP_WITH` .

- 
LOAD_CONST_IMMORTAL(*consti* )[¶](#opcode-LOAD_CONST_IMMORTAL)
- Works as [`LOAD_CONST`](#opcode-LOAD_CONST) , but is more efficient for immortal objects.

- 
JUMP[¶](#opcode-JUMP)
- 
JUMP_NO_INTERRUPT[¶](#opcode-JUMP_NO_INTERRUPT)
- Undirected relative jump instructions which are replaced by their directed (forward/backward) counterparts by the assembler.

- 
JUMP_IF_TRUE[¶](#opcode-JUMP_IF_TRUE)
- 
JUMP_IF_FALSE[¶](#opcode-JUMP_IF_FALSE)
- Conditional jumps which do not impact the stack. Replaced by the sequence `COPY 1` ,`TO_BOOL` ,`POP_JUMP_IF_TRUE/FALSE` .

- 
LOAD_CLOSURE(*i* )[¶](#opcode-LOAD_CLOSURE)
- Pushes a reference to the cell contained in slot `i` of the “fast locals”
storage.Note that `LOAD_CLOSURE` is replaced with`LOAD_FAST` in the assembler.Changed in version 3.13: This opcode is now a pseudo-instruction.

## Opcode collections[¶](#opcode-collections)

These collections are provided for automatic introspection of bytecode instructions:

Changed in version 3.12: The collections now contain pseudo instructions and instrumented
instructions as well. These are opcodes with values `>= MIN_PSEUDO_OPCODE`
and `>= MIN_INSTRUMENTED_OPCODE`.

- 
dis.opname[¶](#dis.opname)
- Sequence of operation names, indexable using the bytecode.

- 
dis.opmap[¶](#dis.opmap)
- Dictionary mapping operation names to bytecodes.

- 
dis.cmp_op[¶](#dis.cmp_op)
- Sequence of all compare operation names.

- 
dis.hasarg[¶](#dis.hasarg)
- Sequence of bytecodes that use their argument. Added in version 3.12.

- 
dis.hasconst[¶](#dis.hasconst)
- Sequence of bytecodes that access a constant.

- 
dis.hasfree[¶](#dis.hasfree)
- Sequence of bytecodes that access a [free (closure) variable](../glossary.html#term-closure-variable) .
‘free’ in this context refers to names in the current scope that are
referenced by inner scopes or names in outer scopes that are referenced
from this scope.  It does*not* include references to global or builtin scopes.

- 
dis.hasname[¶](#dis.hasname)
- Sequence of bytecodes that access an attribute by name.

- 
dis.hasjump[¶](#dis.hasjump)
- Sequence of bytecodes that have a jump target. All jumps are relative. Added in version 3.13.

- 
dis.haslocal[¶](#dis.haslocal)
- Sequence of bytecodes that access a local variable.

- 
dis.hascompare[¶](#dis.hascompare)
- Sequence of bytecodes of Boolean operations.

- 
dis.hasexc[¶](#dis.hasexc)
- Sequence of bytecodes that set an exception handler. Added in version 3.12.

- 
dis.hasjrel[¶](#dis.hasjrel)
- Sequence of bytecodes that have a relative jump target. Deprecated since version 3.13: All jumps are now relative. Use [`hasjump`](#dis.hasjump) .

- 
dis.hasjabs[¶](#dis.hasjabs)
- Sequence of bytecodes that have an absolute jump target. Deprecated since version 3.13: All jumps are now relative. This list is empty.
