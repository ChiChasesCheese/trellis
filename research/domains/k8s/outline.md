# Kubernetes：原理、2026 最佳实践与工程案例（k8s）

三层：第一层「原理」讲它到底怎么运转，第二层「2026 最佳实践」讲现在该怎么用（版本事实全部来自 kubernetes.io 发布博客，见 BUILD.md 的核对表），第三层「工程例子」讲真实事故和迁移。`*` 表示帕累托核心。

## A. 控制面与调和循环（Control plane & reconcile）

- * 声明式 API 与调和循环（declarative API, reconcile loop）— 期望状态写进 API，控制器不断把实际状态拉向期望；为什么「边沿触发」不够、必须「水平触发」。
- * API Server 请求链（request pipeline）— 认证 → 鉴权 → 准入（变更、校验）→ 持久化的顺序，以及每步能拒绝什么。
- * etcd 与 Raft（etcd, Raft）— 唯一的真相来源；多数派写、线性一致读、为什么 3/5 节点、磁盘 fsync 延迟如何拖垮整个集群。(需先: 声明式 API 与调和循环)
- * 资源版本与乐观并发（resourceVersion, optimistic concurrency）— 用 resourceVersion 做 compare-and-swap，冲突时 409 重试，而不是加锁。
- * Watch 与 Informer（watch, informer, work queue）— 控制器如何用 list+watch、本地缓存和工作队列把 etcd 压力降下来；relist、bookmark 的作用。(需先: 资源版本与乐观并发)
- 服务端应用与字段归属（server-side apply, field ownership）— 多个写入者改同一对象时，用 managedFields 解决冲突，对比客户端 apply。
- * Deployment → ReplicaSet → Pod 的控制器链（controller chain）— 一次滚动更新在 API 里到底发生了哪几步，maxSurge/maxUnavailable 怎么算。
- * Job、CronJob 与 Indexed Job（Job semantics）— 完成语义、backoffLimit、并行与重试；成功策略（successPolicy）与按索引的退避上限在 1.33 GA。
- * StatefulSet 与有状态负载（StatefulSet）— 稳定网络身份、有序滚动、volumeClaimTemplates；为什么「Pod 删除」不等于「卷删除」。
- 垃圾回收与 finalizer（garbage collection, ownerReferences, finalizers）— 对象为什么删不掉；Terminating 卡住的排查；1.34 有序命名空间删除（Ordered Namespace deletion）GA。
- * CRD 与 Operator 模式（CRD, operator pattern）— 把领域知识写成控制器；CRD 校验（CEL、ratcheting）与版本转换。(需先: 声明式 API 与调和循环)
- API 聚合与 API 优先级与公平性（aggregation, API Priority and Fairness）— 过载时 apiserver 如何排队限流，防止一个客户端拖垮控制面。
- 控制面高可用与升级（HA control plane, version skew）— 多 apiserver、leader election、版本偏差规则与升级顺序。
- 租约与 leader election（Lease）— 多副本控制器如何只有一个干活；租约过期时的脑裂窗口。

## B. 调度与节点（Scheduler & kubelet）

