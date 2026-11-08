# Field outlines for coding craft (function and class level)

Collected 2026-11-08. Public pages only. Headings below were seen on the page or table of contents named in the row; nothing is reconstructed from memory. Short heading lists only, no source prose.

Shorthand: EP = Effective Python 3e; 6.031 = MIT 6.031 (spring 2022 site); 17-214 = CMU 17-214 (spring 2021 site); SWEG = Software Engineering at Google.

## 1. Language fluency and idioms (Python first, Java and Go as comparison)
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Effective Python 3e (Slatkin) | book | https://effectivepython.com/ | free item list on site, book is paid | TOC read (all 125 items) |
| Python tutorial and data model | official | https://docs.python.org/3/tutorial/index.html , https://docs.python.org/3/reference/datamodel.html | PSF docs, free | TOC read |
| Effective Go | official | https://go.dev/doc/effective_go | CC-BY, free | TOC read (last 7 KB, end of Errors, not read) |
| Effective Java 3e (Bloch) | book | https://pv168.pages.fi.muni.cz/literature/effective-java (course page quoting chapter ranges) | paid book; chapters via course page | TOC read (chapters and item ranges only, no item titles) |
| MIT 6.031 | course | https://web.mit.edu/6.031/www/sp22/ | CC-BY-SA, free | TOC read (29 readings; language is TypeScript) |

- EP: Pythonic thinking; strings and slicing; loops and iterators; dictionaries; functions; comprehensions and generators; classes and interfaces; metaclasses and attributes; robustness; collaboration (plus concurrency, performance, data structures, testing chapters).
- Python tutorial: control flow tools; data structures; modules; I/O; errors and exceptions; classes; stdlib tours; virtual environments. Data model: objects/values/types, standard type hierarchy, special methods (attribute access, descriptors, `__slots__`, class creation, container and numeric emulation, context managers), coroutines.
- Effective Go: formatting; commentary; names; control structures; functions (multiple returns, defer); data (new/make, slices, maps, append); initialization; methods (pointers vs values); interfaces and conversions; blank identifier; embedding; concurrency; errors (panic/recover).
- Effective Java: creating and destroying objects; methods common to all objects; classes and interfaces; generics; enums and annotations; lambdas and streams; methods; general programming; exceptions; concurrency; serialization.
- 6.031: static checking; mutability; ADTs; interfaces, generics, enums; recursion; equality; map/filter/reduce; recursive data types.

**Union of topics**
- Naming, style and formatting conventions (EP, Go, 6.031, Java): 4
- Functions: arguments, defaults, multiple returns, closures (EP, tutorial, Go, Java methods chapter): 4
- Collections and data-structure idioms (EP, tutorial, Go, Java generics/collections): 4
- Iteration, comprehensions, generators, streams (EP, tutorial, Java lambdas/streams, 6.031 map/filter/reduce): 4
- Classes, interfaces, composition vs inheritance, embedding (EP, tutorial, Go, Java, data model): 5
- Object protocol: equality, hash, repr, special methods (EP, data model, Java ch.3, 6.031 equality, Go): 5
- Mutability and aliasing (EP item 30, Java, 6.031, Go slices/copy): 4
- Resource cleanup: context managers, defer, try/finally (EP, tutorial, Go, Java): 4
- Static typing and type hints (EP, 6.031 static checking, Java generics, Go interfaces): 4
- Metaprogramming: descriptors, decorators, metaclasses, reflection (EP, data model, Java annotations): 3
- Equality of strings/bytes/text encoding (EP, io docs, Java): 2
- Modules, packages, initialization order (EP, tutorial, Go init): 3

**Interview probes**
- Rewrite non-idiomatic code (index loops, mutable defaults, string concatenation) in idiomatic form.
- Explain and fix the mutable default argument or late-binding closure bug.
- Implement `__eq__`/`__hash__`/`__repr__` consistently on a value class.
- Write a generator pipeline and explain laziness and single-use iterators.
- Write a context manager or decorator (with `functools.wraps`).
- Compare the same task in Python, Java and Go (error values vs exceptions, interfaces vs ABCs/protocols).
- Slicing, unpacking and dict/set idioms on a small data-wrangling task.
- Spot where an `isinstance` chain should become polymorphism or `singledispatch`.

## 2. Data modelling in code
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| MIT 6.031 readings 8, 10 (mutability, abstract data types) | course | https://web.mit.edu/6.031/www/sp22/classes/10-abstract-data-types/ | CC-BY-SA, free | page read (headings) |
| Python `dataclasses` docs | official | https://docs.python.org/3/library/dataclasses.html | PSF docs | page read |
| Python typing documentation | official | https://typing.python.org/en/latest/ | free | page read (nav sections) |
| Effective Python ch.5, 7 | book | https://effectivepython.com/ | item list free | TOC read |
| Refactoring catalog, "Organizing Data" group | practitioner | https://refactoring.guru/refactoring/techniques | free to read | page read |

