# Task: amazon.amz-locker-onsite

- **Leaf id**: `amazon.amz-locker-onsite`   **slug**: `amz-locker-onsite`   **kind**: cards-only (5–7 stepped cards, no problem folder) + readings
- **题目**: Amazon 现场版快递柜（Amazon Locker, onsite）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- 1p3a 1193105 (posted 2026-10-14; SDE II, in-person onsite 2026-10-02, four back-to-back rounds; summary: 'OA, phone screen, four-round onsite, task and course scheduling, URL shortener design, and Amazon Locker LLD'; coding/LLD were dry run) https://www.1point3acres.com/bbs/thread-1193105-1-1.html [high for the problem name; details hidden]
- Hello Interview `amazon-lockers-delivery` (system design, senior, 2026-09-10): 'package delivery system that integrates with e-commerce platforms, allowing customers to select locker locations during checkout and securely retrieve their packages using authentication codes' https://www.hellointerview.com/community/questions?company=Amazon (question slug `amazon-lockers-delivery`) [medium]
- kit forums JC-ibzau1 follow-ups: 'locations、S/M/L 格口、取件码带过期、release/return、并发、持久化表'; Locker 4 SDE I / 7 SDE II+ refs (`vault/interviews/companies/amazon/lld/route.md` §2 row 2)

## (reconstructed) — not in any visible report

- the order of follow-ups in this onsite

## Reuse / link (our own repo first)

- bank leaf problems.machines.amazon-locker: [[solution-amazon-locker]], drill design-amazon-locker, its 8 cards (do not duplicate them — these cards are the Amazon-onsite layer: what to write in 45 minutes on a notepad, the follow-ups Amazon asks, multi-location, the SD version)
- HI locker breakdown: /Users/chizhang/.claude/jobs/5ce355d9/tmp/1p3a/hi_lld/amazon-locker.txt (the bank already has src-hellointerview-amazon-locker.md; add a reading `src-1p3a-amz-locker-onsite.md` for the report)

## Card ladder notes

- 1 how Amazon asked it this month + clarify · 2 what to have on the notepad at minute 20 · 3 the follow-ups Amazon adds beyond the bank's 4 stages (multi-location, return flow) · 4 dry-run discipline: walking one package through by hand · 5 the step from LLD to the SD version (checkout picks a location) · 6 (optional) the most common way this round is lost
