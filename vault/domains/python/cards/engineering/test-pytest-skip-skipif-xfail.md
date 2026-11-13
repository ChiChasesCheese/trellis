---
id: test-pytest-skip-skipif-xfail
node: engineering.testing
type: qa
---
## Q
pytest 里 `skip`、`skipif`、`xfail` 各表示什么？一个已知 bug 还没修，测试该标成 skip 还是 xfail？`xfail(strict=True)` 解决什么问题？

## A
**skip 表示「这里不该跑」，xfail 表示「跑，但预期失败」。已知 bug 用 xfail，因为它仍然在跑，bug 一修好你就会知道。**

```python
@pytest.mark.skipif(sys.platform == "win32", reason="需要 POSIX 信号")
def test_sigterm_graceful(): ...

@pytest.mark.xfail(reason="BUG-123 长输入截断", raises=IndexError, strict=True)
def test_long_input(): ...

np = pytest.importorskip("numpy")    # 没装 numpy 就跳过整个模块
```

- **`skip` / `skipif`：** 条件不满足时根本不执行，比如平台不对、缺依赖、缺硬件。报告中记为 `s`。`reason` 必填式地写清楚，否则一年后没人知道为什么跳过。
- **`xfail`：** 照常执行。失败记为 `x`（预期内），意外通过记为 `X`（XPASS）。`raises=IndexError` 让它只接受这一种失败，别的异常照样算真失败，防止一个新 bug 藏在旧 bug 的 xfail 后面。`run=False` 用于跑了会崩溃或卡死的情况。
- **strict 解决什么：** 默认 XPASS 不会让构建失败，bug 修好了也没人去摘标记，这个测试就永远失去作用。`strict=True`（或在 `pytest.ini` 里设 `xfail_strict = true`）让 XPASS 直接变成失败，逼人把标记删掉。
- **为什么已知 bug 不用 skip：** skip 的测试不运行，bug 修好或变得更糟你都看不到；xfail 持续运行，状态一变就报告。
- **看汇总：** `pytest -rsxX` 在结尾列出所有跳过、预期失败和意外通过的测试及原因，适合定期清理。