- 6.031 ADT: what abstraction means; classifying types and operations (creators, producers, observers, mutators); designing an abstract type; representation independence; realizing ADTs; testing an ADT. Reading 8: mutable vs immutable, risks of mutation, aliasing, contracts. Reading 11 (title only): abstraction functions and rep invariants.
- dataclasses: `@dataclass`, `field()`, `__post_init__`, ClassVar, InitVar, frozen instances, inheritance, keyword-only fields, default factories, mutable default rule.
- typing: generics, protocols and structural subtyping, type narrowing, exhaustiveness, dataclasses, typed dicts, named tuples, enumerations, literals, overloads.
- EP: compose classes instead of nesting dicts/tuples (29); dedicated result objects (31); dataclasses (51, 56); `collections.abc` containers (57).
- Refactoring.guru Organizing Data: replace data value with object, replace array with object, encapsulate field/collection, replace type code with class/subclasses/state, replace magic number with constant, change value to reference and back.

**Union of topics**
- Value types and immutability (6.031, dataclasses, EP, refactoring): 4
- Aliasing and defensive copying (6.031, EP, refactoring): 3
- Encapsulation and invariants (6.031, EP, refactoring, typing): 4
- Replace primitives/tuples/dicts with small classes (EP, refactoring, 6.031): 3
- Enumerations and sum-type-like modelling (typing, 6.031 enums, refactoring type code): 3
- Defaults, optional and null handling (dataclasses, 6.031 "avoid null", typing narrowing): 3
- Generics and parametric containers (typing, 6.031, EP): 3
- Typed dict / record vs class decision (typing, dataclasses, EP): 3
- Abstraction function and rep invariant (6.031): 1
- Equality and hashing of data types (6.031 reading 15, dataclasses `eq`/`frozen`, EP): 3

**Interview probes**
- Model a domain (orders, bookings, inventory) as types; justify entity vs value object.
- Make a class immutable and say what breaks (hashing, mutation of shared lists).
- State the rep invariant and where it is checked.
- Choose dataclass / NamedTuple / TypedDict / plain class for a case.
- Replace a type-code string with an enum or subclass hierarchy.
- Find aliasing bugs in a class that returns its internal list.
- Add a field to a frozen dataclass without breaking callers.
- Represent "one of several shapes" with typing and exhaustive matching.

## 3. API and interface design
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| CMU 17-214 lectures "Designing APIs" 1 and 2, libraries and frameworks | course | https://www.cs.cmu.edu/~charlie/courses/17-214/2021-spring/ | free | TOC read (lecture titles only) |
| Google API Improvement Proposals (AIP 100-200) | official | https://google.aip.dev/general | CC-BY, free | page read (titles) |
| MIT 6.031 readings 6 and 7 (specifications) | course | https://web.mit.edu/6.031/www/sp22/classes/07-designing-specs/ | CC-BY-SA | page read |
| Effective Java ch.8 Methods (items 49-56) | book | https://pv168.pages.fi.muni.cz/literature/effective-java | paid | TOC read (ranges only) |
| EP ch.5 and 14 | book | https://effectivepython.com/ | item list free | TOC read |

- 17-214: design for change and information hiding; specification and unit testing; design for reuse (behavioral subtyping, delegation); designing APIs I and II; libraries and frameworks; Java Collections case study.
- AIP: resource-oriented design, resource names, standard methods (get/list/create/update/delete), custom methods, field names, time and duration, pagination, filtering, field masks, long-running operations, backwards compatibility, versioning, naming conventions, errors, retry configuration.
- 6.031 reading 6: behavioural equivalence, specification structure, avoid null, include emptiness, mutating functions, exceptions, special results. Reading 7: deterministic vs underdetermined, declarative vs operational, stronger vs weaker specs, coherent / informative / strong enough / weak enough, precondition or postcondition.
- Effective Java ch.8 (items 49-56): methods chapter (parameter checks, defensive copies, signatures, overloading, varargs, return values).
- EP: keyword-only and positional-only arguments (37); optional behaviour via kwargs (35); root exception to insulate callers (121); packages for stable APIs (119); `warnings` for migration (123); typing (124).

**Union of topics**
- Specifications: preconditions, postconditions, contracts (6.031, 17-214, Java methods): 3
- Information hiding, minimal public surface (17-214, EP packages, Java, AIP stability): 4
- Naming and consistency (AIP, EP, Java, 17-214): 4
- Parameter design: keyword-only, defaults, flags (EP, Java methods, AIP field rules): 3
- Return values and special results; avoid None/null (6.031, EP 32, Java): 3
- Error contract of an API (AIP errors, 6.031 exceptions, EP root exception): 3
- Evolution: versioning, deprecation, backward compatibility (AIP, EP warnings, 17-214 libraries): 3
- Standard methods and uniform shapes (AIP, 17-214 Collections): 2
- Behavioral subtyping and substitutability (17-214, 6.031 stronger/weaker specs): 2
- Pagination, idempotency and retries (AIP): 1

**Interview probes**
- Design the public interface of a small library (rate limiter, cache, logger) and defend each signature.
- Critique a given API: boolean flags, ambiguous returns, leaky types.
- Write the contract (pre/post conditions) for a function and decide who checks what.
- Evolve an API without breaking existing callers.
- Decide between exception, special value, or result object.
- Make the API hard to misuse (types, builder, required arguments).
- Pagination or iterator interface for a large result set.
- Name things and justify consistency across a set of methods.

