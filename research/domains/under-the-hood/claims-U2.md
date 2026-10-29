# Claim ledger — group U2

| card id | claim | source (repo@tag:path:function, or doc URL) | how checked (read / ran) |
|---|---|---|---|
| uth-cpp-vector-1-growth | libstdc++ grows to size + max(size, n), i.e. 2x for push_back | gcc@releases/gcc-16.2.0:libstdc++-v3/include/bits/stl_vector.h:_M_check_len; vector.tcc:emplace_back -> _M_realloc_append | read |
| uth-cpp-vector-1-growth | libc++ grows max(2*cap, new_size) | llvm-project@llvmorg-23.1.4:libcxx/include/__vector/vector.h:__recommend | read |
| uth-cpp-vector-1-growth | MSVC grows by cap + cap/2 | microsoft/STL@main:stl/inc/vector:_Calculate_growth | read |
| uth-cpp-vector-1-growth | libc++ capacity sequence 1 2 4 8 16 32 64 128 for 100 push_backs | /tmp/uth_U2/v.cpp, Apple clang 21 libc++ | ran |
| uth-cpp-vector-2-invalidation | reserve(1000) moves storage (old &w[0] != new &w[0]) | /tmp/uth_U2/v.cpp, libc++ | ran |
| uth-cpp-vector-3-noexcept | non-noexcept move ctor -> copy on growth; noexcept -> move | /tmp/uth_U2/m.cpp, libc++ output "copy" vs "move"; libstdc++ stl_vector.h _S_use_relocate / _S_nothrow_relocate | ran + read |
| uth-cpp-vector-3-noexcept | rationale: strong exception guarantee (move_if_noexcept) | C++ standard [vector.modifiers]; libstdc++ __uninitialized_move_if_noexcept_a use in vector.tcc | read (rationale is the standard's wording) |
| uth-cpp-sort-1-introsort | libstdc++ sort: introsort loop, depth limit 2*lg(n), heap fallback (__partial_sort), threshold 16, final insertion sort, median-of-3 pivot | gcc@releases/gcc-16.2.0:libstdc++-v3/include/bits/stl_algo.h:__sort, __introsort_loop, __final_insertion_sort, __unguarded_partition_pivot, enum _S_threshold | read |
| uth-cpp-sort-1-introsort | libc++ sort: insertion sort for len < 24, ninther above 128, depth 2*log2(n) | llvm-project@llvmorg-23.1.4:libcxx/include/__algorithm/sort.h:__introsort, __sort | read |
| uth-cpp-sort-2-stable-nth | stable_sort buffer is (n+1)/2, falls back to __inplace_stable_sort if no buffer, merge sort | gcc@releases/gcc-16.2.0:stl_algo.h:__stable_sort, __stable_sort_adaptive, __inplace_stable_sort | read |
| uth-cpp-sort-2-stable-nth | stable_sort O(N log N) with extra memory, else O(N log^2 N) | C++ draft https://eel.is/c++draft/stable.sort ; cppreference stable_sort | read |
| uth-cpp-sort-2-stable-nth | nth_element = introselect, recurses into one side, heap_select at depth limit | stl_algo.h:__introselect, nth_element (depth 2*lg) | read |
| uth-cpp-sort-3-comparator | sort with a<=b on 1000 equal ints crashes (exit 138 = SIGBUS) | /tmp/uth_U2/s.cpp, Apple clang 21 libc++ -O1 | ran |
| uth-cpp-sort-3-comparator | unguarded insertion/partition loops rely on sentinels: `while (comp(val,*next))` with no bounds check | stl_algo.h:__unguarded_linear_insert, __unguarded_insertion_sort | read |
| uth-cpp-unordered-map-1-nodes | libstdc++ hashtable = forward_list of nodes + bucket array holding the node before the first node of each bucket | gcc@releases/gcc-16.2.0:libstdc++-v3/include/bits/hashtable.h (class comment lines ~100-170) | read |
| uth-cpp-unordered-map-1-nodes | max_load_factor default 1.0; growth factor 2, prime bucket counts | hashtable_policy.h:_Prime_rehash_policy (_S_growth_factor = 2), src/c++11/hashtable_c++0x.cc:_M_need_rehash; /tmp/uth_U2/u.cpp printed max_load_factor 1.0 | read + ran |
| uth-cpp-unordered-map-1-nodes | libc++ bucket counts 2,5,11,23,47,97,197,397 | /tmp/uth_U2/u.cpp, libc++ | ran |
| uth-cpp-unordered-map-1-nodes | references/pointers stay valid across rehash (ran: same address); iterators invalidated only if rehash | /tmp/uth_U2/u.cpp; https://en.cppreference.com/w/cpp/container/unordered_map (iterator invalidation table) | ran + read |
| uth-cpp-unordered-map-2-flat | flat_hash_map is open addressing with control bytes + slots; max load 7/8 for big tables; rehash/move invalidates pointers | abseil-cpp@master:absl/container/internal/raw_hash_set.h (header comment), flat_hash_map.h comments | read |
| uth-cpp-unordered-map-2-flat | bucket->node->key is two dependent memory loads (structural reading of hashtable.h) | hashtable.h comment | read |
| uth-cpp-unordered-map-3-identity-hash | std::hash<int> is identity; 50 multiples of bucket_count (97) land in one bucket (longest 50) | /tmp/uth_U2/h.cpp libc++; libstdc++ functional_hash.h _Cxx_hashtable_define_trivial_hash(int) | ran + read |
| uth-cpp-map-set-1-rbtree | node = color + parent + left + right; header keeps leftmost/rightmost/count; begin() returns header._M_left | gcc@releases/gcc-16.2.0:libstdc++-v3/include/bits/stl_tree.h:_Rb_tree_node_base, _Rb_tree_header, begin() | read |
| uth-cpp-map-set-1-rbtree | Java TreeMap is a red-black tree | openjdk/jdk21u@master:src/java.base/share/classes/java/util/TreeMap.java line 35, RED/BLACK constants | read |
| uth-cpp-map-set-1-rbtree | farthest path <= 2x nearest path; insert at most two rotations; AVL more rigid | https://en.wikipedia.org/wiki/Red%E2%80%93black_tree (raw wikitext) | read |
| uth-cpp-map-set-2-lower-bound | set.lower_bound 2000 queries on 200k set ~165 us vs std::lower_bound ~1.74 s | /tmp/uth_U2/t.cpp, clang++ -O2 libc++, this machine | ran |
| uth-cpp-map-set-3-java-mapping | TreeMap has lowerKey, floorKey, ceilingKey, higherKey | TreeMap.java lines 1022-1088 | read |
| uth-cpp-priority-queue-deque-1-heap | priority_queue = Sequence(vector) + make_heap/push_heap/pop_heap; Compare default less | gcc@releases/gcc-16.2.0:libstdc++-v3/include/bits/stl_queue.h:class priority_queue (line 550) | read |
| uth-cpp-priority-queue-deque-1-heap | top() of pushes 3 1 4 1 5 is 5 | /tmp/uth_U2/d.cpp libc++ | ran |
| uth-cpp-priority-queue-deque-1-heap | make_heap sifts down from parent (len-2)/2 to 0 (bottom-up, O(n)) | stl_heap.h:__make_heap | read |
| uth-cpp-priority-queue-deque-1-heap | n pushes cost O(n log n) (standard complexity of push_heap each O(log n)) | stl_heap.h:__push_heap | read |
| uth-cpp-priority-queue-deque-2-pop-heap | __adjust_heap sifts the hole down always choosing larger child (one comparison per level), then __push_heap sifts value back up | stl_heap.h:__adjust_heap, __pop_heap | read |
| uth-cpp-priority-queue-deque-3-deque | libstdc++ deque buffer 512 bytes, 1 element per block if sizeof >= 512 | stl_deque.h:_GLIBCXX_DEQUE_BUF_SIZE, __deque_buf_size | read |
| uth-cpp-priority-queue-deque-3-deque | libc++ block = 4096 bytes if sizeof<256 (else 16 elements) by default ABI | llvm-project@llvmorg-23.1.4:libcxx/include/deque:__deque_block_size | read |
| uth-cpp-priority-queue-deque-3-deque | deque<int> contiguous run of 1024 ints; first element address stable after 100k push_back | /tmp/uth_U2/d.cpp libc++ | ran |
| uth-cpp-priority-queue-deque-3-deque | std::queue and std::stack default Sequence = deque | stl_queue.h line 103; stl_stack.h line 106 | read |
| uth-cpp-string-1-sso | libstdc++ _S_local_capacity = 15/sizeof(CharT) (15 chars), layout pointer + length + union{local_buf[16], capacity} = 32 bytes | gcc@releases/gcc-16.2.0:libstdc++-v3/include/bits/basic_string.h lines 205-225 | read |
| uth-cpp-string-1-sso | libc++: sizeof(string)=24, empty capacity 22, 22 chars inline, 23 on heap | /tmp/uth_U2/st.cpp libc++; libcxx/include/string __min_cap | ran + read |
| uth-cpp-string-2-cow | C++ forbids COW; non-const operator[]/begin etc must not invalidate references | https://eel.is/c++draft/string.require para 4; https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_dual_abi.html | read |
| uth-cpp-string-2-cow | GCC 5.1 introduced new libstdc++ ABI (no COW), controlled by _GLIBCXX_USE_CXX11_ABI | https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_dual_abi.html | read |
| uth-cpp-string-2-cow | libc++ copy does not share buffer (a.data() != b.data()) | /tmp/uth_U2/st.cpp | ran |
| uth-cpp-string-3-sso-pointer | after vector growth data() changes for len 5, unchanged for len 40 | /tmp/uth_U2/st2.cpp libc++ | ran |
| uth-go-rust-go-slice-map-1-append | nextslicecap: <256 doubles; else newcap += (newcap+3*256)>>2 until >= newLen; then roundupsize to size class | golang/go@go1.27.3:src/runtime/slice.go:nextslicecap, growslice | read |
| uth-go-rust-go-slice-map-1-append | []int append capacity sequence ... 256 512 848 1280 1792 2560 3408 5120 | /tmp/uth_U2/gox/main.go, go1.27.2 darwin/arm64 | ran |
| uth-go-rust-go-slice-map-1-append | formula changed in Go 1.18 | https://go.dev/doc/go1.18 ("append now uses a slightly different formula") | read |
| uth-go-rust-go-slice-map-2-alias | b := a[:2]; append writes through (a=[1 2 99 4], b=[1 2 99], cap 4); a[:2:2] forces copy | /tmp/uth_U2/gox/main.go | ran |
| uth-go-rust-go-slice-map-3-swiss | Go 1.24 map is Swiss-table based | https://go.dev/doc/go1.24 ; internal/runtime/maps/map.go header | read |
| uth-go-rust-go-slice-map-3-swiss | group = 8 slots + 8-byte control word, H2 = low 7 bits, quadratic probing, extendible hashing, maxTableCapacity 1024, load factor 7/8 | golang/go@go1.27.3:src/internal/runtime/maps/map.go (header comment), table.go (maxTableCapacity), group.go (maxAvgGroupLoad = 7) | read |
| uth-go-rust-go-slice-map-3-swiss | iteration start randomized (rotated order across runs of the loop) | /tmp/uth_U2/gox/main.go output; spec says unspecified | ran |
| uth-go-rust-go-scheduler-1-gmp | per-P runq [256]guintptr, runnext slot, full queue moves half (128) + new G to global queue | golang/go@go1.27.3:src/runtime/runtime2.go (type p), proc.go:runqputslow | read |
| uth-go-rust-go-scheduler-1-gmp | GOMAXPROCS default = min(logical CPU count, affinity, cgroup limit) | src/runtime/debug.go doc for GOMAXPROCS | read |
| uth-go-rust-go-scheduler-2-steal | runqgrab steals n - n/2; stealTries = 4 with runnext/timers only on last; random steal order; schedtick%61 global queue check | proc.go:runqgrab, findRunnable/stealWork (lines ~3458, 3848-3852), randomOrder | read |
| uth-go-rust-go-scheduler-3-timers | per-P timers, 4-ary heap (timerHeapN = 4), children 4i+1.., parent (i-1)/4, siftDown scans 4 contiguous children | src/runtime/time.go:timers, siftUp, siftDown | read |
| uth-go-rust-go-scheduler-3-timers | scheduler loop calls pp.timers.check each round | proc.go:findRunnable line ~3430 | read |
| uth-go-rust-go-channel-1-hchan | hchan fields qcount, dataqsiz, buf, sendx, recvx, recvq, sendq, lock; send: waiting receiver first, then buffer space, then park | golang/go@go1.27.3:src/runtime/chan.go:hchan, chansend (lines 229-236) | read |
| uth-go-rust-go-channel-2-unbuffered | unbuffered: recvDirect/sendDirect copy between stacks; full buffered: recv takes head, sender's value goes to same slot | chan.go:recv, sendDirect, recvDirect | read |
| uth-go-rust-go-channel-3-select | select: random pollorder (cheaprandn shuffle), lockorder by hchan address via heap sort | src/runtime/select.go:selectgo lines ~135-215 | read |
| uth-go-rust-go-channel-3-select | 10000 selects with both ready -> [4919 5081] | /tmp/uth_U2/gox/main.go | ran |
| uth-go-rust-rust-collections-1-vec | growth = max(2*cap, required); min non-zero cap 8 (size 1) / 4 (size <= 1024) / 1 | rust-lang/rust@1.99.1:library/alloc/src/raw_vec/mod.rs:grow_amortized, min_non_zero_cap | read |
| uth-go-rust-rust-collections-1-vec | Vec<i32> caps 4 8 16 32 64 128; Vec<u8> 8 16 32 64 128 | /tmp/uth_U2/rs/m.rs, rustc 1.99.1 | ran |
| uth-go-rust-rust-collections-2-hashmap | std HashMap = hashbrown 0.17.1, "quadratic probing and SIMD lookup" | rust@1.99.1:library/std/Cargo.toml, library/Cargo.lock, std/src/collections/hash/map.rs doc | read |
| uth-go-rust-rust-collections-2-hashmap | control byte = top 7 bits of hash (Tag::full); probe stride += Group::WIDTH; load 7/8 (bucket_mask_to_capacity) | rust-lang/hashbrown@v0.17.1:src/control/tag.rs, src/raw.rs:ProbeSeq, bucket_mask_to_capacity | read |
| uth-go-rust-rust-collections-2-hashmap | SSE2 group is 16 bytes; aarch64 NEON group is uint8x8_t (8 bytes) | hashbrown@v0.17.1:src/control/group/{mod,sse2,neon}.rs | read |
| uth-go-rust-rust-collections-2-hashmap | capacity sequence 3 7 14 28 56 112; two maps give different iteration order | /tmp/uth_U2/rs/m.rs | ran |
| uth-go-rust-rust-collections-2-hashmap | default hasher SipHash 1-3 with random per-map seed, HashDoS resistance; others faster for small keys | rust@1.99.1:library/std/src/collections/hash/map.rs, std/src/hash/random.rs | read |
| uth-go-rust-rust-collections-3-btreemap | B = 6, CAPACITY = 2B-1 = 11, node holds B-1..2B-1 keys; rationale (allocations / B, cache misses, linear search B*log n) | rust@1.99.1:library/alloc/src/collections/btree/node.rs, map.rs doc "Background" | read |
| uth-go-rust-modern-sorts-1-pdqsort | Go 1.19 switched to pdqsort | https://go.dev/doc/go1.19 | read |
| uth-go-rust-modern-sorts-1-pdqsort | maxInsertion 12; ninther >= 50; breakPatterns when unbalanced (< len/8); limit = bits.Len(n) -> heapSort; partitionEqual | golang/go@go1.27.3:src/sort/zsortfunc.go:pdqsort_func, choosePivot_func, breakPatterns_func; sort/sort.go:Sort | read |
| uth-go-rust-modern-sorts-2-drift-ipn | Rust 1.81 replaced sorts by driftsort (stable) and ipnsort (unstable) | rust@1.99.1:RELEASES.md Version 1.81.0 | read |
| uth-go-rust-modern-sorts-2-drift-ipn | ipnsort: len <= 20 insertion; find_existing_run whole-array shortcut; limit 2*ilog2(len) then heapsort | rust@1.99.1:library/core/src/slice/sort/unstable/mod.rs, unstable/quicksort.rs | read |
| uth-go-rust-modern-sorts-2-drift-ipn | driftsort: natural runs, powersort merge heuristic, quicksort for unsorted runs, scratch max(n - n/2, min(n, 8MB/size)) | rust@1.99.1:library/core/src/slice/sort/stable/{mod,drift}.rs | read |
| uth-go-rust-modern-sorts-3-sorted-input | sorted/reversed 1e6: Rust 999999 comparisons (stable and unstable); Go sort.Slice ~1000011 | /tmp/uth_U2/rs/s.rs, /tmp/uth_U2/gox/main.go | ran |
| uth-go-rust-modern-sorts-3-sorted-input | Go reverses decreasing input (hint decreasingHint -> reverseRange) | sort/zsortfunc.go:pdqsort_func lines 89-97 | read |
| uth-go-rust-modern-sorts-3-sorted-input | new Rust sorts may panic on non-total-order comparators | rust@1.99.1:RELEASES.md 1.81 compatibility notes | read |
| uth-redis-sds-dict-1-sds | SDS header len/alloc/flags; 5 types (8/16/32/64-bit len fields + type 5 for < 32 chars) | redis/redis@8.10.3:src/sds.h (sdshdr5..64), sds.c:sdsReqType | read |
| uth-redis-sds-dict-1-sds | sdsMakeRoomFor: newlen < SDS_MAX_PREALLOC (1MB) doubles, else += 1MB | redis@8.10.3:src/sds.h SDS_MAX_PREALLOC, src/sds.c:sdsMakeRoomFor lines 292-298 | read |
| uth-redis-sds-dict-2-rehash | dict has ht_table[2], rehashidx; initial size 4 (DICT_HT_INITIAL_EXP 2) | redis@8.10.3:src/dict.h lines 168, 212-213 | read |
| uth-redis-sds-dict-2-rehash | expand when used >= buckets (ratio 1) to next power of two of used+1 | src/dict.c:dictExpandIfNeeded line 1649-1673 | read |
| uth-redis-sds-dict-2-rehash | _dictRehashStep -> dictRehash(d,1); inserts go to table 1 while rehashing; empty_visits n*10 | src/dict.c:_dictRehashStep, dictRehash, line 552, 1781 | read |
| uth-redis-sds-dict-2-rehash | serverCron active rehashing up to INCREMENTAL_REHASHING_THRESHOLD_US = 1000 | src/server.h:147, src/server.c:1351-1358 | read |
| uth-redis-sds-dict-3-cow | resize policy FORBID in fork child, AVOID when parent has child; AVOID still expands at ratio 4 and shrinks at 1/(8*4) | src/server.c:updateDictResizePolicy; src/dict.c lines 34-46, dictExpandIfNeeded; src/dict.h HASHTABLE_MIN_FILL 8 | read |
| uth-redis-sds-dict-3-cow | rationale: copy-on-write while child saves | comment at src/dict.c lines 34-38 | read |
| uth-redis-zset-1-skiplist-dict | ZSET = dict + skiplist sharing the SDS; Pugh skiplist modified | redis@8.10.3:src/t_zset.c header comment lines 18-42; server.h zset struct | read |
| uth-redis-zset-1-skiplist-dict | ZSKIPLIST_MAXLEVEL 32, ZSKIPLIST_P 0.25; zset-max-listpack-entries 128, zset-max-listpack-value 64 | src/server.h:656-657; src/config.c:3603,3607 | read |
| uth-redis-zset-2-span-rank | zslGetRank sums level spans along the search path; zslGetElementByRank uses spans | src/t_zset.c:zslGetRank, zslGetElementByRankFromNode | read |
| uth-redis-zset-2-span-rank | avg level 1.334 for P=0.25, 1.999 for P=0.5 (zslRandomLevel loop) | python simulation of zslRandomLevel (1e6 draws) | ran |
| uth-redis-zset-3-why-skiplist | three reasons (memory tunable, ZRANGE cache locality, simplicity; ZRANK patch) | antirez HN comment 1171934 https://news.ycombinator.com/item?id=1171934 (fetched via hn.algolia.com API) | read |
| uth-redis-compact-encodings-1-listpack | listpack 6-byte header (32-bit total bytes + 16-bit count), backlen at entry end allowing reverse traversal | redis@8.10.3:src/listpack.c LP_HDR_SIZE, lpEncodeBacklen; antirez/listpack listpack.md | read |
| uth-redis-compact-encodings-1-listpack | defaults hash-max-listpack-entries 512, zset 128/64, hash value 64 | src/config.c lines 3593-3607 | read |
| uth-redis-compact-encodings-2-ziplist-cascade | ziplist prevlen 1-5 bytes -> cascade update; listpack replaced ziplist in 7.0 (Hash, List, Zset) | https://github.com/antirez/listpack/blob/master/listpack.md; redis@7.0.0:00-RELEASENOTES line 447 | read |
| uth-redis-compact-encodings-3-quicklist-intset | quicklist = doubly linked list of listpack nodes; list-max-listpack-size -2 => 8192 bytes (optimization_level[1]) | src/quicklist.h:quicklistNode, quicklist.c:optimization_level, quicklistNodeNegFillLimit; config.c:3511 | read |
| uth-redis-compact-encodings-3-quicklist-intset | intset: sorted array, binary search, int16/32/64 upgrade on larger value, remove never downgrades; set-max-intset-entries 512 | src/intset.c:intsetSearch, intsetUpgradeAndAdd, intsetRemove; config.c:3600 | read |
| uth-redis-eviction-expire-1-approx-lru | lru 24 bits, 1000 ms resolution; EVPOOL_SIZE 16; maxmemory-samples default 5, max 64; pool persists across rounds | src/object.h:92-94; src/evict.c:36, evictionPoolPopulate; src/config.c:3522; redis.conf | read |
| uth-redis-eviction-expire-1-approx-lru | 2^24 seconds = 194.18 days | python3 arithmetic | ran |
| uth-redis-eviction-expire-2-lfu | lru = 16-bit minutes + 8-bit counter; LFU_INIT_VAL 5; p = 1/((c-5)*factor+1); decay per lfu-decay-time minutes; defaults factor 10, decay 1 | src/evict.c:LFULogIncr, LFUDecrAndReturn, LFUGetTimeInMinutes; server.h:4471; config.c:3518-3519 | read |
| uth-redis-eviction-expire-2-lfu | counter after 100/1000/100K/1M hits at factor 10 = 10/18/142/255 | redis.conf table (lines 2578-2592); python simulation gave 10/20/146/255 | read + ran |
| uth-redis-eviction-expire-3-expire | 20 keys per loop, repeat if >10% expired, 25% CPU cap, slow cycle at hz (usually 10) | src/expire.c lines 60-100, 444-447 | read |
| uth-redis-eviction-expire-3-expire | replica does not expire keys itself, master sends DEL | src/db.c:expireIfNeeded comment lines 3020-3037 | read |
| uth-redis-hyperloglog-bitmap-1-hll | HLL_P 14, 16384 registers, 6 bits each, dense size 12288 + 16-byte header; index = hash & mask, count = ctz(hash>>P | 1<<Q)+1; hash MurmurHash64A | redis@8.10.3:src/hyperloglog.c lines 20-60, 194-202, hllPatLen | read |
| uth-redis-hyperloglog-bitmap-1-hll | standard error 0.81% (= 1.04/sqrt(16384) = 0.8125%), up to 12 KB | https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/ | read |
| uth-redis-hyperloglog-bitmap-1-hll | PFMERGE takes max of registers | src/hyperloglog.c:hllMerge(uint8_t *max, robj *hll), hllMergeDense | read |
| uth-redis-hyperloglog-bitmap-2-sparse | sparse opcodes ZERO (1-64), XZERO (up to 16384), VAL (value 1-32, run 1-4); empty HLL = XZERO:16384; promote when value > 32 or size > hll-sparse-max-bytes (3000); size table 100->267, 1000->1882, 10000->10591 | src/hyperloglog.c lines 100-180, 390-393, 701; config.c:3608 | read |
| uth-redis-hyperloglog-bitmap-3-bitmap | bit 0 is MSB of first byte (bit = 7 - (offset & 7)); max offset 2^32 -> 512MB; SETBIT far offset allocation can block server | src/bitops.c:setbitCommand line 873-875; https://redis.io/docs/latest/commands/setbit/ ; docs data-types/bitmaps | read |
| uth-redis-hyperloglog-bitmap-3-bitmap | redisPopcount: POPCNT path 4x64-bit counters; fallback SWAR with 0x55555555/0x33333333/0x0F0F0F0F | src/bitops.c:redisPopcount lines 62-150 | read |
| uth-redis-hyperloglog-bitmap-3-bitmap | 1e8 users / 8 = 12.5 MB | arithmetic | read |
| uth-redis-event-loop-persistence-1-event-loop | backend selection evport/epoll/kqueue/select; loop: beforesleep, aeApiPoll, process events | src/ae.c lines ~30-45, aeProcessEvents | read |
| uth-redis-event-loop-persistence-1-event-loop | io-threads default 1; with threads, reads/writes/parsing offloaded; "mostly single threaded" | src/config.c:3507; redis.conf THREADED I/O section; https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/ | read |
| uth-redis-event-loop-persistence-2-rdb-fork | rdbSaveBackground uses redisFork; default save points 3600/1, 300/100, 60/10000; fork may stall for ms to ~1s on big datasets | src/rdb.c:rdbSaveBackground, server.c:redisFork; redis.conf lines 486-506; https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/ | read |
| uth-redis-event-loop-persistence-3-aof | Multi Part AOF in 7.0: manifest + BASE + INCR (+HISTORY); appendfsync default everysec | src/aof.c lines 36-75; config.c:3492; redis@7.0.0:00-RELEASENOTES line 325 | read |
| uth-redis-streams-geo-1-stream-rax | stream = radix tree of listpacks keyed by 128-bit ID encoded big endian; defaults stream-node-max-entries 100, stream-node-max-bytes 4096 | redis@8.10.3:src/t_stream.c (comments lines 65-73, 566-575, 600-640), stream.h:9-20, config.c:3582,3606; streamEncodeID | read |
| uth-redis-streams-geo-2-delta | master entry per listpack holds field names; entries use ms/seq deltas vs the node key; SAMEFIELDS flag omits fields; XDEL flags entries, node removed when count reaches 0 | src/t_stream.c lines 16-22, 576-600, streamIteratorRemoveEntry (~1583-1600) | read |
| uth-redis-streams-geo-3-geo | GEO step max 26 => 52 bits; lat limits +-85.05112878; bits interleaved (interleave64); score stored in zset | src/geohash.h:46-52, geohash.c:interleave64, geo.c | read |
| uth-redis-streams-geo-3-geo | search estimates step from radius, takes center + 8 neighbors (9 ranges) from the zset, filters by exact distance | src/geohash_helper.c:geohashEstimateStepsByRadius, geohashCalculateAreasByShapeWGS84; geo.c:membersOfAllNeighbors, geoWithinShape | read |
