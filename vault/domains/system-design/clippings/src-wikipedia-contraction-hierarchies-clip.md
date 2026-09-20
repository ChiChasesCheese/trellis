---
title: Contraction hierarchies - Wikipedia
source: https://en.wikipedia.org/wiki/Contraction_hierarchies
published: '2010-12-27'
site: Wikimedia Foundation, Inc.
clipped: '2026-09-20'
---

# Contraction hierarchies - Wikipedia

# Contraction hierarchies

In [computer science](https://en.wikipedia.org/wiki/Computer_science), the method of **contraction hierarchies** is a [speed-up technique](https://en.wikipedia.org/wiki/Speedup) for finding the [shortest path](https://en.wikipedia.org/wiki/Shortest_path_problem) in a [graph](https://en.wikipedia.org/wiki/Graph_theory). The most intuitive applications are car-navigation systems: a user wants to drive from  to  using the quickest possible route. The metric optimized here is the travel time. Intersections are represented by [vertices](<https://en.wikipedia.org/wiki/Vertex_(graph_theory)>), the road sections connecting them by [edges](<https://en.wikipedia.org/wiki/Edge_(graph_theory)>). The edge weights represent the time it takes to drive along this segment of the road. A path from  to  is a sequence of edges (road sections); the shortest path is the one with the minimal sum of edge weights among all possible paths. The shortest path in a graph can be computed using [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra's_algorithm) but, given that road networks consist of tens of millions of vertices, this is impractical.<sup>[\[1\]](#cite_note-dibbelt2015-1)</sup> Contraction hierarchies is a speed-up method optimized to exploit properties of graphs representing road networks.<sup>[\[2\]](#cite_note-bast2016-2)</sup> The speed-up is achieved by creating shortcuts in a preprocessing phase which are then used during a shortest-path query to skip over "unimportant" vertices.<sup>[\[2\]](#cite_note-bast2016-2)</sup> This is based on the observation that road networks are highly hierarchical. Some intersections, for example highway junctions, are "more important" and higher up in the hierarchy than for example a junction leading into a dead end. Shortcuts can be used to save the precomputed distance between two important junctions such that the algorithm doesn't have to consider the full path between these junctions at query time. Contraction hierarchies do not know about which roads humans consider "important" (e.g. highways), but they are provided with the graph as input and are able to assign importance to vertices using heuristics.

Contraction hierarchies are not only applied to speed-up algorithms in [car-navigation systems](https://en.wikipedia.org/wiki/Automotive_navigation_system) but also in web-based [route planners](https://en.wikipedia.org/wiki/Journey_planner), [traffic simulation](https://en.wikipedia.org/wiki/Traffic_simulation), and logistics optimization.[\[3\]](#cite_note-geisberger12-3)[\[1\]](#cite_note-dibbelt2015-1)<sup>[\[4\]](#cite_note-delling09-4)</sup> Implementations of the algorithm are publicly available as [open source software](https://en.wikipedia.org/wiki/Open-source_software).[\[5\]](#cite_note-5)[\[6\]](#cite_note-6)[\[7\]](#cite_note-RoutingKit-7)

## Algorithm

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=1)]

The contraction hierarchies (CH) algorithm is a two-phase approach to the [shortest path problem](https://en.wikipedia.org/wiki/Shortest_path_problem) consisting of a **preprocessing phase** and a **query phase**. As road networks change rather infrequently, more time (seconds to hours) can be used to once precompute some calculations before queries are to be answered. Using this precomputed data, many queries can be answered taking very little time (microseconds) each.[\[1\]](#cite_note-dibbelt2015-1)<sup>[\[3\]](#cite_note-geisberger12-3)</sup> CHs rely on shortcuts to achieve this speedup. A shortcut connects two vertices  and  not adjacent in the original graph. Its edge weight is the sum of the edge weights on the shortest - path.

Consider two large cities connected by a highway. Between these two cities, there is a multitude of junctions leading to small villages and suburbs. Most drivers want to get from one city to the other – maybe as part of a larger route – and not take one of the exits on the way. In the graph representing this road layout, each intersection is represented by a node and edges are created between neighboring intersections. To calculate the distance between these two cities, the algorithm has to traverse all the edges along the way, adding up their length. Precomputing this distance once and storing it in an additional edge created between the two large cities will save calculations each time this highway has to be evaluated in a query. This additional edge is called a "shortcut" and has no counterpart in the real world. The contraction hierarchies algorithm has no knowledge about road types but is able to determine which shortcuts have to be created using the graph alone as input.

### Preprocessing phase

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=2)]

