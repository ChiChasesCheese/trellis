---
title: Runners
source: https://docs.python.org/3/library/asyncio-runner.html
corpus: python-docs
section: 34-asyncio-runner
clipped: '2026-09-21'
---

# Runners

# Runners[¶](#runners)

**Source code:** [Lib/asyncio/runners.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/runners.py)

This section outlines high-level asyncio primitives to run asyncio code.

They are built on top of an [event loop](asyncio-eventloop.html#asyncio-event-loop) with the aim
to simplify async code usage for common wide-spread scenarios.

## [Running an asyncio Program](#id1)[¶](#running-an-asyncio-program)

- 
asyncio.run(*coro* ,*** ,*debug=None* ,*loop_factory=None* )[¶](#asyncio.run)
- Execute *coro* in an asyncio event loop and return the result.The argument can be any awaitable object. This function runs the awaitable, taking care of managing the asyncio event loop, *finalizing asynchronous generators* , and
closing the executor.This function cannot be called when another asyncio event loop is running in the same thread. If *debug* is`True` , the event loop will be run in debug mode.`False` disables
debug mode explicitly.`None` is used to respect the global[Debug Mode](asyncio-dev.html#asyncio-debug-mode) settings.If *loop_factory* is not`None` , it is used to create a new event loop;
otherwise[`asyncio.new_event_loop()`](asyncio-eventloop.html#asyncio.new_event_loop) is used. The loop is closed at the end.
This function should be used as a main entry point for asyncio programs,
and should ideally only be called once. It is recommended to use*loop_factory* to configure the event loop instead of policies.
Passing[`asyncio.EventLoop`](asyncio-eventloop.html#asyncio.EventLoop) allows running asyncio without the
policy system.The executor is given a timeout duration of 5 minutes to shutdown. If the executor hasn’t finished within that duration, a warning is emitted and the executor is closed. Example: async def main(): await asyncio.sleep(1) print('hello') asyncio.run(main()) Added in version 3.7. Changed in version 3.9: Updated to use [`loop.shutdown_default_executor()`](asyncio-eventloop.html#asyncio.loop.shutdown_default_executor) .Changed in version 3.10: *debug* is`None` by default to respect the global debug mode settings.Changed in version 3.12: Added *loop_factory* parameter.Changed in version 3.14: *coro* can be any awaitable object.Note The `asyncio` policy system is deprecated and will be removed
in Python 3.16; from there on, an explicit*loop_factory* is needed
to configure the event loop.

## [Runner context manager](#id2)[¶](#runner-context-manager)

- 
*class* asyncio.Runner(*** ,*debug=None* ,*loop_factory=None* )[¶](#asyncio.Runner)
- A context manager that simplifies *multiple* async function calls in the same
context.Sometimes several top-level async functions should be called in the same [event
loop](asyncio-eventloop.html#asyncio-event-loop) and[`contextvars.Context`](contextvars.html#contextvars.Context) .If *debug* is`True` , the event loop will be run in debug mode.`False` disables
debug mode explicitly.`None` is used to respect the global[Debug Mode](asyncio-dev.html#asyncio-debug-mode) settings.*loop_factory* could be used for overriding the loop creation.
It is the responsibility of the*loop_factory* to set the created loop as the
current one. By default[`asyncio.new_event_loop()`](asyncio-eventloop.html#asyncio.new_event_loop) is used and set as
current event loop with[`asyncio.set_event_loop()`](asyncio-eventloop.html#asyncio.set_event_loop) if*loop_factory* is`None` .Basically, [`asyncio.run()`](#asyncio.run) example can be rewritten with the runner usage:async def main(): await asyncio.sleep(1) print('hello') with asyncio.Runner() as runner: runner.run(main()) Added in version 3.11. 
  - 
run(*coro* ,*** ,*context=None* )[¶](#asyncio.Runner.run)
  - Execute *coro* in the embedded event loop.The argument can be any awaitable object. If the argument is a coroutine, it is wrapped in a Task. An optional keyword-only *context* argument allows specifying a
custom[`contextvars.Context`](contextvars.html#contextvars.Context) for the code to run in.
The runner’s default context is used if context is`None` .Returns the awaitable’s result or raises an exception. This function cannot be called when another asyncio event loop is running in the same thread. Changed in version 3.14: *coro* can be any awaitable object.
 
  - 
close()[¶](#asyncio.Runner.close)
  - Close the runner. Finalize asynchronous generators, shutdown default executor, close the event loop and release embedded [`contextvars.Context`](contextvars.html#contextvars.Context) .
 
  - 
get_loop()[¶](#asyncio.Runner.get_loop)
  - Return the event loop associated with the runner instance.
 Note `Runner` uses the lazy initialization strategy, its constructor doesn’t
initialize underlying low-level structures.Embedded *loop* and*context* are created at the[`with`](../reference/compound_stmts.html#with) body entering
or the first call of[`run()`](#asyncio.run) or[`get_loop()`](#asyncio.Runner.get_loop) .
- 
run(

## [Handling Keyboard Interruption](#id3)[¶](#handling-keyboard-interruption)

Added in version 3.11.

When [`signal.SIGINT`](signal.html#signal.SIGINT) is raised by `Ctrl`-`C`, [`KeyboardInterrupt`](../builtins/exceptions.html#KeyboardInterrupt)
exception is raised in the main thread by default. However this doesn’t work with
[`asyncio`](asyncio.html#module-asyncio) because it can interrupt asyncio internals and can hang the program from
exiting.

To mitigate this issue, [`asyncio`](asyncio.html#module-asyncio) handles [`signal.SIGINT`](signal.html#signal.SIGINT) as follows:

1. [`asyncio.Runner.run()`](#asyncio.Runner.run) installs a custom[`signal.SIGINT`](signal.html#signal.SIGINT) handler before
any user code is executed and removes it when exiting from the function.
2. The [`Runner`](#asyncio.Runner) creates the main task for the passed coroutine for its
execution.
3. When [`signal.SIGINT`](signal.html#signal.SIGINT) is raised by`Ctrl` -`C` , the custom signal handler
cancels the main task by calling[`asyncio.Task.cancel()`](asyncio-task.html#asyncio.Task.cancel) which raises[`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError) inside the main task.  This causes the Python stack
to unwind,`try/except` and`try/finally` blocks can be used for resource
cleanup.  After the main task is cancelled,[`asyncio.Runner.run()`](#asyncio.Runner.run) raises[`KeyboardInterrupt`](../builtins/exceptions.html#KeyboardInterrupt) .
4. A user could write a tight loop which cannot be interrupted by [`asyncio.Task.cancel()`](asyncio-task.html#asyncio.Task.cancel) , in which case the second following`Ctrl` -`C` immediately raises the[`KeyboardInterrupt`](../builtins/exceptions.html#KeyboardInterrupt) without cancelling the main task.