## 4. OOP and design patterns
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| CMU 17-214 | course | https://www.cs.cmu.edu/~charlie/courses/17-214/2021-spring/ | free | TOC read (26 lectures) |
| Refactoring.guru pattern catalog | practitioner | https://refactoring.guru/design-patterns/catalog | free to read | page read |
| Effective Java ch.2-4 | book | https://pv168.pages.fi.muni.cz/literature/effective-java | paid | TOC read (ranges) |
| Effective Python ch.7 | book | https://effectivepython.com/ | item list free | TOC read |
| Game Programming Patterns (State chapter seen; book is a pattern catalogue) | practitioner | https://gameprogrammingpatterns.com/state.html | free online | page read (one chapter only) |

- 17-214: design for change and information hiding; behavioral subtyping, delegation, inheritance; design patterns for reuse (two lectures); OO analysis (domain model); OO design (responsibility assignment); "tis a gift to be simple"; Swing and Collections case studies; design pattern tour.
- Refactoring.guru: creational (Factory Method, Abstract Factory, Builder, Prototype, Singleton); structural (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy); behavioural (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor).
- Effective Java: static factories, builders, singleton, composition over inheritance, interfaces over abstract classes, minimize accessibility.
- EP ch.7: functions instead of classes for simple interfaces; polymorphism over isinstance; singledispatch; classmethod polymorphism; super; mix-ins; public attributes; `collections.abc`.

**Union of topics**
- Encapsulation / information hiding (17-214, Java, EP, catalog): 4
- Inheritance vs composition/delegation (17-214, Java, EP, catalog Bridge/Decorator): 4
- Polymorphism and subtyping (17-214, Java, EP, GPP): 4
- Creational patterns (17-214, catalog, Java items 1-5): 3
- Behavioural patterns incl. Strategy, Observer, Command, State (17-214, catalog, GPP, EP "functions as interfaces"): 4
- Structural patterns (17-214, catalog): 2
- Responsibility assignment and domain modelling (17-214): 1
- Singleton and its costs (catalog, Java, 17-214): 3
- Patterns as language features in Python (EP): 1
- Frameworks vs libraries (17-214): 1

**Interview probes**
- Class design from requirements: pick classes, responsibilities, relationships (parking lot, elevator, library).
- Choose Strategy vs inheritance and show the extension point.
- Implement Observer or Command with undo.
- Replace conditionals with polymorphism.
- Explain composition over inheritance with a concrete failure of inheritance.
- Show where a pattern becomes a plain function in Python.
- Apply SOLID critique to a given class.
- Add a new variant with minimal edits (open-closed in practice).

## 5. State machines
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Game Programming Patterns, "State" | book | https://gameprogrammingpatterns.com/state.html | free online | page read |
| statecharts.dev | practitioner | https://statecharts.dev/ | free | page read (home and glossary nav) |
| Stately / XState docs | practitioner | https://stately.ai/docs | free | page read (nav only: State Machines, Actors, Agents) |
| Refactoring.guru State pattern | practitioner | https://refactoring.guru/design-patterns/catalog | free | page read (listing only) |

- GPP: finite state machines; enums and switches; the State pattern (state interface, classes per state, delegate); static vs instantiated states; enter and exit actions; concurrent, hierarchical state machines; pushdown automata.
- statecharts.dev: what/why/why-not statecharts; executable statecharts; glossary: action, activity, atomic and compound state, guard, history state, initial and final state, parallel state, event, transition (automatic, delayed, internal, local, self), enter/exit.
- Stately docs: state machines, actors, agents, Studio (only nav read).
- Refactoring catalog: State listed under behavioural patterns; "Replace Type Code with State/Strategy" in refactoring.guru.

**Union of topics**
- States, events, transitions (GPP, statecharts, Stately): 3
- Enum plus switch vs State pattern (GPP, catalog): 2
- Guards and actions (statecharts, Stately): 2
- Enter/exit actions (GPP, statecharts): 2
- Hierarchical states (GPP, statecharts): 2
- Parallel/concurrent states (GPP, statecharts): 2
- History states (statecharts): 1
- Pushdown automata / state stack (GPP): 1
- Replacing type-code or flag soup with explicit states (GPP, refactoring.guru): 2
- Actor model on top of machines (Stately): 1

Thin: no university course outline was found for state machines at function level (not reached; see end).

**Interview probes**
- Implement an order, vending machine, traffic light or elevator as a transition table.
- Reject illegal transitions and report them.
- Convert boolean-flag code into explicit states.
- Add enter/exit hooks and a new state with minimal changes.
- Choose enum+table vs State classes and justify.
- Model a hierarchical case (media player with nested states).
- Test a machine exhaustively over (state, event) pairs.
- Persist and resume a machine.

## 6. Concurrency (threads, locks, async, memory model)
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Java Concurrency in Practice | book | https://www.informit.com/store/java-concurrency-in-practice-9780321349606 | paid | TOC read |
| MIT 6.031 readings 21-24 | course | https://web.mit.edu/6.031/www/sp22/classes/21-concurrency/ | CC-BY-SA | page read (reading 21 headings; 22-24 titles from index) |
| CMU 17-214 lectures 18-21 | course | https://www.cs.cmu.edu/~charlie/courses/17-214/2021-spring/ | free | TOC read |
| Python asyncio docs | official | https://docs.python.org/3/library/asyncio.html | PSF docs | TOC read |
| Python threading docs | official | https://docs.python.org/3/library/threading.html | PSF docs | page read |
| Go memory model | official | https://go.dev/ref/mem | CC-BY | page read |
| Effective Python ch.9 | book | https://effectivepython.com/ | item list free | TOC read |

