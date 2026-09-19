You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "caching.strategies": ["<id shown first>", "…"],
  "caching.invalidation": ["<id shown first>", "…"],
  "caching.placement": ["<id shown first>", "…"]
}

## caching.strategies — Write & Read Strategies
Cache-aside, read-through, write-through, write-behind, refresh-ahead — who populates the cache and when.
- `caching-aside-vs-read-through` Q: Cache-aside and read-through both populate the cache on a miss. What actually differs, and when does that difference matter?
  A: **Who owns the load logic.** In cache-aside the *application* checks the cache, fetches from the DB on miss, and writes the cache; in read-through the *cache la
- `caching-cache-warming` Q: A new cache cluster (or one recovering from a flush) goes live cold. What happens at cutover, and what are three warming techniques?
  A: Hit rate starts at ~0%, so the database briefly receives the *full* read load it was never provisioned for — the cold-start herd can take it down (the math: [[c
- `caching-memcached-vs-redis` Q: When is Memcached the right pick over Redis, and what does Redis add that decides most other cases?
  A: **Memcached**: multithreaded (one instance saturates all cores), simple slab-allocated LRU byte cache, very flat performance — right when the job is purely a lo
- `caching-negative-caching` Q: Lookups for keys that *don't exist* miss the cache every time and hit the DB. What's the fix, and its two risks?
  A: **Negative caching**: on a DB miss, store a "not found" marker under the key with a short TTL — repeated lookups (dead links, scrapers, id enumeration) get abso
- `caching-refresh-ahead-fit` Q: When is refresh-ahead worth the complexity over plain TTL + cache-aside, and what does it waste when misapplied?
  A: Refresh-ahead asynchronously reloads a key *before* its TTL expires, so hot keys never pay a miss. - Worth it when: a small, predictable set of hot keys, expens
- `caching-write-through-vs-behind` Q: Write-through vs write-behind (write-back): what does each cost you, and what breaks in write-behind if the cache node dies?
  A: - **Write-through**: write goes to cache *and* store synchronously. Cost: every write pays store latency; cache is never fresher than needed. Safe but slow. - *

## caching.invalidation — Invalidation & Eviction
TTLs, eviction policies, stale reads, and cache stampede protection.
- `caching-cdc-invalidation` Q: Why drive cache invalidation from the database's change stream (CDC/binlog) instead of application code — and what gap remains?
  A: App-side invalidation must be remembered on *every* write path, and it silently fails when an app server crashes between DB commit and cache delete — stale unti
- `caching-delete-not-update` Q: On a DB write, why is *deleting* the cache key generally safer than *updating* it with the new value?
  A: Concurrent updates race: two writers can update the DB in one order and the cache in the opposite order, leaving the cache holding the **older value indefinitel
- `caching-key-version-invalidation` Q: You need to invalidate a whole *group* of cache entries at once (every page of a user's feed) without tracking each key. Pattern and costs?
  A: **Generation (versioned) keys**: embed a per-group version in every key — `feed:{user}:v42:page3`. To invalidate the group, bump the version; old entries become
- `caching-lease-cas` Q: Even with delete-on-write, cache-aside has a residual stale-set race. How do memcached *leases* (Facebook) close it?
  A: The race: reader misses, reads the old value from the DB; a write commits and deletes the key; the reader then sets its stale value — wrong until TTL ([[caching
- `caching-lru-vs-lfu` Q: Your cache hit rate collapses whenever a nightly batch job scans the full table. Which eviction policy is failing, and what do you switch to?
  A: **LRU** — a one-time scan touches every key once and evicts the genuinely hot working set (cache pollution / scan thrash). Switch to a frequency-aware policy: *
- `caching-ttl-jitter` Q: When many keys are warmed at the same moment (deploy, cache flush, midnight job), identical TTLs make them all expire together and hammer the backend at once. The fix is {{c1::adding random jitter to each TTL (e.g. `ttl + rand(0, 10%·ttl)`)}} so expiries spread out; for a single hot key, use {{c2::a lock / single-flight recompute (one request rebuilds, others serve stale)}} to stop a stampede.

## caching.placement — Cache Placement
Client, CDN, gateway, application, and database layers — what each layer can and cannot absorb.
- `caching-cache-shard-blast-radius` Q: Clients shard keys across 10 cache nodes. Why consistent hashing instead of `hash(key) % 10`, and what is the blast radius when one node dies?
  A: With modulo, any membership change remaps nearly **all** keys — adding or losing a node is an effective cluster-wide flush, and the resulting miss storm lands o
- `caching-hit-rate-outage-math` Q: Second-order dependency math: at a 99% hit rate, losing the cache multiplies database read load by {{c1::100× (1 ÷ miss rate)}} — so either the DB is provisioned for full miss-storm traffic (almost never) or the cache is a **hard dependency** that needs {{c2::HA (replication/failover) plus warmed, gradual recovery — never a cold restart into live traffic}}. The trap: every hit-rate improvement quietly shrinks DB headroom, until a "cache" the database cannot survive without is really {{c3::a serving tier, not an optimization}}.
- `caching-hot-key-replication` Q: One cache key (a celebrity's profile during an event) exceeds what a single cache node can serve. Why doesn't adding nodes help, and what does?
  A: Sharding places each key on exactly **one** node — more nodes just move the key; that node's NIC and CPU still cap the key's throughput. - **Key replication**: 
- `caching-layer-absorption` Q: Traffic doubles on a page that is 90% identical for all users and 10% personalized. Which cache layers absorb which part, and why can't the CDN take it all?
  A: - **CDN/edge** absorbs the shared 90%: static assets and any response whose cache key is URL-derivable and user-independent. - The personalized 10% must be serv
- `caching-local-vs-remote` Q: In-process (local) cache vs shared remote cache (Redis): what do you gain and lose with each, and what pattern combines them?
  A: - **In-process**: ~100ns–1µs access, no network hop — but each instance holds its own copy (memory × N, cold on every deploy) and **cross-instance invalidation 
- `caching-placement-cost-of-depth` Q: Each cache layer sits closer to the client than the last, and the trade moves the same direction every step: pushing a cache toward the client (browser → CDN → gateway → app → DB) buys {{c1::lower latency and more offloaded backend traffic}} at the price of {{c2::weaker control over freshness/invalidation and less request context (no auth, no per-user data) available at that layer}}.
