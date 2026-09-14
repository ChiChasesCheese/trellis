---
title: Fast and flexible observability with canonical log lines
source: https://stripe.com/blog/canonical-log-lines
author: Brandur Leach
published: '2019-07-30'
site: Stripe
clipped: '2026-08-30'
---

# Fast and flexible observability with canonical log lines

# 
      [Fast and flexible observability with canonical log lines](/blog/canonical-log-lines)
    

    
    
  Logging is one of the oldest and most ubiquitous patterns in computing. Key to gaining insight into problems ranging from basic failures in test environments to the most tangled problems in production, it’s common practice across all software stacks and all types of infrastructure, and has been for decades.

Although logs are powerful and flexible, their sheer volume often makes it impractical to extract insight from them in an expedient way. Relevant information is spread across many individual log lines, and even with the most powerful log processing systems, searching for the right details can be slow and requires intricate query syntax.

We’ve found using a slight augmentation to traditional logging immensely useful at Stripe—an idea that we call canonical log lines. It’s quite a simple technique: in addition to their normal log traces, requests also emit one long log line at the end that includes many of their key characteristics. Having that data colocated in single information-dense lines makes queries and aggregations over it faster to write, and faster to run.

Out of all the tools and techniques we deploy to help get insight into production, canonical log lines in particular have proven to be *so* useful for added operational visibility and incident response that we’ve put them in almost every service we run—not only are they used in our main API, but there’s one emitted every time a webhook is sent, a credit card is tokenized by our PCI vault, or a page is loaded in the Stripe Dashboard.

## Structured logging

Just like in many other places in computing, logging is used extensively in APIs and web services. In a payments API, a single request might generate a log trace that looks like this:

