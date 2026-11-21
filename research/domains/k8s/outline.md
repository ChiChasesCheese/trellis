# Kubernetes：从零开始，按书的顺序学（k8s）

**教法**：和系统设计领域一样，树上每一节（叶子）是一篇中文正文里的一个小节；整篇正文多图、带推演过的例子（YAML + `kubectl` 输出，按书里的例子改写，不照抄）；正文下面挂四类卡：先修（prerequisite）、摘要（summary）、考点（interview probe）、拓展（2026 最佳实践，带版本号）。不做动手实验。`*` 表示帕累托核心。

**脊柱**：Kubernetes in Action 第 2 版（KIA2，Manning 2026）的 18 章，章序就是树序。Poulton《The Kubernetes Book 2026》补 KIA2 缺的部分，标「补充章」。两本书都不覆盖的（弹性、GPU/DRA、策略、GitOps、可观测、事故）放在后面的部分，出处用 kubernetes.io 文档与发布博客；版本事实只取 BUILD.md 核对表。出处写法：`〔出处：KIA2 §15.2〕`、`〔Poulton ch2〕`、`〔docs: <url>〕`。

**Poulton 内容的放置选择及理由**
1. ch2「原理」放在 KIA2 ch3（第一个应用跑起来）之后，作为补充章。理由：读者先学会容器（KIA2 ch2），再亲眼看到应用跑起来（ch3），这时讲控制面与声明式模型才有东西可对照；放在 ch1 之前会是一堆没见过的名词。KIA2 ch1 只讲「是什么」，不讲组件内部。
2. ch14「Kubernetes API」放在 KIA2 ch4（API 与对象模型）之后，作为补充章。理由：ch4 教读对象，这里教 API 服务器怎么处理请求、etcd 与 watch，两者连着读最顺。
3. ch10/11/12（存储、ConfigMap/Secret、StatefulSet）不单独成章，并入 KIA2 对应章（ch10、ch8、ch16）的叶子，出处标 Poulton；Poulton ch6/7（Deployment/Service）同理并入 KIA2 ch15/11。
4. ch8（Gateway API）并入 KIA2 ch13；ch9（服务发现深入）单独成补充章，放在 KIA2 ch13 之后，因为要先懂 Service、Ingress、Gateway 才读得懂。
5. ch13/15/16（安全）整体后移成第 6 部分，因为 RBAC、准入、威胁建模需要先熟悉所有工作负载对象；初学者在前面只会碰到 ServiceAccount 和 Secret，那里用「先修」卡指向第 6 部分。
6. 调度、requests/limits、节点（kubelet、驱逐）两本书都讲得很薄，放在第 2 部分末尾作补充章：读者刚学会 Pod 与探针，下一个问题就是「它被放到哪、吃多少资源」。

---

# 第 1 部分 从零开始：容器、第一个应用与 API

## 第 1 章 认识 Kubernetes（KIA2 ch1）

- * 为什么需要 Kubernetes（what and why）— 单机部署到多机部署会遇到的问题；把一堆机器当成一台计算机的想法。 〔出处：KIA2 §1.1〕
- * 集群的架构与应用如何运行（cluster architecture）— 控制面与工作节点的分工，一份描述提交后谁做了什么。 〔出处：KIA2 §1.2〕
- 要不要用、托管还是自建（adoption: managed vs self-hosted, vanilla vs extended）— 引入组织的取舍，什么时候不该用。 〔出处：KIA2 §1.3〕

图：① 单机部署 vs 集群上由调度器放置的对比 ② 控制面 + 工作节点的组件框图 ③ 「提交描述 → 应用运行」的流程。
2026：CNCF 2025 调查「82% 的容器用户在生产跑 Kubernetes」（BUILD.md 来源 6）；当前最新小版本 v1.36（2026-04-22）。托管服务细节待核实，不收。

## 第 2 章 容器与容器化应用（KIA2 ch2）

- * 容器与虚拟机（containers vs VMs）— 共享内核的进程隔离 vs 完整客户机；启动、体积、隔离强度的取舍。 〔出处：KIA2 §2.1.1〕
- 镜像、Dockerfile 与仓库（image, Dockerfile, registry）— 分层镜像、构建、推送、拉取；用 Kiada 示例应用走一遍。 〔出处：KIA2 §2.2〕
- * 容器的底层：命名空间与 cgroup（kernel namespaces, cgroups）— 进程看到什么由 namespace 决定，能用多少由 cgroup 决定；容器不是一个内核对象。 〔出处：KIA2 §2.3.1–2.3.3〕
- OCI、Docker 的替代品与加固隔离（OCI, runtimes, seccomp/capabilities）— 镜像与运行时标准；为什么 Kubernetes 不依赖 Docker。 〔出处：KIA2 §2.1.4, §2.3.4〕

图：① 容器 vs VM 的分层栈 ② 镜像分层与写时复制 ③ 一个进程在 PID/网络/挂载 namespace 里看到的世界 + cgroup 限额。
2026：cgroup v1 在 v1.35 被移除（kubelet 起不来）；containerd 1.x 的最后支持版本是 v1.35；用户命名空间（user namespaces）v1.36 GA。

