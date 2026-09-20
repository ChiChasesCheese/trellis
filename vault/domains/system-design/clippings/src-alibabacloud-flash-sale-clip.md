---
title: System Stability Assurance for Large Scale Flash Sales
source: https://www.alibabacloud.com/blog/system-stability-assurance-for-large-scale-flash-sales_596968
published: '2020-08-12'
site: Alibaba Cloud Community
clipped: '2026-09-20'
---

# System Stability Assurance for Large Scale Flash Sales

[Blog](https://www.alibabacloud.com/blog/)

[Events](https://resource.alibabacloud.com/event/index)

[Webinars](https://resource.alibabacloud.com/webinar/index.htm)

[Tutorials](https://community.alibabacloud.com/tags/type_blog-tagid_28404/)

[Forum](https://www.alibabacloud.com/forum)

*The Alibaba Cloud 2021 [Double 11 Cloud Services Sale](https://int.alibabacloud.com/m/1000304074/) is live now! For a limited time only you can turbocharge your cloud journey with core Alibaba Cloud products available from [just $1](https://int.alibabacloud.com/m/1000304074/), while you can win up to $1,111 in cash plus $1,111 in Alibaba Cloud credits in the [Number Guessing Contest](https://int.alibabacloud.com/m/1000303353/).*

*By [Aliware Team](https://community.alibabacloud.com/users/5691256246350893)*

Twenty-six seconds after midnight on November 11, Tmall reached its peak with 583,000 transactions per second. Once again, Alibaba Cloud withstood the world's largest flow peak. This year, it was 1,457 times higher than that of the first Tmall Double 11 in 2009.

Every year during the Double 11 Global Shopping Festival, everyone needs to address the challenge of ensuring that the system can withstand peak hours and remain stable for a long time. Before the 2020 Double 11 Global Shopping Festival, Alibaba Cloud held an offline meeting in Shanghai. In the meeting, directors of Alibaba's promotion and stability assurance, middleware experts, and solution experts shared their experience with big promotions with the participants. Some of the highlights are listed below:

The first speaker is Jiang Nan. He is the Senior Solution Architect of Alibaba Cloud's East China Internet Team and has more than a decade of software development experience. Jiang Nan has been engaged in the development and architecture of cloud computing in recent years, conducting the development and construction of several cloud platforms and PaaS platforms. Therefore, he has a deep understanding and practice in cloud and Internet architectures. Currently, Jiang Nan focuses on cloud-native technologies, such as containers, middleware, and Serverless infrastructure.

Jiang Nan shared many major downtime events in the news this year. The reasons for the downtime are very typical, such as intentional data destruction, vicious attacks, improper capacity planning, insufficient scalability, or system changes. The consequences are still relatively serious. For example, the direct economic loss of a SaaS service provider was more than 20 million, and the market value fell by one billion on the same day. Besides, the market value of a new energy vehicle manufacturer fell by tens of billions of US dollars due to network interruption. The stock price can rise back, but it is difficult to eliminate the damage to consumers' confidence and the impact on the enterprise's reputation in a short time.

As for the current situation of industry stability construction, many enterprises still pay little attention to stability construction. Some small and traditional enterprises may not be ready for high availability. Even large and medium-sized companies still have shortcomings in stability construction.

The work related to stability construction is difficult to be seen, recognized, or objectively judged. They are fortunate this accident didn't happen. Even if an accident happens, it is also possible that ten other major accidents have been avoided due to good stability construction. Therefore, some methods are needed to make some qualitative and quantitative evaluations for the stability construction. By doing so, there have been different explorations, attempts, follow-up processes, and test results.

Alibaba Cloud put forward an idea about the stability construction maturity model. The two methods for evaluating the stability construction maturity have been suggested from 11 dimensions. One is the radar chart mode with the scoring from 11 dimensions to obtain an overall score. Another is the hierarchical mode. Each dimension in this mode is given 0 to 4 points according to the perfection degree of the construction. Alibaba Cloud hopes that all enterprises will at least reach the basic level, medium and large enterprises will reach the development level, and industry leaders will reach the mature level.

This maturity model is not perfect, but it is used for reference and discussion. In the future, Alibaba Cloud will continue to optimize the model by giving enterprises a reasonable evaluation reference method and analyzing the overall level of the industry. By doing so, every enterprise will have a clear understanding of the level of its stability construction in the industry and set goals for itself.

Here are some additional ideas for stability construction. The essence of stability construction is nothing more than the process of discovering and eliminating risks. Risks are mainly from the potential risks leftover from their systems and products, from the system decay caused by long-term use, from new features released and system upgrades, and from big promotions. So, the stability construction is to make these risks controllable.

Alibaba Cloud provides comprehensive products and solutions for the stability construction of the comprehensive procedure from resources to methodologies based on Alibaba Cloud. The top customers in the industry, with a small number of SREs, can provide highly efficient, stable, and comprehensive system assurance based on the various high-availability capabilities of Alibaba Cloud.

The second speaker is Zhong Ting. He is a Senior Technical Expert of the Alibaba High-Availability Architecture Team and a Team Leader of the Multi-Active Disaster Recovery and Fault Walkthroughs. He joined Alibaba in 2011 and led the 2015 Double 11 Global Shopping Festival. Zhong Ting is currently responsible for the high-availability assurance of the Alibaba economy and the output of commercial products.

Zhong Ting introduced two technical products with high-availability that can provide services to the public through two cloud services - Performance Testing Service (PTS) and [Application High Availability Service (AHAS)](https://www.alibabacloud.com/products/ahas). Preparation for Double 11 at Alibaba is a complex project that involves hundreds of horizontal and vertical projects. Technical points and issues, including capacity, architecture, and organization, needed to be solved. Focusing on these issues, Zhong Ting introduced the evolution history and selection of high-availability technologies and provided the following cloud-based high-availability solutions.

Comprehensive availability protection for business systems can be provided, covering two protections in gateway and application, multiple dimensions of ingress, application, inter-application, and single-instance load. By doing so, the high availability of systems will be improved from the aspects of low-cost access, comprehensive protection, multi-language support, and second-level protection.

The multi-site high availability (MSHA) plan is the combination of customized technology products, consulting services, and ecosystem partners.

Expertise and solutions for chaos engineering followed the experiment principles of chaos engineering and integrated with Alibaba Cloud's internal practices. Expertise and solutions provide various fault scenarios to improve fault tolerance and recoverability for distributed systems. There are various libraries, including basic resources, applications, and cloud products. Also, scenario-based walkthroughs, such as strong and weak dependencies, messages, and databases, and enterprise-level practices, such as defense walkthroughs and asset loss walkthroughs, are all available.

The third speaker is Lu Xuan. He is an architect of Alibaba Cloud's intelligent solutions. He has been responsible for the development and maintenance of large distributed systems and gained years of experience in cloud computing and cloud-native. Therefore, he has extensive practical experience in system architecture selection, troubleshooting, and performance optimization. Lu Xuan is committed to transforming cloud-native architectures to help Alibaba Cloud customers in various industries realize their business value.

The business process of flash sales is relatively simple. The point is to place an order to reduce inventory.

The flash sales promotion system is designed based on the following principles:

**1. Hotspot Identification**

Collect information in advance through marketing activities and sellers signing up

**2. Isolation Principle**

Implement isolation at the front page, application layers, and data layers

**3. Intercept requests on the system upstream whenever possible**

The traditional flash sales promotion system often fails when all of the requests are sent to the back-end data layer. In this case, slim reader/writer (SRW) lock conflicts occur, which causes high concurrency and slow response. Almost all of the requests are overtime. Among the heavy traffic, the effective traffic for a successful order is very little. For example, for a commodity with an inventory of 1,000, but over 1,000,000 consumers have checked it, the effective rate of a majority of the requests would be 0.

**4. Use cache in more-reading and less-writing scenarios**

Flash sales promotion is a typical scenario with more reading and less writing. For example, let's consider a commodity with an inventory of 1,000, but with over 1,000,000 consumers that want to buy it. The maximum number of successful orders is limited to only 1,000. The rest will just query the inventory. Under conditions like this, the writing ratio is only 0.1%, and the reading ratio is 99.9%. Therefore, this scenario is suitable for using the cache.

In the flash sales promotion scenario, the following issues needed to be considered at the architecture level.

**1. Inventory Cache** 

Redis is the main contributor to inventory deductions during the promotion. The product ID is used as the key of the [ApsaraDB for Redis](https://www.alibabacloud.com/product/apsaradb-for-redis) instance. The available inventory, equivalent to total inventory minus withheld inventory, is used as the value. The transaction feature of LUA (pronounced "LOO-ah") scripts is used to implement the logic of "deducting after reading the remaining inventory" in Redis.

**2. Capacity Planning**

By using Alibaba Cloud's Performance Testing (PTS), real user requests can be simulated to verify the impact of real business operations through users in China on the server-side performance, capacity, and system stability. This stimulation will help ensure stable support for major events.

**3. Performance Optimization**

During the pressure testing, developers can monitor all metrics of application and physical machines in real-time with the three-dimensional monitoring capability of the [Application Real-Time Monitoring Service (ARMS)](https://www.alibabacloud.com/product/arms). This helps developers quickly locate and troubleshoot issues to improve system performance.

**4. Limitation on Traffic and Requests**

[Alibaba Cloud AHAS](https://www.alibabacloud.com/products/ahas) is used for traffic limitation and degradation, ensuring stability for the system in case of an unexpected burst of traffic. Moreover, AHAS also can configure hotspot rules. In other words, if the value of the parameter exceeds a specific threshold, the system queues the traffic of Hotspot products. For example, when many consumers purchase the same products at the same time, more than 100 requests will be sent within one second while the others wait in the queue.

**5. Asynchronous Decoupling and Load Shifting**

Based on [Apache RocketMQ](rocketmq.apache.org), [RocketMQ](https://www.alibabacloud.com/product/mq) is a distributed message middleware developed by Alibaba Cloud with low latency, high concurrency, high availability, and high reliability. RocketMQ provides capabilities of asynchronous decoupling and load shifting for distributed application systems. Furthermore, features for internet applications, including massive message accumulation, high throughput, and reliable retry, are also supported.

**6. Elasticity**

Consumers with periodic promotional activities can use the Serverless Application Engine (SAE) for quick application deployment. By taking advantage of the timing elasticity, automatic scaling can be made before and after the promotion period to maximize resource utilization without manual intervention.

The fourth speaker is Ji Yuan. He is an architect of Alibaba Cloud's Intelligent Solutions. He has worked in the IT industry for 12 years and fully experienced and practiced the transformation of service-oriented architecture (SOA), microservices architecture, and cloud-native architecture in the energy industry and the internet business to business (ToB) industry. Therefore, Ji Yuan has an in-depth understanding of the cloud-native architecture of the Internet, governance, and management, and optimization of architecture high availability of microservices. With abundant practical experience, he has helped Alibaba Cloud customers make a complete cloud-native transformation for the system architecture.

Ji Yuan stated, *"The big promotion and flash sales can be used for maximizing traffic dividends, but many enterprises still haven't enjoyed traffic dividends yet. Their systems cannot support the impact of large traffic. This is caused by unpredictable issues in system performance."*

The entire system has many procedures. Each procedure may become the bottleneck, disadvantage, or constraint of the whole system. Different communication protocols, data formats, and specifications complicated the entire distributed system architecture. In addition, in the microservices architecture, service requests from beginning to end take a very long time. Once a single server goes wrong, a "domino effect" will easily occur.

Currently, most products are presented as an entry point or an app for users. The content of those is composed of multiple product lines and many well-organized modules. In practice, different teams are responsible for testing different modules and product lines. These teams take charge of the quality of a certain module or product line. When these modules are combined, the issues that are caused by mismatching or cooperation are increasing. These uncertain issues bring great challenges to the user experience, brand effect, and product revenue.

To solve the fundamental issue, these uncertain factors should be identified as completely as possible by effective solutions and methods. A system can run in two scenarios for instantaneous traffic peaks and long-term steady state.

**4.1 Instantaneous Traffic Peaks Scenario**

The scenario corresponds to big promotions and flash sales. Comprehensive procedure pressure testing can be performed in the production environment to simulate real user traffic to the maximum extent. By continuously increasing pressure, the performance constraint points of the system will be found out and optimized. This whole process will be repeated constantly. There are two key points in this process. One is the traffic source similar to real user traffic. Another is the pressure testing under the production environment for creating a real big promotion scenario to discover system uncertainties.

**4.2 Long-Term Steady State Scenario**

Alibaba Cloud implements fixed solutions of comprehensive procedure pressure testing, performs periodical fault walkthroughs, and ensures the quality of version releases and configuration changes through a unified console. Therefore, many uncertainties can be identified as soon as possible by traffic peak scenarios, and uncertainties in the system could be monitored through a long-term steady state scenario. Therefore, Alibaba Cloud can analyze and solve uncertainties to optimize system stability and high availability.

In terms of adding pressure, Alibaba Cloud's PTS simulates traffic initiated by various regions and providers based on nationwide edge nodes and content delivery network (CDN) nodes. PTS can initiate hundreds of thousands of traffic within a certain period and dynamically set regions and providers. The PTS console provides a visual method to allow customers to easily create business scenarios. Furthermore, it also integrates the native engine of [JMeter](https://www.alibabacloud.com/blog/performance-testing-using-apache-jmeter_593860?spm=a2c5t.10695662.1996646101.searchclickresult.5113b3f0SydWhO), quickly importing JMeter scripts and performing seamless migration of pressure testing tools.

In terms of traffic isolation, Alibaba Cloud provides a non-intrusive agent mode, carrying traffic isolation without modifying code to the business system. The isolation of traffic and data from pressure testing can be achieved by the rule configuration of application programming interface (API) Mock, shadow database, and pressure testing data offsets on the PTS console.

All of Alibaba Cloud's cloud-native technologies have been migrated to the cloud. Cloud-native products are used at a large scale, including [Container Service for Kubernetes (ACK)](https://www.alibabacloud.com/product/kubernetes), [RocketMQ](https://www.alibabacloud.com/product/mq), [Enterprise Distributed Application Service (EDAS)](https://www.alibabacloud.com/product/edas), [ARMS](https://www.alibabacloud.com/product/arms), and PTS. By using these products, consumers will benefit from improved cost, stability, and R&D and O&M efficiency. Moreover, these technologies have been applied to and battled tested at the 2020 Double 11 Global Shopping Festival.

                                
                                    [The Cloud Infrastructure of STO Perfectly Handles Massive Amounts of Parcels During Double 11](/blog/the-cloud-infrastructure-of-sto-perfectly-handles-massive-amounts-of-parcels-during-double-11_596967)
                                
                            

                                
                                    [SSR-based Optimization of Double 11 Virtual Venue – A More Complex Rendering Architecture](/blog/ssr-based-optimization-of-double-11-virtual-venue-a-more-complex-rendering-architecture_596970)
                                
                            

2,593 posts | 795 followers

zcm_cathy - December 7, 2020

ApsaraDB - August 12, 2020

Apache Flink Community - March 20, 2025

Alibaba Clouder - August 16, 2021

Community Builder - June 8, 2026

Alibaba Cloud Community - April 25, 2022

A key value database service that offers in-memory caching and high-speed access to applications hosted on the cloud

MSE provides a fully managed registration and configuration center, and gateway and microservices governance capabilities.

ApsaraMQ for RocketMQ is a distributed message queue service that supports reliable message-based asynchronous communication among microservices, distributed systems, and serverless applications.
