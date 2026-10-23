---
id: hl-j13-preview-status
node: java21.j13-unnamed-variables
type: qa
step: 3
---
## Q
未命名变量与模式 `_` 在 Java 21 是什么状态？哪个版本转正？不带标志编译会怎样？

## A
Java 21 里是**预览（Preview）特性**：`javac --release 21 --enable-preview`，运行 `java --enable-preview`。**JDK 22 转正，没有改动地定稿**，之后不再需要 `--enable-preview`，升级后去掉编译/运行参数即可。

JDK 21 上不带 `--enable-preview` 直接编译失败：

```
error: unnamed variables are a preview feature and are disabled by default.
  (use --enable-preview to enable unnamed variables)
```
用了 `_` 的类被打上预览依赖标记，必须 `--enable-preview` 运行。代价：团队/CI 工具链（旧版 IDE、Checkstyle、SpotBugs、ErrorProne）可能还不认识 `_`，先确认。
