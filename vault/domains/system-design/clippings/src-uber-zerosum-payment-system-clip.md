---
title: 'Zero-Sum by Design: 10 Years of Uber’s Payments Platform'
source: https://www.uber.com/us/en/blog/ubers-payments-platform/
published: '2026-09-20'
site: Uber
clipped: '2026-09-20'
---

# Zero-Sum by Design: 10 Years of Uber’s Payments Platform

# Zero Sum by Design 10 Years of Uber's Payments Platform

Distinguished Engineer

Sr. Engineering Manager

Principal Engineer

# Introduction

The journey of Uber’s Payments Platform (known internally as Gulfstream) began in 2016 in a single conference room, where a small team bootstrapped a foundational set of microservices. A decade later, many of those services still run in production, reflecting the durability of the system’s early design.

Over the same period, Uber scaled from $50 billion to $217 billion in annualized gross bookings. Supporting this growth required a platform that not only collects payments from customers, but also disburses funds to drivers, couriers, and merchants—processing nearly 2x gross bookings in total money movement and maintaining ledger balances for more than 1.2 billion entities.

In this post, we share the core principles that shaped this journey and continue to underpin the system today.

### Core Principles

#### Immutable Money Order

One of the most critical data models within our architecture is called a Money Order. It is a series of debits and credits between the entities involved in the real-world commerce transaction (such as a trip, an Uber Eats order, a freight shipment, or a digital Uber Cash top-up). To make our system self-auditable, we made our money order immutable.

One may ask: What happens when a trip is adjusted or a food item is missed in an Uber Eats order? We write additional money orders to capture the adjustment.

But the principle stands; an order once written can’t be changed in any shape or form.

#### Zero Sum Principle

Before writing a money order down, we always run pre-commit validations. One of the validations is to ensure that all entries in any money order sum to zero. That is, no money can ever be created or destroyed.

In addition, we also follow the *double-entry bookkeeping* principle, where every credit entry on the order has an equivalent debit entry, which in turn ensures that the zero-sum principle can never really be violated. Over the years, we have even pushed these principles to systems upstream of the Payments Platform. 

#### Strongly Consistent Ledger Balances

Back in 2016, Uber was just coming off its monolith architecture, and while we had a homegrown sharded MySQL® offering, there was no perfect solution to guarantee strong consistency for ledger balances. We ended up building this specific data store on Amazon DynamoDB®. Each entity (such as a Spender, Earner, or Business) can have multiple sub-ledger accounts, all stored as a single row in DynamoDB. The typical entity size was 1KB, though over the years, we definitely had to manage the number of sub-ledger accounts within each entity. We had to ensure any sub-ledger account with a 0 balance was pruned to manage the row size.

#### Core Data Models

Our early emphasis on defining core data models proved to be a strategic investment that has yielded significant returns, as these models remain foundational to our operations today.

The 3 data models that matter the most are:

- **Money order** : Models money movements between 2 or more real-world entities, encapsulating a commerce transaction at Uber.
- **Ledger** : Represents a real-world entity with 1 or more accounts, each account holding a balance.
- **Entity changelog** : Captures balance updates on the ledger, providing a complete audit trail and the ability to recreate an entity’s ledger since inception

#### Loosely Coupled Architecture

We designed the Payments Platform as a collection of independent, stateless microservices, each owning a discrete unit of the money movement lifecycle — money order creation, processing, collection, and disbursement — with Apache Kafka® as the underlying messaging bus. The two shared sources of truth across all services are the money order store and the entity balance store. This async pipeline processes the majority of Uber's money traffic today. For user-in-session flows, we used Uber’s internal workflow engine - Cadence, to support synchronous payments without compromising the async backbone.

#### Line of Business (LOB) Agnostic

When we were building the platform, Uber had one core business, Rides, and we were just getting started with Uber Eats. However, we wanted to build the platform so that if Uber ventured into new product lines, it would just work out of the box.

To this effect, to model the typical real-world money movement, we had generic money orders like:

- Collection Money Order
- Disbursement Money Order
- Refund Money Order, and so on

These were pure platform concepts and had no association with any specific product line.

We also built a generic commerce Money Order to capture money movements between entities, representing any real-world commerce transaction between 2 or more entities.

Over the years, we onboarded, Uber Freight, 2-wheels, Transit, Hotels, Rental Cars, Grocery & Retail, Ads, Memberships (Uber one, Costco etc.) and other lines of businesses that has needed very little to no changes within the core platform.

#### Payment Instrument Agnostic

In our early days, we already supported half a dozen payment instruments, including some regional payment instruments, but we knew that over time we’d want to add all of the top payment instruments for any specific country to delight our customers. To this end, we wanted our core platform to operate on a generic concept of a Payment Instrument, backed by a Payment integration interface with APIs such as charge, disburse, refund, and so on.

