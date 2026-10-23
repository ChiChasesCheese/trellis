---
title: Hash table - Wikipedia
source: https://en.wikipedia.org/wiki/Hash_table
author: Authority control databases GND
published: '2001-09-27'
site: Wikimedia Foundation, Inc.
clipped: '2026-10-23'
---

# Hash table - Wikipedia

# Hash table

| Hash table |  | 
|---|---|
| [Type](https://en.wikipedia.org/wiki/List_of_data_structures) | Unordered [associative array](https://en.wikipedia.org/wiki/Associative_array) | 
| Invented | 1953 | 

| [Time complexity](https://en.wikipedia.org/wiki/Time_complexity) in[big O notation](https://en.wikipedia.org/wiki/Big_O_notation) |  |  |  | 
|---|---|---|---|
| Operation | **Average** | **Worst case** |  | 
| Search | Θ(1) | O( *n* )<sup>[\[a\]](#cite_note-2)</sup> |  | 
| Insert | Θ(1) | O( *n* ) |  | 
| Delete | Θ(1) | O( *n* ) |  | 
| [Space complexity](https://en.wikipedia.org/wiki/Space_complexity) |  |  |  | 
| Space | Θ( *n* )<sup>[\[2\]](#cite_note-Cormen_et_al-3)</sup> | O( *n* ) |  | 

In [computer science](https://en.wikipedia.org/wiki/Computer_science), a **hash table** is a [data structure](https://en.wikipedia.org/wiki/Data_structure) that implements an [associative array](https://en.wikipedia.org/wiki/Associative_array), also called a **dictionary** or simply **map**; an associative array is an [abstract data type](https://en.wikipedia.org/wiki/Abstract_data_type) that maps [keys](https://en.wikipedia.org/wiki/Unique_key) to [values](<https://en.wikipedia.org/wiki/Value_(computer_science)>).<sup>[\[3\]](#cite_note-ms-4)</sup> A hash table uses a [hash function](https://en.wikipedia.org/wiki/Hash_function) to compute an *index*, also called a *hash code*, into an array of *buckets* or *slots*, from which the desired value can be found. During lookup, the key is hashed and the resulting hash indicates where the corresponding value is stored. A map implemented by a hash table is called a **hash map**.

Most hash table designs employ an [imperfect hash function](https://en.wikipedia.org/wiki/Perfect_hash_function). [Hash collisions](https://en.wikipedia.org/wiki/Hash_collision), where the hash function generates the same index for more than one key, therefore typically must be accommodated in some way. Common strategies to handle hash collisions include separate chaining, which stores multiple elements in the same slot using linked lists, and open addressing, which searches for the next available slot according to a probing sequence.[\[4\]](#cite_note-knuth-5)

In a well-dimensioned hash table, the average time complexity for each lookup is independent of the number of elements stored in the table. Many hash table designs also allow arbitrary insertions and deletions of [key–value pairs](https://en.wikipedia.org/wiki/Name–value_pair), at [amortized](https://en.wikipedia.org/wiki/Amortized_analysis) constant average cost per operation.[\[5\]](#cite_note-leiser-6)[\[4\]](#cite_note-knuth-5)<sup>: 513–558</sup> [\[6\]](#cite_note-cormen-7)

Hashing is an example of a [space–time tradeoff](https://en.wikipedia.org/wiki/Space–time_tradeoff). If [memory](https://en.wikipedia.org/wiki/Computer_memory) is infinite, the entire key can be used directly as an index to locate its value with a single memory access. On the other hand, if infinite time is available, values can be stored without regard for their keys, and a [binary search](https://en.wikipedia.org/wiki/Binary_search) or [linear search](https://en.wikipedia.org/wiki/Linear_search) can be used to retrieve the element.[\[7\]](#cite_note-algo1rob-8)<sup>: 458</sup> 

In many situations, hash tables turn out to be on average more efficient than [search trees](https://en.wikipedia.org/wiki/Search_tree) or any other [table](<https://en.wikipedia.org/wiki/Table_(computing)>) lookup structure. For this reason, they are widely used in many kinds of computer [software](https://en.wikipedia.org/wiki/Software), particularly for [associative arrays](https://en.wikipedia.org/wiki/Associative_array), [database indexing](https://en.wikipedia.org/wiki/Database_index), [caches](<https://en.wikipedia.org/wiki/Cache_(computing)>), and [sets](<https://en.wikipedia.org/wiki/Set_(abstract_data_type)>).<sup>[\[8\]](#cite_note-9)</sup> Many programming languages provide built-in hash table structures, such as Python’s dictionaries, Java’s HashMap, C++’s unordered_map, and Go maps, which abstract the complexity of hashing from the programmer.[\[9\]](#cite_note-10)

## History

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=1)]

The idea of hashing arose independently in different places. In January 1953, [Hans Peter Luhn](https://en.wikipedia.org/wiki/Hans_Peter_Luhn) wrote an internal [IBM](https://en.wikipedia.org/wiki/IBM) memorandum that used hashing with chaining.  The first example of [open addressing](https://en.wikipedia.org/wiki/Open_addressing) was proposed by A. D. Linh, building on Luhn's memorandum.[\[4\]](#cite_note-knuth-5)<sup>: 547</sup>  Around the same time, [Gene Amdahl](https://en.wikipedia.org/wiki/Gene_Amdahl), [Elaine M. McGraw](https://en.wikipedia.org/wiki/Elaine_M._McGraw), [Nathaniel Rochester](<https://en.wikipedia.org/wiki/Nathaniel_Rochester_(computer_scientist)>), and [Arthur Samuel](<https://en.wikipedia.org/wiki/Arthur_Samuel_(computer_scientist)>) of [IBM Research](https://en.wikipedia.org/wiki/IBM_Research) implemented hashing for the [IBM 701](https://en.wikipedia.org/wiki/IBM_701) [assembler](https://en.wikipedia.org/wiki/Assembly_language#Assembler).[\[10\]](#cite_note-Konheim-11)<sup>: 124</sup>  Open addressing with linear probing is credited to Amdahl, although [Andrey Ershov](https://en.wikipedia.org/wiki/Andrey_Ershov) independently had the same idea.[\[10\]](#cite_note-Konheim-11)<sup>: 124–125</sup>  The term "open addressing" was coined by [W. Wesley Peterson](https://en.wikipedia.org/wiki/W._Wesley_Peterson) in his article which discusses the problem of search in large files.[\[11\]](#cite_note-hashhist-12)<sup>: 15</sup> 

The first published work on hashing with chaining is credited to [Arnold Dumey](https://en.wikipedia.org/wiki/Arnold_Dumey), who discussed the idea of using remainder modulo a prime as a hash function.[\[11\]](#cite_note-hashhist-12)<sup>: 15</sup>  The word "hashing" was first published in an article by Robert Morris.[\[10\]](#cite_note-Konheim-11)<sup>: 126</sup>  A [theoretical analysis](https://en.wikipedia.org/wiki/Analysis_of_algorithms) of linear probing was submitted originally by Konheim and Weiss.[\[11\]](#cite_note-hashhist-12)<sup>: 15</sup> 

## Overview

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=2)]

An [associative array](https://en.wikipedia.org/wiki/Associative_array) stores a [set](<https://en.wikipedia.org/wiki/Set_(abstract_data_type)>) of (key, value) pairs and allows insertion, deletion, and lookup (search), with the constraint of [unique keys](https://en.wikipedia.org/wiki/Unique_key). In the hash table implementation of associative arrays, an array  of length  is partially filled with  elements, where . A key  **is hashed using a hash function  to compute an index location  in the hash table, where . At this index, both the key and its associated value are stored. Storing the key alongside the value ensures that lookups can verify the key at the index to retrieve the correct value, even in the presence of collisions. Under reasonable assumptions, hash tables have better** [time complexity](https://en.wikipedia.org/wiki/Time_complexity) bounds on search, delete, and insert operations in comparison to [self-balancing binary search trees](https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree).[\[11\]](#cite_note-hashhist-12)<sup>: 1</sup> 

### Load factor

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=3)]

The efficiency of a hash table depends on the *load factor* (), defined as the ratio of the number of stored elements to the number of available slots, with lower load factors generally yielding faster operations.<sup>[\[12\]](#cite_note-13)</sup> Load factor is a critical statistic of a hash table, and is defined as follows:<sup>[\[2\]](#cite_note-Cormen_et_al-3)</sup>
where

- is the number of key-value pairs in the hash table.
- is the number of buckets.

The performance of the hash table deteriorates in relation to the load factor .[\[11\]](#cite_note-hashhist-12)<sup>: 2</sup>   In the limit of large  and , each bucket statistically has a [Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution) with expectation  for an ideally random [hash function](https://en.wikipedia.org/wiki/Hash_function).

The implementation of a hash table typically ensures that the load factor  remains below a certain constant, . This helps maintain good performance. Therefore, a common approach is to resize or "rehash" the hash table whenever the load factor  reaches . Similarly the table may also be resized if the load factor drops below .[\[13\]](#cite_note-cornell08-14)

#### Load factor for open addressing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=4)]

With open addressing, each slot of the bucket array holds exactly one item. Therefore an open-addressed hash table cannot have a load factor greater than 1.[\[14\]](#cite_note-plank-15)

The performance of open addressing becomes very bad when the load factor approaches 1.<sup>[\[13\]](#cite_note-cornell08-14)</sup> Therefore a hash table that uses open addressing *must* be resized or *rehashed* if the load factor  approaches 1.[\[13\]](#cite_note-cornell08-14)

With open addressing, acceptable figures of max load factor  should range around 0.6 to 0.75.[\[15\]](#cite_note-16)[\[16\]](#cite_note-owo03-17)<sup>: 110</sup> 

#### Load factor for separate chaining

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=5)]

With separate chaining hash tables, each slot of the bucket array stores a pointer to a list or array of data.[\[14\]](#cite_note-plank-15)

Separate chaining hash tables suffer gradually declining performance as the load factor grows, unlike the sharply decreasing performance of open addressing hash tables around . There is not a fixed point with respect to load factor beyond which resizing is absolutely needed.[\[13\]](#cite_note-cornell08-14)

With separate chaining, the value of  that gives best performance is typically between 1 and 3.[\[13\]](#cite_note-cornell08-14)

## Hash function

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=6)]

A [hash function](https://en.wikipedia.org/wiki/Hash_function)  maps the universe  of keys to indices or slots within the table, that is,  for . The conventional implementations of hash functions are based on the *integer universe assumption* that all elements of the table stem from the universe , where the [bit length](https://en.wikipedia.org/wiki/Bit_length) of  is confined within the [word size](<https://en.wikipedia.org/wiki/Word_(computer_architecture)>) of a [computer architecture](https://en.wikipedia.org/wiki/Computer_architecture).[\[11\]](#cite_note-hashhist-12)<sup>: 2</sup> 

A hash function  is said to be [perfect](https://en.wikipedia.org/wiki/Perfect_hash_function) for a given set  if it is [injective](https://en.wikipedia.org/wiki/Injective_function) on , that is, if each element  maps to a different value in .[\[17\]](#cite_note-Yi06-18)<sup>[\[18\]](#cite_note-CHD-19)</sup> A perfect hash function can be created if all the keys are known ahead of time.[\[17\]](#cite_note-Yi06-18)

### Integer universe assumption

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=7)]

The schemes of hashing used in *integer universe assumption* include hashing by division, hashing by multiplication, [universal hashing](https://en.wikipedia.org/wiki/Universal_hashing), [dynamic perfect hashing](https://en.wikipedia.org/wiki/Dynamic_perfect_hashing), and [static perfect hashing](https://en.wikipedia.org/wiki/Static_Hashing).[\[11\]](#cite_note-hashhist-12)<sup>: 2</sup>  However, hashing by division is the commonly used scheme.[\[19\]](#cite_note-cormenalgo01-20)<sup>: 264</sup> [\[16\]](#cite_note-owo03-17)<sup>: 110</sup> 

#### Hashing by division

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=8)]

The scheme in hashing by division is as follows:[\[11\]](#cite_note-hashhist-12)<sup>: 2</sup> 
where  is the hash value of  and  is the size of the table.

#### Hashing by multiplication

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=9)]

The scheme in hashing by multiplication is as follows:[\[11\]](#cite_note-hashhist-12)<sup>: 2–3</sup> 
Where  is a non-integer [real-valued constant](https://en.wikipedia.org/wiki/Real_number) and  is the size of the table. An advantage of the hashing by multiplication is that the  is not critical.[\[11\]](#cite_note-hashhist-12)<sup>: 2–3</sup>  Although any value  produces a hash function, [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth) suggests using the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio).[\[11\]](#cite_note-hashhist-12)<sup>: 3</sup> 

#### String hashing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=10)]

Commonly a string is used as a key to the hash function. The third edition of *[The C++ Programming Language](https://en.wikipedia.org/wiki/The_C++_Programming_Language)* describes a simple hash function in which an unsigned integer that is initially zero is repeatedly left shifted one bit and then xor'ed with the integer value of the next character.  This hash value is then taken modulo the table size.<sup>[\[20\]](#cite_note-21)</sup> If the left shift is not circular, then the string length should be at least eight bits less than the size of the unsigned integer in bits.  Another common way to hash a string to an integer is with a  [polynomial rolling hash function](https://en.wikipedia.org/wiki/Rolling_hash).

### Choosing a hash function

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=11)]

[Uniform distribution](<https://en.wikipedia.org/wiki/Uniform_distribution_(discrete)>) of the hash values is a fundamental requirement of a hash function. A non-uniform distribution increases the number of collisions and the cost of resolving them. Uniformity is sometimes difficult to ensure by design, but may be evaluated empirically using statistical tests, e.g., a [Pearson's chi-squared test](https://en.wikipedia.org/wiki/Pearson's_chi-squared_test#Discrete_uniform_distribution) for discrete uniform distributions.[\[21\]](#cite_note-chernoff-22)[\[22\]](#cite_note-plackett-23)

The distribution needs to be uniform only for table sizes that occur in the application. In particular, if one uses dynamic resizing with exact doubling and halving of the table size, then the hash function needs to be uniform only when the size is a [power of two](https://en.wikipedia.org/wiki/Power_of_two). Here the index can be computed as some range of bits of the hash function. On the other hand, some hashing algorithms prefer to have the size be a [prime number](https://en.wikipedia.org/wiki/Prime_number).[\[23\]](#cite_note-:0-24)

For [open addressing](https://en.wikipedia.org/wiki/Open_addressing) schemes, the hash function should also avoid *[runs](https://en.wikipedia.org/wiki/Primary_clustering)*, the mapping of two or more keys to consecutive slots. Such runs may cause the lookup cost to skyrocket, even if the load factor is low and collisions are infrequent. The popular multiplicative hash is claimed to have particularly poor run behavior.[\[23\]](#cite_note-:0-24)[\[4\]](#cite_note-knuth-5)

[K-independent hashing](https://en.wikipedia.org/wiki/K-independent_hashing) offers a way to prove a certain hash function does not have bad keysets for a given type of hashtable. A number of K-independence results are known for collision resolution schemes such as linear probing and cuckoo hashing. Since K-independence can prove a hash function works, one can then focus on finding the fastest possible such hash function.[\[24\]](#cite_note-25)

## Collision resolution

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=12)]

A search algorithm that uses hashing consists of two parts. The first part is computing a [hash function](https://en.wikipedia.org/wiki/Hash_function) which transforms the search key into an [array index](https://en.wikipedia.org/wiki/Array_index). The ideal case is such that no two search keys hash to the same array index. However, this is not always the case and impossible to guarantee for unseen given data.[\[4\]](#cite_note-knuth-5)<sup>: 515</sup>  Hence the second part of the algorithm is collision resolution. The two common methods for collision resolution are separate chaining and open addressing.[\[7\]](#cite_note-algo1rob-8)<sup>: 458</sup> 

### Separate chaining

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=13)]

In separate chaining, the process involves building a [linked list](https://en.wikipedia.org/wiki/Linked_list) of [key–value pairs](https://en.wikipedia.org/wiki/Key–value_pair) for each search array index. The collided items are chained together through a single linked list, which can be traversed during lookup of a specific key.[\[7\]](#cite_note-algo1rob-8)<sup>: 464</sup>  Collision resolution through chaining with linked lists is a common method of implementation of hash tables. Let  be the hash table,  be an element , and  be its key. The operations involved are as follows:[\[19\]](#cite_note-cormenalgo01-20)<sup>: 258</sup> 

Chained-Hash-Insert(*T*, *x*)
  *insert* *x* *at the head of linked list* *T*[*h*(*k*)]
Chained-Hash-Search(*T*, *k*)
  *search for an element with key* *k* *in linked list* *T*[*h*(*k*)]
Chained-Hash-Delete(*T*, *x*)
  *delete* *x* *from the linked list* *T*[*h*(*k*)]

If the element is comparable either [numerically](https://en.wikipedia.org/wiki/Sequence#Analysis) or [lexically](https://en.wikipedia.org/wiki/Lexicographic_order), and inserted into the list by maintaining the [total order](https://en.wikipedia.org/wiki/Total_order), it results in faster termination of unsuccessful searches.[\[4\]](#cite_note-knuth-5)<sup>: 520–521</sup> 

#### Other data structures for separate chaining

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=14)]

If the keys are [ordered](https://en.wikipedia.org/wiki/Total_order), it could be efficient to use "[self-organizing](https://en.wikipedia.org/wiki/Optimal_binary_search_tree)" concepts such as using a [self-balancing binary search tree](https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree), through which the [theoretical worst case](https://en.wikipedia.org/wiki/Worst-case_complexity) could be brought down to , although it introduces additional complexities.[\[4\]](#cite_note-knuth-5)<sup>: 521</sup> 

In [dynamic perfect hashing](https://en.wikipedia.org/wiki/Dynamic_perfect_hashing), two-level hash tables are used to reduce the look-up complexity to be a guaranteed  in the worst case. In this technique, the buckets of  entries are organized as [perfect hash tables](https://en.wikipedia.org/wiki/Perfect_hash_function) with  slots providing constant worst-case lookup time, and low amortized time for insertion.<sup>[\[25\]](#cite_note-26)</sup> A study shows array-based separate chaining to be 97% more performant when compared to the standard linked list method under heavy load.[\[26\]](#cite_note-nick05-27)<sup>: 99</sup> 

Techniques such as using [fusion tree](https://en.wikipedia.org/wiki/Fusion_tree) for each bucket also result in constant time for all operations with high probability.[\[27\]](#cite_note-28)

#### Caching and locality of reference

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=15)]

Linked lists in separate chaining may not be [cache-conscious](https://en.wikipedia.org/wiki/Cache-oblivious_algorithm) due to [spatial locality](https://en.wikipedia.org/wiki/Spatial_locality)—[locality of reference](https://en.wikipedia.org/wiki/Locality_of_reference)—when the nodes of the linked list are scattered across memory, thus the list traversal during insert and search may entail [CPU cache](https://en.wikipedia.org/wiki/CPU_cache) inefficiencies.[\[26\]](#cite_note-nick05-27)<sup>: 91</sup> 

In [cache-conscious variants](https://en.wikipedia.org/wiki/Cache-oblivious_algorithm) of collision resolution through separate chaining, a [dynamic array](https://en.wikipedia.org/wiki/Dynamic_array) found to be more [cache-friendly](https://en.wikipedia.org/wiki/CPU_cache) is used in the place where a linked list or self-balancing binary search tree is usually deployed, since the [contiguous allocation](<https://en.wikipedia.org/wiki/Memory_management_(operating_systems)#Single_contiguous_allocation>) pattern of  the array could be exploited by [hardware-cache prefetchers](https://en.wikipedia.org/wiki/Cache_prefetching)—such as [translation lookaside buffers](https://en.wikipedia.org/wiki/Translation_lookaside_buffer)—resulting in reduced access time and memory consumption.[\[28\]](#cite_note-29)[\[29\]](#cite_note-30)[\[30\]](#cite_note-31)

### Open addressing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=16)]

[Open addressing](https://en.wikipedia.org/wiki/Open_addressing) is another collision resolution technique in which every entry record is stored in the bucket array itself, and the hash resolution is performed through **probing**. When a new entry has to be inserted, the buckets are examined, starting with the hashed-to slot and proceeding in some *probe sequence*, until an unoccupied slot is found. When searching for an entry, the buckets are scanned in the same sequence,  until either the target record is found, or an unused array slot is found, which indicates an unsuccessful search.[\[31\]](#cite_note-tenenbaum90-32)

Well-known probe sequences include:

- [Linear probing](https://en.wikipedia.org/wiki/Linear_probing) , in which the interval between probes is fixed (usually 1).<sup>[\[32\]](#cite_note-Cuckoo-33)</sup>
- [Quadratic probing](https://en.wikipedia.org/wiki/Quadratic_probing) , in which the interval between probes is increased by adding the successive outputs of a quadratic polynomial to the value given by the original hash computation.<sup>[\[33\]](#cite_note-clrs-34)</sup><sup>: 272</sup> 
- [Double hashing](https://en.wikipedia.org/wiki/Double_hashing) , in which the interval between probes is computed by a secondary hash function.<sup>[\[33\]](#cite_note-clrs-34)</sup><sup>: 272–273</sup> 

The performance of open addressing may be slower compared to separate chaining since the probe sequence increases when the load factor  approaches 1.[\[13\]](#cite_note-cornell08-14)[\[26\]](#cite_note-nick05-27)<sup>: 93</sup>  The probing results in an [infinite loop](https://en.wikipedia.org/wiki/Infinite_loop) if the load factor reaches 1, in the case of a completely filled table.[\[7\]](#cite_note-algo1rob-8)<sup>: 471</sup>  The [average cost](https://en.wikipedia.org/wiki/Average-case_complexity) of linear probing depends on the hash function's ability to [distribute](https://en.wikipedia.org/wiki/Probability_distribution) the elements [uniformly](https://en.wikipedia.org/wiki/Continuous_uniform_distribution) throughout the table to avoid [runs](https://en.wikipedia.org/wiki/Primary_clustering), since formation of runs would result in increased search time.[\[7\]](#cite_note-algo1rob-8)<sup>: 472</sup> 

#### Caching and locality of reference

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=17)]

Since the slots are located in successive locations, linear probing could lead to better utilization of [CPU cache](https://en.wikipedia.org/wiki/CPU_cache) due to [locality of references](https://en.wikipedia.org/wiki/Locality_of_reference) resulting in reduced [memory latency](https://en.wikipedia.org/wiki/Memory_latency).[\[32\]](#cite_note-Cuckoo-33)

#### Other collision resolution techniques based on open addressing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=18)]

##### Coalesced hashing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=19)]

[Coalesced hashing](https://en.wikipedia.org/wiki/Coalesced_hashing) is a hybrid of both separate chaining and open addressing.[\[34\]](#cite_note-chen87-35)<sup>: 6–8</sup>  When an element being inserted is hashed to an occupied bucket, the element is instead inserted into the largest-indexed available slot in the hash table, and the original bucket is linked to that slot using a next pointer.[\[34\]](#cite_note-chen87-35)<sup>: 8</sup>  Coalesced hashing is ideally suited for [fixed memory allocation](https://en.wikipedia.org/wiki/Memory_pool).[\[34\]](#cite_note-chen87-35)<sup>: 4</sup> 

##### Cuckoo hashing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=20)]

[Cuckoo hashing](https://en.wikipedia.org/wiki/Cuckoo_hashing) is a form of open addressing collision resolution which guarantees  worst-case lookup complexity and constant amortized time for insertions. Collisions are resolved through maintaining two hash tables, each having its own hashing function, and collided slot gets replaced with the given item, and the preoccupied element of the slot gets displaced into the other hash table. The process continues until every key has its own spot in the empty buckets of the tables; if the procedure enters into [infinite loop](https://en.wikipedia.org/wiki/Infinite_loop)—which is identified through maintaining a threshold loop counter—both hash tables get rehashed with newer hash functions and the procedure continues.[\[35\]](#cite_note-36)<sup>: 124–125</sup> 

##### Hopscotch hashing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=21)]

[Hopscotch hashing](https://en.wikipedia.org/wiki/Hopscotch_hashing) is an open addressing based algorithm which combines the elements of [cuckoo hashing](https://en.wikipedia.org/wiki/Cuckoo_hashing), [linear probing](https://en.wikipedia.org/wiki/Linear_probing) and separate chaining through the notion of a *neighbourhood* of buckets—the subsequent buckets around any given occupied bucket, also called a "virtual" bucket.[\[36\]](#cite_note-nir08-37)<sup>: 351–352</sup>  The algorithm is designed to deliver better performance when the load factor of the hash table grows beyond 90%; it also provides high throughput in [concurrent settings](https://en.wikipedia.org/wiki/Concurrent_computing), thus is well suited for implementing resizable [concurrent hash tables](https://en.wikipedia.org/wiki/Concurrent_hash_table).[\[36\]](#cite_note-nir08-37)<sup>: 350</sup>  The neighbourhood characteristic of hopscotch hashing guarantees the property that, the cost of finding the desired item from any given buckets within the neighbourhood is very close to the cost of finding it in the bucket itself; the algorithm attempts to be an item into its neighbourhood—with a possible cost involved in displacing other items.[\[36\]](#cite_note-nir08-37)<sup>: 352</sup> 

Each bucket within the hash table includes an additional "hop-information"—an *H*-bit [bit array](https://en.wikipedia.org/wiki/Bit_array) for indicating the [relative distance](https://en.wikipedia.org/wiki/Euclidean_distance#One_dimension) of the item which was originally hashed into the current virtual bucket within *H* − 1 entries.[\[36\]](#cite_note-nir08-37)<sup>: 352</sup>  Let  and  be the key to be inserted and bucket to which the key is hashed into respectively; several cases are involved in the insertion procedure such that the neighbourhood property of the algorithm is vowed:[\[36\]](#cite_note-nir08-37)<sup>: 352–353</sup>  if  is empty, the element is inserted, and the leftmost bit of bitmap is [set](https://en.wikipedia.org/wiki/Bitwise_operation) to 1; if not empty, linear probing is used for finding an empty slot in the table, the bitmap of the bucket gets updated followed by the insertion; if the empty slot is not within the range of the *neighbourhood,* i.e. *H* − 1, subsequent swap and hop-info bit array manipulation of each bucket is performed in accordance with its neighbourhood [invariant properties](<https://en.wikipedia.org/wiki/Invariant_(mathematics)>).[\[36\]](#cite_note-nir08-37)<sup>: 353</sup> 

##### Robin Hood hashing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=22)]

Robin Hood hashing is an open addressing based collision resolution algorithm; the collisions are resolved through favouring the displacement of the element that is farthest—or longest *probe sequence length* (PSL)—from its "home location" i.e. the bucket to which the item was hashed into.[\[37\]](#cite_note-waterloo86-38)<sup>: 12</sup>  It is named after [Robin Hood](https://en.wikipedia.org/wiki/Robin_Hood), a mythical [heroic outlaw](https://en.wikipedia.org/wiki/Heroic_outlaw) who stole from the rich to give to the poor.

Although Robin Hood hashing does not change the [theoretical search cost](https://en.wikipedia.org/wiki/Computational_complexity_theory), it significantly affects the [variance](https://en.wikipedia.org/wiki/Variance) of the [distribution](https://en.wikipedia.org/wiki/Probability_distribution) of the items on the buckets,[\[38\]](#cite_note-39)<sup>: 2</sup>  i.e. dealing with [long run](https://en.wikipedia.org/wiki/Primary_clustering) formation in the hash table.<sup>[\[39\]](#cite_note-cornell14-40)</sup> Each node within the hash table that uses Robin Hood hashing should be augmented to store an extra PSL value.<sup>[\[40\]](#cite_note-41)</sup> Let  be the key to be inserted,  be the (incremental) PSL length of ,  be the hash table and  be the index, the insertion procedure is as follows:[\[37\]](#cite_note-waterloo86-38)<sup>: 12–13</sup> [\[41\]](#cite_note-indiana88-42)<sup>: 5</sup> 

- If : the iteration goes into the next bucket without attempting an external probe.
- If : insert the item into the bucket ; swap with —let it be ; continue the probe from the th bucket to insert ; repeat the procedure until every element is inserted.

## Dynamic resizing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=23)]

Repeated insertions cause the number of entries in a hash table to grow, which consequently increases the load factor; to maintain the amortized  performance of the lookup and insertion operations, a hash table is dynamically resized and the items of the tables are *rehashed* into the buckets of the new hash table.<sup>[\[13\]](#cite_note-cornell08-14)</sup> The items cannot simply be copied over into the same indices since the hash function depends on the table size. If a hash table becomes "too empty" after deleting some elements, resizing may be performed to avoid excessive [memory usage](https://en.wikipedia.org/wiki/Memory_footprint).[\[42\]](#cite_note-43)

### Resizing by moving all entries

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=24)]

Generally, a new hash table with a size double that of the original hash table gets [allocated](https://en.wikipedia.org/wiki/Dynamic_memory_allocation) privately and every item in the original hash table gets moved to the newly allocated one by computing the hash values of the items followed by the insertion operation. Rehashing is simple, but computationally expensive.[\[43\]](#cite_note-44)<sup>: 478–479</sup> 

### Alternatives to all-at-once rehashing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=25)]

Some hash table implementations, notably in [real-time systems](https://en.wikipedia.org/wiki/Real-time_system), cannot pay the price of enlarging the hash table all at once, because it may interrupt time-critical operations. If one cannot avoid dynamic resizing, a solution is to perform the resizing gradually to avoid storage blip—typically at 50% of new table's size—during rehashing and to avoid [memory fragmentation](<https://en.wikipedia.org/wiki/Fragmentation_(computing)>) that triggers [heap compaction](https://en.wikipedia.org/wiki/Mark–compact_algorithm) due to deallocation of large [memory blocks](<https://en.wikipedia.org/wiki/Page_(computer_memory)>) caused by the old hash table.[\[44\]](#cite_note-scott03-45)<sup>: 2–3</sup>  In such case, the rehashing operation is done incrementally through extending prior memory block allocated for the old hash table such that the buckets of the hash table remain unaltered. A common approach for amortized rehashing involves maintaining two hash functions  and . The process of rehashing a bucket's items in accordance with the new hash function is termed as *cleaning*, which is implemented through [command pattern](https://en.wikipedia.org/wiki/Command_pattern) by encapsulating the operations such as ,  and  through a  [wrapper](https://en.wikipedia.org/wiki/Wrapper_function) such that each element in the bucket gets rehashed and its procedure involve as follows:[\[44\]](#cite_note-scott03-45)<sup>: 3</sup> 

- Clean bucket.
- Clean bucket.
- The *command* gets executed.

#### Linear hashing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=26)]

[Linear hashing](https://en.wikipedia.org/wiki/Linear_hashing) is an implementation of the hash table which enables dynamic growths or shrinks of the table one bucket at a time.[\[45\]](#cite_note-46)

## Performance

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=27)]

The performance of a hash table is dependent on the hash function's ability in generating [quasi-random numbers](https://en.wikipedia.org/wiki/Low-discrepancy_sequence) () for entries in the hash table where ,  and  denotes the key, number of buckets and the hash function such that . If the hash function generates the same  for distinct keys (), this results in a collision. The constant time complexity () of various operations in a hash table is presupposed on the condition that the hash function doesn't generate colliding indices; thus, the performance of the hash table is [directly proportional](<https://en.wikipedia.org/wiki/Proportionality_(mathematics)#Direct_proportionality>) to the chosen hash function's ability to [disperse](https://en.wikipedia.org/wiki/Statistical_dispersion) the indices.[\[46\]](#cite_note-dijk10-47)<sup>: 1</sup>  However, construction of such a hash function is [practically infeasible](https://en.wikipedia.org/wiki/NP-hardness), that being so, implementations depend on [case-specific](https://en.wikipedia.org/wiki/Use_case) [collision resolution techniques](#Collision_resolution) in achieving higher performance.[\[46\]](#cite_note-dijk10-47)<sup>: 2</sup> 

The best performance is obtained in the case that the hash function distributes the elements of the universe uniformly, and the elements stored in the table are drawn at random from the universe. In this case, in hashing with chaining, the expected time for a successful search is , and the expected time for an unsuccessful search is .[\[47\]](#cite_note-48)

## Applications

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=28)]

### Associative arrays

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=29)]

Hash tables are commonly used to implement many types of in-memory tables. They are used to implement [associative arrays](https://en.wikipedia.org/wiki/Associative_array).[\[33\]](#cite_note-clrs-34)

### Database indexing

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=30)]

Hash tables may also be used as [disk](https://en.wikipedia.org/wiki/Disk_drive)-based data structures and [database indices](<https://en.wikipedia.org/wiki/Index_(database)>) (such as in [dbm](<https://en.wikipedia.org/wiki/DBM_(computing)>)) although [B-trees](https://en.wikipedia.org/wiki/B-tree) are more popular in these applications.[\[48\]](#cite_note-49)

### Caches

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=31)]

Hash tables can be used to implement [caches](<https://en.wikipedia.org/wiki/Cache_(computing)>), auxiliary data tables that are used to speed up the access to data that is primarily stored in slower media. In this application, hash collisions can be handled by discarding one of the two colliding entries—usually erasing the old item that is currently stored in the table and overwriting it with the new item, so every item in the table has a unique hash value.[\[49\]](#cite_note-50)[\[50\]](#cite_note-51)

### Sets

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=32)]

Hash tables can be used in the implementation of the [set data structure](https://en.wikipedia.org/wiki/Set_data_structure), which can store unique values without any particular order; sets are typically used in testing the membership of a value in a collection, rather than element retrieval.<sup>[\[51\]](#cite_note-52)</sup> Hash tables are used as sets by omitting the stored value for each key and merely tracking whether the key is present.[\[11\]](#cite_note-hashhist-12)<sup>: 1</sup> 

### Transposition table

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=33)]

[Transposition tables](https://en.wikipedia.org/wiki/Transposition_table), which store previously seen positions and associated evaluations in a search tree, such as a game tree, are typically implemented as hash tables.

## Implementations

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=34)]

Many programming languages provide hash table functionality, either as built-in associative arrays or as [standard library](https://en.wikipedia.org/wiki/Standard_library) modules.

- In [JavaScript](https://en.wikipedia.org/wiki/JavaScript) , an "object" is a mutable collection of key–value pairs (called "properties"), where each key is either a string or a guaranteed-unique "symbol"; any other value, when used as a key, is first[coerced](https://en.wikipedia.org/wiki/Type_conversion) to a string. Aside from the seven "primitive" data types, every value in JavaScript is an object.<sup>[\[52\]](#cite_note-53)</sup> ECMAScript 2015 also added the`Map` data structure, which accepts arbitrary values as keys.<sup>[\[53\]](#cite_note-54)</sup>
- [C++11](https://en.wikipedia.org/wiki/C++11) includes[unordered_map](<https://en.wikipedia.org/wiki/Unordered_map_(C++)>)
[arbitrary types](<https://en.wikipedia.org/wiki/Template_(C++)>) .<sup>[\[54\]](#cite_note-55)</sup>
- [Go](<https://en.wikipedia.org/wiki/Go_(programming_language)>) 's built-in`map` implements a map type in the form of a[type](https://en.wikipedia.org/wiki/Primitive_data_type) , which is often (but not guaranteed to be) a hash table.<sup>[\[55\]](#cite_note-56)</sup>
- [Java](<https://en.wikipedia.org/wiki/Java_(programming_language)>) programming language includes the`HashSet` ,`HashMap` ,`LinkedHashSet` , and`LinkedHashMap`[generic](https://en.wikipedia.org/wiki/Generics_in_Java) collections.<sup>[\[56\]](#cite_note-57)</sup>
- [Python](<https://en.wikipedia.org/wiki/Python_(programming_language)>) 's built-in`dict` implements a hash table in the form of a[type](https://en.wikipedia.org/wiki/Primitive_data_type) .<sup>[\[57\]](#cite_note-58)</sup>
- [Ruby](<https://en.wikipedia.org/wiki/Ruby_(programming_language)>) 's built-in`Hash` uses the open addressing model from Ruby 2.4 onwards.<sup>[\[58\]](#cite_note-59)</sup>
- [Rust](<https://en.wikipedia.org/wiki/Rust_(programming_language)>) programming language includes`HashMap` ,`HashSet` as part of the Rust Standard Library.<sup>[\[59\]](#cite_note-60)</sup>
- The [.NET](https://en.wikipedia.org/wiki/.NET) standard library includes`HashSet` and`Dictionary` ,<sup>[\[60\]](#cite_note-61)</sup><sup>[\[61\]](#cite_note-62)</sup> so it can be used from languages such as[C#](<https://en.wikipedia.org/wiki/C_Sharp_(programming_language)>) and[VB.NET](https://en.wikipedia.org/wiki/VB.NET) .<sup>[\[62\]](#cite_note-63)</sup>

## See also

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=35)]

## Notes

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=36)]

## References

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=37)]

1. [↑](#cite_ref-Farach-Colton_2024_1-0) Martin Farach-Colton; Andrew Krapivin; William Kuszmaul.*Optimal Bounds for Open Addressing Without Reordering* . 2024 IEEE 65th Annual Symposium on Foundations of Computer Science (FOCS).[arXiv](<https://en.wikipedia.org/wiki/ArXiv_(identifier)>) :[2501.02305](https://arxiv.org/abs/2501.02305) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/FOCS61266.2024.00045](https://doi.org/10.1109%2FFOCS61266.2024.00045) .
2. [1](#cite_ref-Cormen_et_al_3-0)[2](#cite_ref-Cormen_et_al_3-1)[Cormen, Thomas H.](https://en.wikipedia.org/wiki/Thomas_H._Cormen) ;[Leiserson, Charles E.](https://en.wikipedia.org/wiki/Charles_E._Leiserson) ;[Rivest, Ronald L.](https://en.wikipedia.org/wiki/Ronald_L._Rivest) ;[Stein, Clifford](https://en.wikipedia.org/wiki/Clifford_Stein) (2009).[*Introduction to Algorithms*](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) (3rd ed.). Massachusetts Institute of Technology. pp. 253–280.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-262-03384-8](https://en.wikipedia.org/wiki/Special:BookSources/978-0-262-03384-8) .
3. [↑](#cite_ref-ms_4-0)[Mehlhorn, Kurt](https://en.wikipedia.org/wiki/Kurt_Mehlhorn) ;[Sanders, Peter](<https://en.wikipedia.org/wiki/Peter_Sanders_(computer_scientist)>) (2008).["Hash Tables and Associative Arrays"](https://people.mpi-inf.mpg.de/~mehlhorn/ftp/Toolbox/HashTables.pdf) (PDF).*Algorithms and Data Structures* . Springer. pp. 81–98.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-540-77978-0_4](https://doi.org/10.1007%2F978-3-540-77978-0_4) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-540-77977-3](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-77977-3) .
4. [1](#cite_ref-knuth_5-0)[2](#cite_ref-knuth_5-1)[3](#cite_ref-knuth_5-2)[4](#cite_ref-knuth_5-3)[5](#cite_ref-knuth_5-4)[6](#cite_ref-knuth_5-5)[7](#cite_ref-knuth_5-6)[Knuth, Donald E.](https://en.wikipedia.org/wiki/Donald_E._Knuth) (April 24, 1998).[*The Art of Computer Programming: Volume 3: Sorting and Searching*](https://dl.acm.org/doi/10.5555/280635) (2nd ed.).[Addison-Wesley Professional](https://en.wikipedia.org/wiki/Addison-Wesley_Professional) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-201-89685-5](https://en.wikipedia.org/wiki/Special:BookSources/978-0-201-89685-5) .
5. [↑](#cite_ref-leiser_6-0)[Leiserson, Charles E.](https://en.wikipedia.org/wiki/Charles_E._Leiserson) (Fall 2005).["Lecture 13: Amortized Algorithms, Table Doubling, Potential Method"](https://videolectures.net/mit6046jf05_leiserson_lec13/) .*course MIT 6.046J/18.410J Introduction to Algorithms* .[Archived](https://web.archive.org/web/20090807022046/http://videolectures.net/mit6046jf05_leiserson_lec13/) from the original on August 7, 2009.
6. [↑](#cite_ref-cormen_7-0)[Cormen, Thomas H.](https://en.wikipedia.org/wiki/Thomas_H._Cormen) ;[Leiserson, Charles E.](https://en.wikipedia.org/wiki/Charles_E._Leiserson) ;[Rivest, Ronald L.](https://en.wikipedia.org/wiki/Ronald_L._Rivest) ;[Stein, Clifford](https://en.wikipedia.org/wiki/Clifford_Stein) (2001). "Chapter 11: Hash Tables".[*Introduction to Algorithms*](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) (2nd ed.). MIT Press and McGraw-Hill. pp.[221](https://archive.org/details/introductiontoal00corm_691/page/n243) –252.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-262-53196-2](https://en.wikipedia.org/wiki/Special:BookSources/978-0-262-53196-2) .
7. [1](#cite_ref-algo1rob_8-0)[2](#cite_ref-algo1rob_8-1)[3](#cite_ref-algo1rob_8-2)[4](#cite_ref-algo1rob_8-3)[5](#cite_ref-algo1rob_8-4)[Sedgewick, Robert](<https://en.wikipedia.org/wiki/Robert_Sedgewick_(computer_scientist)>) ; Wayne, Kevin (2011).[*Algorithms*](https://algs4.cs.princeton.edu/) . Vol. 1 (4 ed.). Addison-Wesley Professional – via[Princeton University](https://en.wikipedia.org/wiki/Princeton_University) , Department of Computer Science.
8. [↑](#cite_ref-9) Silberschatz, A.; Korth, H. F.; Sudarshan, S. (2020).*Database System Concepts* (7th ed.).[McGraw-Hill](https://en.wikipedia.org/wiki/McGraw-Hill) .
9. [↑](#cite_ref-10) Goodrich, M. T.; Tamassia, R.; Goldwasser, M. H. (2014).*Data Structures and Algorithms in Java* (6th ed.).[Wiley](<https://en.wikipedia.org/wiki/Wiley_(publisher)>) .
10. [1](#cite_ref-Konheim_11-0)[2](#cite_ref-Konheim_11-1)[3](#cite_ref-Konheim_11-2) Konheim, Alan G. (2010).*Hashing in Computer Science* .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1002/9780470630617](https://doi.org/10.1002%2F9780470630617) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-470-34473-6](https://en.wikipedia.org/wiki/Special:BookSources/978-0-470-34473-6) .
11. [1](#cite_ref-hashhist_12-0)[2](#cite_ref-hashhist_12-1)[3](#cite_ref-hashhist_12-2)[4](#cite_ref-hashhist_12-3)[5](#cite_ref-hashhist_12-4)[6](#cite_ref-hashhist_12-5)[7](#cite_ref-hashhist_12-6)[8](#cite_ref-hashhist_12-7)[9](#cite_ref-hashhist_12-8)[10](#cite_ref-hashhist_12-9)[11](#cite_ref-hashhist_12-10)[12](#cite_ref-hashhist_12-11) Mehta, Dinesh P.; Mehta, Dinesh P.; Sahni, Sartaj, eds. (2004).*Handbook of Data Structures and Applications* .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1201/9781420035179](https://doi.org/10.1201%2F9781420035179) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-429-14701-2](https://en.wikipedia.org/wiki/Special:BookSources/978-0-429-14701-2) .
12. [↑](#cite_ref-13) Cormen, T. H.; Leiserson, C. E.;[Rivest, R. L.](https://en.wikipedia.org/wiki/Ronald_Rivest) ; Stein, C. (2009).*Introduction to Algorithms* (3rd ed.).[MIT Press](https://en.wikipedia.org/wiki/MIT_Press) .
13. [1](#cite_ref-cornell08_14-0)[2](#cite_ref-cornell08_14-1)[3](#cite_ref-cornell08_14-2)[4](#cite_ref-cornell08_14-3)[5](#cite_ref-cornell08_14-4)[6](#cite_ref-cornell08_14-5)[7](#cite_ref-cornell08_14-6) Mayers, Andrew (2008).["CS 312: Hash tables and amortized analysis"](https://www.cs.cornell.edu/courses/cs312/2008sp/lectures/lec20.html) .[Cornell University](https://en.wikipedia.org/wiki/Cornell_University) , Department of Computer Science.[Archived](https://web.archive.org/web/20210426052033/http://www.cs.cornell.edu/courses/cs312/2008sp/lectures/lec20.html) from the original on April 26, 2021. Retrieved October 26, 2021 – via cs.cornell.edu.
14. [1](#cite_ref-plank_15-0)[2](#cite_ref-plank_15-1) James S. Plank and Brad Vander Zanden.["CS140 Lecture notes -- Hashing"](https://web.eecs.utk.edu/~bvanderz/teaching/cs140Sp15/Notes/Hashing/) .
15. [↑](#cite_ref-16) Maurer, W. D.; Lewis, T. G. (March 1975). "Hash Table Methods".*ACM Computing Surveys* .**7** (1): 5–19.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/356643.356645](https://doi.org/10.1145%2F356643.356645) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[17874775](https://api.semanticscholar.org/CorpusID:17874775) .
16. [1](#cite_ref-owo03_17-0)[2](#cite_ref-owo03_17-1) Owolabi, Olumide (February 2003). "Empirical studies of some hashing functions".*Information and Software Technology* .**45** (2): 109–112.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1016/S0950-5849(02)00174-X](https://doi.org/10.1016%2FS0950-5849%2802%2900174-X) .
17. [1](#cite_ref-Yi06_18-0)[2](#cite_ref-Yi06_18-1) Lu, Yi; Prabhakar, Balaji; Bonomi, Flavio (2006).*Perfect Hashing for Network Applications* . 2006 IEEE International Symposium on Information Theory. pp. 2774–2778.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/ISIT.2006.261567](https://doi.org/10.1109%2FISIT.2006.261567) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[1-4244-0505-X](https://en.wikipedia.org/wiki/Special:BookSources/1-4244-0505-X) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[1494710](https://api.semanticscholar.org/CorpusID:1494710) .
18. [↑](#cite_ref-CHD_19-0) Belazzougui, Djamal; Botelho, Fabiano C.; Dietzfelbinger, Martin (2009).["Hash, displace, and compress"](https://cmph.sourceforge.net/papers/esa09.pdf) (PDF).*Algorithms—ESA 2009: 17th Annual European Symposium, Copenhagen, Denmark, September 7–9, 2009, Proceedings* .[Lecture Notes in Computer Science](https://en.wikipedia.org/wiki/Lecture_Notes_in_Computer_Science) . Vol. 5757. Berlin: Springer. pp. 682–693.[CiteSeerX](<https://en.wikipedia.org/wiki/CiteSeerX_(identifier)>)[10.1.1.568.130](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.568.130) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-642-04128-0_61](https://doi.org/10.1007%2F978-3-642-04128-0_61) .[MR](<https://en.wikipedia.org/wiki/MR_(identifier)>)[2557794](https://mathscinet.ams.org/mathscinet-getitem?mr=2557794) .`{{`[cite conference](https://en.wikipedia.org/wiki/Template:Cite_conference) }}
: Cite uses deprecated parameter`|citeseerx=` ([help](https://en.wikipedia.org/wiki/Help:CS1_errors#deprecated_params) )
19. [1](#cite_ref-cormenalgo01_20-0)[2](#cite_ref-cormenalgo01_20-1)[Cormen, Thomas H.](https://en.wikipedia.org/wiki/Thomas_H._Cormen) ;[Leiserson, Charles E.](https://en.wikipedia.org/wiki/Charles_E._Leiserson) ;[Rivest, Ronald L.](https://en.wikipedia.org/wiki/Ronald_L._Rivest) ;[Stein, Clifford](https://en.wikipedia.org/wiki/Clifford_Stein) (2001). "Chapter 11: Hash Tables".[*Introduction to Algorithms*](https://en.wikipedia.org/wiki/Introduction_to_Algorithms) (2nd ed.).[Massachusetts Institute of Technology](https://en.wikipedia.org/wiki/Massachusetts_Institute_of_Technology) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-262-53196-2](https://en.wikipedia.org/wiki/Special:BookSources/978-0-262-53196-2) .
20. [↑](#cite_ref-21) Stroustrup, Bjarne (1997).*The C++ Programming Language Third Edition* . Reading Massachusetts: Addison-Wesley. p. 503.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[0-201-88954-4](https://en.wikipedia.org/wiki/Special:BookSources/0-201-88954-4) .
21. [↑](#cite_ref-chernoff_22-0)[Pearson, Karl](https://en.wikipedia.org/wiki/Karl_Pearson) (1900).["On the criterion that a given system of deviations from the probable in the case of a correlated system of variables is such that it can be reasonably supposed to have arisen from random sampling"](https://zenodo.org/record/1430618) .*Philosophical Magazine* . Series 5.**50** (302): 157–175.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1080/14786440009463897](https://doi.org/10.1080%2F14786440009463897) .
22. [↑](#cite_ref-plackett_23-0)[Plackett, Robin](https://en.wikipedia.org/wiki/Robin_Plackett) (1983). "Karl Pearson and the Chi-Squared Test".*International Statistical Review* .**51** (1): 59–72.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.2307/1402731](https://doi.org/10.2307%2F1402731) .[JSTOR](<https://en.wikipedia.org/wiki/JSTOR_(identifier)>)[1402731](https://www.jstor.org/stable/1402731) .
23. [1](#cite_ref-:0_24-0)[2](#cite_ref-:0_24-1) Wang, Thomas (March 1997).["Prime Double Hash Table"](https://web.archive.org/web/19990903133921/http://www.concentric.net/~Ttwang/tech/primehash.htm) . Archived from[the original](https://www.concentric.net/~Ttwang/tech/primehash.htm) on September 3, 1999. Retrieved May 10, 2015.
24. [↑](#cite_ref-25) Wegman, Mark N.; Carter, J.Lawrence (June 1981).["New hash functions and their use in authentication and set equality"](https://doi.org/10.1016%2F0022-0000%2881%2990033-7) .*Journal of Computer and System Sciences* .**22** (3): 265–279.[Bibcode](<https://en.wikipedia.org/wiki/Bibcode_(identifier)>) :[1981JCoSS..22..265W](https://ui.adsabs.harvard.edu/abs/1981JCoSS..22..265W) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1016/0022-0000(81)90033-7](https://doi.org/10.1016%2F0022-0000%2881%2990033-7) .
25. [↑](#cite_ref-26) Demaine, Erik; Lind, Jeff (Spring 2003).["Lecture 2"](https://courses.csail.mit.edu/6.897/spring03/scribe_notes/L2/lecture2.pdf) (PDF).*6.897: Advanced Data Structures. MIT Computer Science and Artificial Intelligence Laboratory* .[Archived](https://web.archive.org/web/20100615203901/http://courses.csail.mit.edu/6.897/spring03/scribe_notes/L2/lecture2.pdf) (PDF) from the original on June 15, 2010. Retrieved June 30, 2008.
26. [1](#cite_ref-nick05_27-0)[2](#cite_ref-nick05_27-1)[3](#cite_ref-nick05_27-2) Culpepper, J. Shane; Moffat, Alistair (2005). "Enhanced Byte Codes with Restricted Prefix Properties".*String Processing and Information Retrieval* . Lecture Notes in Computer Science. Vol. 3772. pp. 1–12.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/11575832_1](https://doi.org/10.1007%2F11575832_1) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-540-29740-6](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-29740-6) .
27. [↑](#cite_ref-28)[Willard, Dan E.](https://en.wikipedia.org/wiki/Dan_Willard) (2000). "Examining computational geometry, van Emde Boas trees, and hashing from the perspective of the fusion tree".*[SIAM Journal on Computing](https://en.wikipedia.org/wiki/SIAM_Journal_on_Computing)* .**29** (3): 1030–1049.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1137/S0097539797322425](https://doi.org/10.1137%2FS0097539797322425) .[MR](<https://en.wikipedia.org/wiki/MR_(identifier)>)[1740562](https://mathscinet.ams.org/mathscinet-getitem?mr=1740562) ..
28. [↑](#cite_ref-29) Askitis, Nikolas; Sinha, Ranjan (October 2010). "Engineering scalable, cache and space efficient tries for strings".*The VLDB Journal* .**19** (5): 633–660.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/s00778-010-0183-9](https://doi.org/10.1007%2Fs00778-010-0183-9) .
29. [↑](#cite_ref-30) Askitis, Nikolas; Zobel, Justin (October 2005). "Cache-conscious Collision Resolution in String Hash Tables".*Proceedings of the 12th International Conference, String Processing and Information Retrieval (SPIRE 2005)* . Vol. 3772/2005. pp. 91–102.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/11575832_11](https://doi.org/10.1007%2F11575832_11) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-540-29740-6](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-29740-6) .
30. [↑](#cite_ref-31) Askitis, Nikolas (2009).["Fast and Compact Hash Tables for Integer Keys"](https://web.archive.org/web/20110216180225/http://crpit.com/confpapers/CRPITV91Askitis.pdf) (PDF).*Proceedings of the 32nd Australasian Computer Science Conference (ACSC 2009)* . Vol. 91. pp. 113–122.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-1-920682-72-9](https://en.wikipedia.org/wiki/Special:BookSources/978-1-920682-72-9) . Archived from[the original](https://crpit.com/confpapers/CRPITV91Askitis.pdf) (PDF) on February 16, 2011. Retrieved June 13, 2010.
31. [↑](#cite_ref-tenenbaum90_32-0) Tenenbaum, Aaron M.; Langsam, Yedidyah; Augenstein, Moshe J. (1990).*Data Structures Using C* . Prentice Hall. pp. 456–461, p. 472.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-13-199746-2](https://en.wikipedia.org/wiki/Special:BookSources/978-0-13-199746-2) .
32. [1](#cite_ref-Cuckoo_33-0)[2](#cite_ref-Cuckoo_33-1)[Pagh, Rasmus](https://en.wikipedia.org/wiki/Rasmus_Pagh) ; Rodler, Flemming Friche (2001). "Cuckoo Hashing".*Algorithms — ESA 2001* . Lecture Notes in Computer Science. Vol. 2161. pp. 121–133.[CiteSeerX](<https://en.wikipedia.org/wiki/CiteSeerX_(identifier)>)[10.1.1.25.4189](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.25.4189) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/3-540-44676-1_10](https://doi.org/10.1007%2F3-540-44676-1_10) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-540-42493-2](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-42493-2) .`{{`[cite book](https://en.wikipedia.org/wiki/Template:Cite_book) }}
: Cite uses deprecated parameter`|citeseerx=` ([help](https://en.wikipedia.org/wiki/Help:CS1_errors#deprecated_params) )
33. [1](#cite_ref-clrs_34-0)[2](#cite_ref-clrs_34-1)[3](#cite_ref-clrs_34-2)[Cormen, Thomas H.](https://en.wikipedia.org/wiki/Thomas_H._Cormen) ;[Leiserson, Charles E.](https://en.wikipedia.org/wiki/Charles_E._Leiserson) ;[Rivest, Ronald L.](https://en.wikipedia.org/wiki/Ron_Rivest) ;[Stein, Clifford](https://en.wikipedia.org/wiki/Clifford_Stein) (2001), "11 Hash Tables",*[Introduction to Algorithms](https://en.wikipedia.org/wiki/Introduction_to_Algorithms)* (2nd ed.),[MIT Press](https://en.wikipedia.org/wiki/MIT_Press) and[McGraw-Hill](https://en.wikipedia.org/wiki/McGraw-Hill) , pp. 221–252,[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[0-262-03293-7](https://en.wikipedia.org/wiki/Special:BookSources/0-262-03293-7) .
34. [1](#cite_ref-chen87_35-0)[2](#cite_ref-chen87_35-1)[3](#cite_ref-chen87_35-2) Vitter, Jeffery S.; Chen, Wen-Chin (1987).[*The design and analysis of coalesced hashing*](https://archive.org/details/designanalysisof0000vitt/) . New York, United States:[Oxford University Press](https://en.wikipedia.org/wiki/Oxford_University_Press) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-19-504182-8](https://en.wikipedia.org/wiki/Special:BookSources/978-0-19-504182-8) – via[Archive.org](https://en.wikipedia.org/wiki/Archive.org) .
35. [↑](#cite_ref-36)[Pagh, Rasmus](https://en.wikipedia.org/wiki/Rasmus_Pagh) ; Rodler, Flemming Friche (2001). "Cuckoo Hashing".*Algorithms — ESA 2001* . Lecture Notes in Computer Science. Vol. 2161. pp. 121–133.[CiteSeerX](<https://en.wikipedia.org/wiki/CiteSeerX_(identifier)>)[10.1.1.25.4189](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.25.4189) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/3-540-44676-1_10](https://doi.org/10.1007%2F3-540-44676-1_10) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-540-42493-2](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-42493-2) .`{{`[cite book](https://en.wikipedia.org/wiki/Template:Cite_book) }}
: Cite uses deprecated parameter`|citeseerx=` ([help](https://en.wikipedia.org/wiki/Help:CS1_errors#deprecated_params) )
36. [1](#cite_ref-nir08_37-0)[2](#cite_ref-nir08_37-1)[3](#cite_ref-nir08_37-2)[4](#cite_ref-nir08_37-3)[5](#cite_ref-nir08_37-4)[6](#cite_ref-nir08_37-5) Herlihy, Maurice; Shavit, Nir; Tzafrir, Moran (2008). "Hopscotch Hashing".*Distributed Computing* . Lecture Notes in Computer Science. Vol. 5218. pp. 350–364.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-540-87779-0_24](https://doi.org/10.1007%2F978-3-540-87779-0_24) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-540-87778-3](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-87778-3) .
37. [1](#cite_ref-waterloo86_38-0)[2](#cite_ref-waterloo86_38-1) Celis, Pedro (1986).[*Robin Hood Hashing*](https://cs.uwaterloo.ca/research/tr/1986/CS-86-14.pdf) (PDF). Ontario, Canada:[University of Waterloo](https://en.wikipedia.org/wiki/University_of_Waterloo) , Dept. of Computer Science.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-315-29700-5](https://en.wikipedia.org/wiki/Special:BookSources/978-0-315-29700-5) .[OCLC](<https://en.wikipedia.org/wiki/OCLC_(identifier)>)[14083698](https://search.worldcat.org/oclc/14083698) .[Archived](https://web.archive.org/web/20211101071032/https://cs.uwaterloo.ca/research/tr/1986/CS-86-14.pdf) (PDF) from the original on November 1, 2021. Retrieved November 2, 2021.
38. [↑](#cite_ref-39) Poblete, P. V.; Viola, A. (July 2019).["Analysis of Robin Hood and Other Hashing Algorithms Under the Random Probing Model, With and Without Deletions"](https://doi.org/10.1017%2FS0963548318000408) .*Combinatorics, Probability and Computing* .**28** (4): 600–617.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1017/S0963548318000408](https://doi.org/10.1017%2FS0963548318000408) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[125374363](https://api.semanticscholar.org/CorpusID:125374363) .
39. [↑](#cite_ref-cornell14_40-0) Clarkson, Michael (2014).["Lecture 13: Hash tables"](https://www.cs.cornell.edu/courses/cs3110/2014fa/lectures/13/lec13.html) .[Cornell University](https://en.wikipedia.org/wiki/Cornell_University) , Department of Computer Science.[Archived](https://web.archive.org/web/20211007011300/https://www.cs.cornell.edu/courses/cs3110/2014fa/lectures/13/lec13.html) from the original on October 7, 2021. Retrieved November 1, 2021 – via cs.cornell.edu.
40. [↑](#cite_ref-41) Gries, David (2017).["JavaHyperText and Data Structure: Robin Hood Hashing"](https://www.cs.cornell.edu/courses/JavaAndDS/files/hashing_RobinHood.pdf) (PDF).[Cornell University](https://en.wikipedia.org/wiki/Cornell_University) , Department of Computer Science.[Archived](https://web.archive.org/web/20210426051503/http://www.cs.cornell.edu/courses/JavaAndDS/files/hashing_RobinHood.pdf) (PDF) from the original on April 26, 2021. Retrieved November 2, 2021 – via cs.cornell.edu.
41. [↑](#cite_ref-indiana88_42-0) Celis, Pedro (March 28, 1988).[*External Robin Hood Hashing*](https://legacy.cs.indiana.edu/ftp/techreports/TR246.pdf) (PDF) (Technical report). Bloomington, Indiana:[Indiana University](https://en.wikipedia.org/wiki/Indiana_University) , Department of Computer Science. 246.[Archived](https://web.archive.org/web/20211103013505/https://legacy.cs.indiana.edu/ftp/techreports/TR246.pdf) (PDF) from the original on November 3, 2021. Retrieved November 2, 2021.
42. [↑](#cite_ref-43) Devadas, Srini; Demaine, Erik (February 25, 2011).["Intro to Algorithms: Resizing Hash Tables"](https://courses.csail.mit.edu/6.006/spring11/rec/rec07.pdf) (PDF).[Massachusetts Institute of Technology](https://en.wikipedia.org/wiki/Massachusetts_Institute_of_Technology) , Department of Computer Science.[Archived](https://web.archive.org/web/20210507102944/https://courses.csail.mit.edu/6.006/spring11/rec/rec07.pdf) (PDF) from the original on May 7, 2021. Retrieved November 9, 2021 – via[MIT OpenCourseWare](https://en.wikipedia.org/wiki/MIT_OpenCourseWare) .
43. [↑](#cite_ref-44) Thareja, Reema (2014). "Hashing and Collision".*Data Structures Using C* . Oxford University Press. pp. 464–488.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-19-809930-7](https://en.wikipedia.org/wiki/Special:BookSources/978-0-19-809930-7) .
44. [1](#cite_ref-scott03_45-0)[2](#cite_ref-scott03_45-1) Friedman, Scott; Krishnan, Anand; Leidefrost, Nicholas (March 18, 2003).["Hash Tables for Embedded and Real-time systems"](https://users.cs.northwestern.edu/~sef318/docs/hashtables.pdf) (PDF).*All Computer Science and Engineering Research* .[Washington University in St. Louis](https://en.wikipedia.org/wiki/Washington_University_in_St._Louis) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.7936/K7WD3XXV](https://doi.org/10.7936%2FK7WD3XXV) .[Archived](https://web.archive.org/web/20210609163643/https://users.cs.northwestern.edu/~sef318/docs/hashtables.pdf) (PDF) from the original on June 9, 2021. Retrieved November 9, 2021 – via[Northwestern University](https://en.wikipedia.org/wiki/Northwestern_University) , Department of Computer Science.
45. [↑](#cite_ref-46) Litwin, Witold (1980).["Linear hashing: A new tool for file and table addressing"](https://www.cs.cmu.edu/afs/cs.cmu.edu/user/christos/www/courses/826-resources/PAPERS+BOOK/linear-hashing.PDF) (PDF).*Proc. 6th Conference on Very Large Databases* .[Carnegie Mellon University](https://en.wikipedia.org/wiki/Carnegie_Mellon_University) . pp. 212–223.[Archived](https://web.archive.org/web/20210506233325/http://www.cs.cmu.edu/afs/cs.cmu.edu/user/christos/www/courses/826-resources/PAPERS+BOOK/linear-hashing.PDF) (PDF) from the original on May 6, 2021. Retrieved November 10, 2021 – via cs.cmu.edu.
46. [1](#cite_ref-dijk10_47-0)[2](#cite_ref-dijk10_47-1) Dijk, Tom Van (2010).["Analysing and Improving Hash Table Performance"](https://www.tvandijk.nl/pdf/bscthesis.pdf) (PDF).[Netherlands](https://en.wikipedia.org/wiki/Netherlands) :[University of Twente](https://en.wikipedia.org/wiki/University_of_Twente) .[Archived](https://web.archive.org/web/20211106094558/http://www.tvandijk.nl/pdf/bscthesis.pdf) (PDF) from the original on November 6, 2021. Retrieved December 31, 2021.
47. [↑](#cite_ref-48) Baeza-Yates, Ricardo; Poblete, Patricio V. (1999). "Chapter 2: Searching". In Atallah (ed.).*Algorithms and Theory of Computation Handbook* . CRC Press. pp. 2–6.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[0849326494](https://en.wikipedia.org/wiki/Special:BookSources/0849326494) .
48. [↑](#cite_ref-49) Lech Banachowski.["Indexes and external sorting"](https://ghostarchive.org/archive/HW0hp) .[pl:Polsko-Japońska Akademia Technik Komputerowych](https://pl.wikipedia.org/wiki/Polsko-Japońska%20Akademia%20Technik%20Komputerowych) . Archived from[the original](https://edux.pjwstk.edu.pl/mat/262/lec/rW9.htm) on March 26, 2022. Retrieved March 26, 2022.
49. [↑](#cite_ref-50) Zhong, Liang; Zheng, Xueqian; Liu, Yong; Wang, Mengting; Cao, Yang (February 2020). "Cache hit ratio maximization in device-to-device communications overlaying cellular networks".*China Communications* .**17** (2): 232–238.[Bibcode](<https://en.wikipedia.org/wiki/Bibcode_(identifier)>) :[2020CComm..17b.232Z](https://ui.adsabs.harvard.edu/abs/2020CComm..17b.232Z) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.23919/jcc.2020.02.018](https://doi.org/10.23919%2Fjcc.2020.02.018) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[212649328](https://api.semanticscholar.org/CorpusID:212649328) .
50. [↑](#cite_ref-51) Bottommley, James (January 1, 2004).["Understanding Caching"](https://www.linuxjournal.com/article/7105) .[Linux Journal](https://en.wikipedia.org/wiki/Linux_Journal) .[Archived](https://web.archive.org/web/20201204195114/https://www.linuxjournal.com/article/7105) from the original on December 4, 2020. Retrieved April 16, 2022.
51. [↑](#cite_ref-52) Jill Seaman (2014).["Set & Hash Tables"](https://web.archive.org/web/20220401134706/https://userweb.cs.txstate.edu/~js236/201412/cs5301/week13.pdf) (PDF).[Texas State University](https://en.wikipedia.org/wiki/Texas_State_University) . Archived from the original on April 1, 2022. Retrieved March 26, 2022.`{{`[cite web](https://en.wikipedia.org/wiki/Template:Cite_web) }}
:  CS1 maint: bot: original URL status unknown ([link](https://en.wikipedia.org/wiki/Category:CS1_maint:_bot:_original_URL_status_unknown) )
52. [↑](#cite_ref-53)["JavaScript data types and data structures - JavaScript | MDN"](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Data_structures#objects) .*developer.mozilla.org* . Retrieved July 24, 2022.
53. [↑](#cite_ref-54)["Map - JavaScript | MDN"](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) .*developer.mozilla.org* . June 20, 2023. Retrieved July 15, 2023.
54. [↑](#cite_ref-55)["Programming language C++ - Technical Specification"](https://web.archive.org/web/20220121061142/http://www.open-std.org/JTC1/SC22/WG21/docs/papers/2013/n3690.pdf) (PDF).[International Organization for Standardization](https://en.wikipedia.org/wiki/International_Organization_for_Standardization) . pp. 812–813. Archived from[the original](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3690.pdf) (PDF) on January 21, 2022. Retrieved February 8, 2022.
55. [↑](#cite_ref-56)["The Go Programming Language Specification"](https://go.dev/ref/spec#Map_types) .*go.dev* . Retrieved January 1, 2023.
56. [↑](#cite_ref-57)["Lesson: Implementations (The Java™ Tutorials > Collections)"](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) .*docs.oracle.com* .[Archived](https://web.archive.org/web/20170118041252/https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) from the original on January 18, 2017. Retrieved April 27, 2018.
57. [↑](#cite_ref-58) Zhang, Juan; Jia, Yunwei (2020).["Redis rehash optimization based on machine learning"](https://doi.org/10.1088%2F1742-6596%2F1453%2F1%2F012048) .*[Journal of Physics: Conference Series](https://en.wikipedia.org/wiki/Journal_of_Physics:_Conference_Series)* .**1453** (1): 3.[Bibcode](<https://en.wikipedia.org/wiki/Bibcode_(identifier)>) :[2020JPhCS1453a2048Z](https://ui.adsabs.harvard.edu/abs/2020JPhCS1453a2048Z) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1088/1742-6596/1453/1/012048](https://doi.org/10.1088%2F1742-6596%2F1453%2F1%2F012048) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[215943738](https://api.semanticscholar.org/CorpusID:215943738) .
58. [↑](#cite_ref-59) Jonan Scheffler (December 25, 2016).["Ruby 2.4 Released: Faster Hashes, Unified Integers and Better Rounding"](https://blog.heroku.com/ruby-2-4-features-hashes-integers-rounding#hash-changes) .*heroku.com* .[Archived](https://web.archive.org/web/20190703145530/https://blog.heroku.com/ruby-2-4-features-hashes-integers-rounding#hash-changes) from the original on July 3, 2019. Retrieved July 3, 2019.
59. [↑](#cite_ref-60)["doc.rust-lang.org"](https://doc.rust-lang.org/std/index.html) .[Archived](https://web.archive.org/web/20221208155205/https://doc.rust-lang.org/std/index.html) from the original on December 8, 2022. Retrieved December 14, 2022.
60. [↑](#cite_ref-61)["HashSet Class (System.Collections.Generic)"](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.hashset-1?view=net-7.0) .*learn.microsoft.com* . Retrieved July 1, 2023.
61. [↑](#cite_ref-62) dotnet-bot.["Dictionary Class (System.Collections.Generic)"](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.dictionary-2?view=net-8.0) .*learn.microsoft.com* . Retrieved January 16, 2024.
62. [↑](#cite_ref-63)["VB.NET HashSet Example"](https://www.dotnetperls.com/hashset-vbnet) .*Dot Net Perls* .

## Further reading

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=38)]

- Tamassia, Roberto; Goodrich, Michael T. (2006). "Chapter Nine: Maps and Dictionaries". [*Data structures and algorithms in Java : \[updated for Java 5.0\]*](https://archive.org/details/datastructuresal00good_183) (4th ed.). Hoboken, NJ: Wiley. pp.[369](https://archive.org/details/datastructuresal00good_183/page/n368) –418.[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-0-471-73884-8](https://en.wikipedia.org/wiki/Special:BookSources/978-0-471-73884-8) .
- McKenzie, B. J.; Harries, R.; Bell, T. (February 1990). "Selecting a hashing algorithm". *Software: Practice and Experience* .**20** (2): 209–224.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1002/spe.4380200207](https://doi.org/10.1002%2Fspe.4380200207) .[hdl](<https://en.wikipedia.org/wiki/Hdl_(identifier)>) :[10092/9691](https://hdl.handle.net/10092%2F9691) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[12854386](https://api.semanticscholar.org/CorpusID:12854386) .

## External links

[
[edit](/w/index.php?title=Hash_table&action=edit§ion=39)]

[Hash tables](https://commons.wikimedia.org/wiki/Category:Hash%20tables).

[Data Structures/Hash Tables](https://en.wikibooks.org/wiki/Data%20Structures/Hash%20Tables)
- [NIST](https://en.wikipedia.org/wiki/NIST) entry on[hash tables](https://xlinux.nist.gov/dads/HTML/hashtab.html)
- [Open Data Structures – Chapter 5 – Hash Tables](https://opendatastructures.org/versions/edition-0.1e/ods-java/5_Hash_Tables.html) ,[Pat Morin](https://en.wikipedia.org/wiki/Pat_Morin)
- [MIT's Introduction to Algorithms: Hashing 1](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-introduction-to-algorithms-sma-5503-fall-2005/video-lectures/lecture-7-hashing-hash-functions/) MIT OCW lecture Video
- [MIT's Introduction to Algorithms: Hashing 2](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-introduction-to-algorithms-sma-5503-fall-2005/video-lectures/lecture-8-universal-hashing-perfect-hashing/) MIT OCW lecture Video
