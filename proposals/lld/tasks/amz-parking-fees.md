# Task: amazon.amz-parking-fees

- **Leaf id**: `amazon.amz-parking-fees`   **slug**: `amz-parking-fees`   **kind**: problem
- **题目**: 停车场计费（Parking Lot Fees）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- Hello Interview `parking-lot-system` report 2026-09-20 senior APAC: 'The focus was more on calculating the parking fees and has different logics for different scenarios'; prompt: 'The code is expected to be syntactically correct, although it will not be executed.' https://www.hellointerview.com/community/questions?company=Amazon (question slug `parking-lot-system`) [medium–high]
- kit forums: LC8293563 (parking lot, vehicle types, 5–6 new requirements), LC8568929 (best spot by vehicle type), LC8525216 (parking ticket / receipt system)

## (reconstructed) — not in any visible report

- the concrete fee rules (hourly by vehicle type, first-N-minutes free, daily cap, overnight/weekend rate, lost ticket) — choose a set and label it 推断

## Reuse / link (our own repo first)

- bank [[solution-parking-lot]] (spot allocation — link, do not redo); this leaf is the fee engine on top
- HI parking lot breakdown: /Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/hi_lld/parking-lot.txt
- `vault/interviews/companies/amazon/lld/pricing_billing.md` (Money, tiered pricing, caps)
- concept leaf patterns.strategy

## Card ladder notes

- ladder; step 4 = billing a stay that crosses a rate boundary (split the interval) with a concrete entry/exit time and fee; step 8 = two exits paying the same ticket
