---
id: kafka-admin-offset-export-import-dry-run
node: admin.consumer-group-ops
type: qa
step: 5
source: kafka-2e
---
## Q
用 `kafka-consumer-groups.sh --reset-offsets` 修改消费者群组偏移量前，为什么建议先加 `--dry-run` 参数导出一份 CSV 再修改导入，而不是直接执行重置命令？

## A
`--reset-offsets` 命令一旦不加 `--dry-run`，偏移量会被立即真实修改，这个操作没有撤销功能；先用 `--dry-run` 把当前每个主题分区对应的偏移量导出成 `<topic>,<partition>,<offset>` 格式的 CSV 文件，相当于对当前状态做了一份备份和可视化确认。修改前先备份一份原始文件，再在副本上改出想要的目标偏移量，用 `--from-file` 加 `--execute` 导入执行，这样如果改错了还能用最初导出的备份文件把偏移量改回去，比直接执行一次不可逆的重置要安全得多。