- JCIP: thread safety; sharing objects; composing objects; building blocks; task execution; cancellation and shutdown; thread pools; GUI; liveness hazards; performance and scalability; testing concurrent programs; explicit locks; custom synchronizers; atomics and nonblocking; Java memory model.
- 6.031: two models (shared memory, message passing); processes, threads, time-slicing; interleaving; race condition; hard to test; promises; mutual exclusion; message passing; networking (22-25 titles).
- 17-214: Java primitives (two lectures); safety and structuring applications; parallelizing algorithms and frameworks; multi-threading and GUIs.
- asyncio: runners; coroutines and tasks; streams; synchronization primitives; subprocesses; queues; exceptions; event loop; futures; developing with asyncio; asyncio and free-threaded Python.
- threading: GIL and performance; thread-local data; Lock, RLock, Condition, Semaphore, Event, Timer, Barrier; locks in `with`.
- Go memory model: happens-before; data races and DRF-SC; goroutine creation/destruction; channel communication; locks; Once; atomics; incorrect synchronization (double-checked locking, busy waiting).
- EP ch.9: subprocess; threads for blocking I/O; Lock; Queue; ThreadPoolExecutor; coroutines; porting to asyncio; concurrent.futures for parallelism.

**Union of topics**
- Race conditions, interleavings, data races (JCIP, 6.031, 17-214, Go MM, EP, threading): 6
- Mutual exclusion: locks, monitors (JCIP, 6.031, 17-214, threading, Go MM, EP): 6
- Message passing, queues, channels (6.031, JCIP, asyncio, Go MM, EP): 5
- Memory model and visibility (JCIP, Go MM, threading GIL note): 3
- Thread pools and executors, task structure (JCIP, 17-214, EP, asyncio): 4
- Coroutines and event loops (asyncio, EP, 6.031 promises): 3
- Deadlock and liveness (JCIP, 17-214, 6.031 reading 23 title): 3
- Cancellation, timeouts and shutdown (JCIP, asyncio tasks, EP): 3
- Atomics and lock-free (JCIP, Go MM): 2
- Condition variables, semaphores, barriers, events (threading, JCIP, asyncio sync): 3
- GIL and CPU vs I/O bound choice (threading, EP, asyncio threading page): 3
- Testing concurrent code (JCIP, 6.031): 2
- Parallelizing algorithms (17-214, EP): 2
- Immutability and confinement for thread safety (JCIP, 17-214, 6.031): 3

**Interview probes**
- Thread-safe counter, cache or bounded queue; find the race in given code.
- Producer-consumer with Condition or Queue.
- Dining-philosophers-style deadlock: find and fix by lock ordering.
- Pick threads vs processes vs asyncio for a workload and justify.
- Write an asyncio fan-out with timeout and cancellation.
- Explain happens-before / why double-checked locking breaks.
- Rate limiter or semaphore-bounded worker pool.
- Make a class thread-safe without locks (immutability, confinement).

## 7. Error handling
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Python tutorial ch.8 Errors and Exceptions | official | https://docs.python.org/3/tutorial/errors.html | PSF docs | page read |
| Go blog, "Error handling and Go" and Effective Go Errors | official | https://go.dev/blog/error-handling-and-go | CC-BY | page read |
| MIT 6.031 reading 6 (exceptions, special results) and reading 9 | course | https://web.mit.edu/6.031/www/sp22/classes/06-specifications/ | CC-BY-SA | page read |
| Effective Java ch.10 Exceptions (items 69-77) | book | https://pv168.pages.fi.muni.cz/literature/effective-java | paid | TOC read (range only) |
| Effective Python ch.10 Robustness | book | https://effectivepython.com/ | item list free | TOC read |
| Rust Book ch.9 | official | https://doc.rust-lang.org/book/ch09-00-error-handling.html | MIT/Apache | existence only (chapter intro; subsections not seen) |

- Python ch.8: syntax errors; exceptions; handling; raising; chaining; user-defined; clean-up actions; predefined clean-up; exception groups; notes.
- Go blog: the error type; simplifying repetitive handling. Effective Go: multiple returns, defer, panic, recover.
- 6.031: exceptions for signalling bugs vs anticipated failures; special results; fail fast (reading 4); assertions, what to assert and what not (reading 9).
- Java ch.10: exceptions chapter, items 69-77 (titles not seen).
- EP ch.10: try/except/else/finally; assert vs raise; contextlib; short try blocks; do not catch Exception; Exception vs BaseException; traceback; exception chaining; resources and generators. Ch.5: raise instead of returning None (32). Ch.14: root exception (121).
- Rust ch.9: panic vs Result (intro says only this).

