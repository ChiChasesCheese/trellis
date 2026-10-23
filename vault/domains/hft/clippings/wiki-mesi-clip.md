---
title: MESI protocol - Wikipedia
source: https://en.wikipedia.org/wiki/MESI_protocol
published: '2003-07-14'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# MESI protocol - Wikipedia

# MESI protocol

The **MESI protocol** is an invalidate-based [cache coherence protocol](https://en.wikipedia.org/wiki/List_of_cache_coherency_protocols), and is one of the most common protocols that support [write-back caches](https://en.wikipedia.org/wiki/Write-back_cache). It is also known as the **Illinois protocol** due to its development at the [University of Illinois at Urbana-Champaign](https://en.wikipedia.org/wiki/University_of_Illinois_Urbana-Champaign).<sup>[\[1\]](#cite_note-1)</sup> Write back caches can save considerable bandwidth generally wasted on a [write through cache](<https://en.wikipedia.org/wiki/Cache_(computing)#Writing_policies>). There is always a dirty state present in write-back caches that indicates that the data in the cache is different from that in the main memory. The Illinois Protocol requires a cache-to-cache transfer on a miss if the block resides in another cache. This protocol reduces the number of main memory transactions with respect to the [MSI protocol](https://en.wikipedia.org/wiki/MSI_protocol). This marks a significant improvement in performance.[\[2\]](#cite_note-2)

## States

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=1)]

The letters in the acronym MESI represent four exclusive states that a [cache line](https://en.wikipedia.org/wiki/CPU_cache) can be marked with (encoded using two additional [bits](https://en.wikipedia.org/wiki/Bit)):

- Modified (M)
- The cache line is present only in the current cache, and is *dirty* - it has been modified (M state) from the value in[main memory](https://en.wikipedia.org/wiki/Main_memory) .  The cache is required to write the data back to the main memory at some time in the future, before permitting any other read of the (no longer valid) main memory state.  The write-back changes the line to the Shared state (S).
- Exclusive (E)
- The cache line is present only in the current cache, but is *clean* - it matches main memory.  It may be changed to the Shared state at any time, in response to a read request.  Alternatively, it may be changed to the Modified state when writing to it.
- Shared (S)
- Indicates that this cache line may be stored in other caches of the machine and is *clean* - it matches the main memory.  The line may be discarded (changed to the Invalid state) at any time.
- Invalid (I)
- Indicates that this cache line is invalid (unused).

For any given pair of caches, the permitted states of a given cache line are as follows:

|  | M | E | S | I | 
|---|---|---|---|---|
| M |  |  |  |  | 
| E |  |  |  |  | 
| S |  |  |  |  | 
| I |  |  |  |  | 

When the block is marked M (modified) or E (exclusive), the copies of the block in other Caches are marked as I (Invalid).

## Operation

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=2)]

The MESI protocol is defined by a [finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine) that transitions from one state to another based on 2 stimuli.

The first stimulus is the processor-specific Read and Write request. For example: A processor P1 has a Block X in its Cache, and there is a request from the processor to read or write from that block.

The second stimulus is given through the bus connecting the processors. In particular, the "Bus side requests" come from other processors that don't have the cache block or the updated data in their Cache. The bus requests are monitored with the help of [Snoopers](https://en.wikipedia.org/wiki/Bus_snooping),<sup>[\[4\]](#cite_note-4)</sup> which monitor all the bus transactions.

Following are the different types of Processor requests and Bus side requests:

Processor Requests to Cache include the following operations:

1. PrRd: The processor requests to **read** a Cache block.
2. PrWr: The processor requests to **write** a Cache block

Bus side requests are the following:

1. BusRd: Snooped request that indicates there is a **read** request to a Cache block requested by another processor
2. BusRdX: Snooped request that indicates there is a **write** request to a Cache block requested by another processor that**doesn't already have the block.**
3. BusUpgr: Snooped request that indicates that there is a write request to a Cache block requested by another processor that already has that **cache block residing in its own cache** .
4. Flush: Snooped request that indicates that an entire cache block is written back to the main memory by another processor.
5. FlushOpt: Snooped request that indicates that an entire cache block is posted on the bus in order to supply it to another processor (Cache to Cache transfers).

