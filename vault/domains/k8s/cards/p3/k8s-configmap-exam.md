---
id: k8s-configmap-exam
node: p3.t01.configmap-pod-manifest
type: qa
step: 2
tags: [考点]
---
## Q
**ConfigMap · 考点**｜考点 · 必会

你修改了 ConfigMap `kiada-config` 里的 `log-level`，改成了 `warn`。有两个 Pod，一个把它注入成**环境变量**，一个挂载成**卷里的文件**。几分钟后，两个 Pod 里的值分别是什么？怎么让环境变量那个也生效？

## A
| Pod | 几分钟后 | 原因 |
|---|---|---|
| 环境变量那个 | **仍是旧值** | 环境变量在容器启动时就定下来了，进程运行期间不会变 |
| 卷里文件那个 | **变成新值** | kubelet 会定期同步卷里的文件，用符号链接原子替换，所有文件同时更新 |

- **让环境变量生效：** 重启容器。书里的说法：容器重启后（崩溃或被 liveness 杀掉）会用新值。主动做：`kubectl rollout restart deployment <名字>`，滚动换掉所有 Pod。
- **卷里的文件虽然更新了：** 应用要自己重新读文件才会用到新值（很多程序只在启动时读一次）。
- **这是个取舍：** 环境变量方式更稳（一个 Pod 的配置不会中途变），卷方式更灵活。要不要自动热更新，取决于你的应用能不能安全处理配置变化。

**出处：** KIA2 §8.2（What happens when you modify a ConfigMap）、§9.4（configMap 卷的原子更新）
