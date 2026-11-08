# Outline map: field outlines against the LLD skeleton

Each bullet under Union of topics and Interview probes in FIELD_OUTLINES.md, mapped to leaves in skeleton/low-level-design.yaml. A leaf counts only when its title and summary say the thing. Gap leaf ids below are proposals; none exists yet.

## 1. Language fluency and idioms
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Naming, style and formatting conventions | topic | GAP | fluency.style (api.naming is API consistency only; review.priorities just says leave style to tools) |
| Functions: arguments, defaults, multiple returns, closures | topic | covered | fluency.functions, python.first-class-functions |
| Collections and data-structure idioms | topic | covered | fluency.collections |
| Iteration, comprehensions, generators, streams | topic | covered | fluency.iteration, python.context-iterators |
| Classes, interfaces, composition vs inheritance, embedding | topic | covered | principles.composition, python.protocols-abc, oop.interfaces (Go embedding not named in languages.go-idioms) |
| Object protocol: equality, hash, repr, special methods | topic | covered | python.data-model |
| Mutability and aliasing | topic | covered | fluency.mutability, data.defensive-copy |
| Resource cleanup: context managers, defer, try/finally | topic | covered | python.context-iterators, errors.cleanup |
| Static typing and type hints | topic | covered | python.typing |
| Metaprogramming: descriptors, decorators, metaclasses, reflection | topic | GAP | python.metaprogramming (only decorators are taught, in python.first-class-functions; no descriptors, property, metaclass, __init_subclass__, reflection) |
| Equality of strings/bytes/text encoding | topic | covered | fluency.strings-bytes |
| Modules, packages, initialization order | topic | covered | python.modules |
| Rewrite non-idiomatic code in idiomatic form | probe | covered | fluency.idiomatic-rewrite |
| Explain and fix mutable default / late-binding closure bug | probe | covered | fluency.mutability |
| Implement __eq__/__hash__/__repr__ consistently | probe | covered | python.data-model |
| Generator pipeline, laziness, single-use iterators | probe | covered | python.context-iterators, parsing-io.streams |
| Write a context manager or decorator with functools.wraps | probe | covered | python.context-iterators, python.first-class-functions |
| Compare same task in Python, Java and Go | probe | covered | languages.models, languages.go-idioms, languages.java-modern |
| Slicing, unpacking, dict/set idioms on a data-wrangling task | probe | covered | fluency.collections, fluency.functions, fluency.strings-bytes |
| Spot isinstance chain, use polymorphism or singledispatch | probe | covered | fluency.idiomatic-rewrite, refactoring.conditionals |

## 2. Data modelling in code
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Value types and immutability | topic | covered | data.value-entity, oop.values, python.dataclasses-enums |
| Aliasing and defensive copying | topic | covered | data.defensive-copy, fluency.mutability |
| Encapsulation and invariants | topic | covered | data.invariants |
| Replace primitives/tuples/dicts with small classes | topic | covered | data.primitive-obsession |
| Enumerations and sum-type-like modelling | topic | covered | data.sum-types, python.dataclasses-enums |
| Defaults, optional and null handling | topic | covered | data.optional, python.dataclasses-enums (default_factory) |
| Generics and parametric containers | topic | covered | python.typing |
| Typed dict / record vs class decision | topic | covered | data.record-choice |
| Abstraction function and rep invariant | topic | GAP | data.abstraction-function (data.invariants names the rep invariant only; the abstraction function and representation independence are not taught) |
| Equality and hashing of data types | topic | covered | python.data-model, data.value-entity |
| Model a domain as types; entity vs value object | probe | covered | data.value-entity, method.modeling |
| Make a class immutable and say what breaks | probe | covered | data.value-entity, oop.values |
| State the rep invariant and where it is checked | probe | covered | data.invariants |
| Choose dataclass / NamedTuple / TypedDict / plain class | probe | covered | data.record-choice |
| Replace a type-code string with an enum or hierarchy | probe | covered | data.sum-types |
| Find aliasing bugs in a class returning its internal list | probe | covered | data.defensive-copy |
| Add a field to a frozen dataclass without breaking callers | probe | covered | data.evolution |
| Represent "one of several shapes" with exhaustive matching | probe | covered | data.sum-types |

