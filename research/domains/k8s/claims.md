# k8s claims ledger (card id | claim | source)

| card | claim | source |
|---|---|---|
| k8s-why-kubernetes | Kubernetes is an API plus simple controllers that keep containerized apps running | KIA2 ch1 intro |
| k8s-why-kubernetes-exam | scheduler marks a task pending if no suitable node | Poulton ch2 "The scheduler" |
| k8s-cluster-architecture-prereq | prod: 3 or 5 control plane nodes across AZs; user apps on workers | Poulton ch2 "The control plane" |
| k8s-control-plane-down-exam | etcd split-brain -> read-only; apps keep working but cannot scale/update; odd replica count; HA is not backup | Poulton ch2 "The cluster store" |
| k8s-containers-vs-vms-exam | Windows containers need Windows worker nodes; mixed clusters ok | Poulton ch2 |
| k8s-namespaces-cgroups-notes | namespace types mnt/pid/net/ipc/uts/user/time/cgroup; cgroups limit CPU/memory/disk/net bw; docker --memory is cgroup config | KIA2 §2.3.1–2.3.2 |
| k8s-namespaces-cgroups-beyond | cgroup v1 removed v1.35 (kubelet fails to start); user namespaces GA v1.36 | BUILD.md verified table; orchestrator check |
| k8s-kubectl-declarative-exam | created/unchanged/configured outputs; create twice -> AlreadyExists | kubectl behaviour (docs: Declarative Management) |
| k8s-first-deployment-notes | Pod name pattern, Pending then Running, expose --type=LoadBalancer, EXTERNAL-IP <pending> | KIA2 §3.3 |
| k8s-reconcile-loop-beyond | staleness symptoms (wrong action, no action, slow); mitigation beta v1.36 | k8s blog 2026-04-28 (symptoms read); beta per BUILD.md orchestrator check |
| k8s-api-rest-* | /api/v1, /apis/<group>/<version>, namespaced path extra segments, kubectl api-resources | Poulton ch14 "The API" |
| k8s-api-pipeline-* | authn -> authz (RBAC deny by default) -> mutating -> validating admission | Poulton ch13 "Admission control" |
| k8s-api-pipeline-notes/exam | 401 = unauthenticated, 403 = forbidden | HTTP semantics; kubernetes.io controlling-access |
| k8s-pod-debug-* | logs --previous, exec, port-forward, kubectl debug ephemeral container | KIA2 §5.3; kubernetes.io Tasks > Debug Running Pods |
| k8s-multi-container-* / beyond | native sidecar = init container + restartPolicy: Always; supported since v1.28 (book); GA v1.33; shut down after normal containers, reverse order | KIA2 §5.5; BUILD.md verified table (v1.33 GA) |
| k8s-probes-exam | restart delay: none, 10 s, doubling, cap 5 min, reset after running 2x cap | KIA2 ch6 summary |
| k8s-probes-beyond | restricted PSS forbids `host` in probes/lifecycle handlers from v1.34, KEP-4940 | k8s v1.34 release post |
| k8s-graceful-termination-* | default terminationGracePeriodSeconds 30 s; preStop -> SIGTERM -> KILL | KIA2 §6.4 |
| k8s-namespaces-beyond | ordered namespace deletion: introduced v1.33, stable v1.34; pods deleted first; CVE-2024-7598 | k8s v1.34 release post |
| k8s-resources-notes | QoS criteria and eviction order | kubernetes.io Pod QoS Classes (fetched) |
| k8s-resources-beyond | pod-level resources beta v1.34; in-place resize of pod-level resources beta v1.36 | BUILD.md verified table |
| k8s-kubelet-eviction-notes | soft vs hard (hard = 0s grace), ignores PDB and terminationGracePeriodSeconds, signals | kubernetes.io Node-pressure Eviction (fetched) |
| k8s-configmap-exam | env vars not updated when ConfigMap changes; new container uses new values; volume files updated atomically via symlinks | KIA2 §8.2, §9.4 |
| k8s-secret-* | Base64 is encoding not encryption; etcd unencrypted unless enabled; RBAC; no auto rotation except volume file sync; external tools (Vault) | KIA2 §8.3 |
| k8s-secret-notes | KMS as a way to encrypt etcd secrets | kubernetes.io docs (general; not fetched this session; lowest-confidence mention) |
| k8s-emptydir-* | emptyDir data preserved for Pod's lifetime, across container restarts, shared between containers | KIA2 §9.2 |
| k8s-pv-pvc-* | Immediate vs WaitForFirstConsumer; CSI driver controller + per-node component | KIA2 §10.2 |
| k8s-pv-pvc-exam | zone-affinity rationale for WaitForFirstConsumer | KIA2 §10.2 (the book's table 10.4 explanation; rationale paraphrased, not quoted) |
| k8s-pv-pvc-beyond | VolumeAttributesClass GA v1.34; expansion failure recovery GA v1.34; VolumeGroupSnapshot GA v1.36 | BUILD.md orchestrator check; v1.34 post titles seen |
| k8s-service-clusterip-* | ClusterIP virtual, no route; kube-proxy watches Service/EndpointSlice and writes kernel rules | Poulton ch9 "ClusterIP routing" |
| k8s-nodeport-lb-notes | NodePort range 30000-32767 | KIA2 §11.2 (firewall rule tcp:30000-32767) |
| k8s-nodeport-lb-exam | Cluster vs Local: extra hop, SNAT hides client IP, Local hangs without local pod, healthCheckNodePort, 50/25/25 split | KIA2 §11.2 |
| k8s-endpointslice-beyond | Endpoints deprecated v1.33; multiple Service CIDRs GA v1.33; externalIPs deprecated v1.36, removal planned v1.43 | BUILD.md verified table |
| k8s-endpointslice-notes | EndpointSlice splitting reduces update amplification | BUILD.md leaf summary + kubernetes.io EndpointSlices (general, not fetched) |
| k8s-gateway-* | Gateway API spec only, no default implementation; objects, roles; v1 resources; conditions Accepted/Programmed/ResolvedRefs | Poulton ch8; KIA2 ch13 |
| k8s-gateway-vs-ingress-exam | Ingress NGINX retired 2026-03-24; Gateway API v1.0 GA 2023-10-31 | BUILD.md verified table |
| k8s-dns-ndots-* | resolv.conf with 3 search domains, ndots:5, nameserver = kube-dns ClusterIP | Poulton ch9 |
| k8s-dns-ndots-exam | 4 queries for a name with <5 dots (3 failures); trailing dot / lower ndots | derived from resolv.conf(5) semantics; not in the book |
| k8s-networkpolicy-* | default non-isolated; isolation by policyTypes; additive; both sides; reply traffic; CNI must implement | kubernetes.io Network Policies (fetched) |
| k8s-replicaset-* | owner/dependent, controller:true, GC cascades, --cascade=orphan, template change affects only new Pods, label change removes Pod and RS creates replacement, selector immutable | KIA2 §14.1.1, §14.1.3, §14.2.2, §14.3.3, §14.4.2 |
| k8s-deployment-basics-* | Deployment->RS->Pod chain; scale doesn't create RS; owner re-corrects manual RS scaling | KIA2 §15.1; re-correction is general reconcile behaviour (not from book) |
| k8s-rolling-update-notes / k8s-maxsurge-exam | approved samples; defaults 25%, surge round up, unavailable round down | KIA2 §15.2 table 15.3; kubernetes.io Deployments |
| k8s-rolling-faulty-exam | Progressing=False ProgressDeadlineExceeded after 10 min; no auto rollback; minReadySeconds as airbag | KIA2 §15.2.5 |
| k8s-rollout-undo-exam | undo reverts only template; revisionHistoryLimit default 10; pause blocks rollouts | KIA2 §15.2.4, §15.2.6 |
| k8s-statefulset-* | stable names/PVCs, ordered start, headless Service DNS name, at-most-one on node failure, force delete | KIA2 §16.1.2, §16.1.5, §16.2.2 |
| k8s-job-notes / failure-exam | completions/parallelism default 1; restartPolicy OnFailure|Never; Indexed; backoffLimit default 6 (as observed in book); activeDeadlineSeconds; ttlSecondsAfterFinished | KIA2 §18.1.1-18.1.4 |
| k8s-job-policies-beyond | successPolicy (succeededIndexes/succeededCount), backoffLimitPerIndex+maxFailedIndexes require Indexed; GA v1.33 | kubernetes.io Job docs (field names, partly from general knowledge since fetch truncated); GA per BUILD.md orchestrator check |
| k8s-inplace-resize-beyond | in-place resize beta v1.33, GA v1.35; pod-level resize beta v1.36; resizePolicy | BUILD.md verified table (KEP-1287) |
