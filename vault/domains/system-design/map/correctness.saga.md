%% trellis:begin %%
# Sagas
*Correctness Patterns*

Long-running workflows via compensating actions when a distributed transaction is off the table.

**Requires:** [[domains/system-design/map/distributed.transactions|Transactions]]

**Unlocks:** [[domains/system-design/map/problems.geo.food-delivery|Food & Grocery Delivery (DoorDash/Gopuff)]], [[domains/system-design/map/problems.commerce.e-commerce|E-Commerce Platform (Amazon)]]

## Readings
- [[microservices-io-saga|Saga (microservices.io, Chris Richardson)]]

## Drills
- [[design-e-commerce|Drill: Design the core purchase flow for an e-commerce platform (Amazon-style)]]
- [[design-food-delivery|Drill: Design a food and grocery delivery platform like DoorDash/Gopuff]]

## Cards (6)
1. [[correctness-saga-vs-2pc]]
2. [[correctness-saga-orchestration-choreography]]
3. [[correctness-saga-compensation-limits]]
4. [[correctness-saga-compensation-race]]
5. [[correctness-saga-isolation]]
6. [[correctness-saga-orchestrator-recovery]]
%% trellis:end %%

## Notes
