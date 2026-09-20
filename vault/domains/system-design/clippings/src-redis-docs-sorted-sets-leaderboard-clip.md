---
title: Redis sorted sets
source: https://redis.io/docs/latest/develop/data-types/sorted-sets/
published: '2026-09-10'
site: Docs
clipped: '2026-09-20'
---

# Redis sorted sets

# Redis sorted sets

Introduction to Redis sorted sets

[(view reference, 35 commands)](https://redis.io/docs/latest/commands/?group=sorted-set)

- 
          
            BZMPOP v7.0.0 @write @sortedset @slow @blockingRemoves and returns a member by score from one or more sorted sets. Blocks until a member is available otherwise. Deletes the sorted set if the last element was popped. O(K) + O(M*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.
- 
          
            BZPOPMAX v5.0.0 @write @sortedset @fast @blockingRemoves and returns the member with the highest score from one or more sorted sets. Blocks until a member available otherwise. Deletes the sorted set if the last element was popped. O(log(N)) with N being the number of elements in the sorted set.
- 
          
            BZPOPMIN v5.0.0 @write @sortedset @fast @blockingRemoves and returns the member with the lowest score from one or more sorted sets. Blocks until a member is available otherwise. Deletes the sorted set if the last element was popped. O(log(N)) with N being the number of elements in the sorted set.
- 
          
            ZADD v1.2.0 @write @sortedset @fastAdds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist. O(log(N)) for each item added, where N is the number of elements in the sorted set.
- 
          
            ZCARD v1.2.0 @read @sortedset @fastReturns the number of members in a sorted set. O(1)
- 
          
            ZCOUNT v2.0.0 @read @sortedset @fastReturns the count of members in a sorted set that have scores within a range. O(log(N)) with N being the number of elements in the sorted set.
- 
          
            ZDIFF v6.2.0 @read @sortedset @slowReturns the difference between multiple sorted sets. O(L + (N-K)log(N)) worst case where L is the total number of elements in all the sets, N is the size of the first set, and K is the size of the result set.
- 
          
            ZDIFFSTORE v6.2.0 @write @sortedset @slowStores the difference of multiple sorted sets in a key. O(L + (N-K)log(N)) worst case where L is the total number of elements in all the sets, N is the size of the first set, and K is the size of the result set.
- 
          
            ZINCRBY v1.2.0 @write @sortedset @fastIncrements the score of a member in a sorted set. O(log(N)) where N is the number of elements in the sorted set.
- 
          
            ZINTER v6.2.0 @read @sortedset @slowReturns the intersect of multiple sorted sets. O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted set, K being the number of input sorted sets and M being the number of elements in the resulting sorted set.
- 
          
            ZINTERCARD v7.0.0 @read @sortedset @slowReturns the number of members of the intersect of multiple sorted sets. O(N*K) worst case with N being the smallest input sorted set, K being the number of input sorted sets.
- 
          
            ZINTERSTORE v2.0.0 @write @sortedset @slowStores the intersect of multiple sorted sets in a key. O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted set, K being the number of input sorted sets and M being the number of elements in the resulting sorted set.
- 
          
            ZLEXCOUNT v2.8.9 @read @sortedset @fastReturns the number of members in a sorted set within a lexicographical range. O(log(N)) with N being the number of elements in the sorted set.
- 
          
            ZMPOP v7.0.0 @write @sortedset @slowReturns the highest- or lowest-scoring members from one or more sorted sets after removing them. Deletes the sorted set if the last member was popped. O(K) + O(M*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.
- 
          
            ZMSCORE v6.2.0 @read @sortedset @fastReturns the score of one or more members in a sorted set. O(N) where N is the number of members being requested.
- 
          
            ZPOPMAX v5.0.0 @write @sortedset @fastReturns the highest-scoring members from a sorted set after removing them. Deletes the sorted set if the last member was popped. O(log(N)*M) with N being the number of elements in the sorted set, and M being the number of elements popped.
- 
          
            ZPOPMIN v5.0.0 @write @sortedset @fastReturns the lowest-scoring members from a sorted set after removing them. Deletes the sorted set if the last member was popped. O(log(N)*M) with N being the number of elements in the sorted set, and M being the number of elements popped.
- 
          
            ZRANDMEMBER v6.2.0 @read @sortedset @slowReturns one or more random members from a sorted set. O(N) where N is the number of members returned
- 
          
            ZRANGE v1.2.0 @read @sortedset @slowReturns members in a sorted set within a range of indexes. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.
- 
          
            ZRANGEBYLEX v2.8.9 @read @sortedset @slowReturns members in a sorted set within a lexicographical range. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- 
          
            ZRANGEBYSCORE v1.0.5 @read @sortedset @slowReturns members in a sorted set within a range of scores. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- 
          
            ZRANGESTORE v6.2.0 @write @sortedset @slowStores a range of members from sorted set in a key. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements stored into the destination key.
- 
          
            ZRANK v2.0.0 @read @sortedset @fastReturns the index of a member in a sorted set ordered by ascending scores. O(log(N))
- 
          
            ZREM v1.2.0 @write @sortedset @fastRemoves one or more members from a sorted set. Deletes the sorted set if all members were removed. O(M*log(N)) with N being the number of elements in the sorted set and M the number of elements to be removed.
- 
          
            ZREMRANGEBYLEX v2.8.9 @write @sortedset @slowRemoves members in a sorted set within a lexicographical range. Deletes the sorted set if all members were removed. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.
- 
          
            ZREMRANGEBYRANK v2.0.0 @write @sortedset @slowRemoves members in a sorted set within a range of indexes. Deletes the sorted set if all members were removed. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.
- 
          
            ZREMRANGEBYSCORE v1.2.0 @write @sortedset @slowRemoves members in a sorted set within a range of scores. Deletes the sorted set if all members were removed. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.
- 
          
            ZREVRANGE v1.2.0 @read @sortedset @slowReturns members in a sorted set within a range of indexes in reverse order. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.
- 
          
            ZREVRANGEBYLEX v2.8.9 @read @sortedset @slowReturns members in a sorted set within a lexicographical range in reverse order. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- 
          
            ZREVRANGEBYSCORE v2.2.0 @read @sortedset @slowReturns members in a sorted set within a range of scores in reverse order. O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- 
          
            ZREVRANK v2.0.0 @read @sortedset @fastReturns the index of a member in a sorted set ordered by descending scores. O(log(N))
- 
          
            ZSCAN v2.8.0 @read @sortedset @slowIterates over members and scores of a sorted set. O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.
- 
          
            ZSCORE v1.2.0 @read @sortedset @fastReturns the score of a member in a sorted set. O(1)
- 
          
            ZUNION v6.2.0 @read @sortedset @slowReturns the union of multiple sorted sets. O(N)+O(M*log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.
- 
          
            ZUNIONSTORE v2.0.0 @write @sortedset @slowStores the union of multiple sorted sets in a key. O(N)+O(M log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.

A Redis sorted set is a collection of unique strings (members) ordered by an associated score. When more than one string has the same score, the strings are ordered lexicographically. Some use cases for sorted sets include:

- Leaderboards. For example, you can use sorted sets to easily maintain ordered lists of the highest scores in a massive online game.
- Rate limiters. In particular, you can use a sorted set to build a sliding-window rate limiter to prevent excessive API requests.

You can think of sorted sets as a mix between a Set and a Hash. Like sets, sorted sets are composed of unique, non-repeating string elements, so in some sense a sorted set is a set as well.

However while elements inside sets are not ordered, every element in
a sorted set is associated with a floating point value, called *the score*
(this is why the type is also similar to a hash, since every element
is mapped to a value).

Moreover, elements in a sorted set are *taken in order* (so they are not
ordered on request, order is a peculiarity of the data structure used to
represent sorted sets). They are ordered according to the following rule:

- If B and A are two elements with a different score, then A > B if A.score is > B.score.
- If B and A have exactly the same score, then A > B if the A string is lexicographically greater than the B string. B and A strings can't be equal since sorted sets only have unique elements.

Let's start with a simple example, we'll add all our racers and the score they got in the first race:

> ZADD racer_scores 10 "Norem"
(integer) 1
> ZADD racer_scores 12 "Castilla"
(integer) 1
> ZADD racer_scores 8 "Sam-Bodden" 10 "Royce" 6 "Ford" 14 "Prickett"
(integer) 4

- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)

[and](https://redis.io/docs/latest/develop/tools/insight/)

**Redis Insight**
[.](https://redis.io/docs/latest/develop/tools/redis-for-vscode/)

**Redis for VS Code**```
res1 = r.zadd("racer_scores", {"Norem": 10})
print(res1)  # >>> 1
res2 = r.zadd("racer_scores", {"Castilla": 12})
print(res2)  # >>> 1
res3 = r.zadd(
    "racer_scores",
    {"Sam-Bodden": 8, "Royce": 10, "Ford": 6, "Prickett": 14, "Castilla": 12},
)
print(res3)  # >>> 4
```
```
"""
Code samples for Sorted set doc pages:
    https://redis.io/docs/latest/develop/data-types/sorted-sets/
"""
import redis
r = redis.Redis(decode_responses=True)
res1 = r.zadd("racer_scores", {"Norem": 10})
print(res1)  # >>> 1
res2 = r.zadd("racer_scores", {"Castilla": 12})
print(res2)  # >>> 1
res3 = r.zadd(
    "racer_scores",
    {"Sam-Bodden": 8, "Royce": 10, "Ford": 6, "Prickett": 14, "Castilla": 12},
)
print(res3)  # >>> 4
res4 = r.zrange("racer_scores", 0, -1)
print(res4)  # >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce', 'Castilla', 'Prickett']
res5 = r.zrevrange("racer_scores", 0, -1)
print(res5)  # >>> ['Prickett', 'Castilla', 'Royce', 'Norem', 'Sam-Bodden', 'Ford']
res6 = r.zrange("racer_scores", 0, -1, withscores=True)
print(
    res6
)
# >>> [
#       ('Ford', 6.0), ('Sam-Bodden', 8.0), ('Norem', 10.0), ('Royce', 10.0),
#       ('Castilla', 12.0), ('Prickett', 14.0)
# ]
res7 = r.zrangebyscore("racer_scores", "-inf", 10)
print(res7)  # >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce']
res8 = r.zrem("racer_scores", "Castilla")
print(res8)  # >>> 1
res9 = r.zremrangebyscore("racer_scores", "-inf", 9)
print(res9)  # >>> 2
res10 = r.zrange("racer_scores", 0, -1)
print(res10)  # >>> ['Norem', 'Royce', 'Prickett']
# Recreate the three remaining racers so this example runs on its own.
r.delete("racer_scores")
r.zadd(
    "racer_scores",
    {"Norem": 10, "Royce": 10, "Prickett": 14},
)
res11 = r.zrank("racer_scores", "Norem")
print(res11)  # >>> 0
res12 = r.zrevrank("racer_scores", "Norem")
print(res12)  # >>> 2
res13 = r.zadd(
    "racer_scores",
    {
        "Norem": 0,
        "Sam-Bodden": 0,
        "Royce": 0,
        "Ford": 0,
        "Prickett": 0,
        "Castilla": 0,
    },
)
print(res13)  # >>> 3
res14 = r.zrange("racer_scores", 0, -1)
print(res14)  # >>> ['Castilla', 'Ford', 'Norem', 'Prickett', 'Royce', 'Sam-Bodden']
res15 = r.zrangebylex("racer_scores", "[A", "[L")
print(res15)  # >>> ['Castilla', 'Ford']
res16 = r.zadd("racer_scores", {"Wood": 100})
print(res16)  # >>> 1
res17 = r.zadd("racer_scores", {"Henshaw": 100})
print(res17)  # >>> 1
res18 = r.zadd("racer_scores", {"Henshaw": 150})
print(res18)  # >>> 0
res19 = r.zincrby("racer_scores", 50, "Wood")
print(res19)  # >>> 150.0
res20 = r.zincrby("racer_scores", 50, "Henshaw")
print(res20)  # >>> 200.0
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - name: KeyT,
    - mapping: Mapping[AnyKeyT, EncodableT],
    - nx: bool = False,
    - xx: bool = False,
    - ch: bool = False,
    - incr: bool = False,
    - gt: bool = False,
    - lt: bool = False
- 
                                            
                                            zadd(
                                            
                                            
                                            

```
const res1 = await client.zAdd('racer_scores', { score: 10, value: 'Norem' });
console.log(res1);  // >>> 1
const res2 = await client.zAdd('racer_scores', { score: 12, value: 'Castilla' });
console.log(res2);  // >>> 1
const res3 = await client.zAdd('racer_scores', [
  { score: 8, value: 'Sam-Bodden' },
  { score: 10, value: 'Royce' },
  { score: 6, value: 'Ford' },
  { score: 14, value: 'Prickett' },
  { score: 12, value: 'Castilla' }
]);
console.log(res3);  // >>> 4
```
```
import assert from 'assert';
import { createClient } from 'redis';
const client = createClient();
await client.connect();
const res1 = await client.zAdd('racer_scores', { score: 10, value: 'Norem' });
console.log(res1);  // >>> 1
const res2 = await client.zAdd('racer_scores', { score: 12, value: 'Castilla' });
console.log(res2);  // >>> 1
const res3 = await client.zAdd('racer_scores', [
  { score: 8, value: 'Sam-Bodden' },
  { score: 10, value: 'Royce' },
  { score: 6, value: 'Ford' },
  { score: 14, value: 'Prickett' },
  { score: 12, value: 'Castilla' }
]);
console.log(res3);  // >>> 4
const res4 = await client.zRange('racer_scores', 0, -1);
console.log(res4);  // >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce', 'Castilla', 'Prickett']
const res6 = await client.zRangeWithScores('racer_scores', 0, -1);
console.log(res6);
// >>> [
//       { value: 'Ford', score: 6 }, { value: 'Sam-Bodden', score: 8 },
//       { value: 'Norem', score: 10 }, { value: 'Royce', score: 10 },
//       { value: 'Castilla', score: 12 }, { value: 'Prickett', score: 14 }
// ]
const res7 = await client.zRangeByScore('racer_scores', '-inf', 10);
console.log(res7);  // >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce']
const res8 = await client.zRem('racer_scores', 'Castilla');
console.log(res8);  // >>> 1
const res9 = await client.zRemRangeByScore('racer_scores', '-inf', 9);
console.log(res9);  // >>> 2
const res10 = await client.zRange('racer_scores', 0, -1);
console.log(res10);  // >>> ['Norem', 'Royce', 'Prickett']
// Recreate the three remaining racers so this example runs on its own.
await client.del('racer_scores');
await client.zAdd('racer_scores', [
  { score: 10, value: 'Norem' },
  { score: 10, value: 'Royce' },
  { score: 14, value: 'Prickett' }
]);
const res11 = await client.zRank('racer_scores', 'Norem');
console.log(res11);  // >>> 0
const res12 = await client.zRevRank('racer_scores', 'Norem');
console.log(res12);  // >>> 2
const res13 = await client.zAdd('racer_scores', [
  { score: 0, value: 'Norem' },
  { score: 0, value: 'Sam-Bodden' },
  { score: 0, value: 'Royce' },
  { score: 0, value: 'Ford' },
  { score: 0, value: 'Prickett' },
  { score: 0, value: 'Castilla' }
]);
console.log(res13);  // >>> 3
const res14 = await client.zRange('racer_scores', 0, -1);
console.log(res14);  // >>> ['Castilla', 'Ford', 'Norem', 'Prickett', 'Royce', 'Sam-Bodden']
const res15 = await client.zRangeByLex('racer_scores', '[A', '[L');
console.log(res15);  // >>> ['Castilla', 'Ford']
const res16 = await client.zAdd('racer_scores', { score: 100, value: 'Wood' });
console.log(res16);  // >>> 1
const res17 = await client.zAdd('racer_scores', { score: 100, value: 'Henshaw' });
console.log(res17);  // >>> 1
const res18 = await client.zAdd('racer_scores', { score: 150, value: 'Henshaw' }, { nx: true });
console.log(res18);  // >>> 0
const res19 = await client.zIncrBy('racer_scores', 50, 'Wood');
console.log(res19);  // >>> 150.0
const res20 = await client.zIncrBy('racer_scores', 50, 'Henshaw');
console.log(res20);  // >>> 200.0
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZADD(
                                            
                                            
                                            
    - key: RedisArgument,
    - members: SortedSetMember | Array<SortedSetMember>,
    - options?: ZAddOptions
- 
                                            
                                            ZADD(
                                            
                                            
                                            

```
    long res1 = jedis.zadd("racer_scores", 10d, "Norem");
    System.out.println(res1); // >>> 1
    long res2 = jedis.zadd("racer_scores", 12d, "Castilla");
    System.out.println(res2); // >>> 1
    long res3 = jedis.zadd("racer_scores", new HashMap<String,Double>() {{
      put("Sam-Bodden", 8d);
      put("Royce", 10d);
      put("Ford", 6d);
      put("Prickett", 14d);
      put("Castilla", 12d);
    }});
    System.out.println(res3); // >>> 4
```
```
package io.redis.examples;
import redis.clients.jedis.UnifiedJedis;
import redis.clients.jedis.resps.Tuple;
public class SortedSetsExample {
  public void run() {
    UnifiedJedis jedis = new UnifiedJedis("redis://localhost:6379");
    long res1 = jedis.zadd("racer_scores", 10d, "Norem");
    System.out.println(res1); // >>> 1
    long res2 = jedis.zadd("racer_scores", 12d, "Castilla");
    System.out.println(res2); // >>> 1
    long res3 = jedis.zadd("racer_scores", new HashMap<String,Double>() {{
      put("Sam-Bodden", 8d);
      put("Royce", 10d);
      put("Ford", 6d);
      put("Prickett", 14d);
      put("Castilla", 12d);
    }});
    System.out.println(res3); // >>> 4
    List<String> res4 = jedis.zrange("racer_scores", 0, -1);
    System.out.println(res4); // >>> [Ford, Sam-Bodden, Norem, Royce, Castil, Castilla, Prickett]
    List<String> res5 = jedis.zrevrange("racer_scores", 0, -1);
    System.out.println(res5); // >>> [Prickett, Castilla, Castil, Royce, Norem, Sam-Bodden, Ford]
    List<Tuple> res6 = jedis.zrangeWithScores("racer_scores", 0, -1);
    System.out.println(res6); // >>> [[Ford,6.0], [Sam-Bodden,8.0], [Norem,10.0], [Royce,10.0], [Castil,12.0], [Castilla,12.0], [Prickett,14.0]]
    List<String> res7 = jedis.zrangeByScore("racer_scores", Double.NEGATIVE_INFINITY, 10d);
    System.out.println(res7); // >>> [Ford, Sam-Bodden, Norem, Royce]
    long res8 = jedis.zrem("racer_scores", "Castilla");
    System.out.println(res8); // >>> 1
    long res9 = jedis.zremrangeByScore("racer_scores", Double.NEGATIVE_INFINITY, 9d);
    System.out.println(res9); // >>> 2
    List<String> res10 = jedis.zrange("racer_scores", 0, -1);
    System.out.println(res10); // >>> [Norem, Royce, Prickett]
    // Recreate the three remaining racers so this example runs on its own.
    jedis.del("racer_scores");
    jedis.zadd("racer_scores", new HashMap<String,Double>() {{
      put("Norem", 10d);
      put("Royce", 10d);
      put("Prickett", 14d);
    }});
    long res11 = jedis.zrank("racer_scores", "Norem");
    System.out.println(res11); // >>> 0
    long res12 = jedis.zrevrank("racer_scores", "Norem");
    System.out.println(res12); // >>> 2
    long res13 = jedis.zadd("racer_scores", new HashMap<String,Double>() {{
      put("Norem", 0d);
      put("Sam-Bodden", 0d);
      put("Royce", 0d);
      put("Ford", 0d);
      put("Prickett", 0d);
      put("Castilla", 0d);
    }});
    System.out.println(res13); // >>> 3
    List<String> res14 = jedis.zrange("racer_scores", 0, -1);
    System.out.println(res14); // >>> [Castilla, Ford, Norem, Prickett, Royce, Sam-Bodden]
    List<String> res15 = jedis.zrangeByLex("racer_scores", "[A", "[L");
    System.out.println(res15); // >>> [Castilla, Ford]
    long res16 = jedis.zadd("racer_scores", 100d, "Wood");
    System.out.println(res16); // >>> 1
    long res17 = jedis.zadd("racer_scores", 100d, "Henshaw");
    System.out.println(res17); // >>> 1
    long res18 = jedis.zadd("racer_scores", 150d, "Henshaw");
    System.out.println(res18); // >>> 0
    double res19 = jedis.zincrby("racer_scores", 50d, "Wood");
    System.out.println(res19); // >>> 150.0
    double res20 = jedis.zincrby("racer_scores", 50d, "Henshaw");
    System.out.println(res20); // >>> 200.0
    jedis.close();
  }
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - score: double,
    - member: byte[]
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - score: double,
    - params: byte[] member final ZAddParams
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - scoreMembers: Map<byte[], Double>
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - scoreMembers: Map<byte[], Double>,
    - params: ZAddParams
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: String,
    - score: double,
    - member: String
- 
                                            
                                            zadd(
                                            
                                            
                                            

```
            CompletableFuture<Void> zadd = asyncCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem"))
                    .thenCompose(res1 -> {
                        System.out.println(res1); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(12d, "Castilla"));
                    }).thenCompose(res2 -> {
                        System.out.println(res2); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(8d, "Sam-Bodden"),
                                ScoredValue.just(10d, "Royce"), ScoredValue.just(6d, "Ford"),
                                ScoredValue.just(14d, "Prickett"));
                    })
                    .thenAccept(System.out::println) // >>> 4
                    .toCompletableFuture();
```
```
package io.redis.examples.async;
import io.lettuce.core.*;
import io.lettuce.core.api.async.RedisAsyncCommands;
import io.lettuce.core.api.StatefulRedisConnection;
import java.util.*;
import java.util.concurrent.CompletableFuture;
public class SortedSetExample {
    public void run() {
        RedisClient redisClient = RedisClient.create("redis://localhost:6379");
        try (StatefulRedisConnection<String, String> connection = redisClient.connect()) {
            RedisAsyncCommands<String, String> asyncCommands = connection.async();
            CompletableFuture<Void> zadd = asyncCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem"))
                    .thenCompose(res1 -> {
                        System.out.println(res1); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(12d, "Castilla"));
                    }).thenCompose(res2 -> {
                        System.out.println(res2); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(8d, "Sam-Bodden"),
                                ScoredValue.just(10d, "Royce"), ScoredValue.just(6d, "Ford"),
                                ScoredValue.just(14d, "Prickett"));
                    })
                    .thenAccept(System.out::println) // >>> 4
                    .toCompletableFuture();
            zadd.join();
            CompletableFuture<Void> zrange = asyncCommands.zrange("racer_scores", 0, -1).thenCompose(res3 -> {
                System.out.println(res3);
                // >>> [Ford, Sam-Bodden, Norem, Royce, Castilla, Prickett]
                return asyncCommands.zrevrange("racer_scores", 0, -1);
            })
                    .thenAccept(System.out::println)
                    // >>> [Prickett, Castilla, Royce, Norem, Sam-Bodden, Ford]
                    .toCompletableFuture();
            zrange.join();
            CompletableFuture<Void> zrangeWithScores = asyncCommands.zrangeWithScores("racer_scores", 0, -1)
                    .thenAccept(System.out::println)
                    // >>> [ScoredValue[6.000000, Ford], ScoredValue[8.000000, Sam-Bodden]...
                    .toCompletableFuture();
            zrangeWithScores.join();
            CompletableFuture<Void> zrangebyscore = asyncCommands
                    .zrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 10))
                    .thenAccept(System.out::println)
                    // >>> [Ford, Sam-Bodden, Norem, Royce]
                    .toCompletableFuture();
            zrangebyscore.join();
            CompletableFuture<Void> zremrangebyscore = asyncCommands.zrem("racer_scores", "Castilla").thenCompose(res4 -> {
                System.out.println(res4); // >>> 1
                return asyncCommands.zremrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 9));
            }).thenCompose(res5 -> {
                System.out.println(res5); // >>> 2
                return asyncCommands.zrange("racer_scores", 0, -1);
            })
                    .thenAccept(System.out::println)
                    // >>> [Norem, Royce, Prickett]
                    .toCompletableFuture();
            zremrangebyscore.join();
            // Recreate the three remaining racers so this example runs on its own.
            CompletableFuture<Void> zrank = asyncCommands.del("racer_scores")
                    .thenCompose(delRes -> asyncCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem"),
                            ScoredValue.just(10d, "Royce"), ScoredValue.just(14d, "Prickett")))
                    .thenCompose(addRes -> asyncCommands.zrank("racer_scores", "Norem"))
                    .thenCompose(res6 -> {
                        System.out.println(res6); // >>> 0
                        return asyncCommands.zrevrank("racer_scores", "Norem");
                    })
                    .thenAccept(System.out::println) // >>> 2
                    .toCompletableFuture();
            zrank.join();
            CompletableFuture<Void> zaddLex = asyncCommands.zadd("racer_scores", ScoredValue.just(0d, "Norem"),
                    ScoredValue.just(0d, "Sam-Bodden"), ScoredValue.just(0d, "Royce"), ScoredValue.just(0d, "Castilla"),
                    ScoredValue.just(0d, "Prickett"), ScoredValue.just(0d, "Ford")).thenCompose(res7 -> {
                        System.out.println(res7); // >>> 3
                        return asyncCommands.zrange("racer_scores", 0, -1);
                    }).thenCompose(res8 -> {
                        System.out.println(res8);
                        // >>> [Castilla, Ford, Norem, Prickett, Royce, Sam-Bodden]
                        return asyncCommands.zrangebylex("racer_scores", Range.create("A", "L"));
                    })
                    .thenAccept(System.out::println)
                    // >>> [Castilla, Ford]
                    .toCompletableFuture();
            zaddLex.join();
            CompletableFuture<Void> leaderboard = asyncCommands.zadd("racer_scores", ScoredValue.just(100, "Wood"))
                    .thenCompose(res9 -> {
                        System.out.println(res9); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(100, "Henshaw"));
                    }).thenCompose(res10 -> {
                        System.out.println(res10); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(150, "Henshaw"));
                    }).thenCompose(res11 -> {
                        System.out.println(res11); // >>> 0
                        return asyncCommands.zincrby("racer_scores", 50, "Wood");
                    }).thenCompose(res12 -> {
                        System.out.println(res12); // >>> 150
                        return asyncCommands.zincrby("racer_scores", 50, "Henshaw");
                    })
                    .thenAccept(System.out::println) // >>> 200
                    .toCompletableFuture();
            leaderboard.join();
        } finally {
            redisClient.shutdown();
        }
    }
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...
- 
                                            
                                            zadd(
                                            
                                            
                                            

```
            Mono<Void> zadd = reactiveCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem")).doOnNext(result -> {
                System.out.println(result); // >>> 1
            }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(12d, "Castilla"))).doOnNext(result -> {
                System.out.println(result); // >>> 1
            }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(8d, "Sam-Bodden"),
                    ScoredValue.just(10d, "Royce"), ScoredValue.just(6d, "Ford"),
                    ScoredValue.just(14d, "Prickett"))).doOnNext(result -> {
                        System.out.println(result); // >>> 4
                    }).then();
```
```
package io.redis.examples.reactive;
import io.lettuce.core.*;
import io.lettuce.core.api.reactive.RedisReactiveCommands;
import io.lettuce.core.api.StatefulRedisConnection;
import reactor.core.publisher.Mono;
import java.util.*;
public class SortedSetExample {
    public void run() {
        RedisClient redisClient = RedisClient.create("redis://localhost:6379");
        try (StatefulRedisConnection<String, String> connection = redisClient.connect()) {
            RedisReactiveCommands<String, String> reactiveCommands = connection.reactive();
            Mono<Void> zadd = reactiveCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem")).doOnNext(result -> {
                System.out.println(result); // >>> 1
            }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(12d, "Castilla"))).doOnNext(result -> {
                System.out.println(result); // >>> 1
            }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(8d, "Sam-Bodden"),
                    ScoredValue.just(10d, "Royce"), ScoredValue.just(6d, "Ford"),
                    ScoredValue.just(14d, "Prickett"))).doOnNext(result -> {
                        System.out.println(result); // >>> 4
                    }).then();
            zadd.block();
            Mono<Void> zrange = reactiveCommands.zrange("racer_scores", 0, -1).collectList().doOnNext(result -> {
                System.out.println(result);
                // >>> [Ford, Sam-Bodden, Norem, Royce, Castilla, Prickett]
            }).flatMap(v -> reactiveCommands.zrevrange("racer_scores", 0, -1).collectList()).doOnNext(result -> {
                System.out.println(result);
                // >>> [Prickett, Castilla, Royce, Norem, Sam-Bodden, Ford]
            }).then();
            zrange.block();
            Mono<Void> zrangeWithScores = reactiveCommands.zrangeWithScores("racer_scores", 0, -1).collectList()
                    .doOnNext(result -> {
                        System.out.println(result);
                        // >>> [ScoredValue[6.000000, Ford], ScoredValue[8.000000, Sam-Bodden]...
                    }).then();
            zrangeWithScores.block();
            Mono<Void> zrangebyscore = reactiveCommands
                    .zrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 10)).collectList().doOnNext(result -> {
                        System.out.println(result); // >>> [Ford, Sam-Bodden, Norem, Royce]
                    }).then();
            zrangebyscore.block();
            Mono<Void> zremrangebyscore = reactiveCommands.zrem("racer_scores", "Castilla").doOnNext(result -> {
                System.out.println(result); // >>> 1
            }).flatMap(v -> reactiveCommands.zremrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 9)))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 2
                    }).flatMap(v -> reactiveCommands.zrange("racer_scores", 0, -1).collectList()).doOnNext(result -> {
                        System.out.println(result); // >>> [Norem, Royce, Prickett]
                    }).then();
            zremrangebyscore.block();
            // Recreate the three remaining racers so this example runs on its own.
            Mono<Void> zrank = reactiveCommands.del("racer_scores")
                    .flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem"),
                            ScoredValue.just(10d, "Royce"), ScoredValue.just(14d, "Prickett")))
                    .flatMap(v -> reactiveCommands.zrank("racer_scores", "Norem")).doOnNext(result -> {
                        System.out.println(result); // >>> 0
                    }).flatMap(v -> reactiveCommands.zrevrank("racer_scores", "Norem")).doOnNext(result -> {
                        System.out.println(result); // >>> 2
                    }).then();
            zrank.block();
            Mono<Void> zaddLex = reactiveCommands
                    .zadd("racer_scores", ScoredValue.just(0d, "Norem"), ScoredValue.just(0d, "Sam-Bodden"),
                            ScoredValue.just(0d, "Royce"), ScoredValue.just(0d, "Castilla"),
                            ScoredValue.just(0d, "Prickett"), ScoredValue.just(0d, "Ford"))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 3
                    }).flatMap(v -> reactiveCommands.zrange("racer_scores", 0, -1).collectList()).doOnNext(result -> {
                        System.out.println(result);
                        // >>> [Castilla, Ford, Norem, Prickett, Royce, Sam-Bodden]
                    }).flatMap(v -> reactiveCommands.zrangebylex("racer_scores", Range.create("A", "L")).collectList())
                    .doOnNext(result -> {
                        System.out.println(result); // >>> [Castilla, Ford]
                    }).then();
            zaddLex.block();
            Mono<Void> leaderboard = reactiveCommands.zadd("racer_scores", ScoredValue.just(100, "Wood"))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 1
                    }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(100, "Henshaw")))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 1
                    }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(150, "Henshaw")))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 0
                    }).flatMap(v -> reactiveCommands.zincrby("racer_scores", 50, "Wood")).doOnNext(result -> {
                        System.out.println(result); // >>> 150
                    }).flatMap(v -> reactiveCommands.zincrby("racer_scores", 50, "Henshaw")).doOnNext(result -> {
                        System.out.println(result); // >>> 200
                    }).then();
            leaderboard.block();
        } finally {
            redisClient.shutdown();
        }
    }
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...
- 
                                            
                                            zadd(
                                            
                                            
                                            

```
	res1, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res1) // >>> 1
	res2, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res2) // >>> 1
	res3, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Sam-Bodden", Score: 8},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Ford", Score: 6},
		redis.Z{Member: "Prickett", Score: 14},
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res3) // >>> 4
```
```
package example_commands_test
import (
	"context"
	"fmt"
	"github.com/redis/go-redis/v9"
)
func ExampleClient_zadd() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	res1, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res1) // >>> 1
	res2, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res2) // >>> 1
	res3, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Sam-Bodden", Score: 8},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Ford", Score: 6},
		redis.Z{Member: "Prickett", Score: 14},
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res3) // >>> 4
}
func ExampleClient_zrange() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	_, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Sam-Bodden", Score: 8},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Ford", Score: 6},
		redis.Z{Member: "Prickett", Score: 14},
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	res4, err := rdb.ZRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res4)
	// >>> [Ford Sam-Bodden Norem Royce Castilla Prickett]
	res5, err := rdb.ZRevRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res5)
	// >>> [Prickett Castilla Royce Norem Sam-Bodden Ford]
}
func ExampleClient_zrangewithscores() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	_, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Sam-Bodden", Score: 8},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Ford", Score: 6},
		redis.Z{Member: "Prickett", Score: 14},
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	res6, err := rdb.ZRangeWithScores(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res6)
	// >>> [{6 Ford} {8 Sam-Bodden} {10 Norem} {10 Royce} {12 Castilla} {14 Prickett}]
}
func ExampleClient_zrangebyscore() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	_, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Sam-Bodden", Score: 8},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Ford", Score: 6},
		redis.Z{Member: "Prickett", Score: 14},
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	res7, err := rdb.ZRangeByScore(ctx, "racer_scores",
		&redis.ZRangeBy{Min: "-inf", Max: "10"},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res7)
	// >>> [Ford Sam-Bodden Norem Royce]
}
func ExampleClient_zremrangebyscore() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	_, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Sam-Bodden", Score: 8},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Ford", Score: 6},
		redis.Z{Member: "Prickett", Score: 14},
		redis.Z{Member: "Castilla", Score: 12},
	).Result()
	if err != nil {
		panic(err)
	}
	res8, err := rdb.ZRem(ctx, "racer_scores", "Castilla").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res8) // >>> 1
	res9, err := rdb.ZRemRangeByScore(ctx, "racer_scores", "-inf", "9").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res9) // >>> 2
	res10, err := rdb.ZRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res10)
	// >>> [Norem Royce Prickett]
}
func ExampleClient_zrank() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	// Recreate the three remaining racers so this example runs on its own.
	rdb.Del(ctx, "racer_scores")
	rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Prickett", Score: 14},
	)
	res11, err := rdb.ZRank(ctx, "racer_scores", "Norem").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res11) // >>> 0
	res12, err := rdb.ZRevRank(ctx, "racer_scores", "Norem").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res12) // >>> 2
}
func ExampleClient_zaddlex() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	_, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 0},
		redis.Z{Member: "Royce", Score: 0},
		redis.Z{Member: "Prickett", Score: 0},
	).Result()
	res13, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 0},
		redis.Z{Member: "Sam-Bodden", Score: 0},
		redis.Z{Member: "Royce", Score: 0},
		redis.Z{Member: "Ford", Score: 0},
		redis.Z{Member: "Prickett", Score: 0},
		redis.Z{Member: "Castilla", Score: 0},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res13) // >>> 3
	res14, err := rdb.ZRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res14)
	// >>> [Castilla Ford Norem Prickett Royce Sam-Bodden]
	res15, err := rdb.ZRangeByLex(ctx, "racer_scores", &redis.ZRangeBy{
		Min: "[A", Max: "[L",
	}).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res15) // >>> [Castilla Ford]
}
func ExampleClient_leaderboard() {
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})
	res16, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Wood", Score: 100},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res16) // >>> 1
	res17, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Henshaw", Score: 100},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res17) // >>> 1
	res18, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Henshaw", Score: 150},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res18) // >>> 0
	res19, err := rdb.ZIncrBy(ctx, "racer_scores", 50, "Wood").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res19) // >>> 150
	res20, err := rdb.ZIncrBy(ctx, "racer_scores", 50, "Henshaw").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res20) // >>> 200
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZAdd(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - members: ...Z
- 
                                            
                                            ZAdd(
                                            
                                            
                                            

```
        bool res1 = db.SortedSetAdd("racer_scores", "Norem", 10);
        Console.WriteLine(res1); // >>> True
        bool res2 = db.SortedSetAdd("racer_scores", "Castilla", 12);
        Console.WriteLine(res2); // >>> True
        long res3 = db.SortedSetAdd("racer_scores", [
            new("Sam-Bodden", 8),
            new("Royce", 10),
            new("Ford", 6),
            new("Prickett", 14),
            new("Castilla", 12)
        ]);
        Console.WriteLine(res3); // >>> 4
```
```
using StackExchange.Redis;
public class SortedSetExample
{
    public void Run()
    {
        var muxer = ConnectionMultiplexer.Connect("localhost:6379");
        var db = muxer.GetDatabase();
        bool res1 = db.SortedSetAdd("racer_scores", "Norem", 10);
        Console.WriteLine(res1); // >>> True
        bool res2 = db.SortedSetAdd("racer_scores", "Castilla", 12);
        Console.WriteLine(res2); // >>> True
        long res3 = db.SortedSetAdd("racer_scores", [
            new("Sam-Bodden", 8),
            new("Royce", 10),
            new("Ford", 6),
            new("Prickett", 14),
            new("Castilla", 12)
        ]);
        Console.WriteLine(res3); // >>> 4
        RedisValue[] res4 = db.SortedSetRangeByRank("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res4)); // >>> Ford, Sam-Bodden, Norem, Royce, Castilla, Prickett
        RedisValue[] res5 = db.SortedSetRangeByRank("racer_scores", 0, -1, Order.Descending);
        Console.WriteLine(string.Join(", ", res5)); // >>> Prickett, Castilla, Royce, Norem, Sam-Bodden, Ford
        SortedSetEntry[] res6 = db.SortedSetRangeByRankWithScores("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res6)); // >>> Ford: 6, Sam-Bodden: 8, Norem: 10, Royce: 10, Castilla: 12, Prickett: 14
        RedisValue[] res7 = db.SortedSetRangeByScore("racer_scores", double.NegativeInfinity, 10);
        Console.WriteLine(string.Join(", ", res7)); // >>> Ford, Sam-Bodden, Norem, Royce
        bool res8 = db.SortedSetRemove("racer_scores", "Castilla");
        Console.WriteLine(res8); // >>> True
        long res9 = db.SortedSetRemoveRangeByScore("racer_scores", double.NegativeInfinity, 9);
        Console.WriteLine(res9); // >>> 2
        RedisValue[] res10 = db.SortedSetRangeByRank("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res10)); // >>> Norem, Royce, Prickett
        // Recreate the three remaining racers so this example runs on its own.
        db.KeyDelete("racer_scores");
        db.SortedSetAdd("racer_scores", [
            new("Norem", 10),
            new("Royce", 10),
            new("Prickett", 14)
        ]);
        long? res11 = db.SortedSetRank("racer_scores", "Norem");
        Console.WriteLine(res11); // >>> 0
        long? res12 = db.SortedSetRank("racer_scores", "Norem", Order.Descending);
        Console.WriteLine(res12); // >>> 2
        long res13 = db.SortedSetAdd("racer_scores", [
            new("Norem", 0),
            new("Sam-Bodden", 0),
            new("Royce", 0),
            new("Ford", 0),
            new("Prickett", 0),
            new("Castilla", 0)
        ]);
        Console.WriteLine(res13); // >>> 3
        RedisValue[] res14 = db.SortedSetRangeByRank("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res14)); // >>> Castilla, Ford, Norem, Pricket, Royce, Sam-Bodden
        RedisValue[] res15 = db.SortedSetRangeByValue("racer_scores", "A", "L", Exclude.None);
        Console.WriteLine(string.Join(", ", res15)); // >>> Castilla, Ford
        bool res16 = db.SortedSetAdd("racer_scores", "Wood", 100);
        Console.WriteLine(res16); // >>> True
        bool res17 = db.SortedSetAdd("racer_scores", "Henshaw", 100);
        Console.WriteLine(res17); // >>> True
        bool res18 = db.SortedSetAdd("racer_scores", "Henshaw", 150);
        Console.WriteLine(res18); // >>> False
        double res19 = db.SortedSetIncrement("racer_scores", "Wood", 50);
        Console.WriteLine(res19); // >>> 150.0
        double res20 = db.SortedSetIncrement("racer_scores", "Henshaw", 50);
        Console.WriteLine(res20); // >>> 200.0
    }
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: SortedSetWhen, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            

```
        $res1 = $r->zadd('racer_scores', ['Norem' => 10]);
        echo $res1 . PHP_EOL;
        // >>> 1
        $res2 = $r->zadd('racer_scores', ['Castilla' => 12]);
        echo $res2 . PHP_EOL;
        // >>> 1
        $res3 = $r->zadd('racer_scores', [
            'Sam-Bodden' => 8,
            'Royce' => 10,
            'Ford' => 6,
            'Prickett' => 14,
            'Castilla' => 12,
        ]);
        echo $res3 . PHP_EOL;
        // >>> 4
```
```
<?php
require 'vendor/autoload.php';
use Predis\Client as PredisClient;
class DtSortedSetsTest
{
    public function testDtSortedSet() {
        $r = new PredisClient([
            'scheme'   => 'tcp',
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'password' => '',
            'database' => 0,
        ]);
        $res1 = $r->zadd('racer_scores', ['Norem' => 10]);
        echo $res1 . PHP_EOL;
        // >>> 1
        $res2 = $r->zadd('racer_scores', ['Castilla' => 12]);
        echo $res2 . PHP_EOL;
        // >>> 1
        $res3 = $r->zadd('racer_scores', [
            'Sam-Bodden' => 8,
            'Royce' => 10,
            'Ford' => 6,
            'Prickett' => 14,
            'Castilla' => 12,
        ]);
        echo $res3 . PHP_EOL;
        // >>> 4
        $res4 = $r->zrange('racer_scores', 0, -1);
        echo json_encode($res4) . PHP_EOL;
        // >>> ["Ford","Sam-Bodden","Norem","Royce","Castilla","Prickett"]
        $res5 = $r->zrevrange('racer_scores', 0, -1);
        echo json_encode($res5) . PHP_EOL;
        // >>> ["Prickett","Castilla","Royce","Norem","Sam-Bodden","Ford"]
        $res6 = $r->zrange('racer_scores', 0, -1,[
            'withscores' => true,
        ]);
        echo json_encode($res6) . PHP_EOL;
        // >>> {"Ford":"6","Sam-Bodden":"8","Norem":"10","Royce":"10","Castilla":"12","Prickett":"14"}
        $res7 = $r->zrangebyscore('racer_scores', '-inf', 10);
        echo json_encode($res7) . PHP_EOL;
        // >>> ["Ford","Sam-Bodden","Norem","Royce"]
        $res8 = $r->zrem('racer_scores', 'Castilla');
        echo $res8 . PHP_EOL;
        // >>> 1
        $res9 = $r->zremrangebyscore('racer_scores', '-inf', 9);
        echo $res9 . PHP_EOL;
        // >>> 2
        $res10 = $r->zrange('racer_scores', 0, -1);
        echo json_encode($res10) . PHP_EOL;
        // >>> ["Norem","Royce","Prickett"]
        // Recreate the three remaining racers so this example runs on its own.
        $r->del('racer_scores');
        $r->zadd('racer_scores', [
            'Norem' => 10,
            'Royce' => 10,
            'Prickett' => 14,
        ]);
        $res11 = $r->zrank('racer_scores', 'Norem');
        echo $res11 . PHP_EOL;
        // >>> 0
        $res12 = $r->zrevrank('racer_scores', 'Norem');
        echo $res12 . PHP_EOL;
        // >>> 2
        $res13 = $r->zadd('racer_scores', [
            'Norem' => 0,
            'Sam-Bodden' => 0,
            'Royce' => 0,
            'Ford' => 0,
            'Prickett' => 0,
            'Castilla' => 0,
        ]);
        echo $res13 . PHP_EOL;
        // >>> 3
        $res14 = $r->zrange('racer_scores', 0, -1);
        echo json_encode($res14) . PHP_EOL;
        // >>> ["Castilla","Ford","Norem","Prickett","Royce","Sam-Bodden"]
        $res15 = $r->zrangebylex('racer_scores', '[A', '[L');
        echo json_encode($res15) . PHP_EOL;
        // >>> ["Castilla","Ford"]
        $res16 = $r->zadd('racer_scores', ['Wood' => 100]);
        echo $res16 . PHP_EOL;
        // >>> 1
        $res17 = $r->zadd('racer_scores', ['Henshaw' => 100]);
        echo $res17 . PHP_EOL;
        // >>> 1
        $res18 = $r->zadd('racer_scores', ['Henshaw' => 150]);
        echo $res18 . PHP_EOL;
        // >>> 0
        $res19 = $r->zincrby('racer_scores', 50, 'Wood');
        echo $res19 . PHP_EOL;
        // >>> 150
        $res20 = $r->zincrby('racer_scores', 50, 'Henshaw');
        echo $res20 . PHP_EOL;
        // >>> 200
    }
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - $key: string,
    - $membersAndScoresDictionary: array
- 
                                            
                                            zadd(
                                            
                                            
                                            

```
res1 = r.zadd('racer_scores', [[10, 'Norem']])
puts res1 # >>> 1
res2 = r.zadd('racer_scores', [[12, 'Castilla']])
puts res2 # >>> 1
res3 = r.zadd('racer_scores', [
  [8, 'Sam-Bodden'],
  [10, 'Royce'],
  [6, 'Ford'],
  [14, 'Prickett'],
  [12, 'Castilla']
])
puts res3 # >>> 4
```
```
require 'redis'
r = Redis.new
res1 = r.zadd('racer_scores', [[10, 'Norem']])
puts res1 # >>> 1
res2 = r.zadd('racer_scores', [[12, 'Castilla']])
puts res2 # >>> 1
res3 = r.zadd('racer_scores', [
  [8, 'Sam-Bodden'],
  [10, 'Royce'],
  [6, 'Ford'],
  [14, 'Prickett'],
  [12, 'Castilla']
])
puts res3 # >>> 4
res4 = r.zrange('racer_scores', 0, -1)
puts res4.inspect # >>> ["Ford", "Sam-Bodden", "Norem", "Royce", "Castilla", "Prickett"]
res5 = r.zrevrange('racer_scores', 0, -1)
puts res5.inspect # >>> ["Prickett", "Castilla", "Royce", "Norem", "Sam-Bodden", "Ford"]
res6 = r.zrange('racer_scores', 0, -1, with_scores: true)
puts res6.inspect
# >>> [["Ford", 6.0], ["Sam-Bodden", 8.0], ["Norem", 10.0], ["Royce", 10.0],
#  ["Castilla", 12.0], ["Prickett", 14.0]]
res7 = r.zrangebyscore('racer_scores', '-inf', 10)
puts res7.inspect # >>> ["Ford", "Sam-Bodden", "Norem", "Royce"]
res8 = r.zrem('racer_scores', ['Castilla'])
puts res8 # >>> 1
res9 = r.zremrangebyscore('racer_scores', '-inf', 9)
puts res9 # >>> 2
res10 = r.zrange('racer_scores', 0, -1)
puts res10.inspect # >>> ["Norem", "Royce", "Prickett"]
# Recreate the three remaining racers so this example runs on its own.
r.del('racer_scores')
r.zadd('racer_scores', [[10, 'Norem'], [10, 'Royce'], [14, 'Prickett']])
res11 = r.zrank('racer_scores', 'Norem')
puts res11 # >>> 0
res12 = r.zrevrank('racer_scores', 'Norem')
puts res12 # >>> 2
res13 = r.zadd('racer_scores', [
  [0, 'Norem'],
  [0, 'Sam-Bodden'],
  [0, 'Royce'],
  [0, 'Ford'],
  [0, 'Prickett'],
  [0, 'Castilla']
])
puts res13 # >>> 3
res14 = r.zrange('racer_scores', 0, -1)
puts res14.inspect # >>> ["Castilla", "Ford", "Norem", "Prickett", "Royce", "Sam-Bodden"]
res15 = r.zrangebylex('racer_scores', '[A', '[L')
puts res15.inspect # >>> ["Castilla", "Ford"]
res16 = r.zadd('racer_scores', [[100, 'Wood']])
puts res16 # >>> 1
res17 = r.zadd('racer_scores', [[100, 'Henshaw']])
puts res17 # >>> 1
res18 = r.zadd('racer_scores', [[150, 'Henshaw']])
puts res18 # >>> 0
res19 = r.zincrby('racer_scores', 50, 'Wood')
puts res19 # >>> 150.0
res20 = r.zincrby('racer_scores', 50, 'Henshaw')
puts res20 # >>> 200.0
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: String,
    - *args: [Float, String], Array<[Float, String]>, // a single [score, member] pair or an array of pairs
    - nx: Boolean, // Only add elements that do not already exist
    - xx: Boolean, // Only update elements that already exist
    - lt: Boolean, // Only update existing elements if the new score is less than the current score
    - gt: Boolean, // Only update existing elements if the new score is greater than the current score
    - ch: Boolean, // Return the total number of elements changed
    - incr: Boolean // ZADD acts like ZINCRBY
- 
                                            
                                            zadd(
                                            
                                            
                                            

```
        if let Ok(res) = r.zadd("racer_scores", "Norem", 10) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Castilla", 12) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd_multiple(
            "racer_scores",
            &[
                (8, "Sam-Bodden"),
                (10, "Royce"),
                (6, "Ford"),
                (14, "Prickett"),
                (12, "Castilla"),
            ],
        ) {
            let res: usize = res;
            println!("{res}"); // >>> 4
        }
```
```
mod sorted_set_tests {
    use redis::Commands;
    fn strings(values: &[&str]) -> Vec<String> {
        values.iter().map(|value| value.to_string()).collect()
    }
    fn score_pairs(values: &[(&str, f64)]) -> Vec<(String, f64)> {
        values
            .iter()
            .map(|(member, score)| (member.to_string(), *score))
            .collect()
    }
    fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => match client.get_connection() {
                Ok(conn) => conn,
                Err(e) => {
                    println!("Failed to connect to Redis: {e}");
                    return;
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };
        if let Ok(res) = r.zadd("racer_scores", "Norem", 10) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Castilla", 12) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd_multiple(
            "racer_scores",
            &[
                (8, "Sam-Bodden"),
                (10, "Royce"),
                (6, "Ford"),
                (14, "Prickett"),
                (12, "Castilla"),
            ],
        ) {
            let res: usize = res;
            println!("{res}"); // >>> 4
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Ford", "Sam-Bodden", "Norem", "Royce", "Castilla", "Prickett"]
        }
        if let Ok(res) = r.zrevrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Prickett", "Castilla", "Royce", "Norem", "Sam-Bodden", "Ford"]
        }
        if let Ok(res) = r.zrange_withscores("racer_scores", 0, -1) {
            let res: Vec<(String, f64)> = res;
            println!("{res:?}");
            // >>> [("Ford", 6.0), ("Sam-Bodden", 8.0), ("Norem", 10.0), ("Royce", 10.0), ("Castilla", 12.0), ("Prickett", 14.0)]
        }
        if let Ok(res) = r.zrangebyscore("racer_scores", "-inf", 10) {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Ford", "Sam-Bodden", "Norem", "Royce"]
        }
        if let Ok(res) = r.zrem("racer_scores", "Castilla") {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zrembyscore("racer_scores", "-inf", 9) {
            let res: usize = res;
            println!("{res}"); // >>> 2
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Norem", "Royce", "Prickett"]
        }
        // Recreate the three remaining racers so this example runs on its own.
        let _: () = r.del("racer_scores").expect("Failed to del");
        let _: usize = r
            .zadd_multiple(
                "racer_scores",
                &[(10, "Norem"), (10, "Royce"), (14, "Prickett")],
            )
            .expect("Failed to zadd");
        if let Ok(res) = r.zrank("racer_scores", "Norem") {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 0
            }
        }
        if let Ok(res) = r.zrevrank("racer_scores", "Norem") {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 2
            }
        }
        if let Ok(res) = r.zadd_multiple(
            "racer_scores",
            &[
                (0, "Norem"),
                (0, "Sam-Bodden"),
                (0, "Royce"),
                (0, "Ford"),
                (0, "Prickett"),
                (0, "Castilla"),
            ],
        ) {
            let res: usize = res;
            println!("{res}"); // >>> 3
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Castilla", "Ford", "Norem", "Prickett", "Royce", "Sam-Bodden"]
        }
        if let Ok(res) = r.zrangebylex("racer_scores", "[A", "[L") {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Castilla", "Ford"]
        }
        if let Ok(res) = r.zadd("racer_scores", "Wood", 100) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 100) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 150) {
            let res: usize = res;
            println!("{res}"); // >>> 0
        }
        if let Ok(res) = r.zincr("racer_scores", "Wood", 50) {
            let res: f64 = res;
            println!("{res}"); // >>> 150
        }
        if let Ok(res) = r.zincr("racer_scores", "Henshaw", 50) {
            let res: f64 = res;
            println!("{res}"); // >>> 200
        }
    }
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S
  - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)]
  - 
                                            
                                            zadd_options(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions
- 
                                            
                                            zadd(
                                            
                                            
                                            

```
        if let Ok(res) = r.zadd("racer_scores", "Norem", 10).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Castilla", 12).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r
            .zadd_multiple(
                "racer_scores",
                &[
                    (8, "Sam-Bodden"),
                    (10, "Royce"),
                    (6, "Ford"),
                    (14, "Prickett"),
                    (12, "Castilla"),
                ],
            )
            .await
        {
            let res: usize = res;
            println!("{res}"); // >>> 4
        }
```
```
mod tests {
    use redis::AsyncCommands;
    fn strings(values: &[&str]) -> Vec<String> {
        values.iter().map(|value| value.to_string()).collect()
    }
    fn score_pairs(values: &[(&str, f64)]) -> Vec<(String, f64)> {
        values
            .iter()
            .map(|(member, score)| (member.to_string(), *score))
            .collect()
    }
    async fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => match client.get_multiplexed_async_connection().await {
                Ok(conn) => conn,
                Err(e) => {
                    println!("Failed to connect to Redis: {e}");
                    return;
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };
        if let Ok(res) = r.zadd("racer_scores", "Norem", 10).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Castilla", 12).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r
            .zadd_multiple(
                "racer_scores",
                &[
                    (8, "Sam-Bodden"),
                    (10, "Royce"),
                    (6, "Ford"),
                    (14, "Prickett"),
                    (12, "Castilla"),
                ],
            )
            .await
        {
            let res: usize = res;
            println!("{res}"); // >>> 4
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Ford", "Sam-Bodden", "Norem", "Royce", "Castilla", "Prickett"]
        }
        if let Ok(res) = r.zrevrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Prickett", "Castilla", "Royce", "Norem", "Sam-Bodden", "Ford"]
        }
        if let Ok(res) = r.zrange_withscores("racer_scores", 0, -1).await {
            let res: Vec<(String, f64)> = res;
            println!("{res:?}");
            // >>> [("Ford", 6.0), ("Sam-Bodden", 8.0), ("Norem", 10.0), ("Royce", 10.0), ("Castilla", 12.0), ("Prickett", 14.0)]
        }
        if let Ok(res) = r.zrangebyscore("racer_scores", "-inf", 10).await {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Ford", "Sam-Bodden", "Norem", "Royce"]
        }
        if let Ok(res) = r.zrem("racer_scores", "Castilla").await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zrembyscore("racer_scores", "-inf", 9).await {
            let res: usize = res;
            println!("{res}"); // >>> 2
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Norem", "Royce", "Prickett"]
        }
        // Recreate the three remaining racers so this example runs on its own.
        let _: () = r.del("racer_scores").await.expect("Failed to del");
        let _: usize = r
            .zadd_multiple(
                "racer_scores",
                &[(10, "Norem"), (10, "Royce"), (14, "Prickett")],
            )
            .await
            .expect("Failed to zadd");
        if let Ok(res) = r.zrank("racer_scores", "Norem").await {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 0
            }
        }
        if let Ok(res) = r.zrevrank("racer_scores", "Norem").await {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 2
            }
        }
        if let Ok(res) = r
            .zadd_multiple(
                "racer_scores",
                &[
                    (0, "Norem"),
                    (0, "Sam-Bodden"),
                    (0, "Royce"),
                    (0, "Ford"),
                    (0, "Prickett"),
                    (0, "Castilla"),
                ],
            )
            .await
        {
            let res: usize = res;
            println!("{res}"); // >>> 3
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Castilla", "Ford", "Norem", "Prickett", "Royce", "Sam-Bodden"]
        }
        if let Ok(res) = r.zrangebylex("racer_scores", "[A", "[L").await {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Castilla", "Ford"]
        }
        if let Ok(res) = r.zadd("racer_scores", "Wood", 100).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 100).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 150).await {
            let res: usize = res;
            println!("{res}"); // >>> 0
        }
        if let Ok(res) = r.zincr("racer_scores", "Wood", 50).await {
            let res: f64 = res;
            println!("{res}"); // >>> 150
        }
        if let Ok(res) = r.zincr("racer_scores", "Henshaw", 50).await {
            let res: f64 = res;
            println!("{res}"); // >>> 200
        }
    }
}
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S
  - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)]
  - 
                                            
                                            zadd_options(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions
- 
                                            
                                            zadd(
                                            
                                            
                                            

As you can see [`ZADD`](/docs/latest/commands/zadd/) is similar to [`SADD`](/docs/latest/commands/sadd/), but takes one additional argument
(placed before the element to be added) which is the score.
[`ZADD`](/docs/latest/commands/zadd/) is also variadic, so you are free to specify multiple score-value
pairs, as shown in the example above.

With sorted sets it is trivial to return a list of racers sorted by their
score because actually *they are already sorted*.

Implementation note: Sorted sets are implemented via a
dual-ported data structure containing both a skip list and a hash table, so
every time we add an element Redis performs an O(log(N)) operation. That's
good, so when we ask for sorted elements, Redis does not have to do any work at
all, it's already sorted. Note that the [`ZRANGE`](/docs/latest/commands/zrange/) order is low to high, while the [`ZREVRANGE`](/docs/latest/commands/zrevrange/) order is high to low:

> ZRANGE racer_scores 0 -1
1) "Ford"
2) "Sam-Bodden"
3) "Norem"
4) "Royce"
5) "Castilla"
6) "Prickett"
> ZREVRANGE racer_scores 0 -1
1) "Prickett"
2) "Castilla"
3) "Royce"
4) "Norem"
5) "Sam-Bodden"
6) "Ford"

- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)

[and](https://redis.io/docs/latest/develop/tools/insight/)

**Redis Insight**
[.](https://redis.io/docs/latest/develop/tools/redis-for-vscode/)

**Redis for VS Code**```
res4 = r.zrange("racer_scores", 0, -1)
print(res4)  # >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce', 'Castilla', 'Prickett']
res5 = r.zrevrange("racer_scores", 0, -1)
print(res5)  # >>> ['Prickett', 'Castilla', 'Royce', 'Norem', 'Sam-Bodden', 'Ford']
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - name: KeyT,
    - start: EncodableT,
    - end: EncodableT,
    - desc: bool = False,
    - withscores: bool = False,
    - score_cast_func: Union[type, Callable] = float,
    - byscore: bool = False,
    - bylex: bool = False,
    - offset: Optional[int] = None,
    - num: Optional[int] = None
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - name: KeyT,
    - start: int,
    - end: int,
    - withscores: bool = False,
    - score_cast_func: Union[type, Callable] = float
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

```
const res4 = await client.zRange('racer_scores', 0, -1);
console.log(res4);  // >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce', 'Castilla', 'Prickett']
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRANGE(
                                            
                                            
                                            
    - key: RedisArgument,
    - min: RedisArgument | number,
    - max: RedisArgument | number,
    - options?: ZRangeOptions
  - 
                                            
                                            ZRANGE_WITHSCORES(
                                            
                                            
                                            
    - ...args: Parameters<typeof ZRANGE.parseCommand>
- 
                                            
                                            ZRANGE(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )

```
    List<String> res4 = jedis.zrange("racer_scores", 0, -1);
    System.out.println(res4); // >>> [Ford, Sam-Bodden, Norem, Royce, Castil, Castilla, Prickett]
    List<String> res5 = jedis.zrevrange("racer_scores", 0, -1);
    System.out.println(res5); // >>> [Prickett, Castilla, Castil, Royce, Norem, Sam-Bodden, Ford]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - zRangeParams: ZRangeParams
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - zRangeParams: ZRangeParams
- 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

```
            CompletableFuture<Void> zrange = asyncCommands.zrange("racer_scores", 0, -1).thenCompose(res3 -> {
                System.out.println(res3);
                // >>> [Ford, Sam-Bodden, Norem, Royce, Castilla, Prickett]
                return asyncCommands.zrevrange("racer_scores", 0, -1);
            })
                    .thenAccept(System.out::println)
                    // >>> [Prickett, Castilla, Royce, Norem, Sam-Bodden, Ford]
                    .toCompletableFuture();
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every scored value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

```
            Mono<Void> zrange = reactiveCommands.zrange("racer_scores", 0, -1).collectList().doOnNext(result -> {
                System.out.println(result);
                // >>> [Ford, Sam-Bodden, Norem, Royce, Castilla, Prickett]
            }).flatMap(v -> reactiveCommands.zrevrange("racer_scores", 0, -1).collectList()).doOnNext(result -> {
                System.out.println(result);
                // >>> [Prickett, Castilla, Royce, Norem, Sam-Bodden, Ford]
            }).then();
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every scored value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

```
	res4, err := rdb.ZRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res4)
	// >>> [Ford Sam-Bodden Norem Royce Castilla Prickett]
	res5, err := rdb.ZRevRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res5)
	// >>> [Prickett Castilla Royce Norem Sam-Bodden Ford]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRange(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
  - 
                                            
                                            ZRangeWithScores(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
- 
                                            
                                            ZRange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRevRange(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
- 
                                            
                                            ZRevRange(
                                            
                                            
                                            

```
        RedisValue[] res4 = db.SortedSetRangeByRank("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res4)); // >>> Ford, Sam-Bodden, Norem, Royce, Castilla, Prickett
        RedisValue[] res5 = db.SortedSetRangeByRank("racer_scores", 0, -1, Order.Descending);
        Console.WriteLine(string.Join(", ", res5)); // >>> Prickett, Castilla, Royce, Norem, Sam-Bodden, Ford
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByScore(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: double, // The minimum score to filter by.
    - stop: double, // The maximum score to filter by.
    - exclude: Exclude, // Which of start and stop to exclude (defaults to both inclusive).
    - order: Order, // The order to sort by (defaults to ascending).
    - skip: long, // How many items to skip.
    - take: long, // How many items to take.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            

```
        $res4 = $r->zrange('racer_scores', 0, -1);
        echo json_encode($res4) . PHP_EOL;
        // >>> ["Ford","Sam-Bodden","Norem","Royce","Castilla","Prickett"]
        $res5 = $r->zrevrange('racer_scores', 0, -1);
        echo json_encode($res5) . PHP_EOL;
        // >>> ["Prickett","Castilla","Royce","Norem","Sam-Bodden","Ford"]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - $key: string,
    - $start: int|string,
    - $stop: int|string,
    - ?array $options = null: Any
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - $key: string,
    - $start: int|string,
    - $stop: int|string,
    - ?array $options = null: Any
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

```
res4 = r.zrange('racer_scores', 0, -1)
puts res4.inspect # >>> ["Ford", "Sam-Bodden", "Norem", "Royce", "Castilla", "Prickett"]
res5 = r.zrevrange('racer_scores', 0, -1)
puts res5.inspect # >>> ["Prickett", "Castilla", "Royce", "Norem", "Sam-Bodden", "Ford"]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: Integer, // start index
    - stop: Integer, // stop index
    - by_score: Boolean, // return members by score
    - by_lex: Boolean, // return members by lexicographical ordering
    - rev: Boolean, // reverse the ordering
    - limit: Array, // [offset, count]
    - with_scores: Boolean // include scores in output
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - key: String,
    - start: Integer,
    - stop: Integer,
    - with_scores: Boolean // include scores in output
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Ford", "Sam-Bodden", "Norem", "Royce", "Castilla", "Prickett"]
        }
        if let Ok(res) = r.zrevrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Prickett", "Castilla", "Royce", "Norem", "Sam-Bodden", "Ford"]
        }
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrevrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Ford", "Sam-Bodden", "Norem", "Royce", "Castilla", "Prickett"]
        }
        if let Ok(res) = r.zrevrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Prickett", "Castilla", "Royce", "Norem", "Sam-Bodden", "Ford"]
        }
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes in reverse order.
                                    [ZREVRANGE](https://redis.io/docs/latest/commands/zrevrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrevrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrevrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrevrange(
                                            
                                            
                                            

Note: 0 and -1 means from element index 0 to the last element (-1 works
here just as it does in the case of the [`LRANGE`](/docs/latest/commands/lrange/) command).

It is possible to return scores as well, using the `WITHSCORES` argument:

> ZRANGE racer_scores 0 -1 withscores
 1) "Ford"
 2) "6"
 3) "Sam-Bodden"
 4) "8"
 5) "Norem"
 6) "10"
 7) "Royce"
 8) "10"
 9) "Castilla"