## 3. API and interface design
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Specifications: pre/postconditions, contracts | topic | covered | api.specs, structure.api |
| Information hiding, minimal public surface | topic | covered | api.library-design, python.modules, oop.pillars |
| Naming and consistency | topic | covered | api.naming |
| Parameter design: keyword-only, defaults, flags | topic | covered | api.parameters, fluency.functions |
| Return values and special results; avoid None | topic | covered | api.returns, data.optional |
| Error contract of an API | topic | covered | api.error-contract |
| Evolution: versioning, deprecation, compatibility | topic | covered | api.evolution, structure.api |
| Standard methods and uniform shapes | topic | covered | api.naming (shape consistency of a method set; weakest match, no standard-method catalogue) |
| Behavioral subtyping and substitutability | topic | covered | principles.solid (Liskov), api.specs (stronger/weaker specs) |
| Pagination, idempotency and retries | topic | covered | api.paging-iteration, errors.retry, parsing-io.http-client |
| Design public interface of a small library, defend signatures | probe | covered | api.library-design, problems.components.rate-limiter |
| Critique an API: flags, ambiguous returns, leaky types | probe | covered | api.parameters, api.returns, api.hard-to-misuse |
| Write the contract and decide who checks what | probe | covered | api.specs |
| Evolve an API without breaking callers | probe | covered | api.evolution |
| Choose exception, special value or result object | probe | covered | api.returns, errors.exceptions-vs-values |
| Make the API hard to misuse | probe | covered | api.hard-to-misuse, patterns.creational |
| Pagination or iterator interface for a large result set | probe | covered | api.paging-iteration |
| Name things and justify consistency | probe | covered | api.naming |

