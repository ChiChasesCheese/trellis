%% trellis:begin %%
# 值对象与不可变性（Value Objects）
*对象建模（Object Modeling）*

实体与值对象的区分、相等语义、不可变为什么让推理变简单。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/python.dataclasses-enums|dataclass 与 Enum]]

**Unlocks:** [[domains/low-level-design/map/amazon.amz-train-fare|火车线路票价（Train Fare Calculator）]], [[domains/low-level-design/map/amazon.amz-discount-engine|购物车折扣引擎（Checkout Price Engine）]], [[domains/low-level-design/map/amazon.amz-aws-billing|AWS 账单服务（AWS Billing Service）（low priority）]]

## Readings
- [[fowler-value-object|ValueObject (Martin Fowler, bliki)]]
- [[solution-amz-aws-billing|设计题解：AWS 账单服务（AWS Billing Service）（low priority）]]

## Drills
- [[design-amz-aws-billing|Drill：AWS 账单服务（AWS Billing Service）]]
- [[design-amz-discount-engine|Drill：购物车折扣引擎（Checkout Price Engine）]]
- [[design-amz-pizza-order|Drill：披萨订单（Pizza Order）]]
- [[design-amz-train-fare|Drill：火车线路票价（Train Fare Calculator）]]
- [[design-splitwise|Drill：分账（Splitwise）]]

## Cards (5)
1. [[oop-entity-vs-value-object]]
2. [[oop-immutability-payoff]]
3. [[oop-equals-hashcode-contract]]
4. [[oop-primitive-obsession-fix]]
5. [[oop-enum-with-behavior]]
%% trellis:end %%

## Notes
