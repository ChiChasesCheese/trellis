---
id: pl-eco-packages-pitfall-silent-resolution
node: ecosystem.package-managers
type: qa
step: 11
---
## Q
依赖解析在生产中最危险的失败是什么？Python 解析器悄悄回溯到旧版本、Maven 悄悄忽略较新版本，分别是怎样的真实表现？

## A
最危险的不是报错，而是**解析成功但结果不是你想要的**。

**Python：回溯到远古版本**。

```
uv add "urllib3==1.20" "requests>=2.0"
 + requests==2.15.1
 + urllib3==1.20
```

你写的是 `requests>=2.0`，期望拿到当前的 2.3x，结果得到 2.15.1。因为你固定的 `urllib3==1.20` 与新版 `requests` 冲突，解析器为满足全部约束，一路回溯到一个很旧的版本，而且这是**成功**的结果，没有任何警告，旧版本里可能有已修复的漏洞。当约束再收紧，则会得到明确的错误：`your project's requirements are unsatisfiable`。

**Maven：较新的版本被忽略**。依赖树里出现 `(x:d:jar:2.0:compile - omitted for conflict with 1.0)`：`c` 需要 `d:2.0`，但先声明的 `b` 带来 `d:1.0`，Maven 选了 1.0。构建成功，单元测试可能全过；`c` 调用了 2.0 才有的方法，在运行时才出 `NoSuchMethodError`，甚至只在少见的代码路径上出现。

**共同模式**：解析器为了“成功”做了你没有明确同意的取舍，构建完成后没有人审视结果。

**防线**：
1. **审查锁文件的 diff**：每次依赖变更，PR 里看实际装了什么，而不只是看你写的约束。
2. **把关键包钉到范围下限**：写 `requests>=2.32`，让回溯不可能越过这个下限（下限冲突时变成显式的错误）。
3. **Maven 开 enforcer 的 `dependencyConvergence`**，冲突时让构建失败，而不是悄悄选一个。
4. **CI 里跑 `pip-audit` / `govulncheck` / OWASP dependency-check**，扫描实际装进去的版本。
5. **测试覆盖真实使用的依赖版本**，而不是开发机上随手装的版本。
