---
nodes: [security-cost.request-integrity, security-cost.signed-content]
url: https://www.rfc-editor.org/rfc/rfc9110.html
---
# RFC 9110: HTTP Semantics for Request Integrity

Read the sections on routing, fields, intermediaries, message forwarding, conditional requests, and URI normalization. Extract the protocol boundaries that every signer, proxy, cache, and origin must interpret consistently.

Use the standard as the final authority for [[security-request-integrity-hop-headers]], [[security-request-integrity-trusted-proxy]], and [[security-signed-canonical-input]]. Cryptography cannot repair disagreement about the resource or message being authenticated.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc9110.html)
%% trellis:end %%
