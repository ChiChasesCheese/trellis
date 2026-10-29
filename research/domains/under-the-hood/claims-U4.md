# Claim ledger — group U4

Per Chi's instruction (2026-10-28) everything was verified online only (source at a tag, official docs, papers); nothing was built or run. L = linux@v7.3, N = nginx@release-1.31.8, G = git@v2.56.0.

| card id | claim | source (repo@tag:path:function, or doc URL) | how checked (read / ran) |
|---|---|---|---|
| uth-os-net-scheduler-1-rbtree | 6.5 CFS keys the rbtree on vruntime (entity_before compares vruntime) | linux@v6.5:kernel/sched/fair.c:entity_before | read |
| uth-os-net-scheduler-1-rbtree | 7.3 entity_before compares deadline; tree is rb_root_cached, leftmost via rb_first_cached | L:kernel/sched/fair.c:entity_before, __pick_first_entity, cfs_rq->tasks_timeline | read |
| uth-os-net-scheduler-1-rbtree | EEVDF introduced in 6.6 (pick_eevdf absent in v6.5, present in v6.6) | linux@v6.5 / v6.6:kernel/sched/fair.c; Documentation/scheduler/sched-eevdf.rst | read |
| uth-os-net-scheduler-1-rbtree | CFS doc: leftmost of time-ordered rbtree, no array switch artifacts | linux@v6.5:Documentation/scheduler/sched-design-CFS.rst | read |
| uth-os-net-scheduler-2-weight | sched_prio_to_weight: nice 0 = 1024, 1 = 820, -1 = 1277, -20 = 88761, 19 = 15 | L:kernel/sched/core.c:sched_prio_to_weight[40] | read |
| uth-os-net-scheduler-2-weight | vruntime += calc_delta_fair(delta_exec) (scaled by NICE_0_LOAD/weight) | L:kernel/sched/fair.c:update_curr (line 2250), calc_delta_fair | read |
| uth-os-net-scheduler-2-weight | share 1024:820 = 55.5%:44.5%; 88761/15 = 5917 | arithmetic on table above | derived |
| uth-os-net-scheduler-3-eevdf | deadline = vruntime + calc_delta_fair(slice, se) | L:kernel/sched/fair.c:update_deadline | read |
| uth-os-net-scheduler-3-eevdf | pick: eligible first, earliest deadline; augmented rbtree with min_vruntime prunes; O(log n) | L:kernel/sched/fair.c:pick_eevdf comment and loop | read |
| uth-os-net-scheduler-3-eevdf | sysctl_sched_base_slice = 700000 ns, "0.70 msec * (1 + ilog(ncpus))" | L:kernel/sched/fair.c:sysctl_sched_base_slice | read |
| uth-os-net-scheduler-3-eevdf | tasks can request slices via sched_setattr() | L:Documentation/scheduler/sched-eevdf.rst | read |
| uth-os-net-epoll-1-rbtree-ready | struct eventpoll has rdllist and rb_root_cached rbr | L:fs/eventpoll.c:struct eventpoll | read |
| uth-os-net-epoll-1-rbtree-ready | ep_poll_callback does list_add_tail(&epi->rdllink, &ep->rdllist) | L:fs/eventpoll.c:ep_poll_callback | read |
| uth-os-net-epoll-1-rbtree-ready | ep_send_events iterates only the ready batch (scan_batch spliced from rdllist) | L:fs/eventpoll.c:ep_send_events, ep_start_scan | read |
| uth-os-net-epoll-2-select | __FD_SETSIZE = 1024, fd_set is a bit array | L:include/uapi/linux/posix_types.h | read |
| uth-os-net-epoll-2-select | core_sys_select copies the three sets in (get_fd_set) and out (set_fd_set) | L:fs/select.c:core_sys_select | read |
| uth-os-net-epoll-2-select | do_select loops over all bits up to n calling select_poll_one | L:fs/select.c:do_select | read |
| uth-os-net-epoll-3-level-edge | LT: after delivery list_add_tail back to rdllist; ET: not re-queued | L:fs/eventpoll.c:ep_deliver_event | read |
| uth-os-net-epoll-3-level-edge | EPOLLONESHOT: epi->event.events &= EP_PRIVATE_BITS after one delivery | L:fs/eventpoll.c:ep_deliver_event | read |
| uth-os-net-allocators-1-buddy | MAX_PAGE_ORDER 10, NR_PAGE_ORDERS 11, free_area per order | L:include/linux/mmzone.h | read |
| uth-os-net-allocators-1-buddy | buddy pfn = page_pfn ^ (1 << order) | linux@v6.12:mm/internal.h:__find_buddy_pfn | read |
| uth-os-net-allocators-1-buddy | merge loop to MAX_PAGE_ORDER, combined_pfn = buddy_pfn & pfn | L:mm/page_alloc.c:__free_one_page | read |
| uth-os-net-allocators-1-buddy | allocation splits larger block via expand() | L:mm/page_alloc.c (expand call sites) | read |
| uth-os-net-allocators-2-slub | kmalloc size classes include 96 and 192 between powers of two | L:mm/slab_common.c:kmalloc_info[] | read |
| uth-os-net-allocators-2-slub | only SLUB / SLUB_TINY remain in mm/Kconfig | L:mm/Kconfig | read |
| uth-os-net-allocators-2-slub | free-object pointer stored inside the free object (object + s->offset) | L:mm/slub.c:get_freepointer / set_freepointer | read |
| uth-os-net-allocators-2-slub | 65 B -> 96 class wastes 31 B vs 63 B with a 128 class; 100 B -> 128 | arithmetic on kmalloc_info | derived |
| uth-os-net-allocators-3-jemalloc | 4 size classes per doubling, internal fragmentation about 20%, slab bitmap | jemalloc@5.3.0:doc/jemalloc.xml.in (intro + Size classes table) | read |
| uth-os-net-allocators-3-jemalloc | classes 16..128 step 16, then 160,192,224,256, 320..512 (16-byte quantum, 4 KiB pages) | same, table "Size classes" | read |
| uth-os-net-allocators-3-jemalloc | tcache default max size class 32 KiB | same, opt.tcache_max | read |
| uth-os-net-page-cache-1-xarray | address_space has struct xarray i_pages | L:include/linux/fs.h:struct address_space | read |
| uth-os-net-page-cache-1-xarray | XA_CHUNK_SHIFT 6 (4 if CONFIG_BASE_SMALL); page cache is the most important XArray user; RCU lookups | L:include/linux/xarray.h; Documentation/core-api/xarray.rst | read |
| uth-os-net-page-cache-2-lru | LRU_INACTIVE_FILE / LRU_ACTIVE_FILE lists | L:include/linux/mmzone.h | read |
| uth-os-net-page-cache-2-lru | second access moves inactive,referenced -> active (classic LRU) | linux@v6.12:mm/swap.c:folio_mark_accessed | read |
| uth-os-net-page-cache-2-lru | reclaim scans inactive list; active list is only deactivated | L:mm/vmscan.c:shrink_list | read |
| uth-os-net-page-cache-2-lru | MGLRU: CONFIG_LRU_GEN absent in v6.0, present in v6.1; MAX_NR_GENS 4 | linux@v6.0/v6.1:mm/Kconfig; L:include/linux/mmzone.h | read |
| uth-os-net-page-cache-3-kafka | writes into pagecache, no in-process cache; 28-30 GB of 32 GB; warm after restart; 10 GB cache about 10 min rebuild | apache/kafka@trunk:docs/design/design.md | read |
| uth-os-net-page-cache-3-kafka | sendfile avoids copies, only final copy to NIC; caught-up consumers cause no disk reads | same | read |
| uth-os-net-tcp-1-window | window = cwnd test + snd window test before sending | L:net/ipv4/tcp_output.c:tcp_cwnd_test, tcp_snd_wnd_test | read |
| uth-os-net-tcp-1-window | TCP_MAX_WSCALE 14 (65535 << 14 about 1 GB) | L:include/net/tcp.h | read + arithmetic |
| uth-os-net-tcp-2-aimd | TCP_INIT_CWND 10 | L:include/net/tcp.h | read |
| uth-os-net-tcp-2-aimd | tcp_slow_start: cwnd += acked up to ssthresh | L:net/ipv4/tcp_cong.c:tcp_slow_start | read |
| uth-os-net-tcp-2-aimd | Reno ssthresh = max(cwnd/2, 2); tcp_cong_avoid_ai adds 1 per cwnd acked | L:net/ipv4/tcp_cong.c:tcp_reno_ssthresh, tcp_cong_avoid_ai | read |
| uth-os-net-tcp-2-aimd | CUBIC beta = 717/1024; ssthresh = cwnd*beta/1024 | L:net/ipv4/tcp_cubic.c:beta, cubictcp_recalc_ssthresh | read |
| uth-os-net-tcp-2-aimd | default congestion control is cubic | L:net/ipv4/Kconfig (DEFAULT_CUBIC) | read |
| uth-os-net-tcp-3-bbr | bandwidth = windowed_max over 10 round trips, min_rtt = windowed_min over 10 s; cwnd = max(cwnd_gain*bw*min_rtt, 4) | L:net/ipv4/tcp_bbr.c header comment | read |
| uth-os-net-tcp-3-bbr | cwnd_gain 2; PROBE_BW gains 5/4, 3/4, then 1.0 | L:net/ipv4/tcp_bbr.c:bbr_cwnd_gain, bbr_pacing_gain[] | read |
| uth-os-net-tcp-3-bbr | high_gain = 2/ln(2) about 2.885, smallest gain that doubles rate each RTT | L:net/ipv4/tcp_bbr.c:bbr_high_gain comment | read |
| uth-os-net-load-balancing-1-ring | npoints = weight * 160, crc32 of host/port/prev hash; binary search for first point >= hash | N:src/http/modules/ngx_http_upstream_hash_module.c:chash point setup (lines 362-433), ngx_http_upstream_find_chash_point | read |
| uth-os-net-load-balancing-2-swrr | algorithm: current_weight += effective_weight; pick max; best->current_weight -= total; skips down/max_fails/max_conns | N:src/http/ngx_http_upstream_round_robin.c:ngx_http_upstream_get_peer | read |
| uth-os-net-load-balancing-2-swrr | 5:1:1 gives a a b a c a a, returns to 0 after 7 rounds | hand-simulation of the code above (ties keep first max) | derived by hand |
| uth-os-net-load-balancing-3-p2c | equal weights: pick N (default 2) random hosts, fewest active requests; P2C; herding; weighted formula weight/(active+1)^bias | envoyproxy/envoy@main:docs/root/intro/arch_overview/upstream/load_balancing/load_balancers.rst | read |
| uth-os-net-rate-limit-1-token | SmoothBursty maxBurstSeconds 1.0; fields storedPermits, nextFreeTicketMicros | google/guava@v33.7.0:guava/src/com/google/common/util/concurrent/RateLimiter.java:create, SmoothRateLimiter.java | read |
| uth-os-net-rate-limit-1-token | resync adds (now - nextFree)/coolDown permits capped at maxPermits; reserveEarliestAvailable returns old nextFree and advances it | SmoothRateLimiter.java:resync, reserveEarliestAvailable | read |
| uth-os-net-rate-limit-2-leaky | excess = excess - rate*ms/1000 + 1000, floor 0; reject if excess > burst; burst stored *1000; delay from excess; "leaky bucket" | N:src/http/modules/ngx_http_limit_req_module.c:ngx_http_limit_req_lookup, _account, _create_conf; nginx.org ngx_http_limit_req_module doc | read |
| uth-os-net-rate-limit-3-state | rbtree + LRU queue in shared zone; 64/128 B state; 1 MB about 16k/8k states; LRU eviction; binary addr 4/16 B | N:ngx_http_limit_req_module.c (rbtree, queue); nginx.org doc | read |
| uth-devtools-git-objects-1-content-address | header "<type> <size>" + NUL hashed with content | G:object-file.c:format_object_header | read |
| uth-devtools-git-objects-1-content-address | zlib-deflated, path = first 2 / remaining 38 hex chars | progit2:book/10-git-internals/sections/objects.asc | read |
| uth-devtools-git-objects-1-content-address | SHA-1 default, SHA-256 supported, transition doc | G:hash.h (GIT_HASH_SHA256), Documentation/technical/hash-function-transition.adoc | read |
| uth-devtools-git-objects-2-merkle | tree entries = mode + hash + name; branch is a file in .git/refs/heads holding a SHA-1 | progit2:objects.asc, refs.asc | read |
| uth-devtools-git-objects-3-pack | OBJ_OFS_DELTA (6) / OBJ_REF_DELTA (7); copy/insert instructions | G:Documentation/gitformat-pack.adoc | read |
| uth-devtools-git-objects-3-pack | window = 10, depth = 50 | G:builtin/pack-objects.c (static int window = 10, depth = 50); Documentation/config/pack.adoc | read |
| uth-devtools-git-objects-3-pack | sort by type, name hash, size large first; large window expensive | G:builtin/pack-objects.c:type_size_sort; Documentation/technical/pack-heuristics.adoc | read |
| uth-devtools-diff-1-myers | xdiff cites Myers O(ND), forward/backward diagonals from both ends (xdl_split) | G:xdiff/xdiffi.c header comments | read |
| uth-devtools-diff-1-myers | heuristic cut: mxcost = bogosqrt(ndiags), at least 256 (XDL_MAX_COST_MIN); need_min bypass | G:xdiff/xdiffi.c:xdl_do_diff, xdl_split | read |
| uth-devtools-diff-1-myers | default algorithm myers; minimal / patience / histogram exist | G:Documentation/diff-algorithm-option.adoc | read |
| uth-devtools-diff-1-myers | insert/delete-only edit distance = n + m - 2 LCS | en.wikipedia.org/wiki/Longest_common_subsequence | read |
| uth-devtools-diff-2-preprocess | lines classified to minimal_perfect_hash integers | G:xdiff/xprepare.c:xdl_classify_record | read |
| uth-devtools-diff-2-preprocess | xdl_trim_ends trims matching head/tail; cleanup discards records with no match on the other side; mlim = bogosqrt(nrec) capped at XDL_MAX_EQLIMIT 1024, unlimited with XDF_NEED_MINIMAL | G:xdiff/xprepare.c:xdl_trim_ends, xdl_cleanup_records | read |
| uth-devtools-diff-3-patience | unique lines, longest increasing common sequence, recursion, Myers between anchors | G:xdiff/xpatience.c header comment, find_longest_common_sequence | read |
| uth-devtools-diff-3-patience | histogram extends patience for low-occurrence elements | G:Documentation/diff-algorithm-option.adoc | read |
| uth-devtools-build-deps-1-topo | DFS RecomputeNodeDirty with stack, VerifyDAG error "dependency cycle: "; dirty by most recent input mtime vs output | ninja-build/ninja@v1.13.2:src/graph.cc | read |
| uth-devtools-build-deps-1-topo | GuessParallelism: 1 CPU -> 2, 2 -> 3, else processors + 2 | ninja@v1.13.2:src/ninja.cc:GuessParallelism | read |
| uth-devtools-build-deps-1-topo | make message "Circular xxx <- yyy dependency dropped" | gnu.org/software/make/manual (Common Errors) | read |
| uth-devtools-build-deps-2-pip | no precomputed tree, backtracking, metadata on demand, resolvelib provider | pypa/pip@main:docs/html/topics/more-dependency-resolution.md | read |
| uth-devtools-build-deps-2-pip | version resolution is SAT / NP-complete | astral-sh/uv@main:docs/reference/internals/resolver.md | read |
| uth-devtools-build-deps-3-pubgrub | pubgrub-rs, incompatibility {a 2, b 2} example, error trace, highest-first, lockfile preference, metadata loading slowest | uv@main:docs/reference/internals/resolver.md | read |
| uth-devtools-regex-1-backtrack-automata | Go regexp guaranteed linear; RE2 syntax | golang/go@go1.25.0:src/regexp/regexp.go package doc | read |
| uth-devtools-regex-1-backtrack-automata | RE2: no backreferences or generalized assertions | google/re2@2025-11-05:re2/re2.h header | read |
| uth-devtools-regex-1-backtrack-automata | a?^n a^n: Perl over 60 s at n=29, Thompson NFA 20 microseconds | swtch.com/~rsc/regexp/regexp1.html | read |
| uth-devtools-regex-2-cloudflare | 2019-07-02 WAF rule, core `.*(?:.*=.*)`, CPU near 100%, 502s | blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/ | read |
| uth-devtools-regex-2-cloudflare | possessive quantifiers and atomic groups, added 3.11 | python/cpython@v3.14.0:Doc/library/re.rst | read |
| uth-devtools-regex-2-cloudflare | single-start cost O(n^2) of `.*(?:.*=.*)` with no `=` | reasoning (pairs of split points) | derived |
| uth-devtools-regex-3-go-engines | onepass -> backtrack when len < maxBitStateLen -> NFA | go1.25.0:src/regexp/exec.go:doExecute | read |
| uth-devtools-regex-3-go-engines | maxBacktrackProg 500, maxBacktrackVector 256*1024 bits, maxBitStateLen = vector/len(prog.Inst) | go1.25.0:src/regexp/backtrack.go | read |
| uth-devtools-editor-buffers-1-gap | gap buffer: gpt, gap_size; GAP_BYTES_DFL 2000; make_gap_larger adds nbytes + 2000; gap_left moves by copying | emacs-mirror/emacs@emacs-30.1:src/buffer.h, src/insdel.c | read |
| uth-devtools-editor-buffers-2-piece | piece tree: red-black tree, left-subtree length/line-break counts, O(log N) line lookup, 35 MB / 13.7M lines -> about 600 MB, near file size after piece tree, VS Code 1.21 | code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation | read |
| uth-devtools-editor-buffers-3-undo | Vim undo branches / undo-tree, :undolist, change numbers, undo files | vim/vim@v9.1.0000:runtime/doc/undo.txt | read |
| uth-devtools-compression-1-deflate | distance 1..32768, length 3..258, code lengths 0..15 | RFC 1951 sections 3.2.5, 3.2.7 | read |
| uth-devtools-compression-1-deflate | MIN_MATCH 3, MAX_MATCH 258; level 6 {8,16,128,128}, level 9 chain 4096; default level 6 | madler/zlib@v1.3.2:deflate.c:configuration_table, zutil.h, zlib.h | read |
| uth-devtools-compression-2-huffman | code lengths 0..15 transmitted, shorter codes first, same-length codes in alphabet order | RFC 1951 section 3.2.2 | read |
| uth-devtools-compression-3-zstd-lz4 | LZ4: token 4+4 bits, offset max 65535, minmatch 4, 255 continuation bytes | lz4/lz4@v1.10.0:doc/lz4_Block_format.md | read |
| uth-devtools-compression-3-zstd-lz4 | zstd default level 3; decoders support windows up to 8 MB; FSE + Huffman | facebook/zstd@v1.5.7:lib/zstd.h; RFC 8878 | read |
