# Claims ledger — group U1

| card id | claim | source | how checked |
|---|---|---|---|
| uth-python-list-1-growth | growth 0,4,8,16,24,32,40,52,64,76; new_allocated = (n + n>>3 + 6) & ~3 | cpython@v3.14.0:Objects/listobject.c:list_resize | read; ran sys.getsizeof loop on 3.14.8 (capacity jumps at len 1,5,9,17,25,33,41,53,65) |
| uth-python-list-2-insert-front | insert shifts pointers one by one, pop(idx) uses memmove | cpython@v3.14.0:Objects/listobject.c:ins1, list_pop_impl | read |
| uth-python-list-2-insert-front | 1e6 elements: insert(0)+pop(0) ~226us vs append+pop ~0.023us | local timeit, CPython 3.14.8 | ran |
| uth-python-list-3-pointers | [x]*n copies the same pointer; getsizeof([None]*1000)=8056 (56 header + 8*1000) | local run, CPython 3.14.8 | ran |
| uth-python-dict-1-compact | two arrays: dk_indices (hash table of ints) + dk_entries (hash,key,value in insertion order) | cpython@v3.14.0:Objects/dictobject.c header comment; Include/internal/pycore_dict.h PyDictKeyEntry | read |
| uth-python-dict-1-compact | index width 1 byte when dk_size <= 128; entries length = USABLE_FRACTION = 2n/3 | cpython@v3.14.0:Objects/dictobject.c (comment near line 35, USABLE_FRACTION) | read |
| uth-python-dict-1-compact | 3.6 compact dict uses 20-25% less memory; 3.7 guarantees insertion order | cpython@v3.6.0:Doc/whatsnew/3.6.rst; cpython@v3.7.0:Doc/library/stdtypes.rst | read |
| uth-python-dict-1-compact | 3.5 and earlier stored each full entry in every hash slot | cpython 3.6 whatsnew ("more compact representation similar to PyPy") | read (inference from whatsnew; layout of old table not source-read) |
| uth-python-dict-2-probe-resize | probe: perturb >>= 5; i = (i*5 + perturb + 1) & mask; perturb init = hash | cpython@v3.14.0:Objects/dictobject.c (PERTURB_SHIFT 5, comment ~l.335-358, l.995) | read |
| uth-python-dict-2-probe-resize | PyDict_MINSIZE 8, USABLE_FRACTION(n)=2n/3, GROWTH_RATE = used*3 | cpython@v3.14.0:Objects/dictobject.c l.116, 543, 590 | read |
| uth-python-dict-2-probe-resize | getsizeof jumps when inserting 1st, 6th, 11th, 22nd, 43rd key | local run CPython 3.14.8 | ran |
| uth-python-dict-3-collision | constant __hash__: 500/1000/2000 inserts = 2.8/10.9/44.1 ms (quadratic) | local run CPython 3.14.8 | ran |
| uth-python-set-1-table | setentry = {key, hash}; PySet_MINSIZE 8; no index array | cpython@v3.14.0:Include/cpython/setobject.h | read |
| uth-python-set-1-table | resize when fill*5 >= mask*3; new size used*4 (used*2 if used>50000); LINEAR_PROBES 9 | cpython@v3.14.0:Objects/setobject.c:set_add_entry, header comment | read |
| uth-python-set-1-table | getsizeof set(range(4)) vs set(range(5)): 216 -> 728 at the 5th element | local run CPython 3.14.8 (checked {1}=216, set(range(5))=728) | ran |
| uth-python-set-2-hash-seed | str/bytes hash is SipHash13 by default; random seed; PYTHONHASHSEED=0 disables | cpython@v3.14.0:Python/pyhash.c (siphash13 PyHash_Func), Doc/using/cmdline.rst PYTHONHASHSEED; sys.hash_info.algorithm = siphash13 | read; ran |
| uth-python-set-2-hash-seed | set order changes between runs for str (3 runs, 3 orders); fixed with PYTHONHASHSEED=0 | local run | ran |
| uth-python-set-2-hash-seed | purpose is DoS protection against O(n^2) dict insertion | cpython@v3.14.0:Doc/reference/datamodel.rst object.__hash__ | read |
| uth-python-set-3-intersection | set_intersection swaps so it iterates the smaller set | cpython@v3.14.0:Objects/setobject.c:set_intersection | read |
| uth-python-set-3-intersection | small&big 0.056us; 999999 in set 0.017us vs list 5ms | local timeit | ran |
| uth-python-str-int-1-str-kinds | strings use 1/2/4 bytes per char by widest char (PEP 393 kinds); compact ASCII struct is smaller | cpython@v3.14.0:Include/cpython/unicodeobject.h (PyASCIIObject comment, PyUnicode_1/2/4BYTE_KIND) | read |
| uth-python-str-int-1-str-kinds | getsizeof 'a'*10=51, 'é'*10=67, '中'*10=78, '😀'*10=100 (header 40 ASCII / 56 other + n*width + terminator) | local run CPython 3.14.8 | ran |
| uth-python-str-int-2-intern | small int cache -5..256 | cpython@v3.14.0:Doc/c-api/long.rst l.46; ran int('-5') is int('-5') True, '-6' False, '256' True, '257' False | read; ran |
| uth-python-str-int-2-intern | identifiers/attribute names auto-interned; interned keys compare by pointer; sys.intern | cpython@v3.14.0:Doc/library/sys.rst intern() | read; ran ('hello_world' joined is not literal, intern makes it identical) |
| uth-python-str-int-3-bigint | PyLong_SHIFT 30, digit uint32_t; getsizeof 1=28, 2**30=32, 2**60=36 | cpython@v3.14.0:Include/cpython/longintrepr.h; sys.int_info(bits_per_digit=30) | read; ran |
| uth-python-str-int-3-bigint | KARATSUBA_CUTOFF 70 digits | cpython@v3.14.0:Objects/longobject.c l.82 | read |
| uth-python-str-int-3-bigint | 4000-digit square 35.7us, 8000-digit 112us (3.1x) | local timeit | ran |
| uth-python-str-int-3-bigint | default int<->str limit 4300 digits (3.11+, CVE-2020-10735); no linear conversion algorithm for base 10 | cpython@v3.14.0:Doc/library/stdtypes.rst "Integer string conversion length limitation"; sys.int_info.default_max_str_digits=4300 | read; ran |
| uth-python-sort-1-runs | run detection, descending runs reversed, binary insertion to minrun, merge; minrun 32..64 | cpython@v3.14.0:Objects/listsort.txt; Objects/listobject.c merge_compute_minrun, MAX_MINRUN 64 | read; ran merge_compute_minrun(1e6)=62 |
| uth-python-sort-1-runs | comparisons for 100k: sorted 99999, reversed 99999, random 1532042 (n log2 n = 1660964), all-equal 99999 | local run CPython 3.14.8 counting __lt__ | ran |
| uth-python-sort-2-powersort | 3.11 switched to powersort; old strategy loosely Fibonacci-invariant based, broken by machine proof attempt | cpython@v3.14.0:Objects/listsort.txt l.342-366; cpython@v3.11.0a1:Misc/NEWS.d/3.11.0a1.rst; listsort.txt has 0 'powersort' hits at v3.10.0, 3 at v3.11.0 | read |
| uth-python-sort-2-powersort | power = depth in conceptual binary merge tree; merge adjacent runs with greater power; stack powers strictly decreasing | cpython@v3.14.0:Objects/listobject.c found_new_run; listsort.txt l.426 | read |
| uth-python-sort-2-powersort | "fast approximations to optimal binary search trees" | cpython@v3.14.0:Objects/listsort.txt l.370 | read |
| uth-python-sort-3-gallop-key | MIN_GALLOP 7; galloping via B[0],B[1],B[3],B[7],..; min_gallop adaptive | cpython@v3.14.0:Objects/listobject.c, listsort.txt "Galloping" | read |
| uth-python-sort-3-gallop-key | two 100k runs (second all smaller): 200042 compares vs 199999 for one sorted 200k | local run | ran |
| uth-python-sort-3-gallop-key | key called once per element (1000 calls); sort is stable | local run; listsort.txt line 3 "adaptive, stable, natural mergesort" | ran; read |
| uth-python-heapq-bisect-1-array-heap | heap is a plain list; children 2i+1, 2i+2; parent (pos-1)>>1; heapify loops reversed(range(n//2)) calling _siftup | cpython@v3.14.0:Lib/heapq.py heapify, _siftup, _siftdown (C _heapq mirrors via `from _heapq import *`) | read |
| uth-python-heapq-bisect-1-array-heap | 1e6 floats: heapify 15.5 ms vs 1e6 heappush 26.3 ms | local timeit CPython 3.14.8 | ran |
| uth-python-heapq-bisect-1-array-heap | (1, object()) twice raises TypeError on push | local run | ran |
| uth-python-heapq-bisect-2-max-heap | _siftup bubbles smaller child to leaf then _siftdown; comment: 1000 heappops 14996 -> 8680 compares | cpython@v3.14.0:Lib/heapq.py comment above heapify | read |
| uth-python-heapq-bisect-2-max-heap | heappush_max/heappop_max/heapify_max/heappushpop_max/heapreplace_max added in 3.14 | cpython@v3.14.0:Doc/library/heapq.rst versionadded 3.14; Lib/heapq.py def lines 181-210 | read |
| uth-python-heapq-bisect-3-bisect | bisect_left([1,2,2,2,3],2)=1, bisect_right=4 | local run | ran |
| uth-python-heapq-bisect-3-bisect | bisect_left compares key(a[mid]) < x, bisect_right x < key(a[mid]); insort = bisect + list.insert; docs say O(log n) search dominated by O(n) insertion; key= added 3.10; C _bisect overrides | cpython@v3.14.0:Lib/bisect.py; Doc/library/bisect.rst | read |
| uth-python-deque-ordereddict-1-blocks | BLOCKLEN 64, doubly-linked list of fixed blocks, never realloc, textbook list has 200% link overhead | cpython@v3.14.0:Modules/_collectionsmodule.c header comment l.70-95, struct BLOCK | read |
| uth-python-deque-ordereddict-1-blocks | 2 links per 64 slots = ~3% | derived from struct BLOCK (leftlink + rightlink, data[64]) | computed |
| uth-python-deque-ordereddict-1-blocks | appendleft+popleft ~22 ns | local timeit | ran |
| uth-python-deque-ordereddict-2-index | deque_item walks blocks from the nearer end; d[0], d[-1] direct; d[500000] ~20us vs list 0.018us (1e6 elements) | cpython@v3.14.0:Modules/_collectionsmodule.c deque_item_lock_held; local timeit | read; ran |
| uth-python-deque-ordereddict-2-index | deque(maxlen=3) after appending 0..5 is [3,4,5] | local run | ran |
| uth-python-deque-ordereddict-3-ordereddict | C OrderedDict: dict + doubly-linked list + array mirroring dict entries to node pointers for O(1) node lookup | cpython@v3.14.0:Objects/odictobject.c header comment | read |
| uth-python-deque-ordereddict-3-ordereddict | OD==OD order-sensitive False, dict==dict True; move_to_end, popitem(last=False); getsizeof 1000 keys: 85400 vs 36952 | local run | ran |
| uth-python-lru-cache-1-linked-list | dict key->lru_list_elem + circular doubly linked list with root sentinel; hit extract+append at tail; full: evict root.next, reuse link | cpython@v3.14.0:Modules/_functoolsmodule.c bounded_lru_cache_get_lock_held / _update_lock_held, lru_cache_append_link, init root.prev=root.next=&root | read |
| uth-python-lru-cache-1-linked-list | f(1) f(2) f(1) f(3) f(2) with maxsize=2 -> hits=1 misses=4 currsize=2 | local run | ran |
| uth-python-lru-cache-2-variants | maxsize None -> infinite_lru_cache_wrapper (dict only), 0 -> uncached wrapper; functools.cache = lru_cache(maxsize=None); single int/str arg used directly as key | cpython@v3.14.0:Modules/_functoolsmodule.c l.1184-1547, lru_cache_make_key; Lib/functools.py cache | read |
| uth-python-lru-cache-2-variants | lru_cache with list arg raises TypeError: unhashable type: 'list' | local run | ran |
| uth-python-lru-cache-3-method-leak | lru_cache on a method keeps instance alive after del + gc.collect (weakref still alive) | local run CPython 3.14.8 | ran |
| uth-python-memory-gc-1-refcount | getrefcount(a) is 2 / 3 / 2 for a, b=a, del b | local run CPython 3.14.8 | ran |
| uth-python-memory-gc-1-refcount | refcount drives deallocation; del removes a name | local run | ran |
| uth-python-memory-gc-2-cycle | update_refs (gc_refs = refcnt), subtract_refs (traverse + visit_decref), move_unreachable; only tracked container objects | cpython@v3.14.8:Python/gc.c deduce_unreachable, update_refs, subtract_refs | read |
| uth-python-memory-gc-2-cycle | x.me=x; del x -> weakref alive; gc.collect() returns 1; then dead | local run | ran |
| uth-python-memory-gc-3-generations | 3 generations, thresholds (2000,10,10); full collection skipped unless long_lived_pending >= long_lived_total/4 | cpython@v3.14.8:Python/gc.c gc_select_generation; gc.get_threshold() on 3.14.8; Doc/library/gc.rst set_threshold | read; ran |
| uth-python-memory-gc-3-generations | 3.14.0-3.14.4 shipped incremental GC, reverted in 3.14.5 to the 3.13 generational GC | cpython@v3.14.8:Doc/whatsnew/3.14.rst "Garbage collection" section; Doc/library/gc.rst versionchanged 3.14.5 | read |
| uth-python-memory-gc-4-arena | 64-bit: ARENA 1 MiB (USE_LARGE_ARENAS), POOL 16 KiB (USE_LARGE_POOLS) | cpython@v3.14.8:Include/internal/pycore_obmalloc.h | read |
| uth-python-memory-gc-4-arena | 2M strings 189 MB; after del keeping 1% still 189 MB; after full del 37 MB (ps rss) | local run /tmp/uth_U1/rss.py | ran |
| uth-python-asyncio-1-loop | _run_once: timeout 0 if _ready else heap top - now; selector.select; pop due timers to _ready; run ntodo ready handles; _ready is collections.deque, _scheduled uses heapq | cpython@v3.14.0:Lib/asyncio/base_events.py:_run_once l.1965-2050, call_at l.813, __init__ l.423 | read |
| uth-python-asyncio-1-loop | asyncio.sleep(delay>0) uses loop.call_later | cpython@v3.14.0:Lib/asyncio/tasks.py sleep | read |
| uth-python-asyncio-2-lazy-cancel | cancelled timers stay in heap; popped at head; if >100 scheduled and cancelled fraction >0.5, filter + heapify | cpython@v3.14.0:Lib/asyncio/base_events.py l.56-62, _run_once l.1974-1996 | read |
| uth-python-asyncio-2-lazy-cancel | 1000 timers, cancel tail 400 -> len(_scheduled)=1000; cancel 600 total -> 400 | local run CPython 3.14.8 | ran |
| uth-python-asyncio-3-blocking | time.sleep(0.5) in one coroutine delays asyncio.sleep(0.1) to 0.52 s; call_soon inside callback runs next iteration (a,b,c); slow_callback_duration = 0.1 | local run; cpython@v3.14.0:Lib/asyncio/base_events.py l.437, _run_once comment l.2030 | ran; read |
| uth-java-arraylist-arraydeque-1-arraylist | grow: newLength(old, min, old>>1) -> 1.5x; empty ArrayList allocates DEFAULT_CAPACITY 10 at first add | openjdk/jdk@jdk-25-ga:src/java.base/share/classes/java/util/ArrayList.java:grow, jdk/internal/util/ArraysSupport.newLength | read |
| uth-java-arraylist-arraydeque-1-arraylist | capacities 10 15 22 33 49 73 109 163 244 | ran jt/Cap.java on Java 25.0.4 via reflection (--add-opens) | ran |
| uth-java-arraylist-arraydeque-1-arraylist | ensureCapacity reduces incremental reallocation | ArrayList.java javadoc l.58 | read |
| uth-java-arraylist-arraydeque-2-arraydeque | head/tail circular array; addFirst dec(head), addLast inc(tail); full when head==tail -> grow | openjdk/jdk@jdk-25-ga:.../ArrayDeque.java addFirst, addLast, inc, dec | read |
| uth-java-arraylist-arraydeque-2-arraydeque | default array length 16+1; grow: jump = old<64 ? old+2 : old>>1; capacities 17 36 74 111 166 249 | ArrayDeque.java ctor + grow; ran Cap.java | read; ran |
| uth-java-arraylist-arraydeque-2-arraydeque | JDK 8 ArrayDeque array length always a power of two (mask-based); JDK 9+ not (SKELETON SUMMARY WRONG) | openjdk/jdk8u-dev:jdk/src/share/classes/java/util/ArrayDeque.java l.92 "always a power of two" | read |
| uth-java-arraylist-arraydeque-3-vs-stack | javadoc: faster than Stack as stack and LinkedList as queue; null prohibited; Stack extends Vector with synchronized pop/peek; LinkedList.Node item/next/prev; pollFirst returns null for empty slot | ArrayDeque.java l.48, Stack.java, LinkedList.java l.982, ArrayDeque.pollFirst; addFirst(null) throws NPE | read |
| uth-java-hashmap-1-buckets | DEFAULT_INITIAL_CAPACITY 16, DEFAULT_LOAD_FACTOR 0.75, threshold = 12; power-of-two capacity, index = (n-1)&hash | openjdk/jdk@jdk-25-ga:.../HashMap.java l.238-250, resize(), putVal | read |
| uth-java-hashmap-1-buckets | size 12 -> table 16, size 13 -> 32 | ran jt/Hm.java on Java 25.0.4 (reflection on HashMap.table) | ran |
| uth-java-hashmap-1-buckets | HashMap.newHashMap(n) exists since Java 19 | HashMap.java l.2579 @since 19 | read |
| uth-java-hashmap-2-spread | hash(key) = h ^ (h >>> 16); comment: Float keys with consecutive whole numbers collide in small tables; trees as backstop | HashMap.java l.320-339 | read |
| uth-java-hashmap-2-spread | keys k<<16 (k=1..6), cap 16: unspread buckets all 0, spread 1..6 | ran Hm.java | ran |
| uth-java-hashmap-3-resize-split | resize splits chain by (hash & oldCap)==0 into lo (index j) and hi (j+oldCap) lists; TreeNode.split; untreeify if <= UNTREEIFY_THRESHOLD(6) | HashMap.java resize(), TreeNode.split l.2326-2335 | read |
| uth-java-hashmap-4-treeify | TREEIFY_THRESHOLD 8, UNTREEIFY 6, MIN_TREEIFY_CAPACITY 64; treeifyBin resizes if table < 64; TreeNodes ~2x size; tree ordered by hash then Comparable | HashMap.java l.160-180, 260-275, treeifyBin l.762 | read |
| uth-java-hashmap-4-treeify | 11 equal-hash Comparable keys: table 16 (n<=8), 32 (n=9), 64 (n=10), TreeNode at n=11 | ran Hm.java | ran |
| uth-java-linkedhashmap-treemap-1-lru | LinkedHashMap.Entry extends HashMap.Node with before/after; accessOrder moves node to tail in afterNodeAccess; afterNodeInsertion calls removeEldestEntry(head) | openjdk/jdk@jdk-25-ga:.../LinkedHashMap.java l.205, afterNodeAccess, afterNodeInsertion | read |
| uth-java-linkedhashmap-treemap-1-lru | put a,b,c; get a; put d (max 3) -> [c, a, d] | ran jt/Lh.java Java 25.0.4 | ran |
| uth-java-linkedhashmap-treemap-2-get-cme | get in accessOrder mode does ++modCount; iterating keySet while get -> ConcurrentModificationException | LinkedHashMap.afterNodeAccess; ran Lh.java | read; ran |
| uth-java-linkedhashmap-treemap-3-treemap | TreeMap.Entry has left/right/parent/color (RED/BLACK); getCeilingEntry descends by compare | TreeMap.java l.427-457, l.2409 | read |
| uth-java-linkedhashmap-treemap-3-treemap | floorKey(25)=20, ceilingKey(25)=30, floorKey(5)=null on {10,20,30}; BigDecimal 1.0 vs 1.00: TreeMap size 1, HashMap size 2 | ran Lh.java | ran |
| uth-java-priorityqueue-1-heap | array binary heap, children 2n+1/2(n+1); DEFAULT_INITIAL_CAPACITY 11; grow: old<64 ? old+2 : old>>1 (via ArraysSupport.newLength) | openjdk/jdk@jdk-25-ga:.../PriorityQueue.java l.93-103, grow l.291 | read |
| uth-java-priorityqueue-1-heap | add 5,3,8,1,9,2 prints [1, 3, 2, 5, 9, 8]; poll order 1 2 3 5 8 9; reverseOrder peek 9 | ran jt/Pq.java Java 25.0.4 | ran |
| uth-java-priorityqueue-1-heap | remove(Object) linear search | PriorityQueue.remove(Object) uses indexOf (standard); javadoc "linear time" for remove(Object) | read |
| uth-java-priorityqueue-2-scheduled | DelayedWorkQueue binary heap on trigger time then sequenceNumber; heapIndex gives O(log n) removal; leader-follower; removeOnCancel default false; INITIAL_CAPACITY 16 | openjdk/jdk@jdk-25-ga:.../ScheduledThreadPoolExecutor.java l.253-267, l.890-935, setRemoveOnCancelPolicy javadoc l.770-790 | read |
| uth-java-priorityqueue-2-scheduled | DelayQueue wraps PriorityQueue and take() waits on head delay with a leader thread | DelayQueue.java l.104, take() | read |
| uth-java-priorityqueue-3-timer | TaskQueue is balanced binary heap on nextExecutionTime, 1-based, array 128; single TimerThread; uncaught exception kills thread -> IllegalStateException "Timer already cancelled." | Timer.java l.586-595, TimerThread.run/mainLoop; ran jt/Tm.java | read; ran |
| uth-java-concurrenthashmap-1-cas-lock | empty bin -> casTabAt, else synchronized(f) on head; get has no lock; Node.val/next volatile; unused Segment class kept for serialization | openjdk/jdk@jdk-25-ga:.../ConcurrentHashMap.java putVal l.1022-1089, get, Node l.639-640, comment l.486 | read |
| uth-java-concurrenthashmap-2-size | baseCount + @Contended CounterCell[] picked by ThreadLocalRandom probe; sumCount; size reflects transient states; MIN_TRANSFER_STRIDE 16; helpTransfer | ConcurrentHashMap.java addCount l.2340, CounterCell l.2581, sumCount, l.100-104, l.571 | read |
| uth-java-concurrenthashmap-3-compound | null key/value -> NPE; computeIfAbsent recursion -> IllegalStateException "Recursive update" (ReservationNode check) | ConcurrentHashMap.java l.1023, l.1074; ran jt/Chm.java Java 25.0.4 | read; ran |
| uth-java-sort-1-two-algorithms | Arrays.sort(int[]) -> DualPivotQuicksort; sort(Object[]) -> ComparableTimSort; sort(T[],Comparator) -> TimSort | openjdk/jdk@jdk-25-ga:.../Arrays.java l.98, l.1034, l.1223 | read |
| uth-java-sort-1-two-algorithms | 2M random: int[] ~76 ms vs Integer[] ~228 ms (3 reps, 86/76/76 vs 279/251/228) | ran jt/So.java Java 25.0.4 | ran |
| uth-java-sort-2-dual-pivot | 2 pivots, 3 parts; 5-sample pivot selection with golden-ratio approx; heap sort when bits > MAX_RECURSION_DEPTH = 64*DELTA(6) = 384; counting sort byte>=64, short/char>=1750; tryMergeRuns; docs 'all data sets' (25) vs 'many data sets that cause other quicksorts to degrade' (jdk-11+28) | DualPivotQuicksort.java l.28-45, 64-124, 262-300, 414-480; openjdk/jdk@jdk-11+28 same file l.31 | read |
| uth-java-sort-3-timsort-contract | TimSort adapted from Tim Peters's list sort; MIN_MERGE 32 (minrun in [16,32]); 'Comparison method violates its general contract!' | TimSort.java l.36-42, l.80, l.390-403, l.782 | read |
| uth-java-sort-3-timsort-contract | compares for 100k Integer: sorted 99999, reversed 99999, random 1534703; (p,q)->p-q on [MAX,-5,3,MIN,0] -> [MAX,-5,0,3,MIN]; random comparator throws IAE | ran So.java, Cmp.java | ran |
| uth-java-string-1-compact | String = byte[] value + coder (LATIN1/UTF16); COMPACT_STRINGS | openjdk/jdk@jdk-25-ga:.../String.java l.165-228 | read |
| uth-java-string-1-compact | "hello world" 11 chars/11 bytes coder 0; "héllo" 5/5; "你好世界" 4/8 coder 1; "hello€" 6/12 coder 1 | ran jt/Str.java via reflection (--add-opens) Java 25.0.4 | ran |
| uth-java-string-1-compact | Java 8 and earlier used char[] (JEP 254 in Java 9) | general knowledge; Java 25 source shows byte[]; NOT re-verified against jdk8 source | read (partial) |
| uth-java-string-2-hashcode | hash cached in `hash`, hashIsZero for zero hash; polynomial 31*h + c; "Aa" and "BB" both 2112 | String.hashCode l.2422-2440, ArraysSupport.hashCodeOfUnsigned (31 * initialValue ...); ran Str.java | read; ran |
| uth-java-string-3-builder | StringBuilder() -> capacity 16; newCapacity = ArraysSupport.newLength(old, growth, old + (2<<coder)) -> 2n+2 chars; capacities 16 34 70 142 286 574 | StringBuilder.java l.105; AbstractStringBuilder.java l.340-349; ran Str.java | read; ran |
| uth-java-string-3-builder | s += "x" 20k/40k/80k = 39/86/233 ms vs append <1 ms; a + b + "x" compiles to invokedynamic makeConcatWithConstants | ran jt/Cc.java; javac+javap on Java 25 | ran |
| uth-java-forkjoin-1-deque | per-worker deque, circular array, power-of-two size, INITIAL_QUEUE_CAPACITY 1<<6; push/pop by owner at top (LIFO), poll (steal) by others at base via CAS (FIFO), random scans; FIFO async mode; work stealing beats work dealing | openjdk/jdk@jdk-25-ga:.../ForkJoinPool.java l.208-225, 252-320, 1067, 1098 | read |
| uth-java-forkjoin-2-common-pool | common pool parallelism = max(1, availableProcessors()-1); CompletableFuture default ASYNC_POOL = ForkJoinPool.asyncCommonPool(); system property ...common.parallelism | ForkJoinPool.java l.3080-3081, l.160-164; CompletableFuture.java l.477 | read |
| uth-java-forkjoin-2-common-pool | 12 cores -> commonPool parallelism 11; worker names ForkJoinPool.commonPool-worker-N; supplyAsync ran in commonPool-worker-11 | ran jt/Fj.java Java 25.0.4 | ran |
| uth-java-forkjoin-3-blocking | 8 x sleep(500) in parallel stream: 502 ms default (11 workers), 1180 ms with -D...common.parallelism=3; compensation only when pool might stall | ran jt/Fj3.java; ForkJoinPool.java l.790-815 | ran; read |
