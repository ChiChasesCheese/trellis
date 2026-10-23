---
title: 'Safepoints: Meaning, Side Effects and Overheads'
source: https://psy-lob-saw.blogspot.com/2015/12/safepoints.html
published: '2015-12-14'
site: psy-lob-saw.blogspot.com
clipped: '2026-10-23'
---

# Safepoints: Meaning, Side Effects and Overheads

### 

I was recently asked: "Are safepoints like safe words?". The short answer is "not really", but since I like the metaphor I'll run with it:

Imagine if you will a JVM full of mutator threads, all busy, sweating, mutating the heap. Some of them have <gasp> shared mutable state. They're mutating each others state, concurrently, like animals. Some stand in corners mutating their own state (go blind they will). Suddenly a neon sign flashes the word PINEAPPLES. One by one the mutators stop their rampant heap romping and wait, sweat dripping. When the last mutator stops, a bunch of elves come in, empty the ashtrays, fill up all the drinks, mop up the puddles, and quickly as they can they vanish back to the north pole. The sign is turned off and the threads go back to it....

There are many references to Safepoints to be found online and what follows here is my attempt at a more nuanced use/definition, no sweating mutators from this point onwards.

A 

This is particularly useful when the JVM wishes to examine or change the heap, for a GC or any one of many other reasons. If references on the stack were unaccounted for and the JVM was to run a GC it may miss the fact that some objects are still alive (referenced from the stack) and collect them, or it may move some object without updating it's reference on the stack leading to memory corruption.

Imagine if you will a JVM full of mutator threads, all busy, sweating, mutating the heap. Some of them have <gasp> shared mutable state. They're mutating each others state, concurrently, like animals. Some stand in corners mutating their own state (go blind they will). Suddenly a neon sign flashes the word PINEAPPLES. One by one the mutators stop their rampant heap romping and wait, sweat dripping. When the last mutator stops, a bunch of elves come in, empty the ashtrays, fill up all the drinks, mop up the puddles, and quickly as they can they vanish back to the north pole. The sign is turned off and the threads go back to it....

*<inner-dialogue>Too much? It's like 35c in the shade here, so sweating is like... no? never mind </inner-dialogue>*
There are many references to Safepoints to be found online and what follows here is my attempt at a more nuanced use/definition, no sweating mutators from this point onwards.

A **safepoint** is a range of execution where the state of the executing thread is well described. **Mutator** threads are threads which manipulate the JVM heap (all your Java Threads are **mutators**. Non-Java threads may also be regarded as **mutators** when they call into JVM APIs which interact with the heap).

**At a safepoint** the **mutator** thread is at a known and well defined point in it's interaction with the heap. This means that all the references on the stack are mapped (at known locations) and the JVM can account for all of them. As long as the thread remains **at a safepoint** we can safely manipulate the heap + stack such that the thread's view of the world remains consistent when it leaves the safepoint.

A JVM will therefore need means of bringing threads to safepoints (and keeping them there) so that all sorts of runtime magic can happen. Here's a partial list of activities which JVMs run only once all mutator threads are at a safepoint 

__and cannot leave it until released__(at a**global safepoint**), these are sometime called**safepoint operations**:
- Some GC phases (the Stop The World kind)
- JVMTI stack sampling methods (not always a global safepoint operation for Zing))
- Class redefinition
- Heap dumping
- Monitor deflation (not a global safepoint operation for Zing)
- Lock unbiasing
- Method deoptimization (not always)
- And many more!

A 

Note that the distinction between requesting a