The CH algorithm relies on shortcuts created in the preprocessing phase to reduce the search space – that is the number of vertices CH has to look at, at query time. To achieve this, iterative vertex contractions are performed. When contracting a vertex  it is temporarily removed from the graph , and a shortcut is created between each pair  of neighboring vertices if the shortest path from  to  contains .<sup>[\[2\]](#cite_note-bast2016-2)</sup> The process of determining if the shortest path between  and  contains  is called witness search. It can be performed for example by computing a path from  to  using a forward search using only not yet contracted nodes.[\[3\]](#cite_note-geisberger12-3)

#### Node order

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=3)]

The vertices of the input graph have to be contracted in a way which minimizes the number of edges added to the graph by contractions. As optimal node ordering is [NP-complete](https://en.wikipedia.org/wiki/NP-completeness),[\[8\]](#cite_note-8)[heuristics](<https://en.wikipedia.org/wiki/Heuristic_(computer_science)>) are used.[\[2\]](#cite_note-bast2016-2)

*Bottom-up* and *top-down* heuristics exist. On one hand, the [computationally cheaper](https://en.wikipedia.org/wiki/Computational_complexity_theory) bottom-up heuristics decide the order in which to contract the vertices in a [greedy](https://en.wikipedia.org/wiki/Greedy_algorithm) fashion; this means the order is not known in advance but rather the next node is selected for contraction after the previous contraction has been completed. Top-down heuristics on the other hand precompute the whole node ordering before the first node is contracted. This yields better results but needs more preprocessing time.[\[2\]](#cite_note-bast2016-2)

In *bottom-up* heuristics, a combination of factors is used to select the next vertex for contraction. As the number of shortcuts is the primary factor that determines preprocessing and query runtime, we want to keep it as small as possible. The most important term by which to select the next node for contraction is therefore the net number of edges added when contracting a node . This is defined as  where  is the number of shortcuts that would be created if  were to be contracted and  is the number of edges incident to . Using this criterion alone, a linear path would result in a linear hierarchy (many [levels](<https://en.wikipedia.org/wiki/Level_(logarithmic_quantity)>)) and no created shortcuts.  By considering the number of nearby vertices that are already contracted, a uniform contraction and a flat hierarchy (less levels) is achieved. This can, for example, be done by maintaining a counter for each node that is incremented each time a neighboring vertex is contracted. Nodes with lower counters are then preferred to nodes with higher counters.[\[9\]](#cite_note-9)

*Top-down* heuristics, on the other hand, yield better results but need more preprocessing time. They classify vertices that are part of many shortest paths as more important than those that are only needed for a few shortest paths. This can be [approximated](https://en.wikipedia.org/wiki/Approximation_algorithm) using [nested dissections](https://en.wikipedia.org/wiki/Nested_dissection).<sup>[\[2\]](#cite_note-bast2016-2)</sup> To compute a nested dissection, one recursively separates a graph into two parts, which are themselves then separated into two parts and so on. That is, find a subset of nodes  which when removed from the graph  separate  into two disjunct pieces  of approximately equal size such that . Place all nodes  *last* in the node ordering and then recursively compute the nested dissection for  and ,<sup>[\[10\]](#cite_note-10)</sup> the intuition being that all queries from one half of the graph to the other half of the graph need to pass through the small separator and therefore nodes in this separator are of high importance. Nested dissections can be efficiently calculated on road networks because of their small separators.[\[11\]](#cite_note-11)

### Query phase

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=4)]

In the query phase, a [bidirectional search](https://en.wikipedia.org/wiki/Bidirectional_search) is performed starting from the starting node  and the target node  on the original graph augmented by the shortcuts created in the preprocessing phase.<sup>[\[2\]](#cite_note-bast2016-2)</sup> The most important vertex on the shortest path between  and  will be either  or  themselves or more important than both  and . Therefore, the vertex  minimizing  is on the shortest  path in the original graph and  holds.<sup>[\[2\]](#cite_note-bast2016-2)</sup> This, in combination with how shortcuts are created, means that both forward and backward search only need to relax edges leading to more important nodes (upwards) in the hierarchy which keeps the search space small.<sup>[\[3\]](#cite_note-geisberger12-3)</sup> In all up-(down-up)-down paths, the inner (down-up) can be skipped, because a shortcut has been created in the preprocessing stage.

#### Path retrieval

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=5)]

A CH query, as described above, yields the time or distance from  to  but not the actual path. To obtain the list of edges (roads) on the shortest path, the shortcuts taken have to be unpacked. Each shortcut is the concatenation of two edges: either two edges of the original graph, or two shortcuts, or one original edge and one shortcut. Storing the middle vertex of each shortcut during contraction enables linear-time recursive unpacking of the shortest route.[\[2\]](#cite_note-bast2016-2)[\[3\]](#cite_note-geisberger12-3)

## Customized contraction hierarchies

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=6)]

If the edge weights are changed more often than the [network topology](https://en.wikipedia.org/wiki/Network_topology), CH can be extended to a three-phase approach by including a customization phase between the preprocessing and query phase. This can be used for example to switch between shortest distance and shortest time or include current traffic information as well as user preferences like avoiding certain types of roads (ferries, highways, ...). In the preprocessing phase, most of the runtime is spent on computing the order in which the nodes are contracted.<sup>[\[3\]](#cite_note-geisberger12-3)</sup> This sequence of contraction operations in the preprocessing phase can be saved for when they are later needed in the customization phase. Each time the metric is customized, the contractions can then be efficiently applied in the stored order using the custom metric.<sup>[\[2\]](#cite_note-bast2016-2)</sup> Additionally, depending on the new edge weights it may be necessary to recompute some shortcuts.<sup>[\[3\]](#cite_note-geisberger12-3)</sup> For this to work, the contraction order has to be computed using metric-independent nested dissections.[\[1\]](#cite_note-dibbelt2015-1)

## Extensions and applications

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=7)]

