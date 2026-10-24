---
id: pl-eco-packages-intro-java
node: ecosystem.package-managers
type: qa
step: 4
---
## Q
Java 的 Maven（以及 Gradle）怎样管理依赖？坐标、传递依赖和「最近优先」（nearest wins）规则各是什么，一个例子里发生了什么？

## A
**Maven**：Java 最主流的构建与依赖管理工具。项目根有 `pom.xml`，依赖用三元组**坐标**标识：`groupId:artifactId:version`（如 `com.fasterxml.jackson.core:jackson-databind:2.17.0`）。依赖从中央仓库 Maven Central 下载到本地 `~/.m2`。**Gradle** 用脚本代替 XML，解析规则不同（默认选最高版本），本卡讲 Maven。

**传递依赖与冲突**：依赖的 JAR 自带 pom，声明它的依赖，一路传递。同一个库出现不同版本时，Maven 的规则是**最近优先**：依赖树里离你的项目**最近**（层级最浅）的那个版本胜出；层级相同，**先声明的胜出**。这不是比较版本号，哪怕另一个是更新的。

**场景**：应用依次声明依赖 `b` 和 `c`；`b` 依赖 `d:1.0`，`c` 依赖 `d:2.0`，两者深度相同。真实输出的依赖树：

```
x:app:jar:1.0
+- x:b:jar:1.0:compile
|  \- x:d:jar:1.0:compile
\- x:c:jar:1.0:compile
   \- (x:d:jar:2.0:compile - omitted for conflict with 1.0)
```

`d:2.0` 被忽略。`c` 在运行时拿到的是 `d:1.0`，如果它用了 2.0 才有的方法，就会在运行时抛 `NoSuchMethodError`。调整声明顺序，结果就变了。

**要点**：
1. Maven 默认没有锁文件；版本固定靠在 pom 里写明确版本（不写范围），或用 `dependencyManagement` 统一管理版本。
2. 用 `mvn dependency:tree` 看实际解析结果；用 `maven-enforcer-plugin` 的依赖收敛规则让冲突变成构建失败。
3. Java 类路径上同名类只有一份，所以 Maven 必须在冲突的版本里选一个。
