---
nodes: [structure.api]
url: https://web.stanford.edu/~ouster/cgi-bin/book.php
tags: [book, canonical]
---
# A Philosophy of Software Design (John Ousterhout)

The best modern book on designing in-process interfaces: its "deep modules"
thesis — small stable interface, powerful implementation — is the criterion
for every class boundary you draw in a machine-coding round.

**Extract on read:**
- Deep vs shallow modules: an interface should hide far more than it exposes;
  many tiny pass-through classes are a design smell, not decomposition.
- "Define errors out of existence" — redesign contracts so edge cases aren't
  errors (e.g. delete-nonexistent is a no-op).
- Somewhat-general-purpose interfaces outlive their first caller; comments and
  names are part of the abstraction.

%% trellis:begin %%
## Source
[Open the original ↗](https://web.stanford.edu/~ouster/cgi-bin/book.php)
%% trellis:end %%
