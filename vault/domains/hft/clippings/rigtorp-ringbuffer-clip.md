---
title: Optimizing a ring buffer for throughput
source: https://rigtorp.se/ringbuffer/
author: Erik Rigtorp
published: '2021-12-13'
site: Rigtorp
clipped: '2026-10-23'
---

# Optimizing a ring buffer for throughput

# Optimizing a ring buffer for throughput

In this article I will take a look at the classic concurrent ring buffer and how
it can be optimized to increase throughput. I will show you how to significantly
increase throughput from 5.5M items/s to 112M items/s, beating the
[Boost](https://www.boost.org/) and [Folly](https://github.com/facebook/folly)
implementations. If you need a ready implementation with these optimizations
checkout my [*SPSCQueue.h* library](https://github.com/rigtorp/SPSCQueue).

The ringer buffer data structure is also referred to as a circular buffer or
single producer single consumer (SPSC) queue. It’s a wait-free (hence also
lock-free) concurrency primitive. It has a lot of uses for example it’s used to
communicate network packets between NICs and OS drivers and to receive I/O
completion events in the recently introduced
[*io_uring*](https://lwn.net/Articles/776703/) asynchronous I/O API.

## The classic ring buffer

First let’s start by implementing a simple ring buffer. In C++ it can be defined like this:

```
struct ringbuffer {
  std::vector<int> data_;
  alignas(64) std::atomic<size_t> readIdx_{0};
  alignas(64) std::atomic<size_t> writeIdx_{0};
  ringbuffer(size_t capacity) : data_(capacity, 0) {}
}
```
In this implementation I chose to allow any queue size as opposed to allowing only sizes that are a power-of-two. This means that at least one queue item is unused in order to disambiguate between the empty queue and full queue state. You can choose to require a power-of-two size to avoid this if memory is at a premium.

Another important thing to note is that read (`readIdx_`) and write
(`writeIdx_`) indices are aligned to the size of a cache line (`alignas(64)`).
This is done to reduce cache coherency traffic. On AMD64 / x86_64 and ARM a
cache line is 64 bytes, on other CPUs you need to adjust to the appropriate
alignment, using
[`std::hardware_destructive_interference_size`](https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size)
is a good choice if it’s available. It can also be interesting to try aligning
to a multiple of the cache line size in case adjacent cache lines are being
pre-fetched.

This is quite similar to how *io_uring* defines its ring buffer inside the Linux
kernel:

```
struct io_uring {
  u32 head ____cacheline_aligned_in_smp;
  u32 tail ____cacheline_aligned_in_smp;
};
```
[*boost::lockfree::spsc*](https://www.boost.org/doc/libs/1_76_0/doc/html/boost/lockfree/spsc_queue.html)
also defines it’s ring buffer in pretty much the same way.

We can now implement the push (or write) operation:

```
bool push(int val) {
  auto const writeIdx = writeIdx_.load(std::memory_order_relaxed);
  auto nextWriteIdx = writeIdx + 1;
  if (nextWriteIdx == data_.size()) {
    nextWriteIdx = 0;
  }
  if (nextWriteIdx == readIdx_.load(std::memory_order_acquire)) {
    return false;
  }
  data_[writeIdx] = val;
  writeIdx_.store(nextWriteIdx, std::memory_order_release);
  return true;
}
```
Note how one item is left unused to indicate that the queue is full, when
`writeIdx_` is one item behind `readIdx_` the queue is full.

Next we implement the pop (or read) operation:

```
bool pop(int &val) {
  auto const readIdx = readIdx_.load(std::memory_order_relaxed);
  if (readIdx == writeIdx_.load(std::memory_order_acquire)) {
    return false;
  }
  val = data_[readIdx];
  auto nextReadIdx = readIdx + 1;
  if (nextReadIdx == data_.size()) {
    nextReadIdx = 0;
  }
  readIdx_.store(nextReadIdx, std::memory_order_release);
  return true;
}
```
Again note that `readIdx_ == writeIdx_` indicates that the queue is empty.

I chose a very small item size (`sizeof(int) == 4`) since for large item sizes
the performance will be dominated by the memory copying of the items and the
goal is not to measure the performance of `memcpy()`. This of course also means
that if you have large items you don’t have much to gain from optimizing your
ring buffer.

Now lets analyze the performance of this queue. I wrote [a simple benchmark
`ringbuffer.cpp`](/ringbuffer.cpp) that pushes 100M items between 2 threads
through a ring buffer of size 100k. Measuring how long it takes until the reader
thread has read all items. Compile [`ringbuffer.cpp`](/ringbuffer.cpp) as
follows:

```
g++ -Wall -O3 -march=native -std=c++20 ringbuffer.cpp
```
I ran this on a AMD Ryzen 9 3900X 12-Core Processor placing the two threads on different chiplets / core complexes (CCX):

```
$ perf stat -e cache-misses,cache-references,l2_request_g1.change_to_x ./a.out 1 11
5513850 ops/s
 Performance counter stats for './a.out 1 11':
       349,857,603      cache-misses:u            #   91.228 % of all cache refs    
       383,497,078      cache-references:u                                          
         6,673,242      l2_request_g1.change_to_x:u                                   
      18.137421039 seconds time elapsed
      36.140630000 seconds user
       0.002986000 seconds sys
```
We see here that we achieved a throughput of 5.5M items per second. This is in
line with the performance you will see from libraries such as
[*boost::lockfree::spsc*](https://www.boost.org/doc/libs/1_76_0/doc/html/boost/lockfree/spsc_queue.html)
and
[*folly::ProducerConsumerQueue*](https://github.com/facebook/folly/blob/master/folly/docs/ProducerConsumerQueue.md).
The number of cache misses (~300M) seems to be proportional (3x) to the number
of items (100M) that were processed.

## The optimized ring buffer

Why do we have 3 cache misses per read-write pair? Consider a read operation:
the read index needs to be updated and thus that cache line is loaded into the
L1 cache in exclusive state (see [MESI
protocol](https://en.wikipedia.org/wiki/MESI_protocol)). The write index needs
to be read in order to check that the queue is not empty and is thus loaded into
the L1 cache in shared state. Since a queue write operation needs to read the
read index it causes the reader’s read index cache line to be evicted or
transition into shared state. Now the read operation requires some cache
coherency traffic to bring the read index cache line back into exclusive state.
In turn a write operation will require some cache coherency traffic to bring the
write index cache line back into exclusive state. In the worst case there will
be one cache line transition from shared to exclusive for every read and write
operation. These cache line state transitions are counted as cache misses. We
don’t know the exact implementation details of the cache coherency protocol, but
it will behave roughly as the MESI protocol.

To reduce the amount of coherency traffic the reader and writer can keep a
cached copy of the write and read index respectively. In this case when a reader
first observes that *N* items are available to read, it caches this information
and the *N-1* subsequent reads won’t need to read the write index. Similarly
when a writer first observes that *N* items are available for writing, it caches
this information and the *N-1* subsequent writes won’t need to read the read
index.

The new ring buffer is defined as follows:

```
struct ringbuffer2 {
  std::vector<int> data_{};
  alignas(64) std::atomic<size_t> readIdx_{0};
  alignas(64) size_t writeIdxCached_{0};
  alignas(64) std::atomic<size_t> writeIdx_{0};
  alignas(64) size_t readIdxCached_{0};
  ringbuffer2(size_t capacity) : data_(capacity, 0) {}
}
```
The push operation is updated to first consult the cached read index
(`readIdxCached_`) and if that fails retry after updating the cache:

```
if (nextWriteIdx == readIdxCached_) {
  readIdxCached_ = readIdx_.load(std::memory_order_acquire);
  if (nextWriteIdx == readIdxCached_) {
    return false;
  }
}
```
The pop operation is updated in a similar way to first consult the cached write
index (`writeIdxCached_`):

```
if (readIdx == writeIdxCached_) {
  writeIdxCached_ = writeIdx_.load(std::memory_order_acquire);
  if (readIdx == writeIdxCached_) {
    return false;
  }
}
```
Re-running the same benchmark as before with the new ring buffer implementation:

```
$ perf stat -e cache-misses,cache-references,l2_request_g1.change_to_x ./a.out 1 11
112287037 ops/s
 Performance counter stats for './a.out 1 11':
        15,010,392      cache-misses:u            #   32.553 % of all cache refs    
        46,110,663      cache-references:u                                          
         6,781,273      l2_request_g1.change_to_x:u                                   
       0.892256380 seconds time elapsed
       1.775185000 seconds user
       0.000996000 seconds sys
```
Wow this is great! Throughput is now 112M items per second and the number of
cache misses was significantly reduced. Checkout
[`ringbuffer.cpp`](/ringbuffer.cpp) if you want to verify this yourself.

## Further optimizations

Supporting batched push and pop operations can reduce the number of times the read and write indices needs to be updated to less than once per item.

Using huge pages for the ring buffer backing memory can reduce TLB misses.