- * 调度流程：过滤与打分（scheduling cycle: filter, score, bind）— kube-scheduler 的队列、调度周期与绑定周期，为什么调度本身是一个控制器。
- * requests、limits 与 QoS 类（requests/limits, QoS classes）— requests 决定调度，limits 决定节流/OOM；Guaranteed/Burstable/BestEffort 的驱逐顺序。
- * CPU limit 与节流（CFS throttling）— 为什么低 CPU limit 会造成尾延迟，何时该去掉 limit。
- * 亲和、反亲和、污点与拓扑分布约束（affinity, taints, topology spread）— 高可用放置的工具箱；matchLabelKeys 与污点参与 skew 计算在 1.33 GA。
- 优先级与抢占（PriorityClass, preemption）— 谁能挤掉谁，以及抢占引发级联驱逐的风险。
- * kubelet 的职责（kubelet: pod lifecycle, PLEG, probes）— 同步循环、容器状态上报、探针三种（startup/liveness/readiness）的语义与误用。
- * 优雅终止（graceful termination）— SIGTERM、preStop、terminationGracePeriod 与 endpoint 摘除的竞态；为什么部署时会出现 502。
- * 节点压力驱逐（node-pressure eviction）— 内存/磁盘阈值、软硬驱逐、OOM killer 与 kubelet 驱逐的区别。
- cgroup v2 与资源隔离（cgroup v2）— v1.35 起 kubelet 不再支持 cgroup v1；PSI 压力指标 1.36 GA；内存 QoS。
- * 容器运行时接口 CRI（CRI, containerd, CRI-O）— kubelet 经 gRPC 调运行时；dockershim 为何被移除；containerd 1.x 支持在 v1.35 结束。
- 镜像拉取与缓存（image pull, pull policy, credential providers）— 拉取策略、镜像 GC、并行拉取上限、凭证插件。
- 设备插件与拓扑管理器（device plugins, Topology Manager, NUMA）— GPU 等设备怎么暴露给 kubelet；CPU Manager 与 NUMA 对齐。

## C. 网络（Networking）

- * Pod 网络模型与 CNI（pod network model, CNI）— 每个 Pod 一个 IP、无 NAT 互通；CNI 插件在 Pod 创建时做什么。
- * Service 与 kube-proxy（ClusterIP, kube-proxy: iptables/nftables）— Service 只是规则不是进程；DNAT、conntrack；nftables 后端在 1.33 GA，ipvs 模式在 1.35 被弃用。
- * EndpointSlice 与就绪（EndpointSlice, readiness gates）— 为什么 Endpoints API 在 1.33 被弃用；大规模 Service 的更新放大问题。(需先: Service 与 kube-proxy)
- * CoreDNS 与 ndots:5（cluster DNS）— 搜索域导致的额外查询与 5 秒延迟；DNS 是最常见的「莫名其妙」根因。
- * NodePort、LoadBalancer 与 externalTrafficPolicy — 外部流量怎么进来，源 IP 保留与节点排空时的丢流量。
- eBPF 数据面（Cilium, eBPF dataplane）— 绕开 iptables 的转发与策略；它换来了什么、带来了什么新的故障模式。(需先: Service 与 kube-proxy)
- * NetworkPolicy — 默认全通；白名单模型；策略由 CNI 实现，没有支持的 CNI 就不生效。
- 流量分布与拓扑感知路由（trafficDistribution, topology-aware routing）— 1.33 GA；PreferSameNode 在 1.35 GA；省跨区流量费。
- 多 Service CIDR 与 IP 耗尽（multiple Service CIDRs, IP exhaustion）— 1.33 GA 的 ServiceCIDR/IPAddress；Pod CIDR 用尽导致无法扩容。
- 服务网格：sidecar 与 ambient（service mesh）— mTLS、重试、流量切分挪出应用代码，换来延迟与运维成本。

## D. 存储（Storage）

- * PV、PVC 与 StorageClass（PV/PVC/StorageClass）— 静态与动态供给、绑定模式（WaitForFirstConsumer）、回收策略（1.33 起一律遵守）。
- * CSI 架构（CSI: controller, node plugin, sidecars）— 供给、挂载、扩容、快照各由哪个组件做。
- 卷扩容与 VolumeAttributesClass（volume expansion, VolumeAttributesClass）— 扩容失败恢复与不停机改卷参数，均在 1.34 GA。
- 快照与组快照（VolumeSnapshot, VolumeGroupSnapshot）— 组快照在 1.36 GA；一致性的边界。
- 运行有状态服务的取舍（databases on Kubernetes）— 什么时候用 Operator 跑数据库，什么时候该用托管服务。(需先: StatefulSet 与有状态负载)

## E. 安全与访问控制（Security）