## 第 3 章 在 Kubernetes 上部署第一个应用（KIA2 ch3）

- 本地集群与 kubectl（local cluster, kubectl, kubeconfig）— kind/minikube/Docker Desktop 起一个集群；kubeconfig 里的 cluster/user/context 三元组。 〔出处：KIA2 §3.1–3.2；Poulton ch3〕
- * 部署、暴露、扩容第一个应用（first deployment）— 一条 Deployment 创建了哪些对象，Service 如何让它可访问，扩副本看到什么。 〔出处：KIA2 §3.3〕

图：① kubectl → 集群 的一次部署链路 ② 创建 Deployment 后出现的对象树（Deployment/ReplicaSet/Pod）③ Service 把流量分给多个 Pod。
2026：本章只引入名词，机制在第 2 章补充章解释；无新特性（无）。

## 补充章 原理：控制面、声明式模型与调和循环（Poulton ch2）

- * 控制面与工作节点的组件（control plane & node components）— apiserver、etcd、scheduler、controller-manager、kubelet、kube-proxy、容器运行时各管什么，谁只和谁说话。 〔Poulton ch2〕
- * 声明式模型与调和循环（declarative model, reconcile loop）— 期望状态写进 API，控制器持续把实际状态拉向期望；水平触发为何比事件触发稳。 〔Poulton ch2；docs: https://kubernetes.io/docs/concepts/architecture/controller/〕
- * 一条请求的完整旅程（end-to-end walk-through）— 从 `kubectl apply` 到容器在节点上运行，经过 API、etcd、调度、kubelet、CRI 的时序。 〔Poulton ch2；KIA2 §1.2.4〕

图：① 控制面组件间的通信图（只有 apiserver 碰 etcd）② 调和循环：观察 → 比较 → 行动 ③ apply 到运行的时序图。
2026：v1.35 起 kubelet 不支持 cgroup v1；控制面 z-pages：/statusz v1.36 beta（默认开启）；控制器陈旧缓存（staleness）缓解 v1.36 beta。

## 第 4 章 导航 API 与对象模型（KIA2 ch4）

- * 对象清单的结构（object manifest: apiVersion, kind, metadata, spec, status）— 所有对象的共同骨架；用 Node 对象逐字段读一遍。 〔出处：KIA2 §4.1–4.2.2〕
- * spec 与 status、状态条件（spec vs status, conditions）— 谁写 spec、谁写 status；conditions 为什么比一个布尔值有用。 〔出处：KIA2 §4.2.3〕
- Event 与 describe（Events, kubectl describe）— 排查时先看什么；事件会过期。 〔出处：KIA2 §4.2.4, §4.3〕

图：① 对象清单字段的标注解剖图 ② spec/status 与控制器写入方向 ③ 一个 Event 从产生到被 describe 看到。
2026：无（无）。

## 补充章 Kubernetes API 与存储层（Poulton ch14 + docs）

- * API 的形状：REST 路径、API 组与版本（API groups, versions, resources）— 核心组与命名组、`/api/v1` 与 `/apis/<group>/<version>`、版本弃用。 〔Poulton ch14〕
- * 请求链：认证 → 鉴权 → 准入 → 持久化（API server request pipeline）— 每步能拒绝什么、变更与校验准入的先后。 〔Poulton ch14；docs: https://kubernetes.io/docs/reference/access-authn-authz/controlling-access/〕
- etcd 与乐观并发（etcd, resourceVersion）— 唯一真相来源；用 resourceVersion 做 compare-and-swap，冲突返回 409；fsync 延迟如何拖垮集群。 〔Poulton ch2；docs: https://kubernetes.io/docs/concepts/architecture/〕
- watch 与 Informer（watch, informer, work queue）— list+watch、本地缓存与工作队列让控制器不压垮 etcd；relist 与 bookmark。 〔docs: https://kubernetes.io/docs/reference/using-api/api-concepts/〕
- 服务端应用、finalizer 与垃圾回收（server-side apply, finalizers, ownerReferences）— managedFields 如何解决多写入者；对象为什么删不掉。 〔docs: https://kubernetes.io/docs/reference/using-api/server-side-apply/〕

图：① 请求链四个关卡的流程 ② resourceVersion 冲突的两次写入时序 ③ informer 内部：reflector → 本地缓存 → 队列 → worker。
2026：有序命名空间删除（Ordered Namespace deletion）v1.34 GA；其余无。

---

# 第 2 部分 在 Kubernetes 中运行应用

## 第 5 章 用 Pod 运行应用（KIA2 ch5）

- * Pod 是什么、为什么不直接用容器（pod purpose）— 共享网络与存储的最小调度单位；何时把容器放进同一个 Pod。 〔出处：KIA2 §5.1〕
- 写 Pod 清单并创建、检查（pod manifest）— 一份最小 Pod YAML 逐行读，创建后看 status。 〔出处：KIA2 §5.2〕
- * 与 Pod 交互：日志、exec、端口转发、临时调试容器（logs, exec, port-forward, ephemeral containers）— 排障基本动作。 〔出处：KIA2 §5.3〕
- * 多容器 Pod、init 容器与原生 sidecar（multi-container, init containers, native sidecars）— 启动顺序与「Job 不结束」问题如何被解决。 〔出处：KIA2 §5.4–5.5〕

