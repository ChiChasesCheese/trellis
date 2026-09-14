---
id: networking-dns-record-types
node: networking.dns
type: qa
---
## Q
A vs CNAME vs ALIAS/ANAME: which do you use at a zone apex pointing to a load balancer's changing IPs, and why?

## A
- **A/AAAA**: name → IP. Breaks when the LB's IPs change.
- **CNAME**: name → another name. Correct for `www`, but **forbidden at the apex** (`example.com`) because the apex must also hold SOA/NS records.
- **ALIAS/ANAME** (provider extension, e.g. Route 53 alias): apex-safe — the DNS provider resolves the target name and serves fresh A records itself.

Answer: ALIAS at the apex, CNAME everywhere else.

## Q zh
A vs CNAME vs ALIAS/ANAME：在区域顶点指向负载均衡器的变化 IP 时，你使用哪一个，为什么？

## A zh
- **A/AAAA**：名称 → IP。当 LB 的 IP 改变时破坏。
- **CNAME**：名称 → 另一个名称。对 `www` 正确，但**在顶点禁止**（`example.com`），因为顶点必须也保有 SOA/NS 记录。
- **ALIAS/ANAME**（提供商扩展，例如 Route 53 alias）：顶点安全 — DNS 提供商解析目标名称并自己提供新鲜的 A 记录。

答案：在顶点使用 ALIAS，其他地方使用 CNAME。