**Union of topics**
- Exceptions vs return codes/values (Python, Go, 6.031, Java, EP, Rust): 6
- Bug vs anticipated failure distinction (6.031, Java, EP assert/raise, Rust panic vs Result): 4
- Fail fast and assertions (6.031, EP, Java): 3
- Resource cleanup (finally, with, defer) (Python, Go, EP): 3
- Exception chaining and wrapping with context (Python, EP, Go blog): 3
- Custom exception hierarchies / error types (Python, Go blog, EP, Java): 4
- Narrow try blocks, never swallow errors, avoid broad catch (EP, Java): 2
- Panic/recover and unrecoverable errors (Go, Rust): 2
- Exception groups and notes (Python): 1
- Error contract in API (6.031, EP root exception): 2

**Interview probes**
- Critique code that swallows exceptions or catches `Exception`.
- Design the error types for a small library.
- Retry with backoff and say which errors are retriable.
- Ensure cleanup on every path (with / finally).
- Wrap a lower-level error without losing the cause.
- Decide return None vs raise, with the caller's view.
- Validate inputs at the boundary vs assert internal invariants.
- Convert an error-code function to exceptions (or the reverse in Go).

## 8. Testing
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| MIT 6.031 reading 3 Testing | course | https://web.mit.edu/6.031/www/sp22/classes/03-testing/ | CC-BY-SA | page read |
| Software Engineering at Google, ch.11-14 | book | https://abseil.io/resources/swe-book/html/toc.html | CC-BY-NC-ND, free online | TOC read |
| pytest how-to guides | official | https://docs.pytest.org/en/stable/how-to/index.html | MIT, free | page read |
| Effective Python ch.13 | book | https://effectivepython.com/ | item list free | TOC read |
| CMU 17-214 (specification and unit testing, CI recitation) | course | https://www.cs.cmu.edu/~charlie/courses/17-214/2021-spring/ | free | TOC read (one lecture title) |

- 6.031: validation; why testing is hard; test-first; systematic testing; partitioning and boundaries; automated unit testing; documenting strategy; black/glass box; coverage; unit vs integration; regression; iterative test-first.
- SWEG: Testing Overview; Unit Testing; Test Doubles; Larger Testing.
- pytest: invoke; assertions; fixtures; marks; parametrize; subtests; temp files; monkeypatch/mock; doctests; rerun failures; skip/xfail; logging and capture.
- EP ch.13: TestCase subclasses; integration over unit tests; setUp/tearDown isolation; mocks; encapsulating dependencies; assertAlmostEqual; pdb; tracemalloc.

**Union of topics**
- Test case selection: partitioning, boundaries (6.031, EP, pytest parametrize): 3
- Unit vs integration vs larger tests (6.031, SWEG, EP): 3
- Test doubles: mocks, fakes, stubs (SWEG, EP, pytest monkeypatch): 3
- Test isolation and fixtures (pytest, EP, SWEG): 3
- Test-first / TDD (6.031, 17-214): 2
- Coverage and its limits (6.031, SWEG): 2
- Regression tests (6.031, SWEG): 2
- Black box vs glass box (6.031, SWEG): 2
- Floating point and tolerant assertions (EP, pytest assertions): 2
- Testing concurrency (6.031 reading 21 exercise, JCIP ch.12): 2 (outside this row set)
- Flaky tests and determinism (SWEG larger testing): 1
- Writing testable design: dependency encapsulation (EP, SWEG test doubles, 17-214): 3

**Interview probes**
- Write tests for a given function: partitions, boundaries, error cases.
- Make untestable code testable (inject clock, network, randomness).
- Choose mock vs fake vs real dependency.
- Spot a flaky test and fix its cause.
- Parametrized tests and a fixture for shared setup.
- Say what coverage does not show; add a property or mutation-style check.
- Write the failing test first for a bug report.
- Test a concurrent or time-dependent function deterministically.

## 9. Parsing and I/O
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Crafting Interpreters | book | https://craftinginterpreters.com/contents.html | free online (CC-BY-NC-ND text) | TOC read |
| MIT 6.031 readings 18-19, 26-27 | course | https://web.mit.edu/6.031/www/sp22/classes/19-parsers/ | CC-BY-SA | page read (19); 18, 26, 27 titles from index (18 page 404) |
| Python `io` docs | official | https://docs.python.org/3/library/io.html | PSF docs | page read |
| Python tutorial ch.7 Input and Output | official | https://docs.python.org/3/tutorial/index.html | PSF docs | TOC read (chapter title only) |
| Python Logging HOWTO | official | https://docs.python.org/3/howto/logging.html | PSF docs | page read |

- Crafting Interpreters: scanning; representing code; parsing expressions; evaluating; statements and state; control flow; functions; resolving; classes; bytecode VM chapters (chunks, VM, scanning on demand, compiling expressions, hash tables, closures, GC).
- 6.031: regular expressions and grammars; parser generators; grammar; whitespace; parse tree; abstract syntax tree; handling errors; left recursion; little languages I and II.
- io: text vs binary vs raw I/O; text encoding; buffered streams; class hierarchy; performance; multi-threading; reentrancy.
- Logging HOWTO: loggers, handlers, formatters, levels, configuration for a library.

