---
nodes: [security.authn]
url: https://developer.okta.com/blog/2019/10/21/illustrated-guide-to-oauth-and-oidc
tags: [intro, canonical]
---
# An Illustrated Guide to OAuth and OpenID Connect (David Neal, Okta)

The famous illustrated walkthrough that makes the authorization-code flow and
the OAuth-vs-OIDC distinction stick in one read — the "one diagram" the
skeleton asks for, with hand-drawn actors instead of RFC prose.

**Extract on read:**
- OAuth 2.0 grants delegated *authorization* (access token); OIDC adds *authentication* (ID token).
- Authorization code flow + PKCE, actor by actor — the only flow to reach for by default.
- Access tokens are for APIs, ID tokens for the client; conflating them is the classic design error.

%% trellis:begin %%
## Source
[Open the original ↗](https://developer.okta.com/blog/2019/10/21/illustrated-guide-to-oauth-and-oidc)

## Archived copy
![[okta-illustrated-oauth-oidc-clip]]
%% trellis:end %%
