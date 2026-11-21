# k8s — Kubernetes：原理、2026 最佳实践与工程案例

Survey date 2026-11-20 (steps 1–2 of `building-study-domains`). No skeleton, no cards yet. Outline: `outline.md`.

## Sources surveyed (step 1)

| # | URL | Licence | Covers | Role |
|---|---|---|---|---|
| 1 | https://kubernetes.io/docs/concepts/ | free-online | Official concepts: architecture, workloads, services/networking, storage, config, security, scheduling, policy, extend | authoritative outline |
| 2 | https://github.com/cncf/curriculum (CKA / CKAD / CKS PDFs, file names `*_v1.37.pdf`) | free-online | Exam competency lists. CKA weights: Troubleshooting 30%, Cluster architecture/install/config 25%, Services & networking 20%, Workloads & scheduling 15%, Storage 10% (now names Gateway API, Helm/Kustomize, CRDs/operators). CKS: cluster setup 15, hardening 15, system hardening 10, microservice vulnerabilities 20, supply chain 20 (+ monitoring/runtime) | independent outline (competency-based) |
| 3 | Kubernetes in Action, 2nd ed. (Lukša, Conner; Manning, 2026). Listings: https://www.oreilly.com/library/view/kubernetes-in-action/9781617297618/ , https://www.simonandschuster.com/books/Kubernetes-in-Action-Second-Edition/Marko-Luksa/9781617297618 | commercial | Intro, containers, API object model, pods, controllers, Deployments, StatefulSets, DaemonSets, networking. Full TOC NOT confirmed (publisher pages truncated; author list differs across sellers) | independent outline (book) |
| 4 | Production Kubernetes (Rosso, Lander, Brand, Harris; O'Reilly 2021) — https://www.oreilly.com/library/view/production-kubernetes/9781492092292/ | commercial | Platform design: app platform, container runtime, networking, identity, secrets, multi-tenancy, policy, observability, delivery. TOC taken from memory, not re-fetched | independent outline (production) |
| 5 | https://kubernetes.io/blog/ release posts v1.33 (2025-04-23), v1.34 (2025-08-27), v1.35 (2025-12-17), v1.36 (2026-04-22) | free-online | Exact graduation stage per feature with KEP numbers — the source for every GA claim in the outline | version ground truth |
| 6 | https://www.cncf.io/announcements/2026/01/20/kubernetes-established-as-the-de-facto-operating-system-for-ai-as-production-use-hits-82-in-2025-cncf-annual-cloud-native-survey/ (survey PDF: https://www.linuxfoundation.org/hubfs/Research%20Reports/CNCF_Annual_Survey_Report_1.15.26.pdf) | free-online | 2025 survey: 82% of container users run Kubernetes in production (66% in 2023); 628 respondents, fielded Sept 2025; 66% of AI adopters use it for inference | adoption / AI context |
| 7 | https://k8s.af (source moved to https://codeberg.org/hjacobs/kubernetes-failure-stories; GitHub mirror hjacobs/kubernetes-failure-stories, 6.2k stars) | free-online | ~59 public postmortems 2017–2023 (CPU throttling, conntrack/DNS, ndots:5, admission webhooks, IP exhaustion, etcd, upgrades) | case source |
| 8 | https://github.com/ramitsurana/awesome-kubernetes (16k stars, pushed 2026-10-31); https://github.com/magnologan/awesome-k8s-security | free-online | Curated link lists (tools, security, GitOps, networking) | breadth cross-check |
| 9 | https://learnk8s.io , https://github.com/shubheksha/kubernetes-internals | free-online | Practitioner tutorials; internals notes. Not fetched this session; kept as reading candidates, content unverified | step-6 readings |
| 10 | https://gateway-api.sigs.k8s.io/ ; https://kubernetes.io/blog/2023/10/31/gateway-api-ga/ | free-online | Gateway API v1.0 GA on 2023-10-31 | networking best practice |
| 11 | https://status.openai.com/incidents/ctrsv3lwd797 ; https://www.datadoghq.com/blog/engineering/2023-03-08-deep-dive-into-platform-level-impact/ | free-online | Two modern postmortems (details in outline) | cases |

## Verified version facts (from release posts, this session)

| Feature | Stage / version | Source |
|---|---|---|
| Sidecar containers (KEP-753) | GA v1.33 | v1.33 post |
| nftables kube-proxy backend (KEP-3866) | GA v1.33 (iptables still default then) | v1.33 post |
| Topology-aware routing / `trafficDistribution: PreferClose` | GA v1.33; `PreferSameNode` GA v1.35; `PreferClose` deprecated in favour of `PreferSameZone` | v1.33, v1.34, v1.35 posts |
| Multiple Service CIDRs (KEP-1880) | GA v1.33 | v1.33 post |
| Endpoints API | deprecated v1.33 (use EndpointSlice) | v1.33 post |
| DRA core (`resource.k8s.io/v1`, KEP-4381) | GA v1.34 | v1.34 post |
| DRA admin access, prioritized alternatives | beta v1.34 → GA v1.36 | v1.34, v1.36 posts |
| VolumeAttributesClass (KEP-3751) | GA v1.34 | v1.34 post |
| CEL admission, ValidatingAdmissionPolicy ("CEL for Admission Control", KEP-3488) | stable v1.30 | v1.30 post (listed as KEP 3488; the post does not name the VAP object) |
| MutatingAdmissionPolicy (KEP-3962) | beta v1.34 → GA v1.36 | v1.34, v1.36 posts |
| In-place Pod resize (KEP-1287) | beta v1.33 → GA v1.35; Pod-level resources resize beta v1.36 | v1.33, v1.35, v1.36 posts |
| Pod-level resources (KEP-2837) | beta v1.34 | v1.34 post |
| User namespaces (KEP-127) | beta v1.33 → GA v1.36 | v1.33, v1.36 posts |
| OCI image/artifact volume source (KEP-4639) | beta v1.33 → GA v1.36 | v1.33, v1.36 posts |
| External ServiceAccount token signing (KEP-740) | beta v1.34 → GA v1.36 | v1.34, v1.36 posts |
| Fine-grained kubelet API authorization | GA v1.36 | v1.36 post |
| PSI metrics | GA v1.36 | v1.36 post |
| Gang / workload-aware scheduling (KEP-4671) | alpha v1.35 (Workload/PodGroup APIs advanced in v1.36, still alpha) | v1.35, v1.36 posts |
| HPA scale-to-zero (KEP-2021) | alpha v1.36 | v1.36 post |
| cgroup v1 support | removed (kubelet fails to start) in v1.35 | v1.35 post |
| kube-proxy `ipvs` mode | deprecated v1.35 | v1.35 post |
| containerd 1.x | v1.35 last release supporting it | v1.34, v1.35 posts |
| Service `.spec.externalIPs` | deprecated v1.36, removal planned v1.43 | v1.36 post |
| `gitRepo` volume | removed v1.36 | v1.36 post |
| Ingress NGINX | retired 2026-03-24 (no more releases or security fixes) | v1.36 post; https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/ |
| Gateway API | v1.0 GA 2023-10-31 (Gateway, GatewayClass, HTTPRoute at v1) | https://kubernetes.io/blog/2023/10/31/gateway-api-ga/ (HTTPRoute listing partly from the fetched summary) |
| Karpenter | v1.0 announced Aug 2024 (stable NodePool/EC2NodeClass APIs) | https://aws.amazon.com/about-aws/whats-new/2024/08/karpenter-1-0/ |
| Restricted PSS forbids `host` in probes/lifecycle handlers | v1.34 behaviour change | v1.34 post |

## Not confirmed (do not put on cards until checked)

- Pod Security Admission GA version (1.25) and PodSecurityPolicy removal version: from memory only.
- CNCF maturity (graduated) status of Argo CD, Flux, KEDA, Cilium, Karpenter: search returned nothing; check cncf.io/projects.
- AppArmor GA: v1.30 and v1.34 posts both list KEP-24 as stable, so the version is unclear; skip until the KEP page is read.
- Kubernetes in Action 2nd ed. full TOC; Production Kubernetes TOC; OpenTelemetry-in-Kubernetes specifics (Collector/Operator, kubelet tracing version).
- Whether the v1.37 CKA curriculum (file name) matches current exam environment version.
- Anything about Linkerd/Istio ambient GA status, Cilium/eBPF performance numbers, Argo CD vs Flux market share: not searched.

## Ledger

| Step | Status |
|---|---|
| 1 survey | done 2026-11-20 |
| 2 outline | drafted, awaiting review (`outline.md`) |

**Orchestrator check 2026-11-20 against the v1.33–v1.36 release blogs:** confirmed cgroup v1 removal (v1.35), /statusz beta (v1.36), controller staleness mitigation beta (v1.36), ordered namespace deletion GA (v1.34), volume-expansion-failure recovery GA (v1.34), VolumeAttributesClass GA (v1.34), VolumeGroupSnapshot GA (v1.36), Job successPolicy and backoff-limit-per-index GA (v1.33), structured authentication configuration GA (v1.34), HPA configurable tolerance alpha v1.33 → beta v1.35, kube-proxy nftables GA (v1.33), ipvs deprecated (v1.35), containerd 1.x support ends in v1.36 (v1.34 blog). Pod Security Admission GA v1.25 (kubernetes.io blog 2022-08-25). Still unverified: StatefulSet PVC retention GA version, CNCF maturity of Argo/Flux/KEDA, Istio ambient GA, OTel/Sigstore/ingress2gateway versions.
