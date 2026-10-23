---
id: hl-j17-preview-flags
node: java21.j17-ffm-api
type: qa
step: 4
---
## Q
FFM API 在 Java 21 是什么状态？编译、运行、调 C 函数各需要什么命令行参数？

## A
Java 21 里是**第三次预览**，**JDK 22 转正**。

- 编译：`javac --release 21 --enable-preview`
- 运行：`java --enable-preview`
- 调 C 函数再加：`--enable-native-access=ALL-UNNAMED`，否则打印受限方法警告。

用了 FFM 的类被标记为依赖预览，必须 `--enable-preview` 运行。编译器除此之外无新语法。