图：① Pod 内共享 net/IPC/volume 的容器框图 ② init 容器 → 主容器 → sidecar 的启动时序 ③ 临时调试容器附着到运行中的 Pod。
2026：原生 sidecar（initContainer + `restartPolicy: Always`）v1.33 GA。

## 第 6 章 管理 Pod 生命周期与容器健康（KIA2 ch6）

- * Pod 状态：phase、conditions、容器状态（pod status）— 为什么 Running 不等于可用。 〔出处：KIA2 §6.1〕
- * 自动重启与三种探针（restart policy, liveness, readiness, startup）— CrashLoopBackOff 的退避；HTTP/exec/tcp 探针的语义与区别。 〔出处：KIA2 §6.2〕
- 探针设计的最佳实践（probe design）— 什么时候用 startupProbe；liveness 为什么不能检查下游依赖。 〔出处：KIA2 §6.2.7；docs: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/〕
- 启动/停止钩子与完整生命周期（postStart, preStop, lifecycle）— 初始化、运行、终止三阶段的全景时序。 〔出处：KIA2 §6.3–6.4〕
- * 优雅终止与滚动发布时的 502（graceful termination）— SIGTERM、preStop、`terminationGracePeriodSeconds` 与 endpoint 摘除的竞态。 〔docs: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/〕

图：① Pod phase 状态机 ② 容器全生命周期时间线（init → postStart → 探针 → preStop → SIGTERM → SIGKILL）③ 终止时 endpoint 摘除与 SIGTERM 的竞态。
2026：v1.34 起 restricted 级 Pod Security 标准禁止探针与生命周期处理器使用 `host` 字段；其余无。

## 第 7 章 用命名空间与标签组织资源（KIA2 ch7）

- * 命名空间（namespaces）— 逻辑分组而非隔离；跨命名空间访问；删除命名空间时发生什么。 〔出处：KIA2 §7.1〕
- * 标签与选择器（labels, selectors）— 标签语法、标准标签键；控制器与 Service 靠选择器认领 Pod。 〔出处：KIA2 §7.2–7.3〕
- 字段选择器与注解（field selectors, annotations）— 与标签的分工：筛选用 vs 附带元数据。 〔出处：KIA2 §7.4–7.5〕

图：① 命名空间与集群范围对象的包含关系 ② 标签选择器把 Pod 分成不同子集的示意。
2026：无（无）。

## 补充章 资源、调度与节点（docs，两本书覆盖很薄）

- * requests、limits 与 QoS（resource requests/limits, QoS classes）— requests 决定调度，limits 决定节流与 OOM；Guaranteed/Burstable/BestEffort 的驱逐顺序。 〔docs: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/〕
- CPU 节流与 OOM（CFS throttling, OOM kill）— 低 CPU limit 造成尾延迟；何时去掉 CPU limit；内存超限的结局。 〔docs: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/〕
- * 调度：过滤、打分、绑定（scheduling cycle）— 调度器本身是一个控制器；队列、调度周期、绑定周期。 〔docs: https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/〕
- 亲和、污点与拓扑分布（affinity, taints & tolerations, topology spread）— 高可用放置的工具箱。 〔docs: https://kubernetes.io/docs/concepts/scheduling-eviction/〕
- * kubelet、CRI 与节点压力驱逐（kubelet, CRI, node-pressure eviction）— 同步循环、容器运行时接口、软硬驱逐阈值与 OOM killer 的区别。 〔docs: https://kubernetes.io/docs/concepts/architecture/nodes/〕
- 优先级、抢占与 PodDisruptionBudget（PriorityClass, preemption, PDB）— 谁能挤掉谁；PDB 配错会让升级卡死。 〔docs: https://kubernetes.io/docs/concepts/workloads/pods/disruptions/〕

图：① requests/limits 与 cgroup 的对应、QoS 驱逐顺序 ② 调度周期：队列 → 过滤 → 打分 → 绑定 ③ 拓扑分布约束下的 skew 计算例子 ④ kubelet 与 CRI 的调用关系。
2026：Pod 原地调整大小（in-place resize）v1.35 GA；Pod 级资源（pod-level resources）v1.34 beta；matchLabelKeys 与污点参与 skew 计算 v1.33 GA（取自 v1 outline，待在 v1.33 发布博客核实）；PSI 压力指标 v1.36 GA；cgroup v1 v1.35 移除。

---

# 第 3 部分 应用配置与存储

## 第 8 章 用 ConfigMap 与 Secret 配置应用（KIA2 ch8）

