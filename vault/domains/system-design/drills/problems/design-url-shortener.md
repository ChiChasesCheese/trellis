---
nodes: [problems.foundations.url-shortener, caching.strategies, storage.nosql]
tags: [problem]
---
# Drill: Design a URL shortener

Design a service like Bitly or TinyURL: users submit a long URL and get back a
short one; anyone who visits the short link is redirected to the original.
Assume a public, read-heavy product where most links are shared and clicked
far more often than they are created.

**Constraints to state and honor**
- 1,000,000 new short links per day; a 100:1 read-to-write (redirect-to-create) ratio.
- Redirect p99 latency < 100ms; redirect path availability target 99.99%.
- Default 5-year retention; links can carry an optional custom alias and an optional expiration date.

**Grading points**
- States and uses the DAU→QPS arithmetic correctly, and says which estimate changes which design decision ([[problems-url-shortener-capacity-arithmetic]]).
- Justifies the storage choice by access pattern (pure key lookup, no joins) rather than by raw data volume ([[problems-url-shortener-nosql-vs-relational]]).
- Picks a collision-free short-code generation scheme and argues it against a hashing-based alternative with a concrete collision-probability estimate ([[problems-url-shortener-counter-vs-hash]]).
- Separates the point-lookup cache-aside read path from write-through population, per the cache-aside/read-through distinction ([[caching-aside-vs-read-through]]).
- Identifies hot-key (viral-link) traffic as a distinct problem from average load and names two mitigations for it ([[problems-url-shortener-hot-key-mitigation]]).
- Keeps click analytics off the synchronous redirect path and explains the write-amplification risk of not doing so ([[problems-url-shortener-async-analytics]]).
- Defends the 302-vs-301 redirect status code choice against the alternative's caching benefit ([[problems-url-shortener-302-vs-301]]).
- Explains what degrades and what keeps working when the short-code coordination service goes down ([[problems-url-shortener-kgs-outage]]).
- Describes the structural change to the design at 10x and 100x traffic, not just "add more servers" ([[problems-url-shortener-10x-100x-evolution]]).

**Solution**: [[solution-url-shortener]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
