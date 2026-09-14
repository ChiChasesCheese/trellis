---
nodes: [storage.search]
url: https://nlp.stanford.edu/IR-book/information-retrieval-book.html
tags: [book, canonical]
---
# Introduction to Information Retrieval (Manning, Raghavan, Schütze)

The free canonical textbook behind every search engine — read chapter 1
(inverted index construction and boolean retrieval) and chapter 6 (TF-IDF
scoring) for exactly the depth a design conversation needs.

**Extract on read:**
- Inverted index: dictionary + postings lists; why it inverts the document→terms direction of a B-tree.
- Relevance basics: term frequency × inverse document frequency, vector-space scoring (BM25's lineage).
- Index construction and updating — why search clusters sync from the source of truth in near-real-time batches rather than transactionally.

%% trellis:begin %%
## Source
[Open the original ↗](https://nlp.stanford.edu/IR-book/information-retrieval-book.html)
%% trellis:end %%
