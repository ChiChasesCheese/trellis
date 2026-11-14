# 03 · 多次 CI 结果 → 失败签名 → 回归、不稳定还是环境问题

限时 30 分钟，Python。

同一套测试每天在 CI 上跑很多次。一个测试挂了，分诊的人要先回答三个问题：是代码真的坏了（回归），还是这个测试时过时挂（不稳定），还是机器、网络、磁盘出了问题（环境）？这组练习让你写一个分诊工具：读几次 CI 运行产出的 JUnit XML，把每条失败信息规范化成"失败签名"，再按每个测试在各次运行里的过挂序列给它归类，最后打印一张表。没有 AI 概念，考的是解析、正则和把规则写清楚。

## 输入

`runs/run_01.xml` 到 `run_06.xml`，由 `make_runs.py` 生成，是 6 次运行的结果，文件名顺序就是时间顺序。JUnit XML 是 pytest（`--junitxml`）、Maven 和多数 CI 工具都会写的格式：

```xml
<testsuites>
  <testsuite name="pytest" tests="10" failures="5" errors="0" skipped="1">
    <testcase classname="tests.test_math" name="test_add" time="0.330"/>
    <testcase classname="tests.test_cache" name="test_eviction" time="0.380">
      <failure message="KeyError: 'k15' not found in LRU at 0x7f9aaba5c0" type="KeyError">Traceback ...</failure>
    </testcase>
    <testcase classname="tests.test_gpu" name="test_cuda" time="0.340">
      <skipped message="no GPU on this runner"></skipped>
    </testcase>
  </testsuite>
</testsuites>
```

- 根元素可能是 `<testsuites>`，也可能直接是一个 `<testsuite>`。
- `<failure>`（断言失败）和 `<error>`（测试本身出错，比如环境连不上）都算失败；`<skipped>` 算跳过；没有子元素算通过。
- 失败信息取 `message` 属性；没有就取元素正文第一个非空行。
- 测试的标识是 `classname::name`，没有 `classname` 就只用 `name`。

## 任务

### Part 1：解析（约 7 分钟）

`parse_junit(path, run=None) -> [Outcome]`：每个 `<testcase>` 一个 `Outcome(test, run, status, message)`，`status` 是 `pass` / `fail` / `skip`，`run` 默认取文件名（不含扩展名）。XML 坏了或根元素不是 JUnit：`ValueError`。

### Part 2：失败签名（约 8 分钟）

`signature(message, max_len=200) -> str`：把每次运行都会变的部分换成占位符，让同一个 bug 在每次运行里得到同样的文本。按顺序替换（顺序重要：先换形状特殊的，否则数字规则会把它们拆碎）：

| 顺序 | 换掉什么 | 换成 |
|---|---|---|
| 1 | UUID：按 8-4-4-4-12 位分段的十六进制串 | `<UUID>` |
| 2 | 时间戳，如 `2026-11-14T03:00:00Z`、`2026-11-14 22:10:59.123` | `<TS>` |
| 3 | 十六进制地址，如 `0x7f9aaba5c0` | `<ADDR>` |
| 4 | IP 和端口，如 `10.0.3.13:8443` | `<IP>` |
| 5 | 临时路径：以 `/tmp/`、`/private/var/`、`/var/folders/`、`/var/tmp/` 开头直到空白或引号 | `<TMP>` |
| 6 | 其余数字（含小数） | `<N>` |
| 7 | 连续空白 | 一个空格 |

最后去掉首尾空白，截到 `max_len`。`is_infra(sig, patterns=INFRA_PATTERNS)`：签名匹配任一环境模式（不分大小写）即为环境问题，默认模式有 connection refused、connection reset by peer、no space left on device、timed out waiting for device、OOMKilled / out of memory、could not resolve host、resource temporarily unavailable。

### Part 3：归类（约 10 分钟）

`classify(history) -> TestReport`，`history` 是一个测试按运行顺序的结果（没出现的运行就没有记录）：

1. 去掉跳过的运行。一次都没跑：`skipped`。没有失败：`pass`。
2. 所有失败都是环境问题：`infra`。
3. 否则先把环境失败的那几次运行去掉（它们说明不了代码），剩下的过挂序列写成 `P`/`F` 串：
   - 形如 `P…PF…F` 或全是 `F`：`regression`，`since` = 最后这段连续失败的第一次运行。
   - 形如 `F…FP…P`：`fixed`，`since` = 第一次通过的运行。
   - 其他（过挂交替不止一次）：`flaky`。
4. `fails` = 失败次数（环境失败也算），`runs` = 实际跑了的次数，`signatures` = 各签名出现次数（`Counter`），`top_signature` = 最常见的那个。

`analyze(paths)`：按给定顺序读所有文件，每个测试一份报告。