[great talk by Azul's own John Cuthbertson from JavaOne 2014](https://www.parleys.com/tutorial/with-gc-solved-what-else-makes-jvm-pause)goes into some background on Safepoints and allot of details about safepoint operations other than GC (we at Azul feel GC is a solved problem, so the talk goes into the remaining reasons to stop).
Note that the distinction between requesting a

**global safepoint**and a**thread safepoint**exists only for some JVM implementations (e.g.**Zing**, the Azul Systems JVM.__Reminder: I work for Azul__). Importantly it does**not**exist on OpenJDK/Oracle JVMs. This means that Zing can bring a single thread to a safepoint.
To summarize:

- Safepoints are a common JVM implementation detail
- They are used to put mutator threads on hold while the JVM 'fixes stuff up'
- On OpenJDK/Oracle every safepoint operation requires a **global safepoint**
- All current JVMs have some requirement for **global safepoints**

### When is my thread at a safepoint?

So having threads at a safepoint allows the JVM to get on with it's managed runtime magic show, great! When is this groovy state happening?

- A Java thread is **at a safepoint** if it is blocked on a lock or synchronized block, waiting on a monitor, parked, or blocked on blocking IO. Essentially these all qualify as orderly de-scheduling events for the Java thread and as part of tidying up before put on hold the thread is brought to a safepoint.
- A Java thread is **at a safepoint** while executing JNI code. Before crossing the native call boundary the stack is left in a consistent state before handing off to the native code. This means that the thread can still run while**at a safepoint** .
- A Java thread which is executing bytecode **is NOT at a safepoint**  (or at least the JVM cannot assume that it is at a safepoint).
- A Java thread which is interrupted (by the OS) while not at a safepoint is not brought to a safepoint before being de-scheduled.

- The JVM cannot force any thread into a safepoint state.
- The JVM can stop threads from leaving a safepoint state.

__known state__, not just interrupting i

__t__. To achieve this goal JVMs have the Java threads suspend themselves at convenient spots if they observe a 'safepoint flag'.

### Bringing a Java Thread to a Safepoint

Java threads poll a 'safepoint flag' (global or thread level) at 'reasonable' intervals and transition into a safepoint state (thread is blocked at a safepoint) when they observe a 'Go to safepoint' flag. This is simple enough, but since we don't want to spend all of our time checking if we need to stop the C1/C2 compilers (-client/-server JIT compilers) try and keep safepoint polls to a minimum. On top of the cost of the flag check itself, maintaining a 'known state' adds significant complexity to the implementation of certain optimizations and so keeping safepoints further apart opens up a wider scope for optimization. These considerations combined lead to the following locations for
**safepoint polls:**

- Between any 2 bytecodes while running in the interpreter (effectively)
- On 'non-counted' loop back edge in C1/C2 compiled code
- Method entry/exit (entry for Zing, exit for OpenJDK) in C1/C2 compiled code. Note that the compiler will remove these safepoint polls when methods are inlined.

- **'{poll}'** or '**{poll return}'** on OpenJDK, this will be in the instructions comments
- '**tls.pls_self_suspend** ' on Zing, this will be the flag examined at the poll operation

- On Oracle/OpenJDK a blind TEST of an address on a special memory page is issued. Blind because it has no branch following it so it acts as a very unobtrusive instruction (usually a TEST is immediately followed by a branch instruction). When the JVM wishes to bring threads to a safepoint it protects the page causing a SEGV which is caught and handled appropriately by the JVM. There is one such special page per JVM and therefore to bring any thread to a safepoint we must bring all threads to a safepoint.
- On Zing the safepoint flag is thread local (hence the tls prefix). Threads can be brought to a safepoint independently.

[Dude, Where's My Safepoint?](https://psy-lob-saw.blogspot.com/2014/03/where-is-my-safepoint.html)for more details on polls.

Once a thread detects the safepoint flag it will perform the safepoint action that the poll triggers. This normally means blocking on some sort of JVM level lock, to be released when the safepoint operation is over. Think of it as a locking mechanism where:

- Threads can lock themselves out (e.g. by calling into JNI, or blocking at a safepoint).
- Threads can try and re-enter (when returning from JNI), but if the lock is held by the JVM they will block.
- The **safepoint operation** requests the lock and blocks until it own it (when all the mutators have locked themselves out)

### All Together Now

Now we have all the moving parts of the safepoint process:
- Safepoint triggers/operations: reasons to request, and stuff to do which requires one or all threads to be at a safepoint
- Safepoint state/lock: into which Java threads can voluntarily check in, but can only leave when the JVM is done executing the safepoint operation
- Safepoint poll: the voluntary act by a Java thread to go into a safepoint if one is needed

**GREEN : Executing Java**

**YELLOW : Descheduled Java**

**RED : Native**

This diagram highlights several components of safepoint operation overheads:

1. Time To Safe Point(TTSP): Each thread enters a safepoint when it hits a safepoint poll. But arriving at a safepoint poll requires executing an unknown number of instructions. We can see J1 hits a safepoint poll straight away and is suspended. J2 and J3 are contending on the availability of CPU time. J3 grabs some CPU time pushing J2 into the run queue, but J2  is not in a safepoint. J3 arrives **at a safepoint** and suspends, freeing up the core for J2 to make enough progress to get to a safepoint poll. J4 and J5 are already at a safepoint while executing JNI code, they are not affected. Note that J5 is trying to leave JNI halfway through the safepoint and is suspended before resuming Java code. Importantly we observe that the time to safepoint varies from thread to thread and some threads are paused for longer than others, Java threads which take a long time to get to a safepoint can delay many other threads.
2. Cost of the **safepoint operation** : This will depend on the operation. For GetStackTrace the cost of the operation itself will depend on the depth of the stack for instance. If your profiler is sampling many threads (or all the threads) in one go (e.g. via JVMTI::GetAllStackTraces) the duration will grow as more threads are involved. A secondary effect may be that the JVM will take the opportunity to execute some other safepoint operations while the going is good.
3. Cost of resuming the threads.

1. Long TTSP can dominate pause times: some causes for long TTSP include page faults, CPU over-subscription, long running counted loops.
2. The cost of stopping all threads and starting all threads scales with the number of threads. The more threads the higher the cost. Assuming some non-zero cost to suspend/resume and TTSP, multiply by number of threads...
3. Add -XX:+PrintGCApplicationStoppedTime to your list of favourite flags! It prints the pause time and the TTSP.

[Azul Systems on the Zing JVM](https://www.azul.com/products/zing/), so feel free to assume bias on my part. My main motivation in including both JVMs is so that I can demonstrate the effect of -XX:+KeepSafepointsInCountedLoops on Zing.

NOTE: The benchmarks are not intended to spark a flame war and though Zing happens to compile this particular piece of code 'better' I would not get over excited about it. What is exciting is the extra option Zing makes available here to control and minimize TTSP, and the additional perspective it offers on how a JVM can deal with these challenges.

### Example 0: Long TTSP Hangs Application

The above code should exit in 5 seconds (or 

The reason it's so stuck is because the computation is running in a 'counted' loop, and counted loops are considered short by the JVM. Short enough to not have safepoints. This thread refusing to come to a safepoint will lead to all other threads suspending indefinitely at the next safepoint operation.

We can fix this (somewhat contrived) problem in several ways:

[see it on GitHub](https://github.com/nitsanw/safepoint-experiments/blob/master/src/main/java/safepoint/hang/WhenWillItExitInt.java)). The silly computation running in the daemon thread should not stop it from exiting (the JVM should exit if all remaining running Java threads are daemon threads). But if we run this sample we will find that the JVM does not exit after 5 seconds. It doesn't exit at all**[UPDATE: this example turned out to be a bit flaky as per discussion in comments and following**. Not only does it not exit, it will also refuse incoming JMX connections, it won't respond the jmap/jstack. It won't naturally die, you'll have to 'kill -9' this fucker.[blog post](http://psy-lob-saw.blogspot.co.za/2016/02/wait-for-it-counteduncounted-loops.html)]
The reason it's so stuck is because the computation is running in a 'counted' loop, and counted loops are considered short by the JVM. Short enough to not have safepoints. This thread refusing to come to a safepoint will lead to all other threads suspending indefinitely at the next safepoint operation.

We can fix this (somewhat contrived) problem in several ways:

1. Prevent C1/C2 compilation: Use -Xint or a compile command to prevent the method compilation. This will force safepoint polls everywhere and the thread will stop hurting the JVM.
2. Replace the index type with long: this will make the JVM consider this loop as 'uncounted' and include a safepoint poll in each iteration.
3. On Zing you can apply the -XX:+KeepSafepointsInCountedLoops option on either the JVM or method level (via a -XX:CompileCommand=option,... or via a compiler oracle file). This option is [coming shortly to an OpenJDK near you](https://bugs.openjdk.java.net/browse/JDK-6869327) . See also related bug where[breaking the loop into an inner/outer loop with safepoints in the outer loop](https://bugs.openjdk.java.net/browse/JDK-5014723) is discussed.

**Summary:**Delaying a**safepoint poll**indefinitely can be harmful...
### Example 1: More Running Threads -> Longer TTSP, Higher Pause Times

**safepoint operation**by calling

*safepointMethod()*(in this case the

*System.gc()*will be called as a result) and many threads scanning a byte array. The byte array scan loop will not have a

**safepoint poll**(it's a counted loop), so the size of the array will act as our intended

**safepoint poll interval**. With this setup we can control the frequency of safepoint operations (with some overhead), avg. distance from safepoint poll and with JMH the number of threads. We can use -XX:+PrintGCApplicationStoppedTime to log the stopped time and TTSP. Armed with this experiment we can now find a large machine to play on and see what happens. I use the command line '-tg' parameter to control the number of threads executing the

*contains1()*method.

So, here goes on a 48 core Haswell Xeon machine, Cent OS, I'll be using Oracle 8u60. The benchmark class I'm running is

[here](https://github.com/nitsanw/safepoint-experiments/blob/master/src/main/java/safepoint/fair/SafepointUsingGc.java).

Lets start with no

*contains1()*threads and explain the method and data collection as we go along:

$ java -jar safepoints.jar -f 1 -i 10 -wi 10 -jvmArgs="-XX:+PrintGCApplicationStoppedTime -Xms1g -Xmx1g" -tg 0,0,0,1 SafepointUsingGc

There's 4 thread groups because I add another benchmark to run with this crowd in the next sample.

This spouts allot of PrintGCApplicationStoppedTime printouts similar to:

Total time for which application threads were stopped: 0.0180172 seconds, Stopping threads took: 0.0000513 seconds

I'm no Unix shell guru, but with some googling even I can AWK something to summarize this shit:

grep 'Total time' output.file | awk '{ stopped += $9;ttsp += $14; n++ } END { if (n > 0) print "stopped.avg=" stopped / n ", ttsp.avg=" ttsp / n; }'

It's summing up the warmup period measurements as well, but I'm willing to let it ride. So with that in mind, lets compare the benchmark output with the reported pause times:

SafepointUsingGc.run_together:safepoint 100 10 32768 true avgt 10 118611444.689 ± 1288530.618 ns/op

stopped.avg=0.015759, ttsp.avg=6.98995e-05

Or formatted for humans:

__park+gc(ms) |Stp.ms|TTSP.ms|__
119 ± 1.0 | 16.1 | 0.07 |

We went with the default intervalMs=100, so we'd expect the

*safepoint()*cost to be around 100 + stopped.avg, it's actually 2ms more than that. This is why we have the

*park()*benchmark to baseline against. Running again with the park group enabled ('-tg 0,0,1,1'):

__park(ms) | park+gc(ms) |Stp.ms|TTSP.ms|__
101 ± 0.8 | 118 ± 1.4 | 15.9 | 0.07 |

We can see that there's some variance to the GC call and some scheduling variance which can account for delta between our expected value and actual. Small potatoes, lets move on. Start with measuring the cost of the

*contains1()*call when we're not slapping it with a GC every 100ms ('-tg 1,0,1,0' we're running the park baseline):

__contains1(us) | park(ms) |Stp.ms|TTSP.ms|__
32.2 ± 0.02 | 100.1 ± 0.0 | 0.0 | 0.0 |

Note the

*contains1()*method cost is in microseconds. Awesome, now lets ramp up the number of

*contains1()*thread with the GC thread running every 100ms:

__T |contains1(us) | park(ms) | park+gc(ms) |Stp.ms|TTSP.ms|__
1 | 51.4 ± 3.1 | 100.7 ± 0.7 | 117.5 ± 0.7 | 15.1 | 0.1 |

2 | 49.5 ± 17.1 | 101.6 ± 1.9 | 116.9 ± 0.5 | 14.4 | 0.1 |

4 | 45.5 ± 2.6 | 102.8 ± 4.0 | 116.9 ± 0.7 | 14.4 | 0.1 |

8 | 45.6 ± 2.1 | 103.6 ± 5.6 | 114.0 ± 0.7 | 13.3 | 0.1 |

16 | 46.8 ± 1.3 | 103.4 ± 6.8 | 115.0 ± 1.5 | 12.8 | 0.2 |

32 | 65.7 ± 2.0 | 101.8 ± 0.9 | 113.0 ± 1.3 | 11.4 | 0.7 |

64 | 121.9 ± 1.9 | 106.0 ± 8.1 | 116.1 ± 1.4 | 14.5 | 5.4 |

128 | 251.9 ± 6.6 | 103.6 ± 5.3 | 119.6 ± 2.3 | 16.9 | 6.4 |

256 | 513.2 ± 13.4 | 109.2 ± 9.7 | 123.4 ± 1.7 | 20.7 | 8.0 |

512 |1111.3 ± 69.7 | 143.9 ±24.8 | 134.8 ±15.3 | 27.8 | 10.0 |

OK, that escalated not so quickly. Keep in mind we only actually have 48 cores (hyper-threaded), and so when we cross the line between 32 and 64 we are now looking at the effect of contention and scheduling on the TTSP. It is evident that if you have more CPU bound threads than CPUs performance will degrade, but that is not really what we're after.

At 1 thread we already see a big drop in performance for

We can see a steady growth in TTSP while within the core count, going from 0.1ms to 0.7ms, this is bad news to anyone looking to keep their latencies in the low microseconds count as touched upon in

Once we have more threads than cores the TTSP cost goes into the milliseconds, but escalates rather slowly once there. Going from 5ms to 10ms while we go from 64 to 512 threads is better than I expected.

At 1 thread we already see a big drop in performance for

*contains1()*. This is somewhat understandable in the presence of 15ms stolen from the application every 100ms. But where you'd expect a 15% difference we're actually looking at a far more significant drop in performance. Going from 32us to 51us kinda sucks.
We can see a steady growth in TTSP while within the core count, going from 0.1ms to 0.7ms, this is bad news to anyone looking to keep their latencies in the low microseconds count as touched upon in

[this post from the brilliant Mark Price](https://www.lmax.com/blog/staff-blogs/2015/08/05/jvm-guaranteed-safepoints/). Mark highlights the fact that the JVM regularly calls for a global safepoint ([“whether she needed it or not”](http://muslimvilla.smfforfree.com/index.php?topic=3219.0;wap2)), so you may find to your delight that these little hiccups come round even when you've been allocating nothing.
Once we have more threads than cores the TTSP cost goes into the milliseconds, but escalates rather slowly once there. Going from 5ms to 10ms while we go from 64 to 512 threads is better than I expected.

**Summary:**By increasing the thread count we increase the TTSP. CPU over-subscription will lead to a further increase in TTSP. Monitor machines load avg to detect this kind of misconfiguration.
### Example 2: Long TTSP has Unfair Impact

Building on previous benchmark, but now we have 2 methods: 

1 | 32.3 ± 0.1 | 34.8 ± 1.7 | 100.0 ± 0.0 | 0.0 | 0.0 |

10 | 32.4 ± 0.5 | 349.7 ± 18.0 | 100.0 ± 0.0 | 0.0 | 0.0 |

100 | 38.4 ± 2.8 | 3452.7 ± 130.4 | 100.0 ± 0.0 | 0.2 | 0.1 |

1000 | 39.8 ± 1.1 | 33419.9 ± 421.6 | 100.0 ± 0.0 | 0.0 | 0.0 |

10000 | 41.7 ± 5.0 | 336112.5 ± 10306.5 | 100.5 ± 1.7 | 0.0 | 0.0 |

Indeed the cost of

Here's what happens as we throw in the safepoint ops:

*contains1()*and*contains1toK()*.*contains1toK()*is K times further away from a**safepoint poll**(outer loop is counted, the contains needle methods gets inlined removing the method exit safepoint and the loop inside it is counted). By increasing K we can see the impact of one thread on the other, in particular we expect the cost of*contains1()*to increase as the cost of*contains1toK()*increases, in the presence of**safepoint operations**. The unfairness here being that while*contains1toK()*is making progress it is making*contains1(legen...)*wait for it (...DARY!). Because using GC as the safepoint operation is rather heavy handed (even though it's a small heap and there's no garbage) we'll switch to using another**safepoint operation**for this case:*ManagementFactory.getThreadMXBean().findDeadlockedThreads()*. This is allot more lightweight than GC but becomes more expensive as we pile on threads (not by that much, but still) so I did not use it for prior example (though come to think of it the number of threads should also impact GC length a bit, oh well). Anyway, variety is the spice of life. Here's the results with both methods and*park()*, but no**safepoint operation**(benchmark class is[here](https://github.com/nitsanw/safepoint-experiments/blob/master/src/main/java/safepoint/fair/SafepointUsingFindDeadlocks.java)):

__K |contain1(us)| containsK(us) | park(ms) |Stp.ms|TTSP.ms|__
1 | 32.3 ± 0.1 | 34.8 ± 1.7 | 100.0 ± 0.0 | 0.0 | 0.0 |

10 | 32.4 ± 0.5 | 349.7 ± 18.0 | 100.0 ± 0.0 | 0.0 | 0.0 |

100 | 38.4 ± 2.8 | 3452.7 ± 130.4 | 100.0 ± 0.0 | 0.2 | 0.1 |

1000 | 39.8 ± 1.1 | 33419.9 ± 421.6 | 100.0 ± 0.0 | 0.0 | 0.0 |

10000 | 41.7 ± 5.0 | 336112.5 ± 10306.5 | 100.5 ± 1.7 | 0.0 | 0.0 |

Indeed the cost of

*contains1toK()*grows linearly with K and the 2 methods don't seem to impact each other that significantly.
Here's what happens as we throw in the safepoint ops:

__K |contains1(us)| containsK(us) | park(ms) | park+FDT(ms) |Stp.ms |TTSP.ms|__
1 | 39.7 ± 0.9 | 39.6 ± 1.4 | 100.0 ± 0.0 | 100.3 ± 0.0 | 0.1 | 0.1 |

10 | 40.0 ± 1.0 | 400.1 ± 14.4 | 100.0 ± 0.0 | 100.5 ± 0.0 | 0.2 | 0.2 |

100 | 41.8 ± 1.1 | 3835.4 ± 141.2 | 100.1 ± 0.0 | 102.7 ± 0.1 | 2.1 | 2.0 |

1000 | 67.4 ± 3.5 | 37535.7 ± 2237.2 | 102.5 ± 1.9 | 127.1 ± 1.1 | 20.7 | 20.7 |

10000 | 183.4 ± 8.5 | 346048.6 ± 9818.2 | 194.9 ± 11.5 | 348.4 ± 11.4 | 152.8 | 152.8 |

A terrible thing, right? The annoying/unfair thing is that being a shit has no effect on

*contains1toK()*performance. It scales linearly and seems oblivious to the havoc it's wrecking for everyone else. Note that the problem we see here was present in the run where no safepoint operations were invoked, there were just no safepoint operations to bring it out. On a long enough timeline a safepoint operation will come along and around it we'll have seen the same issue.

How can we fix it, and at what cost? Lets explore some options.

#### Solution 1: I use Zing -> use -XX:+KeepSafepointsInCountedLoops

So Zing is super awesome, and has this option to keep safepoint polls in counted loops which can come in handy in cases where one particular method is killing you softly with TTSP. Here's the results we get with Zing when running the benchmark above (same jvmArgs, same machine etc):

__K |contains1(us) | containsK(us) | park(ms) | park+FDT(ms) | Stp.ms|__
1 | 31.9 ± 0.9 | 30.5 ± 1.0 | 100.0 ± 0.0 | 100.2 ± 0.0 | 0.0 |

10 | 32.9 ± 0.2 | 317.8 ± 8.8 | 100.0 ± 0.0 | 100.2 ± 0.0 | 0.0 |

100 | 34.1 ± 2.4 | 3337.8 ± 265.4 | 100.1 ± 0.0 | 100.8 ± 0.2 | 0.4 |

1000 | 44.4 ± 1.9 | 33991.6 ± 1199.0 | 100.9 ± 0.2 | 117.0 ± 0.6 | 10.2 |

10000 | 159.0 ± 12.1 |299839.3 ± 6297.2 | 156.3 ± 8.0 | 319.8 ± 30.5 | 113.4 |

Still bad, but Zing happens to squeeze better performance from the

*containsNeedle()*method and while

*contains1()*performance degrades it's opening a wide gap with observed behaviour above probably because less time is lost to TTSP (because

*contains1toK()*finishes quicker). Also note that -XX:+PrintGCApplicationStoppedTime only prints out the stopped time for Zing. A separate command line argument is available which prints out safepoint statistics, but as this post grows longer I'm losing my will to rerun and parse stuff...

We add the JVM argument: "-XX:CompileCommand=option,*.contains1ToK,+KeepSafepointsInCountedLoops" and watch the world burn:

__K |contain1(us)| containsK(us) | park(ms) | park+FDT(ms)| Stp.ms|__
1 | 33.0 ± 0.6 | 40.1 ± 1.2 | 100.0 ± 0.0 | 100.2 ± 0.0 | 0.0 |

10 | 32.8 ± 0.7 | 405.1 ± 13.1 | 100.0 ± 0.0 | 100.2 ± 0.0 | 0.0 |

100 | 33.3 ± 0.7 | 4124.8 ± 104.4 | 100.0 ± 0.0 | 100.3 ± 0.0 | 0.1 |

1000 | 32.9 ± 0.2 | 40839.6 ± 854.0 | 100.0 ± 0.0 | 101.0 ± 0.3 | 0.6 |

10000 | 40.2 ± 2.9 | 374935.6 ± 7145.3 | 111.3 ± 3.7 | 100.2 ± 0.0 | 0.0 |

SHAZZZING!... This is pretty fucking awesome

*.*The impact on

*contains1toK()*is visible, but I didn't have to change the code and the TTSP issue is

[gone man, solid GONE](https://www.youtube.com/watch?v=CEEPaYD5KZE&feature=youtu.be&t=147). A look at the assembly verifies that the inner loop is still unrolled within the outer loop, with the addition of the requested

**safepoint polls**. There are more safepoint polls than I'd like here, since the option is applied to both the outer method and the inlined method (to be improved upon sometime down the road...).

#### Solution 2: I use OpenJDK/Oracle, disable inner loop inlining

If the inner loop is in it's own method as our example, or if we can perhaps modify the code such that it is, we can ask the compiler to not inline that method. This should work out nicely here. To force the JVM to not inline the
*containsNeedle()*method only in

*contains1toK()*I made a copy of

*containsNeedle()*called

*containsNeedle2()*and used this argument: "-XX:CompilerCommand=dontinline,*.containsNeedle2". The results:

__K |contain1(us)| containsK(us) | park(ms) | park+FDT(ms)|Stp.ms|TTSP.ms|__
1 | 39.9 ± 1.0 | 40.0 ± 2.6 | 100.0 ± 0.0 | 100.3 ± 0.0 | 0.1 | 0.0 |

10 | 39.9 ± .7 | 395.6 ± 10.0 | 100.0 ± 0.0 | 100.3 ± 0.0 | 0.1 | 0.0 |

100 | 41.3 ± 3.9 | 4030.6 ± 405.0 | 100.0 ± 0.0 | 100.3 ± 0.0 | 0.1 | 0.0 |

1000 | 39.6 ± 2.1 | 34543.8 ± 1409.9 | 100.0 ± 0.0 | 100.3 ± 0.0 | 0.1 | 0.0 |

10000 | 39.1 ± 1.2 | 328380.6 ± 8478.1 | 100.0 ± 0.0 | 100.3 ± 0.0 | 0.1 | 0.0 |

That worked well! No harm to 

*contains1()*, no TTSP issue, and*contains1toK()*performance didn't suffer for it. Inlining is usually a key optimization you want to make sure happens, but in this case the right thing to do is stop it from happening. The work inside*containsNeedle()*is chunky enough to make this a good tradeoff. If the external loop was at a very high count, and the array size rather small this would have been a very different story.
#### Solution 3: Last resort. stop compiling the offending method

This is a bit terrible, but if things get bad AND you can't change the code, you can use a CompileCommand to exclude the method from compilation. The method will be force to stay in the interpreter, so will effectively have a 

**safepoint poll**between every 2 bytecodes. Performance will suck, but at least the application will be responsive. I am not gonna run this option, but if you want to add the following argument to the command line and watch it roll: "-XX:CompilerCommand=exclude,*.contains1toK"
**Summary:**Threads which suffer from large TTSP will cause other threads to wait for them in the presence of a global safepoint attempt.

### Example 3: Safepoint Operation Cost Scale

For this example we replace the

*safepoint()*method with gathering thread stacks using

*ManagementFactory.getThreadMXBean().dumpAllThreads(false, false)*. Gathering thread stacks also occurs at a safepoint and the safepoint operation cost will scale with the number of threads. We construct a number of idle threads in the setup method to control the

**safepoint operation**cost. To make sampling the threads stack expensive we park the fuckers 256 frames deep.

Different

**safepoint operations**scale with different aspects of your process. Certain GC algorithms stop the world phases will scale with heap size. Profiling by collecting thread dumps (as done by JVisualVM sampler for instance) will scale with the number of threads (idle or not) and the stack depth. Deflating monitors will scale with the number of monitors in your application etc.

Here's what happens as we pile on the idle threads (running only

*contains1()*):

**IT | contain1(us)| park(ms) | park+DTS(ms) | Stp.ms|TTSP.ms|**
0 | 38.0 ± 1.6 | 100.0 ± 0.0 | 100.5 ± 0.0 | 0.2 | 0.0 |

1 | 40.7 ± 1.4 | 100.1 ± 0.0 | 102.2 ± 0.0 | 0.6 | 0.0 |

10 | 44.7 ± 0.8 | 100.2 ± 0.1 | 117.2 ± 0.1 | 5.5 | 0.0 |

100 | 75.5 ± 0.8 | 122.6 ± 3.5 | 261.9 ± 2.3 | 61.3 | 0.1 |

1000 | 204.5 ± 38.5 | 257.5 ± 28.8 | 1414.2 ± 47.0 | 313.0 | 1.0 |

We get long stops and short TTSPs! hoorah! You can play with the number of threads and the depth of the stack to get the effect you want. It is interesting that most profilers using JVMTI::Get*StackTrace opt for sampling all threads. This is risky to my mind as we can see above the profiling overhead is open ended. It would seem reasonable to sample 1 to X threads (randomly picking the threads we sample) to keep the overhead in check on the one hand and pick a reasonable balance of TTSP vs operation cost on the other.

As mention previously, JVMTI::GetStackTrace does not cause a global safepoint on Zing. Sadly AFAIK no commercial profilers use this method, but if they did it would help. The JMX thread bean does expose a single thread profiling method, but this only delegates to the multi-thread stack trace method underneath, which does cause a global safepoint...

**Summary:**This final step adds another interesting control for us to play with completing our set:

- **Safepoint poll** interval -> Will drive time to safepoint. CPU scarcity, swapping and page faults are other common reasons for large TTSP.
- **Safepoint operation** interval -> Sometimes in your control (be careful how you profile/monitor your application), sometimes not.
- **Safepoint operation cost** -> Will drive time in safepoint. Will depend on the operation and your application specifics. Study your GC logs.

### Example 4: Adding Safepoint Polls Stops Optimization

This is a repeat of a benchmark I ran to demonstrate the side effect of safepoint polls in loops on loop optimizations in 

The benchmark:

We are debating replacing the length and DataSet index types from int to longs. The impact on usage inside loops is substantial as demonstrated by the following results:

copyInt 1000 avgt 5 76.943 ± 14.256 ns/op

copyLong 1000 avgt 5 796.583 ± 55.583 ns/op

equalsInt 1000 avgt 5 367.192 ± 16.398 ns/op

equalsLong 1000 avgt 5 806.421 ± 196.106 ns/op

fillInt 1000 avgt 5 84.075 ± 19.033 ns/op

fillLong 1000 avgt 5 567.866 ± 10.154 ns/op

sumInt 1000 avgt 5 338.204 ± 44.529 ns/op

sumLong 1000 avgt 5 585.657 ± 105.808 ns/op
There are several optimizations negated by the transition from counted to un-counted loop (uncounted loops currently include loops limited by a long, and therefore include a safepoint):

The latter 2 have been [the context of changing one of the Netty APIs](https://github.com/netty/netty/pull/3969#issuecomment-132559757). This post is so long by now that if you had the strength to read this far you can probably click through to the ticket. I'll quote the basic results here for completeness.
The benchmark:

We are debating replacing the length and DataSet index types from int to longs. The impact on usage inside loops is substantial as demonstrated by the following results:

**Benchmark (size) Mode Cnt Score Error Units**
copyInt 1000 avgt 5 76.943 ± 14.256 ns/op

copyLong 1000 avgt 5 796.583 ± 55.583 ns/op

equalsInt 1000 avgt 5 367.192 ± 16.398 ns/op

equalsLong 1000 avgt 5 806.421 ± 196.106 ns/op

fillInt 1000 avgt 5 84.075 ± 19.033 ns/op

fillLong 1000 avgt 5 567.866 ± 10.154 ns/op

sumInt 1000 avgt 5 338.204 ± 44.529 ns/op

sumLong 1000 avgt 5 585.657 ± 105.808 ns/op

- Loop unrolling : This is not really a safepoint issue, can be fixed as per the KeepSafepointsInCountedLoops option
- Fill pattern replacement (-XX:+OptimizeFill): the current fill implementation has no safepoints and the loop pattern it recognizes does not allow it.
- Superword optimizations (-XX:+UseSuperword): current Superword implementation doesn't allow for long loops. This will probably require the compiler to construct an outer loop with an inner superword loop

[discussed on this blog before in some detail](http://psy-lob-saw.blogspot.co.za/2015/04/on-arraysfill-intrinsics-superword-and.html).

### Final Summary And Testament

[If you've read this far, you deserve a summary, or a beer, or something. WELL DONE YOU!!! Here's what I consider the main takeaways from this discussion/topic:](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgkvriHNHxT7Q_9tJ2rzTunNLxjR9rQRuDy596Af1U52fKCzI-9JUGGC5_rFKCUHg4Xn35tKOTipGiuJFwkRhW76T_Zq1NHwH4fdbMP6lkmWQxuATfeNP2Of3i21Q5_2pBfqfFzLgFl1EY/s1600/fmercury-thumbsup.jpeg)

- Safepoint/Safepoint poll/Safepoint operation are 3 distinct terms, often mingled. Separating them allows us to consider their costs and impacts individually.
- In most discussions the term Safepoint is used to describe a global safepoint. Some JVMs can control safepoint transition on the thread level. By considering the individual thread state we can more easily reason about the transition costs on a thread by thread level.
- The failure of any thread to reach a safepoint (by hitting a safepoint poll) can cripple the whole JVM. In this sense most any bit of Java code can be considered blocking (as in not lock free). Consider for example a CAS loop, it's not counted, it will have a safepoint poll in it, the thread executing can be blocked indefinitely if another Java thread is suspended while not at a safepoint.
- JVMs have many safepoint operations. If you are worried about their impact you should enable -XX:+PrintGCApplicationStoppedTime. Further detail on what types of safepoint operations were involved can be made available using -XX:+PrintSafepointStatistics –XX:PrintSafepointStatisticsCount=X. Try it out, it's educational.

### References

- From the [OpenJDK Runtime Overview](http://openjdk.java.net/groups/hotspot/docs/RuntimeOverview.html#Thread%20Management|outline) look for the "VM Operations and Safepoints" section. Note that the term safepoint is used here to mean a global safepoint.
- [J.Bempel's post](http://jpbempel.blogspot.co.za/2013/03/safety-first-safepoints.html) covering many safepoint operations and observing the impact of safepoints.
- [Alexey Ragozin's post](http://blog.ragozin.info/2012/10/safepoints-in-hotspot-jvm.html) also covers similar definition to the Runtime Overview and explores the safepoint poll mechanism and logging options.
- [Gil Tene post on the Mechanical Sympathy mailing list](https://groups.google.com/forum/#!msg/mechanical-sympathy/GGByLdAzlPw/cF1_XW1AbpEJ) which closely matches the "Thread State" approach above. Gil goes into the topic in the context of Unsafe operations and assumptions surrounding safepoints.

-go blind they will- lol!!!

ReplyDelete
Hm, WhenWIllItExit exits alright for me

ReplyDelete
tried with 8u31 on windows and 8u45 on linux

The timing of the compilation matters here. On a fast enough machine less time is sufficient for C2/C1 compilation to compile the safepoint out. Extend the sleep time to 10/15/20 seconds and see if it works.

Delete
Also, well done on testing out the code!!!! I would buy you a beer for that alone. A critical reader is good to find.

Delete
I'm seeing the same result as Oleg. Mac OS X, JDK 1.8.0_65. I turned on the appropriate JVM flags and observe that method recompilation happens after about 2.5 seconds. The method disassembly includes a {poll} on the inner for loop.

Delete
OK, I've now managed to reproduce the different results, the outcome is interesting. It seems that if I save the class from Eclipse and run it (from Eclipse or command line or wherever) I get the loop with no inner safepoints. If I build it with Maven (with an OpenJDK JAVA_HOME) I get the a safepoint and the program exits after 5 seconds.

Delete
It appears that Eclipse and Maven produce different bytecode (.class files) for the same compilation unit. Both are legal (as in runnable by JVMs, pass validation etc) but end up with very different results at runtime. I'll dig into it further in the next blog post. It's quite curious :).

Thanks for commenting on this, let me know if the other samples act weird too.

OK, it's all explained in the next post here: http://psy-lob-saw.blogspot.co.za/2016/02/wait-for-it-counteduncounted-loops.html

Delete
I think we hit this, and ended up getting https://bugs.openjdk.java.net/browse/JDK-8144827 filed and fixed on our behalf.

ReplyDelete
When you say 'this' it's kinda hard to know what you mean...

Delete
Preserving safepoints in counted loops as an option is great (the bug you link to), and according to the bug will be available from 8u92, which is not yet shipped (current latest is 8u77).

I should have been more specific, I meant that we were hitting an issue where we had counted loops that had no safepoints causing long TTSP.

ReplyDelete
8u92 is out, and we've tried the flag with the sample it works, but on a production instance it crashes, so we're chasing another bug.

However, your recent updates to this blog go on to show that using the flag is probably a really bad idea.

I assume the best thing to do here is to run with perfasm output, and look for vmovdqu vs the mov as you outline in https://github.com/netty/netty/pull/3969#issuecomment-132559757.

Thanks for the updates, I'm reading this yet again. :)

Here's another way TTSP can ruin your productivity for a week: https://bugs.openjdk.java.net/browse/JDK-8057003

ReplyDelete
In my case, we had a bad configuration that resulted in a Koloboke hashmap with 50M entries. Whenever it came time for the GC to mark that object, the GC thread went without a safepoint poll for 15 seconds or so, causing STW pauses while all my threads were waiting for the safepoint to happen.

Thank you for all the great posts, Nitsan!

What is the difference between poll and poll_return in the PrintAssembly output?

ReplyDelete
Thanks, love all your blog posts!

poll - loop back edge

Delete
poll_return - before method exit

Glad you're enjoying it :-)

> Safepoint operation interval -> Sometimes in your control (be careful how you profile/monitor your application), sometimes not.

ReplyDelete
It seems there are no benchmark results that show effects of increasing the frequency of safepoint operation requests in the post (that must be configured with `@Param int intervalMs;`).

The higher the frequency of requests for safepoint operations, the bigger the impact on the user code, is that correct?

Thank you for the post, it's wonderful!