(*Such Cache to Cache transfers can reduce the read miss [latency](https://en.wikipedia.org/wiki/CAS_latency) if the latency to bring the block from the main memory is more than from Cache to Cache transfers, which is generally the case in bus based systems.*)

**Snooping Operation**: In a snooping system, all caches on a bus monitor all the transactions on that bus. Every cache has a copy of the sharing status of every block of physical memory it has stored. The state of the block is changed according to the [State Diagram](https://en.wikipedia.org/wiki/State_diagram) of the protocol used. (Refer image above for MESI state diagram). The bus has snoopers on both sides:

1. Snooper towards the Processor/Cache side.
2. The snooping function on the memory side is done by the [Memory controller](https://en.wikipedia.org/wiki/Memory_controller) .

**Explanation:**

Each Cache block has its own 4 state [finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine) (refer image 1.1). The State transitions and the responses at a particular state with respect to different inputs are shown in Table1.1 and Table 1.2

| Table 1.1 State Transitions and response to various Processor Operations |  |  | 
|---|---|---|
| Initial State | Operation | Response | 
|---|---|---|
| Invalid(I) | PrRd |  | 
|  | PrWr |  | 
| Exclusive(E) | PrRd |  | 
|  | PrWr |  | 
| Shared(S) | PrRd |  | 
|  | PrWr |  | 
| Modified(M) | PrRd |  | 
|  | PrWr |  | 

| Table 1.2 State Transitions and response to various Bus Operations |  |  | 
|---|---|---|
| Initial State | Operation | Response | 
|---|---|---|
| Invalid(I) | BusRd |  | 
|  | BusRdX/BusUpgr |  | 
| Exclusive(E) | BusRd |  | 
|  | BusRdX |  | 
| Shared(S) | BusRd |  | 
|  | BusRdX/BusUpgr |  | 
| Modified(M) | BusRd |  | 
|  | BusRdX |  | 

A write may only be performed freely if the cache line is in the Modified or Exclusive state. If it is in the Shared state, all other cached copies must be invalidated first. This is typically done by a broadcast operation known as *Request For Ownership (RFO)*.

A cache that holds a line in the Modified state must *[snoop](https://en.wikipedia.org/wiki/Bus_snooping)* (intercept) all attempted reads (from all the other caches in the system) of the corresponding main memory location and insert the data that it holds.  This can be done by forcing the read to *back off* (i.e. retry later), then writing the data to main memory and changing the cache line to the Shared state.  It can also be done by sending data from Modified cache to the cache performing the read.  Note, snooping only required for read misses (protocol ensures that Modified cannot exist if any other cache can perform a read hit).

A cache that holds a line in the Shared state must listen for invalidate or request-for-ownership broadcasts from other caches, and discard the line (by moving it into Invalid state) on a match.

The Modified and Exclusive states are always precise: i.e. they match the true cache line ownership situation in the system. The Shared state may be imprecise: if another cache discards a Shared line, this cache may become the sole owner of that cache line, but it will not be promoted to Exclusive state. Other caches do not broadcast notices when they discard cache lines, and this cache could not use such notifications without maintaining a count of the number of shared copies.

In that sense the Exclusive state is an opportunistic optimization: If the CPU wants to modify a cache line in state S, a bus transaction is necessary to invalidate all other cached copies. State E enables modifying a cache line with no bus transaction.

**Illustration of MESI protocol operations**

For example, let us assume that the following stream of read/write references. All the references are to the same location and the digit refers to the processor issuing the reference.

The stream is : R1, W1, R3, W3, R1, R3, R2.

Initially it is assumed that all the caches are empty.

| Table 1.3 An example of how MESI works All operations to same cache block  (Example: "R3" means read block by processor 3) |  |  |  |  |  |  | 
|---|---|---|---|---|---|---|
|  | ***Local******Request*** | ***P1*** | ***P2*** | ***P3*** | *Generated**Bus Request* | *Data Supplier* | 
|---|---|---|---|---|---|---|
| 0 | **Initially** | - | - | - | - | - | 
| 1 | R1 | E | - | - | **BusRd** | **Mem** | 
| 2 | W1 | M | - | - | - | - | 
| 3 | R3 | S | - | S | **BusRd** | **P1's Cache** | 
| 4 | W3 | I | - | M | **BusUpgr** | **-** | 
| **5** | R1 | **S** | **-** | **S** | BusRd | P3's Cache | 
| **6** | R3 | **S** | **-** | **S** | **-** | **-** | 
| **7** | R2 | **S** | **S** | **S** | BusRd | P1/P3's Cache | 

**Note:** *The term snooping referred to below is a protocol for maintaining cache coherency in symmetric multiprocessing environments. All the caches on the bus monitor (snoop) the bus if they have a copy of the block of data that is requested on the bus.*

- Step 1: As the cache is initially empty, so the main memory provides P1 with the block and it becomes exclusive state.
- Step 2: As the block is already present in the cache and in an exclusive state so it directly modifies that without any bus instruction. The block is now in a modified state.
- Step 3: In this step, a BusRd is posted on the bus and the snooper on P1 senses this. It then flushes the data and changes its state to shared. The block on P3 also changes its state to shared as it has received data from another cache. The data is also written back to the main memory.
- Step 4: Here a BusUpgr is posted on the bus and the snooper on P1 senses this and invalidates the block as it is going to be modified by another cache. P3 then changes its block state to modified.
- Step 5: As the current state is invalid, thus it will post a BusRd on the bus. The snooper at P3 will sense this and so will flush the data out. The state of both the blocks on P1 and P3 will become shared now. Notice that this is when even the main memory will be updated with the previously modified data.
- Step 6: There is a hit in the cache and it is in the shared state so no bus request is made here.
- Step 7: There is cache miss on P2 and a BusRd is posted. The snooper on P1 and P3 sense this and both will attempt a flush. Whichever gets access of the bus first will do that operation.

### Read For Ownership

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=3)]

A *Read For Ownership (RFO)* is an operation in [cache coherency](https://en.wikipedia.org/wiki/Cache_coherency) protocols that combines a read and an invalidate broadcast.  The operation is issued by a processor trying to write into a cache line that is in the shared (S) or invalid (I) states of the MESI protocol. The operation causes all other caches to set the state of such a line to I. A read for ownership transaction is a read operation with intent to write to that [memory address](https://en.wikipedia.org/wiki/Memory_address). Therefore, this operation is exclusive. It brings data to the cache and invalidates all other processor caches that hold this memory line. This is termed "BusRdX" in tables above.

### Memory Barriers

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=4)]

MESI in its naive, straightforward implementation exhibits two particular performance issues. First, when writing to an invalid cache line, there is a long delay while the line is fetched from other CPUs. Second, moving cache lines to the invalid state is time-consuming. To mitigate these delays, CPUs implement store buffers and invalidate queues.[\[5\]](#cite_note-5)

#### Store Buffer

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=5)]

A store buffer is used when writing to an invalid cache line. As the write will proceed anyway, the CPU issues a read-invalid message (hence the cache line in question and all other CPUs' cache lines that store that memory address are invalidated) and then pushes the write into the store buffer, to be executed when the cache line finally arrives in the cache.

A direct consequence of the store buffer's existence is that when a CPU commits a write, that write is not immediately written in the cache. Therefore, whenever a CPU needs to read a cache line, it first scans its own store buffer for the existence of the same line, as there is a possibility that the same line was written by the same CPU before but hasn't yet been written in the cache (the preceding write is still waiting in the store buffer). Note that while a CPU can read its own previous writes in its store buffer, other CPUs *cannot see those writes* until they are flushed to the cache — a CPU cannot scan the store buffer of other CPUs.

#### Invalidate Queues

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=6)]

