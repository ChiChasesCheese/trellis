---
id: hl-j18-fail-fast
node: java21.j18-comparators-interfaces
type: qa
step: 12
---
## Q
为什么要在构造器和公共方法开头就做 `Objects.requireNonNull` 检查（fail fast）？抛 NPE 还是 IAE？

## A
错误越早抛离原因越近。`null` 被放进对象后，几十步后才在别处 NPE，要倒着追半天。所以在 `Order`、`Limit`、`Market` 的紧凑构造器里写 `Objects.requireNonNull(side, "side")`，公共入口写 `Objects.requireNonNull(cmd, "cmd")`，null 不能进入对象。

`requireNonNull` 抛 NPE 是**约定，不是 bug**：《Effective Java》建议对「传了 null 参数」抛 `NullPointerException`，而不是 `IllegalArgumentException`。消息带上上下文便于定位，如 `"null element in stream " + h.stream`。
