You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "infra.containers": ["<id shown first>", "…"],
  "infra.mesh": ["<id shown first>", "…"],
  "infra.delivery": ["<id shown first>", "…"]
}

## infra.containers — Containers & Orchestration
Containers vs VMs, Kubernetes primitives (pods, services, autoscaling) at design-conversation depth.
- `infra-containers-vs-vms` Q: Containers and VMs both isolate workloads. What is the actual isolation mechanism of each, and what does the difference buy in density and cost in security?
  A: - **VM**: a hypervisor virtualizes hardware; every guest boots its **own kernel**. Strong boundary, but seconds to boot and GBs of overhead per instance. - **Co
- `infra-k8s-overkill` Q: When is Kubernetes over-engineering, and what do you run instead?
  A: K8s charges a **platform tax** — cluster upgrades, networking/ingress/observability stack, YAML sprawl, and in practice a platform team to own it. That tax is o
- `infra-k8s-primitives` Q: At design-conversation depth: what do a Kubernetes Pod, Deployment, Service, and HPA each abstract?
  A: - **Pod**: smallest schedulable unit — one or more containers sharing network and storage. Mortal by design; its IP is ephemeral. - **Deployment**: a declared d
- `infra-requests-limits-noisy-neighbor` Q: On a shared Kubernetes node, what do resource *requests* vs *limits* actually do — and why do CPU and memory overruns fail differently?
  A: - **Requests** = what the scheduler reserves when bin-packing pods onto nodes; your guaranteed share under contention. **Limits** = a hard runtime cap. - **CPU 

## infra.mesh — Service Mesh
Sidecars and ambient meshes — mTLS, retries, and traffic policy moved out of application code, at a latency cost.
- `infra-mesh-sidecar-intercept` Q: Mechanically, what does a service-mesh sidecar do to a pod's traffic — and why does intercepting at that point enable every mesh feature?
  A: At pod startup, iptables rules are installed that transparently **redirect all inbound and outbound TCP through an L7 proxy (Envoy) running in the same pod**. T
- `infra-mesh-tax-ambient` Q: What does a sidecar mesh cost in latency and operations, and how does the ambient/sidecarless model restructure that cost?
  A: - **Latency tax**: two extra proxy traversals per hop (caller's sidecar out, callee's sidecar in), roughly **0.5–2 ms at p99 per hop** — compounding across deep
- `infra-mesh-vs-code` Q: mTLS, retries, and traffic splitting can live in a shared library or in the mesh. When does the mesh win, and what does it inherently do worse than code?
  A: - Mesh wins on **polyglot fleets** (one proxy implementation vs a library per language), **upgrades without redeploying apps**, and **uniform enforcement** — se
- `infra-mesh-when-not` Q: When is a service mesh not worth adopting?
  A: - **Few services or a single language**: a shared library plus an API gateway covers TLS, retries, and metrics with far less machinery. - **Mostly north-south t

## infra.delivery — CI/CD & Progressive Delivery
Pipelines, canary and blue-green automation, feature flags, and config/schema changes as deploys.
- `infra-canary-automation` Q: What components turn a canary from "deploy 5% and stare at dashboards" into automated progressive delivery?
  A: - **Baseline pairing**: compare the canary against a **freshly deployed baseline running the old version** at the same size and traffic share — not against the 
- `infra-flags-deploy-release` Q: Feature flags separate {{c1::deploy}} (code reaches production, dark and inert) from {{c2::release}} (behavior exposed to users) — shipping becomes routine and low-stakes, exposure becomes a runtime decision per cohort, and reverting is an instant {{c3::kill switch (flag off)}} instead of a redeploy. The tax: stale flags multiply untested code-path combinations, so every flag needs an owner and an expiry.
- `infra-pipeline-quality-gates` Q: Why order CI/CD pipeline stages as progressively more expensive quality gates, and what class of failure does each stage uniquely catch?
  A: Each stage should catch what is **cheapest to catch there**; the ordering exists so most failures die in seconds, not in production. - **Build + unit tests** (s
- `infra-rollback-safety` Q: When is a deployment "rollback safe" (AWS's definition), and why must an automated test prove that version N-1 can read what version N wrote *before* N ever ships?
  A: - **Definition**: a deploy is rollback safe when reverting to the previous version is guaranteed to work — specifically, **version N-1 can correctly read every 
- `infra-schema-migration-deploys` Q: Why are database schema changes the riskiest class of deploy, and how does expand–contract make them safe?
  A: Two reasons: during any rolling or canary deploy, **old and new code run against the same schema simultaneously**; and destructive migrations (drop, rename, typ
- `infra-two-phase-format-rollout` Q: To change a persisted or on-the-wire data format safely, serialize the change across **two releases** — the deploy-time twin of expand–contract schema migration. Release 1 ({{c1::"prepare": ship code that can *read* the new format but still *writes* the old one}}) rolls out everywhere first; only then does release 2 ({{c2::"activate": start *writing* the new format — ideally behind a feature flag, so activation is a runtime toggle, not a deploy}}) go out. The ordering rule to memorize: {{c3::readers before writers}} — at every instant, including mid-rollout and after a rollback of release 2, every running version can read everything any version writes.
