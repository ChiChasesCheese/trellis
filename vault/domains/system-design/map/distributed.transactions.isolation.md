%% trellis:begin %%
# Isolation Levels & Anomalies
*Distributed Data / Transactions*

Read committed to serializable through the anomalies each level permits — dirty/non-repeatable reads, write skew, phantoms.

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/system-design/map/problems.commerce.ticket-booking|Ticket Booking (Ticketmaster)]], [[domains/system-design/map/problems.commerce.hotel-reservation|Hotel & Marketplace Reservation (Airbnb)]]

## Readings
- [[hermitage-isolation-levels|Hermitage: Testing the "I" in ACID (Kleppmann)]]

## Drills
- [[design-hotel-reservation|Drill: Design a hotel/marketplace reservation system like Airbnb]]
- [[design-ticket-booking|Drill: Design a ticket booking platform like Ticketmaster]]

## Cards (8)
1. [[distributed-dirty-write]]
2. [[distributed-isolation-anomalies]]
3. [[distributed-read-committed-anomalies]]
4. [[distributed-lost-update-vs-write-skew]]
5. [[distributed-write-skew]]
6. [[distributed-phantoms-predicate-locks]]
7. [[distributed-materializing-conflicts]]
8. [[distributed-repeatable-read-dialects]]
%% trellis:end %%

## Notes
