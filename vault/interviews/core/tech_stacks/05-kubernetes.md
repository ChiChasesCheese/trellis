---
title: TS05 · Kubernetes
aliases:
  - TS05
  - Kubernetes
tags:
  - interview/stack
  - stack/kubernetes
stories: [S11]
---

# 05 · Kubernetes / 容器编排（Container Orchestration）

> 知识层（想更深时去哪）：[[CDN Content MOC|cdn-content]]：[[delivery.terraform-kubernetes]]；[[Kafka MOC|kafka]]：[[practice.kubernetes-strimzi]] · [[practice.cloud-deployment]]；[[System Design MOC|system-design]]：[[infra.containers]] · [[infra.mesh]] <!-- domain-links -->
> 适用于：JD 上出现 Kubernetes / EKS / GKE / 容器化；被问"你们的服务怎么部署的"。
> **不适用于：需要集群运维经验的岗位。这是我证据最薄的一个栈，第 5 节写清楚了边界，先读那节再决定要不要用这份。**

---

## 0. 这个栈在 JD 里到底在问什么

**一、你的服务是怎么跑起来的，你说得清吗。** 最低档的问法。能说清镜像怎么来、配置怎么注入、几个副本、健康检查怎么配，就过了。

**二、你理解声明式收敛这件事吗。** K8s 的所有设计都从一个想法长出来：你声明期望状态，控制器不断把实际状态往那个方向推。理解这一条，Deployment、Service、HPA 的行为都能自己推出来；不理解，就只能背命令。

**三、你运维过集群吗。** 最高档，也是我诚实答"没有"的那一档。区别在于有没有处理过节点压力驱逐、调度失败、网络策略、有状态负载的存储编排。

**这份文章按第一、二档来写。第三档我没有，见第 5 节。**

---

## 1. 来龙去脉

因为第 2 节的实操证据有限，这一节我写得比其他篇更厚——原理这层我是扎实的。

### 1.1 从"在我机器上是好的"到不可变镜像

部署的历史是一部消除环境差异的历史。

**第一阶段：装在机器上。** 部署 = 把代码拷过去 + 装依赖 + 改配置 + 重启。问题是机器会漂移（见 [[04-terraform-iac]] 第 1.1 节的雪花服务器），而且两个应用装在同一台机器上会抢依赖版本。

**第二阶段：虚拟机。** 每个应用一台 VM，隔离干净了。代价是每个 VM 扛着一整个操作系统——启动要分钟级，一台物理机跑不了几个。

**第三阶段：容器。** 关键洞察是：**应用要的不是一整个操作系统，只是一个隔离的文件系统视图和资源边界**。Linux 的 namespace（隔离视图）加 cgroup（限制资源）本来就能做到，容器只是把这两样封装成好用的形式。于是启动降到秒级，密度提高一到两个数量级。

更重要的是**镜像**带来的不可变性：镜像一旦构建就不再改变，部署 = 换一个镜像跑。"改配置导致漂移"这条路被从物理上堵死了——要改就重新构建、重新部署。**这是容器真正的贡献，比资源效率重要得多。**

### 1.2 核心抽象：调和循环（reconciliation loop）

有了容器还不够。一百个容器分布在二十台机器上，谁来决定哪个容器跑在哪台？挂了谁来重启？扩容谁来加？

这就是编排。而 K8s 解决它的方式，是整个系统里唯一真正需要理解的想法：

> **你写下期望状态，控制器持续观察实际状态，发现差异就采取行动缩小它。永不停止。**

```
        ┌──────────────────────────────┐
        │  期望状态（你的 YAML）        │
        │  "我要 3 个 nginx 副本"       │
        └──────────────┬───────────────┘
                       │
                  ┌────▼─────┐
                  │  控制器   │  ← 循环：观察 → 比较 → 行动
                  └────┬─────┘
                       │
        ┌──────────────▼───────────────┐
        │  实际状态（集群里真实的 Pod） │
        │  现在只有 2 个 → 创建 1 个     │
        └──────────────────────────────┘
```

这和 `terraform apply` 的收敛是同一个思想，差别在于**时机**：Terraform 是你手动触发一次，K8s 是永不停歇。所以 K8s 能自愈——节点挂了，副本数少了，控制器把它补回来，没有人介入。

理解这个循环之后，很多行为不需要记：
- 为什么 `kubectl delete pod` 之后 Pod 又出现了？因为 Deployment 的期望值没变，控制器把它补回来了。
- 为什么滚动更新是渐进的？因为控制器按策略一点点改变实际状态，每一步都要通过健康检查。
- 为什么手工改 Deployment 管理的 Pod 会被还原？因为那不是期望状态。

