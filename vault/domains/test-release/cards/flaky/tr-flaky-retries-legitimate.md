---
id: tr-flaky-retries-legitimate
node: flaky.retries
type: qa
step: 2
---
## Q
什么情况下自动重试是合理的？在 pytest 里怎么把重试限制在这些情况？

## A
**合理的重试只针对"与被测代码无关、已知的基础设施瞬时故障"**：
- 测试机器在运行中被回收或断连；
- 从制品库或镜像仓库下载依赖时网络超时；
- 共享测试设备在开始前健康检查失败，需要换一台；
- 外部服务限流（这种情况更好的做法是不依赖外部服务）。

**不合理的重试**：断言失败（`AssertionError`）、超时、崩溃。这些都可能是产品问题。

**在 pytest 里限定重试范围**：pytest-rerunfailures 支持按异常类型过滤：

```bash
pytest --reruns 2 --reruns-delay 5 \
       --only-rerun ConnectionResetError \
       --only-rerun "InfraUnavailable"
```

`--only-rerun` 接收正则表达式，可以写多次，只有匹配的失败才重跑；`--rerun-except AssertionError` 则反过来，除了断言失败都重跑。也可以在单条测试上写 `@pytest.mark.flaky(reruns=2, only_rerun=["ConnectionResetError"])`。

**更好的位置是基础设施层**：在测试调度器那一层识别"机器丢失""设备不可用"，换一台机器重新调度，而不是在测试框架里重跑。这样测试代码里的失败永远是真失败。

**无论哪种，重试都要被记录**：输出里 pytest-rerunfailures 会把重跑过的测试列为 `RERUN`（用 `-r aR` 显示汇总），结果系统应把"重试后通过"计入不稳定率。
