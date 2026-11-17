---
id: ai-verification-mutation
node: ai.verification
type: qa
step: 3
---
## Q
测试都绿了，怎么知道这些测试真的拦得住错？让智能体故意改坏一次是在检查什么？

## A
**改坏一处，测试该变红；不红就是漏洞**

- **做法**：把修好的地方改回旧写法，或把 `<` 换成 `<=`、把“窗口空了就放行”删掉，各改一次，跑测试；
- **判读**：变红说明这条规则有测试守着；仍然绿，说明测试对这处不敏感，补一个能区分的用例；
- **谁来改坏**：可以让智能体动手，但要不要补、补什么由你判断；
- **代价**：每个改坏版本跑一遍测试，规则有几条就几个版本，便宜；这就是变异测试（mutation testing）的手工版。

```python
MUTANTS = {
    "orig":   lambda used, cap, size: used + size <= cap,
    "lt":     lambda used, cap, size: used + size < cap,
    "plus1":  lambda used, cap, size: used + size <= cap + 1,
    "always": lambda used, cap, size: True,
}
def survivors(suite):
    ok = lambda f: all(f(*args) == want for args, want in suite)
    return [n for n, f in MUTANTS.items() if n != "orig" and ok(f)]

weak = [((0, 10, 5), True), ((5, 10, 6), False)]
print(survivors(weak))                        # ['lt']：区分不了 < 和 <=
print(survivors(weak + [((5, 10, 5), True)])) # []：加上恰好等于预算
```

**知识点：**验证输出（Verification）
