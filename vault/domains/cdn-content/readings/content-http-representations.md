---
nodes: [content.negotiation, content.range-compression]
url: https://www.rfc-editor.org/rfc/rfc9110.html
tags: [canonical]
---
# RFC 9110: HTTP Semantics

The normative source for representation metadata, content negotiation, content coding, conditional ranges, `206`, `416`, and `Content-Range`.

**Extract on read:**
- `Content-Type` and `Content-Encoding` describe different layers of a representation.
- Range offsets apply to the selected encoded representation, not arbitrary source bytes.
- `If-Range` prevents clients from combining partial bytes from different versions.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.rfc-editor.org/rfc/rfc9110.html)
%% trellis:end %%