With regard to invalidation messages, CPUs implement invalidate queues, whereby incoming invalidate requests are instantly acknowledged but not immediately acted upon. Instead, invalidation messages simply enter an invalidation queue and their processing occurs as soon as possible (but not necessarily instantly). Consequently, a CPU can be oblivious to the fact that a cache line in its cache is actually invalid, as the invalidation queue contains invalidations that have been received but haven't yet been applied. Note that, unlike the store buffer, the CPU can't scan the invalidation queue, as that CPU and the invalidation queue are physically located on opposite sides of the cache.

As a result, memory barriers are required.  A *store barrier* will flush the store buffer, ensuring all writes have been applied to that CPU's cache.  A *read barrier* will flush the invalidation queue, thus ensuring that all writes by other CPUs become visible to the flushing CPU. Furthermore, [memory management](https://en.wikipedia.org/wiki/Memory_management) units do not scan the store buffer, causing similar problems. This effect is visible even in single threaded processors.[\[6\]](#cite_note-6)

## Advantages of MESI over MSI

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=7)]

The most striking difference between MESI and [MSI](https://en.wikipedia.org/wiki/MSI_protocol) is the extra "exclusive" state present in the MESI protocol. This extra state was added as it has many advantages. When a processor needs to read a block that **none of the other processors have** and then write to it, two bus transactions will take place in the case of MSI. First, a BusRd request is issued to read the block followed by a BusUpgr request before writing to the block. The BusUpgr request in this scenario is useless as none of the other caches have the same block, but there is no way for one cache to know about this. Thus, MESI protocol overcomes this limitation by adding an Exclusive state, which results in saving a bus request. This makes a huge difference when a sequential application is running. As only one processor works on a piece of data, all the accesses will be exclusive. MSI performs much worse in this case due to the extra bus messages. Even in the case of a highly parallel application with minimal sharing of data, MESI is far faster. 
Adding the Exclusive state also comes at no cost as 3 states and 4 states are both representable with 2 bits.

## Disadvantage of MESI

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=8)]

