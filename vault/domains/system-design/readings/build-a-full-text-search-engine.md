---
nodes: [storage.search]
url: https://artem.krylysov.com/blog/2020/07/28/lets-build-a-full-text-search-engine/
tags: [canonical]
---
# Let's build a full-text search engine (Artem Krylysov)

Writes a working inverted index in a couple hundred lines, measuring at each
step: linear scan → regex → inverted index, then tokenisation, stopwords, and
stemming. You come away knowing why a search cluster is a separate system from
your database rather than an index on it.

**Extract on read:**
- The inverted index is term → sorted list of document IDs; boolean AND is a merge/intersection of postings lists, not a table scan.
- The analysis chain (lowercase, drop stopwords, stem) is what decides recall — the same chain must run on query and document or nothing matches.
- Index build is a batch pass over documents, which is precisely why the search index lags the source of truth and must be re-fed from it.

%% trellis:begin %%
## Source
[Open the original ↗](https://artem.krylysov.com/blog/2020/07/28/lets-build-a-full-text-search-engine/)

## Archived copy
![[build-a-full-text-search-engine-clip]]
%% trellis:end %%