### 1.3 对象模型：只有四个是必须理解的

K8s 的对象非常多，但支撑起一个普通服务的只有四个：

| 对象 | 是什么 | 为什么需要它 |
|---|---|---|
| **Pod** | 一组共享网络和存储的容器，调度的最小单位 | 有些容器必须贴在一起跑（应用 + 日志收集 sidecar），Pod 是这个"贴在一起"的边界 |
| **Deployment** | 声明"我要 N 个这样的 Pod"，管理滚动更新 | Pod 是一次性的，挂了就没了。Deployment 提供"总是有 N 个"的保证和版本更替能力 |
| **Service** | 一个稳定的虚拟 IP 和 DNS 名，负载均衡到一组 Pod | Pod 的 IP 会变（重建就换），调用方需要一个不变的地址 |
| **Ingress** | 从集群外进来的 HTTP 路由 | Service 默认只在集群内可达 |

配置和密钥用 **ConfigMap** 和 **Secret** 注入，可以作为环境变量或挂载成文件。要点是：**配置与镜像分离**，同一个镜像在不同环境跑不同配置，这样"测试过的那个镜像"和"上生产的那个镜像"才是同一个东西。

### 1.4 调度与资源：requests 和 limits 的真实含义

每个容器可以声明两个数：

- **requests** —— 调度器用它决定把 Pod 放哪。节点的剩余可分配量必须 ≥ requests。**它是调度的依据，不是运行时的限制。**
- **limits** —— 运行时的硬上限。CPU 超了会被节流（throttle），内存超了会被 **OOMKill**。

两者的差值决定了集群的**超售**程度。requests 设太高，机器买多了浪费；设太低，节点被塞爆，所有 Pod 一起卡。

**最经典的生产事故是内存 limits 设低了**：平时好好的，流量一高就被 OOMKill，Pod 重启，流量转到别的 Pod，把它们也打爆——**级联失败**。CPU 超限只是变慢，内存超限是直接杀死，这个不对称性是调参时必须知道的。

### 1.5 三种探针，各管各的事

这是面试高频，而且很多人搞混：

| 探针 | 失败时发生什么 | 该检查什么 |
|---|---|---|
| **liveness** | **重启容器** | 只查"进程是不是死锁了"。**绝不要在这里查下游依赖** |
| **readiness** | 从 Service 的后端里摘掉，不重启 | 查"我现在能不能服务请求"，包括下游依赖是否就绪 |
| **startup** | 重启容器，但在它通过之前 liveness 不生效 | 给启动慢的应用（JVM）一个宽限期 |

**liveness 查下游是一个典型的放大故障的错误**：数据库抖一下，所有 Pod 的 liveness 一起失败，全部重启，重启后连接池还要重建，把数据库压得更惨。正确做法是下游不可用时 readiness 失败（暂时不接流量），但不重启。

### 1.6 有状态负载为什么难

K8s 的一切设计假设 Pod 是**可随意替换的**——挂了重建一个一样的。有状态应用违反这个假设：一个 Kafka broker 不能随便换成另一个，它有自己的身份和数据。

StatefulSet 给了稳定的网络标识和持久卷，但只解决了一半。真正麻烦的是运维语义：扩容要重新分配分区、升级要按顺序滚动、节点挂了数据要重建。这些是应用特有的，K8s 不懂。

**Operator 模式**是答案：把运维知识写成一个控制器，让它去管这类应用（Kafka 的 Strimzi 就是这个，见 [[practice.kubernetes-strimzi]]）。这也是 1.2 那个调和循环的自然延伸——只不过这次期望状态是"一个健康的 Kafka 集群"。

### 1.7 关键权衡

**买到了**：自愈、声明式的滚动更新与回滚、跨机器的资源池化、统一的部署抽象。

**代价很实在**：
- **复杂度巨大。** 一个"就跑一个 web 服务"的需求，在 K8s 上要碰十来个概念。小团队小规模，这个复杂度换不来对等的收益。
- **调试路径变长。** 请求不通，可能是 Ingress、Service、Pod、NetworkPolicy、DNS 任何一层。
- **需要专门的人。** 集群本身是要运维的，"用 K8s 省运维"通常是个错觉，只是把运维从应用挪到了平台。

---

## 2. 在我们这套系统里它怎么用

三个服务都跑在 K8s 上，但**部署这一层是平台团队提供的**，应用团队按规范填模板。我描述的是我能从仓库里读到的形状。

### 2.1 用 ERB 模板生成 manifest，不是 Helm

三个仓库的 `kubernetes/` 目录里都是 `.yaml.erb` —— Ruby 的 ERB 模板，渲染时注入环境变量：

