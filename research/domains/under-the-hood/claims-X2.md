# Claim ledger, group X2 (ai.vector-search, ai.dedup, ai.autograd)

Sources fetched in this session: pgvector v0.8.0 (`README.md`, `src/hnsw.h`, `src/hnswutils.c`), hnswlib v0.8.0
(`hnswlib/hnswalg.h`), faiss v1.8.0 (`faiss/IndexIVF.h`), HNSW paper arXiv 1603.09320 abstract, datatrove v0.8.0
(`src/datatrove/pipeline/dedup/minhash.py`, `utils/hashing.py`), PyTorch v2.14.0 (`torch/csrc/autograd/engine.cpp`,
`input_buffer.cpp`, `node.h`, `functions/accumulate_grad.h`, `docs/source/notes/autograd.md`), JAX autodiff cookbook.
All "read" = read in the fetched file this session. Arithmetic rows were recomputed with `python3`.

| card id | claim | source | how checked |
|---|---|---|---|
| uth-ai-vector-search-1-graph-walk | brute-force exact search is pgvector's default; HNSW is an approximate index | pgvector@v0.8.0:README.md "By default, pgvector performs exact nearest neighbor search" | read |
| uth-ai-vector-search-1-graph-walk | HNSW default `m = 16` ("max number of connections per layer") | pgvector@v0.8.0:README.md; src/hnsw.h `HNSW_DEFAULT_M 16` | read |
| uth-ai-vector-search-1-graph-walk | layer 0 allows 2m = 32 neighbours, upper layers m | pgvector@v0.8.0:src/hnsw.h `HnswGetLayerM(m, layer) (layer == 0 ? (m) * 2 : (m))`; hnswlib@v0.8.0 `maxM0_ = M_ * 2` | read |
| uth-ai-vector-search-1-graph-walk | search goes greedily from the top layer down, one entry point per layer, then a wider search on layer 0 | hnswlib@v0.8.0:hnswalg.h `searchKnn` (loop `for level = maxlevel_; level > 0`, then `searchBaseLayerST`) | read |
| uth-ai-vector-search-1-graph-walk | layers are nested subsets, higher layer = fewer points, similar to a skip list, logarithmic scaling | arXiv 1603.09320 abstract ("nested subsets", "exponentially decaying probability", "logarithmic complexity scaling", "Similarity ... to the skip list") | read |
| uth-ai-vector-search-1-graph-walk | worked example (5 to 40 on top, 40 to 33 on bottom, vs 5-12-25-33 on bottom) | constructed by hand on the figure's 7 points; each hop moves to a neighbour closer to 30 | derived |
| uth-ai-vector-search-2-ef-heaps | layer search keeps a nearest-first candidate heap C and a furthest-first result heap W, plus a visited set | pgvector@v0.8.0:src/hnswutils.c `HnswSearchLayer` (`pairingheap_allocate(CompareNearestCandidates)` for C, `CompareFurthestCandidates` for W, `visited_hash`); hnswlib `searchBaseLayerST` (two `priority_queue`s, `visited_array`) | read |
| uth-ai-vector-search-2-ef-heaps | stop when nearest candidate is farther than the furthest result | hnswutils.c `HnswSearchLayer`: `if (c->distance > f->distance) break;`; hnswlib `candidate_dist > lowerBound && top_candidates.size() == ef` | read |
| uth-ai-vector-search-2-ef-heaps | W trimmed to `ef` (new closer point pushes out the furthest) | hnswutils.c `if (wlen > ef) { ... pairingheap_remove_first(W)`; hnswlib `top_candidates.size() > ef` pop | read |
| uth-ai-vector-search-2-ef-heaps | `hnsw.ef_search` default 40, range 1 to 1000 | pgvector@v0.8.0:README.md "(40 by default)"; src/hnsw.h `HNSW_DEFAULT_EF_SEARCH 40`, `HNSW_MIN_EF_SEARCH 1`, `HNSW_MAX_EF_SEARCH 1000` | read |
| uth-ai-vector-search-2-ef-heaps | results are limited by `ef_search` | README "Results are limited by the size of the dynamic candidate list (`hnsw.ef_search`)" | read |
| uth-ai-vector-search-2-ef-heaps | filtering happens after the index scan; 10% matching + ef_search 40 gives about 4 rows | README: "If a condition matches 10% of rows, with HNSW and the default `hnsw.ef_search` of 40, only 4 rows will match on average" | read |
| uth-ai-vector-search-2-ef-heaps | example LC 778 code (best-first with heap and seen set) | `vault/interviews/core/leetcode/tiktok/cards/b/tlc-swim-in-rising-water-0-whole.md` | copied unchanged |
| uth-ai-vector-search-3-layers | level = floor(-ln(U) * ml), ml = 1/ln(m) | pgvector@v0.8.0:src/hnswutils.c `HnswInitElement` `(int) (-log(RandomDouble()) * ml)`; src/hnsw.h `HnswGetMl(m) (1 / log(m))`; hnswlib `getRandomLevel`, `mult_ = 1 / log(1.0 * M_)` | read |
| uth-ai-vector-search-3-layers | P(level >= L) = m^-L | derived: P(-ln U / ln m >= L) = P(U <= m^-L) = m^-L | derived |
| uth-ai-vector-search-3-layers | for m = 16 and 1M points: 62500, 3906, 244, 15, 0.95 points at layers 1 to 5 | `python3`: `1e6 * 16**-L` for L = 1..5 | ran |
| uth-ai-vector-search-3-layers | skip list keeps half per layer | textbook skip list with p = 1/2; HNSW paper abstract notes the similarity | read (abstract) |
| uth-ai-vector-search-4-ivf | IVFFlat divides vectors into lists and searches the closest subset; faster build and less memory than HNSW but worse speed-recall | pgvector@v0.8.0:README.md "IVFFlat" section | read |
| uth-ai-vector-search-4-ivf | build runs k-means ("performing k-means" build phase), then assigns tuples | README, progress phases list (`initializing`, `performing k-means`, `assigning tuples`, `loading tuples`) | read |
| uth-ai-vector-search-4-ivf | `lists`: rows/1000 up to 1M rows, sqrt(rows) above; probes start at sqrt(lists); `ivfflat.probes` default 1 | README "Three keys to achieving good recall"; "Specify the number of probes (1 by default)"; faiss@v1.8.0 `nprobe = 1` also | read |
| uth-ai-vector-search-4-ivf | probes = lists is exact search and the planner will not use the index | README: "can be set to the number of lists for exact nearest neighbor search (at which point the planner won't use the index)" | read |
| uth-ai-vector-search-4-ivf | create the index after the table has data; too little data for the lists gives fewer results | README: "Create the index *after* the table has some data"; "Why are there less results ... created with too little data for the number of lists" | read |
| uth-ai-dedup-1-minhash | defaults: 5-grams, 14 buckets, 8 hashes per bucket (112 hashes) | datatrove@v0.8.0:minhash.py `MinhashConfig` (`n_grams: int = 5`, `num_buckets: int = 14`, `hashes_per_bucket: int = 8`), `num_hashes = num_buckets * hashes_per_bucket` | read |
| uth-ai-dedup-1-minhash | shingles are word n-grams of simplified text, hashed | minhash.py `get_shingles` (`word_tokenize(simplify_text(...))`, `ngrams(..., self.config.n_grams)`) | read |
| uth-ai-dedup-1-minhash | permutations are random universal-hash functions `(a*x+b) mod p`, p = 2^61 - 1; signature = min per function | minhash.py `parameters` docstring, `_mersenne_prime = (1 << 61) - 1`, `get_signature` `phv = (shingles * a + b) % _mersenne_prime`, `np.min(phv, axis=0)` | read |
| uth-ai-dedup-1-minhash | P(min of two sets equal) = Jaccard: the first element of the union is shared iff it is in the intersection | derived; worked table: A={a,b,c,d}, B={b,c,d,e}, 3/5 = 0.6; each row checked by hand (first element of the order present in each set) | derived |
| uth-ai-dedup-2-lsh | signature split into 14 bands of 8; docs state threshold (1/14)^(1/8) ~ 0.72, P(0.8) = 0.924 | datatrove@v0.8.0:minhash.py module docstring | read |
| uth-ai-dedup-2-lsh | P(pair) = 1-(1-s^8)^14: 0.5 -> 5.3%, 0.7 -> 56.5%, 0.8 -> 92.4%, 0.9 -> 99.96%; (1/14)^(1/8) = 0.719 | `python3` | ran |
| uth-ai-dedup-2-lsh | each bucket's signatures are sorted per file, then merged with a heap; equal consecutive signatures are written out as a duplicate pair | minhash.py `MinhashDedupSignature.run` ("Sorting buckets", `records.sort`), `MinhashDedupBuckets.run` (`heapq`, `last.sig == v.sig` writes a pair) | read |
| uth-ai-dedup-2-lsh | example LC 49 code (key per element, group by key) | `vault/interviews/core/leetcode/tiktok/cards/a/tlc-group-anagrams-0-whole.md` | copied unchanged |
| uth-ai-dedup-3-union-find | cluster stage unions duplicate pairs, path compression and union by size | minhash.py `MinhashDedupCluster.run` (`parent` with "Path Compression", `union` with "Union by size") | read |
| uth-ai-dedup-3-union-find | only the root of each cluster is kept; the others go to `.remove` files, and the filter stage drops them | minhash.py `MinhashDedupCluster.run` (`if node != p: output_mg.write(f"{file:06d}.remove", ...)`), `MinhashDedupFilter.run` | read |
| uth-ai-dedup-3-union-find | clustering runs with world size 1 | minhash.py `assert world_size == 1, "World size must be 1 for clustering"` | read |
| uth-ai-dedup-3-union-find | A-B and B-C pairs give one A-B-C cluster, only one document kept | minhash.py `MinhashDedupCluster` docstring | read |
| uth-ai-dedup-3-union-find | example LC 721 code | `vault/interviews/core/leetcode/tiktok/cards/a/tlc-accounts-merge-0-whole.md` | copied unchanged |
| uth-ai-autograd-1-record-replay | autograd records a DAG of operations, traversed from roots to leaves by the chain rule; nodes are `grad_fn` | pytorch@v2.14.0:docs/source/notes/autograd.md "How autograd encodes the history" | read |
| uth-ai-autograd-1-record-replay | forward mode builds a Jacobian one column at a time at about one function evaluation each; reverse mode suits a scalar loss over many parameters | JAX autodiff cookbook (jacfwd / jacrev, "wide" Jacobians) | read |
| uth-ai-autograd-1-record-replay | worked example d = a*b + a at a=2, b=3: d=8, grads a=4, b=2 | hand derivation and `python3`: d/da = b + 1 = 4, d/db = a = 2 | derived |
| uth-ai-autograd-2-dependency-count | `compute_dependencies` walks the graph from the root and increments `dependencies[next]` per edge | pytorch@v2.14.0:torch/csrc/autograd/engine.cpp `Engine::compute_dependencies` | read |
| uth-ai-autograd-2-dependency-count | in `evaluate_function`, `--it->second == 0` marks the next node ready and pushes it to the ready queue, otherwise its `InputBuffer` waits in `not_ready` | engine.cpp `Engine::evaluate_function` | read |
| uth-ai-autograd-2-dependency-count | several incoming gradients for one input are summed in the `InputBuffer` | input_buffer.cpp `accumulate` (`buffer[pos] = old_var + var` / `add_`) and `InputBuffer::add` | read |
| uth-ai-autograd-2-dependency-count | ready queue is a priority queue; larger `sequence_nr` (later forward op) runs first | engine.h `ReadyQueue` `std::priority_queue` with `t1.fn_->sequence_nr() < t2.fn_->sequence_nr()`; node.h NOTE [Sequence Number] "nodes with higher priority numbers are executed first ... ops executed later are the first to be executed in the backward pass" | read |
| uth-ai-autograd-2-dependency-count | example LC 210 code (Kahn's algorithm) | `vault/interviews/core/leetcode/tiktok/cards/a/tlc-course-schedule-ii-0-whole.md` | copied unchanged |
| uth-ai-autograd-3-saved-tensors | ops such as x^2 save their input for backward | autograd.md "Saved tensors" ("the function x -> x^2 saves the input x") | read |
| uth-ai-autograd-3-saved-tensors | no-grad mode records nothing in the backward graph | autograd.md "No-grad Mode" ("never recorded in the backward graph") | read |
| uth-ai-autograd-3-saved-tensors | backward with `retain_graph=False` releases saved tensors; a second backward without `retain_graph=True` errors | autograd.md ("Running backward with retain_graph=False releases the saved tensor"; "calling backward() twice without retain_graph=True ... error") | read |
| uth-ai-autograd-3-saved-tensors | only leaf tensors with `requires_grad=True` get `.grad`, and gradients accumulate into it | autograd.md ("only leaf tensors with requires_grad=True will have gradients accumulated into their .grad"); functions/accumulate_grad.h ("variable_grad += new_grad") | read |
| uth-ai-autograd-3-saved-tensors | snippet output 6 then 12 | derived: d(x*x)/dx = 2x = 6 at x=3; second backward on a fresh graph adds another 6 into the existing `.grad` | derived (not run) |
