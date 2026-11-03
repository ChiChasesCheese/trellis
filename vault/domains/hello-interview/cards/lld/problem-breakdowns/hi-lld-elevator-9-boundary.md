---
id: hi-lld-elevator-9-boundary
node: lld.problem-breakdowns.elevator.exam
type: qa
step: 9
---
## Q
**行驶与停靠的区别，边界不要硬编码**｜低层设计 · 题目拆解

为什么 `hasRequestsAhead` 不区分请求类型，却在停靠时要看类型？到 0 层或 9 层要不要单独写判断？

## A
**要点。** 停靠有方向性：上行只停 PICKUP_UP 和 DESTINATION，不停 PICKUP_DOWN。行驶没有方向性：只要前方任何类型的请求存在，都要朝它走。

例：电梯在 4 层上行，6 层有人按下，8 层有目的地。电梯路过 6 层不停，到 8 层停下、换向，回到 6 层才停，这是对的，不是漏停。

**为什么。** 边界不用特判：9 层上行时 `hasRequestsAhead(UP)` 为假，自然换向；0 层下行同理。

**易错。** 写 `if floor == 9: direction = DOWN` 会出错：这时 9 层本身可能还有要停的请求，被强行换向就漏掉了。让运动逻辑自己决定换向。

**对应校验。** `addRequest` 里只检查 0 到 9 越界返回 false、当前层返回 true（空操作），其余加入集合，由 Set 按楼层加类型自动去重。