```erb
<% account = ENV.fetch('ACCOUNT') %>
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: pricing-config
  namespace: pricing
data:
  GRPC_PORT: "50051"
  DIMENSION: "<%= @environment %>"
  KAFKA_BOOTSTRAP_SERVERS: "<%= kafka_standard_bootstrap %>"
  SPRING_PROFILES_ACTIVE: "<%= @environment %>"
```
（`pricing/kubernetes/config.yaml.erb`）

**为什么是 ERB 而不是 Helm 或 Kustomize**：这是 Braintree 内部平台的既有选择，配套有 `custom_scope.rb` / `funding_scope.rb` 这样的辅助类提供模板里可用的方法（比如上面的 `kafka_standard_bootstrap`）。好处是和公司内部的服务发现、账号体系深度集成；代价是脱离了 K8s 生态的通用工具链，`helm diff` 这类东西用不上。

这是一个很常见的情形，值得在面试里诚实描述：**大公司里应用团队面对的往往不是原生 K8s，而是公司包装过的一层**。说清楚自己站在哪一层，比假装熟悉整个栈可信。

### 2.2 一个 codebase 部署成多个角色

`pricing/kubernetes/` 里有四个部署入口：

```
deploy-k8s.yaml          deploy-rest.yaml
deploy-web.yaml          deploy-vas-replay.yaml
```

同一份代码、同一个镜像，按不同角色部署成不同的 Deployment：gRPC 服务、REST API、web、以及 `vas-replay`（重放类的后台处理）。配置里能看到两个端口并存：`GRPC_PORT: 50051` 和 `REST_API_PORT: 8081`。

**这是个好设计**：重放任务很吃资源，和在线请求放在同一组 Pod 里会互相干扰；拆成独立 Deployment 之后，两者可以独立扩缩容、独立设资源上限、独立发布。这正是 1.4 里 requests/limits 隔离的现实用法——**用部署单元切开负载，比在应用内做线程池隔离更彻底**。

### 2.3 数据库迁移是一个 Job，不是部署步骤

`snowglobe/kubernetes/snowglobe_db_migrate.yaml.erb` + `db-migrate.sh`，`pricing/kubernetes/db_migrate.yaml.erb` —— 迁移被建模成独立的 K8s Job。

为什么值得单说：**迁移和应用发布的生命周期不同**。迁移要在新版本代码启动前跑完、要能单独重试、失败时不该让整个发布卡在半途。做成 Job 之后它有自己的成功/失败语义，而不是藏在应用启动脚本里。

snowglobe 还有 `snowglobe_db_snapshot.yaml.erb` + `db-snapshot.sh` —— 迁移前打快照。对着数仓跑 Flyway 迁移风险不小，快照是回滚的前提。这条接到 [[06-cicd-progressive-delivery]] 的回滚讨论。

`pricing/kubernetes/cron_jobs.yaml.erb` 说明定时任务也在 K8s 里管，用 CronJob 而不是机器上的 crontab——同样是消灭雪花机器的一环。

### 2.4 可观测性是部署的一部分

`snowglobe/kubernetes/` 里有 `datadog_agent.yaml.erb` 和 `datadog_agent_configmap.yaml.erb`（后者 51KB），pricing 的 ConfigMap 里有一整组 Datadog 环境变量：

```
DD_JMXFETCH_ENABLED: "true"      DD_TRACE_AGENT_PORT: "30126"
DD_PROFILING_ENABLED: "true"     DD_LOGS_INJECTION: "true"
DD_TRACE_SAMPLE_RATE: "1"        DD_ENV: "<%= @environment %>"
```

同一个 ConfigMap 里还有 **Sentry** 的 DSN，按环境切换 prod / 非 prod 的 project。

**所以 Datadog 和 Sentry 是并存的，分工不同**：Datadog 管指标、APM trace、JVM profiling、日志注入；Sentry 管应用异常。这个事实值得记住——详见 [[08-observability-oncall]]。

### 2.5 我做的部分 `[me]`

**很少，说清楚：我没有 K8s 方面的实质贡献。**

我的工作在 Snowflake 这一侧——存储过程、SQL 管道、数据质量框架（见 [[03-snowflake-warehouse]]、[[07-data-pipelines-cdc]]）。K8s 对我而言是"我的代码跑在上面"的环境，manifest 由平台团队和服务的主要维护者管理。

我确实**读过**这些 manifest（写这份文章时读的，以及排查问题时读过配置），也理解上面描述的每一个设计，但那是理解，不是经验。**这个区别我在面试里会主动说明**，见下一节。

---

## 3. stripe kit 考到的点

K8s 不在 OA 考纲里。间接相关的只有一条思想：

