%% trellis:begin %%
# 购物车折扣引擎（Checkout Price Engine）
*Amazon 专项（Amazon OOD）*

折扣基类 isEligible / apply，百分比、满减、买 X 送 Y 叠加；钱用整数分；规则可插拔。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.strategy|策略模式与可替换算法（Strategy）]], [[domains/low-level-design/map/oop.values|值对象与不可变性（Value Objects）]]

**Unlocks:** [[domains/low-level-design/map/amazon.amz-pizza-order|披萨订单（Pizza Order）]]

## Readings
- [[solution-amz-discount-engine|设计题解：购物车折扣引擎（Checkout Price Engine）]]
- [[src-pythondocs-decimal-amz-discount-engine|decimal — Decimal fixed point and floating point arithmetic]]

## Drills
- [[design-amz-discount-engine|Drill：购物车折扣引擎（Checkout Price Engine）]]

## Cards (9)
1. [[amz-discount-engine-how-it-is-asked]]
2. [[amz-discount-engine-objects-and-jobs]]
3. [[amz-discount-engine-stage-one-flow]]
4. [[amz-discount-engine-integer-cents-single-rounding]]
5. [[amz-discount-engine-line-level-vs-cart-level]]
6. [[amz-discount-engine-buy-x-get-y]]
7. [[amz-discount-engine-stacking-and-clamp]]
8. [[amz-discount-engine-thread-safety]]
9. [[amz-discount-engine-float-money-mistake]]
%% trellis:end %%

## Notes