- 命令、参数与环境变量（command, args, env）— 容器镜像的 ENTRYPOINT/CMD 与 Pod 字段的对应。 〔出处：KIA2 §8.1〕
- * ConfigMap：把配置与 Pod 清单解耦（ConfigMap）— 创建、注入环境变量、更新语义（环境变量不会热更新，卷会）。 〔出处：KIA2 §8.2；Poulton ch11〕
- * Secret 的真实保护程度（Secrets）— base64 不是加密；etcd 静态加密、KMS、外部密钥管理。 〔出处：KIA2 §8.3；Poulton ch11〕
- Downward API（Downward API）— 把 Pod 自己的元数据暴露给容器。 〔出处：KIA2 §8.4〕

图：① 配置注入的三条路径（env、卷、命令行参数）② Secret 从 API 到 etcd 到容器内文件的数据流及各处明文/密文。
2026：外部令牌签发（External ServiceAccount token signing）v1.36 GA，在第 6 部分展开；本章无其他新特性（无）。

## 第 9 章 为存储、配置与元数据添加卷（KIA2 ch9）

- * 卷与 emptyDir（volumes, emptyDir）— 卷的生命周期绑定 Pod 而非容器；容器重启后文件还在。 〔出处：KIA2 §9.1–9.2〕
- configMap、Secret、downwardAPI 与 projected 卷（config volumes, projected）— 以文件形式给配置，热更新机制（符号链接原子替换）。 〔出处：KIA2 §9.5〕
- hostPath、镜像卷与其他卷类型（hostPath, image volume, other types）— 访问节点文件系统的风险；把镜像当卷挂载。 〔出处：KIA2 §9.3–9.4, §9.6〕

图：① 卷在 Pod 内被多个容器挂载 ② configMap 卷的符号链接原子更新 ③ projected 卷把多个来源合成一个目录。
2026：OCI 镜像/制品卷（KEP-4639）v1.36 GA，用于分发模型文件；`gitRepo` 卷 v1.36 移除。

## 第 10 章 用 PersistentVolume 持久化数据（KIA2 ch10）

- * PV、PVC 与 StorageClass 的动态供给（PV/PVC/StorageClass）— 开发者声明需求、管理员或驱动提供卷；绑定模式 WaitForFirstConsumer。 〔出处：KIA2 §10.1–10.2；Poulton ch10〕
- 访问模式、回收策略与静态供给（access modes, reclaim policy, static provisioning）— RWO/RWX/RWOP 的区别；Retain 与 Delete 的后果。 〔出处：KIA2 §10.2.4, §10.3〕
- CSI 架构（CSI: controller, node plugin, sidecars）— 供给、挂载、扩容、快照各由哪个组件完成。 〔出处：KIA2 §10.2.6；Poulton ch10〕
- 扩容、快照与临时卷（resize, VolumeSnapshot, ephemeral volume）— 在线扩容与快照恢复；按 Pod 生成的临时 PVC。 〔出处：KIA2 §10.4–10.5〕

图：① PV/PVC/StorageClass 三者的绑定关系 ② 动态供给时序（PVC → provisioner → PV → 绑定 → 挂载）③ CSI 的 controller 与 node 两侧组件。
2026：VolumeAttributesClass（改卷参数不停机）v1.34 GA；卷扩容失败恢复 v1.34 GA；组快照（VolumeGroupSnapshot）v1.36 GA。

---

# 第 4 部分 连接与暴露应用

## 第 11 章 用 Service 暴露 Pod（KIA2 ch11）

- * Service 与 ClusterIP（Service, ClusterIP）— 稳定入口，选择器选出后端；集群内访问。 〔出处：KIA2 §11.1；Poulton ch7〕
- * NodePort、LoadBalancer 与外部流量策略（NodePort, LoadBalancer, externalTrafficPolicy）— 外部流量进来的路径、源 IP 保留、节点排空时的丢流量。 〔出处：KIA2 §11.2〕
- * Endpoints、EndpointSlice 与就绪探针（EndpointSlice, readiness）— 哪些 Pod 进入后端由就绪决定；大规模 Service 的更新放大。 〔出处：KIA2 §11.3, §11.6〕
- Service 的 DNS 记录与无头服务（DNS records, headless Service）— A/SRV 记录；无头服务直连 Pod；CNAME 别名。 〔出处：KIA2 §11.4〕
- 就近路由：internalTrafficPolicy 与拓扑感知（traffic locality）— 省跨区流量费与延迟。 〔出处：KIA2 §11.5〕

图：① Service 选择器 → EndpointSlice → Pod 的关系 ② 外部流量经 LoadBalancer/NodePort 到 Pod 的路径 ③ 就绪探针失败时端点被摘除的时序。
2026：Endpoints API v1.33 弃用（改用 EndpointSlice）；`trafficDistribution: PreferClose` v1.33 GA，`PreferSameNode` v1.35 GA，`PreferClose` 被 `PreferSameZone` 取代（弃用）；多 Service CIDR v1.33 GA；`.spec.externalIPs` v1.36 弃用。

## 第 12 章 用 Ingress 把流量路由到 Service（KIA2 ch12）

