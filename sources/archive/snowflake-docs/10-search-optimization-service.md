---
title: Search optimization service¶
corpus: snowflake-docs
section: 10-search-optimization-service
level: 1
locator: https://docs.snowflake.com/en/user-guide/search-optimization-service
license: free-online
fetched: '2026-09-13'
---

# Search optimization service[¶](#search-optimization-service)

The search optimization service can significantly improve the performance of certain types of lookup and analytical
queries. An extensive set of filtering predicates are supported (see [Identifying queries that can benefit from search optimization](/user-guide/search-optimization/queries-that-benefit)).

Note

To start with a tutorial that compares execution time with and without search optimization, see
[Getting Started with Search Optimization](https://quickstarts.snowflake.com/guide/getting_started_with_search_optimization/index.html).

The search optimization service aims to significantly improve the performance of certain types of queries on tables, including:

- 
Selective point lookup queries on tables. A point lookup query returns only one or a small number of distinct rows. Use case examples include: 
  - Business users who need fast response times for critical dashboards with highly selective filters.
  - Data scientists who are exploring large data volumes and looking for specific subsets of data.
  - Data applications retrieving a small set of results based on an extensive set of filtering predicates.
 For more information, see [Speeding up point lookup queries with search optimization](/user-guide/search-optimization/point-lookup-queries) .
- 
Character data (text) and IP address searches executed with the [SEARCH](/sql-reference/functions/search) and[SEARCH_IP](/sql-reference/functions/search_ip) functions. For more information, see[Speeding up text queries with search optimization](/user-guide/search-optimization/text-queries) .
- 
Substring and regular expression searches (for example, [LIKE](/sql-reference/functions/like) ,[ILIKE](/sql-reference/functions/ilike) ,[RLIKE](/sql-reference/functions/rlike) , and so on). For more information, see[Speeding up substring and regular expression queries with search optimization](/user-guide/search-optimization/substring-queries) .
- 
Queries on elements in [VARIANT, OBJECT, and ARRAY](/sql-reference/data-types-semistructured) (semi-structured)
columns that use the following types of predicates:
  - Equality predicates.
  - IN predicates.
  - Predicates that use [ARRAY_CONTAINS](/sql-reference/functions/array_contains) .
  - Predicates that use [ARRAYS_OVERLAP](/sql-reference/functions/arrays_overlap) .
  - Predicates that use full-text search with [SEARCH](/sql-reference/functions/search) .
  - Substring and regular expression predicates.
  - Predicates that check for NULL values.
 For more information, see [Speeding up queries of semi-structured data with search optimization](/user-guide/search-optimization/semi-structured-queries) .
- 
Queries on elements in [structured ARRAY, OBJECT, and MAP](/sql-reference/data-types-structured) (structured)
columns that use the following types of predicates:
  - Equality predicates.
  - IN predicates.
  - Substring predicates (on STRING fields).
 For more information, see [Speeding up queries of structured data with search optimization](/user-guide/search-optimization/structured-queries) .
- 
Queries that use selected geospatial functions with [GEOGRAPHY](/sql-reference/data-types-geospatial) values.
For more information, see[Speeding up geospatial queries with search optimization](/user-guide/search-optimization/geospatial-queries) .

Once you identify the queries that can benefit from the search optimization service, you can
[enable search optimization](/user-guide/search-optimization/enabling) for the columns and tables used in those queries.

The search optimization service is generally transparent to users. Queries work the same as they do without search
optimization; some are just faster. However, search optimization does have effects on certain other table operations. For
more information, see [Working with search-optimized tables](/user-guide/search-optimization/working-with-tables).

## How the search optimization service works[¶](#how-the-search-optimization-service-works)

To improve performance of search queries, the search optimization service creates and maintains a persistent data
structure called a *search access path*. The search access path keeps track of which values of the table’s columns might
be found in each of its [micro-partitions](/user-guide/tables-clustering-micropartitions#label-what-are-micropartitions), allowing some micro-partitions to be
skipped when scanning the table.

A maintenance service is responsible for creating and maintaining the search access path:

- 
When you enable search optimization, the maintenance service creates and populates the search access path with the data needed to perform the lookups. Building the search access path can take significant time, depending on the size of the table. The maintenance service works in the background and does not block any operations on the table. Queries are not accelerated until the search access path has been fully built.
- 
When data in the table is updated (for example, by loading new data sets or through DML operations), the maintenance service automatically updates the search access path to reflect the changes to the data. If queries are run while the search access path is still being updated, queries might run more slowly, but will still return correct results.

The progress of each table’s maintenance service appears in the `search_optimization_progress` column in the
output of [SHOW TABLES](/sql-reference/sql/show-tables). Before you measure the performance improvement of search
optimization on a newly-optimized table, make sure this column shows that the table has been fully optimized.

Search access path maintenance is transparent. You don’t need to create a virtual warehouse for running the
maintenance service. However, there is a cost for the storage and compute resources of maintenance. For more details
on costs, see [Search optimization cost estimation and management](/user-guide/search-optimization/cost-estimation).

## Other options for optimizing query performance[¶](#other-options-for-optimizing-query-performance)

The search optimization service is one of several ways to optimize query performance. The following list shows other techniques:

- Query acceleration
- Creating one or more materialized views (clustered or unclustered)
- Clustering a table

For more information, see [Optimizing query performance](/user-guide/performance-query-options).

## Examples[¶](#examples)

Start by creating a table with data:

Add the SEARCH OPTIMIZATION property to the table using [ALTER TABLE](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction):

The following queries can use the search optimization service:

The following query can use the search optimization service because the implicit cast is on the constant, not the column:

The following can’t use the search optimization service because the cast is on the table’s column:

An [IN](/sql-reference/functions/in) clause is supported by the search optimization service:

If predicates are individually supported by the search optimization service, then they can be joined by the conjunction
`AND` and still be supported by the search optimization service:

DELETE and UPDATE (and MERGE) can also use the search optimization service:
