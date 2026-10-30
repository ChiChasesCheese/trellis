# Claims ledger, group P3 (python: exceptions-context, numbers-floats, typing-dataclasses, imports-modules)

CPython references are at tag `v3.14.0` (`cpython@v3.14.0`). "ran" = executed on Python 3.14.8 (uv) in /tmp/uth_P3.
LC example code is copied by script from `sources/local/lc-in-decks.json` entries (the TikTok `source` paths in that
index are stale: the cards moved from `cards/a|b/` to `cards/p2|p3|p4/`; resolved by file name).

| card id | claim | source | how checked |
|---|---|---|---|
| uth-python-exceptions-context-1-unwind | Exception unwinds frame by frame looking for a handler; the traceback gets one entry per frame via PyTraceBack_Here | cpython@v3.14.0:InternalDocs/exception_handling.md (Handling Exceptions) | read |
| uth-python-exceptions-context-1-unwind | No handler anywhere: _PyEval_EvalFrameDefault returns NULL, interpreter prints traceback and exits | cpython@v3.14.0:InternalDocs/exception_handling.md | read |
| uth-python-exceptions-context-1-unwind | Default recursion limit is 1000 | cpython@v3.14.0:Include/internal/pycore_ceval.h:Py_DEFAULT_RECURSION_LIMIT; Doc/library/sys.rst getrecursionlimit/setrecursionlimit (RecursionError) | read |
| uth-python-exceptions-context-1-unwind | Example LC 98 recursive code copied from the Anki deck entry that sets sys.setrecursionlimit(20000) | sources/local/lc-in-decks.json -> LC 98 (LeetCode Tops Anki) | read; code copied by script |
| uth-python-exceptions-context-2-zero-cost | 3.11 'zero-cost' exceptions remove the cost of try when nothing is raised | cpython@v3.14.0:Doc/whatsnew/3.11.rst (Misc) | read |
| uth-python-exceptions-context-2-zero-cost | Before 3.11 entering try executed SETUP_FINALLY (pushes a block onto the block stack) | cpython@v3.10.0:Doc/library/dis.rst (SETUP_FINALLY) | read |
| uth-python-exceptions-context-2-zero-cost | SETUP_FINALLY/POP_BLOCK are pseudo-instructions replaced by the exception table co_exceptiontable; table consulted only when an exception occurs | cpython@v3.14.0:InternalDocs/exception_handling.md | read |
| uth-python-exceptions-context-2-zero-cost | Table entry = start, end, target, stack depth, lasti; sorted/searchable; binary search when table > MAX_LINEAR_SEARCH (40 bytes) then linear scan | cpython@v3.14.0:Python/ceval.c:get_exception_handler; InternalDocs/exception_handling.md (Format of the exception table) | read |
| uth-python-exceptions-context-2-zero-cost | No handler in this frame -> caller's frame is checked next | cpython@v3.14.0:InternalDocs/exception_handling.md | read |
| uth-python-exceptions-context-2-zero-cost | dis.dis of the f() example shows 'L1 to L2 -> L3 [0]' covering only the g() call instructions | Python 3.14.8 dis.dis(f) | ran |
| uth-python-exceptions-context-2-zero-cost | Raising costs more than returning (cost of raising increased) | cpython@v3.14.0:InternalDocs/exception_handling.md (intro) | read |
| uth-python-exceptions-context-3-finally | finally runs on normal exit, return/break/continue, and exception; exception is saved temporarily and re-raised after finally | cpython@v3.14.0:Doc/reference/compound_stmts.rst (finally clause) | read |
| uth-python-exceptions-context-3-finally | Exception raised inside finally gets the saved exception as __context__ | cpython@v3.14.0:Doc/reference/compound_stmts.rst (finally clause) | read |
| uth-python-exceptions-context-3-finally | return/break/continue in finally discards the saved exception; 3.14 emits SyntaxWarning (PEP 765); example f() returns 42 | cpython@v3.14.0:Doc/reference/compound_stmts.rst (versionchanged 3.14) | read; ran on 3.14.8 (warning printed, returns 42) |
| uth-python-exceptions-context-3-finally | os._exit exits 'without calling cleanup handlers, flushing stdio buffers' | cpython@v3.14.0:Doc/library/os.rst:_exit | read |
| uth-python-exceptions-context-3-finally | SIGKILL cannot be caught, blocked or ignored | man7.org signal(7) | read |
| uth-python-exceptions-context-3-finally | KeyboardInterrupt is an exception (BaseException subclass) raised on Ctrl-C, so unwinding runs finally | cpython@v3.14.0:Doc/library/exceptions.rst:KeyboardInterrupt | read |
| uth-python-exceptions-context-4-with | with: __enter__ result bound to target; __exit__ always called if __enter__ returned; truthy return suppresses the exception; args (type, value, tb) or three Nones | cpython@v3.14.0:Doc/reference/compound_stmts.rst (with statement); Doc/reference/datamodel.rst object.__exit__ | read |
| uth-python-exceptions-context-4-with | If __enter__ raises, __exit__ is not called (guarantee starts after __enter__ returns); verified by running | Doc/reference/compound_stmts.rst + local run | read; ran |
| uth-python-exceptions-context-4-with | __enter__/__exit__ are looked up on type(manager) | cpython@v3.14.0:Doc/reference/compound_stmts.rst (equivalent code: type(manager).__enter__) | read |
| uth-python-exceptions-context-4-with | contextmanager: __exit__ throws the body's exception into the generator at the yield; code after yield skipped without try/finally | cpython@v3.14.0:Lib/contextlib.py:_GeneratorContextManager.__exit__ (self.gen.throw) | read; ran (no try/finally -> 'cleanup A' not printed; with -> 'cleanup B' printed) |
| uth-python-exceptions-context-5-eafp-stopiteration | EAFP / LBYL definitions and the LBYL race-condition example | cpython@v3.14.0:Doc/glossary.rst (EAFP, LBYL) | read |
| uth-python-exceptions-context-5-eafp-stopiteration | iterator.__next__ raises StopIteration when no more items; must keep raising afterwards | cpython@v3.14.0:Doc/library/stdtypes.rst (iterator.__next__) | read |
| uth-python-exceptions-context-5-eafp-stopiteration | FOR_ITER catches StopIteration and ends the loop; C iterators returning NULL without an error also end it | cpython@v3.14.0:Python/bytecodes.c:_FOR_ITER | read |
| uth-python-exceptions-context-5-eafp-stopiteration | list iterator returns NULL (no exception) when exhausted; slot_tp_iternext calls the Python __next__ so a Python iterator raises StopIteration | cpython@v3.14.0:Objects/listobject.c:listiter_next; Objects/typeobject.c:slot_tp_iternext | read |
| uth-python-exceptions-context-5-eafp-stopiteration | StopIteration leaking from a generator becomes RuntimeError since 3.7 (PEP 479) | cpython@v3.14.0:Doc/whatsnew/3.7.rst (PEP 479) | read |
| uth-python-exceptions-context-5-eafp-stopiteration | LC 341 code (raises StopIteration in next) copied from the Anki deck entry | sources/local/lc-in-decks.json -> LC 341 | read; code copied by script |
| uth-python-numbers-floats-1-bigint | int = array of 30-bit digits stored in uint32; value = sum digit[i]*2**(30*i); at least one digit allocated | cpython@v3.14.0:Include/cpython/longintrepr.h (PyLong_SHIFT 30, typedef uint32_t digit) | read |
| uth-python-numbers-floats-1-bigint | sys.int_info: bits_per_digit=30, sizeof_digit=4 | Python 3.14.8 sys.int_info | ran |
| uth-python-numbers-floats-1-bigint | getsizeof: 0..2**30-1 -> 28, 2**30 -> 32, 2**60 -> 36, 2**100 -> 40 (24 header + 4 per digit) | Python 3.14.8 sys.getsizeof | ran |
| uth-python-numbers-floats-1-bigint | 30-bit digit chosen so product of two digits fits twodigits (uint64) | cpython@v3.14.0:Include/cpython/longintrepr.h (comment on digit/twodigits) | read |
| uth-python-numbers-floats-1-bigint | 2**65 = digits [0, 0, 32] (66 bits -> 3 digits) | arithmetic: 65 = 2*30 + 5, 2**5 = 32 | ran (python arithmetic) |
| uth-python-numbers-floats-1-bigint | LC 7 code copied from the Anki deck entry | sources/local/lc-in-decks.json -> LC 7 | read; code copied by script |
| uth-python-numbers-floats-2-bigint-cost | Schoolbook multiplication unless both operands have more than KARATSUBA_CUTOFF=70 digits | cpython@v3.14.0:Objects/longobject.c:KARATSUBA_CUTOFF | read |
| uth-python-numbers-floats-2-bigint-cost | 70 digits * 30 bits = 2100 bits ~ 632 decimal digits | arithmetic 2100*log10(2) | ran |
| uth-python-numbers-floats-2-bigint-cost | Karatsuba: k=(ah+al)*(bh+bl) gives the product with 3 half-size multiplications | cpython@v3.14.0:Objects/longobject.c:k_mul (comment, Knuth 4.3.3) | read |
| uth-python-numbers-floats-2-bigint-cost | No linear algorithm for base-10 conversion; linear for bases 2,4,8,16,32, hex/oct/bin, to_bytes | cpython@v3.14.0:Doc/library/stdtypes.rst (Integer string conversion length limitation) | read |
| uth-python-numbers-floats-2-bigint-cost | Default limit 4300 digits, min configurable 640, CVE-2020-10735, since 3.11, set_int_max_str_digits | cpython@v3.14.0:Doc/library/stdtypes.rst; sys.int_info.default_max_str_digits | read; ran (str(10**5000) -> ValueError, len(hex(10**5000))=4155) |
| uth-python-numbers-floats-2-bigint-cost | _pylong used for big int<->str and divmod since 3.12 (file absent in 3.11.9, present in 3.12.0) | cpython@v3.11.9 / v3.12.0:Lib/_pylong.py, Objects/longobject.c | read (HTTP 404 vs 200; grep) |
| uth-python-numbers-floats-3-float | binary64 layout: sign bit 63, exponent bits 62-52 (11), significand bits 51-0 (52) | OpenJDK 21 Double.doubleToLongBits javadoc | read |
| uth-python-numbers-floats-3-float | 53 bits of precision; 0.1 = 3602879701896397 / 2**55 = 0.1000000000000000055511151231257827021181583404541015625 | cpython@v3.14.0:Doc/tutorial/floatingpoint.rst | read; ran |
| uth-python-numbers-floats-3-float | 0.1+0.2 == 0.30000000000000004; 0.1+0.2 == 0.3 is False; float(2**53)+1 == float(2**53) is True | Python 3.14.8 | ran |
| uth-python-numbers-floats-3-float | math.isclose default rel_tol=1e-09 | cpython@v3.14.0:Doc/library/math.rst:isclose | read |
| uth-python-numbers-floats-3-float | 0.1 in binary is 0.000110011001100... (0x1.999999999999ap-4) | Python 3.14.8 (0.1).hex() | ran |
| uth-python-numbers-floats-3-float | LC 2469 judge tolerance 10^-5 and code copied from Anki deck entry | sources/local/lc-in-decks.json -> LC 2469 | read; code copied by script |
| uth-python-numbers-floats-4-decimal-fraction | Decimal default precision 28, rounding ROUND_HALF_EVEN; exact decimal arithmetic; hardware vs software | cpython@v3.14.0:Doc/library/decimal.rst (intro, Context) | read; ran (getcontext().prec == 28) |
| uth-python-numbers-floats-4-decimal-fraction | C implementation uses libmpdec | cpython@v3.14.0:Doc/library/decimal.rst (FAQ: Is the CPython implementation fast for large numbers?) | read |
| uth-python-numbers-floats-4-decimal-fraction | Fraction reduces by math.gcd at construction | cpython@v3.14.0:Lib/fractions.py:Fraction.__new__ (g = math.gcd(numerator, denominator)) | read |
| uth-python-numbers-floats-4-decimal-fraction | Fraction('0.1')+Fraction('0.2') == 3/10; Fraction(1,3)*3 == 1; Decimal(0.1) shows the binary value; Decimal('0.1')+Decimal('0.2') == 0.3 | Python 3.14.8 | ran |
| uth-python-numbers-floats-5-floordiv | // is floor division; % takes the sign of the second operand; x == (x//y)*y + x%y | cpython@v3.14.0:Doc/reference/expressions.rst (binary arithmetic operations) | read |
| uth-python-numbers-floats-5-floordiv | CPython: truncating divrem, then if mod and divisor have opposite signs: mod += w, div -= 1 | cpython@v3.14.0:Objects/longobject.c:l_divmod | read |
| uth-python-numbers-floats-5-floordiv | -7//2=-4, -7%3=2, 7%-3=-2, int(-7/2)=-3, math.fmod(-7,3)=-1.0 | Python 3.14.8 | ran |
| uth-python-numbers-floats-5-floordiv | C++ integer division truncates toward zero; table -5/3=-1, -5%3=-2 | cplusplus/draft:source/expressions.tex (expr.mul) | read |
| uth-python-numbers-floats-5-floordiv | Java integer division rounds toward 0; remainder negative only if dividend negative | JLS 21 sec. 15.17.2, 15.17.3 | read |
| uth-python-numbers-floats-5-floordiv | Go integer division truncated towards zero | go.dev/ref/spec (Arithmetic operators) | read |
| uth-python-numbers-floats-5-floordiv | Rust integer division rounds towards zero; remainder has the sign of the dividend | rust-lang/reference:src/expressions/operator-expr.md | read |
| uth-python-numbers-floats-5-floordiv | math.fmod returns result with the sign of x (C-style) | cpython@v3.14.0:Doc/library/math.rst:fmod | read |
| uth-python-numbers-floats-5-floordiv | LC 150 code (int(a / b)) copied from Anki deck entry | sources/local/lc-in-decks.json -> LC 150 | read; code copied by script |
| uth-python-typing-dataclasses-1-annotation | The runtime does not enforce function and variable type annotations | cpython@v3.14.0:Doc/library/typing.rst (note) | read |
| uth-python-typing-dataclasses-1-annotation | f('not an int') runs; x: int = 'hello' runs; function __annotations__ = {'x': int, ...} | Python 3.14.8 | ran |
| uth-python-typing-dataclasses-1-annotation | 3.14: annotations lazily evaluated via annotate functions (PEP 649/749); forward refs need no quotes | cpython@v3.14.0:Doc/whatsnew/3.14.rst (Deferred evaluation of annotations) | read |
| uth-python-typing-dataclasses-1-annotation | class body 'm: Undefined' ok; reading __annotations__ raises NameError; FORWARDREF/STRING formats available | Python 3.14.8 annotationlib | ran |
| uth-python-typing-dataclasses-1-annotation | Annotations of local variables in function scope are never evaluated or stored | cpython@v3.14.0:Doc/reference/simple_stmts.rst (Annotated assignment statements) | read |
| uth-python-typing-dataclasses-1-annotation | Before 3.14 annotations were evaluated at definition time (forward references needed quotes) | cpython@v3.14.0:Doc/whatsnew/3.14.rst (It is no longer necessary to enclose annotations in strings) | read |
| uth-python-typing-dataclasses-1-annotation | LC 98 iterative code with quoted 'TreeNode | None' copied from Anki deck entry | sources/local/lc-in-decks.json -> LC 98 | read; code copied by script |
| uth-python-typing-dataclasses-2-generic-alias | list[int] is a types.GenericAlias created by subscripting the class (3.9); __origin__/__args__; no checking: list[str]([1,2,3]) -> [1,2,3] | cpython@v3.14.0:Doc/library/stdtypes.rst (Generic Alias Type) | read; ran |
| uth-python-typing-dataclasses-2-generic-alias | isinstance(x, list[int]) -> TypeError 'argument 2 cannot be a parameterized generic'; isinstance('', int | str) ok | cpython@v3.14.0:Doc/library/stdtypes.rst (Generic Alias, Union Type) | read; ran |
| uth-python-typing-dataclasses-2-generic-alias | X | Y available from 3.10; in 3.14 type(int | str) is typing.Union; __or__ on type objects | cpython@v3.14.0:Doc/library/stdtypes.rst (Union Type) | read; ran (type.__or__ slot wrapper) |
| uth-python-typing-dataclasses-2-generic-alias | int | 'Foo' fails at runtime for forward references | cpython@v3.14.0:Doc/library/stdtypes.rst (Union Type note) | read |
| uth-python-typing-dataclasses-2-generic-alias | list.__class_getitem__(int) returns list[int] | Python 3.14.8 | ran |
| uth-python-typing-dataclasses-3-dataclass-codegen | dataclass builds source text, exec()s it in __create_fn__, assigns functions to the class | cpython@v3.14.0:Lib/dataclasses.py:_FuncBuilder.add_fns_to_class | read |
| uth-python-typing-dataclasses-3-dataclass-codegen | __eq__ requires other.__class__ is self.__class__ else NotImplemented, compares fields one by one | cpython@v3.14.0:Lib/dataclasses.py:_process_class (eq) | read; ran (P(1) == (1,0) is False) |
| uth-python-typing-dataclasses-3-dataclass-codegen | Fields come from annotations (get_annotations FORWARDREF); un-annotated z = 1 is not a field | cpython@v3.14.0:Lib/dataclasses.py:_process_class | read; ran (fields() == ['x']) |
| uth-python-typing-dataclasses-3-dataclass-codegen | __match_args__ since 3.10; __repr__ form P(x=1, y=0) | cpython@v3.14.0:Doc/library/dataclasses.rst (match_args versionadded 3.10) | read; ran |
| uth-python-typing-dataclasses-4-frozen-order-hash | Hash rules: eq & frozen -> generated; eq & not frozen -> None; eq=False -> inherited (id-based for object) | cpython@v3.14.0:Doc/library/dataclasses.rst (unsafe_hash rules); Lib/dataclasses.py:_hash_action | read; ran |
| uth-python-typing-dataclasses-4-frozen-order-hash | frozen implemented by generated __setattr__/__delattr__ raising FrozenInstanceError | cpython@v3.14.0:Lib/dataclasses.py:_frozen_get_del_attr | read; ran |
| uth-python-typing-dataclasses-4-frozen-order-hash | order=True: __lt__ etc compare tuples of fields, same class required | cpython@v3.14.0:Doc/library/dataclasses.rst (order); Lib/dataclasses.py (order) | read; ran (TypeError vs tuple) |
| uth-python-typing-dataclasses-4-frozen-order-hash | LC 23 heap tuple (val, i, node) code copied from Anki deck entry | sources/local/lc-in-decks.json -> LC 23 | read; code copied by script |
| uth-python-typing-dataclasses-5-mutable-default | Mutable default check uses default.__class__.__hash__ is None; error text 'mutable default <class 'list'> for field xs is not allowed: use default_factory' | cpython@v3.14.0:Lib/dataclasses.py:_get_field | read; ran |
| uth-python-typing-dataclasses-5-mutable-default | default_factory called when a default is needed; W().xs is W().xs is False | cpython@v3.14.0:Doc/library/dataclasses.rst (field, Mutable default values) | read; ran |
| uth-python-typing-dataclasses-5-mutable-default | Non-default field after default field -> TypeError; kw_only (3.10) fields skip the check | cpython@v3.14.0:Lib/dataclasses.py:_init_fn | read |
| uth-python-typing-dataclasses-5-mutable-default | slots=True since 3.10: __slots__ generated, no __dict__ | cpython@v3.14.0:Doc/library/dataclasses.rst (slots versionadded 3.10) | read; ran (hasattr(S(1), '__dict__') False) |
| uth-python-typing-dataclasses-5-mutable-default | LC 49 code (defaultdict(list)) copied from TikTok whole-answer card | sources/local/lc-in-decks.json -> LC 49 | read; code copied by script |
| uth-python-imports-modules-1-import-once | import checks sys.modules first; missing -> find, create module, then exec | cpython@v3.14.0:Doc/reference/import.rst (The module cache); Lib/importlib/_bootstrap.py:_load_unlocked | read |
| uth-python-imports-modules-1-import-once | Module is put in sys.modules BEFORE exec_module; on failure it is deleted from sys.modules | cpython@v3.14.0:Lib/importlib/_bootstrap.py:_load_unlocked | read |
| uth-python-imports-modules-1-import-once | Each module imported once per session | cpython@v3.14.0:Doc/tutorial/modules.rst | read |
| uth-python-imports-modules-1-import-once | pyc cached as __pycache__/name.cpython-314.pyc; stale check by source mtime and size; script run from command line never cached | cpython@v3.14.0:Doc/tutorial/modules.rst (Compiled Python files); Lib/importlib/_bootstrap_external.py:_validate_timestamp_pyc | read; ran (json.__cached__ path) |
| uth-python-imports-modules-1-import-once | sys.modules is a dict | Python 3.14.8 type(sys.modules) | ran |
| uth-python-imports-modules-2-module-object | Module is a types.ModuleType with its own __dict__; import binds the name to the sys.modules object | cpython@v3.14.0:Doc/reference/import.rst; Doc/reference/datamodel.rst | read; ran |
| uth-python-imports-modules-2-module-object | from m import x copies the binding: cfg.level = 2 leaves earlier 'level' at 1 | Python 3.14.8 | ran (prints '1 2') |
| uth-python-imports-modules-2-module-object | del sys.modules[k] then import gives a new module object; importlib.reload reuses the same object | cpython@v3.14.0:Doc/reference/import.rst (The module cache) | read; ran |
| uth-python-imports-modules-3-search-path | sys.meta_path = BuiltinImporter, FrozenImporter, PathFinder | Python 3.14.8 sys.meta_path | ran |
| uth-python-imports-modules-3-search-path | Built-in module sys is not shadowed by a local sys.py; local random.py shadows stdlib random | Python 3.14.8 (script dir with sys.py and random.py) | ran |
| uth-python-imports-modules-3-search-path | Frozen modules = core startup modules (3.11+); os/site/codecs/abc/io are frozen, random/json are not | cpython@v3.14.0:Doc/whatsnew/3.11.rst (Frozen imports) | read; ran (_imp.is_frozen) |
| uth-python-imports-modules-3-search-path | sys.path[0] = script dir (python script.py) or cwd (python -m); -P / PYTHONSAFEPATH (3.11) removes it | cpython@v3.14.0:Doc/library/sys.rst:path; Doc/using/cmdline.rst:-P | read; ran |
| uth-python-imports-modules-3-search-path | 3.13 error message 'consider renaming ... same name as the standard library module' | cpython@v3.14.0:Doc/whatsnew/3.13.rst (improved error messages) | read; ran (3.14) |
| uth-python-imports-modules-4-circular | from a import fa: getattr on module, fallback sys.modules['a.fa'], else ImportError 'cannot import name ... from partially initialized module ... (most likely due to a circular import)' | cpython@v3.14.0:Python/ceval.c:import_from | read; ran |
| uth-python-imports-modules-4-circular | import a then import b order changes which name fails (fa vs fb); import c/d style does not fail until attribute use | Python 3.14.8 (a.py/b.py, c.py/d.py demo) | ran |
| uth-python-imports-modules-5-main-guard | __name__ is the module name when imported and '__main__' for the top-level script / -m module | cpython@v3.14.0:Doc/library/__main__.rst | read; ran |
| uth-python-imports-modules-5-main-guard | Running m.py that imports m loads the file twice: prints 'run as __main__' then 'run as m' | Python 3.14.8 (python m.py) | ran |
| uth-python-imports-modules-5-main-guard | python -m pkg runs pkg/__main__.py | cpython@v3.14.0:Doc/library/__main__.rst (__main__.py in Python Packages) | read |
