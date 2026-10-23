---
id: hl-javaq-e-q21-implications
node: java-questions.e-jit-gc
type: qa
step: 14
---
## Q
去优化对低延迟系统意味着什么？怎么发现它？`not entrant` 和 `zombie` 有什么区别？
Can deopt be a source of tail latency in production? How would you find it?

## A
- **预热要覆盖真实的类型和分支多样性**：只用 `BUY` 订单预热，上线第一个 `SELL` 会触发去优化，造成一次可见的延迟尖刺。
- 分支投机（`unstable_if`）同理：预热里"从不执行"的错误处理路径，生产中第一次执行也会去优化。
- **发现**：`-XX:+PrintCompilation` 里的 `made not entrant`；JFR 的 `Deoptimization` 事件；对比预热流量与生产流量的分布。
- **not entrant vs zombie**：not entrant 是不再被新调用进入；zombie 是更老版本里待清除的状态，现在由代码缓存清扫处理。只记大意，不要深入。
