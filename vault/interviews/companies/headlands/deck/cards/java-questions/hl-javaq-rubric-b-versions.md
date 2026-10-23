---
id: hl-javaq-rubric-b-versions
node: java-questions.rubric
type: qa
step: 5
---
## Q
回答"Java 8、11、17、21 有什么区别"这类版本差异问题，强、一般、弱的答案各有什么特征？

## A
- **强**：按 LTS 8 / 11 / 17 / 21 讲，每个版本一个特性 + 一个会用的理由；把 record + sealed + 模式 switch 串成一个故事（编译器检查穷尽，对比 visitor）；知道运行时差异（G1 默认、紧凑字符串、偏向锁移除、虚拟线程）；区分正式与预览。
- **一般**：能列 lambda / Stream、`var`、record、虚拟线程，但没有"为什么"和"什么时候不用"。
- **弱**：把非 LTS 当必考；混淆版本号（如说 record 是 Java 11）；提到已撤回的 String Templates；把预览特性当生产特性。
