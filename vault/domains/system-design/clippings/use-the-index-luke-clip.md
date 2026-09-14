---
title: 'SQL Indexing and Tuning e-Book for developers: Use The Index, Luke covers
  Oracle, MySQL, PostgreSQL, SQL Server, ...'
source: https://use-the-index-luke.com/
published: '2026-01-01'
site: SQLPerfTips
clipped: '2026-08-15'
---

# SQL Indexing and Tuning e-Book for developers: Use The Index, Luke covers Oracle, MySQL, PostgreSQL, SQL Server, ...

A site explaining SQL indexing to developers—no crap about administration.

SQL indexing is the most effective tuning method—yet it is often neglected during development. *Use The Index, Luke* explains SQL indexing from grounds up and doesn’t stop at ORM tools like Hibernate.

*Use The Index, Luke* is the free web-edition of [my book **SQL Performance Explained** (from Є9.95)](https://sql-performance-explained.com/?utm_source=use-the-index-luke.com&utm_campaign=front&utm_medium=web). Be sure to [subscribe my **free newsletter**](https://winand.at/lists).

## SQL Indexing in MySQL, Oracle, SQL Server, etc.

*Use The Index, Luke* presents indexing in a vendor agnostic fashion. Product specific notes are provided like here:

- [Db2 (LUW)]
- *Use The Index, Luke* covers SQL indexing for IBM Db2. Tests were conducted with Db2 for Linux, UNIX and Windows, (LUW) V10.5 through 12.1.
- [MySQL]
- *Use The Index, Luke* covers SQL indexing for MySQL. Tests were conducted with MySQL 5.5 through 26.7.0.
- [Oracle]
- *Use The Index, Luke* covers SQL indexing for the Oracle database. Tests were conducted with Oracle 11g through 26ai (23.26.2).
- [PostgreSQL]
- *Use The Index, Luke* covers SQL indexing for PostgreSQL. Tests were conducted with PostgreSQL 9.0 through 17.
- [SQL Server]
- *Use The Index, Luke* covers SQL indexing for Microsoft SQL Server. Tests were conducted with SQL Server 2008R2 through 2025.

Have more questions about SQL indexing or tuning? No problem—have a look at my training and tuning services at [winand.at](https://winand.at/).

## Table of Contents

1. *[Preface](/sql/preface)* — Why is indexing a development task?
2. *[Anatomy of an Index](/sql/anatomy)* — What does an index look like?
  1. *[The Leaf Nodes](/sql/anatomy/the-leaf-nodes)* — A doubly linked list
  2. *[The B-Tree](/sql/anatomy/the-tree)* — It’s a balanced tree
  3. *[Slow Indexes, Part I](/sql/anatomy/slow-indexes)* — Two ingredients make the index slow
3. *[The Where Clause](/sql/where-clause)* — Indexing to improve search performance
  1. *[The Equals Operator](/sql/where-clause/the-equals-operator)* — Exact key lookup
    1. *[Primary Keys](/sql/where-clause/the-equals-operator/primary-keys)* — Verifying index usage
    2. *[Concatenated Keys](/sql/where-clause/the-equals-operator/concatenated-keys)* — Multi-column indexes
    3. *[Slow Indexes, Part II](/sql/where-clause/the-equals-operator/slow-indexes-part-ii)* — The first ingredient, revisited
  2. *[Functions](/sql/where-clause/functions)* — Using functions in the`where` clause
    1. *[Case-Insensitive Search](/sql/where-clause/functions/case-insensitive-search)* —`UPPER` and`LOWER`
    2. *[User-Defined Functions](/sql/where-clause/functions/user-defined-functions)* — Limitations of function-based indexes
    3. *[Over-Indexing](/sql/where-clause/functions/over-indexing)* — Avoid redundancy
  3. *[Bind Variables](/sql/where-clause/bind-parameters)* — For security and performance
  4. *[Searching for Ranges](/sql/where-clause/searching-for-ranges)* — Beyond equality
    1. *[Greater, Less and `BETWEEN`](/sql/where-clause/searching-for-ranges/greater-less-between-tuning-sql-access-filter-predicates)* — The column order revisited
    2. *[Indexing SQL `LIKE` Filters](/sql/where-clause/searching-for-ranges/like-performance-tuning)* —`LIKE` is not for full-text search
    3. *[Index Combine](/sql/where-clause/searching-for-ranges/index-merge-performance)* — Why not using one index for every column?
  5. *[Partial Indexes](/sql/where-clause/partial-and-filtered-indexes)* — Indexing selected rows
  6. *[`NULL` in the Oracle Database](/sql/where-clause/null)* — An important curiosity
    1. *[`NULL` in Indexes](/sql/where-clause/null/index)* — Every index is a partial index
    2. *[`NOT NULL` Constraints](/sql/where-clause/null/not-null-constraint)* — affect index usage
    3. *[Emulating Partial Indexes](/sql/where-clause/null/partial-index)* — using function-based indexing
  7. *[Obfuscated Conditions](/sql/where-clause/obfuscation)* — Common anti-patterns
    1. *[Dates](/sql/where-clause/obfuscation/dates)* — Pay special attention to`DATE` types
    2. *[Numeric Strings](/sql/where-clause/obfuscation/numeric-strings)* — Don’t mix types
    3. *[Combining Columns](/sql/where-clause/obfuscation/concatenation)* — use redundant`where` clauses
    4. *[Smart Logic](/sql/where-clause/obfuscation/smart-logic)* — The smartest way to make SQL slow
    5. *[Math](/sql/where-clause/obfuscation/math)* — Databases don’t solve equations
4. *[Testing and Scalability](/sql/testing-scalability)* — About hardware
  1. *[Data Volume](/sql/testing-scalability/data-volume)* — Sloppy indexing bites back
  2. *[System Load](/sql/testing-scalability/system-load)* — Production load affects response time
  3. *[Response Time and Throughput](/sql/testing-scalability/response-time-throughput-scaling-horizontal)* — Horizontal scalability
5. *[The Join Operation](/sql/join)* — Not slow, if done right
  1. *[Nested Loops](/sql/join/nested-loops-join-n1-problem)* — About the N+1 selects problem in ORM
  2. *[Hash Join](/sql/join/hash-join-partial-objects)* — Requires an entirely different indexing approach
  3. *[Sort-Merge Join](/sql/join/sort-merge-join)* — Like a zipper on two sorted sets
6. *[Clustering Data](/sql/clustering)* — To reduce IO
  1. *[Index Filter Predicates Intentionally Used](/sql/clustering/index-filter-predicates)* — to tune`LIKE`
  2. *[Index-Only Scan](/sql/clustering/index-only-scan-covering-index)* — Avoiding table access
  3. *[Index-Organized Table](/sql/clustering/index-organized-clustered-index)* — Clustered indexes without tables
7. *[Sorting and Grouping](/sql/sorting-grouping)* — Pipelined`order by` : the third power
  1. *[Indexed Order By](/sql/sorting-grouping/indexed-order-by)* —`where` clause interactions
  2. *[`ASC`/`DESC` and `NULL FIRST`/`LAST`](/sql/sorting-grouping/order-by-asc-desc-nulls-last)* — changing index order
  3. *[Indexed Group By](/sql/sorting-grouping/indexed-group-by)* — Pipelining`group by`
8. *[Partial Results](/sql/partial-results)* — Paging efficiently
  1. *[Selecting Top-N Rows](/sql/partial-results/top-n-queries)* — if you need the first few rows only
  2. *[Fetching The Next Page](/sql/partial-results/fetch-next-page)* — The offset and seek methods compared
  3. *[Window-Functions](/sql/partial-results/window-functions)* — Pagination using analytic queries
9. *[Insert, Delete and Update](/sql/dml)* — Indexing impacts on DML statements