**Structured logging** augments the practice by giving developers an easy way to annotate lines with additional data. The use of the word *structured* is ambiguous—it can refer to a natively structured data format like JSON, but it often means that log lines are enhanced by appending `key=value` pairs (sometimes called [logfmt](https://brandur.org/logfmt), even if not universally). The added structure makes it easy for developers to tag lines with extra information without having to awkwardly inject it into the log message itself.

An enriched form of the trace above might look like:

The added structure also makes the emitted logs machine readable (the `key=value` convention is designed to be a compromise between machine and human readability), which makes them ingestible for a number of different log processing tools, many of which provide the ability to query production logs in near real-time.

For example, we might want to know what the last requested API endpoints were. We could figure that out using a log processing system like Splunk and its built-in query language:

Or whether any API requests have recently been rate limited:

Or gather statistics on API execute duration over the last hour:

In practice, it would be much more common to gather these sorts of simplistic vitals from dashboards generated from metrics systems like [Graphite](https://github.com/graphite-project/graphite-web) and [statsd](https://github.com/statsd/statsd), but they have limitations. The emitted metrics and dashboards that interpret them are designed in advance, and in a pinch they’re often difficult to query in creative or unexpected ways. Where logging really shines in comparison to these systems is flexibility.

Logs are usually *over*producing data to the extent that it’s possible to procure just about anything from them, even information that no one thought they’d need. For example, we could check to see which API path is the most popular:

Or let’s say we see that the API is producing 500s (internal server errors). We could check the request duration on the errors to get a good feel as to whether they’re likely caused by database timeouts:

Sophisticated log processing systems tend to also support visualizing information in much the same way as a metrics dashboard, so instead of reading through raw log traces we can have our system graph the results of our ad-hoc queries. Visualizations are more intuitive to interpret, and can make it much easier for us to understand what’s going on.

## Canonical log lines: one line per request per service

Although logs offer additional flexibility in the examples above, we’re still left in a difficult situation if we want to query information *across* the lines in a trace. For example, if we notice there’s a lot of rate limiting occurring in the API, we might ask ourselves the question, “Which users are being rate limited the most?” Knowing the answer helps differentiate between legitimate rate limiting because users are making too many requests, and accidental rate limiting that might occur because of a bug in our system.

The information on whether a request was rate limited and which user performed it is spread across multiple log lines, which makes it harder to query. Most log processing systems can still do so by collating a trace’s data on something like a request ID and querying the result, but that involves scanning a lot of data, and it’s slower to run. It also requires more complex syntax that’s harder for a human to remember, and is more time consuming for them to write.

We use **canonical log lines** to help address this. They’re a simple idea: in addition to their normal log traces, requests (or some other unit of work that’s executing) also emit one long log line at the end that pulls all its key telemetry into one place. They look something like this:

This sample shows the kind of information that a canonical line might contain include:

- The HTTP request verb, path, and response status.
- The authenticated user and related information like how they authenticated (API key, password) and the ID of the API key they used.
- Whether rate limiters allowed the request, and statistics like their allotted quota and what portion remains.
- Timing information like the total request duration, and time spent in database queries.
- The number of database queries issued and the number of objects allocated by the VM.

We call the log line *canonical* because it’s the authoritative line for a particular request, in the same vein that the IETF’s [canonical link relation](https://tools.ietf.org/html/rfc6596) specifies an authoritative URL.

Canonical lines are an ergonomic feature. By colocating everything that’s important to us, we make it accessible through queries that are easy for people to write, even under the duress of a production incident. Because the underlying logging system doesn’t need to piece together multiple log lines at query time they’re also cheap for computers to retrieve and aggregate, which makes them fast to use. The wide variety of information being logged provides almost limitless flexibility in what can be queried. This is especially valuable during the discovery phase of an incident where it’s understood that something’s wrong, but it’s still a mystery as to what.

Getting insight into our rate limiting problem above becomes as simple as:

If only one or a few users are being rate limited, it’s probably legitimate rate limiting because they’re making too many requests. If it’s many distinct users, there’s a good chance that we have a bug.

As a slightly more complex example, we could visualize the performance of the `charges` endpoint for a particular user over time while also making sure to filter out `4xx` errors caused by the user. `4xx` errors tend to short circuit quickly, and therefore don’t tell us anything meaningful about the endpoint’s normal performance characteristics. The query to do so might look something like this:

## Implementation in middleware and beyond

Logging is such a pervasive technique and canonical log lines are a simple enough idea that implementing them tends to be straightforward regardless of the tech stack in use.

The implementation in Stripe’s main API takes the form of a middleware with a post-request step that generates the log line. Modules that execute during the lifecycle of the request decorate the request’s environment with information intended for the canonical log line, which the middleware will extract when it finishes.

Here’s a greatly simplified version of what that looks like:

Over the years our implementation has been hardened to maximize the chance that canonical log lines are emitted for *every* request, even if an internal failure or other unexpected condition occurred. The line is logged in a Ruby `ensure` block just in case the middleware stack is being unwound because an exception was thrown from somewhere below. The logging statement itself is wrapped in its own `begin`/`rescue` block so that any problem constructing a canonical line will never fail a request, and also so someone is notified immediately in case there is. They’re such an important tool for us during incident response that it’s crucial that any problems with them are fixed promptly—not having them would be like flying blind.

## Warehousing history

A problem with log data is that it tends to be verbose. This means long-term retention in anything but cold storage is expensive, especially when considering that the chances it’ll be used again are low. Along with being useful in an operational sense, the succinctness of canonical log lines also make them a convenient medium for archiving historical requests.

At Stripe, canonical log lines are used by engineers so often for introspecting production that we’ve developed muscle memory around the naming of particular fields. So for a long time we’ve made an effort to keep that naming stable—changes are inconvenient for the whole team as everyone has to relearn it. Eventually, we took it a step further and formalized the contract by codifying it with a [protocol buffer](https://developers.google.com/protocol-buffers/).

Along with emitting canonical lines to the logging system, the API also serializes data according to that contract and sends it out asynchronously to a Kafka topic. A consumer reads the topic and accumulates the lines into batches that are stored to S3. Periodic processes ingest those into Presto archives and Redshift, which lets us easily perform long-term analytics that can look at months’ worth of data.

In practice, this lets us measure almost everything we’d ever want to. For example, here’s a graph that tracks the adoption of major Go versions over time from API requests that are issued with our official API libraries:

Better yet, because these warehousing tools are driven by SQL, engineers and non-engineers alike can aggregate and analyze the data. Here’s the source code for the query above:

## Product leverage

We already formalized the schema of our canonical log lines with a protocol buffer to use in analytics, so we took it a step further and started using this data to drive parts of the Stripe product itself. A year ago we introduced our [Developer Dashboard](https://stripe.com/blog/developer-dashboard) which gives users access to high-level metrics on their API integrations.

The [Developer Dashboard](https://stripe.com/blog/developer-dashboard) shows the number of successful API requests for this Stripe account. Data is generated from canonical log lines archived to S3.

The charts produced for this dashboard are also produced from canonical log lines. A MapReduce backend crunches archives stored in S3 to create visualizations tailored to specific users navigating their dashboards. As with our analytics tools, the schema codified in the protocol buffer definition ensures a stable contract so they’re not broken.

Canonical lines are still useful even if they’re never used to power products, but because they contain such a rich trove of historical data, they make an excellent primary data source for this sort of use.

## Sketching a canonical logging pipeline

Canonical log lines are well-suited for practically any production environment, but let’s take a brief look at a few specific technologies that might be used to implement a full pipeline for them.

In most setups, servers log to their local disk and those logs are sent by local collector agents to a central processing system for search and analysis. The [Kubernetes documentation on logging](https://kubernetes.io/docs/concepts/cluster-administration/logging/) suggests the use of Elasticsearch, or when on GCP, Google’s own Stackdriver Logging. For an AWS-based stack, a conventional solution is CloudWatch. All three require an agent like [fluentd](https://github.com/fluent/fluentd) to handle log transmission to them from server nodes. These solutions are common, but far from exclusive—log processing is a thriving ecosystem with dozens of options to choose from, and it’s worth setting aside some time to evaluate and choose the one that works best for you.

Emitting to a data warehouse requires a custom solution, but not one that’s unusual or particularly complex. Servers should emit canonical log data into a stream structure, and asynchronously to keep user operations fast. Kafka is far and away the preferred stream of choice these days, but it’s not particularly cheap or easy to run, so in a smaller-scale setup something like [Redis streams](https://redis.io/topics/streams-intro) are a fine substitute. A group of consumers cooperatively reads the stream and bulk inserts its contents into a warehouse like Redshift or BigQuery. Just like with log processors, there are many data warehousing solutions to choose from.

## Flexible, lightweight observability

To recap the key elements of canonical log lines and why we find them so helpful:

- A canonical line is one line per request per service that collates each request’s key telemetry.
- Canonical lines are not as quick to reference as metrics, but are extremely flexible and easy to use.
- We emit them asynchronously into Kafka topics for ingestion into our data warehouse, which is very useful for analytics.
- The stable contract provided by canonical lines even makes them a great fit to power user-facing products! We use ours to produce the charts on Stripe’s Developer Dashboard.

They’ve proven to be a lightweight, flexible, and technology-agnostic technique for observability that’s easy to implement and very powerful. Small and large organizations alike will find them useful for getting visibility into production services, garner insight through analytics, and even shape their products.
