---
id: test-pytest-junitxml-tmp-path-caplog
node: engineering.testing
type: qa
---
## Q
测试结果要让 CI 平台能展示，测试要写临时文件，还要断言某条警告日志确实被打出来了。分别用 pytest 的哪个功能？`--junitxml`、`tmp_path`、`caplog` 各给你什么？

## A
**`--junitxml` 把结果写成 CI 通用的 XML；`tmp_path` 给每个测试一个独立的临时目录；`caplog` 捕获测试期间产生的日志记录供断言。**

```python
def test_retry_logs_warning(caplog, tmp_path):
    caplog.set_level(logging.WARNING, logger="runner")
    cfg = tmp_path / "job.yaml"            # pathlib.Path，每个测试一个新目录
    cfg.write_text("retries: 2\n")
    run_job(cfg)
    assert "retrying job-7" in caplog.text
    assert any(r.levelno == logging.WARNING for r in caplog.records)
```

- **`--junitxml=report.xml`：** 每个测试一个 `<testcase>`，带耗时、失败信息和捕获的输出。几乎所有 CI 系统（Jenkins、GitLab、GitHub Actions 的报告插件）都能解析，用来显示失败列表和历史趋势。`record_property("build", "1.4.2")` 能给某个测试加自定义属性。
- **`tmp_path`：** 每个测试一个唯一的目录，测试之间不会读到彼此的文件。默认保留最近 3 次运行的目录，失败后能进去看现场。session 范围要共享一个目录时用 `tmp_path_factory.mktemp("models")`。不要写死 `/tmp/out.txt`：并行跑时多个测试会互相覆盖。
- **`caplog`：** `caplog.set_level(level, logger=...)` 调低捕获级别；`caplog.text` 是格式化后的全文，`caplog.records` 是 `LogRecord` 列表，`caplog.record_tuples` 是 `(logger 名, 级别, 消息)` 三元组，适合精确断言；`caplog.clear()` 清空。
- **相近的工具：** `capsys` 捕获 `print` 到 stdout/stderr 的内容；`monkeypatch` 临时改环境变量和属性，测试结束自动恢复。
- **为什么断言日志：** 有些行为只在日志里可见，比如「重试了一次」「降级到了 CPU」。不断言，这类行为坏掉了测试也不会失败。
