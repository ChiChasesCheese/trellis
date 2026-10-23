---
title: Seqlock - Wikipedia
source: https://en.wikipedia.org/wiki/Seqlock
published: '2006-02-12'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Seqlock - Wikipedia

# Seqlock

A **seqlock** (short for *sequence lock*) is a special [locking](<https://en.wikipedia.org/wiki/Lock_(computer)>) mechanism used in [Linux](https://en.wikipedia.org/wiki/Linux) for supporting fast writes of shared variables between two parallel [operating system](https://en.wikipedia.org/wiki/Operating_system) routines. The semantics stabilized as of version 2.5.59, and they are present in the 2.6.x stable kernel series. The seqlocks were developed by Stephen Hemminger  and originally called frlocks, based on earlier work by Andrea Arcangeli. The first implementation was in the x86-64 time code where it was needed to synchronize with user space where it was not possible to use a real lock.

It is a [reader–writer](https://en.wikipedia.org/wiki/Readers–writers_problem) consistent mechanism which avoids the problem of [writer starvation](https://en.wikipedia.org/wiki/Readers–writer_lock). A seqlock consists of storage for saving a sequence number in addition to a lock. The lock is to support synchronization between two writers and the counter is for indicating consistency in readers. In addition to updating the shared data, the writer increments the sequence number, both after acquiring the lock and before releasing the lock. Readers read the sequence number before and after reading the shared data. If the sequence number is odd on either occasion, a writer had taken the lock while the data was being read and it may have changed. If the sequence numbers are different, a writer has changed the data while it was being read. In either case readers simply retry (using a loop) until they read the same even sequence number before and after.

The reader never blocks, but it may have to retry if a write is in progress; this speeds up the readers in the case where the data was not modified, since they do not have to acquire the lock as they would with a traditional read–write lock.  Also, writers do not wait for readers, whereas with traditional read–write locks they do, leading to potential resource starvation in a situation where there are a number of readers (because the writer must wait for there to be no readers).  Because of these two factors, seqlocks are more efficient than traditional [read–write locks](https://en.wikipedia.org/wiki/Readers–writer_lock) for the situation where there are many readers and few writers. The drawback is that if there is too much write activity or the reader is too slow, they might [livelock](https://en.wikipedia.org/wiki/Livelock) (and the readers may starve).

The technique will not work for data that contains pointers, because any writer could invalidate a pointer that a reader has already followed. Updating the memory block being *pointed-to* is fine using seqlocks, but updating the *pointer itself* is not allowed. In a case where the pointers themselves must be updated or changed, using [read-copy-update](https://en.wikipedia.org/wiki/Read-copy-update) synchronization is preferred.

This was first applied to system time counter updating. Each time interrupt updates the time of the day; there may be many readers of the time for operating system internal use and applications, but writes are relatively infrequent and only occur one at a time. The BSD timecounter code for instance appears to use a similar technique.

One subtle issue of using seqlocks for a time counter is that it is impossible to step through it with a debugger. The retry logic will trigger all the time because the debugger is slow enough to make the read race occur always.

## See also

[
[edit](/w/index.php?title=Seqlock&action=edit§ion=1)]

## References

[
[edit](/w/index.php?title=Seqlock&action=edit§ion=2)]
