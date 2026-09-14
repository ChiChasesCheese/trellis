---
title: 'Ledger: Stripe''s system for tracking and validating money movement'
source: https://stripe.com/blog/ledger-stripe-system-for-tracking-and-validating-money-movement
author: Ilya Ganelin
published: '2024-02-16'
site: Stripe Dot Dev Blog
clipped: '2026-08-30'
---

# Ledger: Stripe's system for tracking and validating money movement

Last Black Friday to Cyber Monday, Stripe processed 300 million transactions with a total payment volume of $18.6B—and the Stripe API maintained greater than 99.999% availability. Underlying these metrics is our Global Payments and Treasury Network (GPTN) that manages the complexity of accepting payments, money storage, and money movement. Today, Stripe supports more than 135 currencies and payment methods through partnerships with local banks and financial networks in 185 countries. These entities provide different interfaces, data models, and behaviors, and Stripe continually manages this complexity so developers can quickly integrate the GPTN into their businesses.

Internally, Stripe needs to guarantee that what we expect to happen during payment processing actually happens for internal customers and external auditors of our data. We built Ledger, an immutable and auditable log, as a trustworthy system of record for all of our financial data. Ledger standardizes our representation of money movement, and it serves as the scalable foundation for our automated Data Quality (DQ) Platform—guaranteeing Stripe faithfully manages money for users.

Many existing systems provide primitives for accurate accounting, but the real world is imperfect, incomplete, and constantly changing. We witness basic and obvious failures like malformed reports or propagated errors from banking or network partners, and also broad macroeconomic changes such as currencies ceasing to exist or large banks collapsing overnight. While we aspire to an orderly ideal, at Stripe scale, that’s impossible—instead we built a system that keeps these imperfections manageable and bounded.

Ledger models internal data-producing systems with common patterns, and it relies on proactive alerting to surface issues and proposed solutions. Each day, Ledger sees five billion events and 99.99% of our dollar volume is fully ingested and verified within four days. Of that activity, 99.999% is monitored, categorized, and triaged through rich investigative tooling—while the remaining long-tail is reliably handled through manual analysis. Together, Ledger and the DQ Platform ensure over 99.9999% explainability of money movement, even as Stripe’s data volume has grown 10x.

In this blog post, we’ll share technical details on how we built this state-of-the-art money movement tracking system, and describe how teams at Stripe interact with the data quality metrics that underlie our global payments network.

![Blog > Ledger > 5 billion events per day](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-0.png)

### How Stripe processes payments

The GPTN in part is a payment processing network consisting of customer business calls to Stripe’s API and Stripe’s interactions with a variety of banks and payment methods. There is complexity in tracking the requests Stripe makes to partners, the physical money movement between financial partners, and the reporting Stripe receives back. We make this multifaceted problem tractable by segmenting the Stripe platform into discrete services, databases, and APIs/gRPC interfaces, which lets us solve individual problems without getting overwhelmed by the broader system.

The challenge with this approach is that there is no intrinsic mechanism forcing these systems to represent or deliver data in the same way. Some might operate in real time, while others may operate on a monthly cadence with vastly different data volumes; some producers generate billions of events per day, while others may only generate a few hundred. Moreover, each system might have its own definitions of correctness or reliability. We require a mechanism that can deal with these variations and prove that these individual systems are collectively modeling our financials correctly.

