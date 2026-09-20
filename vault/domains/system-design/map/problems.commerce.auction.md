%% trellis:begin %%
# Online Auction (eBay)
*Design Problems / Commerce, Booking & Money*

Concurrent bids with a strict winner, bid fan-out to watchers, and sniping at the close.

**Requires:** [[domains/system-design/map/distributed.transactions.concurrency-control|Concurrency Control]]

## Readings
- [[solution-auction|设计题解：在线拍卖（Online Auction，eBay）]]
- [[src-ebay-automatic-bidding-auction|Automatic bidding — eBay Help]]
- [[src-ebay-bidding-rules-auction|How bidding works — eBay Help]]
- [[src-hellointerview-auction|Design an Online Auction (eBay) — Hello Interview]]
- [[src-systemdesignschool-auction|System Design School — Problem List (Auction System Design)]]

## Drills
- [[design-auction|Drill: Design an online auction platform (eBay-style)]]

## Cards (8)
1. [[problems-auction-contention-differs-from-ticket-booking]]
2. [[problems-auction-collision-rate-drives-serialized-actor]]
3. [[problems-auction-proxy-bid-increment-table-worked-example]]
4. [[problems-auction-watcher-fanout-decoupled-eventual-consistency]]
5. [[problems-auction-soft-close-expected-extension-needs-cap]]
6. [[problems-auction-close-exactly-once-idempotent-token]]
7. [[problems-auction-actor-crash-rebuild-from-store-not-replay]]
8. [[problems-auction-10x-fanout-sharding-not-actor-throughput]]
%% trellis:end %%

## Notes
