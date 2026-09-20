---
nodes: [problems.commerce.digital-wallet, distributed.transactions.distributed, correctness.ledger]
tags: [problem]
---
# Drill: Design a digital wallet that transfers balances between accounts on different shards

A P2P wallet product: users hold a balance and can transfer to any other user's wallet.
Accounts are sharded by account id across many shards, and most transfers land on two
different shards. Balances must never go negative and must never be lost or duplicated,
even under concurrent transfers and shard failures.

**Constraints to state and honor**
- 256 account shards, peak ~1,450 transfers/sec, P99 transfer latency < 1s.
- Balance reads must be linearizable relative to a completed transfer — no stale "money
  missing" window.
- One leg of some transfers is external (bank top-up / withdrawal via a PSP), not another
  wallet shard.
- Accounts must be migratable to a different shard without losing in-flight transfers.

**Grading points**
- Compute the fraction of transfers that are cross-shard given the shard count, and use it
  to justify treating cross-shard coordination as the default path, not an edge case
  ([[problems-digital-wallet-cross-shard-probability]]).
- Choose the coordination protocol by whether each participant is internal or external:
  2PC for wallet-to-wallet, TCC for the external PSP/bank leg
  ([[problems-digital-wallet-2pc-vs-tcc-by-participant]], [[distributed-internal-vs-heterogeneous-2pc]]).
- Explain a concrete TCC failure mode (dangling/suspension) and the fencing-log fix
  ([[problems-digital-wallet-tcc-dangling-fence]]).
- Explain why a saga is wrong for the core money movement but fine for side effects
  ([[problems-digital-wallet-why-not-saga-for-core-transfer]], [[distributed-saga-tradeoffs]]).
- Require the event-log replay function to be a deterministic pure reducer, and justify why
  ([[problems-digital-wallet-deterministic-reducer]]).
- Design a shard migration procedure that never lets an in-flight transfer diverge between
  source and target ([[problems-digital-wallet-shard-migration-freeze-drain-replay]]).
- State a snapshot cadence for balance derivation and justify it with the growth of a heavy
  account's event count ([[problems-digital-wallet-heavy-account-snapshot-cadence]], [[correctness-balance-derivation]]).

**Solution**: [[solution-digital-wallet]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
