---
id: tr-regression-suite-design-metadata
node: regression.suite-design
type: qa
step: 3
---
## Q
"每条回归用例都要有负责人和明确的失败含义"，具体落实到代码里是什么样子？

## A
**每条测试带上元数据**，让结果流水线能把失败自动路由给对的人：

```python
@pytest.mark.release
@pytest.mark.owner("runtime-team")
@pytest.mark.component("batching")
def test_batch_preserves_request_order(server):
    reqs = [make_request(i) for i in range(32)]
    resps = server.send_batch(reqs)
    ids = [r.request_id for r in resps]
    assert ids == list(range(32)), (
        f"批量返回顺序错乱：期望 0..31，实际 {ids[:8]}…；"
        "检查 batching 调度器的重排逻辑")
```

- **负责人和组件**：用自定义标记（在 `pyproject.toml` 的 `markers` 里注册）或仓库的 `CODEOWNERS` 文件；结果上报时一并写入，失败工单自动分给对应团队。
- **失败信息**：断言消息说明"坏了什么、期望什么、实际什么、先查哪里"。`assert x == y` 本身也会显示两边的值，但只有作者知道这两个值代表什么。
- **一条测试只验证一种行为**：一个测试里混十个断言，失败时难以判断属于哪个问题，也无法单独隔离。
- **记录测试档和超时**：标记所在档；超时用 pytest-timeout 的 `@pytest.mark.timeout(300)`。

**为什么重要**：发布当天有 30 条失败时，分诊者需要在几分钟内知道每条是谁的、坏的是什么。没有负责人的失败最终无人处理，没有含义的失败只能靠重跑碰运气。
