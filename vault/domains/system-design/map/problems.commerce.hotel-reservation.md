%% trellis:begin %%
# Hotel & Marketplace Reservation (Airbnb)
*Design Problems / Commerce, Booking & Money*

Inventory by date range, overbooking policy, search vs booking paths.

**Requires:** [[domains/system-design/map/distributed.transactions.isolation|Isolation Levels & Anomalies]]

## Readings
- [[solution-hotel-reservation|设计题解：酒店与民宿预订系统（Hotel & Marketplace Reservation，Airbnb / 连锁酒店）]]
- [[src-airbnb-payments-hotel-reservation|Avoiding Double Payments in a Distributed Payments System]]
- [[src-airbnb-search-hotel-reservation|Embedding-Based Retrieval for Airbnb Search]]
- [[src-expedia-hotel-reservation|Choosing the Right Candidates for Lodging Ranking]]
- [[src-postgresql-isolation-hotel-reservation|Transaction Isolation]]
- [[src-postgresql-rangetypes-hotel-reservation|Range Types]]

## Drills
- [[design-hotel-reservation|Drill: Design a hotel/marketplace reservation system like Airbnb]]

## Cards (8)
1. [[problems-hotel-reservation-peak-booking-vs-search-qps]]
2. [[problems-hotel-reservation-per-night-inventory-model]]
3. [[problems-hotel-reservation-check-then-write-double-books]]
4. [[problems-hotel-reservation-multirow-conditional-update-rollback]]
5. [[problems-hotel-reservation-overbooking-risk-budget]]
6. [[problems-hotel-reservation-search-index-vs-booking-path]]
7. [[problems-hotel-reservation-cross-channel-conflict]]
8. [[problems-hotel-reservation-10x-inventory-sharding]]
%% trellis:end %%

## Notes
