# 书籍 reading 子代理指令 · `python` domain（skill 第 6 步的"指针型"阅读）

> 你是 `sonnet` 子代理，不得再派生代理。你只拥有 `vault/domains/python/readings/` 下以你的前缀（启动消息里给）开头的文件。
> 这些书是商业书，仓库不存正文：reading 只是指针 + "读什么、带走什么"。标签必须含 `book` 和 `no-archive`（`book` 让 trellis 不把它算作可读源，`no-archive` 让 `clip` 跳过它）。

## 文件格式（照抄，一章一文件）

```markdown
---
nodes: [classes.inheritance-mro, classes.abc-protocols]
url: <出版社/作者页面 URL，见下>
tags: [book, no-archive]
title: Fluent Python 2e · 第 14 章 继承：为了更好或更坏
---
# Fluent Python 2e · 第 14 章 继承：为了更好或更坏

<2–3 句：这一章解决什么问题、为什么这一章值得读、它和这些叶子的关系。中文，术语英文。>

**读时提取：**
- <3–5 条：读完要能回答的具体问题或要能复述的机制；每条一句，带具体名词（C3、`super()`、mixin 约束）>

%% trellis:begin %%
## Source
[Open the original ↗](<同一个 URL>)
%% trellis:end %%
```

`nodes` 只能用 `skeleton/python.yaml` 里存在的叶子 id（先 `grep "id:" skeleton/python.yaml` 核对）。文件名：`<前缀>-<两位章号>-<slug>.md`，例如 `fluent-14-inheritance.md`。

## 章 → 叶子映射（起点；你读完各书目录后可微调，但每章至少一个叶子，每个叶子尽量被至少一本书覆盖）

### Fluent Python, 2e（Ramalho，O'Reilly 2022）— 前缀 `fluent`，URL `https://www.fluentpython.com/`（各章无单独公开 URL；全书用同一 URL，`title` 区分）
1 The Python Data Model → model.dunder-protocols, classes.pythonic-object · 2 An Array of Sequences → model.sequences, iteration.comprehensions · 3 Dictionaries and Sets → model.dict-set-internals, model.hash-eq · 4 Unicode Text versus Bytes → model.text-bytes · 5 Data Class Builders → classes.dataclasses · 6 Object References, Mutability, and Recycling → model.names-objects, model.mutability, model.copy, memory.refcounting, memory.weakref · 7 Functions as First-Class Objects → functions.first-class · 8 Type Hints in Functions → types.basics, types.gradual-typing · 9 Decorators and Closures → functions.scope-closure, functions.decorators, functions.decorator-patterns, functions.functools · 10 Design Patterns with First-Class Functions → functions.first-class · 11 A Pythonic Object → classes.pythonic-object · 12 Special Methods for Sequences → model.dunder-protocols, model.sequences · 13 Interfaces, Protocols, and ABCs → classes.abc-protocols · 14 Inheritance → classes.inheritance-mro · 15 More About Type Hints → types.protocols-generics, types.typeddict-literal · 16 Operator Overloading → classes.operator-overloading · 17 Iterators, Generators, and Classic Coroutines → iteration.iterator-protocol, iteration.generators, iteration.yield-from · 18 with, match, and else Blocks → iteration.context-managers, iteration.comprehensions · 19 Concurrency Models in Python → concurrency.gil, concurrency.threads, concurrency.multiprocessing, concurrency.choosing · 20 Concurrent Executors → concurrency.executors · 21 Asynchronous Programming → asyncio.event-loop, asyncio.coroutines-tasks, asyncio.gather-wait-timeout, asyncio.blocking-and-threads · 22 Dynamic Attributes and Properties → classes.attribute-lookup, classes.properties-descriptors · 23 Attribute Descriptors → classes.properties-descriptors · 24 Class Metaprogramming → classes.metaprogramming

