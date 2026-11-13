---
id: test-pytest-timeout-rerunfailures
node: engineering.testing
type: qa
---
## Q
夜间回归里偶尔有一个测试卡死，整个任务要等到 CI 的 6 小时上限才被杀；另有几个测试偶发失败。`pytest-timeout` 和 `pytest-rerunfailures` 分别怎么用？自动重跑有什么代价？

## A
**`pytest-timeout` 给单个测试设时间上限，卡死的测试变成一条明确的失败；`pytest-rerunfailures` 让失败的测试自动重跑几次。前者几乎总该开，后者要谨慎。**

```bash
pytest --timeout=300                          # 每个测试最多 300 秒
pytest --reruns 2 --reruns-delay 5            # 失败后最多重跑 2 次，间隔 5 秒
pytest --reruns 2 --only-rerun ConnectionError  # 只对这种错误重跑
```

```python
@pytest.mark.timeout(60)
@pytest.mark.flaky(reruns=3)
def test_stream_reconnect(): ...
```

- **超时的两种方式：** `signal`（POSIX 默认）用 `SIGALRM` 在测试里抛异常，这个测试失败、后面的照常继续；`thread` 方式在超时时打印所有线程的栈，然后直接结束整个 pytest 进程。前者适合卡在 Python 代码里，后者适合卡在 C 扩展或系统调用里、信号打断不了的情况。
- **超时值怎么定：** 取这个测试正常耗时的几倍，而不是 CI 的总上限。上限太宽等于没设。
- **重跑在报告中的样子：** 被重跑的测试标为 `R`，结尾汇总写 `N rerun`。重跑后通过的测试算通过。
- **重跑的代价：** 它把「不稳定」变成「通过」，真实的竞态 bug 也会被藏起来，而且失败越来越频繁时没人察觉。可接受的用法：只对明确的基础设施错误重跑（`--only-rerun`），并把每次重跑记录下来统计不稳定率，超过阈值就隔离并修复。
- **不要全局一刀切：** 给整个套件加 `--reruns 3`，相当于把 flaky 测试的治理永久关掉了。
