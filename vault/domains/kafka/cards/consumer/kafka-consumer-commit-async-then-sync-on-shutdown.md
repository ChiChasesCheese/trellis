---
id: kafka-consumer-commit-async-then-sync-on-shutdown
node: consumer.offset-commit
type: qa
step: 5
source: kafka-2e
---
## Q
为什么消费者关闭之前，通常建议在循环体内一直用 `commitAsync()` 提交，但在真正退出循环、关闭消费者之前额外调用一次 `commitSync()`？

## A
循环体内偶尔一次 `commitAsync()` 提交失败通常不是大问题，因为很快就会有下一次提交把偏移量追上来；但如果这是消费者关闭前的最后一次提交，就没有「下一次」去补救了，一旦这次失败，进度就真丢了。所以在退出循环前额外调用一次 `commitSync()`，利用它会持续重试直到成功或遇到不可恢复错误的特性，确保关闭前的最终进度真正被保存下来。
