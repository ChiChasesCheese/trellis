---
id: k8s-lifecycle-hooks-exam
node: p2.t02.poststart-prestop-lifecycle
type: qa
step: 2
tags: [考点]
---
## Q
**Hook 的坑**｜考点 · 必会

有人给 Web 容器加了 postStart hook：`httpGet` 访问**自己**的 `/warmup`。在开发机上正常，上线后偶发容器不停重启。为什么？另外，preStop 里 `exit 1` 会阻止容器终止吗？

## A
| 现象 | 原因 |
|---|---|
| 偶发循环重启 | postStart 和主进程**同时**开始。负载高时 Web 服务器还没监听，hook 的请求失败，容器被重启；重启后同样的竞争再来一遍 |
| 404 也算成功 | HTTP hook 对 404 这类响应不当作失败，路径写错了也没人发现 |
| preStop 失败 | **不阻止终止**，容器照样被杀，只留下一个 `FailedPreStopHook` 警告事件 |

- **规则：** 不要让 postStart 的 HTTP 请求指向自己或同 Pod 的其他容器。需要预热，改用 init 容器、应用自身的启动逻辑，或者用 readiness probe 控制接入流量的时机。
- **看现象：** `kubectl get pods -w` 会看到 `PostStartHookError`；事件里有失败命令和退出码；之后变成 `CrashLoopBackOff`。
- **preStop 常见用途：** 让 nginx 之类不优雅退出的程序先 `nginx -s quit`，或者 `sleep` 几秒给 Service 摘除端点留时间（见 graceful termination）。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §6.3.1「HTTP GET post-start hook…endless restart loop」、§6.3.2（pre-stop 失败不阻止终止）

</details>