CHs as described above search for a shortest path from one starting node to one target node. This is called *one-to-one* shortest path and is used for example in car-navigation systems. Other applications include matching [GPS](https://en.wikipedia.org/wiki/Global_Positioning_System) traces to road segments and speeding up [traffic simulators](https://en.wikipedia.org/wiki/Traffic_simulation) which have to consider the likely routes taken by all drivers in a network. In [route prediction](https://en.wikipedia.org/wiki/Route_prediction?action=edit&redlink=1) one tries to estimate where a vehicle is likely headed by calculating how well its current and past positions agree with a shortest path from its starting point to any possible target. This can be efficiently done using CHs.[\[2\]](#cite_note-bast2016-2)

In *one-to-many* scenarios, a starting node  and a set of target nodes  are given and the distance  for all  has to be computed. The most prominent application for one-to-many queries are point-of-interest searches. Typical examples include finding the closest gas station, restaurant or post office using actual travel time instead of [geographical distance](https://en.wikipedia.org/wiki/Geographical_distance) as metric.[\[2\]](#cite_note-bast2016-2)

In the *many-to-many* shortest path scenario, a set of starting nodes  and a set of target nodes  are given and the distance  for all  has to be computed. This is used for example in logistic applications.<sup>[\[2\]](#cite_note-bast2016-2)</sup> CHs can be extended to many-to-many queries in the following manner. First, perform a backward upward search from each . For each vertex  scanned during this search, one stores  in a bucket . Then, one runs a forward upward search from each , checking for each non-empty bucket, whether the route over the corresponding vertex improves any best distance. That is, if  for any .[\[2\]](#cite_note-bast2016-2)[\[3\]](#cite_note-geisberger12-3)

Some applications even require *one-to-all* computations, i.e., finding the distances from a source vertex  to all other vertices in the graph. As Dijkstra's algorithm visits each edge exactly once and therefore runs in linear time it is theoretically optimal. Dijkstra's algorithm, however, is hard to [parallelize](https://en.wikipedia.org/wiki/Parallel_computing) and is not [cache-optimal](<https://en.wikipedia.org/wiki/Cache_(computing)>) because of its bad locality. CHs can be used for a more cache-optimal implementation. For this, a forward upward search from  followed by a downward scan over all nodes in the shortcut-enriched graph is performed. The later operation scans through memory in a linear fashion, as the nodes are processed in decreasing order of importance and can therefore be placed in memory accordingly.<sup>[\[12\]](#cite_note-12)</sup> Note, that this is possible because the order in which the nodes are processed in the second phase is independent of the source node .[\[2\]](#cite_note-bast2016-2)

In production, car-navigation systems should be able to compute fastest travel routes using predicted traffic information and display alternative routes. Both can be done using CHs.<sup>[\[2\]](#cite_note-bast2016-2)</sup> The former is called routing with time-dependent networks where the travel time of a given edge is no longer constant but rather a function of the time of day when entering the edge. Alternative routes need to be smooth-looking, significantly different from the shortest path but not significantly longer.[\[2\]](#cite_note-bast2016-2)

CHs can be extended to optimize multiple metrics at the same time; this is called *multi-criteria* route planning. For example, one could minimize both travel cost and time. Another example are [electric vehicles](https://en.wikipedia.org/wiki/Electric_vehicle) for which the available battery charge constrains the valid routes as the battery may not run empty.[\[2\]](#cite_note-bast2016-2)

## Theory

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=8)]

A number of bounds have been established on the preprocessing and query performance of contraction hierarchies. In the following let  be the number of vertices in the graph,  the number of edges,  the [highway dimension](https://en.wikipedia.org/wiki/Highway_dimension),  the graph diameter,  is the [tree-depth](https://en.wikipedia.org/wiki/Tree-depth) and  is the [tree-width](https://en.wikipedia.org/wiki/Treewidth).

The first analysis of contraction hierarchy performance relies in part on a quantity known as the *[highway dimension](https://en.wikipedia.org/wiki/Highway_dimension)*. While the definition of this quantity is technical, intuitively a graph has a small highway dimension if for every  there is a sparse set of vertices  such that every shortest path of length greater than  includes a vertex from . Calculating the exact value of the [highway dimension](https://en.wikipedia.org/wiki/Highway_dimension) is [NP-hard](https://en.wikipedia.org/wiki/NP-hardness)[\[13\]](#cite_note-13)<sup>[\[14\]](#cite_note-14)</sup> and most likely [W\[1\]-hard](https://en.wikipedia.org/wiki/Parameterized_complexity),<sup>[\[15\]](#cite_note-15)</sup> but for grids it is known that the [highway dimension](https://en.wikipedia.org/wiki/Highway_dimension) is .[\[16\]](#cite_note-Abraham2010-16)

An alternative analysis was presented in the Customizable Contraction Hierarchy line of work. Query running times can be bounded by . As the tree-depth can be bounded in terms of the tree-width,  is also a valid upper bound. The main source is <sup>[\[17\]](#cite_note-ReferenceA-17)</sup> but the consequences for the worst case running times are better detailed in.[\[18\]](#cite_note-ReferenceB-18)

### Preprocessing Performance

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=9)]

| Preprocessing Time Complexity of Contraction Hierarchies |  |  | 
|---|---|---|
| Algorithm | Year | Time Complexity | 
|---|---|---|
| Randomized Processing <sup>[\[19\]](#cite_note-Funke2015-19)</sup> | 2015 |  | 

### Query Performance

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=10)]

| Query Time Complexity of Contraction Hierarchies |  |  |  | 
|---|---|---|---|
| Algorithm/Analysis Technique | Year | Time Complexity | Notes | 
|---|---|---|---|
| Bounded Growth Graphs <sup>[\[20\]](#cite_note-20)</sup> | 2018 |  |  | 
| Customizable Contraction Hierarchies <sup>[\[17\]](#cite_note-ReferenceA-17)</sup><sup>[\[18\]](#cite_note-ReferenceB-18)</sup> | 2013-2018 | or . | is the [tree-depth](https://en.wikipedia.org/wiki/Tree-depth) and  is the[tree-width](https://en.wikipedia.org/wiki/Treewidth) | 
| Randomized Processing <sup>[\[19\]](#cite_note-Funke2015-19)</sup> | 2015 |  | Exact, no O-notation; works with high probability | 
| Modified SHARC <sup>[\[16\]](#cite_note-Abraham2010-16)</sup> | 2010 |  | Polynomial preprocessing | 
| Modified SHARC <sup>[\[16\]](#cite_note-Abraham2010-16)</sup> | 2010 |  | Superpolynomial preprocessing | 

## References

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=11)]

1. [1](#cite_ref-dibbelt2015_1-0)[2](#cite_ref-dibbelt2015_1-1)[3](#cite_ref-dibbelt2015_1-2)[4](#cite_ref-dibbelt2015_1-3) Dibbelt, Julian; Strasser, Ben; Wagner, Dorothea (5 April 2016). "Customizable Contraction Hierarchies".*Journal of Experimental Algorithmics* .**21** (1): 1–49.[arXiv](<https://en.wikipedia.org/wiki/ArXiv_(identifier)>) :[1402.0402](https://arxiv.org/abs/1402.0402) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/2886843](https://doi.org/10.1145%2F2886843) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[5247950](https://api.semanticscholar.org/CorpusID:5247950) .
2. [1](#cite_ref-bast2016_2-0)[2](#cite_ref-bast2016_2-1)[3](#cite_ref-bast2016_2-2)[4](#cite_ref-bast2016_2-3)[5](#cite_ref-bast2016_2-4)[6](#cite_ref-bast2016_2-5)[7](#cite_ref-bast2016_2-6)[8](#cite_ref-bast2016_2-7)[9](#cite_ref-bast2016_2-8)[10](#cite_ref-bast2016_2-9)[11](#cite_ref-bast2016_2-10)[12](#cite_ref-bast2016_2-11)[13](#cite_ref-bast2016_2-12)[14](#cite_ref-bast2016_2-13)[15](#cite_ref-bast2016_2-14)[16](#cite_ref-bast2016_2-15)[17](#cite_ref-bast2016_2-16)[18](#cite_ref-bast2016_2-17) Bast, Hannah; Delling, Daniel; Goldberg, Andrew V.; Müller-Hannemann, Matthias; Pajor, Thomas; Sanders, Peter; Wagner, Dorothea; Werneck, Renato F. (2016). "Route Planning in Transportation Networks".*Algorithm Engineering* . Lecture Notes in Computer Science. Vol. 9220. pp. 19–80.[arXiv](<https://en.wikipedia.org/wiki/ArXiv_(identifier)>) :[1504.05140](https://arxiv.org/abs/1504.05140) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-319-49487-6_2](https://doi.org/10.1007%2F978-3-319-49487-6_2) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-319-49486-9](https://en.wikipedia.org/wiki/Special:BookSources/978-3-319-49486-9) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[14384915](https://api.semanticscholar.org/CorpusID:14384915) .
3. [1](#cite_ref-geisberger12_3-0)[2](#cite_ref-geisberger12_3-1)[3](#cite_ref-geisberger12_3-2)[4](#cite_ref-geisberger12_3-3)[5](#cite_ref-geisberger12_3-4)[6](#cite_ref-geisberger12_3-5)[7](#cite_ref-geisberger12_3-6)[8](#cite_ref-geisberger12_3-7) Geisberger, Robert; Sanders, Peter; Schultes, Dominik; Vetter, Christian (2012).["Exact Routing in Large Road Networks Using Contraction Hierarchies"](https://publikationen.bibliothek.kit.edu/1000028701) .*Transportation Science* .**46** (3): 388–404.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1287/trsc.1110.0401](https://doi.org/10.1287%2Ftrsc.1110.0401) .
4. [↑](#cite_ref-delling09_4-0) Delling, Daniel; Sanders, Peter; Schultes, Dominik; Wagner, Dorothea (2009). "Engineering Route Planning Algorithms".*Algorithmics of Large and Complex Networks* . Lecture Notes in Computer Science. Vol. 5515. pp. 117–139.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-642-02094-0_7](https://doi.org/10.1007%2F978-3-642-02094-0_7) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-642-02093-3](https://en.wikipedia.org/wiki/Special:BookSources/978-3-642-02093-3) .
5. [↑](#cite_ref-5)["OSRM – Open Source Routing Machine"](http://project-osrm.org/) .
6. [↑](#cite_ref-6)["Web – GraphHopper"](http://graphhopper.com) .
7. [↑](#cite_ref-RoutingKit_7-0)["GitHub – RoutingKit"](https://github.com/RoutingKit/RoutingKit) .*[GitHub](https://en.wikipedia.org/wiki/GitHub)* . 24 January 2022.
8. [↑](#cite_ref-8) Bauer, Reinhard; Delling, Daniel; Sanders, Peter; Schieferdecker, Dennis; Schultes, Dominik; Wagner, Dorothea (2010-03-01).["Combining hierarchical and goal-directed speed-up techniques for dijkstra's algorithm"](https://publikationen.bibliothek.kit.edu/1000014952) .*Journal of Experimental Algorithmics* .**15** : 2.1.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/1671970.1671976](https://doi.org/10.1145%2F1671970.1671976) .[ISSN](<https://en.wikipedia.org/wiki/ISSN_(identifier)>)[1084-6654](https://search.worldcat.org/issn/1084-6654) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[1661292](https://api.semanticscholar.org/CorpusID:1661292) .
9. [↑](#cite_ref-9) Geisberger, Robert; Sanders, Peter; Schultes, Dominik; Delling, Daniel (2008). "Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road Networks". In McGeoch, Catherine C. (ed.).*Experimental Algorithms* . Lecture Notes in Computer Science. Vol. 5038. Springer Berlin Heidelberg. pp. 319–333.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-540-68552-4_24](https://doi.org/10.1007%2F978-3-540-68552-4_24) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-540-68552-4](https://en.wikipedia.org/wiki/Special:BookSources/978-3-540-68552-4) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[777101](https://api.semanticscholar.org/CorpusID:777101) .
10. [↑](#cite_ref-10) Bauer, Reinhard; Columbus, Tobias; Rutter, Ignaz; Wagner, Dorothea (2016-09-13).["Search-space size in contraction hierarchies"](https://doi.org/10.1016%2Fj.tcs.2016.07.003) .*Theoretical Computer Science* .**645** : 112–127.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1016/j.tcs.2016.07.003](https://doi.org/10.1016%2Fj.tcs.2016.07.003) .[ISSN](<https://en.wikipedia.org/wiki/ISSN_(identifier)>)[0304-3975](https://search.worldcat.org/issn/0304-3975) .
11. [↑](#cite_ref-11) Delling, Daniel; Goldberg, Andrew V.; Razenshteyn, Ilya; Werneck, Renato F. (May 2011). "Graph Partitioning with Natural Cuts".*2011 IEEE International Parallel & Distributed Processing Symposium* . pp. 1135–1146.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/ipdps.2011.108](https://doi.org/10.1109%2Fipdps.2011.108) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-1-61284-372-8](https://en.wikipedia.org/wiki/Special:BookSources/978-1-61284-372-8) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[6884123](https://api.semanticscholar.org/CorpusID:6884123) .
12. [↑](#cite_ref-12) Delling, Daniel; Goldberg, Andrew V.; Nowatzyk, Andreas; Werneck, Renato F. (2011). "PHAST: Hardware-Accelerated Shortest Path Trees".*2011 IEEE International Parallel & Distributed Processing Symposium* . pp. 921–931.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1109/ipdps.2011.89](https://doi.org/10.1109%2Fipdps.2011.89) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-1-61284-372-8](https://en.wikipedia.org/wiki/Special:BookSources/978-1-61284-372-8) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[1419921](https://api.semanticscholar.org/CorpusID:1419921) .
13. [↑](#cite_ref-13) Feldmann, Andreas Emil; Fung, Wai Shing; Könemann, Jochen; Post, Ian (2018-01-01).["A $(1+\varepsilon)$-Embedding of Low Highway Dimension Graphs into Bounded Treewidth Graphs"](https://epubs.siam.org/doi/10.1137/16M1067196) .*SIAM Journal on Computing* .**47** (4): 1667–1704.[arXiv](<https://en.wikipedia.org/wiki/ArXiv_(identifier)>) :[1502.04588](https://arxiv.org/abs/1502.04588) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1137/16M1067196](https://doi.org/10.1137%2F16M1067196) .[ISSN](<https://en.wikipedia.org/wiki/ISSN_(identifier)>)[0097-5397](https://search.worldcat.org/issn/0097-5397) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[11339698](https://api.semanticscholar.org/CorpusID:11339698) .
14. [↑](#cite_ref-14) Blum, Johannes (2019). "Hierarchy of Transportation Network Parameters and Hardness Results". In Jansen, Bart M. P.; Telle, Jan Arne (eds.).[*14th International Symposium on Parameterized and Exact Computation (IPEC 2019)*](https://drops.dagstuhl.de/opus/volltexte/2019/11465) . Leibniz International Proceedings in Informatics. Vol. 148. Dagstuhl, Germany: Schloss Dagstuhl–Leibniz-Zentrum fuer Informatik. pp. 4:1–4:15.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.4230/LIPIcs.IPEC.2019.4](https://doi.org/10.4230%2FLIPIcs.IPEC.2019.4) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-95977-129-0](https://en.wikipedia.org/wiki/Special:BookSources/978-3-95977-129-0) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[166228480](https://api.semanticscholar.org/CorpusID:166228480) .
15. [↑](#cite_ref-15) Blum, Johannes; Disser, Yann; Feldmann, Andreas Emil; Gupta, Siddharth; Zych-Pawlewicz, Anna (2022). "On Sparse Hitting Sets: From Fair Vertex Cover to Highway Dimension". In Dell, Holger; Nederlof, Jesper (eds.).*17th International Symposium on Parameterized and Exact Computation (IPEC 2022)* . Leibniz International Proceedings in Informatics. Vol. 249. Dagstuhl, Germany: Schloss Dagstuhl – Leibniz-Zentrum für Informatik. pp. 5:1–5:23.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.4230/LIPIcs.IPEC.2022.5](https://doi.org/10.4230%2FLIPIcs.IPEC.2022.5) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-95977-260-0](https://en.wikipedia.org/wiki/Special:BookSources/978-3-95977-260-0) .
16. [1](#cite_ref-Abraham2010_16-0)[2](#cite_ref-Abraham2010_16-1)[3](#cite_ref-Abraham2010_16-2) Abraham, Ittai; Fiat, Amos; Goldberg, Andrew (2010).[*Highway dimension, shortest paths, and provably efficient algorithms*](https://www.microsoft.com/en-us/research/wp-content/uploads/2010/01/soda10.pdf) (PDF). Proceedings of the 2010 annual ACM-SIAM symposium on discrete algorithms.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1137/1.9781611973075.64](https://doi.org/10.1137%2F1.9781611973075.64) .
17. [1](#cite_ref-ReferenceA_17-0)[2](#cite_ref-ReferenceA_17-1) Dibbelt, Julian; Strasser, Ben; Wagner, Dorothea (2016). "Customizable Contraction Hierarchies".*ACM Journal of Experimental Algorithmics* .**21** : 1–49.[arXiv](<https://en.wikipedia.org/wiki/ArXiv_(identifier)>) :[1402.0402](https://arxiv.org/abs/1402.0402) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/2886843](https://doi.org/10.1145%2F2886843) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[5247950](https://api.semanticscholar.org/CorpusID:5247950) .
18. [1](#cite_ref-ReferenceB_18-0)[2](#cite_ref-ReferenceB_18-1) Hamann, Michael; Strasser, Ben (2018). "Graph Bisection with Pareto Optimization".*ACM Journal of Experimental Algorithmics* .**23** : 1–34.[arXiv](<https://en.wikipedia.org/wiki/ArXiv_(identifier)>) :[1504.03812](https://arxiv.org/abs/1504.03812) .[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1145/3173045](https://doi.org/10.1145%2F3173045) .[S2CID](<https://en.wikipedia.org/wiki/S2CID_(identifier)>)[3395784](https://api.semanticscholar.org/CorpusID:3395784) .
19. [1](#cite_ref-Funke2015_19-0)[2](#cite_ref-Funke2015_19-1) Funke, Stefan; Storandt, Sabine (2015). "Provable Efficiency of Contraction Hierarchies with Randomized Preprocessing".*Algorithms and Computation* . Lecture Notes in Computer Science. Vol. 9472. pp. 479–490.[doi](<https://en.wikipedia.org/wiki/Doi_(identifier)>) :[10.1007/978-3-662-48971-0_41](https://doi.org/10.1007%2F978-3-662-48971-0_41) .[ISBN](<https://en.wikipedia.org/wiki/ISBN_(identifier)>)[978-3-662-48971-0](https://en.wikipedia.org/wiki/Special:BookSources/978-3-662-48971-0) .
20. [↑](#cite_ref-20) Blum, Johannes; Funke, Stefan; Storandt, Sabine (2018).[*Sublinear Search Spaces for Shortest Path Planning in Grid and Road Networks*](https://www.fmi.uni-stuttgart.de/documents/aaai2018.pdf) (PDF). AAAI.

## External links

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=12)]

### Open source implementations

[
[edit](/w/index.php?title=Contraction_hierarchies&action=edit§ion=13)]
