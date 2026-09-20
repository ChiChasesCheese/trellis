---
id: quality-fitness-function-allowlist
node: quality.fitness-functions
type: qa
step: 3
---
## Q
代码库里还有 40 处直接用 `print()` 而不是走统一的日志模块，一次性全改完不现实。怎么用适应度函数防止这个数字继续变大，又不需要马上修完存量？

## A
```python
ALLOWED = {"scripts/debug_tool.py", "scripts/one_off_report.py"}  # 只许在这里删条目，不许新增

def test_print_usage_does_not_grow():
    offenders = {
        str(p) for p in Path("src").rglob("*.py")
        if "print(" in p.read_text() and str(p) not in KNOWN_LEGACY
    }
    assert not offenders, f"new print() usage outside allow-list: {offenders}"
```
把当前的 40 处存量固化成一份"只许缩小的白名单"（`KNOWN_LEGACY`），测试只对**白名单之外**的新增用法报错——这样今天就能挡住问题继续变多,而不用一次性还清历史债务。白名单本身应该被当作一份可见的技术债清单,每次有人顺手清理掉一处旧用法,就从白名单里删掉对应条目,而不是往里加。

关键纪律：代码评审必须把"有人往白名单里新增条目"当作一个需要额外说明理由的信号,否则这份白名单会被悄悄用来豁免新代码,失去它本该起到的棘轮（ratchet）作用。