- [[s11-idempotency-dedup|S11 幂等 / 去重]] —— 调和循环之所以能工作，前提是"把实际状态推向期望状态"这个操作可以反复执行而不出错。这和 `terraform apply`、和 MERGE 的幂等是同一件事在不同尺度上的体现。

系统设计轮里被问到部署和扩缩容时，第 1 节的内容够用。

---

## 4. 常见追问与答法

| 追问 | 一句话答 | 展开的抓手 |
|---|---|---|
| K8s 解决什么问题 | 声明期望状态，控制器持续收敛——于是自愈、滚动更新、资源池化都是它的推论 | 1.2 那张图 |
| liveness 和 readiness 的区别 | liveness 失败重启容器，readiness 失败只摘流量 | 1.5；重点讲"liveness 查下游会放大故障" |
| requests 和 limits 的区别 | requests 是调度依据，limits 是运行时硬顶 | 1.4；CPU 超限只是节流，内存超限直接 OOMKill |
| 为什么有状态应用难 | K8s 假设 Pod 可随意替换，有状态应用不满足这个前提 | 1.6；引到 Operator |
| 你们怎么部署的 | ERB 模板渲染 manifest，同一镜像按角色部署成四个 Deployment，迁移是独立 Job | 2.1–2.3 |
| **（三层）一个 Pod 反复 OOMKill,怎么查** | **先看是不是 limits 设低了还是真泄漏——前者重启周期跟流量相关，后者跟运行时长相关** | 我能讲清思路，但要说明这是推理不是经验 |
| **（三层）滚动更新时老版本和新版本同时在跑,数据库 schema 怎么办** | **迁移必须向后兼容：先加列不删列，等所有实例都上了新版本再清理** | 这个我有真实经验（Flyway + 数仓迁移），接到 [[06-cicd-progressive-delivery]] 的兼容性一节 |

---

## 5. 我的边界

**这一节是这份文章最重要的部分。**

**我没有运维过 K8s 集群。** 没处理过节点压力驱逐、调度失败、网络策略、CNI 问题、集群升级、etcd 运维。
→ 我会说："K8s 我是使用者不是运维者。我们的部署由平台团队提供模板，我理解 manifest 里每一项的含义，也能读懂和改，但我没有运维过集群——节点级的问题、网络策略、集群升级这些我没碰过。"
→ **不要接一句"但我学得很快"。** 那句话不加分。接的应该是具体的相邻经验：

**能接到哪去。** 我真正做过的运维是在数据平台那一侧：生产事故的根因定位（ACH fee-calc 那次，从 PagerDuty 告警追到一个 SQL UDF 的重载歧义，见 [[08-observability-oncall]]）、Terraform 管的基础设施（见 [[04-terraform-iac]]）、以及带回滚能力的生产迁移（见 [[06-cicd-progressive-delivery]]）。**我的运维经验是真的，只是发生在 Snowflake 而不是 K8s 上。** 这么说比含糊其辞强，也比硬吹强。

**Kafka on K8s（Strimzi）我只有概念。** 我简历上曾经有一条实习期的 "Kafka in Kubernetes"，**核对下来证据不足**（见 [[Tech Stacks]] 里的核查结论）。我现在不讲那条了——我有更好的 Kafka 素材：生产环境的事件消费和 CDC 管道（见 [[02-kafka-event-streaming]]）。

**Service mesh 完全没有实操。** Istio / Linkerd 的 sidecar 注入、mTLS、流量切分我只读过。
→ 如果 JD 重度依赖 mesh，这份文章撑不住，别用它硬顶。

---

## 6. 往深里看

| 节点 | 什么时候去读它 |
|---|---|
| [[infra.containers]] | 容器与编排的完整体系——我的主要补课方向 |
| [[delivery.terraform-kubernetes]] | Terraform 管 K8s 资源，两个声明式系统的组合 |
| [[practice.kubernetes-strimzi]] | Operator 模式与 Kafka on K8s（1.6 的展开） |
| [[practice.cloud-deployment]] | 托管服务 vs 自建的取舍 |
| [[infra.mesh]] | Service mesh——我的空白区 |

相邻的几份：[[04-terraform-iac]]（同为声明式收敛，思想同源）、[[06-cicd-progressive-delivery]]（部署之后的发布策略）、[[08-observability-oncall]]（2.4 那套 Datadog/Sentry 配置的用途）。

卡片在 `vault/domains/cdn-content/cards/delivery/`（含 `delivery-kubernetes-rollout-capacity.md`、`delivery-kubernetes-probe-choice.md`）、`vault/domains/kafka/cards/practice/`；readings 在 `vault/domains/cdn-content/readings/delivery-kubernetes-deployments.md`。