- Ingress 与 Ingress 控制器（Ingress, ingress controller）— 七层路由对象和真正干活的反向代理；基于路径与主机的路由。 〔出处：KIA2 §12.1–12.2〕
- TLS、注解、IngressClass 与自定义后端（TLS, annotations, IngressClass）— 为什么注解成了 Ingress 的痛点。 〔出处：KIA2 §12.3–12.6〕

图：① Ingress 对象 + 控制器 + 反向代理的三者关系 ② 路径/主机规则的匹配示意。
2026：Ingress NGINX 于 2026-03-24 退役（无新版本与安全修复）；迁移见下一章。

## 第 13 章 用 Gateway API 路由流量（KIA2 ch13）

- * 为什么 Gateway API 取代 Ingress（why Gateway API）— 角色分离、可移植性、表达力；与 Ingress 对照。 〔出处：KIA2 §13.1；Poulton ch8〕
- * GatewayClass、Gateway 与 HTTPRoute（core resources）— 三个对象谁归谁管，Gateway 的 status 怎么读。 〔出处：KIA2 §13.2–13.3.1；Poulton ch8〕
- 流量切分、过滤器与 TLS（traffic split, filters, TLS）— 权重金丝雀、请求头改写、网关终止 TLS 与透传。 〔出处：KIA2 §13.3.2–13.4〕
- 跨命名空间、TCP/gRPC 路由与通往服务网格（cross-namespace, TCPRoute, GRPCRoute, mesh）— ReferenceGrant；入口网关到网格的过渡。 〔出处：KIA2 §13.5–13.7〕

图：① 三种角色（基础设施提供者、集群运维、应用开发者）与三种对象的对应 ② HTTPRoute 权重切分 90/10 的流量图 ③ 跨命名空间引用与 ReferenceGrant。
2026：Gateway API v1.0 于 2023-10-31 GA（Gateway、GatewayClass、HTTPRoute 为 v1）；ingress2gateway 迁移工具（待核实版本）。

## 补充章 服务发现与集群网络（Poulton ch9 + docs）

- * 服务发现深入：注册、CoreDNS、ndots 与排查（service discovery deep dive）— 服务注册表、集群 DNS、搜索域与 `ndots:5` 的额外查询与延迟；DNS/Service/EndpointSlice 逐层排查。 〔Poulton ch9〕
- Pod 网络模型与 CNI（pod network model, CNI）— 每个 Pod 一个 IP、无 NAT 互通；CNI 插件在 Pod 创建时做什么。 〔docs: https://kubernetes.io/docs/concepts/services-networking/〕
- kube-proxy 与 Service 的数据面（kube-proxy: iptables, nftables）— Service 只是规则不是进程；DNAT 与 conntrack。 〔docs: https://kubernetes.io/docs/reference/networking/virtual-ips/〕
- * NetworkPolicy（NetworkPolicy）— 默认全通；白名单模型；策略由 CNI 实现，不支持的 CNI 不生效。 〔docs: https://kubernetes.io/docs/concepts/services-networking/network-policies/〕
- eBPF 数据面与服务网格（eBPF dataplane, service mesh）— 绕开 iptables；sidecar 与 ambient 的取舍，只讲 Kubernetes 侧机制。 〔docs: https://kubernetes.io/docs/concepts/services-networking/〕

图：① 查询 `svc.ns.svc.cluster.local` 经搜索域展开的 DNS 查询序列 ② Pod 到 Pod 跨节点的数据包路径（CNI）③ kube-proxy 规则链：ClusterIP → DNAT → Pod ④ NetworkPolicy 把默认全通变成白名单。
2026：kube-proxy nftables 后端 v1.33 GA；`ipvs` 模式 v1.35 弃用；Istio ambient、Cilium 数据面成熟度待核实。

---

# 第 5 部分 大规模管理应用

## 第 14 章 用 ReplicaSet 扩缩与维护 Pod（KIA2 ch14）

- * ReplicaSet 与调和循环（ReplicaSet, reconciliation loop）— 数 Pod、补 Pod；Pod 所有权（ownerReferences）；改 Pod 模板不会影响已有 Pod；级联删除与保留孤儿 Pod。 〔出处：KIA2 §14.1–14.3〕

图：① ReplicaSet 控制循环：期望 3 个、实际 2 个 → 创建 ② Pod 的 ownerReferences 指向链。
2026：无（无）。

## 第 15 章 用 Deployment 自动更新应用（KIA2 ch15）

- * 创建、扩缩 Deployment（Deployment basics）— Deployment → ReplicaSet → Pod 的所有权链。 〔出处：KIA2 §15.1；Poulton ch6〕
- * 滚动更新、暂停与回滚（RollingUpdate, rollback）— maxSurge/maxUnavailable 怎么算；更新到坏版本时发生什么；revision 历史。 〔出处：KIA2 §15.2；Poulton ch6〕
- Recreate 及其他发布策略（Recreate, canary, blue/green, A/B, shadowing）— 各策略适用条件，Deployment 自身只做前两种。 〔出处：KIA2 §15.2.1, §15.3〕

