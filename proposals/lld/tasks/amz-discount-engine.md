# Task: amazon.amz-discount-engine

- **Leaf id**: `amazon.amz-discount-engine`   **slug**: `amz-discount-engine`   **kind**: problem
- **题目**: 购物车折扣引擎（Checkout Price Engine）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- 1p3a 1191754 (2026-10-02, Amazon VO 一轮 OOD; partly hidden): visible 「讲清 compute total 的主流程。」「OOD：抽象一个 Discount 基类，isEligible 判断商品是否适用该折扣，apply 返回折扣金额。三种折扣各自实现。PriceEngine 拿到 cart 后遍历 line items，对每个 item 依次检查所有 discount，accumulate 总折扣后从原价扣除。BUY_X_GET_Y 特殊在它不直接减钱，而是把赠品数量乘以单价算出减免。」 https://www.1point3acres.com/bbs/thread-1191754-1-1.html [high]
- 1p3a question bank row `checkout-price-engine-ood` (onsite-coding, 2026-10-02, 1 source) [medium]; row `pizza-restaurant-ood` (onsite, 5 sources, 2026-04-08..09-24) [medium]
- 1p3a 1190571 (2026-09-23, AI infra, offer): 「店面ood: 模拟购物车」 https://www.1point3acres.com/bbs/thread-1190571-1-1.html [high, short]
- kit forums: RD1wcfb9m (EU 2026-09) 'shopping cart price calculator API … apply discounts' + follow-ups (all-products discount, double above EUR100, buy-3-get-1, hot product); LC8568929 (2026-10) cart management 'with proper design patterns, discount rules, full class code on a notepad'

## (reconstructed) — not in any visible report

- the third discount type (visible text names BUY_X_GET_Y and 'three discounts'; pick percentage and threshold/fixed as the other two and label them), stacking order, exclusivity

## Reuse / link (our own repo first)

- `vault/interviews/companies/amazon/lld/pricing_billing.md` + `vault/interviews/companies/amazon/lld/code/pricing_billing.py` (Money, PriceRule, PricingEngine, Receipt — adapt)
- bank [[solution-online-shopping]]
- concept leaves patterns.strategy, oop.values

## Card ladder notes

- ladder; step 5 = per-item discounts vs cart-level rules (where BUY_X_GET_Y must live); a mistake card on float money with a concrete 0.1+0.2 style input
