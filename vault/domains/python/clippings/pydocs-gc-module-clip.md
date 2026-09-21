---
title: gc — Garbage Collector interface
source: https://docs.python.org/3/library/gc.html
corpus: python-docs
section: 39-gc
clipped: '2026-09-21'
---

# gc — Garbage Collector interface

# `gc` — Garbage Collector interface[¶](#module-gc)

This module provides an interface to the optional garbage collector.  It
provides the ability to disable the collector, tune the collection frequency,
and set debugging options.  It also provides access to unreachable objects that
the collector found but cannot free.  Since the collector supplements the
reference counting already used in Python, you can disable the collector if you
are sure your program does not create reference cycles.  Automatic collection
can be disabled by calling `gc.disable()`.  To debug a leaking program call
`gc.set_debug(gc.DEBUG_LEAK)`. Notice that this includes
`gc.DEBUG_SAVEALL`, causing garbage-collected objects to be saved in
gc.garbage for inspection.

The `gc` module provides the following functions:

- 
gc.enable()[¶](#gc.enable)
- Enable automatic garbage collection.

- 
gc.disable()[¶](#gc.disable)
- Disable automatic garbage collection.

- 
gc.isenabled()[¶](#gc.isenabled)
- Return `True` if automatic collection is enabled.

- 
gc.collect(*generation=2* )[¶](#gc.collect)
- With no arguments, run a full collection. The optional argument *generation* may be an integer specifying which generation to collect (from 0 to 2).  A[`ValueError`](../builtins/exceptions.html#ValueError) is raised if the generation number is invalid. The sum of
collected objects and uncollectable objects is returned.The free lists maintained for a number of built-in types are cleared whenever a full collection or collection of the highest generation (2) is run. Not all items in some free lists may be freed due to the particular implementation, in particular [`float`](../builtins/functions.html#float) .The effect of calling `gc.collect()` while the interpreter is already
performing a collection is undefined.Changed in version 3.14: `generation=1` performs an increment of collection.Changed in version 3.14.5: `generation=1` performs collection of the middle generation.

- 
gc.set_debug(*flags* )[¶](#gc.set_debug)
- Set the garbage collection debugging flags. Debugging information will be written to `sys.stderr` .  See below for a list of debugging flags which can be
combined using bit operations to control debugging.

- 
gc.get_debug()[¶](#gc.get_debug)
- Return the debugging flags currently set.

- 
gc.get_objects(*generation=None* )[¶](#gc.get_objects)
- Returns a list of all objects tracked by the collector, excluding the list returned. If *generation* is not`None` , return only the objects tracked by
the collector that are in that generation.Changed in version 3.8: New *generation* parameter.Changed in version 3.14: Generation 1 is removed Changed in version 3.14.5: Generation 1 is reintroduced to maintain GC behavior from 3.13. Raises an [auditing event](sys.html#auditing)`gc.get_objects` with argument`generation` .

- 
gc.get_stats()[¶](#gc.get_stats)
- Return a list of three per-generation dictionaries containing collection statistics since interpreter start. The number of keys may change in the future, but currently each dictionary will contain the following items: 
  - `collections` is the number of times this generation was collected;
  - `collected` is the total number of objects collected inside this
generation;
  - `uncollectable` is the total number of objects which were found
to be uncollectable (and were therefore moved to the[`garbage`](#gc.garbage) list) inside this generation.
 Added in version 3.4.

- 
gc.set_threshold(*threshold0* [,*threshold1* [,*threshold2* ]])[¶](#gc.set_threshold)
- Set the garbage collection thresholds (the collection frequency). Setting *threshold0* to zero disables collection.The GC classifies objects into three generations depending on how many collection sweeps they have survived. New objects are placed in the youngest generation (generation `0` ).  If an object survives a collection it is moved
into the next older generation.  Since generation`2` is the oldest
generation, objects in that generation remain there after a collection.  In
order to decide when to run, the collector keeps track of the number object
allocations and deallocations since the last collection.  When the number of
allocations minus the number of deallocations exceeds*threshold0* , collection
starts.  Initially only generation`0` is examined.  If generation`0` has
been examined more than*threshold1* times since generation`1` has been
examined, then generation`1` is examined as well.
With the third generation, things are a bit more complicated,
see[Collecting the oldest generation](https://github.com/python/cpython/blob/ff0ef0a54bef26fc507fbf9b7a6009eb7d3f17f5/InternalDocs/garbage_collector.md#collecting-the-oldest-generation) for more information.In the free-threaded build, the increase in process memory usage is also checked before running the collector. If the memory usage has not increased by 10% since the last collection and the net number of object allocations has not exceeded 40 times *threshold0* , the collection is not run.See [Garbage collector design](https://github.com/python/cpython/blob/3.14/InternalDocs/garbage_collector.md) for more information.Changed in version 3.14: *threshold2* is ignoredChanged in version 3.14.5: *threshold2* is restored to match Python 3.13 behavior.

- 
gc.get_count()[¶](#gc.get_count)
- Return the current collection counts as a tuple of ```
(count0, count1,
count2)
```
.

- 
gc.get_threshold()[¶](#gc.get_threshold)
- Return the current collection thresholds as a tuple of ```
(threshold0,
threshold1, threshold2)
```
.

- 
gc.get_referrers(**objs* )[¶](#gc.get_referrers)
- Return the list of objects that directly refer to any of objs. This function will only locate those containers which support garbage collection; extension types which do refer to other objects but do not support garbage collection will not be found. Note that objects which have already been dereferenced, but which live in cycles and have not yet been collected by the garbage collector can be listed among the resulting referrers. To get only currently live objects, call [`collect()`](#gc.collect) before calling`get_referrers()` .Warning Care must be taken when using objects returned by `get_referrers()` because
some of them could still be under construction and hence in a temporarily
invalid state. Avoid using`get_referrers()` for any purpose other than
debugging.Raises an [auditing event](sys.html#auditing)`gc.get_referrers` with argument`objs` .

- 
gc.get_referents(**objs* )[¶](#gc.get_referents)
- Return a list of objects directly referred to by any of the arguments. The referents returned are those objects visited by the arguments’ C-level [`tp_traverse`](../c-api/typeobj.html#c.PyTypeObject.tp_traverse) methods (if any), and may not be all objects actually
directly reachable.`tp_traverse` methods are supported only by objects
that support garbage collection, and are only required to visit objects that may
be involved in a cycle.  So, for example, if an integer is directly reachable
from an argument, that integer object may or may not appear in the result list.Raises an [auditing event](sys.html#auditing)`gc.get_referents` with argument`objs` .

- 
gc.is_tracked(*obj* )[¶](#gc.is_tracked)
- Returns `True` if the object is currently tracked by the garbage collector,`False` otherwise.  As a general rule, instances of atomic types aren’t
tracked and instances of non-atomic types (containers, user-defined
objects…) are.  However, some type-specific optimizations can be present
in order to suppress the garbage collector footprint of simple instances
(e.g. dicts containing only atomic keys and values):>>> gc.is_tracked(0) False >>> gc.is_tracked("a") False >>> gc.is_tracked([]) True >>> gc.is_tracked({}) False >>> gc.is_tracked({"a": 1}) True Added in version 3.1.

- 
gc.is_finalized(*obj* )[¶](#gc.is_finalized)
- Returns `True` if the given object has been finalized by the
garbage collector,`False` otherwise.>>> x = None >>> class Lazarus: ... def __del__(self): ... global x ... x = self ... >>> lazarus = Lazarus() >>> gc.is_finalized(lazarus) False >>> del lazarus >>> gc.is_finalized(x) True Added in version 3.9.

- 
gc.freeze()[¶](#gc.freeze)
- Freeze all the objects tracked by the garbage collector; move them to a permanent generation and ignore them in all the future collections. If a process will `fork()` without`exec()` , avoiding unnecessary
copy-on-write in child processes will maximize memory sharing and reduce
overall memory usage. This requires both avoiding creation of freed “holes”
in memory pages in the parent process and ensuring that GC collections in
child processes won’t touch the`gc_refs` counter of long-lived objects
originating in the parent process. To accomplish both, call`gc.disable()` early in the parent process,`gc.freeze()` right before`fork()` , and`gc.enable()` early in child processes.Added in version 3.7.

- 
gc.unfreeze()[¶](#gc.unfreeze)
- Unfreeze the objects in the permanent generation, put them back into the oldest generation. Added in version 3.7.

- 
gc.get_freeze_count()[¶](#gc.get_freeze_count)
- Return the number of objects in the permanent generation. Added in version 3.7.

The following variables are provided for read-only access (you can mutate the values but should not rebind them):

- 
gc.garbage[¶](#gc.garbage)
- A list of objects which the collector found to be unreachable but could not be freed (uncollectable objects). Starting with Python 3.4, this list should be empty most of the time, except when using instances of C extension types with a non- `NULL``tp_del` slot.If [`DEBUG_SAVEALL`](#gc.DEBUG_SAVEALL) is set, then all unreachable objects will be
added to this list rather than freed.Changed in version 3.2: If this list is non-empty at [interpreter shutdown](../glossary.html#term-interpreter-shutdown) , a[`ResourceWarning`](../builtins/exceptions.html#ResourceWarning) is emitted, which is silent by default.  If[`DEBUG_UNCOLLECTABLE`](#gc.DEBUG_UNCOLLECTABLE) is set, in addition all uncollectable objects
are printed.

- 
gc.callbacks[¶](#gc.callbacks)
- A list of callbacks that will be invoked by the garbage collector before and after collection. The callbacks will be called with two arguments, *phase* and*info* .*phase* can be one of two values:“start”: The garbage collection is about to start. “stop”: The garbage collection has finished. *info* is a dict providing more information for the callback.  The following
keys are currently defined:“generation”: The oldest generation being collected. “collected”: When *phase* is “stop”, the number of objects
successfully collected.“uncollectable”: When *phase* is “stop”, the number of objects
that could not be collected and were put in[`garbage`](#gc.garbage) .Applications can add their own callbacks to this list. The primary use cases are: Gathering statistics about garbage collection, such as how often various generations are collected, and how long the collection takes. Allowing applications to identify and clear their own uncollectable types when they appear in [`garbage`](#gc.garbage) .Added in version 3.3.

The following constants are provided for use with [`set_debug()`](#gc.set_debug):

- 
gc.DEBUG_STATS[¶](#gc.DEBUG_STATS)
- Print statistics during collection. This information can be useful when tuning the collection frequency.

- 
gc.DEBUG_COLLECTABLE[¶](#gc.DEBUG_COLLECTABLE)
- Print information on collectable objects found.

- 
gc.DEBUG_UNCOLLECTABLE[¶](#gc.DEBUG_UNCOLLECTABLE)
- Print information of uncollectable objects found (objects which are not reachable but cannot be freed by the collector). These objects will be added to the `garbage` list.Changed in version 3.2: Also print the contents of the [`garbage`](#gc.garbage) list at[interpreter shutdown](../glossary.html#term-interpreter-shutdown) , if it isn’t empty.

- 
gc.DEBUG_SAVEALL[¶](#gc.DEBUG_SAVEALL)
- When set, all unreachable objects found will be appended to *garbage* rather
than being freed.  This can be useful for debugging a leaking program.

- 
gc.DEBUG_LEAK[¶](#gc.DEBUG_LEAK)
- The debugging flags necessary for the collector to print information about a leaking program (equal to ```
DEBUG_COLLECTABLE | DEBUG_UNCOLLECTABLE |
DEBUG_SAVEALL
```
).