## 4. OOP and design patterns
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Encapsulation / information hiding | topic | covered | oop.pillars |
| Inheritance vs composition/delegation | topic | covered | principles.composition, refactoring.hierarchy |
| Polymorphism and subtyping | topic | covered | oop.pillars, python.protocols-abc |
| Creational patterns | topic | covered | patterns.creational |
| Behavioural patterns incl. Strategy, Observer, Command, State | topic | covered | patterns.strategy, patterns.observer, patterns.command, patterns.state, patterns.behavioral |
| Structural patterns | topic | covered | patterns.structural |
| Responsibility assignment and domain modelling | topic | GAP | principles.responsibility (method.modeling does noun-verb extraction and oop.relationships does arrows; nothing teaches who owns a behaviour: information expert, high cohesion, tell-don't-ask) |
| Singleton and its costs | topic | covered | patterns.creational, quality.testability (global state) |
| Patterns as language features in Python | topic | covered | patterns.selection, python.first-class-functions (each pattern leaf asks if Python still needs it) |
| Frameworks vs libraries | topic | GAP | patterns.frameworks (inversion of control, extension points, template method hooks; api.library-design covers libraries only) |
| Class design from requirements (parking lot, elevator, library) | probe | covered | method.modeling, problems.machines.parking-lot, problems.machines.elevator, problems.booking.library |
| Choose Strategy vs inheritance, show the extension point | probe | covered | patterns.strategy, principles.composition |
| Implement Observer or Command with undo | probe | covered | patterns.observer, patterns.command |
| Replace conditionals with polymorphism | probe | covered | refactoring.conditionals, quality.refactoring |
| Explain composition over inheritance with a concrete failure | probe | covered | principles.composition |
| Show where a pattern becomes a plain function | probe | covered | python.first-class-functions, patterns.strategy |
| Apply SOLID critique to a given class | probe | covered | principles.solid |
| Add a new variant with minimal edits | probe | covered | principles.solid, method.evaluation |

## 5. State machines
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| States, events, transitions | topic | covered | fsm.transition-table, structure.state-machines |
| Enum plus switch vs State pattern | topic | covered | fsm.table-vs-pattern, patterns.state |
| Guards and actions | topic | covered | fsm.guards-actions |
| Enter/exit actions | topic | covered | fsm.guards-actions |
| Hierarchical states | topic | covered | fsm.hierarchical |
| Parallel/concurrent states | topic | covered | fsm.hierarchical |
| History states | topic | GAP | fsm.history (fsm.hierarchical names nested, parallel and stack, not history) |
| Pushdown automata / state stack | topic | covered | fsm.hierarchical (state stack) |
| Replacing type-code or flag soup with explicit states | topic | covered | fsm.flags-to-states, data.sum-types |
| Actor model on top of machines | topic | out-of-scope | Actor orchestration (Stately actors/agents) is system architecture, not function/class craft; message passing itself is in concurrency-depth.confinement |
| Implement order/vending/traffic light/elevator as transition table | probe | covered | fsm.transition-table, problems.machines.vending-machine, problems.machines.traffic-signal |
| Reject illegal transitions and report them | probe | covered | fsm.illegal-transitions |
| Convert boolean-flag code into explicit states | probe | covered | fsm.flags-to-states |
| Add enter/exit hooks and a new state with minimal changes | probe | covered | fsm.guards-actions |
| Choose enum+table vs State classes | probe | covered | fsm.table-vs-pattern |
| Model a hierarchical case (media player) | probe | covered | fsm.hierarchical, problems.social.music-streaming |
| Test a machine exhaustively over (state, event) pairs | probe | covered | fsm.testing |
| Persist and resume a machine | probe | covered | fsm.persistence |

## 6. Concurrency
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Race conditions, interleavings, data races | topic | covered | concurrency.model, concurrency-depth.compound-actions, concurrency-depth.memory-model |
| Mutual exclusion: locks, monitors | topic | covered | concurrency.primitives |
| Message passing, queues, channels | topic | covered | concurrency.primitives (queue.Queue), concurrency-depth.confinement, concurrency.patterns |
| Memory model and visibility | topic | covered | concurrency-depth.memory-model |
| Thread pools and executors, task structure | topic | covered | concurrency.patterns, problems.components.thread-pool |
| Coroutines and event loops | topic | covered | concurrency.asyncio |
| Deadlock and liveness | topic | covered | concurrency.hazards |
| Cancellation, timeouts and shutdown | topic | covered | concurrency-depth.cancel-shutdown |
| Atomics and lock-free | topic | covered | concurrency-depth.atomics |
| Condition variables, semaphores, barriers, events | topic | covered | concurrency.primitives, concurrency-depth.conditions (Barrier not named in either) |
| GIL and CPU vs I/O bound choice | topic | covered | concurrency.model, concurrency-depth.selection |
| Testing concurrent code | topic | covered | concurrency-depth.testing |
| Parallelizing algorithms | topic | GAP | concurrency-depth.parallel-scaling (chunking, fork-join, speedup limits; selection only picks the model) |
| Immutability and confinement for thread safety | topic | covered | concurrency-depth.confinement |
| Thread-safe counter, cache or bounded queue; find the race | probe | covered | concurrency-depth.safe-structures, problems.components.bounded-blocking-queue, concurrency-depth.compound-actions |
| Producer-consumer with Condition or Queue | probe | covered | concurrency.patterns, concurrency-depth.conditions |
| Dining-philosophers deadlock, fix by lock ordering | probe | covered | concurrency.hazards |
| Pick threads vs processes vs asyncio | probe | covered | concurrency-depth.selection, concurrency.model |
| asyncio fan-out with timeout and cancellation | probe | covered | concurrency.asyncio, concurrency-depth.cancel-shutdown |
| Explain happens-before / double-checked locking | probe | covered | concurrency-depth.memory-model |
| Rate limiter or semaphore-bounded worker pool | probe | covered | problems.components.rate-limiter, problems.components.thread-pool, concurrency.primitives |
| Make a class thread-safe without locks | probe | covered | concurrency-depth.confinement |

## 7. Error handling
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Exceptions vs return codes/values | topic | covered | errors.exceptions-vs-values, quality.errors, languages.models |
| Bug vs anticipated failure | topic | covered | errors.bug-vs-failure |
| Fail fast and assertions | topic | covered | errors.bug-vs-failure, errors.boundary-validation |
| Resource cleanup (finally, with, defer) | topic | covered | errors.cleanup |
| Exception chaining and wrapping with context | topic | covered | errors.chaining |
| Custom exception hierarchies / error types | topic | covered | errors.taxonomy |
| Narrow try blocks, never swallow, avoid broad catch | topic | covered | errors.narrow-catch |
| Panic/recover and unrecoverable errors | topic | GAP | errors.unrecoverable (when to crash, top-level handlers, recover at a process boundary; languages.go-idioms lists defer but not panic) |
| Exception groups and notes | topic | GAP | errors.exception-groups (ExceptionGroup, except*, add_note; also needed for asyncio TaskGroup) |
| Error contract in API | topic | covered | api.error-contract |
| Critique code that swallows exceptions or catches Exception | probe | covered | errors.narrow-catch |
| Design the error types for a small library | probe | covered | errors.taxonomy, api.error-contract |
| Retry with backoff, which errors are retriable | probe | covered | errors.retry |
| Ensure cleanup on every path | probe | covered | errors.cleanup |
| Wrap a lower-level error without losing the cause | probe | covered | errors.chaining |
| Decide return None vs raise | probe | covered | api.returns, errors.exceptions-vs-values |
| Validate inputs at the boundary vs assert invariants | probe | covered | errors.boundary-validation, errors.bug-vs-failure |
| Convert error-code function to exceptions or reverse in Go | probe | covered | errors.exceptions-vs-values, languages.models, languages.go-idioms |

## 8. Testing
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Test case selection: partitioning, boundaries | topic | covered | testing.partitioning |
| Unit vs integration vs larger tests | topic | covered | testing.test-levels |
| Test doubles: mocks, fakes, stubs | topic | covered | testing.doubles, quality.testability |
| Test isolation and fixtures | topic | covered | testing.pytest-tools |
| Test-first / TDD | topic | covered | testing.test-first |
| Coverage and its limits | topic | covered | testing.coverage-limits |
| Regression tests | topic | covered | testing.test-first (test from a bug report), debugging.prevent |
| Black box vs glass box | topic | GAP | testing.box-testing (testing.partitioning is spec-based only; choosing cases from the code's branches is not taught) |
| Floating point and tolerant assertions | topic | covered | fluency.time-numbers (float comparison; pytest.approx not named in testing.pytest-tools) |
| Testing concurrency | topic | covered | concurrency-depth.testing |
| Flaky tests and determinism | topic | covered | testing.flaky |
| Writing testable design: dependency encapsulation | topic | covered | testing.testable-design, quality.testability |
| Write tests for a function: partitions, boundaries, errors | probe | covered | testing.partitioning |
| Make untestable code testable (inject clock, network, random) | probe | covered | testing.testable-design, reading.seams |
| Choose mock vs fake vs real dependency | probe | covered | testing.doubles |
| Spot a flaky test and fix its cause | probe | covered | testing.flaky |
| Parametrized tests and a fixture for shared setup | probe | covered | testing.pytest-tools |
| Say what coverage does not show; property or mutation check | probe | covered | testing.coverage-limits |
| Write the failing test first for a bug report | probe | covered | testing.test-first |
| Test a concurrent or time-dependent function deterministically | probe | covered | concurrency-depth.testing, testing.testable-design |

## 9. Parsing and I/O
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Grammars and tokenization | topic | covered | parsing-io.tokenizer, parsing-io.recursive-descent |
| Recursive-descent parsing and precedence | topic | covered | parsing-io.recursive-descent |
| ASTs and tree evaluation | topic | covered | parsing-io.ast-eval |
| Parse errors and recovery | topic | covered | parsing-io.parse-errors |
| Regular expressions | topic | covered | parsing-io.regex |
| Text vs bytes and encodings | topic | covered | fluency.strings-bytes |
| Streams, buffering, file I/O | topic | covered | parsing-io.streams, parsing-io.formats |
| Logging and structured diagnostic output | topic | covered | parsing-io.diagnostics |
| Little languages / DSL design | topic | GAP | parsing-io.dsl (the parser leaves build one; no leaf teaches when to make a small language, embedded vs external) |
| Tokenizer and recursive-descent parser for arithmetic/query language | probe | covered | parsing-io.tokenizer, parsing-io.recursive-descent, parsing-io.ast-eval |
| Parse a log or CSV format robustly | probe | covered | parsing-io.formats, bank.practical.log-processing |
| Stream a large file with bounded memory | probe | covered | parsing-io.streams |
| Decode bytes safely; handle encoding errors | probe | covered | fluency.strings-bytes |
| Custom binary or length-prefixed format | probe | covered | parsing-io.binary |
| Implement a simple regex matcher or glob | probe | GAP | parsing-io.pattern-matcher (parsing-io.regex teaches using regexes; hand-writing a matcher with backtracking or DP is nowhere) |
| Evaluate an AST with an environment | probe | covered | parsing-io.ast-eval |
| Report a parse error with position | probe | covered | parsing-io.parse-errors, parsing-io.tokenizer |

## 10. Reading and extending unfamiliar code
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Understanding structure and entry points | topic | covered | reading.entry-points, reading.trace-flow |
| Code search and navigation tooling | topic | covered | reading.code-search |
| Characterization tests before change | topic | covered | reading.characterization |
| Seams and dependency breaking | topic | covered | reading.seams |
| Small safe changes in unfamiliar code | topic | covered | reading.minimal-diff, refactoring.small-steps |
| Static analysis as a reading aid | topic | GAP | reading.static-analysis (type checker, linter, call graph and dead-code reports used to read code) |
| Reading idioms and architecture from famous libraries | topic | GAP | reading.famous-libraries (read one stdlib or well-known module end to end and name its idioms) |
| Walk through an unfamiliar snippet or small repo | probe | covered | reading.entry-points, reading.trace-flow |
| Find where a behaviour is implemented from a symptom | probe | covered | reading.code-search |
| Add a feature with minimal diff | probe | covered | reading.minimal-diff, rounds.extend-code |
| Write a characterization test for unclear code | probe | covered | reading.characterization |
| Predict output or side effects of tangled code | probe | GAP | reading.predict-behaviour (mentally executing code with aliasing, hidden state, evaluation order; reading.trace-flow follows data across modules, a different skill) |
| Identify the seam to break a hard dependency | probe | covered | reading.seams |
| Say what questions you ask before modifying | probe | covered | reading.questions |
| Trace data flow across modules | probe | covered | reading.trace-flow |

## 11. Debugging
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Reproduce the failure | topic | covered | debugging.reproduce |
| Hypothesis-driven investigation | topic | covered | debugging.hypothesis |
| Input minimization / delta debugging | topic | covered | debugging.minimize |
| Bisecting changes | topic | covered | debugging.bisect |
| Assertions and defensive code | topic | covered | errors.bug-vs-failure, debugging.prevent |
| Interactive debugger use | topic | covered | debugging.tools |
| Tracing and logging | topic | covered | debugging.tools, parsing-io.diagnostics |
| Memory and performance debugging | topic | covered | debugging.memory, performance.profiling |
| Slicing / dependency tracking | topic | GAP | debugging.failure-origins (infection chain, backward slice from the wrong value to the first wrong state) |
| Verify the fix, regression test | topic | covered | debugging.prevent |
| Locate the bug from a failing snippet or traceback | probe | covered | debugging.hypothesis, rounds.bug-bash (reading a traceback is not named) |
| Narrate a debugging plan out loud | probe | covered | debugging.hypothesis |
| Minimize a failing input | probe | covered | debugging.minimize |
| Git-bisect reasoning to find a bad commit | probe | covered | debugging.bisect |
| Choose between print, logging, pdb and a test | probe | covered | debugging.tools |
| Diagnose a memory leak or slow request from a profile | probe | covered | debugging.memory, performance.profiling |
| Find a heisenbug from shared state or time | probe | covered | debugging.heisenbugs |
| Prevent recurrence: assertion, test, type | probe | covered | debugging.prevent |

## 12. Refactoring
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Extract function/method and inline | topic | covered | refactoring.composing |
| Rename for clarity | topic | GAP | refactoring.rename (no refactoring leaf names rename, split variable or replace temp with query; api.naming is about API shape) |
| Simplify conditionals: guard clauses, polymorphism | topic | covered | refactoring.conditionals |
| Parameter objects and signature changes | topic | covered | refactoring.signatures |
| Move behaviour between classes; extract class | topic | covered | refactoring.moving |
| Generalization: pull up/push down, delegation over inheritance | topic | covered | refactoring.hierarchy |
| Data encapsulation | topic | covered | data.defensive-copy, data.primitive-obsession, data.invariants |
| Remove duplication, magic numbers, dead code | topic | covered | principles.simplicity, quality.smells (magic numbers not named) |
| Refactor under tests / small safe steps | topic | covered | refactoring.small-steps |
| Break dependencies to enable refactoring | topic | covered | reading.seams, quality.testability |
| Code smell recognition | topic | covered | quality.smells |
| Refactor a messy function: name the smell, apply a named refactoring | probe | covered | quality.smells, refactoring.composing, rounds.refactoring |
| Replace a conditional chain with polymorphism or a table | probe | covered | refactoring.conditionals |
| Extract a class from a god class | probe | covered | refactoring.moving |
| Introduce a parameter object for a long argument list | probe | covered | refactoring.signatures |
| Do it in small steps, say which tests keep you safe | probe | covered | refactoring.small-steps |
| Remove duplication without over-abstracting | probe | covered | refactoring.over-abstraction, principles.simplicity |
| Decide not to refactor | probe | covered | refactoring.when-not |
| Rename and restructure for readability, not behaviour | probe | GAP | refactoring.rename (same leaf as the topic row) |

## 13. Code review
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Review standard: improve code health vs perfection | topic | covered | review.approval-bar |
| What to look for: design, function, complexity, tests, naming, comments | topic | covered | review.priorities |
| Small changes and good descriptions | topic | covered | review.small-changes |
| Review speed and process | topic | out-of-scope | Team turnaround and reviewer assignment are process policy, not code craft at function and class level |
| Writing and receiving comments, pushback | topic | GAP | review.pushback (review.comments covers writing only; responding to reviewer comments and pushback is not taught) |
| Style guides and automated checks | topic | GAP | fluency.style (review.priorities only says leave style to tools; no leaf on formatters, linters, style guides) |
| Concrete smells: DRY, magic numbers, names, globals | topic | covered | quality.smells, principles.simplicity |
| Review a diff aloud and prioritise | probe | covered | review.reading-a-diff, review.priorities |
| Write a comment for a defect, a nit and a design concern | probe | covered | review.comments |
| Judge when a change is good enough to approve | probe | covered | review.approval-bar |
| Split an oversized change | probe | covered | review.small-changes |
| Handle a disagreement with the author | probe | GAP | review.pushback |
| Spot concurrency, error-handling and API-compat issues | probe | covered | review.risk-patterns |
| Rewrite a poor commit or PR description | probe | covered | review.small-changes |
| Say what the author should test | probe | covered | review.priorities, testing.partitioning |

## 14. Performance
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Measure first, profile before optimizing | topic | covered | performance.measure-first |
| Benchmarking pitfalls | topic | covered | performance.benchmarks |
| CPU profiles and flame graph reading | topic | covered | performance.profiling |
| Memory and allocation profiling | topic | covered | debugging.memory (tracemalloc), performance.memory |
| Algorithmic complexity vs constant factors | topic | covered | performance.complexity-constants |
| Zero-copy and avoiding allocations | topic | covered | performance.memory |
| Startup time and lazy loading | topic | GAP | performance.startup (import cost, lazy imports, cold-start measurement) |
| Off-CPU, I/O wait analysis | topic | covered | performance.profiling (CPU time vs waiting time) |
| Scalability under locks | topic | GAP | concurrency-depth.parallel-scaling (lock contention, Amdahl; safe-structures speaks of lock granularity only) |
| Moving hot code to native code | topic | GAP | performance.native (builtins and C-backed stdlib, NumPy vectorisation, extension modules; only NumPy appears in a bank leaf, not as a lesson) |
| Given slow code and a profile, name the hot spot and fix | probe | covered | performance.profiling |
| State complexity and the realistic bottleneck | probe | covered | performance.complexity-constants |
| Design a micro-benchmark that avoids common errors | probe | covered | performance.benchmarks |
| Reduce allocations in a hot loop | probe | covered | performance.memory |
| Choose a data structure for access pattern and size | probe | covered | performance.data-structures, fluency.collections |
| Cache or memoise with correct invalidation | probe | covered | performance.caching |
| Say when not to optimise | probe | covered | performance.when-not |
| Explain CPU-bound vs I/O-bound and which tool shows each | probe | covered | concurrency-depth.selection, performance.profiling |

## 15. Working with AI coding tools
| Item | Kind | Verdict | Leaf ids or reason |
|---|---|---|---|
| Specific prompts and context | topic | covered | ai.specs |
| Planning before coding | topic | covered | ai.decomposition |
| Verification: tests, checks, review of output | topic | covered | ai.verification |
| Persistent project guidance | topic | covered | ai.project-context |
| Permissions, sandboxing and guardrails | topic | covered | ai.risks |
| Tool and context connections: MCP | topic | GAP | ai.tools (connecting external tools and data to an agent; ai.project-context is instruction files and context cost only) |
| Reusable skills / workflows | topic | covered | ai.project-context (reusable procedures) |
| Knowing model limits | topic | covered | ai.failure-modes |
| Cost and context management | topic | covered | ai.project-context |
| Automation and parallel runs | topic | GAP | ai.automation (scripted and scheduled agent runs, parallel sessions, isolation between them) |
| Prompt an agent for a bug fix and verify it | probe | covered | ai.specs, ai.verification, rounds.ai-assisted |
| Review AI-generated code: hallucinated API, edge case, over-engineering | probe | covered | review.ai-code |
| Write the project instruction file for an agent | probe | covered | ai.project-context |
| Decide which tasks to delegate | probe | covered | ai.delegation |
| Specify acceptance checks the agent can run | probe | covered | ai.specs, ai.verification |
| Detect and fix a subtly wrong AI patch | probe | covered | ai.failure-modes, review.ai-code |
| Break a task into agent-sized steps | probe | covered | ai.decomposition |
| Explain risks: secrets, broad permissions, unreviewed code | probe | covered | ai.risks |

## Gaps
Proposed leaves. Branch in the first column; summaries match the voice of existing leaves.

| Proposed id | Branch | Title | Summary | Items it closes |
|---|---|---|---|---|
| fluency.style | fluency | 命名与风格规范（Naming, Style & Linters） | 变量、函数、类的命名惯例，PEP 8 与格式化器、linter 怎样把风格争论交给工具，以及什么时候该破例。 | area 1 naming topic; area 13 style-guides topic |
| python.metaprogramming | python | 描述符、属性与元编程（Descriptors & Metaprogramming） | `property`、描述符、`__init_subclass__`、元类和反射各解决什么问题，以及为什么面试里多数情况下应当拒绝它们。 | area 1 metaprogramming topic |
| data.abstraction-function | data | 抽象函数与表示独立（Abstraction Function） | 抽象函数把内部表示映射到抽象值，与表示不变量一起决定换一种实现时调用方为什么不受影响。 | area 2 abstraction-function topic |
| principles.responsibility | principles | 职责分配（Responsibility Assignment） | 一个行为该放在哪个类里：信息专家、高内聚、「告诉而不是询问」，以及职责放错的典型症状。 | area 4 responsibility topic |
| patterns.frameworks | patterns | 框架与类库（Frameworks vs Libraries） | 类库由你调用、框架调用你：控制反转、扩展点与模板方法钩子，以及怎样在框架约束里写扩展。 | area 4 frameworks topic |
| fsm.history | fsm | 历史状态（History States） | 离开复合状态后再回来时恢复上次的子状态：什么时候需要历史，用转移表怎么记录。 | area 5 history topic |
| concurrency-depth.parallel-scaling | concurrency-depth | 并行加速与锁竞争（Parallel Speedup & Contention） | 把算法切块并行（fork-join、分块归并）、阿姆达尔定律，以及锁竞争怎样吃掉加速比。 | area 6 parallelizing topic; area 14 scalability topic |
| errors.unrecoverable | errors | 不可恢复错误与顶层处理（Crash vs Recover） | 什么错误应当让进程崩溃、什么值得 recover，顶层处理器记录什么，panic 与 Result 的取舍。 | area 7 panic/recover topic |
| errors.exception-groups | errors | 异常组与附注（Exception Groups & Notes） | `ExceptionGroup`、`except*` 与 `add_note`：并发任务同时失败时怎样不丢任何一个错误。 | area 7 exception-groups topic |
| testing.box-testing | testing | 黑盒与白盒用例（Black-Box & Glass-Box） | 先按规格划分用例，再按代码分支补用例，两种视角各自漏掉什么。 | area 8 black/glass-box topic |
| parsing-io.dsl | parsing-io | 小语言设计（Little Languages） | 什么时候值得做一个小语言，内嵌 DSL 与外部语法的取舍，以及语法保持小的纪律。 | area 9 DSL topic |
| parsing-io.pattern-matcher | parsing-io | 手写通配与正则匹配器（Glob & Regex Matcher） | 递归回溯与动态规划两种写法实现 `*`、`?` 和基本正则，以及回溯爆炸的避免。 | area 9 matcher probe |
| reading.static-analysis | reading | 静态分析当作阅读工具（Static Analysis as a Reading Aid） | 用类型检查器、linter、调用图和死代码报告在不运行代码的情况下弄清结构。 | area 10 static-analysis topic |
| reading.famous-libraries | reading | 读名库的写法（Reading Famous Libraries） | 通读一个标准库或知名模块，指出它的接口形状、抽象选择和惯用法，带回自己的代码。 | area 10 famous-libraries topic |
| reading.predict-behaviour | reading | 预测输出与副作用（Predicting Behaviour） | 不运行就推演一段缠绕代码：别名、隐藏状态、求值顺序和默认参数怎样改变结果。 | area 10 predict-output probe |
| debugging.failure-origins | debugging | 追踪失败源头（Tracking Failure Origins） | 从错误的值往回找第一个出错的状态：感染链、反向切片，以及在哪一步设观察点。 | area 11 slicing topic |
| refactoring.rename | refactoring | 重命名与临时变量（Rename & Clarify） | 重命名、拆分变量、用查询替换临时变量：不改行为、只改可读性的最小重构。 | area 12 rename topic and probe |
| review.pushback | review | 回应评审与处理分歧（Handling Pushback） | 作者怎样回应评审意见，评审人怎样在分歧里守住底线又不僵持，以及何时升级。 | area 13 pushback topic and probe |
| performance.startup | performance | 启动时间与懒加载（Startup & Lazy Loading） | 导入成本的测量、延迟导入与惰性初始化，什么时候冷启动比稳态更要紧。 | area 14 startup topic |
| performance.native | performance | 把热点交给原生代码（Native Hot Paths） | 先用内建与 C 实现的标准库，再考虑 NumPy 向量化和扩展模块，以及何时不值得。 | area 14 native-code topic |
| ai.tools | ai | 接入工具与外部上下文（Tools & MCP） | 给 AI 接上外部工具与数据源：该接什么、权限给多大、怎样验证它真的用对了。 | area 15 MCP topic |
| ai.automation | ai | 自动化与并行运行（Automation & Parallel Runs） | 脚本化、定时和并行的 agent 运行：任务怎样隔离、结果怎样汇总核对，失败了怎么恢复。 | area 15 automation topic |

## Counts
Rows: 272; covered: 244; out-of-scope: 2; GAP: 26 (distinct gap leaves: 22)

## Resolution (orchestrator, 2026-11-08)

Added as leaves (12): python.metaprogramming, principles.responsibility, patterns.frameworks, fluency.style, concurrency-depth.parallel-scaling, errors.unrecoverable, parsing-io.pattern-matcher, reading.predict-behaviour, debugging.failure-origins, refactoring.rename, review.pushback, ai.tools-automation (merges the proposed ai.tools and ai.automation).

Merged into an existing leaf's summary (5): abstraction function into data.invariants; history states into fsm.hierarchical; exception groups into errors.chaining; black-box and glass-box into testing.partitioning; static analysis as a reading aid into reading.code-search.

Out of scope (4), each from one source and rarely probed: little languages (parsing-io.ast-eval teaches the mechanism); reading famous libraries (a study habit, not a probe); startup time and lazy loading; moving hot code to native extensions.

All 22 proposals are accounted for: 13 proposals became 12 leaves, 5 merged, 4 out of scope. The two earlier out-of-scope rows stand: actor model and review speed.