![Blog > Ledger > Stripe's interactions with external entities](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-1.png)

A simplified summary view of Stripe’s interactions with external entities

### How we designed Ledger

The Stripe services mentioned above have independent responsibilities, but they collaborate to solve a large federated problem. An ideal solution provides a mental model for correctness—supported by trustworthy statistics—that easily generalizes to new use cases. Further, we want to represent all activity on the Stripe platform in a common data structure that can be analyzed by a single system.

This is the way we approach it:

- Ledger encodes a state machine representation of producer systems, and models its behavior as a logical fund flow—the movement of balances (events) between accounts (states).
- Ledger computes all account balances to evaluate the health of the system, grouped by various subdivisions to generate comprehensive statistics.

This approach abstracts individual differences between underlying systems and provides mathematical evidence that they are functioning correctly.

#### Ledger as a semantic data store

Ledger is a faithful representation of the underlying state of all payment processes on the Stripe platform. Instead of computing a derived dataset based on incoming data pipelines, Ledger models the actual work of producer systems, recording each operation as a transaction. Ledger modeling may diverge from upstream data, but we guard against these cases explicitly with data completeness checks.

Combined with our other data quality metrics, we can safely rely on Ledger’s data representation to monitor external systems. If we instrument Ledger, we indirectly instrument the data-producing pipelines. And, if we identify a problem, we alert our internal users to which part of their data pipeline is broken—and exactly how they can fix it.

![Blog > Ledger > Processing a charge](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-2.png)

Processing a charge with a creation event for a pending charge, and a release event for completion

Inside of Ledger, we represent this activity as a movement of balances between two discrete states (creation and release), turning the above process into an observable state machine.

![Blog > Ledger > Processing a charge in Ledger](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-3.png)

Processing a charge in Ledger, represented by a creation event for a pending charge and a release event for completion

#### System abstraction

Ledger also abstracts producer systems. Instead of separately monitoring handoffs between data pipelines, we model systems as connected fund flows moving money between accounts. Because Ledger is a transaction-level system of record, we can prove that even complex multisystem pipelines with multiple stages of handoff are working correctly. We also model data consistency between otherwise disconnected systems, and we track individual transactions through their entire lifecycle. We call this tracing, and, at our scale, this totals to billions of daily transactions.

#### Unifying separate systems with fund flows

Consider an abstract end-to-end fund flow: for example, a business adding funds to its balance. This requires moving funds between banks, reconciling money movement with third-party reporting, and matching regulatory reporting with financial reporting. The fund flow spans multiple internal team boundaries, with discrete events published to different systems at different times. If we model this fund flow with logical constructs, Ledger can unify this data across separate systems and monitor its correctness.

![Blog > Ledger > Funds flows](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-4.png)

#### Immutability

At its core, Ledger is an immutable log of events. Transactions previously published into Ledger cannot be deleted or modified, and we can always reconstruct past state by processing all events up to that point. All constructs—balances, fund flows, data quality controls, and so on—are transformations of the static underlying structure. Ledger’s immutability ensures we can audit and reproduce any data point at any time. Immutability justifies our data quality measures by guaranteeing that we can explain and analyze the exact problematic data.

### How we designed the Data Quality (DQ) Platform

Ledger is the foundation for our Data Quality (DQ) Platform, which unifies detection of money movement issues and response tooling. Empirically, the DQ Platform ensures reliable and timely reporting across Stripe’s key lines of business: we maintained a 99.999% readiness target, even as data volume grew 10x.

Transaction-level fund flows give us powerful tools to reason about complex interconnected subcomponents. We analyze these abstractions with a set of trustworthy DQ metrics that measure the health of a fund flow. These metrics are based on a common set of questions across all fund flows. For a specific cross-section of data, evaluated at time X, we look at:

- **Clearing:** Did the fund flow complete correctly?
- **Timeliness:** Did the data arrive on time?
- **Completeness:** Do we have a complete representation of the underlying data system?

We then compose DQ metrics on individual fund flows to provide scoring and targeted guidance for technical experts. These measurements roll up to create a unified DQ score—a system with a 99.99% data quality score is extremely unlikely to hide major problems—turning a complex distributed analysis problem into a straightforward tabulation exercise. Technical users can likewise trust that improving DQ scores reflect true improvement in underlying system behavior and accuracy.

#### Clearing

Ledger is based on double-entry bookkeeping, a standard method for guaranteeing that all money in a system is fully accounted for by balancing credits and debits. Grounding our analysis in this construct gives us a mathematical proof of correctness. If you’ve never encountered this term before, a helpful explainer is [“An Engineer’s Guide to Double-Entry Bookkeeping.”](https://anvil.works/blog/double-entry-accounting-for-engineers)

Using double-entry bookkeeping to validate money movement is similar to analyzing a flow of water through a network of pipes (processes) ending in reservoirs (balance sheets). At steady state, terminal (nonclearing) reservoirs are full, and intermediate (clearing) pipes are empty. If there is water stuck in the pipes, then you have a problem—in other words, unresolved balances on the balance sheet.

Traditionally, bookkeeping is purely an accounting construct, but we apply these ideas in a novel way. Rather than just tabulating cash flow in and out, we’re simultaneously modeling internal data system behaviors that may have nothing to do with physical movement of money—for example, currency conversion, report parsing, estimation, or billing analysis. We can use the same bookkeeping concepts to reason about those systems and evaluate their correctness in a much more general way.

#### Detecting problems

Clearing measures the fraction of Ledger that is appropriately zeroed out at steady state. Consider an example that models two steps of a flow: `charge creation` (potential money movement) and `release` (funds becoming available). As you follow the flow, keep in mind these definitions:

- **Accounts** are buckets of money distinguished by their type (e.g., `charge_unsubmitted`) and properties (e.g.,`id`, `business`).
- **Events** move money between accounts (e.g., `charge.creation` and `charge.release`).

![Blog > Ledger > T0 and T1](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-5.png)

At time `T0`, the `charge.creation` event sets up a balance in the undisbursed account; then at `T1`, `charge.release` completes the flow and moves the funds to the `business_balance` account.

It is important to note that the `creation` and `release` events are completely independent. Even if they arrive out of order, or are created by different sources, Ledger maintains accurate fund flows through the identifier for `business` and `id`. But, if the `release` event is never published or has the wrong `id`, Ledger would not clear the balance in the associated `charge_undisbursed` account, and it would instead hold the balance in a different instance of `charge_undisbursed`.

#### Example clearing issue

Consider next how a wrong value (`business: B` vs. `business: A`) results in two clearing accounts with nonzero balance. Instead of having one reservoir of money for `business: A`, we wind up with two—one for `business: A` and one for `business: B`.

![Blog > Ledger > T1 missing event](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-6.png)

Generalizing from this example, we repeat this process for every fund flow, account type, and property-based subdivision inside of Ledger. Even when we have billions of transactions, a single missing, late, or incorrect transaction immediately creates a detectable accuracy issue with a simple query—for example, “*Find the clearing Accounts with nonzero balance.”*

#### Timeliness

Clearing prevents persistent problems, but we also need to guarantee data arrives on time for time-sensitive functions such as monthly report generation. Producers create time stamps when integrating with Ledger, and we measure the delta between when data first enters the Stripe platform and when it reaches Ledger. We set a hard threshold on the data delivery window, and we create headroom for subsequent reporting, analysis, and manipulations to guarantee 99.999% timeliness.

#### Completeness

We guarantee data completeness and guard against missing data from upstream systems with explicit cross-system checks alongside automated anomaly detection. For example, we ensure that every ID in a producer database has a matching Ledger event. We also run statistical modeling on data availability. We have models for every account type that use historical trends to calculate expected data arrival time and, if events do not appear, we interpret this as potentially missing data.

### How teams at Stripe explore DQ metrics

On top of the DQ Platform, we built hierarchical automated alerting and rich tooling. We combine interactive metric displays with analysis and guidance. The experience for internal leaders and team members focuses on proactive feedback, simple manipulation of data, and meaningful metrics. We also provide use-case-specific context that depends on which part of the business is using it. For example, consider how we show team-level DQ metrics for our periodic financial reporting, which we call Accounting Close. Note: some details are blocked out for privacy.

![Blog > Ledger > Accounting Close](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-7.png)

The topline view is generally in a good state, but there are areas for improvement at the team level within the Payment Engineering group. For example, the 50% score for Aging Balances means that some clearing issues have persisted over time:

![Blog > Ledger > Data quality metrics](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-8.png)

A single team-level view of data quality metrics

This team-level view shows DQ metrics alongside a call to action including auto-generated tickets, relevant resources, and tool links—everything required for self-service. For leaders, this view provides the exact dollar impact of DQ issues.

#### Tactical views

DQ scores drop when a problem is observed in Ledger. Although Ledger is a projection of underlying systems, Ledger problems are not usually problems of transcription or data modeling in Ledger. They primarily reveal real problems with system implementations, integrations, or physical money movement. In these cases, we provide tactical views to trace issues back to their root cause inside Stripe platforms or external systems.

Consider an uncleared balance of a specific account type—a processing fee that must be invoiced and paid. At steady state, the invoice should be paid and the balance is zero, but over time we observe a nonclearing balance.

![Blog > Ledger > Breakdown](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-9.png)

#### Investigation and attribution

Clicking on a point in the graph generates SQL queries in Presto (our ad-hoc SQL query engine) and surfaces relevant data: reference keys, metadata, ownership, and tips. If a Ledger user is unable to debug and publish a correction—perhaps because the root cause is related to an infrastructure or third-party incident outside their control—they can reassign ownership to the right internal stakeholders and exclude it from alerting.

When issues are attributed to a known incident, we can retroactively analyze the impact to DQ metrics across teams to fully understand how Stripe was affected:

![Blog > Ledger > Live Clearing](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-10.png)

![Blog > Ledger > Data Quality Artifacts](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-11.png)

Combined, we have the ability to measure and analyze data quality, identify root-cause problems, and flexibly interact with the underlying data constructs to manage our problem load over time. In this case, fixing problems in Ledger may involve republishing data from source systems.

#### Data correction

Ledger is our system of record and must remain an evergreen representation of truth. Persistent problems reduce visibility into new problems and may result in incorrect reporting or derived datasets. Because Ledger is an immutable log of events, we can’t run simple queries to mutate the state; instead, we have to revert and reprocess prior operations. If an incident occurs, we need a tool for correcting data at scale.

We built a supporting utility to create and safely execute migrations, protected by a data quality tool that generates out-of-band reports on the production impact of proposed changes. Together, these tools approximate a CI pipeline for ad-hoc data repair operations. All operations must go through a two-phase review and commit of the data—and its associated DQ impact.

![Blog > Ledger > Data Pipeline Health Summary](https://stripe.dev/images/ledger-stripe-system-for-tracking-and-validating-money-movement/image-12.png)

### Fewer data problems, more reliable reporting

Our systems need to operate within a messy reality, but the innovations described in this blog post drive us towards a trustworthy and explainable operational model. Likewise, as businesses and mechanisms for money movement inevitably evolve, Stripe is empowered to keep pace with that change.

The DQ Platform ensures reliable and timely reporting across all Stripe business lines. The combination of clearing, timeliness, and completeness metrics ensures that internal stakeholders can make sound judgments about the correctness of underlying data systems without worrying about maintaining complex specialized knowledge.

The digital economy will continue to accelerate, and our focus is on building robust and scalable systems to power it. In the future, we want to improve timeliness to minute-level analysis and response—offering lower latency processing, which will strengthen fraud detection and increase available response time to address possible financial problems.

We are also investing in advanced enrichment capabilities that allow us to declaratively compose new datasets and reporting interfaces while guaranteeing that they meet our data quality bar. This work safely evolves the complexity of our internal systems alongside Stripe’s growth.

We’re excited to continue to solve hard, important problems. If you are too, consider joining our [engineering team](https://stripe.com/jobs/search?query=engineer).
