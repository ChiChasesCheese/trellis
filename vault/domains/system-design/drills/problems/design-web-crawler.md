---
nodes: [problems.search.web-crawler, async.queues, networking.dns]
tags: [problem]
---
# Drill: Design a polite, distributed web crawler

Design a crawler that discovers and fetches 10 billion pages over a 30-day cycle, starting
from a set of seed URLs, without overwhelming any single site and without getting stuck in
pathological link structures.

**Constraints to state and honor**
- Never exceed a per-host request rate the target site can tolerate; honor robots.txt disallow rules.
- Never re-crawl a URL already seen, and recognize near-duplicate content reached via different URLs.
- Handle sites with effectively infinite link structures (e.g. calendar pages) without burning the whole crawl budget on one host.
- Re-crawl already-fetched pages at a rate proportional to how often they actually change, not a single fixed interval for everyone.

**Grading points**
- Designs a URL frontier that gives both priority ordering and per-host isolation without needing one physical queue per discovered host ([[problems-web-crawler-mercator-front-back-queues]]).
- Computes why the number of distinct hosts that must be in flight at once, not raw fetch QPS, sets the real machine-count floor under a politeness constraint ([[problems-web-crawler-host-concurrency-sets-machine-floor]]).
- Chooses a Bloom filter for URL-seen deduplication and justifies it by the false-positive/false-negative asymmetry rather than just citing "it saves memory" ([[problems-web-crawler-bloom-filter-asymmetric-tolerance]]).
- Treats URL-level dedup and content-level near-duplicate detection as two separate mechanisms, not one ([[problems-web-crawler-url-vs-content-dedup-two-problems]]).
- Does not treat robots.txt `Crawl-delay` as an authoritative throttle, and explains why with a real standards citation ([[problems-web-crawler-crawl-delay-not-standardized]]).
- Detects spider traps using both URL pattern similarity and content similarity together, not a single fixed max-depth cutoff ([[problems-web-crawler-spider-trap-pattern-plus-similarity]]).
- Correctly argues that DNS is not the bottleneck at this scale once per-host caching is in place, and doesn't over-engineer it ([[problems-web-crawler-dns-not-the-bottleneck]]).
- Recognizes that no amount of added fetcher capacity can raise the sustainable rate against one popular host, and that scaling further means increasing host breadth, not per-host rate ([[problems-web-crawler-politeness-caps-scale-out-not-up]]).

**Solution**: [[solution-web-crawler]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
