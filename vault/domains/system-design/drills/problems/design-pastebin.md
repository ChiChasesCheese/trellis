---
nodes: [problems.foundations.pastebin, storage.object]
tags: [problem]
---
# Drill: Design a pastebin service

Design a service like Pastebin or GitHub Gist: users submit a block of text
(code, logs, config) and get back a short link; anyone with the link can
view it. Pastes can be public, unlisted, or password-protected, can expire,
and can optionally be set to burn after being read once.

**Constraints to state and honor**
- 2,000,000 new pastes/day; paste sizes are long-tailed (most are a few KB,
  a small fraction reach multiple MB).
- Read p99 < 150ms for raw content, < 400ms for a syntax-highlighted view.
- Anonymous pastes capped at 1MB, authenticated at 25MB.

**Grading points**
- Computes the read-to-write ratio from stated assumptions and explains why it is structurally lower than a URL shortener's ([[problems-pastebin-read-write-ratio]]).
- Estimates storage by size tier (not a single blended average) and shows that a small tail of large pastes dominates total bytes ([[problems-pastebin-byte-vs-count-weighted-storage]]).
- Justifies routing small pastes inline into the metadata row versus always using object storage ([[problems-pastebin-inline-vs-object-routing]]).
- Limits content-addressed deduplication to public pastes only and explains the two privacy risks that rule out doing it for private ones ([[problems-pastebin-dedup-privacy-tradeoff]]).
- Sizes the entropy of private/unlisted paste ids against a stated brute-force attack budget, rather than reusing the public short-code scheme ([[problems-pastebin-private-id-entropy]]).
- Explains why an expiry sweeper going down causes wasted storage rather than incorrect serving of expired content ([[problems-pastebin-ttl-sweeper-defense-in-depth]]).
- Identifies that synchronous server-side syntax highlighting is cheap in aggregate but creates a tail-latency problem on large pastes ([[problems-pastebin-highlighting-tail-latency]]).
- Makes burn-after-reading a single atomic conditional operation and explains why its responses must bypass CDN caching ([[problems-pastebin-burn-after-reading-atomicity]]).
- Distinguishes this design's storage-and-payload problem from a URL shortener's cache-the-redirect problem ([[storage-object-vs-filesystem]]).

**Solution**: [[solution-pastebin]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
