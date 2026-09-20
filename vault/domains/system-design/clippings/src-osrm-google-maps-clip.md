---
title: Traffic
source: https://github.com/Project-OSRM/osrm-backend/wiki/Traffic
author: Project-OSRM
published: '2022-01-12'
site: GitHub
clipped: '2026-09-20'
---

# Traffic

- 
          
- 
                [Notifications](/login?return_to=%2FProject-OSRM%2Fosrm-backend)
You must be signed in to change notification settings
- 
              [Fork
    4k](/login?return_to=%2FProject-OSRM%2Fosrm-backend)

# Traffic

[29 revisions](/Project-OSRM/osrm-backend/wiki/Traffic/_history)

OSRM has experimental support of traffic data, as of 4.9.0. This
is achieved by providing `osrm-contract` with an additional file that specifies
edge weight updates. For convenience, updates can be specified in a csv file; each line has to follow the format `from_osm_id,to_osm_id,edge_speed_in_km_h(,edge_rate?,(anything else)?)?`. If the `edge_rate` column is completely missing (i.e. the file only has 3 columns), then the edge speed will be used to update edge weight (corresponds to the "duration" weight). If the `edge_rate` column is supplied but the value is blank, then the existing weight on that edge will be kept, but the duration will be updated.  An example of a CSV file for traffic updates is:

```
50267,27780,32,30.3     <- duration will be updated, weight will be updated with length/30.3
25296,25295,24          <- duration will be updated, weight will be updated to match duration
34491,34494,3,          <- duration will be updated, weight will be unchanged
2837,23844,3,,junk      <- duration will be updated, weight will be unchanged, junk is ignored
1283974,2387,3,junk     <- will cause an error
```
*Every line should be a restriction, an empty line will result in an Segment speed file updates.csv malformed error*

The from/to ids are OSM node IDs that are directly connected.  To update the speed for an entire way, you must list each node pair along the way in the CSV file. Note that order is important, to update both directions for connected nodes A and B, you must list `A,B,new_speed_forward(,new_rate_forward)?` and `B,A,new_speed_backward(,new_rate_backward)?`.

```
./osrm-extract data.osm.pbf -p profile.lua --generate-edge-lookup
./osrm-contract data.osrm --segment-speed-file updates.csv
# modify updates.csv
./osrm-contract data.osrm --segment-speed-file updates.csv
# Repeat in loop for desired update time
```
As of OSRM 5.7 the `--generate-edge-lookup` flag does nothing and this will work without it.

Since this is too slow for big datasets to get meaningful updates cycles, you can do a partial contraction using the `--core` parameter. A core factor drastically increases query times. As a result, the alternative-route search is *slowed down* immensely. Note that the `viaroute` service does not calculate alternative routes *by default*, so you should take care if you enable it to the query.  If you do response times will be very slow.

```
./osrm-extract data.osm.pbf -p profile.lua --generate-edge-lookup
# about x8 speedup wrt to --core 1.0
./osrm-contract data.osrm --segment-speed-file updates.csv --core 0.8
# modify updates.csv
./osrm-contract data.osrm --segment-speed-file updates.csv --core 0.8
# Repeat in loop for desired update time
```
For even more speedups use the `--level-cache` option:

```
./osrm-extract data.osm.pbf -p profile.lua --generate-edge-lookup
# For the first run a core of 1.0 is required
./osrm-contract data.osrm --segment-speed-file updates.csv --core 1.0
# modify updates.csv
./osrm-contract data.osrm --segment-speed-file updates.csv --core 0.8 --level-cache true
# Repeat in loop for desired update time
```
A level cache should always be generated with a full hierarchy (core=1.0). After this initial generation, any core factor can be specified.

Alternatively, you can use the MLD routing algorithm - this calculates routes more slowly than CH, but traffic imports are significantly faster:

```
./osrm-extract data.osm.pbf -p profile.lua
./osrm-partition data.osrm
# Run the following in a loop as you replace updates.csv with new data
./osrm-customize data.osrm --segment-speed-file updates.csv
```
Remember to re-load the data by either restarting `osrm-routed`, or using `osrm-routed -s` along with `osrm-datastore`.

OSRM also supports updating penalties applied to turn maneuvers for more realistic
modelling of turn maneuvers. This is achieved by providing `osrm-contract` with an
additional file that specifies turn penalty updates. For convenience, updates can be
specified in a csv file.
Each line has to follow the format `from_osm_id,via_osm_id,to_osm_id,penalty_in_secs(,weight_penalty)?`.
If `weight_penalty` is not specified in a CSV file then `penalty_in_secs` will be used to update turn penalty weights.

```
138334372,15739272,138334381,0.13,11.1
15337331,13035445,138214289,1.27,22.2
137304004,15903737,15903725,0.73
138708033,13294070,134814059,-0.07
```
*Every line should be a penalty, an empty line will result in an turn penalty file malformed error*

```
./osrm-extract data.osm.pbf -p profile.lua --generate-edge-lookup
./osrm-contract data.osrm --turn-penalty-file penalties.csv
```
The value of turn durations and weights must be in range [-3276.8, 3276.7] and [-32768/10^{weight_precision}, 32767/10^{weight_precision}] respectively.

It is possible to specify multiple CSV files:

```
./osrm-contract data.osrm --segment-speed-file updates1.csv  --segment-speed-file updates2.csv
```
To merge conflicting values a `last-one-wins` behavior is used. So values in `updates2.csv` will have higher priority than in `updates1.csv`. The priority for values with equal keys in one file is not specified.
