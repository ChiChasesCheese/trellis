---
id: cc-output-ordering-rank-unrounded
node: output.ordering
type: qa
---
## Q
Two candidates are 3999.6 and 4000.4 units away. Both print as `4000` after rounding. Do you now apply the alphabetical tie-break?

## A
**No — rank on the exact value and round only for display.** They are not tied; rounding is a formatting step and must never feed a comparison.

- Compute the ordering key from the unrounded quantity, or better from an exact scaled integer (cents, milli-units, squared distance) so no float ever decides an order.
- Apply the declared tie-break only when the *exact* keys are equal.
- Same rule for money: sort on integer minor units and print `x.xx` ([[cc-output-formatting-minor-units]]).
- The mirror mistake is ranking on a value you then recompute differently for display — one formatter, called once, at the print site ([[cc-output-formatting-one-place]]).

## Q zh
两个候选的距离是 3999.6 和 4000.4。四舍五入后都打印成 `4000`。这时该用字母序 tie-break 吗？

## A zh
**不该 —— 用精确值排名，只在显示时取整。** 它们并不并列；取整是格式化步骤，绝不能参与比较。

- 排序 key 用未取整的量计算，更好的是用精确的放大整数（分、毫单位、距离平方），这样就没有任何浮点参与决定顺序。
- 只有当*精确* key 相等时，才应用声明的 tie-break。
- money 同理：按整数最小单位排序，按 `x.xx` 打印（[[cc-output-formatting-minor-units]]）。
- 镜像错误是：排名用一个值，显示时又用另一种方式重算 —— 只保留一个格式化函数，在打印处调用一次（[[cc-output-formatting-one-place]]）。
