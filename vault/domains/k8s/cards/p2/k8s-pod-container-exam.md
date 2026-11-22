---
id: k8s-pod-container-exam
node: p2.t01.pod-container
type: qa
step: 2
tags: [考点]
---
## Q
**Pod 是什么**｜考点 · 必会

下面三种组合，该放同一个 Pod 还是分开？
A. Node.js 应用 + 给它加 HTTPS 的反向代理
B. Node.js 应用 + MongoDB
C. Web 应用 + 一个把它写的日志文件转发出去的辅助程序

## A
| 组合 | 选择 | 理由 |
|---|---|---|
| A | 同一个 Pod | 代理和应用要用 localhost 通信，必须一起启动、一起扩缩、一起消失 |
| B | 分开 | 应用想扩到 5 份，数据库不应该跟着扩成 5 份；两者生命周期也不同 |
| C | 同一个 Pod | 辅助程序要读同一个目录里的日志文件，用共享的卷最简单 |

- **判断法：** 问「它们能不能独立扩缩？必须在同一台机器上吗？」两个都是「必须」才放一起。
- **副作用：** 同一个 Pod 的容器共用一个 IP，所以不能都监听同一个端口。
- **不要图省事：** 把所有东西塞进一个 Pod，就失去了独立扩缩和独立升级。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §5.1.3（何时把多个容器放进同一个 Pod）

</details>
