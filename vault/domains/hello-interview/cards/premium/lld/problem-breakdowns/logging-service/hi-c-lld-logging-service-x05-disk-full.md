---
id: hi-c-lld-logging-service-x05-disk-full
node: lld.problem-breakdowns.logging-service.exam
type: qa
step: 4
---
## Q
**日志库 · 磁盘写满时的行为**｜考点 · 必会

配置了控制台、文件、远程三个目的地，磁盘写满，`FileSink.write` 每次抛 `IOException`。分别预测"异常直接冒泡"和"吞掉并写 stderr"两种实现下，控制台、远程和业务代码各会怎样。

## A
- **冒泡：** 遍历顺序为控制台、文件、远程时，控制台写成功，文件处抛异常，远程永远收不到；异常继续冲进业务代码，比如 `logger.error("payment failed")` 所在的支付函数抛错，把磁盘问题伪装成支付 bug，排查者先去查支付。
- **吞掉并写诊断：** 控制台和远程都正常，文件目的地丢了这批记录，但 stderr 有一行"sink write failed: disk full"，运维能看到；`Logger.log` 正常返回，业务无感。
- **只吞不报：** 业务和其他目的地都正常，但文件默默空了几天。
- **继续追问会问：** 诊断刷屏怎么办（限量、只报首次、退避）；"总不能信任 stderr"（总要信任某个通道，或另有健康指标）。
- **看顺序：** 冒泡版本下，远程是否漏记还取决于它排在文件前还是后，这个不确定性本身就是它的缺陷。
