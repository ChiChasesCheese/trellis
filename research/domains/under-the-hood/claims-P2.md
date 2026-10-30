# Claims ledger — group P2

Source tree: cpython@v3.14.8 (cloned, read in this session); runs on python3.14 / python3.14t 3.14.8 (macOS aarch64).

| card id | claim | source | how checked |
|---|---|---|---|
| uth-python-classes-mro-1-class-is-object | class statement runs body into a namespace then calls metaclass(name, bases, namespace) | cpython@v3.14.8:Doc/reference/datamodel.rst "Creating the class object" | read |
| uth-python-classes-mro-1-class-is-object | type(d) is Dog, type(Dog) is type, type(type) is type, type(int) is type | python3.14 run | ran |
| uth-python-classes-mro-1-class-is-object | type("T",(A,),{...}) builds a class; type(Enum) is EnumType, type(ABC) is ABCMeta | python3.14 run | ran |
| uth-python-classes-mro-2-diamond | D(B,C) with C.f overriding A.f: __mro__ = (D,B,C,A,object), D().f() == "C" | python3.14 run | ran |
| uth-python-classes-mro-2-diamond | single base: MRO = [type] + base MRO (fast path) | Objects/typeobject.c:mro_implementation_unlocked | read |
| uth-python-classes-mro-2-diamond | type attribute cache has 1<<12 = 4096 entries, indexed by type version tag and name | Include/internal/pycore_interp_structs.h:MCACHE_SIZE_EXP; Objects/typeobject.c:MCACHE_HASH_METHOD | read |
| uth-python-classes-mro-2-diamond | method lookup walks tp_mro, first class dict with the name wins | Objects/typeobject.c:find_name_in_mro | read |
| uth-python-classes-mro-3-c3 | pmerge: take candidate head, skip if in tail of any list, else append; lists = base MROs + bases tuple | Objects/typeobject.c:pmerge, mro_implementation_unlocked | read |
| uth-python-classes-mro-3-c3 | error text "Cannot create a consistent method resolution order (MRO) for bases X, Y" for P(X,Y)/Q(Y,X)/R(P,Q) | Objects/typeobject.c:set_mro_error; python3.14 run | read, ran |
| uth-python-classes-mro-3-c3 | class B(object, X) raises the same TypeError | python3.14 run | ran |
| uth-python-classes-mro-3-c3 | C3 used since Python 2.3; monotonicity is the property | Doc/howto/mro.rst | read |
| uth-python-classes-mro-4-super | super() finds __class__ in type(self).__mro__ and searches from the next entry | Objects/typeobject.c:_super_lookup_descr | read |
| uth-python-classes-mro-4-super | zero-arg super uses first arg and the __class__ cell | Objects/typeobject.c:super_init_without_args; datamodel.rst "Creating the class object" | read |
| uth-python-classes-mro-4-super | M(L,R) both calling super().__init__(): prints M L R Base, MRO M L Rr Base object | python3.14 run | ran |
| uth-python-classes-mro-4-super | 3.12 added LOAD_SUPER_ATTR to speed up super() calls | Doc/whatsnew/3.12.rst (line 1086); Python/bytecodes.c LOAD_SUPER_ATTR | read |
| uth-python-classes-mro-5-metaclass | most derived metaclass among explicit metaclass and bases' metaclasses; no candidate satisfying all -> TypeError | Doc/reference/datamodel.rst "Determining the appropriate metaclass" | read |
| uth-python-classes-mro-5-metaclass | __init_subclass__ added 3.6, called on parent for each new subclass; __set_name__ also called by type.__new__ | datamodel.rst "Customizing class creation" | read; ran Plugin-style hook |
| uth-python-dunder-protocols-1-len-slot | len(x) calls __len__ via type slot; negative -> ValueError "__len__() should return >= 0" | Objects/typeobject.c:slot_sq_length | read |
| uth-python-dunder-protocols-1-len-slot | bool(): nb_bool, then mp_length, then sq_length, else true | Objects/object.c:PyObject_IsTrue | read |
| uth-python-dunder-protocols-2-type-lookup | implicit special-method lookup is on the type; c.__len__ = lambda ... makes len(c) raise TypeError; c.__len__() works | datamodel.rst "Special method lookup"; python3.14 run | read, ran |
| uth-python-dunder-protocols-2-type-lookup | lookup_maybe_method uses _PyType_Lookup(Py_TYPE(self), attr) | Objects/typeobject.c:lookup_method_ex | read |
| uth-python-dunder-protocols-2-type-lookup | rationale: int.__hash__() would otherwise be looked up as unbound instance method | datamodel.rst "Special method lookup" | read |
| uth-python-dunder-protocols-3-eq-hash | dict lookup: identity first, then equal hash and ==; | Objects/dictobject.c:compare_generic | read |
| uth-python-dunder-protocols-3-eq-hash | class defining __eq__ without __hash__ gets __hash__ = None | datamodel.rst __hash__; Objects/typeobject.c (overrides_hash, hash None hack) | read, ran |
| uth-python-dunder-protocols-3-eq-hash | 3.14 message "cannot use 'P' as a set element (unhashable type: 'P')" | python3.14 run | ran |
| uth-python-dunder-protocols-3-eq-hash | equal objects must have equal hash; hash((a,b)) advice; mutable -> no __hash__ | datamodel.rst __hash__ | read |
| uth-python-dunder-protocols-4-lt-tuple | list.sort and heapq call only Py_LT | Objects/listobject.c, Modules/_heapqmodule.c, Lib/heapq.py (newitem < parent) | read |
| uth-python-dunder-protocols-4-lt-tuple | tuple compare: find first index where == is false, then compare that index with < | Objects/listobject.c:unsafe_tuple_compare (mirrors tuplerichcompare) | read |
| uth-python-dunder-protocols-4-lt-tuple | reflection: __lt__/__gt__ are each other's; NotImplemented falls to the other side | datamodel.rst rich comparison | read |
| uth-python-dunder-protocols-4-lt-tuple | (1,N(1))<(1,N(2)) raises "'<' not supported between instances of 'N' and 'N'"; (1,..)<(2,..) fine | python3.14 run | ran |
| uth-python-dunder-protocols-4-lt-tuple | total_ordering fills missing ordering methods from one root | Lib/functools.py:total_ordering | read |
| uth-python-dunder-protocols-5-fallback | x in s: __contains__, else __iter__, else __getitem__ from 0 until IndexError | Doc/reference/expressions.rst "Membership test operations"; Objects/abstract.c:PySequence_Contains | read |
| uth-python-dunder-protocols-5-fallback | iter(): tp_iter else sequence protocol (PySeqIter) | Objects/abstract.c:PyObject_GetIter | read |
| uth-python-dunder-protocols-5-fallback | __getitem__-only class: list(obj)==[0,10,20], 20 in obj True | python3.14 run | ran |
| uth-python-iterators-generators-1-for-iter-next | FOR_ITER calls tp_iternext, StopIteration ends loop; GET_ITER calls PyObject_GetIter | Python/bytecodes.c:GET_ITER, FOR_ITER; dis output | read, ran |
| uth-python-iterators-generators-1-for-iter-next | list_iterator holds it_seq and it_index; it_seq set NULL when exhausted | Include/internal/pycore_list.h; Objects/listobject.c | read |
| uth-python-iterators-generators-1-for-iter-next | iter(it) is it; next after exhaustion keeps raising StopIteration | python3.14 run | ran |
| uth-python-iterators-generators-2-one-shot | map object consumed once: list(m) twice gives ['1','2'] then [] | python3.14 run | ran |
| uth-python-iterators-generators-3-generator-frame | PyGenObject embeds _PyInterpreterFrame (gi_iframe); states CREATED, SUSPENDED, EXECUTING, COMPLETED, CLEARED | Include/internal/pycore_interpframe_structs.h; Include/internal/pycore_frame.h | read |
| uth-python-iterators-generators-3-generator-frame | RETURN_GENERATOR creates the generator object; resume via gen_send_ex2 -> _PyEval_EvalFrame | InternalDocs/generators.md; Objects/genobject.c | read |
| uth-python-iterators-generators-3-generator-frame | FOR_ITER_GEN pushes the generator frame directly | Python/bytecodes.c:_FOR_ITER_GEN_FRAME; InternalDocs/generators.md | read |
| uth-python-iterators-generators-3-generator-frame | getgeneratorstate: GEN_CREATED, GEN_SUSPENDED, GEN_CLOSED; return value in StopIteration.value | python3.14 run; Objects/genobject.c:_PyGen_SetStopIterationValue | ran, read |
| uth-python-iterators-generators-4-lazy-genexp | sys.getsizeof: list comp of 10**6 = 8448728 B, genexp = 200 B | python3.14.8 run | ran |
| uth-python-iterators-generators-4-lazy-genexp | StopIteration inside generator becomes RuntimeError "generator raised StopIteration"; mandatory since 3.7 | Python/intrinsics.c:stopiteration_error; Doc/library/__future__.rst; Doc/whatsnew/3.5.rst | read, ran |
| uth-python-iterators-generators-5-yield-from-send | yield from forwards values, send() and exceptions; sub's return becomes StopIteration.value | Doc/reference/expressions.rst "Yield expressions"; python3.14 run | read, ran |
| uth-python-iterators-generators-5-yield-from-send | await x and yield from s both compile to SEND + YIELD_VALUE loop | dis of async def / generator on python3.14 | ran |
| uth-python-iterators-generators-5-yield-from-send | async functions use the same frame-suspend mechanism as generators | InternalDocs/generators.md, InternalDocs/frames.md | read |
| uth-python-iterators-generators-5-yield-from-send | asyncio Task step calls coro.send(None) | Lib/asyncio/tasks.py:__step_run_and_handle_result | read |
| uth-python-bytecode-eval-1-compile-run | dis of f(a,b): a*2+b on 3.14.8: LOAD_FAST_BORROW, LOAD_SMALL_INT, BINARY_OP *, LOAD_FAST_BORROW, BINARY_OP +, RETURN_VALUE | python3.14 dis | ran |
| uth-python-bytecode-eval-1-compile-run | LOAD_SMALL_INT added in 3.14 | Doc/library/dis.rst | read |
| uth-python-bytecode-eval-1-compile-run | instructions are 16-bit code units (opcode + arg) | co_code bytes pairs, InternalDocs/interpreter.md | ran, read |
| uth-python-bytecode-eval-2-code-object-pyc | co_consts=(2,), co_varnames=('a','b'), co_stacksize=2 for f | python3.14 run | ran |
| uth-python-bytecode-eval-2-code-object-pyc | cache_from_source("x.py") = __pycache__/x.cpython-314.pyc | python3.14 run | ran |
| uth-python-bytecode-eval-2-code-object-pyc | mtime check by default; main script not cached; .pyc only speeds loading | Doc/tutorial/modules.rst "Compiled Python files" | read |
| uth-python-bytecode-eval-3-fast-locals | LOAD_FAST reads GETLOCAL(oparg) array slot; LOAD_GLOBAL_MODULE checks dict keys version and reads entries[index] | Python/bytecodes.c | read |
| uth-python-bytecode-eval-3-fast-locals | local variables determined by scanning for binding operations; UnboundLocalError | Doc/reference/executionmodel.rst | read |
| uth-python-bytecode-eval-3-fast-locals | 3.14 message "cannot access local variable 'z' where it is not associated with a value" | python3.14 run | ran |
| uth-python-bytecode-eval-3-fast-locals | 3.11 caches global/builtin index so loads need zero namespace lookups | Doc/whatsnew/3.11.rst PEP 659 table | read |
| uth-python-bytecode-eval-4-adaptive | after 3 calls dis(adaptive=True) shows BINARY_OP_MULTIPLY_INT, BINARY_OP_ADD_INT, LOAD_GLOBAL_MODULE | python3.14.8 run | ran |
| uth-python-bytecode-eval-4-adaptive | ADAPTIVE_WARMUP_VALUE 1; backoff doubles per failure, MAX_BACKOFF 12 -> (1<<12)-1 = 4095 | Include/internal/pycore_code.h; Include/internal/pycore_backoff.h:restart_backoff_counter | read |
| uth-python-bytecode-eval-4-adaptive | specialise only hot code, de-specialise when types change; instruction families | Doc/whatsnew/3.11.rst; InternalDocs/interpreter.md "Specialization" | read |
| uth-python-bytecode-eval-5-eval-loop-jit | computed gotos used when compiler supports them (USE_COMPUTED_GOTOS) | Python/ceval_macros.h | read |
| uth-python-bytecode-eval-5-eval-loop-jit | 3.14 tail-call interpreter: Clang 19+, opt-in --with-tail-call-interp, geometric mean 3-5% faster, not Python tail-call optimisation | Doc/whatsnew/3.14.rst "A new type of interpreter" | read |
| uth-python-bytecode-eval-5-eval-loop-jit | JIT: experimental, 3.13 PEP 744, 3.14 official macOS/Windows binaries include it, PYTHON_JIT=1, 10% slower to 20% faster; hot JUMP_BACKWARD triggers tracing | Doc/whatsnew/3.14.rst jit section; Doc/whatsnew/3.13.rst; InternalDocs/jit.md | read |
| uth-python-gil-concurrency-1-why-gil | default-build Py_INCREF is op->ob_refcnt = cur + 1 (non-atomic) | Include/refcount.h:Py_INCREF | read |
| uth-python-gil-concurrency-1-why-gil | GIL = locked flag + mutex + condvar | Python/ceval_gil.c header comment | read |
| uth-python-gil-concurrency-1-why-gil | GIL makes object model (incl. dict) implicitly safe; released on I/O | Doc/glossary.rst "global interpreter lock" | read |
| uth-python-gil-concurrency-2-switch-io | DEFAULT_INTERVAL 5000 us; waiter times out then sets drop request; sys.getswitchinterval() == 0.005 | Python/ceval_gil.c:take_gil; python3.14 run | read, ran |
| uth-python-gil-concurrency-2-switch-io | eval breaker checked at RESUME, JUMP_BACKWARD, after CALL (_CHECK_PERIODIC) | Python/bytecodes.c | read |
| uth-python-gil-concurrency-2-switch-io | I/O and compression/hashing extensions release the GIL; threading fine for I/O-bound | Doc/glossary.rst; Doc/library/threading.rst | read |
| uth-python-gil-concurrency-3-not-atomic | atomic: L.append(x), x = L[i], D[x] = y; not: i = i+1, D[x] = D[x]+1 | Doc/faq/library.rst | read |
| uth-python-gil-concurrency-3-not-atomic | 4 threads x 1_000_000 n += 1: 3.14 (GIL) 4000000 twice; 3.14t 1068975 and 1051417 | /tmp/uth_P2/t_race.py on python3.14 and python3.14t | ran |
| uth-python-gil-concurrency-4-processes | spawn default on Windows and macOS; forkserver default on other POSIX from 3.14 | Doc/library/multiprocessing.rst; Doc/whatsnew/3.14.rst | read |
| uth-python-gil-concurrency-4-processes | args must be picklable; spawn slow vs fork/forkserver | Doc/library/multiprocessing.rst | read |
| uth-python-gil-concurrency-4-processes | InterpreterPoolExecutor (3.14): own GIL per interpreter, no shared mutable objects | Doc/library/concurrent.futures.rst | read |
| uth-python-gil-concurrency-5-free-threading | free-threaded object header: ob_tid, ob_mutex, ob_ref_local, ob_ref_shared | Include/object.h | read |
| uth-python-gil-concurrency-5-free-threading | owner thread: plain store to ob_ref_local, other threads atomic add to ob_ref_shared | Include/refcount.h:Py_INCREF (Py_GIL_DISABLED branch); PEP 703 "Biased Reference Counting" | read |
| uth-python-gil-concurrency-5-free-threading | 3.13 experimental, 3.14 officially supported (PEP 779) but optional; single-thread overhead ~1% macOS aarch64 to 8% x86-64 Linux; immortal constants; sys._is_gil_enabled(); GIL re-enabled by unsupported extensions | Doc/whatsnew/3.14.rst; Doc/howto/free-threading-python.rst | read |
