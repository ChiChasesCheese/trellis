---
nodes: [security.authz]
url: https://www.osohq.com/post/why-authorization-is-hard
tags: [canonical]
---
# Why Authorization is Hard

The clearest single article on the shape of the authz problem: enforcement
(where in the code the check goes), decision (what data the check needs and
how it gets there), and modeling (RBAC → ABAC → ReBAC, and when each stops
fitting). Written from having watched many teams build this badly.

**Extract on read:**
- Enforcement points multiply: request-level, resource-level, and field-level checks — and list endpoints turn authorization into a *filter*, i.e. a query problem, not a boolean.
- Decision needs data: pulling authz out into a service means either shipping it your application data or accepting an N+1 of remote checks — the central tension behind Zanzibar-style designs.
- Modeling ladder: roles are cheap and run out fast; attributes are flexible and unauditable; relationships (owner-of, member-of, parent) cover most real requirements.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.osohq.com/post/why-authorization-is-hard)

## Archived copy
![[oso-why-authorization-is-hard-clip]]
%% trellis:end %%