图：① Deployment → ReplicaSet → Pod 所有权链 ② 滚动更新时间线（新旧 ReplicaSet 副本数随步变化）③ 金丝雀 vs 蓝绿的流量图。
2026：原生 sidecar 与滚动更新的交互（v1.33 GA 之后）；渐进式发布工具见第 8 部分。

## 第 16 章 处理有状态应用：StatefulSet（KIA2 ch16）

- * 有状态需求与 StatefulSet 对比 Deployment（stateful requirements）— 稳定名字、稳定存储、有序启动；无头 Service 的角色。 〔出处：KIA2 §16.1；Poulton ch12〕
- StatefulSet 的行为：节点故障、缩容与 PVC 保留策略（behavior）— 为什么 Pod 删除不等于卷删除；OrderedReady 管理策略。 〔出处：KIA2 §16.2；Poulton ch12〕
- 更新策略与 Operator（RollingUpdate partition, OnDelete, operators）— 分区灰度；用 Operator 管数据库。 〔出处：KIA2 §16.3–16.4〕

图：① StatefulSet 的 Pod 序号、PVC、DNS 名一一对应 ② 节点失联时 Pod 被替换的时序（含脑裂风险）③ partition 灰度更新。
2026：StatefulSet 的 PVC 保留策略（persistentVolumeClaimRetentionPolicy）GA 版本待核实（疑为 v1.32），不上卡前先查；跑数据库的取舍见第 8 部分。

## 第 17 章 用 DaemonSet 部署每节点负载（KIA2 ch17）

- DaemonSet 与节点代理（DaemonSet, node agents）— 每节点一个 Pod；节点选择；特权、hostPath、hostNetwork 的特殊要求；本地通信方式。 〔出处：KIA2 §17.1–17.3〕

图：① 每个节点一个 Pod 与节点增减时的自动调整 ② 访问本地守护进程的三种方式。
2026：无（无）。

## 第 18 章 用 Job 与 CronJob 批处理（KIA2 ch18）

- * Job：完成语义、失败与并行（Job, backoffLimit, parallelism, indexed）— 一次性任务如何判定成功、如何重试。 〔出处：KIA2 §18.1.1–18.1.4〕
- CronJob（CronJob）— 调度表达式、并发策略、启动期限、保留历史。 〔出处：KIA2 §18.2〕

图：① Job 控制器的完成/失败状态机 ② Indexed Job 并行分片 ③ CronJob → Job → Pod 的三层。
2026：Job 成功策略（successPolicy）与按索引退避上限 v1.33 GA；原生 sidecar v1.33 GA 解决 Job 不结束。

---

# 第 6 部分 安全

## 补充章 API 安全、RBAC 与准入控制（Poulton ch13）

- * 认证与 ServiceAccount 令牌（authentication, ServiceAccount）— 用户证书/OIDC；Pod 的身份与绑定的短期令牌。 〔Poulton ch13〕
- * RBAC（authorization）— Role/ClusterRole/Binding 的判定；`escalate`、`bind`、`impersonate` 的提权陷阱。 〔Poulton ch13〕
- * 准入控制与 Pod Security（admission control, Pod Security Admission）— 变更与校验两段；privileged/baseline/restricted 三档。 〔Poulton ch13；docs: https://kubernetes.io/docs/concepts/security/pod-security-admission/〕

图：① 认证、鉴权、准入三关口下的一次拒绝示例 ② RBAC 四个对象的关系（subject-binding-role-resource）③ 准入链中的 mutating 与 validating 顺序。
2026：外部 ServiceAccount 令牌签发 v1.36 GA；细粒度 kubelet API 授权 v1.36 GA；结构化认证配置 v1.34 GA；Pod Security Admission 早在 v1.25 GA（同版移除 PodSecurityPolicy）。

## 补充章 威胁建模与现实安全（Poulton ch15–16）

- * 用 STRIDE 给 Kubernetes 做威胁建模（threat modeling）— 欺骗、篡改、抵赖、信息泄露、拒绝服务、提权各对应控制面哪里。 〔Poulton ch15〕
- 工作负载隔离（workload isolation）— securityContext、用户命名空间、沙箱运行时（gVisor、Kata）的取舍。 〔Poulton ch16〕
- 供应链、审计与运行时监控（supply chain, auditing, runtime monitoring）— SBOM、镜像签名、审计策略、异常检测。 〔Poulton ch16〕

图：① STRIDE 六类威胁在集群架构图上的落点 ② 从镜像到运行的供应链各检查点 ③ 容器 vs 沙箱运行时的隔离层对比。
2026：用户命名空间 v1.36 GA；Sigstore/cosign 具体版本待核实。

---

# 第 7 部分 弹性、成本与加速器（两本书都不收，用 docs 与发布博客）

## 补充章 自动伸缩与成本（docs）

- * HPA 与指标管线（HPA, metrics pipeline）— `desired = ceil(current × metric/target)`；稳定窗口与容忍度。 〔docs: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/〕
- VPA、原地调整与 requests 调优（VPA, in-place resize, right-sizing）— 为什么多数集群 requests 虚高；与 HPA 的冲突；成本分摊与 FinOps。 〔docs: https://kubernetes.io/docs/concepts/workloads/autoscaling/〕
- KEDA 与 Karpenter（event-driven scaling, node provisioning）— 按队列伸缩、按 Pending Pod 直接挑实例。 〔docs: https://keda.sh/docs/；https://karpenter.sh/docs/〕

