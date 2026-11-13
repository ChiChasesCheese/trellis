---
id: tr-test-infra-results-junit-xml
node: test-infra.results
type: qa
step: 1
---
## Q
JUnit XML 是什么样的格式？`failure` 和 `error` 有什么区别？用 pytest 怎么产出、怎么附加额外信息？

## A
JUnit XML 是测试结果的事实标准格式，几乎所有 CI 系统（Jenkins 的 `junit` 步骤、GitHub Actions 的报告插件、GitLab）都能读。不同语言的测试框架都输出它，结果流水线只需要解析一种格式。

```xml
<testsuites>
  <testsuite name="pytest" tests="3" failures="1" errors="1" skipped="0" time="12.4">
    <testcase classname="tests.test_api" name="test_ok" time="0.8"/>
    <testcase classname="tests.test_api" name="test_len[512]" time="3.1">
      <failure message="assert 511 == 512">...回溯...</failure>
    </testcase>
    <testcase classname="tests.test_api" name="test_stream" time="8.5">
      <error message="failed on setup: ConnectionRefusedError">...</error>
    </testcase>
  </testsuite>
</testsuites>
```

- **`failure`**：断言失败，被测系统的结果和期望不同。默认先怀疑产品。
- **`error`**：测试没能正常完成判定，通常在准备或清理阶段抛了异常（服务没起来、设备申请失败）。默认先怀疑环境或测试本身。分诊时这个区分很有用。
- **`skipped`**：被跳过，带原因。

**pytest 用法**：
- `pytest --junitxml=report.xml`；`junit_family` 配置项选格式，从 pytest 6.1 起默认 `xunit2`。
- `record_testsuite_property("build_id", "1234")`（session 级 fixture）在整个 suite 上加属性，适合写入构建号、机器、固件版本；它和 `xunit2` 兼容。
- `record_property("seed", 42)` 给单条测试加属性，但会让文件不再符合最新的 JUnit XML 模式校验。
- `junit_duration_report = call` 只报告测试本体耗时，默认包含准备和清理。

**局限**：格式只有通过、失败、错误、跳过，没有"重试后通过"、性能数字和附件。这些要靠属性字段或另外上报到结果库。
