---
title: Latency implications of virtual memory
source: https://rigtorp.se/virtual-memory/
author: Erik Rigtorp
published: '2020-07-09'
site: Rigtorp
clipped: '2026-10-23'
---

# Latency implications of virtual memory

# Latency implications of virtual memory

This is a short guide describing the latency implications of the virtual memory abstraction. If you are building systems requiring low and predictable latency such as realtime audio processing, control and high frequency trading (HFT) / algorithmic trading systems this guide will be useful to you. It is written from the perspective Linux kernel running on AMD64 / x86-64 architecture, but the general concepts applies to most operating systems and CPU architectures.

In summary to minimize latency introduced by the virtual memory abstraction you should:

- Minimize page faults by pre-faulting, locking and pre-allocating needed memory. Disable swap.
- Reduce TLB misses by minimizing your working set memory and utilizing huge pages.
- Prevent TLB shootdowns by not modifying your programs page tables after startup.
- Prevent stalls due to page cache writeback by not creating file backed writable memory mappings.
- Disable Linux transparent huge pages (THP).
- Disable Linux kernel samepage merging (KSM).
- Disable Linux automatic NUMA balancing.

## Page faults

When reading or writing to file backed memory that is not in the *page
cache*<sup>[1](#fn:1)</sup> or to *anonymous memory*<sup>[2](#fn:2)</sup> that has been swapped out,
the kernel must first load the data from the underlying storage device. This is
called a major page fault and incurs a similar overhead as issuing a `read` or
`write` system call.

If the page is already in the page cache you will still incur a minor page fault
on first access after calling [`mmap`](https://www.man7.org/linux/man-pages/man2/mmap.2.html), during which the page table is
updated to point to the correct page<sup>[3](#fn:3)</sup>. For anonymous memory there
will also be a minor page fault on first write access, when a anonymous page is
allocated, zeroed and the page table updated<sup>[2](#fn:2)</sup>. Basically memory mappings
are lazily initialized on first use. Note also that access to the page table
during a page fault is protected by locks leading to scalability issues in
multi-threaded applications<sup>[4](#fn:4)</sup>. On systems with non-uniform
memory access (NUMA) the
[automatic NUMA memory balancing](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/kernel.html#numa-balancing)
will also cause page faults.

To avoid page faults you can pre-fault and disable page cache eviction of the
needed memory using the [`mlock`](https://www.man7.org/linux/man-pages/man2/mlock.2.html) system call or the `MAP_LOCKED` and
`MAP_POPULATE` flags to [`mmap`](https://www.man7.org/linux/man-pages/man2/mmap.2.html). You can also disable swap system wide to
prevent anonymous memory from being swapped to disk. Automatic NUMA memory
balancing can be disabled using the following command:

```
echo 0 > /proc/sys/kernel/numa_balancing
```
You can monitor number of page faults using

```
ps -eo min_flt,maj_flt,cmd
```
or

```
perf stat -e faults,minor-faults,major-faults
```
## TLB misses

The
[translation lookaside buffer (TLB)](https://en.wikipedia.org/wiki/Translation_lookaside_buffer)
is a on CPU cache that maps virtual to physical addresses. These mappings are
maintained for pages typically of size 4 KiB, 2/4 MiB or 1 GiB. Usually there
are separate TLBs for data (DTLB) and instructions (ITLB) with a shared second
level TLB (STLB)<sup>[5](#fn:5)</sup>. The TLB has a limited number of entries and if a
address is not found in the TLB or STLB, the page table data in the CPU caches
or main memory needs to be referenced, this is called a TLB miss<sup>[6](#fn:6)</sup>. The
same as a CPU cache miss is more expensive than a cache hit, a TLB miss is more
expensive than a TLB hit.

You can minimize TLB misses by reducing your working set size, making sure to
pack your data into as few pages as possible. Additionally you can utilize
larger page sizes than the default 4 KiB. These larger pages are called *huge
pages*<sup>[7](#fn:7)</sup> and allows you to reference more data using fewer pages.

TLB usage can be monitored using:

```
perf stat -e dTLB-loads,dTLB-load-misses,iTLB-loads,iTLB-load-misses
```
If the above command shows that your workload produces a large fraction of TLB misses huge pages will help reduce that.

## TLB shootdowns

Most processors do not provide coherence guarantees for TLB mappings. Instead
the kernel provides this guarantee using a mechanism called a *TLB shootdown*.
It operates by sending inter-processor interrupts (IPIs) that runs kernel code
to invalidate the stale TLB entries<sup>[8](#fn:8)</sup>. *TLB shootdowns* causes each
affected core to context switch into the kernel and thus causes latency spikes
for the process running on the affected cores. It will also cause TLB misses
when a address with an invalidated page table entry is subsequently accessed.

Any operation that narrows a process' access to memory like `munmap` and
`mprotect` will cause a TLB shootdown. Calls to the C standard library allocator
(`malloc`, `free`, etc) will call `madvise(...MADV_FREE)`/`munmap` internally,
but not necessarily on each invocation. Other causes of TLB shootdowns are:
[transparent huge pages (THP)](https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html), [memory compaction](https://lwn.net/Articles/368869/), [kernel samepage
merging (KSM)](https://www.kernel.org/doc/html/latest/admin-guide/mm/ksm.html), [automatic NUMA memory balancing](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/kernel.html#numa-balancing), [page migration](https://www.kernel.org/doc/html/latest/vm/page_migration.html)
and [page cache writeback](https://www.kernel.org/doc/html/latest/filesystems/vfs.html?highlight=writeback#the-address-space-object).

To avoid TLB shootdowns you can map all needed memory at program startup and
avoid calling any functions that modifies the page table after that. The
[mimalloc allocator](https://github.com/microsoft/mimalloc) can be tuned to
allocate huge pages at program startup (`MIMALLOC_RESERVE_HUGE_OS_PAGES=N`) and
never return memory to the OS (`MIMALLOC_PAGE_RESET=0`).

You can view the number of TLB shootdowns per CPU core in `/proc/interrupts`:

```
$ egrep 'TLB|CPU' /proc/interrupts
            CPU0       CPU1       CPU2       CPU3
 TLB:   16642971   16737647   16870842   16350398   TLB shootdowns
```
I wrote a test program [`tlbshootdown.c`](/tlbshootdown.c) to demonstrate how
`munmap` triggers TLB shootdowns:

```
perf stat -e tlb:tlb_flush  ./tlbshootdown 100000
 Performance counter stats for './tlbshootdown 100000':
           100,016      tlb:tlb_flush
       0.260283596 seconds time elapsed
       0.017426000 seconds user
       0.232625000 seconds sys
```
In a multi-threaded program this would have triggered 100000 TLB shootdowns.

## Page cache writeback

When a page in the *page cache*<sup>[1](#fn:1)</sup> has been modified it is marked as
dirty and needs to be eventually written back to disk. This process is called
writeback and is triggered automatically on a timer or when specifically
requested using the system calls `fsync`, `fdatasync`, `sync`, `syncfs`,
`msync`, and others. If any of the dirty pages are part of a writable memory
mapping, the writeback process must first update the page table to mark the page
as read-only before writing it to disk. Any subsequent memory write to the page
will cause a page fault, letting the kernel update the page cache state to dirty
and mark the page writable again. In practice this means that writeback causes
TLB shootdowns and that writes to pages that are currently being written to disk
must stall until the disk write is complete. This leads to latency spikes for
any process that is using *file backed writable memory mappings*.

To avoid latency spikes due to *page cache writeback* you cannot create any
*file backed* (or more precisely *page cache backed*) writable memory mappings.
Creating anonymous writable memory mappings using `mmap(...MAP_ANONYMOUS)` or by
mapping files on Linux
[*tmpfs*](https://www.kernel.org/doc/html/latest/filesystems/tmpfs.html) or
[*hugetlbfs*](https://www.kernel.org/doc/html/latest/admin-guide/mm/hugetlbpage.html)
filesystem is fine.

I wrote a
[small program `writeback.cpp` to demonstrate this effect](/writeback.cpp). On
my Ryzen 3900X with Samsung 970 EVO NVME SSD running Linux 5.7 I get latency
spikes of hundreds of microseconds due to writeback activity:

```
# ./writeback 9 $HOME/junkfile.bin
threshold: 17792 ns
pid: 382129
jitter     900985 ns
jitter      19036 ns
jitter      33283 ns
jitter      18515 ns
jitter     777301 ns
jitter     715154 ns
jitter     118063 ns
jitter     661983 ns
jitter      18676 ns
```
You can inspect `/proc/[pid]/maps` to see if there are any writable memory
mappings. To print shared writable memory mappings backed by the *page cache*:

```
$ cat /proc/*/maps | grep '.w.s' | grep -v -E "/dev/|/mem:|/run/|/tmp/"
```
Note that the above command can have false positives and false negatives
depending on if *tmpfs* is used for `/run/` and `/tmp/`.

## Transparent huge pages

[Linux *transparent huge page* (THP) support](https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html)
allows the kernel to automatically promote regular memory pages into huge pages.
Huge pages reduces TLB pressure, but THP support can introduce latency spikes.

THP will try to automatically promote pages into huge pages at the time of
allocation during minor page faults. Additionally the *khugepaged* daemon runs
in the background and will try to promote continuos ranges of virtual memory
into huge pages. If no huge pages are available when requested, the
[kernel will try to compact memory](https://lwn.net/Articles/368869/) to make
huge pages available.

Both the background promotion of pages by *khugepaged* and on-demand compaction
of pages by *kcompactd* causes latency spikes since they need to move data
around and update the page tables. There is also
[ongoing work to enable proactive memory compaction](https://nitingupta.dev/post/proactive-compaction/)
which would become another source of latency spikes.

To avoid these latency spikes I recommend disabling THP and instead relying on
manually requesting huge pages. THP can be disabled by supplying the kernel
command line parameter `transparent_hugepage=never` or running the following
command:

```
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```
## Kernel samepage merging

[Linux kernel samepage merging (KSM)](https://www.kernel.org/doc/html/latest/admin-guide/mm/ksm.html) is a feature that de-duplicates
memory pages that contains identical data. The merging process needs to lock the
page tables and issue TLB shootdowns, leading to unpredictable memory access
latencies. KSM only operates on memory pages that has been opted in to samepage
merging using `madvise(...MADV_MERGEABLE)`. If needed KSM can be disabled system
wide by running the following command:

```
echo 0 > /sys/kernel/mm/ksm/run
```
## NUMA and page migration

[Non-uniform memory access (NUMA)](https://www.kernel.org/doc/html/latest/vm/numa.html) occurs when the memory access time
varies with memory location and processor core. You need to take this into
account when designing your system.

On Linux you can use [cpusets](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v1/cpusets.html), [`numactl`](https://www.man7.org/linux/man-pages/man8/numactl.8.html),
[`set_mempolicy`](https://man7.org/linux/man-pages/man2/set_mempolicy.2.html) and [`mbind`](https://man7.org/linux/man-pages/man2/mbind.2.html) to control the NUMA node
memory placement policy.

Additionally Linux supports
[automatic page fault based NUMA memory balancing](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/kernel.html#numa-balancing)
and
[manual page migration](https://www.kernel.org/doc/html/latest/vm/page_migration.html)
of memory between NUMA nodes. Migration of memory pages between NUMA nodes will
cause TLB shootdowns and page faults for applications using the affected memory.

Automatic NUMA memory balancing can be disabled with the following command:

```
echo 0 > /proc/sys/kernel/numa_balancing
```
Also make sure to disable the [*numad*](https://linux.die.net/man/8/numad) user
space NUMA memory balancing service.

## References

- Ulrich Drepper (2007). “What Every Programmer Should Know About Memory”.
[https://www.akkadia.org/drepper/cpumemory.pdf](https://www.akkadia.org/drepper/cpumemory.pdf) ,[https://lwn.net/Articles/250967/](https://lwn.net/Articles/250967/)
- Stack Overflow. “What Every Programmer Should Know About Memory?”.
[https://stackoverflow.com/questions/8126311/what-every-programmer-should-know-about-memory](https://stackoverflow.com/questions/8126311/what-every-programmer-should-know-about-memory)
- “The Linux Kernel documentation”.
[https://www.kernel.org/doc/html/latest/index.html](https://www.kernel.org/doc/html/latest/index.html)
- “AMD64 Architecture Programmer’s Manual”.
[https://developer.amd.com/resources/developer-guides-manuals/](https://developer.amd.com/resources/developer-guides-manuals/)
- “Intel® 64 and IA-32 Architectures Software Developer Manuals”.
[https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html](https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html)
- Félix Cloutier. “x86 and amd64 instruction reference”.
[https://www.felixcloutier.com/x86/](https://www.felixcloutier.com/x86/)
- Nitin Gupta. “Proactive compaction for the kernel”.
[https://lwn.net/Articles/817905/](https://lwn.net/Articles/817905/)
- Nitin Gupta. “Proactive Compaction for the Linux kernel”.
[https://nitingupta.dev/post/proactive-compaction/](https://nitingupta.dev/post/proactive-compaction/)

1. 
“The physical memory is volatile and the common case for getting data into the memory is to read it from files. Whenever a file is read, the data is put into the page cache to avoid expensive disk access on the subsequent reads. Similarly, when one writes to a file, the data is placed in the page cache and eventually gets into the backing storage device. The written pages are marked as dirty and when Linux decides to reuse them for other purposes, it makes sure to synchronize the file contents on the device with the updated data.” [https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html?#page-cache](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html?#page-cache)[↩︎](#fnref:1)
2. 
“The anonymous memory or anonymous mappings represent memory that is not backed by a filesystem. Such mappings are implicitly created for program’s stack and heap or by explicit calls to mmap(2) system call. Usually, the anonymous mappings only define virtual memory areas that the program is allowed to access. The read accesses will result in creation of a page table entry that references a special physical page filled with zeroes. When the program performs a write, a regular physical page will be allocated to hold the written data. The page will be marked dirty and if the kernel decides to repurpose it, the dirty page will be swapped out.” [https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html#anonymous-memory](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html#anonymous-memory)[↩︎](#fnref:2)
3. 
[Travis Downs](https://travisdowns.github.io/) provided an interesting
observation on anonymous vs file backed memory: “One note, although it might
be a bit obscure for the article, is that there is a quite a difference in
minor fault behavior when mapping in pages depending on whether they are
file backed or not. If a page is backed by a file, it is subject to “fault
around” which means that the kernel will map in nearby pages if they are
also present in the page cache (i.e., it was a soft fault). You can tune how
many pages are faulted in with /sys/kernel/debug/fault_around_bytes, which
by default is 64k (16 pages).The upshot of all this is reading a mapped file (for the first time) can be faster than reading from anonymous memory, since you get 1/16th of the minor faults when you are reading the file.” You can find even more details on fault-around here: [https://www.realworldtech.com/forum/?threadid=185310&curpostid=185310](https://www.realworldtech.com/forum/?threadid=185310&curpostid=185310)[↩︎](#fnref:3)
4. 
[https://www.kernel.org/doc/html/latest/vm/split_page_table_lock.html](https://www.kernel.org/doc/html/latest/vm/split_page_table_lock.html)[↩︎](#fnref:4)
5. 
The TLB hierarchy for Intel microarchitectures are documented in the “Intel® 64 and IA-32 Architectures Optimization Reference Manual” [https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html#optimization](https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html#optimization)You can find information on the TLB configuration for many different CPU microarchitectures at [https://en.wikichip.org](https://en.wikichip.org) .[↩︎](#fnref:5)
6. 
“What happens after a L2 TLB miss?”. [https://stackoverflow.com/questions/32256250/what-happens-after-a-l2-tlb-miss](https://stackoverflow.com/questions/32256250/what-happens-after-a-l2-tlb-miss)[↩︎](#fnref:6)
7. 
“The address translation requires several memory accesses and memory accesses are slow relatively to CPU speed. To avoid spending precious processor cycles on the address translation, CPUs maintain a cache of such translations called Translation Lookaside Buffer (or TLB). Usually TLB is pretty scarce resource and applications with large memory working set will experience performance hit because of TLB misses. Many modern CPU architectures allow mapping of the memory pages directly by the higher levels in the page table. For instance, on x86, it is possible to map 2M and even 1G pages using entries in the second and the third level page tables. In Linux such pages are called huge. Usage of huge pages significantly reduces pressure on TLB, improves TLB hit-rate and thus improves overall system performance.” [https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html#huge-pages](https://www.kernel.org/doc/html/latest/admin-guide/mm/concepts.html#huge-pages)[↩︎](#fnref:7)
8. 
On the AMD64 / x86-64 architecture TLB entries are invalidated using the [`INVLPG`](https://www.felixcloutier.com/x86/invlpg) or[`INVPCID](https://www.felixcloutier.com/x86/invpcid) instructions.On the ARM architecture TLB entries are invalidated using the [`TLBI` instruction](https://developer.arm.com/architectures/learn-the-architecture/memory-management/tlb-maintenance) .More information on TLB invalidation can be found in [The Linux Kernel documentation](https://www.kernel.org/doc/html/latest/x86/tlb.html) .[↩︎](#fnref:8)