图：① HPA 控制循环与指标来源 ② 原地调整的状态流转（Pod resize 条件）③ Cluster Autoscaler 与 Karpenter 的差异。
2026：原地调整 v1.35 GA；Pod 级资源原地调整 v1.36 beta；HPA 缩到零 v1.36 alpha；HPA 可配置容忍度 v1.33 alpha、v1.35 beta；Karpenter v1.0 于 2024 年 8 月（稳定 NodePool/EC2NodeClass API）。

## 补充章 GPU、DRA 与 AI 工作负载（docs）

- * 设备插件到 DRA（device plugins → Dynamic Resource Allocation）— ResourceClaim/DeviceClass/ResourceSlice 取代只会数个数的设备插件。 〔docs: https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/〕
- GPU 调度：整卡、切分与共享（GPU scheduling, MIG, time-slicing）— 取舍与拓扑管理器、NUMA 对齐。 〔docs: https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/〕
- 批量与帮派调度、LLM 推理（gang scheduling, Kueue, LLM serving）— 全起或全不起；模型冷启动、按并发而非 CPU 伸缩；只讲调度与伸缩，不讲推理引擎。 〔docs: https://kueue.sigs.k8s.io/docs/〕

图：① 设备插件 vs DRA 的申领流程 ② GPU 整卡/MIG/时间片三种共享方式 ③ 帮派调度的「全或无」队列。
2026：DRA 核心 v1.34 GA；管理员访问与优先备选 v1.36 GA；工作负载感知调度（Workload/PodGroup）v1.35 alpha、v1.36 继续推进仍 alpha；OCI 镜像卷 v1.36 GA。

---

# 第 8 部分 扩展、策略、交付与运维（docs）

## 补充章 扩展与策略

- * CRD 与 Operator 模式（CRD, operator pattern）— 把领域知识写成控制器；CRD 的 CEL 校验与版本转换；与第 16 章数据库 Operator 呼应。 〔docs: https://kubernetes.io/docs/concepts/extend-kubernetes/〕
- * ValidatingAdmissionPolicy 与 MutatingAdmissionPolicy（VAP, MAP, CEL）— 进程内的 CEL 校验/变更替代 Webhook；对比 Kyverno 与 Gatekeeper。 〔docs: https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/〕

图：① CRD → 自定义控制器的调和循环 ② 准入链里 Webhook vs CEL 策略的位置与失败模式。
2026：CEL 准入（KEP-3488）v1.30 稳定；MutatingAdmissionPolicy v1.34 beta → v1.36 GA。

## 补充章 交付、平台与运维

- * GitOps（GitOps: Argo CD, Flux）— Git 为唯一来源、集群内拉取；漂移检测、同步与回滚。 〔docs: https://argo-cd.readthedocs.io/；https://fluxcd.io/docs/〕
- Helm 与 Kustomize（Helm, Kustomize）— 模板 vs 补丁。 〔docs: https://helm.sh/docs/；https://kubectl.docs.kubernetes.io/〕
- 渐进式发布（progressive delivery: Argo Rollouts, Gateway API weights）— 按指标推进或回滚，对比 Deployment 滚动更新。 〔docs: https://argo-rollouts.readthedocs.io/〕
- 多租户与多集群（multi-tenancy, multi-cluster, blast radius）— 命名空间、配额、策略；一个大集群是单点。 〔docs: https://kubernetes.io/docs/concepts/security/multi-tenancy/〕
- * 集群升级策略（upgrade strategy）— 小版本逐级、弃用 API 检查、版本偏差、PDB 卡升级。 〔docs: https://kubernetes.io/docs/tasks/administer-cluster/〕
- 可观测性与 OpenTelemetry（observability, OpenTelemetry）— 指标、日志、追踪；控制面自身的指标。 〔docs: https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/〕

图：① GitOps 拉取式同步循环与漂移 ② 金丝雀按指标自动推进/回滚的流程 ③ 升级顺序：控制面 → 节点，版本偏差窗口。
2026：cgroup v1 移除、v1.36 起不再支持 containerd 1.x（v1.35 是最后支持的版本）、ipvs 弃用（v1.35）都是升级雷；OTel Collector/Operator 的版本事实待核实；Argo CD/Flux/Karpenter 的 CNCF 毕业状态待核实。

---

# 第 9 部分 工程例子：事故与复盘（k8s.af 与官方复盘）

## 补充章 事故与复盘