**Union of topics**
- Grammars and tokenization (Crafting Interpreters, 6.031): 2
- Recursive-descent parsing and precedence (Crafting Interpreters, 6.031): 2
- ASTs and tree evaluation (Crafting Interpreters, 6.031): 2
- Parse errors and recovery (Crafting Interpreters, 6.031): 2
- Regular expressions (6.031, plus Python re, not read): 1 read
- Text vs bytes and encodings (io docs, EP ch.2): 2
- Streams, buffering, file I/O (io docs, tutorial ch.7): 2
- Logging and structured diagnostic output (Logging HOWTO): 1
- Little languages / DSL design (6.031): 1

Thin: only two independent outlines per topic; Python `re` HOWTO and serialization (json/csv) docs not read.

**Interview probes**
- Write a tokenizer and recursive-descent parser for arithmetic or a small query language.
- Parse a log or CSV line format robustly (quoting, malformed rows).
- Stream a large file with bounded memory.
- Decode bytes safely; handle encoding errors.
- Read and write a custom binary or length-prefixed format.
- Implement a simple regex matcher or glob.
- Evaluate an AST with an environment (variables, scopes).
- Report a parse error with position.

## 10. Reading and extending unfamiliar code
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Working Effectively with Legacy Code (Feathers) | book | https://www.informit.com/store/working-effectively-with-legacy-code-9780131177055 | paid | TOC read |
| Software Engineering at Google, ch.17, 20, 22 | book | https://abseil.io/resources/swe-book/html/toc.html | free online | TOC read (titles only) |
| CMU 17-214 case studies (Swing, Collections, functional APIs) | course | https://www.cs.cmu.edu/~charlie/courses/17-214/2021-spring/ | free | TOC read |
| Code Reading (Spinellis) | book | https://www.spinellis.gr/codereading/ | paid | existence only (three chapter titles seen) |

- WELC: changing software; feedback; sensing and separation; seam model; tools; "I can't get this class into a test harness"; "I don't understand the code well enough to change it"; "my application has no structure"; "how do I know I'm not breaking anything"; dependency-breaking techniques.
- SWEG: Code Search; Static Analysis; Large-Scale Changes.
- 17-214: Java Swing, Java Collections and functional-API design case studies (reading real frameworks).
- Spinellis: basic programming elements, documentation, tackling large projects (partial).

**Union of topics**
- Understanding structure and entry points (WELC 16-17, Spinellis, 17-214 case studies): 3
- Code search and navigation tooling (SWEG, Spinellis): 2
- Characterization tests before change (WELC): 1
- Seams and dependency breaking (WELC): 1
- Making small safe changes in unfamiliar code (WELC, SWEG large-scale changes): 2
- Static analysis as a reading aid (SWEG): 1
- Reading idioms and architecture from famous libraries (17-214): 1

Thin: no source gives a systematic reading method beyond WELC; treat as one-book area with supporting material.

**Interview probes**
- Walk through an unfamiliar snippet or small repo and explain it.
- Find where a behaviour is implemented given only a symptom.
- Add a feature to given code with minimal diff.
- Write a characterization test for unclear code.
- Predict the output or side effects of tangled code.
- Identify the seam to break a hard dependency.
- Say what questions you ask before modifying.
- Trace data flow across modules.

## 11. Debugging
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| The Debugging Book (Zeller et al.) | book | https://debuggingbook.org/ | free online, open licence | TOC read |
| MIT 6.031 readings 9 and 13 | course | https://web.mit.edu/6.031/www/sp22/classes/13-debugging/ | CC-BY-SA | page read |
| Python `pdb` docs | official | https://docs.python.org/3/library/pdb.html | PSF docs | page read (two headings only) |
| Effective Python ch.13 (pdb, tracemalloc) | book | https://effectivepython.com/ | item list free | TOC read |
| Go diagnostics | official | https://go.dev/doc/diagnostics | CC-BY | page read |

- Debugging Book: introduction to debugging; tracing executions; how debuggers work; asserting expectations; tracking failure origins; reducing failure-inducing inputs; isolating failure-inducing changes; statistical debugging; mining specifications; generalizing circumstances; debugging performance issues; automatic repair; tracking bugs.
- 6.031 reading 13: reproduce; scientific method (study data, hypothesize, experiment, repeat); fix; slicing; delta debugging; one bug at a time; audit trail; check the plug. Reading 9: make bugs impossible, localize bugs, assertions, incremental development.
- pdb: command-line interface, debugger commands.
- Go diagnostics: profiling, tracing, debugging, runtime statistics.

**Union of topics**
- Reproduce the failure (Debugging Book, 6.031): 2
- Hypothesis-driven investigation (Debugging Book, 6.031): 2
- Input minimization / delta debugging (Debugging Book, 6.031): 2
- Bisecting changes (Debugging Book isolating changes): 1
- Assertions and defensive code (Debugging Book, 6.031, EP): 3
- Interactive debugger use (pdb, Debugging Book, EP, Go): 4
- Tracing and logging (Debugging Book, Go diagnostics, Logging HOWTO): 3
- Memory and performance debugging (Debugging Book, EP tracemalloc, Go diagnostics): 3
- Slicing / dependency tracking (Debugging Book, 6.031): 2
- Verify the fix, regression test (6.031, Debugging Book): 2

**Interview probes**
- Given a failing snippet or traceback, locate the bug and explain.
- Narrate a debugging plan out loud: reproduce, hypothesise, test.
- Minimize a failing input.
- Use git bisect style reasoning to find a bad commit.
- Choose between print, logging, pdb and a test for a case.
- Diagnose a memory leak or slow request from a profile.
- Find a heisenbug caused by shared state or time.
- Prevent recurrence: assertion, test, type.