- * RBAC — Role/ClusterRole/Binding 的判定；最小权限；`escalate`、`bind`、`impersonate` 的提权陷阱。
- * ServiceAccount 与绑定令牌（bound service account tokens）— projected 短期令牌取代永久 Secret 令牌；外部令牌签发在 1.36 GA。
- * Secret 的真实保护程度（Secrets, encryption at rest, external secrets）— base64 不是加密；etcd 静态加密、KMS、外部密钥管理。
- * Pod Security Standards 与 Pod Security Admission — privileged/baseline/restricted 三档按命名空间执行；1.34 restricted 档禁止探针中的 `host` 字段。
- * 准入控制与 Webhook（admission webhooks）— 变更与校验 Webhook 的失败策略（failurePolicy）：错配会让集群变不可写。
- 用户命名空间（user namespaces）— 容器里的 root 映射成宿主机普通用户；1.36 GA。
- 沙箱运行时（gVisor, Kata）— 多租户下防容器逃逸的隔离层与代价。
- 认证配置与 kubelet 授权（structured authentication, kubelet authz）— 结构化认证配置 1.34 GA；细粒度 kubelet API 授权 1.36 GA。

## F. 2026 最佳实践：流量入口与发布

- * Gateway API 取代 Ingress（Gateway API vs Ingress）— GatewayClass/Gateway/HTTPRoute 的角色分离；Gateway API v1.0 于 2023-10-31 GA。
- * Ingress NGINX 退役与迁移（ingress-nginx retirement）— 2026-03-24 停止发布与安全修复；用 ingress2gateway 迁移，迁移前要弄清它的「隐式行为」。
- * Sidecar 容器 GA（native sidecars）— 1.33 GA：initContainer 里 `restartPolicy: Always`，解决启动/退出顺序与 Job 不结束的老问题。
- * 渐进式发布（progressive delivery: canary, blue-green, Argo Rollouts）— 按指标自动推进或回滚；与 Deployment 滚动更新的区别。
- 探针与启动顺序的最佳实践（probe design）— 什么时候用 startupProbe，为什么 liveness 不该检查依赖。
- PodDisruptionBudget 与节点维护（PDB, drain）— 自愿中断的预算；PDB 配错会让升级卡死。

## G. 2026 最佳实践：弹性、成本与 GPU

- * HPA 与自定义指标（HPA, metrics pipeline）— 算法 desired = ceil(current × metric/target)；稳定窗口、容忍度（可配置容忍度 1.35 beta）。
- * 原地 Pod 调整大小（in-place pod resize）— 1.35 GA：不重启改 CPU/内存；Pod 级资源（pod-level resources）1.34 beta，其原地调整 1.36 beta。
- * VPA 与 requests 调优（VPA, right-sizing）— 推荐值、与 HPA 的冲突、为什么大多数集群 requests 虚高。
- * KEDA 与事件驱动伸缩（KEDA, event-driven autoscaling）— 按队列长度等外部指标伸缩，含缩到零；原生 HPA 缩到零 1.36 仍是 alpha。
- * Karpenter 与节点自动供给（Karpenter vs Cluster Autoscaler）— 按 Pending Pod 直接挑实例类型；Karpenter v1.0 于 2024 年 8 月发布稳定 API。
- 成本治理（cost allocation, FinOps）— 命名空间/标签分摊、requests 与实际使用差、spot 与整合（consolidation）。
- * 动态资源分配 DRA（Dynamic Resource Allocation）— 1.34 GA：ResourceClaim/DeviceClass/ResourceSlice 取代只会数个数的设备插件；管理员访问与优先备选在 1.36 GA。(需先: 设备插件与拓扑管理器)
- * GPU 工作负载调度（GPU scheduling, MIG, time-slicing）— 整卡、切分与共享的取舍；DRA 的可分区设备与可消耗容量仍在 beta/alpha。
- * 批量与帮派调度（gang scheduling, Kueue）— 训练任务要么全起要么不起；工作负载感知调度（Workload/PodGroup API）1.35 alpha，1.36 继续推进。
- * 在 Kubernetes 上跑 LLM 推理（LLM serving on Kubernetes）— 模型加载慢、冷启动、按并发而非 CPU 伸缩；OCI 镜像卷（1.36 GA）用于分发模型。(需先: GPU 工作负载调度)