### Effective Python, 3e（Slatkin，2024）— 前缀 `effective`，URL `https://effectivepython.com/`（按章一文件，正文列出该章里最值得读的条目号）
1 Pythonic Thinking → iteration.comprehensions · 2 Strings and Slicing → model.text-bytes, model.sequences · 3 Loops and Iterators → iteration.iterator-protocol, iteration.itertools · 4 Dictionaries → model.dict-set-internals, runtime.stdlib-map · 5 Functions → functions.arguments, functions.scope-closure, functions.decorators · 6 Comprehensions and Generators → iteration.generators, iteration.yield-from · 7 Classes and Interfaces → classes.pythonic-object, classes.dataclasses, classes.abc-protocols, classes.inheritance-mro · 8 Metaclasses and Attributes → classes.attribute-lookup, classes.properties-descriptors, classes.metaprogramming · 9 Concurrency and Parallelism → concurrency.threads, concurrency.locks-races, concurrency.queues, concurrency.executors, asyncio.blocking-and-threads · 10 Robustness → runtime.exceptions, engineering.robustness, iteration.context-managers · 11 Performance → performance.profiling, performance.compiling, runtime.compile-bytecode · 12 Data Structures and Algorithms → runtime.stdlib-map, engineering.money-time, engineering.serialization, performance.containers · 13 Testing and Debugging → engineering.testing, memory.leaks-tracemalloc · 14 Collaboration → engineering.packaging-env, runtime.import-system, engineering.logging-config, types.gradual-typing

### High Performance Python, 2e（Gorelick & Ozsvald，O'Reilly 2020）— 前缀 `hpp`，URL `https://www.oreilly.com/library/view/high-performance-python/9781492055013/`
1 Understanding Performant Programming → performance.profiling · 2 Profiling → performance.profiling, memory.leaks-tracemalloc · 3 Lists and Tuples → performance.containers, model.sequences · 4 Dictionaries and Sets → model.dict-set-internals, performance.containers · 5 Iterators and Generators → iteration.generators, performance.less-ram · 6 Matrix and Vector Computation → performance.numpy-vectorization · 7 Compiling to C → performance.compiling · 8 Asynchronous I/O → asyncio.event-loop, concurrency.choosing · 9 The multiprocessing Module → concurrency.multiprocessing, concurrency.executors · 10 Clusters and Job Queues → concurrency.choosing · 11 Using Less RAM → memory.object-size, performance.less-ram, memory.allocator · 12 Lessons from the Field → performance.pandas-at-scale

### Python Concurrency with asyncio（Fowler，Manning 2022）— 前缀 `fowler`，URL `https://www.manning.com/books/python-concurrency-with-asyncio`
1 Getting to know asyncio → concurrency.gil, concurrency.choosing, asyncio.event-loop · 2 asyncio basics（coroutines, tasks, futures, debug）→ asyncio.coroutines-tasks, asyncio.futures, asyncio.cancellation, asyncio.debugging · 3 A first asyncio application（sockets, event loop）→ asyncio.event-loop, asyncio.streams-protocols · 4 Concurrent web requests（gather, as_completed, timeouts）→ asyncio.gather-wait-timeout · 5 Non-blocking database drivers → asyncio.sync-primitives · 6 Handling CPU-bound work（process pools with asyncio）→ asyncio.blocking-and-threads, concurrency.multiprocessing · 7 Handling blocking work with threads → asyncio.blocking-and-threads, concurrency.threads · 8 Streams → asyncio.streams-protocols · 11 Synchronization → asyncio.sync-primitives, concurrency.locks-races · 12 Asynchronous queues → asyncio.sync-primitives, concurrency.queues · 14 Advanced asyncio（custom awaitables, event loop internals）→ asyncio.futures, asyncio.event-loop（章号按该书目录；9/10/13 与面试无关，跳过）

### CPython Internals（Shaw，Real Python 2021）— 前缀 `cpyint`，URL `https://realpython.com/products/cpython-internals-book/`
The Compiler / Lexing and Parsing → runtime.compile-bytecode · The Evaluation Loop → runtime.frames-eval, runtime.adaptive-jit · Memory Management → memory.refcounting, memory.cyclic-gc, memory.allocator, memory.object-size · Parallelism and Concurrency → concurrency.gil, concurrency.threads, concurrency.multiprocessing, asyncio.event-loop · Objects and Types → model.dict-set-internals, model.names-objects, memory.interning-immortal · Debugging / Benchmarking → performance.profiling

## 硬规则
- 中文正文；不复述整章内容，只写"为什么读、带走什么"；不编造章节里没有的具体数字。
- 每个文件写完后运行一次 `uv run trellis --domain python validate`，最后一行必须 0 errors；有 reading 相关错误（未知 node id、frontmatter 键）立即修。
- 最终回复：文件数、各书章数、validate 最后一行。