## 12. Refactoring
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Fowler's refactoring catalog (2nd ed.) | practitioner | https://refactoring.com/catalog/ | catalog free, book paid | page read (names) |
| Refactoring.guru techniques (1st ed. grouping) | practitioner | https://refactoring.guru/refactoring/techniques | free to read | page read |
| MIT 6.031 reading 4 Code Review (code smells) | course | https://web.mit.edu/6.031/www/sp22/classes/04-code-review/ | CC-BY-SA | page read |
| WELC dependency-breaking techniques and appendix "Refactoring" | book | https://www.informit.com/store/working-effectively-with-legacy-code-9780131177055 | paid | TOC read |

- Fowler catalog (names): extract/inline function and variable; change function declaration; encapsulate variable/record/collection; rename; introduce parameter object; combine functions into class/transform; split phase; move function/field/statements; slide/split loop; replace loop with pipeline; remove dead code; split variable; replace temp with query; extract class; inline class; hide delegate; remove middle man; substitute algorithm; decompose conditional; consolidate conditional; guard clauses; polymorphism; special case; assertion; separate query from modifier; parameterize function; remove flag argument; preserve whole object; replace parameter with query; remove setting method; factory function; command and function; pull up / push down; replace type code with subclasses; remove subclass; extract superclass; collapse hierarchy; subclass/superclass with delegate.
- Refactoring.guru groups: composing methods; moving features between objects; organizing data; simplifying conditionals; simplifying method calls; dealing with generalization.
- 6.031 reading 4: DRY, comments where needed, fail fast, magic numbers, one purpose per variable, good names, whitespace, no globals, return results not print, avoid special-case code.