## H. 2026 最佳实践：策略、交付与平台

- * ValidatingAdmissionPolicy 与 CEL（VAP, CEL）— 1.30 稳定，进程内、无 Webhook 的校验；对比 OPA Gatekeeper/Kyverno。
- * MutatingAdmissionPolicy（MAP）— 1.34 beta、1.36 GA；用 CEL 替代简单的变更 Webhook。
- * GitOps：Argo CD 与 Flux（GitOps）— Git 为唯一来源、集群内拉取；漂移检测、同步策略与回滚。
- Helm 与 Kustomize（Helm, Kustomize）— 模板 vs 补丁；何时用哪个；CKA 课纲已包含两者。
- * 多租户（multi-tenancy）— 命名空间、配额、LimitRange、NetworkPolicy、策略与「每租户一集群」的取舍。
- * 多集群与爆炸半径（multi-cluster, blast radius）— 为什么一个大集群是单点；集群生命周期与批量升级。
- * 集群升级策略（upgrade strategy）— 小版本逐级升级、弃用 API 检查、原地 vs 蓝绿集群；v1.35 的 cgroup v1 移除、containerd 1.x 终止即是典型升级雷。
- 平台工程（platform engineering, golden paths）— 把 Kubernetes 包成内部平台，开发者不碰 YAML；CNCF 平台工程课纲（CNPA/CNPE）。
- * 可观测性与 OpenTelemetry（observability, OpenTelemetry）— 指标、日志、追踪三支柱；Collector 与 Operator；控制面自身的指标与 /statusz /flagz（1.35 alpha、1.36 beta）。
- 控制器过期缓存与可观测（controller staleness）— 1.36 新增的陈旧缓存缓解与指标：为什么控制器会基于旧数据做错事。
- * 供应链安全（supply chain security）— SBOM、镜像签名（Sigstore/cosign）、准入时验签、最小基础镜像。
- 运行时安全与审计（runtime security, audit logs, Falco）— 审计策略、异常行为检测与响应。

## I. 工程例子：事故与复盘（Incidents & postmortems）

- * 控制面过载级联：新增遥测服务压垮 API Server（OpenAI 2024-12-11 事故）— 每节点调用昂贵的 API，大集群才暴露；DNS 缓存延后故障 20 分钟，推广已到全量；控制面不可达使修复变慢。
- * 补丁引发网络路由被清空（Datadog 2023-03-08）— systemd 自动安全更新重启 networkd，清掉 Cilium 管理的路由，数万节点失联；新节点与重启都复现不了。
- * DNS 事故合集（ndots:5, CoreDNS OOM, conntrack）— Zalando 全集群 DNS 故障、MindTickle 5 秒延迟、Toyota Connected 的 musl 问题。
- * CPU 限流导致的延迟（CPU throttling stories）— Buffer、Omio、Airbnb 的复盘：去掉 CPU limit 或调整配额。
- * 准入 Webhook 造成集群不可写（Jetstack）— Webhook 与节点自动修复互相卡死；failurePolicy 与命名空间豁免。
- * GitOps 模板的一行错误删光命名空间（Skyscanner 2021）— 自动同步的爆炸半径；需要防删除保护与分批推进。
- * 全站故障：升级后 CNI/标签问题（Reddit 2023 Pi Day）— 大规模升级、CNI 与控制面标签的交互。
- IP 耗尽阻止扩容（loveholidays GKE）— Pod/节点 IP 用尽，自动扩容卡住。
- 反亲和与优先级引发的级联（Moonlight、Grafana Labs）— 副本全落一台机器；Pod 优先级触发连环驱逐。
- 误删集群而用户无感（Spotify）— Terraform 全局状态与多集群冗余让故障没有外溢。
- * 服务网格上线失败（Exponea Istio 2019）— 代理注入与启动顺序；何时不该上网格。
- * 滚动更新与 502（Ravelin, DevOps Hof）— endpoint 摘除竞态与 externalTrafficPolicy 与排空节点。
- 从虚拟机迁到 Kubernetes 的经验（Saltside, ThredUP, Xing）— 迁移中途退回的原因：LB、DNS、liveness 误用。
- * 把故障变成检查清单（postmortem → guardrails）— 从上面各案例抽象出十条上线前自检（探针、PDB、requests、ndots、webhook 失败策略、分批发布、爆炸半径）。

