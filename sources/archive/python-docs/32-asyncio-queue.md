---
title: Queues
corpus: python-docs
section: 32-asyncio-queue
level: 1
locator: https://docs.python.org/3/library/asyncio-queue.html
license: free-online
fetched: '2026-09-21'
---

# Queues[¶](#queues)

**Source code:** [Lib/asyncio/queues.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/queues.py)

asyncio queues are designed to be similar to classes of the
[`queue`](queue.html#module-queue) module.  Although asyncio queues are not thread-safe,
they are designed to be used specifically in async/await code.

Note that methods of asyncio queues don’t have a *timeout* parameter;
use [`asyncio.wait_for()`](asyncio-task.html#asyncio.wait_for) function to do queue operations with a
timeout.

See also the [Examples](#examples) section below.

## Queue[¶](#queue)

- 
*class* asyncio.Queue(*maxsize=0* )[¶](#asyncio.Queue)
- A first in, first out (FIFO) queue. If *maxsize* is less than or equal to zero, the queue size is
infinite.  If it is an integer greater than`0` , then`await put()` blocks when the queue reaches*maxsize* until an item is removed by[`get()`](#asyncio.Queue.get) .Unlike the standard library threading [`queue`](queue.html#module-queue) , the size of
the queue is always known and can be returned by calling the[`qsize()`](#asyncio.Queue.qsize) method.Changed in version 3.10: Removed the *loop* parameter.This class is [not thread safe](asyncio-dev.html#asyncio-multithreading) .
  - 
maxsize[¶](#asyncio.Queue.maxsize)
  - Number of items allowed in the queue.
 
  - 
empty()[¶](#asyncio.Queue.empty)
  - Return `True` if the queue is empty,`False` otherwise.
 
  - 
full()[¶](#asyncio.Queue.full)
  - Return `True` if there are[`maxsize`](#asyncio.Queue.maxsize) items in the queue.If the queue was initialized with `maxsize=0` (the default),
then`full()` never returns`True` .
 
  - 
*async* get()[¶](#asyncio.Queue.get)
  - Remove and return an item from the queue. If queue is empty, wait until an item is available. Raises [`QueueShutDown`](#asyncio.QueueShutDown) if the queue has been shut down and
is empty, or if the queue has been shut down immediately.
 
  - 
get_nowait()[¶](#asyncio.Queue.get_nowait)
  - Return an item if one is immediately available, else raise [`QueueEmpty`](#asyncio.QueueEmpty) .Raises [`QueueShutDown`](#asyncio.QueueShutDown) if the queue has been shut down and is empty.
 
  - 
*async* join()[¶](#asyncio.Queue.join)
  - Block until all items in the queue have been received and processed. The count of unfinished tasks goes up whenever an item is added to the queue. The count goes down whenever a consumer coroutine calls [`task_done()`](#asyncio.Queue.task_done) to indicate that the item was retrieved and all
work on it is complete.  When the count of unfinished tasks drops
to zero,`join()` unblocks.
 
  - 
*async* put(*item* )[¶](#asyncio.Queue.put)
  - Put an item into the queue. If the queue is full, wait until a free slot is available before adding the item. Raises [`QueueShutDown`](#asyncio.QueueShutDown) if the queue has been shut down.
 
  - 
put_nowait(*item* )[¶](#asyncio.Queue.put_nowait)
  - Put an item into the queue without blocking. If no free slot is immediately available, raise [`QueueFull`](#asyncio.QueueFull) .Raises [`QueueShutDown`](#asyncio.QueueShutDown) if the queue has been shut down.
 
  - 
qsize()[¶](#asyncio.Queue.qsize)
  - Return the number of items in the queue.
 
  - 
shutdown(*immediate=False* )[¶](#asyncio.Queue.shutdown)
  - Put a `Queue` instance into a shutdown mode.The queue can no longer grow. Future calls to [`put()`](#asyncio.Queue.put) raise[`QueueShutDown`](#asyncio.QueueShutDown) .
Currently blocked callers of`put()` will be unblocked
and will raise`QueueShutDown` in the formerly awaiting task.If *immediate* is false (the default), the queue can be wound
down normally with[`get()`](#asyncio.Queue.get) calls to extract tasks
that have already been loaded.And if [`task_done()`](#asyncio.Queue.task_done) is called for each remaining task, a
pending[`join()`](#asyncio.Queue.join) will be unblocked normally.Once the queue is empty, future calls to [`get()`](#asyncio.Queue.get) will
raise[`QueueShutDown`](#asyncio.QueueShutDown) .If *immediate* is true, the queue is terminated immediately.
The queue is drained to be completely empty and the count
of unfinished tasks is reduced by the number of tasks drained.
If unfinished tasks is zero, callers of[`join()`](#asyncio.Queue.join) are unblocked.  Also, blocked callers of[`get()`](#asyncio.Queue.get) are unblocked and will raise[`QueueShutDown`](#asyncio.QueueShutDown) because the
queue is empty.Use caution when using [`join()`](#asyncio.Queue.join) with*immediate* set
to true. This unblocks the join even when no work has been done
on the tasks, violating the usual invariant for joining a queue.Added in version 3.13.
 
  - 
task_done()[¶](#asyncio.Queue.task_done)
  - Indicate that a formerly enqueued work item is complete. Used by queue consumers. For each [`get()`](#asyncio.Queue.get) used to
fetch a work item, a subsequent call to`task_done()` tells the
queue that the processing on the work item is complete.If a [`join()`](#asyncio.Queue.join) is currently blocking, it will resume when all
items have been processed (meaning that a`task_done()` call was received for every item that had been[`put()`](#asyncio.Queue.put) into the queue).Raises [`ValueError`](../builtins/exceptions.html#ValueError) if called more times than there were
items placed in the queue.
- 
maxsize

## Priority Queue[¶](#priority-queue)

## LIFO Queue[¶](#lifo-queue)

## Exceptions[¶](#exceptions)

- 
*exception* asyncio.QueueEmpty[¶](#asyncio.QueueEmpty)
- This exception is raised when the [`get_nowait()`](#asyncio.Queue.get_nowait) method
is called on an empty queue.

- 
*exception* asyncio.QueueFull[¶](#asyncio.QueueFull)
- Exception raised when the [`put_nowait()`](#asyncio.Queue.put_nowait) method is called
on a queue that has reached its*maxsize* .

- 
*exception* asyncio.QueueShutDown[¶](#asyncio.QueueShutDown)
- Exception raised when [`put()`](#asyncio.Queue.put) ,[`put_nowait()`](#asyncio.Queue.put_nowait) ,[`get()`](#asyncio.Queue.get) or[`get_nowait()`](#asyncio.Queue.get_nowait) is called
on a queue which has been shut down.Added in version 3.13.

## Examples[¶](#examples)

Queues can be used to distribute workload between several concurrent tasks:

```
import asyncio
import random
import time
async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()
        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)
        # Notify the queue that the "work item" has been processed.
        queue.task_done()
        print(f'{name} has slept for {sleep_for:.2f} seconds')
async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()
    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)
    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)
    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at
    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)
    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')
asyncio.run(main())
```
