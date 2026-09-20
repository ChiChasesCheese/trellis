You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
Design Problems › Building Blocks & Warm-ups › Pastebin
Store and serve text blobs by short link: metadata vs blob storage, expiry, and abuse limits.

## Position in the knowledge map
Prerequisites (assume known):
  - Object Storage & Separation: S3-style object stores, storage-compute separation, and the modern default of parking cold and big data there.
Sibling topics (OUT of scope):
  - URL Shortener: Short-code generation, a read path that is almost all cache, redirects and analytics at 100:1 read/write.
  - Distributed Rate Limiter: Per-key quotas enforced across many gateways inside a 2 ms budget, and what happens when the counter store is down.
  - Unique ID Generator: Roughly time-ordered 64-bit ids with no coordinator on the hot path; clock skew and sequence exhaustion.
  - Distributed Key-Value Store: Partitioning, replication, quorums, conflict resolution and repair in a Dynamo-style store.
  - Distributed Cache: A Memcached/Redis-class cluster: sharding, eviction, hot keys, replication and cold-start.
  - Content Delivery Network: Request routing, tiered caches, purge and origin shielding for static and large-file delivery.
  - Distributed Message Queue: A Kafka-class log: partitions, replication, consumer groups, retention and delivery semantics.
  - Distributed Job Scheduler: Run millions of scheduled and ad-hoc jobs at least once, on time, with retries and no double-firing.
  - Object Storage (S3): Buckets and immutable blobs at exabyte scale: metadata service, placement, erasure coding, durability math.
  - Distributed Lock & Coordination Service: Leases, fencing tokens and sessions on top of consensus — a Chubby/ZooKeeper-class service.
  - Authentication & Identity Service: Sign-up, login, sessions vs tokens, SSO and revocation for hundreds of millions of accounts.

## Rules
- Write 8 cards for THIS topic only. Sibling topics listed above are
  out of scope — never restate their material.
- One card = one retrievable fact, mechanism, trade-off, or number. If an
  answer needs more than ~4 sentences, split the card.
- Prefer questions that force discrimination ("when would you choose X
  over Y") over definitions, except for terms of art.
- Use `type: "cloze"` with {{c1::...}} syntax for formulas, sequences,
  and lists; `type: "qa"` otherwise.
- Markdown allowed in q/a/text (code spans, tables, lists).
- id: lowercase-hyphenated slug, unique, descriptive, stable.

## Output format (JSON array only, no prose)
[
  {"id": "example-qa-card", "node": "problems.foundations.pastebin", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.foundations.pastebin", "type": "cloze",
    "text": "The formula is {{c1::W + R > N}}.", "tags": []}
]

## Language and self-containment
- Write every card in English. Terms of art stay in English (the reader will
  meet them in code, configs and docs): write the English term and gloss
  it in English once per card, e.g. `consumer group（消费者群组）`.
- SELF-CONTAINED. A reader who has never heard of System Design must understand
  the card from the card alone: the question carries the situation it is
  asking about, the answer defines every term it uses and says WHY, not
  only what. Never "as discussed", "the book says", "see chapter 3" — nor
  their equivalents ("书中建议", "本书", "如前所述"): the importer refuses a
  card that leans on its source. State the advice as a fact.
- Prefer questions whose answer is a mechanism or a decision ("what happens
  when…", "why would you set…") over ones whose answer is a name.
- Do not set `source`; the importer records where these cards came from.

- This domain's cards also carry a Chinese translation, and its deck is
  reviewed in Chinese. Give every card one: `q_zh` and `a_zh` (for a cloze,
  `text_zh` with every `{{{{cN::…}}}}` deletion byte-identical), a faithful
  translation of your English — same structure, terms of art kept in
  English, nothing added or dropped.
