---
title: Apache Parquet - Wikipedia
source: https://en.wikipedia.org/wiki/Apache_Parquet
published: '2016-09-11'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Apache Parquet - Wikipedia

# Apache Parquet

| Apache Parquet |  | 
|---|---|
| Release | 13 March 2013 | 
| [Stable release](https://en.wikipedia.org/wiki/Software_release_life_cycle) | 2.12.0    / 28 August 2025<sup>[\[1\]](#cite_note-1)</sup> | 
| Written in | [Java](<https://en.wikipedia.org/wiki/Java_(programming_language)>) (reference implementation)<sup>[\[2\]](#cite_note-2)</sup> | 
| [Operating system](https://en.wikipedia.org/wiki/Operating_system) | [Cross-platform](https://en.wikipedia.org/wiki/Cross-platform) | 
| [Type](https://en.wikipedia.org/wiki/Software_categories#Categorization_approaches) | [Column-oriented DBMS](https://en.wikipedia.org/wiki/Column-oriented_DBMS) | 
| [License](https://en.wikipedia.org/wiki/Software_license) | [Apache License 2.0](https://en.wikipedia.org/wiki/Apache_License_2.0) | 
| Website | [parquet](https://parquet.apache.org) | 
| [Repository](<https://en.wikipedia.org/wiki/Repository_(version_control)>) |  | 

**Apache Parquet** is a [free and open-source](https://en.wikipedia.org/wiki/Free_and_open-source) [column-oriented](https://en.wikipedia.org/wiki/Column-oriented_DBMS) data storage format in the [Apache Hadoop](https://en.wikipedia.org/wiki/Apache_Hadoop) ecosystem inspired by [Google](https://en.wikipedia.org/wiki/Google) Dremel interactive ad-hoc query system for analysis of read-only nested data.<sup>[\[3\]](#cite_note-3)</sup> It is similar to [RCFile](https://en.wikipedia.org/wiki/RCFile) and [ORC](https://en.wikipedia.org/wiki/Apache_ORC), the other columnar-storage file formats in [Hadoop](https://en.wikipedia.org/wiki/Apache_Hadoop), and is compatible with most of the data processing frameworks around [Hadoop](https://en.wikipedia.org/wiki/Hadoop). It provides [data compression](https://en.wikipedia.org/wiki/Data_compression) and [encoding](https://en.wikipedia.org/wiki/Encoding) schemes with enhanced performance to handle complex data in bulk.

## History

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=1)]

The [open-source](https://en.wikipedia.org/wiki/Open-source_software) project to build Apache Parquet began as a joint effort between [Twitter](https://en.wikipedia.org/wiki/Twitter)<sup>[\[4\]](#cite_note-4)</sup> and [Cloudera](https://en.wikipedia.org/wiki/Cloudera)<sup>[\[5\]](#cite_note-5)</sup> using the record shredding and assembly algorithm<sup>[\[6\]](#cite_note-6)</sup> as described in Google's Dremel.<sup>[\[7\]](#cite_note-7)</sup> Parquet was designed as an improvement on the Trevni columnar storage format created by [Doug Cutting](https://en.wikipedia.org/wiki/Doug_Cutting), the creator of Hadoop. The name 'parquet' (lit. 'small compartment') refers to a [style of decorative flooring](https://en.wikipedia.org/wiki/Parquet) and was chosen to "evoke the bottom layer of a database with an interesting layout".<sup>[\[8\]](#cite_note-8)</sup> The first version, Apache Parquet 1.0, was released in July 2013. Since April 27, 2015, Apache Parquet has been a top-level Apache Software Foundation (ASF)-sponsored project.[\[9\]](#cite_note-9)[\[10\]](#cite_note-10)

## Features

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=2)]

Apache Parquet is implemented using the record-shredding and assembly algorithm,<sup>[\[11\]](#cite_note-11)</sup> which accommodates the complex [data structures](https://en.wikipedia.org/wiki/Data_structures) that can be used to store data.<sup>[\[12\]](#cite_note-:1-12)</sup> The values in each column are stored in contiguous memory locations, providing the following benefits:[\[13\]](#cite_note-13)

- Column-wise compression is efficient in storage space
- Encoding and compression techniques specific to the type of data in each column can be used
- Queries that fetch specific column values need not read the entire row, thus improving performance

Apache Parquet is implemented using the [Apache Thrift](https://en.wikipedia.org/wiki/Apache_Thrift) framework, which increases its flexibility; it can work with a number of programming languages like [C++](https://en.wikipedia.org/wiki/C++), [Java](<https://en.wikipedia.org/wiki/Java_(programming_language)>), [Python](<https://en.wikipedia.org/wiki/Python_(programming_language)>), [PHP](https://en.wikipedia.org/wiki/PHP), etc.[\[14\]](#cite_note-14)

As of August 2015,<sup>[\[15\]](#cite_note-15)</sup> Parquet supports the big-data-processing frameworks including [Apache Hive](https://en.wikipedia.org/wiki/Apache_Hive), [Apache Drill](https://en.wikipedia.org/wiki/Apache_Drill), [Apache Impala](https://en.wikipedia.org/wiki/Apache_Impala), Apache Crunch, [Apache Pig](https://en.wikipedia.org/wiki/Apache_Pig), [Cascading](<https://en.wikipedia.org/wiki/Cascading_(software)>), [Presto](<https://en.wikipedia.org/wiki/Presto_(SQL_query_engine)>) and [Apache Spark](https://en.wikipedia.org/wiki/Apache_Spark). It is one of the external data formats used by the [pandas](<https://en.wikipedia.org/wiki/Pandas_(software)>) [Python](<https://en.wikipedia.org/wiki/Python_(programming_language)>) data manipulation and analysis library.

## Compression and encoding

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=3)]

In Parquet, compression is performed column by column, which enables different encoding schemes to be used for text and integer data. This strategy also keeps the door open for newer and better encoding schemes to be implemented as they are invented.

Parquet supports various compression formats: [snappy](<https://en.wikipedia.org/wiki/Snappy_(compression)>), [gzip](https://en.wikipedia.org/wiki/Gzip), [LZO](https://en.wikipedia.org/wiki/Lempel–Ziv–Oberhumer), [brotli](https://en.wikipedia.org/wiki/Brotli), [zstd](https://en.wikipedia.org/wiki/Zstd), and [LZ4](<https://en.wikipedia.org/wiki/LZ4_(compression_algorithm)>).[\[16\]](#cite_note-16)

### Dictionary encoding

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=4)]

Parquet has an automatic [dictionary encoding](https://en.wikipedia.org/wiki/Dictionary_encoding) enabled dynamically for data with a *small* number of unique values (i.e. below 10<sup>5</sup>) that enables significant compression and boosts processing speed.[\[17\]](#cite_note-:0-17)

### Bit packing

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=5)]

Storage of integers is usually done with dedicated 32 or 64 bits per integer. For small integers, packing multiple integers into the same space makes storage more efficient.[\[17\]](#cite_note-:0-17)

### Run-length encoding (RLE)

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=6)]

To optimize storage of multiple occurrences of the same value, [run-length encoding](https://en.wikipedia.org/wiki/Run-length_encoding) is used, which is where a single value is stored once along with the number of occurrences.[\[17\]](#cite_note-:0-17)

Parquet implements a hybrid of bit packing and RLE, in which the encoding switches based on which produces the best compression results. This strategy works well for certain types of integer data and combines well with dictionary encoding.[\[17\]](#cite_note-:0-17)

## Cloud Storage and Data Lakes

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=7)]

Parquet is widely used as the underlying file format in modern cloud-based [data lake](https://en.wikipedia.org/wiki/Data_lake) architectures. Cloud storage systems such as Amazon S3, Azure Data Lake Storage, and Google Cloud Storage commonly store data in Parquet format due to its efficient columnar representation and retrieval capabilities.<sup>[\[18\]](#cite_note-18)</sup> Data lakehouse frameworks—including [Apache Iceberg](https://en.wikipedia.org/wiki/Apache_Iceberg),<sup>[\[19\]](#cite_note-19)</sup> Delta Lake,<sup>[\[20\]](#cite_note-20)</sup> and Apache Hudi <sup>[\[21\]](#cite_note-21)</sup>—build an additional metadata layer on top of Parquet files to support features such as schema evolution, time-travel queries, and [ACID](https://en.wikipedia.org/wiki/ACID)-compliant transactions. In these architectures, Parquet files serve as the immutable storage layer while the table formats manage data versioning and transactional integrity.

## Comparison

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=8)]

Apache Parquet is comparable to [RCFile](https://en.wikipedia.org/wiki/RCFile) and [Optimized Row Columnar (ORC)](https://en.wikipedia.org/wiki/Apache_ORC) file formats — all three fall under the category of columnar data storage within the Hadoop ecosystem. They all have better compression and encoding with improved read performance at the cost of slower writes. In addition to these features, Apache Parquet supports limited [schema evolution](https://en.wikipedia.org/wiki/Schema_evolution),<sup>[\[22\]](#cite_note-ParquetSchemaEvolution2-22)</sup> i.e., the schema can be modified according to the changes in the data. It also provides the ability to add new columns and merge schemas that do not conflict.[\[22\]](#cite_note-ParquetSchemaEvolution2-22)

[Apache Arrow](https://en.wikipedia.org/wiki/Apache_Arrow) is designed as an in-memory complement to on-disk columnar formats like Parquet and ORC. The Arrow and Parquet projects include libraries that allow for reading and writing between the two formats.[\[23\]](#cite_note-ArrowParquetIntegration-23)

## See also

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=9)]

- [Apache Arrow](https://en.wikipedia.org/wiki/Apache_Arrow)
- [Apache Pig](https://en.wikipedia.org/wiki/Apache_Pig)
- [Apache Hive](https://en.wikipedia.org/wiki/Apache_Hive)
- [Apache Impala](https://en.wikipedia.org/wiki/Apache_Impala)
- [Apache Drill](https://en.wikipedia.org/wiki/Apache_Drill)
- [Apache Kudu](https://en.wikipedia.org/wiki/Apache_Kudu)
- [Apache Spark](https://en.wikipedia.org/wiki/Apache_Spark)
- [Apache Thrift](https://en.wikipedia.org/wiki/Apache_Thrift)
- [Trino (SQL query engine)](<https://en.wikipedia.org/wiki/Trino_(SQL_query_engine)>)
- [Presto (SQL query engine)](<https://en.wikipedia.org/wiki/Presto_(SQL_query_engine)>)
- [SQLite](https://en.wikipedia.org/wiki/SQLite) embedded database system
- [DuckDB](https://en.wikipedia.org/wiki/DuckDB) embedded OLAP database with Parquet support

## References

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=10)]

1. [↑](#cite_ref-1)["Apache Parquet Format– Releases"](https://parquet.apache.org/blog/parquet-format/) .*Apache.org* . Retrieved 18 April 2026.
2. [↑](#cite_ref-2)["Parquet-MR source code"](https://github.com/apache/parquet-mr) .*[GitHub](https://en.wikipedia.org/wiki/GitHub)* .[Archived](https://web.archive.org/web/20180611015409/https://github.com/apache/parquet-mr) from the original on 11 June 2018. Retrieved 2 July 2019.
3. [↑](#cite_ref-3) Melnik, Sergey; Gubarev, Andrey; Long, Jing Jing; Romer, Geoffrey; Shivakumar, Shiva; Tolton, Matt; Vassilakis, Theo (2010).["Dremel: interactive analysis of web-scale datasets"](https://dl.acm.org/doi/10.14778/1920841.1920886) .*Proceedings of the VLDB Endowment* .**3** (1–2): 330–339.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.14778/1920841.1920886](https://doi.org/10.14778%2F1920841.1920886) .[ISSN](<https://en.wikipedia.org/wiki/ISSN_(identifier)>)[2150-8097](https://search.worldcat.org/issn/2150-8097) .
4. [↑](#cite_ref-4)["Release Date"](https://blog.twitter.com/2013/announcing-parquet-10-columnar-storage-for-hadoop) .[Archived](https://web.archive.org/web/20161020154829/https://blog.twitter.com/2013/announcing-parquet-10-columnar-storage-for-hadoop) from the original on 2016-10-20. Retrieved 2016-09-12.
5. [↑](#cite_ref-5)["Introducing Parquet: Efficient Columnar Storage for Apache Hadoop - Cloudera Engineering Blog"](https://web.archive.org/web/20130504133255/http://blog.cloudera.com/blog/2013/03/introducing-parquet-columnar-storage-for-apache-hadoop/) . 2013-03-13. Archived from[the original](http://blog.cloudera.com/blog/2013/03/introducing-parquet-columnar-storage-for-apache-hadoop/) on 2013-05-04. Retrieved 2018-10-22.
6. [↑](#cite_ref-6)["Dremel: Interactive Analysis of Web-Scale Datasets"](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) .*research.google* . Retrieved 2025-11-05.
7. [↑](#cite_ref-7)["Motivation"](https://parquet.apache.org/docs/overview/motivation/) .*Apache Parquet* . Retrieved 2025-11-05.
8. [↑](#cite_ref-8)["Chapter I: The birth of Parquet - The Sympathetic Ink Blog"](https://sympathetic.ink/2024/01/24/Chapter-1-The-birth-of-Parquet.html) . 24 January 2024.[Archived](https://web.archive.org/web/20250318044037/https://sympathetic.ink/2024/01/24/Chapter-1-The-birth-of-Parquet.html) from the original on 2025-03-18. Retrieved 2025-07-23.
9. [↑](#cite_ref-9) Yegulalp, Serdar (28 April 2015).["Apache Parquet paves the way for better Hadoop data storage"](http://www.infoworld.com/article/2915565/big-data/apache-parquet-paves-the-way-towards-better-hadoop-data-storage.html) .*InfoWorld* .[Archived](https://web.archive.org/web/20170531130443/http://www.infoworld.com/article/2915565/big-data/apache-parquet-paves-the-way-towards-better-hadoop-data-storage.html) from the original on 31 May 2017. Retrieved 21 May 2017.
10. [↑](#cite_ref-10)["The Apache Software Foundation Announces Apache™ Parquet™ as a Top-Level Project : The Apache Software Foundation Blog"](https://blogs.apache.org/foundation/entry/the_apache_software_foundation_announces75) . 27 April 2015.[Archived](https://web.archive.org/web/20170820074502/https://blogs.apache.org/foundation/entry/the_apache_software_foundation_announces75) from the original on 20 August 2017. Retrieved 21 May 2017.
11. [↑](#cite_ref-11)["The striping and assembly algorithms from the Google-inspired Dremel paper"](https://github.com/julienledem/redelm/wiki/The-striping-and-assembly-algorithms-from-the-Dremel-paper) .*github* .[Archived](https://web.archive.org/web/20201026095824/https://github.com/julienledem/redelm/wiki/The-striping-and-assembly-algorithms-from-the-Dremel-paper) from the original on 26 October 2020. Retrieved 13 November 2017.
12. [↑](#cite_ref-:1_12-0)["Apache Parquet Documentation"](https://web.archive.org/web/20160905094320/http://parquet.apache.org/documentation/latest/) . Archived from[the original](https://parquet.apache.org/documentation/latest/) on 2016-09-05. Retrieved 2016-09-12.
13. [↑](#cite_ref-13)["Apache Parquet Cloudera"](http://www.cloudera.com/documentation/enterprise/5-5-x/topics/cdh_ig_parquet.html) .[Archived](https://web.archive.org/web/20160919220719/http://www.cloudera.com/documentation/enterprise/5-5-x/topics/cdh_ig_parquet.html) from the original on 2016-09-19. Retrieved 2016-09-12.
14. [↑](#cite_ref-14)["Apache Thrift"](https://thrift.apache.org/) .[Archived](https://web.archive.org/web/20210312025614/http://thrift.apache.org/) from the original on 2021-03-12. Retrieved 2016-09-14.
15. [↑](#cite_ref-15)["Supported Frameworks"](https://cwiki.apache.org/confluence/display/Hive/Parquet) .[Archived](https://web.archive.org/web/20150202145641/https://cwiki.apache.org/confluence/display/Hive/Parquet) from the original on 2015-02-02. Retrieved 2016-09-12.
16. [↑](#cite_ref-16)["Parquet Compression"](https://parquet.apache.org/docs/file-format/data-pages/compression/) .*Apache Parquet Documentation* . Apache Software Foundation. 11 March 2024. Retrieved 2 December 2024.
17. [1](#cite_ref-:0_17-0)[2](#cite_ref-:0_17-1)[3](#cite_ref-:0_17-2)[4](#cite_ref-:0_17-3)["Announcing Parquet 1.0: Columnar Storage for Hadoop | Twitter Blogs"](https://blog.twitter.com/2013/announcing-parquet-10-columnar-storage-for-hadoop) .*blog.twitter.com* .[Archived](https://web.archive.org/web/20161020154829/https://blog.twitter.com/2013/announcing-parquet-10-columnar-storage-for-hadoop) from the original on 2016-10-20. Retrieved 2016-09-14.
18. [↑](#cite_ref-18)["Apache Parquet"](https://parquet.apache.org/) .*Apache Parquet* . Retrieved 2025-03-13.
19. [↑](#cite_ref-19)["Apache Iceberg"](https://iceberg.apache.org/) . Retrieved 2025-03-13.
20. [↑](#cite_ref-20)["Delta Lake"](https://delta.io/) . Retrieved 2025-03-13.
21. [↑](#cite_ref-21)["Apache Hudi"](https://hudi.apache.org/) . Retrieved 2025-03-13.
22. [1](#cite_ref-ParquetSchemaEvolution2_22-0)[2](#cite_ref-ParquetSchemaEvolution2_22-1) "All About Parquet Part 04 — Schema Evolution in Parquet". Medium.[https://medium.com/data-engineering-with-dremio/all-about-parquet-part-04-schema-evolution-in-parquet-c2c2b1aa6141](https://medium.com/data-engineering-with-dremio/all-about-parquet-part-04-schema-evolution-in-parquet-c2c2b1aa6141)
23. [↑](#cite_ref-ArrowParquetIntegration_23-0) "Reading and Writing the Apache Parquet Format". Apache Arrow Documentation.[https://arrow.apache.org/docs/python/parquet.html](https://arrow.apache.org/docs/python/parquet.html)

## External links

[
[edit](/w/index.php?title=Apache_Parquet&action=edit§ion=11)]