**Union of topics**
- Extract function/method and inline (Fowler, guru, 6.031 DRY): 3
- Rename for clarity (Fowler, guru, 6.031): 3
- Simplify conditionals: guard clauses, polymorphism (Fowler, guru): 2
- Parameter objects and signature changes (Fowler, guru): 2
- Move behaviour between classes; extract class (Fowler, guru): 2
- Generalization: pull up/push down, delegation over inheritance (Fowler, guru): 2
- Data encapsulation (Fowler, guru): 2
- Remove duplication, magic numbers, dead code (Fowler, 6.031): 2
- Refactor under tests / small safe steps (WELC): 1 (appendix title only)
- Break dependencies to enable refactoring (WELC): 1
- Code smell recognition (6.031 and Fowler's smell chapter, not read): 1 read

**Interview probes**
- Refactor a messy function: name the smell, apply a named refactoring.
- Replace a conditional chain with polymorphism or a table.
- Extract a class from a god class.
- Introduce a parameter object for a long argument list.
- Do it in small steps and say which tests keep you safe.
- Remove duplication without over-abstracting.
- Decide not to refactor (cost, risk, no tests).
- Rename and restructure for readability, not behaviour.

## 13. Code review
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Google Engineering Practices: code review guide | official | https://google.github.io/eng-practices/review/ | CC-BY, free | page read (nav lists of both guides) |
| Software Engineering at Google, ch.9 Code Review and ch.19 Critique | book | https://abseil.io/resources/swe-book/html/toc.html | free online | TOC read (titles only) |
| MIT 6.031 reading 4 Code Review | course | https://web.mit.edu/6.031/www/sp22/classes/04-code-review/ | CC-BY-SA | page read |

- Google reviewer guide: standard of code review; what to look for; navigating a CL; speed of reviews; writing comments; handling pushback. Author guide: good CL descriptions; small CLs; handling reviewer comments.
- SWEG: Code Review (ch.9), Critique tool (ch.19), Style Guides and Rules (ch.8), Static Analysis (ch.20).
- 6.031: style standards; DRY; comments; fail fast; magic numbers; one purpose per variable; good names; whitespace; globals; return not print; special-case code.

**Union of topics**
- Review standard: improve code health vs perfection (Google, SWEG): 2
- What to look for: design, function, complexity, tests, naming, comments (Google, 6.031): 2
- Small changes and good descriptions (Google, SWEG): 2
- Review speed and process (Google, SWEG): 2
- Writing and receiving comments, pushback (Google, SWEG): 2
- Style guides and automated checks (SWEG, 6.031): 2
- Concrete smells: DRY, magic numbers, names, globals (6.031): 1

**Interview probes**
- Review a diff aloud and prioritise: correctness, design, tests, style.
- Write a review comment for a defect, a nit and a design concern.
- Judge when a change is good enough to approve.
- Split an oversized change.
- Handle a disagreement with the author.
- Spot concurrency, error-handling and API-compat issues in a diff.
- Rewrite a poor commit or PR description.
- Say what the author should test.

## 14. Performance (profiling, complexity in practice, allocation)
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Brendan Gregg, Performance Methodology | practitioner | https://www.brendangregg.com/methodology.html | free | page read |
| Effective Python ch.11 Performance and ch.13 (tracemalloc) | book | https://effectivepython.com/ | item list free | TOC read |
| Python profilers docs | official | https://docs.python.org/3/library/profile.html | PSF docs | page read |
| Go diagnostics | official | https://go.dev/doc/diagnostics | CC-BY | page read |
| JCIP ch.11 Performance and Scalability | book | https://www.informit.com/store/java-concurrency-in-practice-9780321349606 | paid | TOC read (title only) |

- Gregg: scientific method; workload characterization; drill-down; USE; RED; CPU profile; off-CPU analysis; stack profile; active benchmarking; performance mantras; benchmarking checklist; anti-methods (streetlight, random change, etc.).
- EP ch.11: profile before optimizing; timeit microbenchmarks; replace Python with another language; ctypes; extension modules; bytecode caching; lazy imports; memoryview and bytearray (zero copy). Item 115: tracemalloc.
- Python profile docs: deterministic profiling, limitations, calibration, custom timer.
- Go diagnostics: profiling, tracing, runtime statistics.

**Union of topics**
- Measure first, profile before optimizing (Gregg, EP, Python docs, Go): 4
- Benchmarking pitfalls (Gregg, EP timeit, Python profile calibration): 3
- CPU profiles and flame graph reading (Gregg, Python docs, Go): 3
- Memory and allocation profiling (EP tracemalloc, Go): 2
- Algorithmic complexity vs constant factors (EP ch.11-12, Gregg mantras): 2
- Zero-copy and avoiding allocations (EP memoryview, Go runtime stats): 2
- Startup time and lazy loading (EP): 1
- Off-CPU, I/O wait analysis (Gregg, Go tracing): 2
- Scalability under locks (JCIP): 1
- Moving hot code to native code (EP): 1

**Interview probes**
- Given slow code and a profile, name the hot spot and fix.
- State complexity of a snippet and the realistic bottleneck (I/O, allocation, lock).
- Design a micro-benchmark that avoids common errors.
- Reduce allocations in a hot loop (generators, preallocation, views).
- Choose a data structure for access pattern and size.
- Cache or memoise with correct invalidation.
- Say when not to optimise.
- Explain CPU-bound vs I/O-bound and which tool shows each.

## 15. Working with AI coding tools
| Source | Kind | URL | Licence or access | Status |
|---|---|---|---|---|
| Claude Code best practices | official | https://code.claude.com/docs/en/best-practices | public docs | page read |
| OpenAI Codex best practices | official | https://learn.chatgpt.com/guides/best-practices (redirect from developers.openai.com/codex/learn/best-practices) | public docs | page read |
| GitHub Copilot best practices | official | https://docs.github.com/en/copilot/get-started/best-practices | public docs | page read |

- Claude Code: tell Claude what it cannot see (specific prompt, brainstorm first, short CLAUDE.md, scoped rules, skills, connect tools); give it a check to run (review against spec, Stop hook); enforce non-negotiable rules (hooks, permissions, sandbox); change defaults (permission mode, model, subagent cost, context cost); steer the session; run without you (scripts, schedules, parallel sessions).
- Codex: strong first prompt and context; plan first for difficult tasks; reusable AGENTS.md; configure for consistency; testing and review for reliability; MCPs; skills; scheduled tasks; organising long chats; common mistakes.
- Copilot: strengths and weaknesses; choose the right tool; thoughtful prompts; check Copilot's work; guide towards helpful outputs; stay up to date.

**Union of topics**
- Specific prompts and context (all 3): 3
- Planning before coding (Claude brainstorm, Codex): 2
- Verification: tests, checks, review of output (all 3): 3
- Persistent project guidance (CLAUDE.md, AGENTS.md; Copilot guiding outputs): 3
- Permissions, sandboxing and guardrails (Claude): 1
- Tool and context connections: MCP (Claude, Codex): 2
- Reusable skills / workflows (Claude, Codex): 2
- Knowing model limits (Copilot, Codex common mistakes): 2
- Cost and context management (Claude, Codex long chats): 2
- Automation and parallel runs (Claude, Codex scheduled): 2

**Interview probes**
- Walk through how you would prompt an agent for a bug fix and verify it.
- Review AI-generated code: find hallucinated API, missing edge case, over-engineering.
- Write the project instruction file you would give an agent.
- Decide which tasks to delegate and which to do by hand.
- Specify acceptance checks the agent can run.
- Detect and fix a subtly wrong AI patch.
- Break a task into agent-sized steps.
- Explain risks: secrets, over-broad permissions, unreviewed code.

## Not reached
- Effective Java item titles: O'Reilly TOC page returned 403; only chapter names and item ranges seen via a course page.
- Working Effectively with Legacy Code at O'Reilly: 403 (TOC obtained from InformIT instead).
- MIT 6.031 reading 18 (regex and grammars) page: 404; reading 23 (mutual exclusion) page: 404 (guessed slug). Titles taken from the index page only.
- Effective Go: final 7 KB (end of Errors) not read.
- Rust Book ch.9 subsections: the fetch returned only the intro.
- Code Reading (Spinellis): full TOC not on fetched page.
- Fowler's Refactoring smells chapter, Python `re` HOWTO, "Why Programs Fail" book page, Google Testing Blog, Bloch's API talk, Python asyncio dev page, Java memory model chapter details: not fetched (time).
- State machines: no course outline found.
- Sources on Medium, uber.com, dl.acm.org, w3.org: not attempted.
