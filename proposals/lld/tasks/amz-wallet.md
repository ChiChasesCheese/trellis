# Task: amazon.amz-wallet

- **Leaf id**: `amazon.amz-wallet`   **slug**: `amz-wallet`   **kind**: cards-only   **priority**: （low priority）— append this to the H1 of the article and nowhere else
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` + `proposals/WRITING_RULES.md` (the last wins).
- The learning pages you write carry **no provenance at all** (no report, site, date, confidence, 推断, 重建). The facts below are for you only.

## What was asked (for you, never for the page)

- research/companies/amazon/catalog/raw/forums.md: bank/wallet/ATM 1× SDE I ('deposit / credit / summary / tax, extensible'), 1× SDE II+
- More detail: `grep -nE 'wallet|ATM|deposit' research/companies/amazon/catalog/raw/forums.md`

## Reuse

- bank leaves problems.marketplaces.digital-wallet ([[solution-digital-wallet]]) and problems.marketplaces.bank-account ([[solution-bank-account]])

## Stages / card ladder

- cards: money as integer minor units · balance derived from an append-only ledger · transfer atomicity (lock order) · fee/tax rules as strategies · monthly summary
