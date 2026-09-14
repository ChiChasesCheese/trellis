---
title: The What, Why, and When of Single-Table Design with DynamoDB | DeBrie Advisory
source: https://www.alexdebrie.com/posts/dynamodb-single-table/
author: Alex DeBrie Founder; DeBrie Advisory
published: '2020-02-05'
site: alexdebrie.com
clipped: '2026-08-30'
---

# The What, Why, and When of Single-Table Design with DynamoDB | DeBrie Advisory

I've become a big proponent of DynamoDB over the past few years. DynamoDB provides many benefits that other databases don't, such as a flexible pricing model, a stateless connection model that works seamlessly with serverless compute, and consistent response time even as your database scales to enormous size.

Yet data modeling with DynamoDB is tricky for those used to the relational databases that have dominated for the past few decades. There are a number of quirks around data modeling with DynamoDB, but the biggest one is the [recommendation from AWS to use a single table for all of your records](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html#bp-general-nosql-design-concepts).

In this post, we'll do a deep dive on the concepts behind single-table design.

You'll learn:

- [What is single-table design](#what-is-single-table-design)
- [Why single-table design is needed](#the-solution-pre-join-your-data-into-item-collections)
- [The downsides of single-table design](#downsides-of-a-single-table-design)
- [The two times where the downsides of single-table design outweigh the benefits](#when-not-to-use-single-table-design)

I recently did a live debate on this subject on Twitch with Rick Houlihan and Edin Zulich. Check out the recording [here](https://www.twitch.tv/videos/544223958). Rick is more staunchly in the single-table camp, so be sure to watch that as well.

Let's get started!

## What is single-table design[](#what-is-single-table-design)

Before we get too far, let's define single-table design. To do this, we'll take a quick journey through the history of databases. We'll look at some basic modeling in relational databases, then see why you need to model differently in DynamoDB. With this, we'll see the key reason for using single-table design.

At the end of this section, we'll also do a quick look at some other, smaller benefits of single-table design.

### Background on SQL modeling & joins[](#background-on-sql-modeling--joins)

Let's start with our good friend, the relational database.

With relational databases, you generally [normalize](https://en.wikipedia.org/wiki/Database_normalization) your data by creating a table for each type of entity in your application. For example, if you're making an e-commerce application, you'll have one table for Customers and one table for Orders.

Each Order belongs to a certain Customer, and you use [foreign keys](https://en.wikipedia.org/wiki/Foreign_key) to refer from a record in one table to a record in another. These foreign keys act as pointers -- if I need more information about a Customer that placed a particular Order, I can follow the foreign key reference to retrieve items about the Customer.

To follow these pointers, the SQL language for querying relational databases has a concept of *joins*. Joins allow you to combine records from two or more tables at read-time.

### The problem of missing joins in DynamoDB[](#the-problem-of-missing-joins-in-dynamodb)

While convenient, [SQL joins are also expensive](https://www.alexdebrie.com/posts/dynamodb-no-bad-queries/#sql-joins-have-bad-time-complexity). They require scanning large portions of multiple tables in your relational database, comparing different values, and returning a result set.

DynamoDB was built for enormous, high-velocity use cases, such as the [Amazon.com shopping cart](https://www.dynamodbguide.com/the-dynamo-paper/). These use cases can't tolerate the inconsistency and slowing performance of joins as a dataset scales.

DynamoDB closely guards against any operations that won't scale, and there's not a great way to make relational joins scale. Rather than working to make joins scale better, DynamoDB sidesteps the problem by removing the ability to use joins at all.

But as an application developer, you still need some of the benefits of relational joins. And one of the big benefits of joins is the ability to get multiple, heterogenous items from your database in a single request.

In our example above, we want to get both a Customer record and all Orders for the customer. Many developers apply relational design patterns with DynamoDB even though they don't have the relational tools like the join operation. This means they put their items into different tables according to their type. However, since there are no joins in DynamoDB, they'll need to make multiple, serial requests to fetch both the Orders and the Customer record.

This can become a big issue in your application. Network I/O is likely the slowest part of your application, and you're making multiple network requests in a waterfall fashion, where one request provides data that is used for subsequent requests. As your application scales, this pattern gets slower and slower.

### The solution: pre-join your data into item collections[](#the-solution-pre-join-your-data-into-item-collections)

So how do you get fast, consistent performance from DynamoDB without making multiple requests to your database? By *pre-joining* your data using item collections.

An item collection in DynamoDB refers to all the items in a table or index that share a partition key. In the example below, we have a DynamoDB table that contains actors and the movies in which they have played. The primary key is a composite primary key where the partition key is the actor's name and the sort key is the movie name.

You can see there are two items for Tom Hanks -- Cast Away and Toy Story. Because they have the same partition key of `Tom Hanks`, they are in the same item collection.

You can use DynamoDB's `Query` API operation to read multiple items with the same partition key. Thus, if you need to retrieve multiple heterogenous items in a single request, you organize those items so that they are in the same item collection.

Let's look at an example from my [DynamoDB data modeling talk at AWS re:Invent 2019](https://youtu.be/DIQVJqiSUkE?t=831). This example uses an e-commerce application like we've been discussing, which involves Users and Orders. We have an access pattern where we want to fetch the User record and the Order records. To make this possible in a single request, we make sure all Order records live in the same item collection as the User record to which they belong.

Now when we want to fetch the User and Orders, we can do it in a single request without needing a costly join operation:

This is what single-table design is all about -- tuning your table so that your access patterns can be handled with as few requests to DynamoDB as possible, ideally one.

And because everything looks better in fancy quotes, let's say it one more time:

The main reason for using a single table in DynamoDB is to retrieve multiple, heterogenous item types using a single request.

### Other benefits of single-table design[](#other-benefits-of-single-table-design)

While reducing the number of requests for an access pattern is the main reason for using a single-table design with DynamoDB, there are some other benefits as well. I will discuss those briefly.

First, there is some operational overhead with each table you have in DynamoDB. Even though DynamoDB is fully-managed and pretty hands-off compared to a relational database, you still need to configure alarms, monitor metrics, etc. If you have one table with all items in it rather than eight separate tables, you reduce the number of alarms and metrics to watch.

Second, having a single table can save you money as compared to having multiple tables. With each table you have, you need to provision read and write capacity units. Often you will do some back-of-the-envelope math on the traffic you expect, bump it up by X%, and convert it to RCUs and WCUs. If you have one or two entity types in your single table that are accessed much more frequently than the others, you can hide some of the extra capacity for less-frequently accessed items in the buffer for the other items.

While these two benefits are real, they're pretty marginal. The operations burden on DynamoDB is quite low, and the pricing will only save you a bit of money on the margins. Further, if you are using [DynamoDB On-Demand pricing](https://serverless.com/blog/dynamodb-on-demand-serverless/), you won't save *any* money by going to a single-table design.

In general, when thinking about single-table design, you should consider the main benefit to be the performance improvement by making a single request to retrive all needed items.

## Downsides of a single-table design[](#downsides-of-a-single-table-design)

While the single-table pattern is powerful and ridiculously scalable, it doesn't come without costs. In this section, we'll review some of the downsides of a single-table design.

In my mind, there are three downsides of single-table design in DynamoDB:

- The steep learning curve to understand single-table design;
- The inflexibility of adding new access patterns;
- The difficulty of exporting your tables for analytics.

Let's review each of these in turn.

### The steep learning curve of single-table design[](#the-steep-learning-curve-of-single-table-design)

The biggest complaint I get from members of the community is around the *difficulty* of learning single-table design in DynamoDB.

A single, over-loaded DynamoDB table looks really weird compared to the clean, normalized tables of your relational database. It's hard to unlearn all the lessons you've learned over years of relational data modeling.

To those who are avoiding single-table design because of the learning curve, my response is this:

**Tough.**

Software development is a continuous journey of learning, and you can't use the difficulty of learning new things as an excuse to use a new thing poorly.

Later on in this post, I will describe a few times when I think it's OK to decide not to use single-table design. However, you should absolutely understand the principles behind single-table design before making that decision. Ignorance is not a reason to avoid the general best practices.

### The inflexibility of new access patterns[](#the-inflexibility-of-new-access-patterns)

A second complaint about DynamoDB is the difficulty of accommodating new access patterns in a single-table design. This complaint has much more validity.

When modeling a single-table design in DynamoDB, you start with your access patterns first. Think hard (and write down!) how you will access your data, then carefully model your table to satisfy those access patterns. When doing this, you will organize your items into collections such that each access pattern can be handled with as few requests as possible -- ideally a single request.

Once you have your table modeled out, then you put it into action and write the code to implement it. And, done properly, this will work great! Your application will be able to scale infinitely with no degradation in performance.

However, your table design is narrowly tailored for the exact purpose for which it has been designed. If your access patterns change because you're adding new objects or accessing multiple objects in different ways, you may need to do an ETL process to scan every item in your table and update with new attributes. This process isn't impossible, but it does add friction to your development process.

### The difficulty of analytics[](#the-difficulty-of-analytics)

DynamoDB is designed for [OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing) use cases -- high speed, high velocity data access where you're operating on a few records at a time. But users also have a need for [OLAP](https://en.wikipedia.org/wiki/Online_analytical_processing) access patterns -- big, analytical queries over the entire dataset to find popular items, or number of orders by day, or other insights.

DynamoDB is not good at OLAP queries. This is intentional. DynamoDB focuses on being ultra-performant at OLTP queries and wants you to use other, purpose-built databases for OLAP. To do this, you'll need to get your data from DynamoDB into another system.

If you have a single table design, getting it into the proper format for an analytics system can be tricky. You've denormalized your data and twisted it into a pretzel that's designed to handle your exact use cases. Now you need to unwind that table and re-normalize it so that it's useful for analytics.

My favorite quote on this comes from [Forrest Brazeal's excellent walkthrough on single-table design](https://www.trek10.com/blog/dynamodb-single-table-relational-modeling/):

[A] well-optimized single-table DynamoDB layout looks more like machine code than a simple spreadsheet

Spreadsheets are easy for analytics, whereas a single-table design takes some work to unwind. Your data infrastructure work will need to be pushed forward in your development process to make sure you can reconstitute your table in an analytics-friendly way.

## When not to use single-table design[](#when-not-to-use-single-table-design)

So far, we know the pros and cons of single-table design in DynamoDB. Now it's time to get to the more controversial part -- when, if ever, should you *not* use single-table design in DynamoDB?

At a basic level, the answer is "whenever the benefits don't outweigh the costs". But that generic answer doesn't help us much. The more concrete answer is "whenever I need query flexibility and/or easier analytics more than I need blazing fast performance." And I think there are two occasions where this is most likely:

- in new applications where developer agility is more important than application performance;
- in applications using GraphQL.

We'll explore each of these below. But first I want to emphasize that these are exceptions, not general guidance. When modeling with DynamoDB, you should be following best practices. This includes denormalization, single-table design, and other proper NoSQL modeling principles. And even if you opt into a multi-table design, you should understand single-table design to know why it's not a good fit for your specific application.

### New applications that prioritize flexibility[](#new-applications-that-prioritize-flexibility)

In the past few years, many startups and enterprises are choosing to build on serverless compute like AWS Lambda for their applications. There are a number of benefits to the serverless model, from the ease of deployments to the painless scaling to the pay-per-use pricing model.

Many of these applications use DynamoDB as their database because of the way it fits seamlessly with the serverless model. From provisioning to pricing to permissions to the connection model, DynamoDB is a perfect fit with serverless applications, whereas traditional relational databases are more problematic.

However, it's important to remember that while DynamoDB works great *with* serverless, it was not built *for* serverless.

[DynamoDB was built for large-scale, high-velocity applications that were outscaling the capabilities of relational databases](https://www.dynamodbguide.com/the-dynamo-paper/). And relational databases can scale pretty darn far! If you're in the situation where you're out-scaling a relational database, you probably have a good sense of the access patterns you need. But if you're making a greenfield application at a startup, it's unlikely you absolutely require the scaling capabilities of DynamoDB to start, and you may not know how your application will evolve over time.

In this situation, you may decide that the performance characteristics of a single-table design are not worth the loss of flexibility and more difficult analytics. You may opt for a [Faux-SQL approach](https://www.alexdebrie.com/posts/dynamodb-patterns-serverless/#faux-sql) where you use DynamoDB but in a relational way by normalizing your data across multiple tables.

This means you may need to make multiple, serial calls to DynamoDB to satisfy your access patterns. Your application may look as follows:

Notice how there are two separate requests to DynamoDB. First, there's a request to fetch the User, then there's a follow up request to fetch the Orders for the given User. Because multiple requests must be made and these requests must be made serially, there's going to be a slower response time for clients of your backend application.

For some use cases, this may be acceptable. Not all applications need to have sub-30ms response times. If your application is fine with 100ms response times, the increased flexibility and easier analytics for early-stage use cases might be worth the slower performance.

### GraphQL & Single-table design[](#graphql--single-table-design)

The second place where you may want to avoid single-table design with DynamoDB is in GraphQL applications.

Before I get 'Well, actually'-d to death on this one, I want to clarify that yes, I know GraphQL is an execution engine rather than a query language for a specific database. And yes, I know that GraphQL is database agnostic.

My point is not that you *cannot* use a single-table design with GraphQL. I'm saying that because of the way GraphQL's execution works, you're losing most of the benefits of a single-table design while still inheriting all of the costs.

To understand why, let's take a look at how GraphQL works and one of the main problems it aims to solve.

For the past few years, many applications have opted for a [REST-based API](https://restfulapi.net/) on the backend and a [single-page application](https://en.wikipedia.org/wiki/Single-page_application) on the frontend. It might look as follows:

In a REST-based API, you have different *resources* which generally map to an entity in your application, such as Users or Orders. You can perform [CRUD-like](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations on these resources by using different [HTTP verbs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) to indicate the operation you want to perform.

One common source of frustration for frontend developers when using REST-based APIs is that they may need to make multiple requests to different endpoints to fetch all the data for a given page:

In the example above, the client has to make two requests -- one to get the User, and one to get the most recent Orders for a user.

With GraphQL, you can fetch all the data you need for a page in a single request. For example, you might have a GraphQL query that looks as follows:

```
query {
  User(id: 112233) {
    firstName
    lastName
    addresses
    orders {
      orderDate
      amount
      status
    }
  }
}
```
In the block above, we're making a query to fetch the User with id 112233, then we're fetching certain attributes about the user (including firstName, lastName, and addresses), as well as all of the orders that are owned by that user.

Now our flow looks as follows:

The web browser makes a single request to our backend server. The contents of that request will be our GraphQL query, as shown below the server. The GraphQL implementation will parse the query and handle it.

This looks like a win -- our client is only making a single request to the backend! Hurrah!

In a way, this mirrors our discussion earlier about why you want to use single-table design with DynamoDB. We only want to make a single request to DynamoDB to fetch heterogenous items, just like the frontend wants to make a single request to the backend to fetch heterogenous resources. This sounds like a match made in heaven!

The issue is in *how* GraphQL handles those resources in the backend. Each field on each type in your GraphQL schema is handled by a [resolver](https://graphql.org/learn/execution/). This resolver understands how to fill in the data for the field.

For different types in your query, such as `User` and `Order` in our example, you would usually have a resolver that would make a database request to resolve the value. The resolver would be given some arguments to indicate which instances of that type should be fetched, and then the resolver will fetch and return the data.

The problem is that resolvers are essentially independent from each other. In the example above, the root resolver would execute first to find the User with ID 112233. This would involve a query to the database. Then, once that data is available, it would be passed to the Order resolver in order to fetch the relevant Orders for this User. This would make subsequent requests to the database to resolve those entities.

Now our flow looks like this:

In this flow, our backend is making multiple, serial requests to DynamoDB to fulfill our access pattern. This is exactly what we're trying to avoid with single-table design!

None of this goes to say that you can't use DynamoDB with GraphQL -- you absolutely can. I just think it's a waste to spend time on a single-table design when using GraphQL with DynamoDB. Because GraphQL entities are resolved separately, I think it's fine to model each entity in a separate table. It will allow for more flexibility and make it easier for analytics purposes going forward.

## Conclusion[](#conclusion)

In this post, we reviewed the concept of single-table design in DynamoDB. First, we went through some history on how NoSQL & DynamoDB evolved and why single-table design is necessary.

Second, we looked at some downsides to single-table design in DynamoDB. Specifically, we saw how single-table design can make it harder to evolve your access patterns and complicates your analytics work.

Finally, we looked at two situations where the benefits of single-table design in DynamoDB may not outweigh the costs. The first situation is in new, fast-evolving applications using serverless compute where developer agility is paramount. The second situation is when using GraphQL due to the way the GraphQL execution flow works.

I'm still a strong proponent of single-table design in DynamoDB in most use cases. And even if you don't think it's right for your situation, I still think you should learn and understand single-table design before opting out of it. Basic NoSQL design principles will help you even if you don't follow the best practices for large-scale design.

If you have questions or comments on this piece, feel free to leave a note below or [email me directly](mailto:alexdebrie1@gmail.com).
