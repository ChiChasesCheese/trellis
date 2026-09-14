---
nodes:
- security.authz
url: https://owasp.org/API-Security/
tags:
- canonical
- reference
- index
---
# OWASP API Security Top 10

The authoritative checklist of how APIs actually get breached — and its top
entries are all authorization failures, which is exactly the point: authz is
per-object, per-request work, not a gateway checkbox.

**Extract on read:**
- BOLA (broken object-level authorization) is #1: check ownership on every object access, every time.
- Object-level vs function-level authz — RBAC/ABAC decisions must be enforced at both.
- The supporting cast: unrestricted resource consumption (rate limits), broken authentication, and never trusting client-supplied ids.

%% trellis:begin %%
## Source
[Open the original ↗](https://owasp.org/API-Security/)
%% trellis:end %%
