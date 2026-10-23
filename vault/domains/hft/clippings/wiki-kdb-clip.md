---
title: kdb+ - Wikipedia
source: https://en.wikipedia.org/wiki/Kdb%2B
published: '2016-06-08'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# kdb+ - Wikipedia

# kdb+

| kdb+ |  | 
|---|---|
| [Original author](https://en.wikipedia.org/wiki/Programmer) | [Arthur Whitney](<https://en.wikipedia.org/wiki/Arthur_Whitney_(computer_scientist)>) | 
| [Developer](https://en.wikipedia.org/wiki/Programmer) | [KX Systems](https://en.wikipedia.org/wiki/KX_Systems) | 
| Release | 2003 | 
| Written in | [q](<https://en.wikipedia.org/wiki/Q_(programming_language_from_Kx_Systems)>) | 
| [Operating system](https://en.wikipedia.org/wiki/Operating_system) | [Windows](https://en.wikipedia.org/wiki/Microsoft_Windows) ,[macOS](https://en.wikipedia.org/wiki/MacOS) ,[Linux](https://en.wikipedia.org/wiki/Linux) ,[Solaris](https://en.wikipedia.org/wiki/Oracle_Solaris) | 
| [Platform](https://en.wikipedia.org/wiki/Computing_platform) | [IA-32](https://en.wikipedia.org/wiki/IA-32) ,[x86-64](https://en.wikipedia.org/wiki/X86-64) ,[SPARC](https://en.wikipedia.org/wiki/SPARC) | 
| Available in | English | 
| [Type](https://en.wikipedia.org/wiki/Software_categories#Categorization_approaches) | [relational](https://en.wikipedia.org/wiki/Relational_database)[time series database](https://en.wikipedia.org/wiki/Time_series_database) | 
| [License](https://en.wikipedia.org/wiki/Software_license) | [Proprietary](https://en.wikipedia.org/wiki/Proprietary_software) | 
| Website | [kx](https://kx.com/) | 

**kdb+** is a column-based [relational](https://en.wikipedia.org/wiki/Relational_database) [time series database](https://en.wikipedia.org/wiki/Time_series_database) (TSDB) with [in-memory](https://en.wikipedia.org/wiki/In-memory_database) (IMDB) abilities, developed and marketed by [KX Systems](https://en.wikipedia.org/wiki/KX_Systems).<sup>[\[1\]](#cite_note-inside-1)</sup> The [database](https://en.wikipedia.org/wiki/Database) is commonly used in [high-frequency trading](https://en.wikipedia.org/wiki/High-frequency_trading) (HFT) to store, analyze, process, and retrieve large data sets at high speed.<sup>[\[2\]](#cite_note-trading-2)</sup> kdb+ has the ability to handle billions of records and analyzes data within a database.<sup>[\[3\]](#cite_note-forbes-3)</sup> The database is available in [32-bit](https://en.wikipedia.org/wiki/32-bit_computing) and [64-bit](https://en.wikipedia.org/wiki/64-bit_computing) versions for several [operating systems](https://en.wikipedia.org/wiki/Operating_system).<sup>[\[4\]](#cite_note-quant-4)</sup> Financial institutions use kdb+ to analyze [time series](https://en.wikipedia.org/wiki/Time_series) data such as [stock](https://en.wikipedia.org/wiki/Stock_exchange) or [commodity](https://en.wikipedia.org/wiki/Commodity_market) exchange data.<sup>[\[5\]](#cite_note-cluster-5)</sup> The database has also been used for other time-sensitive data applications including [commodity markets](https://en.wikipedia.org/wiki/Commodity_market) such as energy trading, [telecommunications](https://en.wikipedia.org/wiki/Telecommunication), sensor data, log data, machine and [computer network](https://en.wikipedia.org/wiki/Computer_network) usage monitoring<sup>[\[6\]](#cite_note-6)</sup> along with real time analytics in [Formula One](https://en.wikipedia.org/wiki/Formula_One) racing.[\[7\]](#cite_note-7)

## Overview

[
[edit](/w/index.php?title=Kdb%2B&action=edit§ion=1)]

kdb+ is a high-performance [column-store database](https://en.wikipedia.org/wiki/Column-oriented_DBMS) that was designed to process and store large amounts of data. Commonly accessed data is pushed into [random-access memory](https://en.wikipedia.org/wiki/Random-access_memory) (RAM), which is faster to access than data in [disk storage](https://en.wikipedia.org/wiki/Disk_storage). Created with financial institutions in mind, the database was developed as a central repository to store time series data that supports real-time analysis of billions of records.[\[8\]](#cite_note-finance-8)[\[1\]](#cite_note-inside-1)<sup>[\[9\]](#cite_note-itl-9)</sup> kdb+ has the ability to analyze data over time and responds to queries similar to Structured Query Language ([SQL](https://en.wikipedia.org/wiki/SQL)).[\[2\]](#cite_note-trading-2)

Columnar databases return answers to some queries in a more efficient way than row-based database management systems.<sup>[\[5\]](#cite_note-cluster-5)</sup> kdb+ dictionaries, tables and nanosecond time stamps are native data types and are used to store [time series](https://en.wikipedia.org/wiki/Time_series) data.[\[5\]](#cite_note-cluster-5)[\[10\]](#cite_note-wst-10)

At the core of kdb+ is the built-in programming language, [q](<https://en.wikipedia.org/wiki/Q_(programming_language_from_Kx_Systems)>), a concise, expressive query array language, and [dialect](<https://en.wikipedia.org/wiki/Dialect_(computing)>) of the language [APL](<https://en.wikipedia.org/wiki/APL_(programming_language)>).<sup>[\[8\]](#cite_note-finance-8)</sup> Q can manipulate [streaming](<https://en.wikipedia.org/wiki/Stream_(computing)>), [real-time](https://en.wikipedia.org/wiki/Real-time_data), and historical data.<sup>[\[2\]](#cite_note-trading-2)</sup> kdb+ uses q to aggregate and analyze data, perform statistical functions, and join data sets and supports SQL queries.<sup>[\[11\]](#cite_note-markets-11)</sup> The vector language q was built for speed and expressiveness and eliminates most need for [looping structures](<https://en.wikipedia.org/wiki/Loop_(computing)>).<sup>[\[5\]](#cite_note-cluster-5)</sup> kdb+ includes interfaces in [C](<https://en.wikipedia.org/wiki/C_(programming_language)>), [C++](https://en.wikipedia.org/wiki/C++), [Java](<https://en.wikipedia.org/wiki/Java_(programming_language)>), [C#](<https://en.wikipedia.org/wiki/C_Sharp_(programming_language)>), and [Python](<https://en.wikipedia.org/wiki/Python_(programming_language)>).[\[4\]](#cite_note-quant-4)[\[5\]](#cite_note-cluster-5)

## History

[
[edit](/w/index.php?title=Kdb%2B&action=edit§ion=2)]

In 1998, KX released kdb, a database built on the language [K](<https://en.wikipedia.org/wiki/K_(programming_language)>) written by [Arthur Whitney](<https://en.wikipedia.org/wiki/Arthur_Whitney_(computer_scientist)>). In 2003, kdb+ was released as a 64-bit version of kdb. In 2004, the kdb+ tick market database framework was released along with kdb+ taq, a loader for the [New York Stock Exchange](https://en.wikipedia.org/wiki/New_York_Stock_Exchange) (NYSE) taq data. kdb+ was created by Arthur Whitney, building on his prior work with array languages.[\[5\]](#cite_note-cluster-5)

In April 2007, KX announced that it was releasing a version of kdb+ for [Mac OS X](https://en.wikipedia.org/wiki/MacOS). Then, kdb+ was also available on the operating systems [Linux](https://en.wikipedia.org/wiki/Linux), [Windows](https://en.wikipedia.org/wiki/Microsoft_Windows), and [Solaris](https://en.wikipedia.org/wiki/Oracle_Solaris).[\[12\]](#cite_note-mac-12)

In September 2012, version 3.0 was released. It was optimized for Intel's upgraded processors with support for [WebSockets](https://en.wikipedia.org/wiki/WebSocket), and [universally unique identifiers](https://en.wikipedia.org/wiki/Universally_unique_identifier) (UUIDs, termed *globally* unique identifiers (GUID)s in Microsoft software). Intel's [Advanced Vector Extensions](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions) (AVX) and Streaming SIMD Extensions 4 ([SSE4](https://en.wikipedia.org/wiki/SSE4)) 4.2 on the [Sandy Bridge](https://en.wikipedia.org/wiki/Sandy_Bridge) processors of the time allowed for enhanced support of the kdb+ system.<sup>[\[3\]](#cite_note-forbes-3)</sup> In June 2013, version 3.1 was released, with benchmarks up to 8 times faster than older versions.[\[13\]](#cite_note-auto-13)

In March 2020, version 4.0 was released.<sup>[\[14\]](#cite_note-kx-14)</sup> New features included multithreaded primitives, Intel [Optane](https://en.wikipedia.org/wiki/Optane) DC persistent memory support, and [data at rest](https://en.wikipedia.org/wiki/Data_at_rest) encryption.

## References

[
[edit](/w/index.php?title=Kdb%2B&action=edit§ion=3)]

1. [1](#cite_ref-inside_1-0)[2](#cite_ref-inside_1-1) Gutierrez, Daniel (January 19, 2015).["Kdb+ and the Internet of Things/Big Data"](http://insidebigdata.com/2015/01/19/kdb-internet-thingsbig-data/) . Inside Big Data. Retrieved June 8, 2016.
2. [1](#cite_ref-trading_2-0)[2](#cite_ref-trading_2-1)[3](#cite_ref-trading_2-2)["Kx Systems and High Frequency Trading"](https://web.archive.org/web/20181219134322/http://www.thetradingmesh.com/pg/blog/mike/read/5388/kx-systems-and-high-frequency-trading) . The Trading Mesh. June 10, 2011. Archived from[the original](http://www.thetradingmesh.com/pg/blog/mike/read/5388/kx-systems-and-high-frequency-trading) on December 19, 2018. Retrieved June 8, 2016.
3. [1](#cite_ref-forbes_3-0)[2](#cite_ref-forbes_3-1) Groenfeldt, Tom (September 24, 2012).["At Kx Systems Big Data Is Old News"](https://www.forbes.com/sites/tomgroenfeldt/2012/09/24/at-kx-systems-big-data-is-old-news/#1b2e873e7010) .*Forbes* . Retrieved June 8, 2016.
4. [1](#cite_ref-quant_4-0)[2](#cite_ref-quant_4-1) Sbardella, Luca (October 2, 2009).["A first look at kdb+"](https://web.archive.org/web/20190129063946/http://quantmind.com/blog/2009/10/a-first-look-at-kdb) . Quantmind. Archived from[the original](http://quantmind.com/blog/2009/10/a-first-look-at-kdb) on January 29, 2019. Retrieved June 8, 2016.
5. [1](#cite_ref-cluster_5-0)[2](#cite_ref-cluster_5-1)[3](#cite_ref-cluster_5-2)[4](#cite_ref-cluster_5-3)[5](#cite_ref-cluster_5-4)[6](#cite_ref-cluster_5-5) Eadline, Douglas (September 9, 2014).["Working Down the Column: The Kdb+ Community"](http://www.clustermonkey.net/Deep-Dive/working-down-the-column-the-kdb-community.html) . Cluster Monkey. Retrieved June 8, 2016.
6. [↑](#cite_ref-6) Stamper, Jason (September 4, 2014). "Kx Systems readies faster database in push beyond financial services".*451 Research* .
7. [↑](#cite_ref-7)["Williams Racing Announce KX as an Official Supplier"](https://www.williamsf1.com/posts/ea41af4f-c0b5-413c-a8d5-b7065586ff0e/williams-racing-announce-kx-as-an-official-supplier) .*Williams Racing* . Retrieved 2023-01-24.
8. [1](#cite_ref-finance_8-0)[2](#cite_ref-finance_8-1) Golovtchenko, Victor (January 1, 2016).["First Derivatives Boosts its KDB+ Software Business with New Acquisition"](http://www.financemagnates.com/institutional-forex/technology/first-derivatives-boosts-its-kdb-software-business-with-new-acquisition/) . Finance Magnates. Retrieved June 8, 2016.
9. [↑](#cite_ref-itl_9-0)["Kdb+"](https://web.archive.org/web/20191114222227/http://itl-g.com/solutions/kdb/) . Itl Group. Archived from[the original](http://itl-g.com/solutions/kdb/) on November 14, 2019. Retrieved June 8, 2016.
10. [↑](#cite_ref-wst_10-0) Crosman, Penny (September 14, 2009).["Kx Offers Nanosecond Timestamps in Updated Database"](https://web.archive.org/web/20170816234948/http://www.wallstreetandtech.com/latency/kx-offers-nanosecond-timestamps-in-updated-database/d/d-id/1262409) . Information Week. Archived from[the original](http://www.wallstreetandtech.com/latency/kx-offers-nanosecond-timestamps-in-updated-database/d/d-id/1262409) on August 16, 2017. Retrieved June 8, 2016.
11. [↑](#cite_ref-markets_11-0) Marlin, Steve (June 19, 2014).["Wall Street Firms Extend 'Big Data; Capabilities"](http://marketsmedia.com/wall-street-firms-extend-big-data-capabilities/) . Markets Media. Retrieved June 8, 2016.
12. [↑](#cite_ref-mac_12-0) Cohen, Peter (April 17, 2007).["Kdb+ financial database comes to Mac OS X"](http://www.macworld.com/article/1057391/kx.html) . Macworld. Retrieved June 8, 2016.
13. [↑](#cite_ref-auto_13-0)["Kx's kdb+ claims up to 8x faster than any previous STAC M3 benchmarks"](https://web.archive.org/web/20181219090914/http://www.automatedtrader.net/news/at/142863/kxs-kdb+-claims-up-to-8x-faster-than-any-previous-stac-m3--benchmarks) . Automated Trader. June 11, 2013. Archived from[the original](http://www.automatedtrader.net/news/at/142863/kxs-kdb+-claims-up-to-8x-faster-than-any-previous-stac-m3--benchmarks) on December 19, 2018. Retrieved June 8, 2016.
14. [↑](#cite_ref-kx_14-0) Garland, Simon (March 23, 2020).["Kdb+ version 4.0 – faster, more secure"](https://kx.com/blog/kdb-version-4-0-faster-more-secure/) . Retrieved December 4, 2021.

## External links

[
[edit](/w/index.php?title=Kdb%2B&action=edit§ion=4)]
