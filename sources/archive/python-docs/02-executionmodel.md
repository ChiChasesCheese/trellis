---
title: 4. Execution model
corpus: python-docs
section: 02-executionmodel
level: 1
locator: https://docs.python.org/3/reference/executionmodel.html
license: free-online
fetched: '2026-09-21'
---

# 4. Execution model[¶](#execution-model)

## 4.1. Structure of a program[¶](#structure-of-a-program)

A Python program is constructed from code blocks.
A *block* is a piece of Python program text that is executed as a unit.
The following are blocks: a module, a function body, and a class definition.
Each command typed interactively is a block.  A script file (a file given as
standard input to the interpreter or specified as a command line argument to the
interpreter) is a code block.  A script command (a command specified on the
interpreter command line with the [`-c`](../using/cmdline.html#cmdoption-c) option) is a code block.
A module run as a top level script (as module `__main__`) from the command
line using a [`-m`](../using/cmdline.html#cmdoption-m) argument is also a code block. The string
argument passed to the built-in functions [`eval()`](../builtins/functions.html#eval) and [`exec()`](../builtins/functions.html#exec) is a
code block.

A code block is executed in an *execution frame*.  A frame contains some
administrative information (used for debugging) and determines where and how
execution continues after the code block’s execution has completed.

## 4.2. Naming and binding[¶](#naming-and-binding)

### 4.2.1. Binding of names[¶](#binding-of-names)

*Names* refer to objects.  Names are introduced by name binding operations.

The following constructs bind names:

- formal parameters to functions,
- class definitions,
- function definitions,
- assignment expressions,
- [targets](simple_stmts.html#assignment) that are identifiers if occurring in
an assignment:
- [`import`](simple_stmts.html#import) statements.
- [`type`](simple_stmts.html#type) statements.
- [type parameter lists](compound_stmts.html#type-params) .

The `import` statement of the form `from ... import *` binds all
names defined in the imported module, except those beginning with an underscore.
This form may only be used at the module level.

A target occurring in a [`del`](simple_stmts.html#del) statement is also considered bound for
this purpose (though the actual semantics are to unbind the name).

Each assignment or import statement occurs within a block defined by a class or function definition or at the module level (the top-level code block).

If a name is bound in a block, it is a local variable of that block, unless
declared as [`nonlocal`](simple_stmts.html#nonlocal) or [`global`](simple_stmts.html#global).  If a name is bound at
the module level, it is a global variable.  (The variables of the module code
block are local and global.)  If a variable is used in a code block but not
defined there, it is a [free variable](../glossary.html#term-free-variable).

Each occurrence of a name in the program text refers to the *binding* of
that name established by the following name resolution rules.

### 4.2.2. Resolution of names[¶](#resolution-of-names)

A *scope* defines the visibility of a name within a block.  If a local
variable is defined in a block, its scope includes that block.  If the
definition occurs in a function block, the scope extends to any blocks contained
within the defining one, unless a contained block introduces a different binding
for the name.

When a name is used in a code block, it is resolved using the nearest enclosing
scope.  The set of all such scopes visible to a code block is called the block’s
*environment*.

When a name is not found at all, a [`NameError`](../builtins/exceptions.html#NameError) exception is raised.
If the current scope is a function scope, and the name refers to a local
variable that has not yet been bound to a value at the point where the name is
used, an [`UnboundLocalError`](../builtins/exceptions.html#UnboundLocalError) exception is raised.
`UnboundLocalError` is a subclass of `NameError`.

If a name binding operation occurs anywhere within a code block, all uses of the
name within the block are treated as references to the current block.  This can
lead to errors when a name is used within a block before it is bound.  This rule
is subtle.  Python lacks declarations and allows name binding operations to
occur anywhere within a code block.  The local variables of a code block can be
determined by scanning the entire text of the block for name binding operations.
See [the FAQ entry on UnboundLocalError](../faq/programming.html#faq-unboundlocalerror)
for examples.

If the [`global`](simple_stmts.html#global) statement occurs within a block, all uses of the names
specified in the statement refer to the bindings of those names in the top-level
namespace.  Names are resolved in the top-level namespace by searching the
global namespace, i.e. the namespace of the module containing the code block,
and the builtins namespace, the namespace of the module [`builtins`](../library/builtins.html#module-builtins).  The
global namespace is searched first.  If the names are not found there, the
builtins namespace is searched next. If the names are also not found in the
builtins namespace, new variables are created in the global namespace.
The global statement must precede all uses of the listed names.

The [`global`](simple_stmts.html#global) statement has the same scope as a name binding operation
in the same block.  If the nearest enclosing scope for a free variable contains
a global statement, the free variable is treated as a global.

The [`nonlocal`](simple_stmts.html#nonlocal) statement causes corresponding names to refer
to previously bound variables in the nearest enclosing function scope.
[`SyntaxError`](../builtins/exceptions.html#SyntaxError) is raised at compile time if the given name does not
exist in any enclosing function scope. [Type parameters](compound_stmts.html#type-params)
cannot be rebound with the `nonlocal` statement.

The namespace for a module is automatically created the first time a module is
imported.  The main module for a script is always called [`__main__`](../library/__main__.html#module-__main__).

Class definition blocks and arguments to [`exec()`](../builtins/functions.html#exec) and [`eval()`](../builtins/functions.html#eval) are
special in the context of name resolution.
A class definition is an executable statement that may use and define names.
These references follow the normal rules for name resolution with an exception
that unbound local variables are looked up in the global namespace.
The namespace of the class definition becomes the attribute dictionary of
the class. The scope of names defined in a class block is limited to the
class block; it does not extend to the code blocks of methods. This includes
comprehensions and generator expressions, but it does not include
[annotation scopes](#annotation-scopes),
which have access to their enclosing class scopes.
This means that the following will fail:

```
class A:
    a = 42
    b = list(a + i for i in range(10))
```
However, the following will succeed:

```
class A:
    type Alias = Nested
    class Nested: pass
print(A.Alias.__value__)  # <type 'A.Nested'>
```
### 4.2.3. Annotation scopes[¶](#annotation-scopes)

[Annotations](../glossary.html#term-annotation), [type parameter lists](compound_stmts.html#type-params)
and [`type`](simple_stmts.html#type) statements
introduce *annotation scopes*, which behave mostly like function scopes,
but with some exceptions discussed below.

Annotation scopes are used in the following contexts:

- [Function annotations](../glossary.html#term-function-annotation) .
- [Variable annotations](../glossary.html#term-variable-annotation) .
- Type parameter lists for [generic type aliases](compound_stmts.html#generic-type-aliases) .
- Type parameter lists for [generic functions](compound_stmts.html#generic-functions) .
A generic function’s annotations are
executed within the annotation scope, but its defaults and decorators are not.
- Type parameter lists for [generic classes](compound_stmts.html#generic-classes) .
A generic class’s base classes and
keyword arguments are executed within the annotation scope, but its decorators are not.
- The bounds, constraints, and default values for type parameters ( [lazily evaluated](#lazy-evaluation) ).
- The value of type aliases ( [lazily evaluated](#lazy-evaluation) ).

Annotation scopes differ from function scopes in the following ways:

- Annotation scopes have access to their enclosing class namespace. If an annotation scope is immediately within a class scope, or within another annotation scope that is immediately within a class scope, the code in the annotation scope can use names defined in the class scope as if it were executed directly within the class body. This contrasts with regular functions defined within classes, which cannot access names defined in the class scope.
- Expressions in annotation scopes cannot contain [`yield`](simple_stmts.html#yield) ,`yield from` ,[`await`](expressions.html#await) , or[`:=`](expressions.html#grammar-token-python-grammar-assignment_expression) expressions. (These expressions are allowed in other scopes contained within the
annotation scope.)
- Names defined in annotation scopes cannot be rebound with [`nonlocal`](simple_stmts.html#nonlocal) statements in inner scopes. This includes only type parameters, as no other
syntactic elements that can appear within annotation scopes can introduce new names.
- While annotation scopes have an internal name, that name is not reflected in the [qualified name](../glossary.html#term-qualified-name) of objects defined within the scope.
Instead, the[`__qualname__`](../builtins/stdtypes.html#definition.__qualname__) of such objects is as if the object were defined in the enclosing scope.

Added in version 3.12: Annotation scopes were introduced in Python 3.12 as part of [**PEP 695**](https://peps.python.org/pep-0695/).

Changed in version 3.13: Annotation scopes are also used for type parameter defaults, as
introduced by [**PEP 696**](https://peps.python.org/pep-0696/).

### 4.2.4. Lazy evaluation[¶](#lazy-evaluation)

Most annotation scopes are *lazily evaluated*. This includes annotations,
the values of type aliases created through the [`type`](simple_stmts.html#type) statement, and
the bounds, constraints, and default values of type
variables created through the [type parameter syntax](compound_stmts.html#type-params).
This means that they are not evaluated when the type alias or type variable is
created, or when the object carrying annotations is created. Instead, they
are only evaluated when necessary, for example when the `__value__`
attribute on a type alias is accessed.

Example:

```
>>> type Alias = 1/0
>>> Alias.__value__
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
>>> def func[T: 1/0](): pass
>>> T = func.__type_params__[0]
>>> T.__bound__
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```
Here the exception is raised only when the `__value__` attribute
of the type alias or the `__bound__` attribute of the type variable
is accessed.

This behavior is primarily useful for references to types that have not yet been defined when the type alias or type variable is created. For example, lazy evaluation enables creation of mutually recursive type aliases:

```
from typing import Literal
type SimpleExpr = int | Parenthesized
type Parenthesized = tuple[Literal["("], Expr, Literal[")"]]
type Expr = SimpleExpr | tuple[SimpleExpr, Literal["+", "-"], Expr]
```
Lazily evaluated values are evaluated in [annotation scope](#annotation-scopes),
which means that names that appear inside the lazily evaluated value are looked up
as if they were used in the immediately enclosing scope.

Added in version 3.12.

### 4.2.5. Builtins and restricted execution[¶](#builtins-and-restricted-execution)

**CPython implementation detail:** Users should not touch `__builtins__`; it is strictly an implementation
detail.  Users wanting to override values in the builtins namespace should
[`import`](simple_stmts.html#import) the [`builtins`](../library/builtins.html#module-builtins) module and modify its
attributes appropriately.

The builtins namespace associated with the execution of a code block
is actually found by looking up the name `__builtins__` in its
global namespace; this should be a dictionary or a module (in the
latter case the module’s dictionary is used).  By default, when in the
[`__main__`](../library/__main__.html#module-__main__) module, `__builtins__` is the built-in module
[`builtins`](../library/builtins.html#module-builtins); when in any other module, `__builtins__` is an
alias for the dictionary of the `builtins` module itself.

### 4.2.6. Interaction with dynamic features[¶](#interaction-with-dynamic-features)

Name resolution of free variables occurs at runtime, not at compile time. This means that the following code will print 42:

```
i = 10
def f():
    print(i)
i = 42
f()
```
The [`eval()`](../builtins/functions.html#eval) and [`exec()`](../builtins/functions.html#exec) functions do not have access to the full
environment for resolving names.  Names may be resolved in the local and global
namespaces of the caller.  Free variables are not resolved in the nearest
enclosing namespace, but in the global namespace.  [\[1\]](#id5) The `exec()` and
`eval()` functions have optional arguments to override the global and local
namespace.  If only one namespace is specified, it is used for both.

## 4.3. Exceptions[¶](#exceptions)

Exceptions are a means of breaking out of the normal flow of control of a code
block in order to handle errors or other exceptional conditions.  An exception
is *raised* at the point where the error is detected; it may be *handled* by the
surrounding code block or by any code block that directly or indirectly invoked
the code block where the error occurred.

The Python interpreter raises an exception when it detects a run-time error
(such as division by zero).  A Python program can also explicitly raise an
exception with the [`raise`](simple_stmts.html#raise) statement. Exception handlers are specified
with the [`try`](compound_stmts.html#try) … [`except`](compound_stmts.html#except) statement.  The [`finally`](compound_stmts.html#finally)
clause of such a statement can be used to specify cleanup code which does not
handle the exception, but is executed whether an exception occurred or not in
the preceding code.

Python uses the “termination” model of error handling: an exception handler can find out what happened and continue execution at an outer level, but it cannot repair the cause of the error and retry the failing operation (except by re-entering the offending piece of code from the top).

When an exception is not handled at all, the interpreter terminates execution of
the program, or returns to its interactive main loop.  In either case, it prints
a stack traceback, except when the exception is [`SystemExit`](../builtins/exceptions.html#SystemExit).

Exceptions are identified by class instances.  The [`except`](compound_stmts.html#except) clause is
selected depending on the class of the instance: it must reference the class of
the instance or a [non-virtual base class](../glossary.html#term-abstract-base-class) thereof.
The instance can be received by the handler and can carry additional information
about the exceptional condition.

Note

Exception messages are not part of the Python API. Their contents may change from one version of Python to the next without warning and should not be relied on by code which will run under multiple versions of the interpreter.

See also the description of the [`try`](compound_stmts.html#try) statement in section [The try statement](compound_stmts.html#try)
and [`raise`](simple_stmts.html#raise) statement in section [The raise statement](simple_stmts.html#raise).

## 4.4. Runtime Components[¶](#runtime-components)

### 4.4.1. General Computing Model[¶](#general-computing-model)

Python’s execution model does not operate in a vacuum. It runs on a host machine and through that host’s runtime environment, including its operating system (OS), if there is one. When a program runs, the conceptual layers of how it runs on the host look something like this:

**host machine****process** (global resources)**thread** (runs machine code)

Each process represents a program running on the host. Think of each process itself as the data part of its program. Think of the process’ threads as the execution part of the program. This distinction will be important to understand the conceptual Python runtime.

The process, as the data part, is the execution context in which the program runs. It mostly consists of the set of resources assigned to the program by the host, including memory, signals, file handles, sockets, and environment variables.

Processes are isolated and independent from one another. (The same is true for hosts.) The host manages the process’ access to its assigned resources, in addition to coordinating between processes.

Each thread represents the actual execution of the program’s machine code, running relative to the resources assigned to the program’s process. It’s strictly up to the host how and when that execution takes place.

From the point of view of Python, a program always starts with exactly one thread. However, the program may grow to run in multiple simultaneous threads. Not all hosts support multiple threads per process, but most do. Unlike processes, threads in a process are not isolated and independent from one another. Specifically, all threads in a process share all of the process’ resources.

The fundamental point of threads is that each one does *run*
independently, at the same time as the others.  That may be only
conceptually at the same time (“concurrently”) or physically
(“in parallel”).  Either way, the threads effectively run
at a non-synchronized rate.

Note

That non-synchronized rate means none of the process’ memory is
guaranteed to stay consistent for the code running in any given
thread.  Thus multi-threaded programs must take care to coordinate
access to intentionally shared resources.  Likewise, they must take
care to be absolutely diligent about not accessing any *other*
resources in multiple threads; otherwise two threads running at the
same time might accidentally interfere with each other’s use of some
shared data.  All this is true for both Python programs and the
Python runtime.

The cost of this broad, unstructured requirement is the tradeoff for the kind of raw concurrency that threads provide. The alternative to the required discipline generally means dealing with non-deterministic bugs and data corruption.

### 4.4.2. Python Runtime Model[¶](#python-runtime-model)

The same conceptual layers apply to each Python program, with some extra data layers specific to Python:

**host machine****process** (global resources)Python global runtime (*state*)Python interpreter (*state*)**thread** (runs Python bytecode and “C-API”)Python thread*state*

At the conceptual level: when a Python program starts, it looks exactly like that diagram, with one of each. The runtime may grow to include multiple interpreters, and each interpreter may grow to include multiple thread states.

Note

A Python implementation won’t necessarily implement the runtime
layers distinctly or even concretely.  The only exception is places
where distinct layers are directly specified or exposed to users,
like through the [`threading`](../library/threading.html#module-threading) module.

Note

The initial interpreter is typically called the “main” interpreter. Some Python implementations, like CPython, assign special roles to the main interpreter.

Likewise, the host thread where the runtime was initialized is known as the “main” thread. It may be different from the process’ initial thread, though they are often the same. In some cases “main thread” may be even more specific and refer to the initial thread state. A Python runtime might assign specific responsibilities to the main thread, such as handling signals.

As a whole, the Python runtime consists of the global runtime state, interpreters, and thread states. The runtime ensures all that state stays consistent over its lifetime, particularly when used with multiple host threads.

The global runtime, at the conceptual level, is just a set of interpreters. While those interpreters are otherwise isolated and independent from one another, they may share some data or other resources. The runtime is responsible for managing these global resources safely. The actual nature and management of these resources is implementation-specific. Ultimately, the external utility of the global runtime is limited to managing interpreters.

In contrast, an “interpreter” is conceptually what we would normally think of as the (full-featured) “Python runtime”. When machine code executing in a host thread interacts with the Python runtime, it calls into Python in the context of a specific interpreter.

Note

The term “interpreter” here is not the same as the “bytecode interpreter”, which is what regularly runs in threads, executing compiled Python code.

In an ideal world, “Python runtime” would refer to what we currently
call “interpreter”.  However, it’s been called “interpreter” at least
since introduced in 1997 ([CPython:a027efa5b](https://github.com/python/cpython/commit/a027efa5b)).

Each interpreter completely encapsulates all of the non-process-global,
non-thread-specific state needed for the Python runtime to work.
Notably, the interpreter’s state persists between uses.  It includes
fundamental data like [`sys.modules`](../library/sys.html#sys.modules).  The runtime ensures
multiple threads using the same interpreter will safely
share it between them.

A Python implementation may support using multiple interpreters at the
same time in the same process.  They are independent and isolated from
one another.  For example, each interpreter has its own
[`sys.modules`](../library/sys.html#sys.modules).

For thread-specific runtime state, each interpreter has a set of thread states, which it manages, in the same way the global runtime contains a set of interpreters. It can have thread states for as many host threads as it needs. It may even have multiple thread states for the same host thread, though that isn’t as common.

Each thread state, conceptually, has all the thread-specific runtime data an interpreter needs to operate in one host thread. The thread state includes the current raised exception and the thread’s Python call stack. It may include other thread-specific resources.

Note

The term “Python thread” can sometimes refer to a thread state, but
normally it means a thread created using the [`threading`](../library/threading.html#module-threading) module.

Each thread state, over its lifetime, is always tied to exactly one interpreter and exactly one host thread. It will only ever be used in that thread and with that interpreter.

Multiple thread states may be tied to the same host thread, whether for different interpreters or even the same interpreter. However, for any given host thread, only one of the thread states tied to it can be used by the thread at a time.

Thread states are isolated and independent from one another and don’t share any data, except for possibly sharing an interpreter and objects or other resources belonging to that interpreter.

Once a program is running, new Python threads can be created using the
[`threading`](../library/threading.html#module-threading) module (on platforms and Python implementations that
support threads).  Additional processes can be created using the
[`os`](../library/os.html#module-os), [`subprocess`](../library/subprocess.html#module-subprocess), and [`multiprocessing`](../library/multiprocessing.html#module-multiprocessing) modules.
Interpreters can be created and used with the
[`interpreters`](../library/concurrent.interpreters.html#module-concurrent.interpreters) module.  Coroutines (async) can
be run using [`asyncio`](../library/asyncio.html#module-asyncio) in each interpreter, typically only
in a single thread (often the main thread).

Footnotes