### Part 4：表格（约 5 分钟）

`table(reports)` 和 `main(argv)`：`main` 先把文件名排序（文件名即时间顺序），按 regression、flaky、infra、fixed、skipped、pass 的顺序打印，同类按测试名排序。每行：测试、类别、since、失败次数/运行次数、最常见的签名。

## 例子

参考解在 6 次运行上的输出：

```text
test                                    verdict     since    fails  signature
tests.test_api::test_login              regression  run_04   3/6    AssertionError: expected <N>, got <N> (request <UUID>)
tests.test_cache::test_eviction         regression  run_01   6/6    KeyError: 'k<N>' not found in LRU at <ADDR>
tests.test_mixed::test_infra_then_real  regression  run_05   3/6    ValueError: shape mismatch (<N>, <N>) vs (<N>,)
tests.test_tmp::test_paths              regression  run_05   2/6    FileNotFoundError: [Errno <N>] No such file or directory: '<TMP>'
tests.test_io::test_upload              flaky       -        2/6    TimeoutError: upload took <N>s > <N>s
tests.test_device::test_compile         infra       -        1/6    ConnectionRefusedError: [Errno <N>] Connection refused: <IP>
tests.test_model::test_logits           fixed       run_03   2/6    AssertionError: max abs diff <N> > <N>e-<N> at index <N>
tests.test_gpu::test_cuda               skipped     -        0/0
tests.test_math::test_add               pass        -        0/6
tests.test_new::test_feature            pass        -        0/3
```

`test_infra_then_real` 在第 2 次运行因为磁盘满失败，第 5、6 次因为真的 bug 失败：去掉第 2 次后序列是 `PPPFF`，所以是从 run_05 开始的回归，而不是不稳定。

## 边界情况

- 空的 `<testsuite>`；`<failure/>` 没有 `message` 也没有正文（签名是空串）。
- 测试只在后几次运行里出现（新加的测试）：没出现的运行不算运行。
- 中间夹着跳过：`SPSFSF` 去掉跳过后是 `PFF`，是从 run_04 开始的回归。
- 同一个测试先因环境失败、后因真 bug 失败。
- XML 写了一半；根元素是 `<html>`。

## 面试官会追问

| 追问 | 答题要点 |
|---|---|
| 文件有 10 GB 怎么办？ | 用 `ET.iterparse(path, events=("end",))`，每处理完一个 `testcase` 就 `elem.clear()`，内存只和单个用例有关；结果按测试聚合成计数，不保存全部原文 |
| 签名太粗会怎样，太细会怎样？ | 太粗：不同 bug 合成一类，第二个 bug 被第一个的工单掩盖（例如数字全换成 `<N>` 后，`expected 200, got 500` 和 `expected 200, got 404` 成了同一个签名，可一个是服务端崩了、一个是路由丢了）。太细：同一个 bug 每次一个签名，看起来像很多新问题。办法：保留状态码、errno 这类有含义的数字，再加上栈顶几帧的函数名 |
| 为什么不直接用失败次数 / 运行次数判断不稳定？ | 比例分不清"一直挂了 3 次"（回归）和"挂 3 次过 3 次交替"（不稳定），它们的处理完全不同：回归要找引入它的提交，不稳定要隔离并修测试 |
| 回归是哪次提交引入的？ | `since` 那次运行和前一次运行之间的提交范围；范围大时用 `git bisect` 在这段里二分 |
| 环境模式表误判怎么办？ | 只匹配签名而不是整个栈；每条模式要有负例测试；环境类失败在下一次运行自动重跑确认，重跑仍失败就升级为真失败 |
| 结果怎么进系统？ | 签名作为键存库，记录首次出现时间、出现次数、关联工单；新签名触发通知，老签名只累计，这就是错误追踪系统的指纹去重 |
| 运行顺序为什么不用 XML 里的 timestamp？ | 可以用，而且更可靠；但不同 CI 写的格式不一，这里按文件名排序，追问时说出可以改用 timestamp |

## 评分看什么

- 先问清楚 `error` 算不算失败、跳过怎么处理、运行顺序怎么定，再写代码。
- 正则替换有顺序意识，并能举出一个"顺序错了会怎样"的例子（先换数字，UUID 和 IP 会被拆碎）。
- 归类规则写成能逐条测试的小函数，而不是一大段 if。
- 自己举出 `PIPPFF` 这类混合用例并说出结果。
- 能说出流式解析和签名粒度的取舍。

## 怎么跑

```bash
cd vault/interviews/companies/cerebras
uv run --project ../../../.. pytest practice/03_failure_signatures -q
IMPL=starter uv run --project ../../../.. pytest practice/03_failure_signatures -q
cd practice/03_failure_signatures && uv run --project ../../../../../.. python solution.py runs/*.xml
```
