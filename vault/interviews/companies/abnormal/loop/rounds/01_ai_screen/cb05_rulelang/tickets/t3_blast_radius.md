# RUL-244: Blast radius of a compromised account

When we confirm an account is compromised, the SOC wants to know who else is at risk: people that
account emailed after the compromise time, and who they forwarded it to.

Expose it as `GET /blast-radius?account=<addr>&since=<ISO timestamp>` and as
`python -m rulelang blast-radius <addr> --since <ts>`. The hop limit is a tenant setting,
`[blast_radius] max_hops` (default 2).
