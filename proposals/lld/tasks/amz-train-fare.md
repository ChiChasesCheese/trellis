# Task: amazon.amz-train-fare

- **Leaf id**: `amazon.amz-train-fare`   **slug**: `amz-train-fare`   **kind**: problem
- **题目**: 火车线路票价（Train Fare Calculator）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- 1p3a 1192827 (2026-10-12, Amazon SDE onsite, NewGrad): 「设计火车票价计算系统。已知一条火车线路：G → U → H → K → I，每两个相邻站之间的乘车费用为 1（例如，从 G 到 I 的费用为 4）。1. 实现 calculateFare(start, stop) … 2. 考虑 OOP/LLD 设计：思考路线数据从何处获取，设计并实现一个类，支持动态添加/推入站点到路线中。3. 追问：如果是在周末（Weekends），总票价需要设置一个上限封顶」(rest hidden) https://www.1point3acres.com/bbs/thread-1192827-1-1.html [high]
- kit `vault/interviews/companies/amazon/catalog/raw/forums.md` LC8500377 (2026-09): same train route G→U→H→K→I, calculateFare, weekend cap ('turned out to be an OOP/LLD question') [high, independent]

## (reconstructed) — not in any visible report

- what the cap applies to (a single trip vs a day's total per rider), cap value, direction of travel, unknown stations; stage 4 (推断): several lines / transfers, per-segment prices, peak hours

## Reuse / link (our own repo first)

- `vault/interviews/companies/amazon/lld/pricing_billing.md` §4 step 9 and `vault/interviews/companies/amazon/lld/code/pricing_billing.py` `FareCalculator` (our own code — adapt it)
- concept leaves oop.values, patterns.strategy

## Card ladder notes

- ladder; step 4 = prefix sums over station positions (fare = |pos[a]-pos[b]|) and why insertion in the middle breaks naive prefix arrays
