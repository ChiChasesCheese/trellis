---
id: bagu-k8s-pod-1-crashloop-probes
node: a.linux.k8s-pod
type: qa
step: 1
---
## Q
**Kubernetes Pod · 起不来与反复重启**｜追问

面试官：「Kubernetes 里 Pod 起不来、反复重启，怎么查？存活探针和就绪探针有什么区别？」

## A
**基本回答。** 先 `kubectl describe pod` 看 Events 和 State，再 `kubectl logs --previous` 看上一个崩溃容器的日志，最后按状态判断原因。存活探针失败会重启容器，就绪探针失败只摘除流量。
CrashLoopBackOff：kubelet 指数退避重启，间隔从 10 秒涨到 5 分钟上限。退出码 137 = 128 + 9（SIGKILL），多半是内存超 limit，`describe` 显示 `OOMKilled`，也可能是停止超时被强杀。`requests` 决定调度和 QoS，`limits` 是运行上限：CPU 超限被限流，内存超限被杀。K8s 1.35 起可原地调整运行中 Pod 的 CPU 和内存（resize），缩小内存 limit 仍可能 OOM。发布出问题用 `rollout undo` 回滚。
**2026 亮点。** K8s 1.35 起可原地改运行中 Pod 的 CPU 和内存（resize 子资源，resizePolicy 决定是否重启容器），QoS 类不能变；缩小内存 limit 只是尽力而为，仍可能 OOM，泄漏的根因还得查。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<rect x="4" y="6" width="130" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="69" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Pending</text>
<line x1="134" y1="26" x2="139.0" y2="26.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="146,26 139.0,29.2 139.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="152" y="23" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">资源不足、污点、亲和性、</text>
<text x="152" y="39" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">PVC 没绑定：看 Events</text>
<rect x="4" y="60" width="130" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="69" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ImagePullBackOff</text>
<line x1="134" y1="80" x2="139.0" y2="80.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="146,80 139.0,83.2 139.0,76.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="152" y="77" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">镜像名或标签错、无权限、</text>
<text x="152" y="93" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">仓库不可达：看 Events</text>
<rect x="4" y="114" width="130" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="69" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CrashLoopBackOff</text>
<line x1="134" y1="134" x2="139.0" y2="134.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="146,134 139.0,137.2 139.0,130.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="152" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">启动即退、配置错、依赖连不上、</text>
<text x="152" y="147" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">OOM：logs --previous</text>
<rect x="4" y="168" width="130" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="69" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OOMKilled（137）</text>
<line x1="134" y1="188" x2="139.0" y2="188.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="146,188 139.0,191.2 139.0,184.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="152" y="185" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">超过内存 limit：</text>
<text x="152" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">调大 limit 或修泄漏</text>
<rect x="4" y="222" width="130" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="69" y="246" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Running 但没 Ready</text>
<line x1="134" y1="242" x2="139.0" y2="242.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="146,242 139.0,245.2 139.0,238.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="152" y="239" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">就绪探针失败：</text>
<text x="152" y="255" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">启动慢，或路径端口写错</text>
</svg>
先看 Pod 显示的状态，每种状态对应几类常见原因和该看的地方。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="4" y="8" width="120" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">startup 探针</text>
<text x="64" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（启动探针）</text>
<text x="132" y="26" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">慢启动应用先用它，</text>
<text x="132" y="42" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">通过前存活探针不会误杀</text>
<rect x="4" y="70" width="120" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="64" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">liveness 探针</text>
<text x="64" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（存活）</text>
<text x="132" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">失败 → kubelet 重启容器</text>
<text x="132" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">用来救卡死的进程</text>
<rect x="4" y="132" width="120" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64" y="150.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">readiness 探针</text>
<text x="64" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（就绪）</text>
<text x="132" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">失败 → 只摘除流量，</text>
<text x="132" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">不重启，好了再放流量</text>
</svg>
三种探针失败后的结果不同：蓝色那个会重启容器，就绪探针只摘流量。
**举个例子。** 一个服务的 Pod 一直起不来：
1. **看状态：** `kubectl get pod -o wide` 显示 `CrashLoopBackOff`，RESTARTS 一直在涨。
2. **看详情：** `kubectl describe pod` 里 Last State 是 Terminated，Reason 是 `OOMKilled`，Exit Code 是 137。
3. **看日志：** `kubectl logs <pod> --previous` 看上一次崩溃前的日志，确认启动时内存增长很快。
4. **处理：** 调整内存限制，让容器够用。
5. **再看就绪：** 之后 Pod 是 Running 但一直没 Ready，`describe` 的 Events 里有就绪探针失败，发现探针路径写错了；改对路径后恢复。
6. **发布出问题时：** 新版本一发就大面积异常，直接 `kubectl rollout undo deployment/<name>` 回到上一个版本。
**容易错。**
- **只看当前日志：** CrashLoopBackOff 时当前容器刚重启，日志几乎是空的，要加 `--previous` 看上一次崩溃。
- **存活探针设得太严：** 慢启动的应用会被反复杀掉，应该用 startup 探针给启动留时间。
- **以为就绪探针失败会重启：** 它只摘除流量，不重启容器。
- **以为 CPU 超 limit 会被杀：** CPU 超 limit 只会被限流，延迟升高；超内存 limit 才会被杀。
- **看到 137 就断定是 OOM：** 137 只代表 SIGKILL，最常见是内存超限，也可能是停止时超过优雅退出时间被强杀，要看 `describe` 里的 Reason。