In case continuous read and write operations are performed by various caches on a particular block, the data has to be flushed to the bus every time. Thus, the main memory will pull this on every flush and remain in a clean state. But this is not a requirement and is just an additional overhead caused by using MESI. This challenge was overcome by the [MOESI protocol](https://en.wikipedia.org/wiki/MOESI_protocol).[\[7\]](#cite_note-7)

In case of S (Shared State), multiple snoopers may response with FlushOpt with the same data (see the example above). The F state in [MESIF](https://en.wikipedia.org/wiki/MESIF_protocol) addresses this redundancy.

## See also

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=9)]

- [Coherence protocol](https://en.wikipedia.org/wiki/Coherence_protocol)
- [MSI protocol](https://en.wikipedia.org/wiki/MSI_protocol) , the basic protocol from which the MESI protocol is derived.
- [Write-once (cache coherency)](<https://en.wikipedia.org/wiki/Write-once_(cache_coherency)>) , an early form of the MESI protocol.
- [MOSI protocol](https://en.wikipedia.org/wiki/MOSI_protocol)
- [MOESI protocol](https://en.wikipedia.org/wiki/MOESI_protocol)
- [MESIF protocol](https://en.wikipedia.org/wiki/MESIF_protocol)
- [MERSI protocol](https://en.wikipedia.org/wiki/MERSI_protocol)
- [Dragon protocol](https://en.wikipedia.org/wiki/Dragon_protocol)
- [Firefly protocol](<https://en.wikipedia.org/wiki/Firefly_(cache_coherence_protocol)>)

## References

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=10)]

1. [↑](#cite_ref-1) Papamarcos, M. S.; Patel, J. H. (1984).["A low-overhead coherence solution for multiprocessors with private cache memories"](https://www.csl.cornell.edu/courses/ece5720/papamarcos.isca84.pdf) (PDF).*Proceedings of the 11th annual international symposium on Computer architecture - ISCA '84* . p. 348.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/800015.808204](https://doi.org/10.1145%2F800015.808204) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[0818605383](https://en.wikipedia.org/wiki/Special:BookSources/0818605383) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[195848872](https://api.semanticscholar.org/CorpusID:195848872) . Retrieved March 19, 2013.
2. [↑](#cite_ref-2) Gómez-Luna, J.; Herruzo, E.; Benavides, J.I. "MESI Cache Coherence Simulator for Teaching Purposes".*Clei Electronic Journal* .**12** (1, PAPER 5, APRIL 2009).[CiteSeerX](<https://en.wikipedia.org/wiki/CiteSeerX_(identifier)>)[10.1.1.590.6891](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.590.6891) .`{{`[cite journal](https://en.wikipedia.org/wiki/Template:Cite_journal) }}
: Cite uses deprecated parameter`|citeseerx=` ([help](https://en.wikipedia.org/wiki/Help:CS1_errors#deprecated_params) )
3. [↑](#cite_ref-3) Culler, David (1997).*Parallel Computer Architecture* . Morgan Kaufmann Publishers. pp. Figure 5–15 State transition diagram for the Illinois MESI protocol. Pg 286.
4. [↑](#cite_ref-4) Bigelow, Narasiman, Suleman.["An evaluation of Snoopy Based Cache Coherence protocols"](http://hps.ece.utexas.edu/people/suleman/class_projects/pca_report.pdf) (PDF). ECE Department, University of Texas at Austin.`{{`[cite web](https://en.wikipedia.org/wiki/Template:Cite_web) }}
:  CS1 maint: multiple names: authors list ([link](https://en.wikipedia.org/wiki/Category:CS1_maint:_multiple_names:_authors_list) )
5. [↑](#cite_ref-5) Handy, Jim (1998).*The Cache Memory Book* . Morgan Kaufmann.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[9780123229809](https://en.wikipedia.org/wiki/Special:BookSources/9780123229809) .
6. [↑](#cite_ref-6) Chen, G.; Cohen, E.; Kovalev, M. (2014). "Store Buffer Reduction with MMUs".*Verified Software: Theories, Tools and Experiments* . Lecture Notes in Computer Science. Vol. 8471. p. 117.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-319-12154-3_8](https://doi.org/10.1007%2F978-3-319-12154-3_8) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-319-12153-6](https://en.wikipedia.org/wiki/Special:BookSources/978-3-319-12153-6) .
7. [↑](#cite_ref-7)["Memory System (Memory Coherency and Protocol)"](http://www.cs.wustl.edu/~roger/569M/24593.pdf) (PDF). AMD64 Technology. September 2006.

## External links

[
[edit](/w/index.php?title=MESI_protocol&action=edit§ion=11)]
