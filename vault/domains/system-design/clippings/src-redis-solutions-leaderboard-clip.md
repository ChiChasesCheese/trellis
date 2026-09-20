---
title: Fast leaderboards with Redis solutions
source: https://redis.io/solutions/leaderboards/
published: '2025-06-14'
site: Redis
clipped: '2026-09-20'
---

# Fast leaderboards with Redis solutions

97% believe in it. 4% have built it. New research: State of context engineering.

The concept of a leaderboard—a scoreboard showing the ranked names and current scores (or other data points) of the leading competitors—is essential to the world of computer gaming, but leaderboards are now about more than just games. They are about gamification, a broader implementation that can include any group of people with a common goal (coworkers, students, sales groups, fitness groups, volunteers, and so on).

Leaderboards can encourage healthy competition in a group by openly displaying the current ranking of each group member. They also provide a clear way to view the ongoing achievements of the entire team as members move towards a goal.

Gamification of tasks and goals via leaderboards is a great way to motivate people by providing them with constant feedback of where they rank in comparison to other group members. Done well, this can lead to healthy competition that builds group cohesion.

Here’s a graphic example of a simple leaderboard that a company might use to motivate employees to participate in its employer health program.

In this example, employees can see the top ranking competitors along with their current scores. They can also see the amount of time left in the contest and the motivational prizes. Of course, as the data changes (as users upload verified step counts) the rankings change in real time.

In our internet-connected world, leaderboards for popular games can be shared by hundreds of thousands, even millions, of competitors. The same applies to non-traditional uses of leaderboards, such as fitness and health applications and social media, or internal organizational tasks such as customer service, logistics, or fraud mitigation.

The data used for leaderboards is constantly updated and users want to see the data sliced in many ways. That makes leaderboards a great example of real-time analytics in action, as well as a showcase for the speed at which your data layer handles reads, writes, sorting, and other key operations.

Providing this data in real time and keeping the system available is beyond the scope of many web technologies. However, this is a challenge that Redis Enterprise solves with data structures built for use cases like these, and with the variety of deployment options that Redis Enterprise provides.

Sorted Sets (ZSETs) within Redis are a built-in data structure that makes leaderboards simple to create and manipulate.

Redis Enterprise is based on a shared-nothing, symmetric architecture that lets dataset sizes grow linearly and seamlessly without requiring changes to the application code.

Redis Enterprise offers multiple models of high availability and lets you deploy Redis in a geographic distribution manner while enabling local latencies for your users when needed.

Multiple persistence options (AOF per write or per second and snapshots) that don’t impact performance ensure that you don’t have to rebuild your database servers after failures.

Support for [extremely large datasets](/software/) with the use of intelligent tiered access to memory (RAM, persistent memory or Flash) ensures that you can scale your datasets to meet the demands of your users without significantly impacting performance.

Creating a Sorted Set is easy using the Redis [ZADD](/docs/latest/commands/zadd/) command. For example, imagine adding a set of players to a leaderboard. Each player consists of a screen name and the player’s score, which will change continually over time

Adding a player to a Sorted Set is as easy as using the ZADD command and passing the name of the set, a score and the player’s name:

If the set doesn’t already exist, Redis will create it. If it does exist, then Redis adds new data to the existing set. Every item in the Sorted Set must be unique, so if the player name (member) doesn’t exist, then it will be added to the set. But if the member already exists, then its value will be set to the new value provided. The built-in [Sorted Set commands](/docs/latest/develop/data-types/sorted-sets/) let you perform quick, native sorting and reporting operations easily.

For example, the ZRANGE command returns a range of members. ZRANGEBYSCORE returns a range of members within a range of scores. ZRANK returns the ranking of a specified member.

Redis makes it easy to increment the score of any player using the ZINCRBY command, passing in the member name and the amount by which to increment the score.

Furthermore, you can manage multiple Sorted Sets for your game/application. For example, a global Sorted Set includes the aggregated scores across all tournaments and then multiple Sorted Sets, per each tournament. You can then use Redis’ unique capability for operation between Sorted Sets, for instance [ZUNIONSTORE](/docs/latest/commands/zunionstore/) for union operation with and without weights.

These simple data examples don’t display graphical type data, but that is part of the power of Redis Sorted Set: it’s pure data in memory and not tied to any view. That means you can use the data to display it any way you like.

Let’s take a quick high-level look at how to implement a leaderboard in Node.js alongside a previously existing web app. With Node Package Manager (NPM), it’s easy to add Redis to your web app using the simple command npm install redis.

Once the Redis Node packages are installed into your web app project, you can access Redis functionality via a JavaScript API. (The official docs at [the node_redis Github repository](https://github.com/NodeRedis/node_redis) can help you get started.)

To demonstrate, let’s create a simple in-memory database using the Sorted Set. We will create members named player: [uniqueId], where uniqueId is an integer value that could easily be generated by your JavaScript or Python code when a user joins the competition.

The score can be any numeric data you want to use to rank the players (daily steps in a company health program, aliens shot down in a computer game and so on).

Now look at a bit of Node.js code that you can use to display the data.

You can create a dataset that can be sliced by numerous variables. To do so, it’s helpful to store data in a structure that represents each competitor. Redis provides just such a structure, called a Hash. A Hash can hold numerous name-value pairs that are associated with one key.

You can use a simple numeric key as a unique identifier in your hash, and then associate that unique key with a Sorted Set, which will contain the score and the key. In this way, you can quickly obtain the score for your top competitors or a range of competitors. Then, if you want more data, you can easily obtain it from the Hash using the key value stored in the Sorted Set.

Next, create a new Hash named with a key of player:100 and add a screenName property that has the value Fred. You could just make the hash key 100, but using the format of [stringID:IntegerID] makes it a bit more readable. When you add another player, you’ll create a new Hash key, like player:101.

If you want to retrieve all the properties and values (name-value pairs) stored for a particular hash, simply use this command:

You can see that there is one name-value pair at this time.

The Hash is a flexible structure and it is easy to add properties and values dynamically.

Imagine that you want to save the date the player last logged in:

Now when you call hgetall again you see:

It is just a matter of adding each user to your allPlayers Hash with its own unique ID. Then you can associate those with a Sorted Set that will contain each player’s score.

Once you add the Hashes (player:NNN) then you have your list and you can leverage those player data keys by using them when you add data to the Sorted Set. This is how you leverage the power of the Redis in-memory database to work with huge datasets (millions of players!) that track the rankings of each player, but stays amazingly fast.

Now you can easily implement a solution that pulls the data using Node and the node_redis package so that you can keep the leaderboard fresh on your web app. This work is easy using the node_redis package API, which allows you to pull back the Sorted Set by name (playerRank).

Redis Enterprise is essential for keeping your leaderboard fresh and your users coming back to see their rankings.

Watch our recent Tech Talk on best practices in leaderboards with Redis!