10) "12"
11) "Prickett"
12) "14"

- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)

[and](https://redis.io/docs/latest/develop/tools/insight/)

**Redis Insight**
[.](https://redis.io/docs/latest/develop/tools/redis-for-vscode/)

**Redis for VS Code**```
res6 = r.zrange("racer_scores", 0, -1, withscores=True)
print(
    res6
)
# >>> [
#       ('Ford', 6.0), ('Sam-Bodden', 8.0), ('Norem', 10.0), ('Royce', 10.0),
#       ('Castilla', 12.0), ('Prickett', 14.0)
# ]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - name: KeyT,
    - start: EncodableT,
    - end: EncodableT,
    - desc: bool = False,
    - withscores: bool = False,
    - score_cast_func: Union[type, Callable] = float,
    - byscore: bool = False,
    - bylex: bool = False,
    - offset: Optional[int] = None,
    - num: Optional[int] = None
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
const res6 = await client.zRangeWithScores('racer_scores', 0, -1);
console.log(res6);
// >>> [
//       { value: 'Ford', score: 6 }, { value: 'Sam-Bodden', score: 8 },
//       { value: 'Norem', score: 10 }, { value: 'Royce', score: 10 },
//       { value: 'Castilla', score: 12 }, { value: 'Prickett', score: 14 }
// ]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRANGE(
                                            
                                            
                                            
    - key: RedisArgument,
    - min: RedisArgument | number,
    - max: RedisArgument | number,
    - options?: ZRangeOptions
  - 
                                            
                                            ZRANGE_WITHSCORES(
                                            
                                            
                                            
    - ...args: Parameters<typeof ZRANGE.parseCommand>
- 
                                            
                                            ZRANGE(
                                            
                                            
                                            

```
    List<Tuple> res6 = jedis.zrangeWithScores("racer_scores", 0, -1);
    System.out.println(res6); // >>> [[Ford,6.0], [Sam-Bodden,8.0], [Norem,10.0], [Royce,10.0], [Castil,12.0], [Castilla,12.0], [Prickett,14.0]]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - zRangeParams: ZRangeParams
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - zRangeParams: ZRangeParams
- 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            

```
            CompletableFuture<Void> zrangeWithScores = asyncCommands.zrangeWithScores("racer_scores", 0, -1)
                    .thenAccept(System.out::println)
                    // >>> [ScoredValue[6.000000, Ford], ScoredValue[8.000000, Sam-Bodden]...
                    .toCompletableFuture();
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
            Mono<Void> zrangeWithScores = reactiveCommands.zrangeWithScores("racer_scores", 0, -1).collectList()
                    .doOnNext(result -> {
                        System.out.println(result);
                        // >>> [ScoredValue[6.000000, Ford], ScoredValue[8.000000, Sam-Bodden]...
                    }).then();
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
	res6, err := rdb.ZRangeWithScores(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res6)
	// >>> [{6 Ford} {8 Sam-Bodden} {10 Norem} {10 Royce} {12 Castilla} {14 Prickett}]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRange(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
  - 
                                            
                                            ZRangeWithScores(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
- 
                                            
                                            ZRange(
                                            
                                            
                                            

```
        SortedSetEntry[] res6 = db.SortedSetRangeByRankWithScores("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res6)); // >>> Ford: 6, Sam-Bodden: 8, Norem: 10, Royce: 10, Castilla: 12, Prickett: 14
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByScore(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: double, // The minimum score to filter by.
    - stop: double, // The maximum score to filter by.
    - exclude: Exclude, // Which of start and stop to exclude (defaults to both inclusive).
    - order: Order, // The order to sort by (defaults to ascending).
    - skip: long, // How many items to skip.
    - take: long, // How many items to take.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            

```
        $res6 = $r->zrange('racer_scores', 0, -1,[
            'withscores' => true,
        ]);
        echo json_encode($res6) . PHP_EOL;
        // >>> {"Ford":"6","Sam-Bodden":"8","Norem":"10","Royce":"10","Castilla":"12","Prickett":"14"}
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - $key: string,
    - $start: int|string,
    - $stop: int|string,
    - ?array $options = null: Any
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
res6 = r.zrange('racer_scores', 0, -1, with_scores: true)
puts res6.inspect
# >>> [["Ford", 6.0], ["Sam-Bodden", 8.0], ["Norem", 10.0], ["Royce", 10.0],
#  ["Castilla", 12.0], ["Prickett", 14.0]]
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: Integer, // start index
    - stop: Integer, // stop index
    - by_score: Boolean, // return members by score
    - by_lex: Boolean, // return members by lexicographical ordering
    - rev: Boolean, // reverse the ordering
    - limit: Array, // [offset, count]
    - with_scores: Boolean // include scores in output
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrange_withscores("racer_scores", 0, -1) {
            let res: Vec<(String, f64)> = res;
            println!("{res:?}");
            // >>> [("Ford", 6.0), ("Sam-Bodden", 8.0), ("Norem", 10.0), ("Royce", 10.0), ("Castilla", 12.0), ("Prickett", 14.0)]
        }
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrange_withscores("racer_scores", 0, -1).await {
            let res: Vec<(String, f64)> = res;
            println!("{res:?}");
            // >>> [("Ford", 6.0), ("Sam-Bodden", 8.0), ("Norem", 10.0), ("Royce", 10.0), ("Castilla", 12.0), ("Prickett", 14.0)]
        }
```
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            

## 
  Operating on ranges
  
    
  

Sorted sets are more powerful than this. They can operate on ranges.
Let's get all the racers with 10 or fewer points. We
use the [`ZRANGEBYSCORE`](/docs/latest/commands/zrangebyscore/) command to do it:

> ZRANGEBYSCORE racer_scores -inf 10
1) "Ford"
2) "Sam-Bodden"
3) "Norem"
4) "Royce"

- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)

[and](https://redis.io/docs/latest/develop/tools/insight/)

**Redis Insight**
[.](https://redis.io/docs/latest/develop/tools/redis-for-vscode/)

**Redis for VS Code**```
res7 = r.zrangebyscore("racer_scores", "-inf", 10)
print(res7)  # >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce']
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - name: KeyT,
    - min: ZScoreBoundT,
    - max: ZScoreBoundT,
    - start: Optional[int] = None,
    - num: Optional[int] = None,
    - withscores: bool = False,
    - score_cast_func: Union[type, Callable] = float
- 
                                            
                                            zrangebyscore(
                                            
                                            
                                            

```
const res7 = await client.zRangeByScore('racer_scores', '-inf', 10);
console.log(res7);  // >>> ['Ford', 'Sam-Bodden', 'Norem', 'Royce']
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRANGEBYSCORE(
                                            
                                            
                                            
    - key: RedisArgument,
    - min: string | number,
    - max: string | number,
    - options?: ZRangeByScoreOptions
  - 
                                            
                                            ZRANGEBYSCORE_WITHSCORES(
                                            
                                            
                                            
    - ...args: Parameters<typeof ZRANGEBYSCORE.parseCommand>
- 
                                            
                                            ZRANGEBYSCORE(
                                            
                                            
                                            

```
    List<String> res7 = jedis.zrangeByScore("racer_scores", Double.NEGATIVE_INFINITY, 10d);
    System.out.println(res7); // >>> [Ford, Sam-Bodden, Norem, Royce]
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangeByScore(
                                            
                                            
                                            
    - key: byte[],
    - min: double,
    - offset: double max final int,
    - count: int
  - 
                                            
                                            zrangeByScore(
                                            
                                            
                                            
    - key: byte[],
    - min: byte[],
    - offset: byte[] max final int,
    - count: int
  - 
                                            
                                            zrangeByScore(
                                            
                                            
                                            
    - key: String,
    - min: double,
    - max: double
  - 
                                            
                                            zrangeByScore(
                                            
                                            
                                            
    - key: String,
    - min: String,
    - max: String
  - 
                                            
                                            zrangeByScore(
                                            
                                            
                                            
    - key: String,
    - min: double,
    - offset: double max final int,
    - count: int
- 
                                            
                                            zrangeByScore(
                                            
                                            
                                            

```
            CompletableFuture<Void> zrangebyscore = asyncCommands
                    .zrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 10))
                    .thenAccept(System.out::println)
                    // >>> [Ford, Sam-Bodden, Norem, Royce]
                    .toCompletableFuture();
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: double,
    - max: double
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends Number> // the range.
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: double,
    - max: double,
    - offset: long,
    - count: long
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String,
    - offset: long,
    - count: long
- 
                                            
                                            zrangebyscore(
                                            
                                            
                                            

```
            Mono<Void> zrangebyscore = reactiveCommands
                    .zrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 10)).collectList().doOnNext(result -> {
                        System.out.println(result); // >>> [Ford, Sam-Bodden, Norem, Royce]
                    }).then();
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: double,
    - max: double
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends Number> // the range.
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: double,
    - max: double,
    - offset: long,
    - count: long
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String,
    - offset: long,
    - count: long
- 
                                            
                                            zrangebyscore(
                                            
                                            
                                            

```
	res7, err := rdb.ZRangeByScore(ctx, "racer_scores",
		&redis.ZRangeBy{Min: "-inf", Max: "10"},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res7)
	// >>> [Ford Sam-Bodden Norem Royce]
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRangeByScore(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - opt: *ZRangeBy
- 
                                            
                                            ZRangeByScore(
                                            
                                            
                                            

```
        RedisValue[] res7 = db.SortedSetRangeByScore("racer_scores", double.NegativeInfinity, 10);
        Console.WriteLine(string.Join(", ", res7)); // >>> Ford, Sam-Bodden, Norem, Royce
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRangeByScore(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: double, // The minimum score to filter by.
    - stop: double, // The maximum score to filter by.
    - exclude: Exclude, // Which of start and stop to exclude (defaults to both inclusive).
    - order: Order, // The order to sort by (defaults to ascending).
    - skip: long, // How many items to skip.
    - take: long, // How many items to take.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRangeByScore(
                                            
                                            
                                            

```
        $res7 = $r->zrangebyscore('racer_scores', '-inf', 10);
        echo json_encode($res7) . PHP_EOL;
        // >>> ["Ford","Sam-Bodden","Norem","Royce"]
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - $key: string,
    - $min: int|string,
    - $max: int|string,
    - ?array $options = null: Any
- 
                                            
                                            zrangebyscore(
                                            
                                            
                                            

```
res7 = r.zrangebyscore('racer_scores', '-inf', 10)
puts res7.inspect # >>> ["Ford", "Sam-Bodden", "Norem", "Royce"]
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: String,
    - min: String,
    - max: String,
    - with_scores: Boolean, // include scores in output
    - limit: Array // [offset, count]
- 
                                            
                                            zrangebyscore(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrangebyscore("racer_scores", "-inf", 10) {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Ford", "Sam-Bodden", "Norem", "Royce"]
        }
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
  - 
                                            
                                            zrangebyscore_withscores(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
- 
                                            
                                            zrangebyscore(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrangebyscore("racer_scores", "-inf", 10).await {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Ford", "Sam-Bodden", "Norem", "Royce"]
        }
```
- 
                    
                        Returns members in a sorted set within a range of scores.
                                    [ZRANGEBYSCORE](https://redis.io/docs/latest/commands/zrangebyscore/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebyscore(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
  - 
                                            
                                            zrangebyscore_withscores(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
- 
                                            
                                            zrangebyscore(
                                            
                                            
                                            

We asked Redis to return all the elements with a score between negative infinity and 10 (both extremes are included).

To remove an element we'd simply call [`ZREM`](/docs/latest/commands/zrem/) with the racer's name.
It's also possible to remove ranges of elements. Let's remove racer Castilla along with all
the racers with strictly fewer than 10 points:

> ZREM racer_scores "Castilla"
(integer) 1
> ZREMRANGEBYSCORE racer_scores -inf 9
(integer) 2
> ZRANGE racer_scores 0 -1
1) "Norem"
2) "Royce"
3) "Prickett"

- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)

[and](https://redis.io/docs/latest/develop/tools/insight/)

**Redis Insight**
[.](https://redis.io/docs/latest/develop/tools/redis-for-vscode/)

**Redis for VS Code**```
res8 = r.zrem("racer_scores", "Castilla")
print(res8)  # >>> 1
res9 = r.zremrangebyscore("racer_scores", "-inf", 9)
print(res9)  # >>> 2
res10 = r.zrange("racer_scores", 0, -1)
print(res10)  # >>> ['Norem', 'Royce', 'Prickett']
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - name: KeyT,
    - *values: FieldT
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - name: KeyT,
    - min: ZScoreBoundT,
    - max: ZScoreBoundT
- 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - name: KeyT,
    - start: EncodableT,
    - end: EncodableT,
    - desc: bool = False,
    - withscores: bool = False,
    - score_cast_func: Union[type, Callable] = float,
    - byscore: bool = False,
    - bylex: bool = False,
    - offset: Optional[int] = None,
    - num: Optional[int] = None
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
const res8 = await client.zRem('racer_scores', 'Castilla');
console.log(res8);  // >>> 1
const res9 = await client.zRemRangeByScore('racer_scores', '-inf', 9);
console.log(res9);  // >>> 2
const res10 = await client.zRange('racer_scores', 0, -1);
console.log(res10);  // >>> ['Norem', 'Royce', 'Prickett']
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZREM(
                                            
                                            
                                            
    - key: RedisArgument,
    - member: RedisVariadicArgument
- 
                                            
                                            ZREM(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZREMRANGEBYSCORE(
                                            
                                            
                                            
    - key: RedisArgument,
    - min: RedisArgument | number,
    - max: RedisArgument | number
- 
                                            
                                            ZREMRANGEBYSCORE(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRANGE(
                                            
                                            
                                            
    - key: RedisArgument,
    - min: RedisArgument | number,
    - max: RedisArgument | number,
    - options?: ZRangeOptions
  - 
                                            
                                            ZRANGE_WITHSCORES(
                                            
                                            
                                            
    - ...args: Parameters<typeof ZRANGE.parseCommand>
- 
                                            
                                            ZRANGE(
                                            
                                            
                                            

```
    long res8 = jedis.zrem("racer_scores", "Castilla");
    System.out.println(res8); // >>> 1
    long res9 = jedis.zremrangeByScore("racer_scores", Double.NEGATIVE_INFINITY, 9d);
    System.out.println(res9); // >>> 2
    List<String> res10 = jedis.zrange("racer_scores", 0, -1);
    System.out.println(res10); // >>> [Norem, Royce, Prickett]
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - key: byte[],
    - members: byte[]...
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - key: String,
    - members: String...
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zremrangeByScore(
                                            
                                            
                                            
    - key: byte[],
    - min: double,
    - max: double
  - 
                                            
                                            zremrangeByScore(
                                            
                                            
                                            
    - key: byte[],
    - min: byte[],
    - max: byte[]
  - 
                                            
                                            zremrangeByScore(
                                            
                                            
                                            
    - key: String,
    - min: double,
    - max: double
  - 
                                            
                                            zremrangeByScore(
                                            
                                            
                                            
    - key: String,
    - min: String,
    - max: String
- 
                                            
                                            zremrangeByScore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - zRangeParams: ZRangeParams
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - zRangeParams: ZRangeParams
- 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            

```
            CompletableFuture<Void> zremrangebyscore = asyncCommands.zrem("racer_scores", "Castilla").thenCompose(res4 -> {
                System.out.println(res4); // >>> 1
                return asyncCommands.zremrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 9));
            }).thenCompose(res5 -> {
                System.out.println(res5); // >>> 2
                return asyncCommands.zrange("racer_scores", 0, -1);
            })
                    .thenAccept(System.out::println)
                    // >>> [Norem, Royce, Prickett]
                    .toCompletableFuture();
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - key: K, // the key.
    - members: V... // the member type: value.
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: double,
    - max: double
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends Number> // the range.
- 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
            Mono<Void> zremrangebyscore = reactiveCommands.zrem("racer_scores", "Castilla").doOnNext(result -> {
                System.out.println(result); // >>> 1
            }).flatMap(v -> reactiveCommands.zremrangebyscore("racer_scores", Range.create(Double.NEGATIVE_INFINITY, 9)))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 2
                    }).flatMap(v -> reactiveCommands.zrange("racer_scores", 0, -1).collectList()).doOnNext(result -> {
                        System.out.println(result); // >>> [Norem, Royce, Prickett]
                    }).then();
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - key: K, // the key.
    - members: V... // the member type: value.
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: double,
    - max: double
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends Number> // the range.
- 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
	res8, err := rdb.ZRem(ctx, "racer_scores", "Castilla").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res8) // >>> 1
	res9, err := rdb.ZRemRangeByScore(ctx, "racer_scores", "-inf", "9").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res9) // >>> 2
	res10, err := rdb.ZRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res10)
	// >>> [Norem Royce Prickett]
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZRem(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - members: ...interface{}
- 
                                            
                                            ZRem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRemRangeByScore(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: Any,
    - min: Any,
    - max: string
- 
                                            
                                            ZRemRangeByScore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRange(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
  - 
                                            
                                            ZRangeWithScores(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
- 
                                            
                                            ZRange(
                                            
                                            
                                            

```
        bool res8 = db.SortedSetRemove("racer_scores", "Castilla");
        Console.WriteLine(res8); // >>> True
        long res9 = db.SortedSetRemoveRangeByScore("racer_scores", double.NegativeInfinity, 9);
        Console.WriteLine(res9); // >>> 2
        RedisValue[] res10 = db.SortedSetRangeByRank("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res10)); // >>> Norem, Royce, Prickett
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            SortedSetRemove(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRemove(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - members: RedisValue[], // The members to remove.
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRemove(
                                            
                                            
                                            
    - key: Any, // The key of the sorted set.
    - member: Any,
    - flags: Any // The flags to use for this operation.
  - 
                                            
                                            SortedSetRemove(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRemove(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - members: RedisValue[], // The members to remove.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRemove(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRemoveRangeByScore(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: double, // The minimum score to remove.
    - stop: double, // The maximum score to remove.
    - exclude: Exclude, // Which of start and stop to exclude (defaults to both inclusive).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRemoveRangeByScore(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: double, // The minimum score to remove.
    - stop: double, // The maximum score to remove.
    - exclude: Exclude, // Which of start and stop to exclude (defaults to both inclusive).
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRemoveRangeByScore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByScore(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: double, // The minimum score to filter by.
    - stop: double, // The maximum score to filter by.
    - exclude: Exclude, // Which of start and stop to exclude (defaults to both inclusive).
    - order: Order, // The order to sort by (defaults to ascending).
    - skip: long, // How many items to skip.
    - take: long, // How many items to take.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            

```
        $res8 = $r->zrem('racer_scores', 'Castilla');
        echo $res8 . PHP_EOL;
        // >>> 1
        $res9 = $r->zremrangebyscore('racer_scores', '-inf', 9);
        echo $res9 . PHP_EOL;
        // >>> 2
        $res10 = $r->zrange('racer_scores', 0, -1);
        echo json_encode($res10) . PHP_EOL;
        // >>> ["Norem","Royce","Prickett"]
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - $key: string,
    - $member: string ...
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - $key: string,
    - $min: int|string,
    - $max: int|string
- 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - $key: string,
    - $start: int|string,
    - $stop: int|string,
    - ?array $options = null: Any
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
res8 = r.zrem('racer_scores', ['Castilla'])
puts res8 # >>> 1
res9 = r.zremrangebyscore('racer_scores', '-inf', 9)
puts res9 # >>> 2
res10 = r.zrange('racer_scores', 0, -1)
puts res10.inspect # >>> ["Norem", "Royce", "Prickett"]
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - key: String,
    - member: String, Array<String> // a single member or an array of members
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
    - key: String,
    - min: String,
    - max: String
- 
                                            
                                            zremrangebyscore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: Integer, // start index
    - stop: Integer, // stop index
    - by_score: Boolean, // return members by score
    - by_lex: Boolean, // return members by lexicographical ordering
    - rev: Boolean, // reverse the ordering
    - limit: Array, // [offset, count]
    - with_scores: Boolean // include scores in output
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrem("racer_scores", "Castilla") {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zrembyscore("racer_scores", "-inf", 9) {
            let res: usize = res;
            println!("{res}"); // >>> 2
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Norem", "Royce", "Prickett"]
        }
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - key: K,
    - members: M
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrembyscore(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
- 
                                            
                                            zrembyscore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            

```
        if let Ok(res) = r.zrem("racer_scores", "Castilla").await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zrembyscore("racer_scores", "-inf", 9).await {
            let res: usize = res;
            println!("{res}"); // >>> 2
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Norem", "Royce", "Prickett"]
        }
```
- 
                    
                        Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.
                                    [ZREM](https://redis.io/docs/latest/commands/zrem/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrem(
                                            
                                            
                                            
    - key: K,
    - members: M
- 
                                            
                                            zrem(
                                            
                                            
                                            
- 
                    
                        Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.
                                    [ZREMRANGEBYSCORE](https://redis.io/docs/latest/commands/zremrangebyscore/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrembyscore(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
- 
                                            
                                            zrembyscore(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            

[`ZREMRANGEBYSCORE`](/docs/latest/commands/zremrangebyscore/) is perhaps not the best command name,
but it can be very useful, and returns the number of removed elements.

Another extremely useful operation defined for sorted set elements
is the get-rank operation. It is possible to ask what is the
position of an element in the set of ordered elements.
The [`ZREVRANK`](/docs/latest/commands/zrevrank/) command is also available in order to get the rank, considering
the elements sorted in a descending way.

# Recreate the three remaining racers so this example runs on its own.
> DEL racer_scores
(integer) 1
> ZADD racer_scores 10 "Norem" 10 "Royce" 14 "Prickett"
(integer) 3
> ZRANK racer_scores "Norem"
(integer) 0
> ZREVRANK racer_scores "Norem"
(integer) 2

- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)

[and](https://redis.io/docs/latest/develop/tools/insight/)

**Redis Insight**
[.](https://redis.io/docs/latest/develop/tools/redis-for-vscode/)

**Redis for VS Code**```
# Recreate the three remaining racers so this example runs on its own.
r.delete("racer_scores")
r.zadd(
    "racer_scores",
    {"Norem": 10, "Royce": 10, "Prickett": 14},
)
res11 = r.zrank("racer_scores", "Norem")
print(res11)  # >>> 0
res12 = r.zrevrank("racer_scores", "Norem")
print(res12)  # >>> 2
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - name: KeyT,
    - mapping: Mapping[AnyKeyT, EncodableT],
    - nx: bool = False,
    - xx: bool = False,
    - ch: bool = False,
    - incr: bool = False,
    - gt: bool = False,
    - lt: bool = False
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - name: KeyT,
    - value: EncodableT,
    - withscore: bool = False,
    - score_cast_func: Union[type, Callable] = float
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - name: KeyT,
    - value: EncodableT,
    - withscore: bool = False,
    - score_cast_func: Union[type, Callable] = float
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

```
// Recreate the three remaining racers so this example runs on its own.
await client.del('racer_scores');
await client.zAdd('racer_scores', [
  { score: 10, value: 'Norem' },
  { score: 10, value: 'Royce' },
  { score: 14, value: 'Prickett' }
]);
const res11 = await client.zRank('racer_scores', 'Norem');
console.log(res11);  // >>> 0
const res12 = await client.zRevRank('racer_scores', 'Norem');
console.log(res12);  // >>> 2
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZADD(
                                            
                                            
                                            
    - key: RedisArgument,
    - members: SortedSetMember | Array<SortedSetMember>,
    - options?: ZAddOptions
- 
                                            
                                            ZADD(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZRANK(
                                            
                                            
                                            
    - key: RedisArgument,
    - member: RedisArgument
- 
                                            
                                            ZRANK(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZREVRANK(
                                            
                                            
                                            
    - key: RedisArgument,
    - member: RedisArgument
- 
                                            
                                            ZREVRANK(
                                            
                                            
                                            

```
    // Recreate the three remaining racers so this example runs on its own.
    jedis.del("racer_scores");
    jedis.zadd("racer_scores", new HashMap<String,Double>() {{
      put("Norem", 10d);
      put("Royce", 10d);
      put("Prickett", 14d);
    }});
    long res11 = jedis.zrank("racer_scores", "Norem");
    System.out.println(res11); // >>> 0
    long res12 = jedis.zrevrank("racer_scores", "Norem");
    System.out.println(res12); // >>> 2
```
- 
                    
                        Deletes one or more keys.
  - 
                                            
                                            del(
                                            
                                            
                                            
    - keys: byte[]...
  - 
                                            
                                            del(
                                            
                                            
                                            
    - key: byte[]
  - 
                                            
                                            del(
                                            
                                            
                                            
    - keys: String...
  - 
                                            
                                            del(
                                            
                                            
                                            
    - key: String
- 
                                            
                                            del(
                                            
                                            
                                            
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - score: double,
    - member: byte[]
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - score: double,
    - params: byte[] member final ZAddParams
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - scoreMembers: Map<byte[], Double>
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - scoreMembers: Map<byte[], Double>,
    - params: ZAddParams
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: String,
    - score: double,
    - member: String
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - key: byte[],
    - member: byte[]
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - key: String,
    - member: String
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - key: byte[],
    - member: byte[]
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - key: String,
    - member: String
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

```
            // Recreate the three remaining racers so this example runs on its own.
            CompletableFuture<Void> zrank = asyncCommands.del("racer_scores")
                    .thenCompose(delRes -> asyncCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem"),
                            ScoredValue.just(10d, "Royce"), ScoredValue.just(14d, "Prickett")))
                    .thenCompose(addRes -> asyncCommands.zrank("racer_scores", "Norem"))
                    .thenCompose(res6 -> {
                        System.out.println(res6); // >>> 0
                        return asyncCommands.zrevrank("racer_scores", "Norem");
                    })
                    .thenAccept(System.out::println) // >>> 2
                    .toCompletableFuture();
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - key: K, // the key.
    - member: V // the member type: value.
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - key: K, // the key.
    - member: V // the member type: value.
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

```
            // Recreate the three remaining racers so this example runs on its own.
            Mono<Void> zrank = reactiveCommands.del("racer_scores")
                    .flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(10d, "Norem"),
                            ScoredValue.just(10d, "Royce"), ScoredValue.just(14d, "Prickett")))
                    .flatMap(v -> reactiveCommands.zrank("racer_scores", "Norem")).doOnNext(result -> {
                        System.out.println(result); // >>> 0
                    }).flatMap(v -> reactiveCommands.zrevrank("racer_scores", "Norem")).doOnNext(result -> {
                        System.out.println(result); // >>> 2
                    }).then();
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - key: K, // the key.
    - member: V // the member type: value.
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - key: K, // the key.
    - member: V // the member type: value.
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

```
	// Recreate the three remaining racers so this example runs on its own.
	rdb.Del(ctx, "racer_scores")
	rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 10},
		redis.Z{Member: "Royce", Score: 10},
		redis.Z{Member: "Prickett", Score: 14},
	)
	res11, err := rdb.ZRank(ctx, "racer_scores", "Norem").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res11) // >>> 0
	res12, err := rdb.ZRevRank(ctx, "racer_scores", "Norem").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res12) // >>> 2
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZAdd(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - members: ...Z
- 
                                            
                                            ZAdd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZRank(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: Any,
    - member: string
- 
                                            
                                            ZRank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZRevRank(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: Any,
    - member: string
- 
                                            
                                            ZRevRank(
                                            
                                            
                                            

```
        // Recreate the three remaining racers so this example runs on its own.
        db.KeyDelete("racer_scores");
        db.SortedSetAdd("racer_scores", [
            new("Norem", 10),
            new("Royce", 10),
            new("Prickett", 14)
        ]);
        long? res11 = db.SortedSetRank("racer_scores", "Norem");
        Console.WriteLine(res11); // >>> 0
        long? res12 = db.SortedSetRank("racer_scores", "Norem", Order.Descending);
        Console.WriteLine(res12); // >>> 2
```
- 
                    
                        Deletes one or more keys.
  - 
                                            
                                            KeyDelete(
                                            
                                            
                                            
    - key: RedisKey,
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            KeyDelete(
                                            
                                            
                                            
    - keys: RedisKey[], // The keys to delete.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            KeyDelete(
                                            
                                            
                                            
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: SortedSetWhen, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            SortedSetRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue, // The member to get the rank of.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue, // The member to get the rank of.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            SortedSetRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue, // The member to get the rank of.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue, // The member to get the rank of.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRank(
                                            
                                            
                                            

```
        // Recreate the three remaining racers so this example runs on its own.
        $r->del('racer_scores');
        $r->zadd('racer_scores', [
            'Norem' => 10,
            'Royce' => 10,
            'Prickett' => 14,
        ]);
        $res11 = $r->zrank('racer_scores', 'Norem');
        echo $res11 . PHP_EOL;
        // >>> 0
        $res12 = $r->zrevrank('racer_scores', 'Norem');
        echo $res12 . PHP_EOL;
        // >>> 2
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - $key: string,
    - $membersAndScoresDictionary: array
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - $key: string,
    - $member: string
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - $key: string,
    - $member: string
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

```
# Recreate the three remaining racers so this example runs on its own.
r.del('racer_scores')
r.zadd('racer_scores', [[10, 'Norem'], [10, 'Royce'], [14, 'Prickett']])
res11 = r.zrank('racer_scores', 'Norem')
puts res11 # >>> 0
res12 = r.zrevrank('racer_scores', 'Norem')
puts res12 # >>> 2
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: String,
    - *args: [Float, String], Array<[Float, String]>, // a single [score, member] pair or an array of pairs
    - nx: Boolean, // Only add elements that do not already exist
    - xx: Boolean, // Only update elements that already exist
    - lt: Boolean, // Only update existing elements if the new score is less than the current score
    - gt: Boolean, // Only update existing elements if the new score is greater than the current score
    - ch: Boolean, // Return the total number of elements changed
    - incr: Boolean // ZADD acts like ZINCRBY
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - key: String,
    - member: String,
    - with_score: Boolean // include score in output
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - key: String,
    - member: String,
    - with_score: Boolean // include score in output
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

```
        // Recreate the three remaining racers so this example runs on its own.
        let _: () = r.del("racer_scores").expect("Failed to del");
        let _: usize = r
            .zadd_multiple(
                "racer_scores",
                &[(10, "Norem"), (10, "Royce"), (14, "Prickett")],
            )
            .expect("Failed to zadd");
        if let Ok(res) = r.zrank("racer_scores", "Norem") {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 0
            }
        }
        if let Ok(res) = r.zrevrank("racer_scores", "Norem") {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 2
            }
        }
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S
  - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)]
  - 
                                            
                                            zadd_options(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - key: K,
    - member: M
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - key: K,
    - member: M
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

```
        // Recreate the three remaining racers so this example runs on its own.
        let _: () = r.del("racer_scores").await.expect("Failed to del");
        let _: usize = r
            .zadd_multiple(
                "racer_scores",
                &[(10, "Norem"), (10, "Royce"), (14, "Prickett")],
            )
            .await
            .expect("Failed to zadd");
        if let Ok(res) = r.zrank("racer_scores", "Norem").await {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 0
            }
        }
        if let Ok(res) = r.zrevrank("racer_scores", "Norem").await {
            let res: Option<usize> = res;
            if let Some(res) = res {
                println!("{res}"); // >>> 2
            }
        }
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S
  - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)]
  - 
                                            
                                            zadd_options(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by ascending scores.
                                    [ZRANK](https://redis.io/docs/latest/commands/zrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrank(
                                            
                                            
                                            
    - key: K,
    - member: M
- 
                                            
                                            zrank(
                                            
                                            
                                            
- 
                    
                        Returns the index of a member in a sorted set ordered by descending scores.
                                    [ZREVRANK](https://redis.io/docs/latest/commands/zrevrank/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zrevrank(
                                            
                                            
                                            
    - key: K,
    - member: M
- 
                                            
                                            zrevrank(
                                            
                                            
                                            

## 
  Lexicographical scores
  
    
  

In version Redis 2.8, a new feature was introduced that allows
getting ranges lexicographically, assuming elements in a sorted set are all
inserted with the same identical score (elements are compared with the C
`memcmp` function, so it is guaranteed that there is no collation, and every
Redis instance will reply with the same output).

The main commands to operate with lexicographical ranges are [`ZRANGEBYLEX`](/docs/latest/commands/zrangebylex/),
[`ZREVRANGEBYLEX`](/docs/latest/commands/zrevrangebylex/), [`ZREMRANGEBYLEX`](/docs/latest/commands/zremrangebylex/) and [`ZLEXCOUNT`](/docs/latest/commands/zlexcount/).

For example, let's add again our list of famous racers, but this time
using a score of zero for all the elements. We'll see that because of the sorted sets ordering rules, they are already sorted lexicographically. Using [`ZRANGEBYLEX`](/docs/latest/commands/zrangebylex/) we can ask for lexicographical ranges:

> ZADD racer_scores 0 "Norem" 0 "Sam-Bodden" 0 "Royce" 0 "Castilla" 0 "Prickett" 0 "Ford"
(integer) 3
> ZRANGE racer_scores 0 -1
1) "Castilla"
2) "Ford"
3) "Norem"
4) "Prickett"
5) "Royce"
6) "Sam-Bodden"
> ZRANGEBYLEX racer_scores [A [L
1) "Castilla"
2) "Ford"

- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)

[and](https://redis.io/docs/latest/develop/tools/insight/)

**Redis Insight**
[.](https://redis.io/docs/latest/develop/tools/redis-for-vscode/)

**Redis for VS Code**```
res13 = r.zadd(
    "racer_scores",
    {
        "Norem": 0,
        "Sam-Bodden": 0,
        "Royce": 0,
        "Ford": 0,
        "Prickett": 0,
        "Castilla": 0,
    },
)
print(res13)  # >>> 3
res14 = r.zrange("racer_scores", 0, -1)
print(res14)  # >>> ['Castilla', 'Ford', 'Norem', 'Prickett', 'Royce', 'Sam-Bodden']
res15 = r.zrangebylex("racer_scores", "[A", "[L")
print(res15)  # >>> ['Castilla', 'Ford']
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - name: KeyT,
    - mapping: Mapping[AnyKeyT, EncodableT],
    - nx: bool = False,
    - xx: bool = False,
    - ch: bool = False,
    - incr: bool = False,
    - gt: bool = False,
    - lt: bool = False
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - name: KeyT,
    - start: EncodableT,
    - end: EncodableT,
    - desc: bool = False,
    - withscores: bool = False,
    - score_cast_func: Union[type, Callable] = float,
    - byscore: bool = False,
    - bylex: bool = False,
    - offset: Optional[int] = None,
    - num: Optional[int] = None
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - name: KeyT,
    - min: EncodableT,
    - max: EncodableT,
    - start: Optional[int] = None,
    - num: Optional[int] = None
- 
                                            
                                            zrangebylex(
                                            
                                            
                                            

```
const res13 = await client.zAdd('racer_scores', [
  { score: 0, value: 'Norem' },
  { score: 0, value: 'Sam-Bodden' },
  { score: 0, value: 'Royce' },
  { score: 0, value: 'Ford' },
  { score: 0, value: 'Prickett' },
  { score: 0, value: 'Castilla' }
]);
console.log(res13);  // >>> 3
const res14 = await client.zRange('racer_scores', 0, -1);
console.log(res14);  // >>> ['Castilla', 'Ford', 'Norem', 'Prickett', 'Royce', 'Sam-Bodden']
const res15 = await client.zRangeByLex('racer_scores', '[A', '[L');
console.log(res15);  // >>> ['Castilla', 'Ford']
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZADD(
                                            
                                            
                                            
    - key: RedisArgument,
    - members: SortedSetMember | Array<SortedSetMember>,
    - options?: ZAddOptions
- 
                                            
                                            ZADD(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRANGE(
                                            
                                            
                                            
    - key: RedisArgument,
    - min: RedisArgument | number,
    - max: RedisArgument | number,
    - options?: ZRangeOptions
  - 
                                            
                                            ZRANGE_WITHSCORES(
                                            
                                            
                                            
    - ...args: Parameters<typeof ZRANGE.parseCommand>
- 
                                            
                                            ZRANGE(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRANGEBYLEX(
                                            
                                            
                                            
    - key: RedisArgument,
    - min: RedisArgument,
    - max: RedisArgument,
    - options?: ZRangeByLexOptions
- 
                                            
                                            ZRANGEBYLEX(
                                            
                                            
                                            

```
    long res13 = jedis.zadd("racer_scores", new HashMap<String,Double>() {{
      put("Norem", 0d);
      put("Sam-Bodden", 0d);
      put("Royce", 0d);
      put("Ford", 0d);
      put("Prickett", 0d);
      put("Castilla", 0d);
    }});
    System.out.println(res13); // >>> 3
    List<String> res14 = jedis.zrange("racer_scores", 0, -1);
    System.out.println(res14); // >>> [Castilla, Ford, Norem, Prickett, Royce, Sam-Bodden]
    List<String> res15 = jedis.zrangeByLex("racer_scores", "[A", "[L");
    System.out.println(res15); // >>> [Castilla, Ford]
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - score: double,
    - member: byte[]
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - score: double,
    - params: byte[] member final ZAddParams
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - scoreMembers: Map<byte[], Double>
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: byte[],
    - scoreMembers: Map<byte[], Double>,
    - params: ZAddParams
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: String,
    - score: double,
    - member: String
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: byte[],
    - zRangeParams: ZRangeParams
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: String,
    - start: long,
    - stop: long
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - zRangeParams: ZRangeParams
- 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangeByLex(
                                            
                                            
                                            
    - key: byte[],
    - min: byte[],
    - offset: byte[] max final int,
    - count: int
  - 
                                            
                                            zrangeByLex(
                                            
                                            
                                            
    - key: String,
    - min: String,
    - max: String
  - 
                                            
                                            zrangeByLex(
                                            
                                            
                                            
    - key: String,
    - min: String,
    - offset: String max final int,
    - count: int
- 
                                            
                                            zrangeByLex(
                                            
                                            
                                            

```
            CompletableFuture<Void> zaddLex = asyncCommands.zadd("racer_scores", ScoredValue.just(0d, "Norem"),
                    ScoredValue.just(0d, "Sam-Bodden"), ScoredValue.just(0d, "Royce"), ScoredValue.just(0d, "Castilla"),
                    ScoredValue.just(0d, "Prickett"), ScoredValue.just(0d, "Ford")).thenCompose(res7 -> {
                        System.out.println(res7); // >>> 3
                        return asyncCommands.zrange("racer_scores", 0, -1);
                    }).thenCompose(res8 -> {
                        System.out.println(res8);
                        // >>> [Castilla, Ford, Norem, Prickett, Royce, Sam-Bodden]
                        return asyncCommands.zrangebylex("racer_scores", Range.create("A", "L"));
                    })
                    .thenAccept(System.out::println)
                    // >>> [Castilla, Ford]
                    .toCompletableFuture();
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends V> // the range.
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String,
    - offset: long,
    - count: long
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends V>, // the range.
    - limit: Limit // the limit.
- 
                                            
                                            zrangebylex(
                                            
                                            
                                            

```
            Mono<Void> zaddLex = reactiveCommands
                    .zadd("racer_scores", ScoredValue.just(0d, "Norem"), ScoredValue.just(0d, "Sam-Bodden"),
                            ScoredValue.just(0d, "Royce"), ScoredValue.just(0d, "Castilla"),
                            ScoredValue.just(0d, "Prickett"), ScoredValue.just(0d, "Ford"))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 3
                    }).flatMap(v -> reactiveCommands.zrange("racer_scores", 0, -1).collectList()).doOnNext(result -> {
                        System.out.println(result);
                        // >>> [Castilla, Ford, Norem, Prickett, Royce, Sam-Bodden]
                    }).flatMap(v -> reactiveCommands.zrangebylex("racer_scores", Range.create("A", "L")).collectList())
                    .doOnNext(result -> {
                        System.out.println(result); // >>> [Castilla, Ford]
                    }).then();
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
  - 
                                            
                                            zrangeWithScores(
                                            
                                            
                                            
    - channel: ScoredValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K, // the key.
    - start: long, // the start.
    - stop: long // the stop.
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends V> // the range.
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - min: String,
    - max: String,
    - offset: long,
    - count: long
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K, // the key.
    - range: Range<? extends V>, // the range.
    - limit: Limit // the limit.
- 
                                            
                                            zrangebylex(
                                            
                                            
                                            

```
	res13, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Norem", Score: 0},
		redis.Z{Member: "Sam-Bodden", Score: 0},
		redis.Z{Member: "Royce", Score: 0},
		redis.Z{Member: "Ford", Score: 0},
		redis.Z{Member: "Prickett", Score: 0},
		redis.Z{Member: "Castilla", Score: 0},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res13) // >>> 3
	res14, err := rdb.ZRange(ctx, "racer_scores", 0, -1).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res14)
	// >>> [Castilla Ford Norem Prickett Royce Sam-Bodden]
	res15, err := rdb.ZRangeByLex(ctx, "racer_scores", &redis.ZRangeBy{
		Min: "[A", Max: "[L",
	}).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res15) // >>> [Castilla Ford]
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            ZAdd(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - members: ...Z
- 
                                            
                                            ZAdd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRange(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
  - 
                                            
                                            ZRangeWithScores(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - start: Any,
    - stop: int64
- 
                                            
                                            ZRange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            ZRangeByLex(
                                            
                                            
                                            
    - ctx: context.Context,
    - key: string,
    - opt: *ZRangeBy
- 
                                            
                                            ZRangeByLex(
                                            
                                            
                                            

```
        long res13 = db.SortedSetAdd("racer_scores", [
            new("Norem", 0),
            new("Sam-Bodden", 0),
            new("Royce", 0),
            new("Ford", 0),
            new("Prickett", 0),
            new("Castilla", 0)
        ]);
        Console.WriteLine(res13); // >>> 3
        RedisValue[] res14 = db.SortedSetRangeByRank("racer_scores", 0, -1);
        Console.WriteLine(string.Join(", ", res14)); // >>> Castilla, Ford, Norem, Pricket, Royce, Sam-Bodden
        RedisValue[] res15 = db.SortedSetRangeByValue("racer_scores", "A", "L", Exclude.None);
        Console.WriteLine(string.Join(", ", res15)); // >>> Castilla, Ford
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: SortedSetWhen, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByRankWithScores(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: long, // The start index to get.
    - stop: long, // The stop index to get.
    - order: Order, // The order to sort by (defaults to ascending).
    - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetRangeByScore(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - start: double, // The minimum score to filter by.
    - stop: double, // The maximum score to filter by.
    - exclude: Exclude, // Which of start and stop to exclude (defaults to both inclusive).
    - order: Order, // The order to sort by (defaults to ascending).
    - skip: long, // How many items to skip.
    - take: long, // How many items to take.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRangeByRank(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            SortedSetRangeByValue(
                                            
                                            
                                            
    - key: RedisKey, // The key of the sorted set.
    - min: RedisValue, // The min value to filter by.
    - max: RedisValue, // The max value to filter by.
    - exclude: Exclude, // Which of min and max to exclude (defaults to both inclusive).
    - skip: long, // How many items to skip.
    - take: long, // How many items to take.
    - flags: CommandFlags // The flags to use for this operation.
- 
                                            
                                            SortedSetRangeByValue(
                                            
                                            
                                            

```
        $res13 = $r->zadd('racer_scores', [
            'Norem' => 0,
            'Sam-Bodden' => 0,
            'Royce' => 0,
            'Ford' => 0,
            'Prickett' => 0,
            'Castilla' => 0,
        ]);
        echo $res13 . PHP_EOL;
        // >>> 3
        $res14 = $r->zrange('racer_scores', 0, -1);
        echo json_encode($res14) . PHP_EOL;
        // >>> ["Castilla","Ford","Norem","Prickett","Royce","Sam-Bodden"]
        $res15 = $r->zrangebylex('racer_scores', '[A', '[L');
        echo json_encode($res15) . PHP_EOL;
        // >>> ["Castilla","Ford"]
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - $key: string,
    - $membersAndScoresDictionary: array
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - $key: string,
    - $start: int|string,
    - $stop: int|string,
    - ?array $options = null: Any
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - $key: string,
    - $start: string,
    - $stop: string,
    - ?array $options = null: Any
- 
                                            
                                            zrangebylex(
                                            
                                            
                                            

```
res13 = r.zadd('racer_scores', [
  [0, 'Norem'],
  [0, 'Sam-Bodden'],
  [0, 'Royce'],
  [0, 'Ford'],
  [0, 'Prickett'],
  [0, 'Castilla']
])
puts res13 # >>> 3
res14 = r.zrange('racer_scores', 0, -1)
puts res14.inspect # >>> ["Castilla", "Ford", "Norem", "Prickett", "Royce", "Sam-Bodden"]
res15 = r.zrangebylex('racer_scores', '[A', '[L')
puts res15.inspect # >>> ["Castilla", "Ford"]
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: String,
    - *args: [Float, String], Array<[Float, String]>, // a single [score, member] pair or an array of pairs
    - nx: Boolean, // Only add elements that do not already exist
    - xx: Boolean, // Only update elements that already exist
    - lt: Boolean, // Only update existing elements if the new score is less than the current score
    - gt: Boolean, // Only update existing elements if the new score is greater than the current score
    - ch: Boolean, // Return the total number of elements changed
    - incr: Boolean // ZADD acts like ZINCRBY
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: String,
    - start: Integer, // start index
    - stop: Integer, // stop index
    - by_score: Boolean, // return members by score
    - by_lex: Boolean, // return members by lexicographical ordering
    - rev: Boolean, // reverse the ordering
    - limit: Array, // [offset, count]
    - with_scores: Boolean // include scores in output
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: String,
    - min: String,
    - max: String,
    - limit: Array // [offset, count]
- 
                                            
                                            zrangebylex(
                                            
                                            
                                            

```
        if let Ok(res) = r.zadd_multiple(
            "racer_scores",
            &[
                (0, "Norem"),
                (0, "Sam-Bodden"),
                (0, "Royce"),
                (0, "Ford"),
                (0, "Prickett"),
                (0, "Castilla"),
            ],
        ) {
            let res: usize = res;
            println!("{res}"); // >>> 3
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1) {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Castilla", "Ford", "Norem", "Prickett", "Royce", "Sam-Bodden"]
        }
        if let Ok(res) = r.zrangebylex("racer_scores", "[A", "[L") {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Castilla", "Ford"]
        }
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S
  - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)]
  - 
                                            
                                            zadd_options(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
  - 
                                            
                                            zrangebylex_limit(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM,
    - offset: isize,
    - count: isize
- 
                                            
                                            zrangebylex(
                                            
                                            
                                            

```
        if let Ok(res) = r
            .zadd_multiple(
                "racer_scores",
                &[
                    (0, "Norem"),
                    (0, "Sam-Bodden"),
                    (0, "Royce"),
                    (0, "Ford"),
                    (0, "Prickett"),
                    (0, "Castilla"),
                ],
            )
            .await
        {
            let res: usize = res;
            println!("{res}"); // >>> 3
        }
        if let Ok(res) = r.zrange("racer_scores", 0, -1).await {
            let res: Vec<String> = res;
            println!("{res:?}");
            // >>> ["Castilla", "Ford", "Norem", "Prickett", "Royce", "Sam-Bodden"]
        }
        if let Ok(res) = r.zrangebylex("racer_scores", "[A", "[L").await {
            let res: Vec<String> = res;
            println!("{res:?}"); // >>> ["Castilla", "Ford"]
        }
```
- 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                                            
                                            zadd(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S
  - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)]
  - 
                                            
                                            zadd_options(
                                            
                                            
                                            
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions
- 
                                            
                                            zadd(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a range of indexes.
                                    [ZRANGE](https://redis.io/docs/latest/commands/zrange/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrange(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
  - 
                                            
                                            zrange_withscores(
                                            
                                            
                                            
    - key: K,
    - start: isize,
    - stop: isize
- 
                                            
                                            zrange(
                                            
                                            
                                            
- 
                    
                        Returns members in a sorted set within a lexicographical range.
                                    [ZRANGEBYLEX](https://redis.io/docs/latest/commands/zrangebylex/)
                                (
                                            [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow)
                                        )
  - 
                                            
                                            zrangebylex(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM
  - 
                                            
                                            zrangebylex_limit(
                                            
                                            
                                            
    - key: K,
    - min: M,
    - max: MM,
    - offset: isize,
    - count: isize
- 
                                            
                                            zrangebylex(
                                            
                                            
                                            

Ranges can be inclusive or exclusive (depending on the first character),
also string infinite and minus infinite are specified respectively with
the `+` and `-` strings. See the documentation for more information.

This feature is important because it allows us to use sorted sets as a generic
index. For example, if you want to index elements by a 128-bit unsigned
integer argument, all you need to do is to add elements into a sorted
set with the same score (for example 0) but with a 16 byte prefix
consisting of **the 128 bit number in big endian**. Since numbers in big
endian, when ordered lexicographically (in raw bytes order) are actually
ordered numerically as well, you can ask for ranges in the 128 bit space,
and get the element's value discarding the prefix

## 
  Updating the score: leaderboards
  
    
  

Just a final note about sorted sets before switching to the next topic.
Sorted sets' scores can be updated at any time. Just calling [`ZADD`](/docs/latest/commands/zadd/) against
an element already included in the sorted set will update its score
(and position) with O(log(N)) time complexity.  As such, sorted sets are suitable
when there are tons of updates.

Because of this characteristic a common use case is leaderboards. The typical application is a Facebook game where you combine the ability to take users sorted by their high score, plus the get-rank operation, in order to show the top-N users, and the user rank in the leader board (e.g., "you are the #4932 best score here").

## 
  Examples
  
    
  

- There are two ways we can use a sorted set to represent a leaderboard. If we know a racer's new score, we can update it directly via the [`ZADD`](/docs/latest/commands/zadd/) command. However, if we want to add points to an existing score, we can use the[`ZINCRBY`](/docs/latest/commands/zincrby/) command.> ZADD racer_scores 100 "Wood" (integer) 1 > ZADD racer_scores 100 "Henshaw" (integer) 1 > ZADD racer_scores 150 "Henshaw" (integer) 0 > ZINCRBY racer_scores 50 "Wood" "150" > ZINCRBY racer_scores 50 "Henshaw" "200" 
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
 
                            [Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/)
                        Also, check out our other client tools[**Redis Insight**](https://redis.io/docs/latest/develop/tools/insight/) and[**Redis for VS Code**](https://redis.io/docs/latest/develop/tools/redis-for-vscode/) .```
res16 = r.zadd("racer_scores", {"Wood": 100})
print(res16)  # >>> 1
res17 = r.zadd("racer_scores", {"Henshaw": 100})
print(res17)  # >>> 1
res18 = r.zadd("racer_scores", {"Henshaw": 150})
print(res18)  # >>> 0
res19 = r.zincrby("racer_scores", 50, "Wood")
print(res19)  # >>> 150.0
res20 = r.zincrby("racer_scores", 50, "Henshaw")
print(res20)  # >>> 200.0
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - name: KeyT,
      - mapping: Mapping[AnyKeyT, EncodableT],
      - nx: bool = False,
      - xx: bool = False,
      - ch: bool = False,
      - incr: bool = False,
      - gt: bool = False,
      - lt: bool = False
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - name: KeyT,
      - amount: float,
      - value: EncodableT
  - 
                                            
                                            zincrby(
                                            
                                            
                                            
 ```
const res16 = await client.zAdd('racer_scores', { score: 100, value: 'Wood' });
console.log(res16);  // >>> 1
const res17 = await client.zAdd('racer_scores', { score: 100, value: 'Henshaw' });
console.log(res17);  // >>> 1
const res18 = await client.zAdd('racer_scores', { score: 150, value: 'Henshaw' }, { nx: true });
console.log(res18);  // >>> 0
const res19 = await client.zIncrBy('racer_scores', 50, 'Wood');
console.log(res19);  // >>> 150.0
const res20 = await client.zIncrBy('racer_scores', 50, 'Henshaw');
console.log(res20);  // >>> 200.0
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            ZADD(
                                            
                                            
                                            
      - key: RedisArgument,
      - members: SortedSetMember | Array<SortedSetMember>,
      - options?: ZAddOptions
  - 
                                            
                                            ZADD(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            ZINCRBY(
                                            
                                            
                                            
      - key: RedisArgument,
      - increment: number,
      - member: RedisArgument
  - 
                                            
                                            ZINCRBY(
                                            
                                            
                                            
 ```
    long res16 = jedis.zadd("racer_scores", 100d, "Wood");
    System.out.println(res16); // >>> 1
    long res17 = jedis.zadd("racer_scores", 100d, "Henshaw");
    System.out.println(res17); // >>> 1
    long res18 = jedis.zadd("racer_scores", 150d, "Henshaw");
    System.out.println(res18); // >>> 0
    double res19 = jedis.zincrby("racer_scores", 50d, "Wood");
    System.out.println(res19); // >>> 150.0
    double res20 = jedis.zincrby("racer_scores", 50d, "Henshaw");
    System.out.println(res20); // >>> 200.0
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: byte[],
      - score: double,
      - member: byte[]
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: byte[],
      - score: double,
      - params: byte[] member final ZAddParams
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: byte[],
      - scoreMembers: Map<byte[], Double>
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: byte[],
      - scoreMembers: Map<byte[], Double>,
      - params: ZAddParams
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: String,
      - score: double,
      - member: String
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - key: byte[],
      - increment: double,
      - member: byte[]
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - key: byte[],
      - increment: double,
      - params: byte[] member final ZIncrByParams
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - key: String,
      - increment: double,
      - member: String
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - key: String,
      - increment: double,
      - params: String member final ZIncrByParams
  - 
                                            
                                            zincrby(
                                            
                                            
                                            
 ```
            CompletableFuture<Void> leaderboard = asyncCommands.zadd("racer_scores", ScoredValue.just(100, "Wood"))
                    .thenCompose(res9 -> {
                        System.out.println(res9); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(100, "Henshaw"));
                    }).thenCompose(res10 -> {
                        System.out.println(res10); // >>> 1
                        return asyncCommands.zadd("racer_scores", ScoredValue.just(150, "Henshaw"));
                    }).thenCompose(res11 -> {
                        System.out.println(res11); // >>> 0
                        return asyncCommands.zincrby("racer_scores", 50, "Wood");
                    }).thenCompose(res12 -> {
                        System.out.println(res12); // >>> 150
                        return asyncCommands.zincrby("racer_scores", 50, "Henshaw");
                    })
                    .thenAccept(System.out::println) // >>> 200
                    .toCompletableFuture();
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - score: double,
      - member: V
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - scoresAndValues: Object...
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - scoredValues: ScoredValue<V>... // the scored values.
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - zAddArgs: ZAddArgs, // arguments for zadd.
      - score: double,
      - member: V
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - zAddArgs: ZAddArgs, // arguments for zadd.
      - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - key: K, // the key.
      - amount: double, // the increment type: long.
      - member: V // the member type: value.
  - 
                                            
                                            zincrby(
                                            
                                            
                                            
 ```
            Mono<Void> leaderboard = reactiveCommands.zadd("racer_scores", ScoredValue.just(100, "Wood"))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 1
                    }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(100, "Henshaw")))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 1
                    }).flatMap(v -> reactiveCommands.zadd("racer_scores", ScoredValue.just(150, "Henshaw")))
                    .doOnNext(result -> {
                        System.out.println(result); // >>> 0
                    }).flatMap(v -> reactiveCommands.zincrby("racer_scores", 50, "Wood")).doOnNext(result -> {
                        System.out.println(result); // >>> 150
                    }).flatMap(v -> reactiveCommands.zincrby("racer_scores", 50, "Henshaw")).doOnNext(result -> {
                        System.out.println(result); // >>> 200
                    }).then();
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - score: double,
      - member: V
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - scoresAndValues: Object...
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - scoredValues: ScoredValue<V>... // the scored values.
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - zAddArgs: ZAddArgs, // arguments for zadd.
      - score: double,
      - member: V
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K, // the ke.
      - zAddArgs: ZAddArgs, // arguments for zadd.
      - scoresAndValues: Object...
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - key: K, // the key.
      - amount: double, // the increment type: long.
      - member: V // the member type: value.
  - 
                                            
                                            zincrby(
                                            
                                            
                                            
 ```
	res16, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Wood", Score: 100},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res16) // >>> 1
	res17, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Henshaw", Score: 100},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res17) // >>> 1
	res18, err := rdb.ZAdd(ctx, "racer_scores",
		redis.Z{Member: "Henshaw", Score: 150},
	).Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res18) // >>> 0
	res19, err := rdb.ZIncrBy(ctx, "racer_scores", 50, "Wood").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res19) // >>> 150
	res20, err := rdb.ZIncrBy(ctx, "racer_scores", 50, "Henshaw").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println(res20) // >>> 200
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            ZAdd(
                                            
                                            
                                            
      - ctx: context.Context,
      - key: string,
      - members: ...Z
  - 
                                            
                                            ZAdd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            ZIncrBy(
                                            
                                            
                                            
      - ctx: context.Context,
      - key: string,
      - increment: float64,
      - member: string
  - 
                                            
                                            ZIncrBy(
                                            
                                            
                                            
 ```
        bool res16 = db.SortedSetAdd("racer_scores", "Wood", 100);
        Console.WriteLine(res16); // >>> True
        bool res17 = db.SortedSetAdd("racer_scores", "Henshaw", 100);
        Console.WriteLine(res17); // >>> True
        bool res18 = db.SortedSetAdd("racer_scores", "Henshaw", 150);
        Console.WriteLine(res18); // >>> False
        double res19 = db.SortedSetIncrement("racer_scores", "Wood", 50);
        Console.WriteLine(res19); // >>> 150.0
        double res20 = db.SortedSetIncrement("racer_scores", "Henshaw", 50);
        Console.WriteLine(res20); // >>> 200.0
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
      - key: RedisKey, // The key of the sorted set.
      - member: RedisValue,
      - score: double,
      - flags: CommandFlags // The flags to use for this operation.
    - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
      - key: RedisKey, // The key of the sorted set.
      - member: RedisValue,
      - score: double,
      - when: When, // What conditions to add the element under (defaults to always).
      - flags: CommandFlags // The flags to use for this operation.
    - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
      - key: RedisKey, // The key of the sorted set.
      - member: RedisValue,
      - score: double,
      - when: SortedSetWhen, // What conditions to add the element under (defaults to always).
      - flags: CommandFlags // The flags to use for this operation.
    - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
      - key: RedisKey, // The key of the sorted set.
      - values: SortedSetEntry[], // The members and values to add to the sorted set.
      - flags: CommandFlags // The flags to use for this operation.
    - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
      - key: RedisKey, // The key of the sorted set.
      - values: SortedSetEntry[], // The members and values to add to the sorted set.
      - when: When, // What conditions to add the element under (defaults to always).
      - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetAdd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            SortedSetIncrement(
                                            
                                            
                                            
      - key: RedisKey, // The key of the sorted set.
      - member: RedisValue, // The member to increment.
      - value: double, // The amount to increment by.
      - flags: CommandFlags // The flags to use for this operation.
    - 
                                            
                                            SortedSetIncrement(
                                            
                                            
                                            
      - key: Any, // The key of the sorted set.
      - member: Any, // The member to increment.
      - -value: Any,
      - flags: Any // The flags to use for this operation.
    - 
                                            
                                            SortedSetIncrement(
                                            
                                            
                                            
      - key: RedisKey, // The key of the sorted set.
      - member: RedisValue, // The member to increment.
      - value: double, // The amount to increment by.
      - flags: CommandFlags // The flags to use for this operation.
  - 
                                            
                                            SortedSetIncrement(
                                            
                                            
                                            
 ```
        $res16 = $r->zadd('racer_scores', ['Wood' => 100]);
        echo $res16 . PHP_EOL;
        // >>> 1
        $res17 = $r->zadd('racer_scores', ['Henshaw' => 100]);
        echo $res17 . PHP_EOL;
        // >>> 1
        $res18 = $r->zadd('racer_scores', ['Henshaw' => 150]);
        echo $res18 . PHP_EOL;
        // >>> 0
        $res19 = $r->zincrby('racer_scores', 50, 'Wood');
        echo $res19 . PHP_EOL;
        // >>> 150
        $res20 = $r->zincrby('racer_scores', 50, 'Henshaw');
        echo $res20 . PHP_EOL;
        // >>> 200
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - $key: string,
      - $membersAndScoresDictionary: array
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - $key: string,
      - $increment: int,
      - $member: string
  - 
                                            
                                            zincrby(
                                            
                                            
                                            
 ```
res16 = r.zadd('racer_scores', [[100, 'Wood']])
puts res16 # >>> 1
res17 = r.zadd('racer_scores', [[100, 'Henshaw']])
puts res17 # >>> 1
res18 = r.zadd('racer_scores', [[150, 'Henshaw']])
puts res18 # >>> 0
res19 = r.zincrby('racer_scores', 50, 'Wood')
puts res19 # >>> 150.0
res20 = r.zincrby('racer_scores', 50, 'Henshaw')
puts res20 # >>> 200.0
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: String,
      - *args: [Float, String], Array<[Float, String]>, // a single [score, member] pair or an array of pairs
      - nx: Boolean, // Only add elements that do not already exist
      - xx: Boolean, // Only update elements that already exist
      - lt: Boolean, // Only update existing elements if the new score is less than the current score
      - gt: Boolean, // Only update existing elements if the new score is greater than the current score
      - ch: Boolean, // Return the total number of elements changed
      - incr: Boolean // ZADD acts like ZINCRBY
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincrby(
                                            
                                            
                                            
      - key: String,
      - increment: Float,
      - member: String
  - 
                                            
                                            zincrby(
                                            
                                            
                                            
 ```
        if let Ok(res) = r.zadd("racer_scores", "Wood", 100) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 100) {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 150) {
            let res: usize = res;
            println!("{res}"); // >>> 0
        }
        if let Ok(res) = r.zincr("racer_scores", "Wood", 50) {
            let res: f64 = res;
            println!("{res}"); // >>> 150
        }
        if let Ok(res) = r.zincr("racer_scores", "Henshaw", 50) {
            let res: f64 = res;
            println!("{res}"); // >>> 200
        }
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K,
      - member: M,
      - score: S
    - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
      - key: K,
      - items: &'a [(S, M)]
    - 
                                            
                                            zadd_options(
                                            
                                            
                                            
      - key: K,
      - member: M,
      - score: S,
      - options: &'a SortedSetAddOptions
    - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
      - key: K,
      - items: &'a [(S, M)],
      - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincr(
                                            
                                            
                                            
      - key: K,
      - member: M,
      - delta: D
  - 
                                            
                                            zincr(
                                            
                                            
                                            
 ```
        if let Ok(res) = r.zadd("racer_scores", "Wood", 100).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 100).await {
            let res: usize = res;
            println!("{res}"); // >>> 1
        }
        if let Ok(res) = r.zadd("racer_scores", "Henshaw", 150).await {
            let res: usize = res;
            println!("{res}"); // >>> 0
        }
        if let Ok(res) = r.zincr("racer_scores", "Wood", 50).await {
            let res: f64 = res;
            println!("{res}"); // >>> 150
        }
        if let Ok(res) = r.zincr("racer_scores", "Henshaw", 50).await {
            let res: f64 = res;
            println!("{res}"); // >>> 200
        }
```
  - 
                    
                        Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
                                    [ZADD](https://redis.io/docs/latest/commands/zadd/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zadd(
                                            
                                            
                                            
      - key: K,
      - member: M,
      - score: S
    - 
                                            
                                            zadd_multiple(
                                            
                                            
                                            
      - key: K,
      - items: &'a [(S, M)]
    - 
                                            
                                            zadd_options(
                                            
                                            
                                            
      - key: K,
      - member: M,
      - score: S,
      - options: &'a SortedSetAddOptions
    - 
                                            
                                            zadd_multiple_options(
                                            
                                            
                                            
      - key: K,
      - items: &'a [(S, M)],
      - options: &'a SortedSetAddOptions
  - 
                                            
                                            zadd(
                                            
                                            
                                            
  - 
                    
                        Increments the score of a member in a sorted set.
                                    [ZINCRBY](https://redis.io/docs/latest/commands/zincrby/)
                                (
                                            [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write)
                                        ,
                                            [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset)
                                        ,
                                            [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast)
                                        )
    - 
                                            
                                            zincr(
                                            
                                            
                                            
      - key: K,
      - member: M,
      - delta: D
  - 
                                            
                                            zincr(
                                            
                                            
                                            
- 
                    
                        

You'll see that [`ZADD`](/docs/latest/commands/zadd/) returns 0 when the member already exists (the score is updated), while [`ZINCRBY`](/docs/latest/commands/zincrby/) returns the new score. The score for racer Henshaw went from 100, was changed to 150 with no regard for what score was there before, and then was incremented by 50 to 200.

## 
  Performance
  
    
  

Most sorted set operations are O(log(n)), where *n* is the number of members.

Exercise some caution when running the [`ZRANGE`](/docs/latest/commands/zrange/) command with large returns values (e.g., in the tens of thousands or more).
This command's time complexity is O(log(n) + m), where *m* is the number of results returned.

## 
  Alternatives
  
    
  

Redis sorted sets are sometimes used for indexing other Redis data structures.
If you need to index and query your data, consider the [JSON](/docs/latest/develop/data-types/json/) data type and the [Redis Search](/docs/latest/develop/ai/search-and-query/) features.

## 
  Learn more
  
    
  

- [Redis Sorted Sets Explained](https://www.youtube.com/watch?v=MUKlxdBQZ7g) is an entertaining introduction to sorted sets in Redis.
- [Redis University's RU101](https://university.redis.com/courses/ru101/) explores Redis sorted sets in detail.