The core platform itself had no instrument-specific logic, which was abstracted into a payment integration implementation. Over the years, this has allowed us to scale the platform to a broad range of payment methods, including credit and debit cards, PayPal®, Paytm®, UPI®, Alipay®, Apple Pay®, Google Pay®, iDEAL®, PIX®, and dozens of other local/regional wallets, as well as Uber-native instruments like Uber Cash—each plugging into the platform through the same generic Payment integration interface with little to no change to the core platform. [Uber Pay](https://uberpay.uber.com/#section/Introduction-to-Uber-Pay) alone, our reverse-integration platform for local and alternative payment methods, today manages 50+ payment methods globally.

### Scaling: A Decade-Long Journey

While our core principles provided a strong foundation, we’ve continued to evolve the system as the business scaled. Some noteworthy architectural shifts include simplifying how fare components are recorded and utilized for money movements, addressing the high-throughput challenges of hot ledger entities driven by B2B growth, and supporting diverse internal use cases through a Ledger-as-a-Service model.

##### Data layer

As any software solution matures, regulatory and compliance requirements evolve alongside the product. We initially launched with a simpler data architecture backed by Amazon DynamoDB® for orders and changelogs.

As audit requirements deepened, we moved beyond off-the-shelf databases to build infrastructure tailored to our unique requirements. This led us to partner with Uber's Storage Platform team to architect and build [LedgerStore](https://www.uber.com/us/en/blog/dynamodb-to-docstore-migration/) — a custom storage layer purpose-built for auditability and tamper-evident record-keeping.

##### Entity Fares

While we could model money movements across any number of parties in a single transaction, our upstream systems didn’t fully have the same flexibility nor enforce the same principles (like zero-sum). Any ambiguity in fare representation directly conflicted with the core principles we had established. To address this, we reimagined our approach by introducing Entity Fares. By explicitly recording fares for every participating entity and enforcing the zero-sum principle at the point of computation, we ensured that our foundational tenets remained intact from the very inception of a transaction.

##### Hot Entity Problem

As Uber’s B2B ecosystem—including Uber for Business and Uber Direct—witnessed rapid expansion, a unique architectural challenge surfaced: the hot entity problem. Maintaining strong global consistency while frequently updating the same ledger row posed a significant hurdle to serialized write performance and system correctness. To overcome this, we had to [innovate](https://www.uber.com/us/en/blog/high-throughput-processing/) with a specialized, serialized batch-write mechanism, ultimately enabling us to scale ledger mutations and achieve a 10x increase in throughput for these high-traffic entities.

##### Ledger-as-a-Service

Beyond its core architecture, our Ledger primitives proved versatile enough to support a variety of critical stored value and money movement use cases across Uber, including:

- **Uber Cash and Uber Money** : Managing both closed-loop and semi-open-loop Stored Value systems required a battle-tested ledger to ensure absolute financial integrity.
- **Uber for Business** : To support our B2B invoice-based settlement flows, we leveraged the Ledger to track complex unbilled, billed, and settled balances throughout the entire enterprise billing lifecycle.

By decoupling and generalizing our ledger components, we evolved our infrastructure into a multi-tenant solution. This Ledger-as-a-Service model empowered engineering teams across the company to iterate on specific business requirements without the overhead of building their own financial primitives. Today, several of these multi-tenant ledgers have been operating reliably for over 7 years.

# Conclusion

Building a Payments Platform that moves hundreds of billions of dollars annually doesn’t happen by accident—it’s the result of principled decisions made early and defended consistently over a decade. Immutability kept our audit trail clean. Zero-sum accounting ensured money was never created or destroyed. Strong consistency gave us a ledger we could trust. And by designing around generic abstractions—LOB-agnostic money orders and instrument-agnostic payment integrations—we built a foundation that absorbed every new product line and payment instrument Uber threw at it, all while avoiding the need for any re-architecture and yet evolving to meet Uber’s needs.

### Acknowledgments

None of this would have been possible without the world-class team that built the system back in 2016 and the equally world-class team that has scaled and operationalized it over the years.

Cover Photo Attribution: Generated with ChatGPT

*Alipay is a registered trademark of Advanced New Technologies Co., Ltd.*

*Apache Kafka® is a registered trademark of the Apache Software Foundation*

*Apple Pay is a registered trademark of Apple Inc.* 

*DynamoDB is a registered trademark of Amazon Technologies, Inc.* 

*Google Pay is a registered trademark of Google LLC.* 

*iDEAL is a registered trademark of Currence iDEAL B.V.* 

*MySQL is a registered trademark of Oracle® and/or its affiliates.*

*PayPal is a registered trademark of PayPal, Inc.*

*Paytm is a registered trademark of One 97 Communications Limited.*

*PIX is a registered trademark of the Banco Central do Brasil (Central Bank of Brazil).* 

*UPI is a registered trademark of National Payments Corporation of India (NPCI).*

Nimish Sheth

Distinguished Engineer

Nimish is a Distinguished Engineer at Uber. He’s been at Uber for 10+ years across 2 stints. He helped architect Uber’s Payments Platform from the ground up. More recently, he’s been working on Uber Eats, specifically focusing on Search and B2B platforms.

Manas Kelshikar

Sr. Engineering Manager

Manas is a Sr. Engineering Manager at Uber. Across 2 stints and 8y+ at Uber, he has been an engineer on Uber’s payments platform, transitioned to Eng Management in the payments organization, and, most recently, focused on Financial Products.

Dhirendra Kumar Singh

Principal Engineer

Dhirendra is a Principal Engineer at Uber. He’s been at Uber for 9+ years. He has been an engineer who has helped build & scale Uber’s Payment Platform and Products over the years. More recently, he’s focused on the Payment products like B2B Payments, Recurring Payments, & Uber for Family.

Rajan Jana

Senior Staff Engineer

Rajan is a Senior Staff Engineer at Uber with 9+ years at the company. He has helped build and scale the payments platform and worked across both platform infrastructure and product development.

Wasim Raza

Senior Staff Engineer

Wasim is a Senior Staff Engineer at Uber for 7+ years. He has helped to build and scale Uber’s Payment Platform across platform infrastructure and payment products. His focus area is the core Payments Platform, ensuring it adapts to Uber’s evolving business requirements.
