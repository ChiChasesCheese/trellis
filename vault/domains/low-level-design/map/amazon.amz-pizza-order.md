%% trellis:begin %%
# 披萨订单（Pizza Order）
*Amazon 专项（Amazon OOD）*

饼底、尺寸、配料自由组合并算总价：菜单是数据不是类，Builder 校验组合，复用折扣规则。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.creational|创建型模式（Creational）]], [[domains/low-level-design/map/amazon.amz-discount-engine|购物车折扣引擎（Checkout Price Engine）]]

## Readings
- [[solution-amz-pizza-order|设计题解：披萨订单（Pizza Order）]]

## Drills
- [[design-amz-pizza-order|Drill：披萨订单（Pizza Order）]]

## Cards (9)
1. [[amz-pizza-order-how-it-is-asked]]
2. [[amz-pizza-order-objects-and-jobs]]
3. [[amz-pizza-order-stage1-build-and-validate]]
4. [[amz-pizza-order-menu-as-data-price-by-size]]
5. [[amz-pizza-order-decorator-vs-menu-data]]
6. [[amz-pizza-order-followup-discount-layers]]
7. [[amz-pizza-order-cheapest-free-uses-discounted-price]]
8. [[amz-pizza-order-concurrency-order-lock]]
9. [[amz-pizza-order-unsorted-toppings-mistake]]
%% trellis:end %%

## Notes