## 不收（out of scope）

- 具体云厂商托管服务（EKS/GKE/AKS）的控制台操作 — 随版本变化快，概念已在 C/E/G 覆盖。
- 考试技巧与 kubectl 速记 — 属于认证备考，不是原理；只借用 CKA/CKS 课纲做覆盖对照。
- Windows 节点、边缘轻量发行版（k3s 等）— 面太窄；待 Chi 需要时再开。
- 自建控制面的 kubeadm 逐步安装 — 日常少用；CKA 课纲有，作为链接读物。
- 各 CI/CD 产品的配置语法 — 与 cdn-content 的 delivery.cicd 重复。

## 与已有领域的重叠

- `skeleton/system-design.yaml` `infra.containers`（容器与编排，设计面试深度）— link：本领域是它的下钻，设计面试仍用旧叶；A/B/C 各叶标注「回链 infra.containers」。
- `skeleton/system-design.yaml` `infra.mesh`（服务网格）— link；本领域「服务网格：sidecar 与 ambient」只补 Kubernetes 侧机制（注入、启动顺序）与 Exponea 失败案例，不重讲 mTLS 原理。
- `skeleton/system-design.yaml` `infra.delivery`（CI/CD 与渐进式发布）— link；本领域只加 Argo Rollouts / Gateway API 权重切分的 Kubernetes 实现。
- `skeleton/sysdesign.yaml` `a.linux.k8s-pod`（Pod 起不来或反复重启）— go deeper：旧叶是 kubectl 排查步骤；本领域给 kubelet 同步、探针、OOM、驱逐的机制解释。排查流程不重复。
- `skeleton/sysdesign.yaml` `t.observability` / `platform.observability` — skip 通用可观测；只留 Kubernetes 与 OpenTelemetry 特有部分。
- `skeleton/sysdesign.yaml` 的 Raft 叶（共识算法）— link：etcd 一叶只讲 etcd 如何用 Raft（线性一致读、fsync），不重讲算法。
- `skeleton/cdn-content.yaml` `delivery.terraform-kubernetes`（Terraform 与 Kubernetes 基础）— go deeper：旧叶只到 Pod/Service/探针/滚动更新/自动伸缩的基础；本领域整体取代其 Kubernetes 一半，Terraform 仍留在旧叶。
- `skeleton/cdn-content.yaml` `delivery.canary`、`delivery.cicd` — skip，只链接。
- `skeleton/llm-inference.yaml`（GPU/推理）— link：G 的 GPU 与 LLM 推理叶只讲调度与伸缩，不讲推理引擎内部。

## 卡片格式建议

- 每张机制卡：一句问题 → 一张 mermaid 序列或组件图（如请求链、调和循环、kube-proxy 规则路径）→ 要点。控制面与网络叶至少 30% 带图。
- 版本卡：表格列出「特性 / 阶段 / 版本」，并在卡脚注明来源是哪篇发布博客；没核对的版本不上卡。
- 案例卡：情境问题 → 故障链（触发 → 放大 → 为何测试没抓到）→ 修复与可迁移的检查项；只写来源里有的数字。
- 对比卡：Gateway API vs Ingress、nftables vs iptables vs eBPF、VAP vs Webhook vs Kyverno，各给「何时选」。
- 排查卡与已有 `a.linux.k8s-pod` 区分：这里只问「为什么会这样」，不重复命令清单。

---
叶子计数：A 14、B 12、C 10、D 5、E 8、F 6、G 10、H 12、I 14，合计 91；核心（`*`）61（偏高，评审时可降到约 52）。
