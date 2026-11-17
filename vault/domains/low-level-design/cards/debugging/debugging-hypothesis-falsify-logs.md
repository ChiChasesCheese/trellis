---
id: debugging-hypothesis-falsify-logs
node: debugging.hypothesis
type: qa
step: 2
---
## Q
假设是“所有重复扣款都由客户端超时重试引起”。日志在手，怎么用它去推翻这个假设，而不是只挑支持它的例子？推翻之后怎么办？

## A
**找反例：假设说“所有”，一个不符合的例子就够了**

- **把假设翻成可检查的谓词**：“同一个请求号扣了两次以上”的每一组，事件里都有一条 `timeout`；
- **全量检查，不挑样本**：日志已经在手，写几行代码对全部请求号跑一遍，比人眼翻十几条可靠；
- **一条反例就推翻整个说法**：另一类重复扣款不经过超时，说明至少有第二个原因；
- **反例是线索**：看它的共同点（同一个接口？同一个客户端版本？两次相隔多久？），从中长出下一个假设；
- **别急着修“已经解释了的那一类”**：先确认它们真的是同一个根因，修完再用同样的检查验证它们消失。

```python
logs = [("a1", "charge"), ("a1", "timeout"), ("a1", "charge"),     # 超时后重试
        ("b2", "charge"), ("b2", "charge"),                         # 没有超时也重复
        ("c3", "charge")]

events: dict[str, list[str]] = {}
for req, ev in logs:
    events.setdefault(req, []).append(ev)

dups = {r: e for r, e in events.items() if e.count("charge") >= 2}
print({r: "timeout" in e for r, e in dups.items()})   # {'a1': True, 'b2': False}
# b2 是反例：假设被推翻，下一步研究 b2 为什么没有超时也重复
```

**知识点：**假设驱动（Hypothesis-Driven）