- * 控制面与节点级联故障（OpenAI 2024-12-11；Datadog 2023-03-08）— 遥测服务压垮 API Server、自动补丁清掉 Cilium 路由；为什么测试抓不到。 〔docs: https://status.openai.com/incidents/ctrsv3lwd797；https://www.datadoghq.com/blog/engineering/2023-03-08-deep-dive-into-platform-level-impact/〕
- 网络、DNS 与限流类事故（ndots、conntrack、CPU throttling）— Zalando、MindTickle、Buffer、Omio 等案例的故障链。 〔docs: https://k8s.af〕
- 发布与准入类事故（Webhook 卡死集群、GitOps 删命名空间、滚动更新 502）— Jetstack、Skyscanner、Ravelin 等。 〔docs: https://k8s.af〕
- * 把事故变成上线检查清单（postmortem → guardrails）— 探针、PDB、requests、ndots、webhook 失败策略、分批发布、爆炸半径。 〔docs: https://k8s.af〕

图：① 每个案例的故障链：触发 → 放大 → 为何测试没抓到 ② 检查清单对应到各章的回链图。
2026：事故年份均来自来源，不加新特性；清单回链第 2、4、5、8 部分。

---

## 不收（out of scope）

- 具体云厂商托管服务（EKS/GKE/AKS）的控制台操作 — 随版本变化快，概念已在各章覆盖。KIA2 §3.1.4–3.1.5 与 Poulton ch3 的 LKE 步骤只作背景，不展开。
- 考试技巧与 kubectl 速记 — 属于认证备考，不是原理；只借用 CKA/CKS 课纲做覆盖对照。
- Windows 节点、边缘轻量发行版（k3s 等）— 面太窄；待 Chi 需要时再开。
- 自建控制面的 kubeadm 逐步安装（KIA2 §3.1.6）— 日常少用；CKA 课纲有，作为链接读物。
- 各 CI/CD 产品的配置语法 — 与 cdn-content 的 delivery.cicd 重复。
- 实验手册 — Chi 不要动手实验；正文里只放推演过的例子。

## 与已有领域的重叠

- `skeleton/system-design.yaml` `infra.containers`（容器与编排，设计面试深度）— link：本领域是它的下钻，设计面试仍用旧叶；第 1、2、5 部分各叶标注「回链 infra.containers」。
- `skeleton/system-design.yaml` `infra.mesh`（服务网格）— link；本领域「eBPF 数据面与服务网格」只补 Kubernetes 侧机制（注入、启动顺序）与 Exponea 失败案例，不重讲 mTLS 原理。
- `skeleton/system-design.yaml` `infra.delivery`（CI/CD 与渐进式发布）— link；本领域只加 Argo Rollouts / Gateway API 权重切分的 Kubernetes 实现。
- `skeleton/sysdesign.yaml` `a.linux.k8s-pod`（Pod 起不来或反复重启）— go deeper：旧叶是 kubectl 排查步骤；本领域给 kubelet 同步、探针、OOM、驱逐的机制解释。排查流程不重复。
- `skeleton/sysdesign.yaml` `t.observability` / `platform.observability` — skip 通用可观测；只留 Kubernetes 与 OpenTelemetry 特有部分。
- `skeleton/sysdesign.yaml` 的 Raft 叶（共识算法）— link：etcd 一叶只讲 etcd 如何用 Raft（线性一致读、fsync），不重讲算法。
- `skeleton/cdn-content.yaml` `delivery.terraform-kubernetes`（Terraform 与 Kubernetes 基础）— go deeper：旧叶只到 Pod/Service/探针/滚动更新/自动伸缩的基础；本领域整体取代其 Kubernetes 一半，Terraform 仍留在旧叶。
- `skeleton/cdn-content.yaml` `delivery.canary`、`delivery.cicd` — skip，只链接。
- `skeleton/llm-inference.yaml`（GPU/推理）— link：第 7 部分的 GPU 与 LLM 推理叶只讲调度与伸缩，不讲推理引擎内部。

## 卡片格式建议

- 每个叶子 = 一篇中文正文（正文）中的一节：从零讲起，每节至少一张图（图用 mermaid 或 SVG，见每章「图：」行），带一个推演过的例子（YAML + `kubectl` 输出，读懂而不是照打）；全文不照抄书，不做实验。
- 正文下挂四类卡：
  - 先修（prerequisite）：读这一节前必须会的概念，一张卡一个概念，指向前面的叶子；按先修顺序排。
  - 摘要（summary）：一节压成一两张卡：问题 → 机制（带图）→ 要点，自洽，不依赖正文。
  - 考点（interview probe）：面试会怎么问、怎么答（含追问），对应第 2、4、5 部分的「为什么会这样」；不重复 kubectl 命令清单。
  - 拓展（2026 best practice）：取自每章「2026：」行；表格列「特性 / 阶段 / 版本」，脚注注明发布博客；BUILD.md 核对表之外的一律标待核实，不上卡。
- 机制卡至少 30% 带图（控制面、网络、存储、调度叶）。
- 案例卡（第 9 部分）：情境问题 → 故障链 → 修复与可迁移检查项；只写来源里有的数字。
- 对比卡：Gateway API vs Ingress、nftables vs iptables vs eBPF、VAP vs Webhook vs Kyverno、Deployment vs StatefulSet，各给「何时选」。

---
叶子计数：9 个部分、29 章（KIA2 原章 18 + 补充章 11），99 个叶子，核心（`*`）51（约 52%）。
