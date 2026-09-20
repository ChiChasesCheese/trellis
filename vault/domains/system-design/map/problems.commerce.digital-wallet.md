%% trellis:begin %%
# Digital Wallet
*Design Problems / Commerce, Booking & Money*

Balance transfers that never lose or create money: distributed transactions vs event sourcing.

**Requires:** [[domains/system-design/map/distributed.transactions.distributed|Distributed Transactions]], [[domains/system-design/map/correctness.ledger|Ledgers & Reconciliation]]

## Readings
- [[helland-life-beyond-distributed-transactions|Life beyond Distributed Transactions: An Apostate's Opinion (Pat Helland, CIDR 2007)]]
- [[solution-digital-wallet|设计题解：数字钱包（Digital Wallet）]]
- [[src-eventdrivenio-digital-wallet|Why a bank account is not the best example of Event Sourcing?]]
- [[src-seata-digital-wallet|Alibaba Seata Resolves Idempotence, Dangling, and Empty Rollback Issues in TCC Mode]]
- [[src-spanner-digital-wallet|Spanner: Google's Globally-Distributed Database (OSDI 2012)]]

## Drills
- [[design-digital-wallet|Drill: Design a digital wallet that transfers balances between accounts on different shards]]

## Cards (8)
1. [[problems-digital-wallet-cross-shard-probability]]
2. [[problems-digital-wallet-2pc-vs-tcc-by-participant]]
3. [[problems-digital-wallet-why-not-saga-for-core-transfer]]
4. [[problems-digital-wallet-tcc-dangling-fence]]
5. [[problems-digital-wallet-deterministic-reducer]]
6. [[problems-digital-wallet-heavy-account-snapshot-cadence]]
7. [[problems-digital-wallet-shard-migration-freeze-drain-replay]]
8. [[problems-digital-wallet-more-shards-worsen-coordination]]
%% trellis:end %%

## Notes
