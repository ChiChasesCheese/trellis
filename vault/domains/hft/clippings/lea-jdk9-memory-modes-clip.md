---
title: Using JDK 9 Memory Order Modes
source: https://gee.cs.oswego.edu/dl/html/j9mm.html
published: '2004-01-01'
site: gee.cs.oswego.edu
clipped: '2026-10-23'
---

# Using JDK 9 Memory Order Modes

Last update: Fri Nov 16 08:46:48 2018 Doug Lea

This guide is mainly intended for expert programmers familiar with
  Java concurrency, but unfamiliar with the memory order modes
  available in JDK 9 provided by VarHandles.  Mostly, it focuses on
  how to think about modes when developing parallel software. Feel
  free to first read the  [Summary](#summarysec). 

To get the shockingly ugly syntactic details over with: A VarHandle can be associated with any field, array element, or static, allowing control over access modes. VarHandles should be declared as static final fields and explicitly initialized in static blocks. By convention, we give VarHandles for fields names that are uppercase versions of the field names. For example, in a Point class:

```
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
class Point {
   volatile int x, y;
   private static final VarHandle X;
   static {
     try {
       X = MethodHandles.lookup().
           findVarHandle(Point.class, "x",
                         int.class);
     } catch (ReflectiveOperationException e) {
       throw new Error(e);
     }
   }
   // ...
}
  
```
Also, JDK 9 versions of java.util.concurrent.atomic classes include methods corresponding to these VarHandle constructions, applied to the single elements or arrays held by the associated Atomic objects.

A planned follow-up will present more detailed examples of VarHandle usages and further coding guidelines.

Back in the earliest days of concurrent programming (predating Java), computers were much simpler devices. Uniprocessors single-stepped through instructions accessing memory cells, and emulated concurrency by context-switching across threads. While many of the pioneering ideas about coordination and interference in concurrent programming established during this era still hold, others turn out to be ill-matched for systems employing three forms of parallelism that have since emerged:

Concepts and techniques for dealing with these forms of parallelism are maturing to the point that the same ideas regularly appear across different programming languages, processor architectures, and even non-shared memory (distributed) systems. This guide focuses on Java, but also includes some brief remarks about other languages, notes on processor-level issues that are abstracted over at the language level, and also a few ties to distributed (cluster and cloud) consistency models that otherwise differ mainly with respect to fault tolerance issues that don't normally arise in shared memory systems.

Across these, no single rule or model makes sense for all code in
  all programs. So there must be multiple models, or *modes*,
  along with accounts of how they interrelate.  This was seen even in
  the early days of concurrency. The idea of a *Monitor*
  introduced in the 1960s implicitly established two modes, leading to
  rules for "normal" code appearing in lock-protected bodies, and
  other rules for accessing and ordering locks.  In the 1990s, Java
  introduced another mode, `volatile`, that wasn't formally
  well-specified until JSR133 in 2004.  

Experience with multicores has shown that a few more modes are needed to deal with common concurrent programming problems. Without them, some programmers over-synchronize code, which can make programs slow, some programmers under-synchronize code, which can make programs wrong, and other programmers work around limitations by using unstandardized operations available on particular JVMs and processors, which can make programs unportable.

The new memory order modes are defined with cumulative effect, from weakest to strongest: Plain, Opaque, Release/Acquire, and Volatile. The existing Plain and Volatile modes are defined compatibly with their pre-JDK 9 forms. Any guaranteed property of a weaker mode, plus more, holds for a stronger mode. (Conversely, implementations are allowed to use a stronger mode than requested for any access.) In JDK 9, these are provided without a full formal specification. This document does not include a specification of memory order modes. It instead discusses usage in terms of their properties (mainly: commutativity, coherence, causality, and consensus) that build upon one another. The resulting memory consistency rules can be thought of in terms of increasingly restrictive caching protocols.

Because stronger modes impose more ordering constraints, they reduce potential parallelism, in at least one of the above senses -- if operations are performed in parallel, ordering may require that one activity block (reducing total parallelism and adding overhead) waiting for completion of another. But ordering may also provide guarantees that programs rely on. When you don't enforce required constraints, they may hold anyway sometimes but not always, resulting in hard-to-replicate software errors.

When the strongest synchronization and ordering constructions such as monitors were first devised, the resulting constraints on parallelism were not much of an issue because there was not much parallelism available anyway. But now, choices often entail engineering tradeoffs. Enabling parallelism generally improves scalability. In the fastest but least controlled parallel programs, every thread accesses only local variables and encounters no ordering or resource constraints. But other cases may encounter time, space, energy, and complexity issues that don't always result in better performance on any given program or platform.

  The use of multiple consistency modes can also make correctness more
  difficult to establish.  The existence of a "data race" is not
  always a yes/no matter, but is the result of using a weaker mode
  than you needed to preserve correctness.  Further, many concurrency
  bugs have little to do with modes per se.  For example, no choice of
  mode will fix check-then-act errors of the form `if (v != null)
  use(v)`, where `v` is a concurrently updated variable
  that may become null between the check and use.  Existing
  concurrency tools do not make these fine distinctions, so analysis
  and testing may be more difficult. Additionally, the details of
  using weaker modes, especially in lock-free programming, may
  clash with established lock-oriented rules and conventions, so some
  care may be required when choosing among equivalent-seeming ways of
  expressing constraints.  But if you are reading this, then you are
  probably interested in exploring the tradeoffs encountered when
  arranging for and exploiting parallelism.

Memory order modes describe relations among
  memory *accesses* (reads, writes, and atomic updates), and
  only incidentally constrain other computations. These relations are
  defined over accesses as Read, Write, and Update *events*,
  not the values accessed. The relations focus on *ordering*
  because they restrict the potential parallelism that would be
  enabled by the lack of ordering constraints. Access events might
  have observable durations, but are constrained in terms of
  instantaneous "commit" points.

  Here's some terminology
  about  [ordering
  relations](https://en.wikipedia.org/wiki/Order_theory) as applied to events:
  *Strict* irreflexive orders act like less-than, not
  less-than-or-equals.  In a (strict) *total order* each event
  is ordered with respect to every other event, resulting in a linear
  (sequential) chain of events. In a (strict) *partial order*,
  any two events need not be related at all (so might be concurrent)
  but there are no cycles (circularities). A *linear extension*
  (also known as a topological sort) of a partial order is one of
  possibly many sequentializations (total orderings) that obey all of
  its ordering constraints. In a partial order, two events might be
  unordered, but in any linear extension, one precedes the other.

Most memory ordering properties are ultimately based on only two
  (strict) relations, one within threads, and one across threads.  As
  described below, intrathread *local precedence* denotes that
  access A precedes access B within the same thread.
  The *Read-by* relation orders *interthread* accesses:
  For variable x, if Read Rx reads from the write of Write Wx, then Wx
  must occur before Rx.  The corresponding *reads-from*
  function from each Read to its source Write has the opposite
  directionality, and can be simpler to use in specifications
  because it is a function, not just a relation.

These two relations can be used together to define
  the *antecedence* relation that links temporal orderings
  within threads with those across threads. This takes the same form
  as the original *happens-before* relation defined by
  
    [Leslie Lamport in 1978](http://dl.acm.org/citation.cfm?id=359563). But because happens-before has also
  been defined in several subtly different ways when applied to memory
  model specifications, we'll use this more neutral term to avoid
  confusion. (The ordinary dictionary definition of "antecedes" is,
  appropriately, "precedes in time", and so might be a better term
  anyway.)

Access A antecedes access B if:

  As defined here, antecedence is just a relation without any
  guaranteed properties beyond transitivity (the final clause) --
  intrathread and interthread orderings are not required to be
  consistent with each other.  Memory order modes impose constraints
  on antecedence and/or *execution order* -- the (partial)
  order of accesses in a program execution without regard for
  antecedence, as well as restrictions (projections) of these orders
  to selected events, for example *overwrites* to the same
  variable.

  When represented as graphs with events as nodes and relations as
  links, total orders form linear lists, and partial orders
  form *DAGs* -- directed acyclic graphs. Another way to
  represent ordered events is to give them numerical tags.  These may
  correspond to version numbers or
  
  [timestamps](https://en.wikipedia.org/wiki/Lamport_timestamps) that may be used and compared as
  [Vector
    clocks](https://en.wikipedia.org/wiki/Vector_clock).

Guarantees about ordering properties do not necessarily imply that any given observer could know orderings in advance or validate them after the fact. They are invariants that programmers may rely on and/or provide to help establish the correctness (or at least the possibility of correctness) of programs. For example, some data race errors result when there are not enough constraints to be sure that a given Read has only one possible Write that it could read from.

*Plain* mode applies to syntactic accesses of plain
  (non-volatile) object fields (as in `int v = aPoint.x`), as
  well as statics and array elements.  It also applies to default
  VarHandle `get` and `set` access. Even though it
  behaves in the same way as always, its properties interact with new
  VarHandle modes and operations in ways best explained in terms of a
  quick review of relevant aspects of processor and compiler design.

  Plain mode extends the otherwise unnamed "Local" mode in which all
  accesses are to method-local arguments and variables; for example,
  the code for pure expressions and functions.  Plain mode
  maintains *local precedence* order for accesses, which need
  not match source code statement order or machine instruction order,
  and is not in general even a total (sequential) order.  To
  illustrate, consider this expression-based statement, where all
  variables are method-local ints:
  

```
  d = (a + b) * (c + b);
  
```
```
  1: load a, r1
  2: load b, r2
  3: add r1, r2, r3
  4: load c, r4
  5: load b, r5
  6: add r4, r5, r6
  7: mul r3, r6, r7
  8: store r7, d
  
```
  Such decisions by compilers about instruction order might not matter
  much, because commodity processors themselves perform parallel
  ("out-of-order") instruction execution.  Most processors control
  execution by tracking completion dependencies, using the same
  techniques seen when programming CompletableFutures. For example,
  all of the loads may be started early, triggering the add
  instructions (possibly in parallel on superscalar CPUs) when the
  values are available in registers, and similarly triggering the
  multiply when the adds complete.  Even if two instructions are
  started in sequential order, they may complete (*commit*) in
  a different order, or at the same time.  So *local
  precedence*, defined with respect to these commit points, need
  not include any before/after ordering relation among some
  actions. For example, one possible execution might look like (where
  instructions on the same line operate in parallel):
  

```
 load a, r1 | load b, r2 | load c, r4 | load b, r5
 add r1, r2, r3 | add r4, r5, r6
 mul r3, r6, r7
 store r7, d
  
```
The operations appearing on each line need not actually execute in parallel -- any sequential permutation of each line is also allowed; instructions emitted by a compiler could be correspondingly reordered. Any of these executions might occur even if the original source split the evaluation as:

```
  tmp = (a + b);
  d = tmp * (c + b);
  
```
With the help of optimizing compilers, processors may eliminate unnecessary computations and accesses in a code body using dataflow analyses, and may remove unnecessary dependencies using transformations such as SSA and renaming. Different processors and compilers vary in how extensively they perform such optimizations. For example, some may speculatively execute code within an unevaluated conditional, undoing and throwing away effects if the condition is false. And so on. Method boundaries need not define the boundaries of such transformations. Methods may be inlined or interprocedurally optimized, even to the extent that an entire thread is one code body.

  Even though computation may be parallel by default at the
  instruction level, in Local mode, the observable results of
  dependency-triggered execution are always equivalent to those of
  purely step-wise sequential execution, whether or not any allowed
  optimizations actually occur.  The exact relationships between
  statement order and execution order that maintain the
  associated *uniprocessor semantics* don't matter, and cannot
  even be detected (except possibly by tools such as debuggers).
  There are no source-level programmer controls available to alter
  these relationships.

  This also holds across isolated *thread-confined* variables
  -- those created and only ever used by the current thread. A
  thread-confined variable has no accesses in the
  interthread *read-by* relation, as may be discovered by
  compiler escape analysis, in which case the variable may then be
  treated as if it were local.

  Similar properties hold in full Plain mode when all variables are
  accessed by only one thread throughout the course of a code region;
  for example, when all are correctly protected by a lock in
  a `synchronized` method. All Plain accesses within the
  region, possibly excepting initial reads and final writes, are
  within-thread, and may transiently act as if thread-confined.
  Definitions of stronger modes below are phrased only in terms of
  interthread accesses, because the per-variable constraints they add
  are subsumed by uniprocessor semantics that hold for strictly local
  accesses.

  However, when Plain mode is used with variables concurrently
  accessed by multiple threads (i.e., in the presence of data races),
  mismatches between statement order and the ordering (or lack
  thereof) of variable accesses are often observable.  Not only may
  accesses detectably occur in different orders, they may not occur at
  all. For example optimized execution of `int a = p.x; ... int b =
  p.x` may replace the second read with `int b = a`, and
  execution of `p.x = 1; ... p.x = 2` may eliminate the first
  write, and even the second if `p` is not used again in a
  thread body.  Extra writes not present in source code must not
  occur, but writes may appear to be "prescient" -- observably issued
  before they are programmed to occur: Among the craziest-seeming
  cases result from "write-after-read (WAR) hazards" where `r1 = x;
  y = r2;` acts as if reordered to `y = r2; r1 = x;` when
  the value of y impacts the value assigned to x in another thread.
  The long list of further anomalies discovered by people studying
  memory models includes cases in which future memory accesses appear
  to impact the past, where values appear from apparently untaken
  branches, and where arbitrary results occur when one thread
  does `x = y` and another does `y = x`.  Also, when
  multiple other threads read Plain mode writes, some may see them in
  different orders than others.

Possible outcomes include those in which it might seem as if processors make mistakes assuming the presence of executions (multithreaded schedules) that do not actually occur; for example (but not limited to) executions in which no other thread concurrently executes, as well as those stemming from inter-thread compiler analyses and optimizations. Conversely, data race errors may result from programmers assuming the absence of (or not noticing the possible presence of) executions that do actually occur. Some of these problems are common enough to have been given names. For example, in transaction systems, "nonrepeatable read" errors occur when two reads of the same variable in a transaction body obtain different values, but correctness relies on the values being the same.

  Additionally, while Java Plain accesses to `int`, `char`,
  `short`, `float`, `byte`, and reference types
  are *primitively bitwise atomic*, for the
  others, `long`, `double`, as well as compound Value
  Types planned for future JDK releases, it is possible for a racy
  read to return a value with some bits from a write by one thread,
  and other bits from another, with unusable results.

Due to any combination of these mechanisms, in racy programs, there may be only a weak and complicated observed relation between source code and the order of variable accesses. The only assurance that accesses maintain the type safety properties specified in the JLS, and thus cannot cause memory-related JVM crashes. However, there are no further general guarantees about the values accessed. None of the access constraints for shared variables needed in multithreaded programs are reliably maintained without explicit control. Failure to provide control can lead to nearly inexplicable outcomes.

Unless they are further constrained by the contextual effects of stronger ordering constructions described below, any two Plain mode accesses in a code body may act as if they are unordered with respect to each other, and then subject to further optimization. Experience has shown that guesses about guaranteed orderings in Plain mode are often wrong, which is one basis for the good advice to avoid Plain mode data races unless programs can be shown to remain correct regardless of races. These cases are targets of some proposed Java "@" annotations for defensibly racy code. Otherwise, if a program requires ordering (and/or atomicity) for correctness, then arrange shared variable access explicitly, and restrict Plain mode to local computation on values.

Plain mode is usable in the same contexts as plain "non-atomic" mode in C/C++11. Java and C/C++ have many semantic differences, some stemming from the fact that in C/C++, failure to use a language construct in specified ways (including allowing data races in Plain mode) may result in Undefined Behavior, which may include program crashes. In Java, effects may be surprising, but are still circumscribed as type-safe. These differences do not impact most usages of memory ordering modes, that are otherwise defined similarly (with some naming differences) across languages.

  Unlike the case for programming languages, hardware memory models
  can define the analog of local precedence ("preserved program
  order") by exhaustively enumerating effects of instructions.  For
  examples, see
  
    ["A Tutorial Introduction to the ARM and POWER Relaxed Memory
    Models"](https://www.cl.cam.ac.uk/~pes20/ppc-supplemental/test7.pdf) by Luc Maranget, Susmit Sarkar, and Peter Sewell.
    GPUs extend such rules to instructions that operate on multiple
  (contiguous) variables at a time, and often include memory types
  or modes in which variables cannot be shared across threads.

  Dependency-based techniques are seen at a higher level in Java
    parallel Streams, CompletableFutures, Flows, and other fluent APIs
    based on expressions describing possibly-parallel
    computations. Across these, automating parallelism relies on
    representing (or reconstructing) program fragments as DAG, not
    sequences. Some
  
    [dataflow languages](https://en.wikipedia.org/wiki/Dataflow_programming) offer syntax more directly corresponding to
  DAG.  Like fluent APIs, they can avoid confusion about questions
  such as whether semicolons indicate sequencing, but encounter others
  about scopes and contexts. (If there were a perfect way to express
  parallelism and ordering, we'd all be using it.)

  In transactional approaches to concurrency, transaction code bodies
  are explicitly delimited by programmers, rather than implicit in the
  structure of a program. They encounter the same underlying issues,
  sometimes described using different terminology. For example, races
  are usually categorized in terms of
  
    [isolation levels](<https://en.wikipedia.org/wiki/Isolation_(database_systems)>), not ordering constraints.

  Many higher-level APIs can be designed in terms of commutative
  operations that enable more parallelism by requiring less ordering
  control, as discussed
  in  ["The
  Scalable Commutativity Rule: Designing Scalable Software for
  Multicore Processors"](http://dl.acm.org/citation.cfm?id=2699681) by Clements et al, TOCS 2015.

  Approaches to avoiding mis-specification of the relation
  between source program order and Plain mode include
  
    ["promising"](http://sf.snu.ac.kr/promise-concurrency/) semantics, in which writes are conceptually
  assigned timestamp version numbers, and operational rules avoid
  assigning impossible ones. (The operational approach to
  formulating such rules is similar to that of the original
  
  [JLS version 1 memory model](https://docs.oracle.com/javase/specs/jvms/se6/html/Threads.doc.html), but not the current (JLS5-9) JMM,
  that is expressed in terms of ordering relations.)
  

Opaque mode, obtained using VarHandle `getOpaque`
  and `setOpaque`, adds constraints over Plain mode that
  provide minimal awareness of a variable that is subject to interthread
  access, when all accesses use Opaque (or stronger) mode:
  

This rules out several anomalies described above with Plain mode, including those in which future accesses appear to impact the past. However, this applies only with respect to a single variable, with no assurances about orderings of accesses to other variables. As seen below, this limitation makes Opaque mode inapplicable in most interthread communication constructions.

        Per-variable overwrite order is guaranteed to be consistent
        with both the read-by relation (relating Writes to later
        Reads) and the "antidependence" (*from-read*) relation
        from Reads to later Writes -- a Read of a given Write must
        precede an observed overwrite of that Write.  As discussed
        below, RMW operations extend this by guaranteeing strict
        linear orderings between designated reads and writes.
      

If Opaque (or any stronger) mode is used for all accesses to a variable, updates do not appear out of order. Note that this would not necessarily hold if only the reads (but not writes) were performed in Opaque mode, Plain mode may skip, postpone, or reorder some writes.

        This is a defining property of cache-coherent multiprocessor
        architectures (sometimes defined as one aspect of coherence
        itself), and also (via explicit messaging) of distributed data
        stores. Progress guarantees may be formalized in terms
        of *quiescent consistency*, *eventual
        consistency*, and/or *obstruction freedom*.  These
        all have the same usage impact. For example in constructions
        in which the only modification of some variable x is for one
        thread to write in Opaque (or stronger)
        mode, `X.setOpaque(this, 1)`, any other thread spinning
        in `while(X.getOpaque(this)!=1){}` will eventually
        terminate.
      

        Note that this guarantee does *NOT* hold in Plain mode,
        in which spin loops may (and usually do) infinitely loop --
        they are not required to notice that a write ever occurred in
        another thread if it was not seen on first encounter. Opaque
        mode may also be useful in microbenchmarks to disable
        transformations that may otherwise cause computations and
        access to be optimized away in such usages.
      

The name "opaque" stems from the idea that shared variables need
  not be read or written only by the current thread, so current values
  or their uses might not be known locally, requiring interaction with
  memory systems.  However, Opaque mode does not directly impose any
  ordering constraints with respect to other variables beyond Plain
  mode. So you cannot always tell when Opaque mode will access a
  variable with respect to other plain accesses, and reading a value
  in Opaque mode need not tell you anything about values of any other
  variables. Also, while coherence ensures *some* ordering, it
  does not in itself guarantee specific orderings, in particular about
  read-write pairs (RMW and CAS operations described below extend
  coherence to do so.)  Despite these limitations, Opaque mode still
  sometimes usefully applies. For example, when monitoring and
  collecting progress indicators issued by multiple threads, it may be
  acceptable that results only eventually be accurate upon quiescence.

Opaque mode also applies when surrounding ordering constraints described below are strong enough that further ordering control has no impact, although just using Plain mode here is also OK for primitively atomic variables. In other cases, other ordering constraints in a program, combined with per-variable ordering requirements, may provide acceptable bounds on when accesses occur and/or their possible values.

  When applied to thread-confined variables (i.e., those without
  accesses in the interthread *read-by* relation), none of the
  above constraints can impact observable behavior, so Opaque mode
  access may be implemented in the same way as Local Plain access
  (which also acts coherent from the perspective of the executing
  thread.)

Opaque mode was inspired by Linux "ACCESS_ONCE". It is usable in the same contexts as C++ atomic memory_order_relaxed. Hardware implementations (as well as detailed specifications) of coherence vary across platforms, and continue to evolve. Some processors and GPUs support special non-coherent modes designed primarily for bulk transfer that are not currently accessible from Java, but may be used when applicable by JVMs.

  When contextual ordering constraints suffice to obtain required
  opaque mode properties using Plain mode, the variable and/or
  accessed should be annotated to indicate intent. A standard
  annotation `@IntentionallyWeaklyOrdered` is planned for this
  purpose.

It is almost never a good idea to use bare spins waiting for values of variables. Use Thread.onSpinWait, Thread.yield, and/or blocking synchronization to better cope with the fact that "eventually" can be a long time, especially when there are more threads than cores on a system.

  Most presentations of eventual consistency and techniques that
  exploit it, especially in distributed settings, apply it to stronger
  modes (where it also holds). See for example:
  
    ["Coordination Avoidance in Database Systems"](http://www.bailis.org/papers/ca-vldb2015.pdf) 
    by Peter Bailis et al. VLDB 2015.

Release/Acquire (or RA) mode is obtained using
  VarHandle `setRelease`, `getAcquire` and related
  methods, and adds a "cumulative" *causality* constraint to
  Opaque mode, extending partial order antecedance guarantees to cover
  the indicated (possibly weaker) accesses within the same Thread T
  (see below for some caveats about Plain mode):
  

This is the main idea behind *causally consistent* systems,
  including most distributed data stores. Causality (in the sense of
  partial ordering plus cumulativity) is essential in most forms of
  communication.  For example, if I make dinner, and then I tell you
  that dinner is ready, and you hear me, then you can be sure that
  dinner exists.  Preserving causal consistency means that, upon
  hearing "ready", you have access to its cause, "dinner". Of course,
  RA mode has no understanding of this relationship; it just preserves
  orderings. The partial order property means that causality is not
  cyclic.  As a minimal code example assuming that the only variable
  accesses are the ones shown:

```
 volatile int ready; // Initially 0, with VarHandle READY
 int dinner;         // mode does not matter here
 Thread 1                   |  Thread 2
 dinner = 17;               |  if (READY.getAcquire(this) == 1)
 READY.setRelease(this, 1); |    int d = dinner; // sees 17
```
```
 class Dinner {
   int desc;
   Dinner(int d) { desc = d; }
 }
 volatile Dinner meal; // Initially null, with VarHandle MEAL
 Thread 1                   |  Thread 2
 Dinner f = new Dinner(17); |  Dinner m = MEAL.getAcquire();
 MEAL.setRelease(f);        |  if (m != null)
                            |    int d = m.desc; // sees 17
```
The causality guarantee of RA mode is needed in producer consumer designs, message-passing designs, and many others. Nearly all java.util.concurrent components include causal "happens-before" consistency specifications in their API documentation.

  RA mode is rarely strong enough to guarantee sensible outcomes when
  it is possible for two or more threads to write the same variable at
  the same time.  Most recommended usages can be described in terms
  of *ownership*, in which only the owner may write, but others
  may read. As a basis for such reasoning, when a thread initially
  constructs an object, it is the sole owner until somehow making it
  available to other threads. Designs may additionally rely on a
  release-acquire pair acting as an ownership *transfer* --
  after making an object accessible, the (previous) owner never uses
  it again. Automatic enforcement of this rule forms the basis of most
  differences between "message passing" vs "shared memory" approaches
  to concurrency. Some special-purpose messaging components, such as
  single-producer queues, impose this restriction as a condition that
  component users must obey.  Also, locks can be used to ensure
  transient ownership, and in that sense extend Release/Acquire
  techniques. However, many uses of RA mode are conceptually closer to
  unordered "broadcasts" with multiple readers.

It is possible to use RA mode in a more explicit fashion, that also
  illustrates how it strengthens local ordering constraints.  Instead
  of `X.setRelease(this, v)`, you can use Opaque mode (or Plain
  mode if x is primitively bitwise atomic), preceded with a
  releaseFence: `VarHandle.releaseFence(); x = v;`.  And
  similarly, instead of `int v = X.getAcquire(this)`, you can
  follow a Plain or Opaque mode access with an acquireFence: `int v
  = x; VarHandle.acquireFence()`.

  A releaseFence ensures that *all* ongoing accesses (non-local
  writes and reads) complete before performing another write, which
  may impose more constraints than any given `setRelease`.  It
  is a "fence" in the sense of separating all preceding accesses vs
  all following writes. Similarly, an acquireFence ensures that all
  ongoing reads complete before performing another access. If an
  acquireFence separates two reads, the second read cannot reuse an
  old value it saw before the fence -- an acquireFence "invalidates"
  (all) prior reads. Note that fence method statements are among the
  few contexts in which using a semicolon *does* impact
  sequencing. However, effects may be interleaved with any strictly
  local accesses and computation, so still do not necessarily
  literally operate in source code order. Similarly, in an expression
  such as `X.getAcquire() + Y.get()` left-to-right evaluation
  order is preserved.

This encoding shows that, treated as events, RA fences themselves conform to the primary partial order (relying when necessary on inter-core hardware-level protocols), and the accesses are "carried" by the local precedence rules. However, RA mode accesses are not necessarily implemented using fences. They are instead defined to allow use of special-purpose access instructions when available, as well as to enable several possible optimizations. In particular, within-thread RA accesses may be implemented in the same way as Local Plain mode, or even eliminated entirely, as long as all other required constraints hold.

Release and Acquire operations provide relatively cheap ways to enable communication among threads. People have discovered techniques and idioms that can make some of these effects even cheaper to obtain.

  When preserving causal consistency in a software component, it is
  not usually necessary to use Release/Acquire mode for *every*
  access.  For example, if you read a reference to a Node with
  immutable fields in Acquire mode, you can use Plain mode to access
  the Node's fields.

  Other cases may require more care to obtain intended effects.  It is
  generally good practice to read a value using getAcquire (once) into
  a local variable (possibly marking it `final` for emphasis)
  before using in Plain mode computations, ensuring that each use will
  have the same value; java.util.concurrent code uses this SSA (static
  single assignment) based convention to improve confidence about its
  correctness.  Beware of compiler optimizations that may eliminate
  the need to access variables. For example, if an optimizing compiler
  determines that some variable x cannot be zero, then `if
  (X.getAcquire(this)!=0)` might not have any ordering
  effect. Similarly, if an optimizing compiler can precompute some or
  all parts of a Plain mode access expression (for example, an indexed
  array read), then placing the access itself after an Acquire
  operation might not have the expected effect.  Also note that a
  Release mode write does not ensure that the write be issued
  "immediately"; it is not necessarily ordered with respect to
  subsequent writes.

  Overall, moded accesses tend to be easier for compilers to optimize
  than fences when they are thread-local, and so can reduce overhead
  when conservatively thread-safe code is run in single-threaded
  contexts.  On the other hand, explicit fences are easier to manually
  optimize, and apply in cases where ordering control is not bound to
  a particular variable's access. For example, in some optimistic
  designs, possibly many possibly-Plain reads must be followed by a
  single acquireFence before performing a validation step. (This
  technique is used in java.util.concurrent.locks.StampedLock.)  And
  in some factory designs, a number of possibly-Plain mode writes
  constructing a set of objects must be followed by a releaseFence
  before they are published. These correspond to the optimization of
  moving acquireFences as early as possible, and releaseFences as late
  as possible, in both cases sometimes allowing them to be merged with
  others. A common form of hoisting applies in many linked data
  structures (including most lists and trees), where it suffices to
  use a single acquire fence or access when reading the head, so long
  as all other nodes are guaranteed to be (transitively) reachable
  only from the head. Further, if each link is quaranteed to be read
  only once during the traversal, plain mode suffices. This is one
  aspect of RCU-based techniques described by
  [McKenney](https://www.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html).

Because they impose fewer ordering constraints, RA accesses and fences are expected to be cheaper than Volatile mode operations, with respect to both overhead and opportunities for parallelism when mapped to processors. Compilers must issue code that maintains constraints with respect to platform-level memory models. It might be nice if all processors had instructions or rules corresponding exactly to memory order modes, but none do, so details of effects across them may differ. On TSO (including x86) systems, usage need not result in any extra machine instructions. On some other systems, acquires may be implemented using control instructions in accord with machine-level dependency rules. Some processors (including ARM) support a StoreStore fence that is cheaper than a releaseFence, but can be used in Release/Acquire mode only when it is known that load-store fencing cannot (or is not required to) make a difference; i.e., that it is either impossible or acceptable for an earlier read to return a value that was modified as a consequence of the later write. The VarHandle class includes StoreStoreFence as well as symmetric loadLoadFence methods that may loosen the associated RA ordering constraints when applicable. These methods exist to allow micro-optimizations that might improve performance on some platforms, without impacting others one way or the other.

As a delicate (but commonly exploited) special case of the above
  considerations, acquire-style reads of immutable fields of newly
  constructed objects do not require an explicit fence or moded access
  -- Plain mode reads suffice: If the consumer has not seen the new
  object before, it cannot have stale values that it must otherwise
  ignore or discard, and it cannot perform the read until it knows the
  address. On subsequent encounters, reusing old values is OK, because
  they cannot have changed. This reasoning rests on the only known
  defensible exception to the rule of never making assumptions about
  local precedence order: The reference (address) of a `new`
  object is assumed never to be known and impossible to speculate
  until creation. This assumption is also relied on by other Java
  security requirements.

  The resulting techniques are used in Java `final` field
  implementations, and are the reason why specified guarantees for
  final fields are conditional upon constructors not leaking
  references to objects before constructor return. Classes with final
  fields are normally implemented by issuing a form of Release fence
  upon constructor return.  Further, because nothing need be
  guaranteed about interactions with reads by the constructor, a
  StoreStoreFence suffices. Similar techniques may apply in other
  contexts, but can be unacceptably fragile. For example, code that
  works when the associated objects are always newly constructed may,
  without further safeguards, fail upon later changes to instead
  recycle the objects from pools.

 Release mode writes are compatible with C++ atomic
  memory_order_release, and Acquire mode reads are compatible with
  memory_order_acquire.  Detailed specifications underlying some of
  the optimizations described above await revision of the formal
  memory model.  In java.util.concurrent.atomic classes,
  method `setRelease` replaces the equivalent but poorly named
  `lazySet` (and similarly Unsafe.putOrderedX).
  The  [Rust](https://www.rust-lang.org/en-US/) language
  enforces ownership tracking that can help ensure appropriate use of
  RA constructions.
  The reasoning behind final fields is also seen in
  C++ memory_order_consume, which is not available as a distinct mode
  in Java.  The temporal definition of causality in terms of
  antecedence is only one facet of broader treatments of
  
    [causality (see Wikipedia for example)](https://en.wikipedia.org/wiki/Causality).

Volatile mode is the default access mode for fields qualified
  as `volatile`, or used with VarHandle `setVolatile`,
  `getVolatile` and related methods. It adds to Release/Acquire
  mode the constraint:
  

    *(Interthread) Volatile mode accesses are totally ordered.*
  

When all accesses use Volatile mode, program execution is sequentially consistent, in which case, for two Volatile mode accesses A and B, it must be the case that A precedes execution of B, or vice versa. In RA mode, they might be unordered and concurrent. The main consequences are seen in a famous example that goes by the names "Dekker", "SB", and "write skew". Using "M" to vary across modes:

```
    volatile int x, y; // initially zero, with VarHandles X and Y
    Thread 1               |  Thread 2
    X.setM(this, 1);       |  Y.setM(this, 1);
    int ry = Y.getM(this); |  int rx = X.getM(this);
  
```
It is possible to obtain the effects of Volatile mode using
  fences. The VarHandle.fullFence() method separates all accesses
  before the fence vs all accesses after the fence. Further,
  fullFences are globally totally ordered.  The effects of Volatile
  access can be arranged manually by ensuring that each is separated
  by fullFence(). Ensuring that Volatile accesses are totally ordered
  by separating them with totally ordered fences is in general more
  expensive than RA fences. Further, any pair of Volatile mode
  accesses needs only one fullFence (not two) between them, which can
  make usages difficult to optimize in a modular fashion when accesses
  may occur across different methods. The "trailing fence" convention
  reduces overhead by always encoding writes (for primitively bitwise
  atomic `x`) as `releaseFence(); x = v; fullFence();`
  and reads as `int v = x; fullFence();` (fullfence includes
  the effects of acquireFence; using just acquireFence here would
  emulate Acquire mode; see below).  Either the leading or trailing
  convention must of course be used consistently to be effective; in
  cases of uncertainty (for example, in the presence of foreign
  function calls) use both fences.

Volatile mode accesses are not necessarily implemented in this way. Some processors support special read and write instructions that do not require use of fences. Others may support instructions that are less expensive than separation using fullFence. Also, access methods are defined to allow the same kinds of optimizations as RA mode. In particular, within-thread accesses could be implemented in the same way as Local Plain mode, or even eliminated entirely, as long as all other constraints hold. In some contexts, using Volatile access with a thread-confined variable might indicate a conceptual error.

  Total ordering constraints provide a basis for ensuring
  *consensus* -- momentary agreement among threads about
  program state, such as whether a lock has been acquired, whether all
  of a set of threads have reached a barrier point, or whether an
  element exists in a collection.  (If this is not immediately obvious
  to you, you might be comforted that it took several years and
  missteps before discovery of Dekker's algorithm that extends the
  above construction to provide a simple form of two-party lock, and
  more years to generalize the idea.)  Implementations of update
  methods in most general-purpose concurrent components require at
  least one consensus operation (including cases where one is needed
  just to obtain a lock), as explained in
  
    ["The Laws of Order"](http://dl.acm.org/citation.cfm?id=1926442) by Hagit Attiya et al, POPL 2011.

  As discussed in Herlihy and Shavit's book
  
    [The Art of Multiprocessor Programming](http://booksite.elsevier.com/9780123705914/?ISBN=9780123705914), there's a hierarchy of
  operations in which each higher-consensus-number operation
  can be used to ensure some form of agreement that is impossible in
  "wait-free" bounded time/space using only lower-consensus-number
  operations. The three most commonly useful categories are available:
  

Total ordering guarantees may be overly constraining in some contexts, as illustrated by another famous example that goes by the names "IRIW" (independent reads of independent writes) and "long fork". Again using "M" to vary across modes:

```
    volatile int x, y; // initially zero, with VarHandles X and Y
    Thread 1                |  Thread 2                | Thread 3               | Thread 4
    X.setVolatile(this, 1); |  Y.setVolatile(this, 1); | int r1 = X.getM(this); |  int r3 = Y.getM(this);
                            |                          | int r2 = Y.getM(this); |  int r4 = X.getM(this);
  
```
Combinations of Volatile mode updates (writes, RMW, CAS, fences) with Acquire mode reads apply in most concurrent components. This permits partial (vs total) ordering only when reads are not paired with updates, which matches the intent of most concurrently readable data structures and other read-mostly classes with methods that advertise and maintain causal consistency, but sometimes internally employ stronger ordering due to the algorithmic need for consensus operations. This also corresponds to common goals when dealing with races: Write-Write conflicts and Read-Write conflicts must be controlled, but usually not Read-Read conflicts. This is the same idea behind Read-Write locks, but without explicit locking. It is also seen in hardware memory systems in which cache lines may be in "shared" mode across different processors only if there are no "exclusive" mode writers.

  In mixed mode usages where the *linearization* points at
  which threads must agree on the outcome of a consensus operation
  rely on the presence of fullFence operations demarcating commitment
  points, explicit use of fences may simplify implementation and
  analysis.  In particular, while Volatile writes and reads of a
  variable act as if they are separated by a fullFence, there is no
  requirement about when that fence may occur (if at all, in the case
  of thread-confinement). For example, the above Dekker construction
  is not guaranteed to work using Volatile mode write and Acquire mode
  read. However, it would suffice to use Release mode write, followed
  by an explicit fullFence, followed by Acquire mode read. Or, when
  applicable, Volatile mode CAS, followed by Acquire mode read.
  Further, Opaque read mode may suffice when clients repeatedly poll
  status before attempting a Volatile CAS-based operation,

RMW and CAS operations are also available in RA mode, supporting Acquire-only or Release-only forms. These forms maintain the strong per-variable ordering guarantee of the operation, but relax constraints for surrounding accesses. These may apply, for example when incrementing a global counter in Release mode, and reading it in Acquire mode. Not all processors support these weaker forms, in which case (including on x86) they are implemented using the stronger forms. Also, in principle, compilers may combine serially commutative RMWs such as getAndAdd as if they were parallel (when the individual return values are not used), as in "fusing" adjacent getAndAdd(_,1)'s into getAndAdd(_,2).

On some platforms, RMW and CAS operations are implemented using an instruction pair generically known as LL/SC -- "load-linked" and "store conditional". These provide only the coherence properties of the operation: store-conditional writes and returns true if the write is guaranteed to directly follow the load-linked read in coherence order. (If returning false, the hardware cannot guarantee that no other intervening write occurred.) On these platforms (including POWER and most versions of ARM), RMW or CAS operations may loop. To enable fine-tuning, VarHandle method weakCompareAndSet (weakCAS) is loopless when implemented using LL/SC, returning false if either the store-conditional failed (usually due to contention), or the current value doesn't match expected value. In usages where retries are needed in either case, using weakCAS can be more efficient. On other platforms (such as x86), the method is equivalent to plain CAS. Also, on processors that do not directly support RMW operations, they are implemented using CAS or weakCAS.

  Volatile mode is compatible with C++ atomic memory_order_seq_cst.
  Because total ordering of reads is not usually desired, there has
  been controversy among implementers about supporting it.  The
  introduction of RA mode allows programmers to choose. Alternatives
  to linearizability proofs applicable across these are the subject of
  active research; see for example work
  by  [the MPI-SWS Verification
  group](http://plv.mpi-sws.org/).

The idea of consensus can be extended to multiple variables. Some Hardware Transactional Memory systems provide extensions of CAS and LL/SC that atomically operate on more than one variable at a time. These are not yet available from Java.

Distributed data stores lack hardware coherence-based consensus
  mechanisms so must rely on protocols such as Paxos. In these
  systems, some variant of Volatile mode (most often applied to
  transactions, not single accesses) is usually called "strong
  consistency", some variant of RA "weak consistency", and further
  variants that later detect and repair conflicts in weakly consistent
  operations are "strong eventual consistent". For a survey that tries
  to clarify some of this terminology,
  see 
  ["Consistency in Non-Transactional Distributed Storage Systems"](http://dl.acm.org/citation.cfm?id=2926965)
  by Paolo Viotti and Marko Vukolic, ACM Computing Surveys 2016.
  To an extremely rough approximation, RA mode is to Volatile mode
  what UDP is to TCP.

Locked modes correspond to use of built-in `synchronized`
  blocks, as well as use of java.util.concurrent locks such as
  ReentrantLock.

In terms of ordering, acquiring locks has the same properties as Acquire mode reads, and releasing locks the same as Release mode writes. When applied to locks, the associated ordering constraints are sometimes known as "roach motel" rules -- they allow earlier reads and later writes to "move in" to lock regions, but those inside a region cannot move out.

  Lock usages cannot rely on details, which may vary across lock
  implementations.  Assuming the absence of deadlock, exclusively
  locked regions are *serializable*: They execute under mutual
  exclusion in some sequential order.  Most pure spin-locks can use RA
  mode operations to control this (for example compareAndSetAcquire
  and setRelease).  However, as noted above, most general-purpose
  locks require Volatile ordering upon lock release and/or acquisition
  to control blocking and signaling.  Also, under *biased
  locking*, when a lock is initially used by only one thread,
  heavier operations enabling others to access the lock may be
  postponed until threads reach *safe points* that are
  otherwise mainly used for triggering garbage collection.
  And `synchronized(x)` blocks where x is local or
  thread-confined may be optimized away entirely.

  Additional allowed transformations include lock *coarsening*:
  Two adjacent locked regions on the same lock can be combined, as
  in `synchronized(p) { b1; };synchronized(p) { b2; }`
  transformed to `synchronized(p) { b1; b2; }`.  Doing so acts
  as if the accesses performing unlock of the first block and the
  acquire of the second are guaranteed to be within thread, which
  allows them to be optimized away.  The resulting block can be
  further combined a finite number of times with other adjacent
  blocks. (This must be finitely bounded to maintain progress
  guarantees described above.)

  Correct use of mutual exclusion locks such as `synchronized`
  blocks and ReentrantLock maintains total ordering of locked regions.
  StampedLocks and other optimistic *seqlock*-like locks also
  enforce total orderings of writers, but may allow concurrent
  Acquire-mode (partially ordered) readers.

Locking operations introduce blocking (suspension) and scheduling policies, that fall outside the scope of this document. For specifications of the main accessible blocking primitive, see documentation of park/unpark in class LockSupport. See for example the API documentation for ReentrantLock, StampedLock, and other java.util.concurrent components for more detailed specifications of scheduling policies used in JDK.

Cycling back, locks of various kinds can be used to establish mutual exclusion, that in turn enables the reliable use of Plain mode in locked code bodies. Depending on the relative costs of locks versus ordering control instructions, uncontended lock-based code can be faster than explicitly ordered lock-free code, although with the added risks of deadlock and poorer scalability under contention. (In other words, sometimes a sequential bottleneck is the best solution available short of redesign.)

The above techniques and components are also used in the implementation of Threads themselves to arrange that thread bodies begin with Acquire and end with Release operations. Similarly, callers of Thread.start perform a Release operation and callers of Thread.join an Acquire operation.

  The accounts in this guide are compatible with (and extend) the
  
    [JSR133 (JLS5-8) Specification](http://docs.oracle.com/javase/specs/jls/se8/html/jls-17.html) (except for corrections required
  even in the absence of respecification). But instead of phrasing
  descriptions in terms of deviations from sequential consistency,
  they approach programming issues from the perspective of controlling
  parallelism.  This reflects the main usage impact of VarHandle
  memory order modes, that can be described in terms of constraints
  layered over (possibly *commutative*) Plain mode access
  rules:
  

Intermediate points across these are available by using mixed modes and/or explicit fences, but require more attention to interactions across modes. As indicated when discussing mode definitions, a few details are pending full formal specification, but none are expected to impact usage.

  Taken together, these form building blocks for creating custom
  memory consistency and caching protocols.  But they do not in
  themselves provide solutions.  As attributed
  to  [Phil
  Karlton by Martin Fowler](https://martinfowler.com/bliki/TwoHardThings.html) "There are only two hard things in
  Computer Science: cache invalidation and naming things." Concurrent
  component developers are expected to solve both, so their users
  don't need to.

As an overall guide for developers handling this potentially explosive mixture of C4 (Commutativity, Coherence, Causality, Consensus): most concurrent components must maintain causality guarantees to be usable. But some need stronger constraints for algorithmic reasons, and some are able to employ weaker modes by (perhaps transiently) arranging partial isolation, or by relaxing internal invariants, or when still useful, weakening promises from "now" to "eventually". Further, among the main requirements of concurrent components (including especially java.util.concurrent) is for component users to be satisfied with the resulting APIs and implementations, and so have no need for any of the techniques presented here.

Thanks for comments and suggestions by Aleksey Shipilev, Martin Buchholz, Paul Sandoz, Brian Goetz, David Holmes, Sanjoy Das, Hans Boehm, Paul McKenney, Joe Bowbeer, Stephen Dolan, Heinz Kabutz, Viktor Klang, Tim Peierls,

  This work is released to the public domain, as explained at
  
  [Creative Commons](http://creativecommons.org/publicdomain/zero/1.0/).

  You can also read a 
    [Portuguese translation](https://www.homeyou.com/~edu/memoria-jdk-9) by 
    [Artur Weber](https://www.homeyou.com/~edu/weber).
