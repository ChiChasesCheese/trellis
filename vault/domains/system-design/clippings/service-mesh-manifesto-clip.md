---
title: What is a Service Mesh? Service Mesh Explained
source: https://buoyant.io/service-mesh-manifesto
published: '2020-12-03'
site: 'The Service Mesh: What Every Engineer Needs to Know about the World''s Most
  Over-Hyped Technology'
clipped: '2026-08-15'
---

# What is a Service Mesh? Service Mesh Explained

## Introduction

If you’re a software engineer working anywhere near backend systems, the term “service mesh” has probably infiltrated your consciousness some time over the past few years. Thanks to a strange confluence of events, this phrase has been rolling around the industry like a giant Katamari ball, glomming on successively bigger pieces of marketing and hype and showing no signs of stopping any time soon.

The service mesh was born in the murky, trend-infested waters of the cloud native ecosystem, which unfortunately means that a huge amount of service mesh content ranges from “low-calorie fluff” to—to use a technical term—“basically bullshit”. But there’s some real, concrete, and important value to the service mesh, if you can cut through all the noise.

In this guide we're going to attempt just that: to provide an honest, deep, engineer-focused guide to the service mesh. We are going to cover not just the *what* but also the *why* and the *why now*. Finally, we're going to attempt to describe why we think this particular technology has attracted such a crazy level of hype, which is an interesting story in and of itself.

## What is a service mesh?

A service mesh is a software layer that adds security, reliability, and observability features to cloud native applications by transparently inserting this functionality at the platform layer rather than the application layer.

Architecturally, it’s a bunch of userspace proxies, stuck “next” to your services (we’ll talk about what “next” means in a bit), plus a set of management processes. The proxies are referred to as the service mesh’s *data plane,* and the management processes as its *control plane*. The data plane intercepts calls between services and “does stuff” with these calls; the control plane coordinates the behavior of the proxies and provides an API for you, the operator, to manipulate and measure the mesh as a whole.

What are these proxies? They’re Layer 7-aware TCP proxies, just like haproxy and NGINX. The choice of proxy varies; Linkerd uses a Rust “micro-proxy” simply called [**Linkerd-proxy**](https://github.com/linkerd/linkerd2-proxy) that we built specifically for the service mesh. Other meshes use different proxies; Envoy is a common choice. But the choice of proxy is an implementation detail. *(Edit January 2020: see* *Why Linkerd Doesn't Use Envoy* *for more on why Linkerd uses Linkerd2-proxy rather than Envoy.)*

What do these proxies do? They proxy calls to and from the services, of course. (Strictly speaking, they act as both “proxies” and “reverse proxies”, handling both incoming and outgoing calls.) And they implement a feature set that focuses on the calls *between* services. This focus on traffic between services is what differentiates service mesh proxies from, say, API gateways or ingress proxies, which focus on calls from the outside world into the cluster as a whole.

So that’s the data plane. The control plane is simpler: it’s a set of components that provide whatever machinery the data plane needs to act in a coordinated fashion, including service discovery, TLS certificate issuing, metrics aggregation, and so on. The data plane calls the control plane to inform its behavior; the control plane in turn provides an API to allow the user to modify and inspect the behavior of the data plane as a whole.

Here’s a diagram of Linkerd’s control plane and data plane. You can see that the control plane has several different components, including a small Prometheus instance that aggregates metrics data from the proxies, as well as components such as destination (service discovery), identity (certificate authority), and public-api (web and CLI endpoints). The data plane, by contrast, is just a single linkerd-proxy next to an application instance. This is just the logical diagram; when deployed, you may end up with three replicas of each control plane component but hundreds or thousands of data plane proxies.

(The green lines around the boxes in this diagram represent the boundaries of Kubernetes pods. You can see that the linkerd-proxy containers actually run in the same pod as the application containers. This pattern is known as a *sidecar* container.)

The architecture of the service mesh has a couple big implications. For one, since the proxy featureset is designed for service-to-service calls, the service mesh really only makes sense if your application is built as services. You *could* use it with a monolith, but it would be a whole lot of machinery to run a single proxy, and the featureset wouldn’t be a great fit.

Another consequence is that the service mesh is going to require *lots* and *lots* of proxies. In fact, Linkerd adds one linkerd-proxy per instance of every service. (Some other mesh implementations add one proxy per node / host / VM. It’s a lot either way.) This heavy use of proxies itself has a couple implications:

1. Whatever these data plane proxies are, they’d better be fast. You’re adding two proxy hops to every call, one on the client side and one on the server side.
2. Also, the proxies need to be small and light. Each one will consume memory and CPU, and this consumption will scale linearly with your application.
3. You’re going to need a system for deploying and updating lots of proxies. You don’t want to have to do this by hand.

But, at least at the 10,000ft level, that’s really all there is to the service mesh: you deploy a ton of userspace proxies to “do stuff” to internal, service-to-service traffic, and you use the control plane to change their behavior and to query the data they generate.

Now let’s move on to the why.

## Why does the service mesh make sense?

If you’re encountering the idea of service mesh for the first time, you can be forgiven if your first reaction is mild horror. The design of the service mesh means that not only does it add latency to your application, it *also* consumes resources and *also* introduces a whole bunch of machinery. One minute you’re installing a service mesh, the next you’re suddenly on the hook for operating hundreds or thousands of proxies. Why would anyone want to do this?

There are two parts to the answer. The first is that the operational cost of deploying these proxies can be greatly reduced, thanks to some other changes that are happening in the ecosystem. Lots more on that later.

The more important answer is because this design is actually a great way to introduce additional logic into the system. That’s not only because there are a ton of features you can add right there, but also because you can add them without changing the ecosystem. In fact, the entire service mesh model is predicated on this very insight: that, in a multi-service system, regardless of what individual services actually *do*, the traffic *between* them is an ideal insertion point for functionality.

For example, Linkerd, like most meshes, has a Layer 7 feature set focused primarily on HTTP calls, including HTTP/2 and gRPC.[**<sup>1</sup>**](#) The feature set is broad, but can be divided into three classes:

1. **Reliability features.** Request retries, timeouts, canaries (traffic splitting/shifting), etc.
2. **Observability features.** Aggregation of success rates, latencies, and request volumes for each service, or individual routes; drawing of service topology maps; etc.
3. **Security features.** Mutual TLS, access control, etc.

Many of these features operate at the request level (hence the “L7 proxy”). For example, if service Foo makes an HTTP call to service Bar, the linkerd-proxy on Foo’s side can load balance that call intelligently across all the instances of Bar based on the observed latency of each one; it can retry the request if it fails and if it’s idempotent; it can record the response code and latency; and so on. Similarly, the linkerd-proxy on Bar’s side can reject the call if it’s not allowed, or is over the rate limit; it can record latency from its perspective; and so on.

The proxies can “do stuff” at the connection level too. For example, Foo’s linkerd-proxy can initiate a TLS connection and Bar’s linkerd-proxy can terminate it, and both sides can validate the others’ TLS certificate.[**<sup>2</sup>**](#) This provides not just encryption between services, but a cryptographically secure form of service identity—Foo and Bar can “prove” they are who they say they are.

Whether they’re at the request or at the connection level, one important thing to note is that the features of the service mesh are all *operational* in nature. There isn’t anything in Linkerd about transforming the semantics of the request payload, e.g. adding fields to a JSON blob or transforming a protobuf. This is an important distinction that touch on again when we talk about ESBs and middleware.

So that’s the set of features that the service mesh can provide. But why not just implement them directly in the application? Why bother with the proxies at all?

## Why is the service mesh a good idea?

While the featureset is interesting, the core value of the service mesh is not actually in the features. After all, we *could* implement these features directly in the application themselves. (In fact, we’ll see later that this was the genesis of the service mesh.) If we had to put it into a single sentence, the value of the service mesh comes down to this: **The service mesh gives you features that are critical for running modern server-side software in a way that’s uniform across your stack and decoupled from application code.**

Let’s take that one bit at a time.

**Features that are critical for running modern server-side software**. If you are building a transactional, server side application that is connected to the public Internet and takes requests from the outside world and responds to them within some short timeframe—think web apps, API servers, and the bulk of modern server-side software—and if you are building this system as a collection of services which talk to each other in a synchronous fashion, and if you are continually modifying this software to add more functionality, and if you are tasked with keeping this system running even while you’re modifying it—then congratulations, you are building modern server-side software. And all those glorious features listed above actually turn out to be critical for you. The application must be reliable; it must be secure; and you must be able to observe what it’s doing. And that’s exactly what the service mesh helps with.

(Ok, we snuck an opinion in there: that this approach is the modern way to build server-side software. There are people in the world today who are building monoliths or “reactive microservices” and other things that don’t fit into the definition above, who hold a different opinion.)

**Uniform across your stack**. The features provided by the service mesh aren’t just critical, they apply to every service in your application, regardless of what language the service is written in, what framework is uses, who wrote it, how it was deployed, or any other detail of development or deployment.

**Decoupled from application code**. Finally, the service mesh doesn’t just provide features uniformly across your stack, it does so in a way that requires no application changes. The fundamental ownership of the service mesh functionality—including the operational ownership of configuration, updates, operation, maintenance, etc—lies purely at the platform level, independent of the application. The application can change without the service mesh being involved, and the service mesh can change without the application being involved.

In short: not only does the service mesh provide vital features, it does so in a way that’s global, uniform, and independent of the application. And so while yes, the features of the service mesh could be implemented in the service code (even as a library that was linked to every service), this approach would not provide the decoupling and uniformity that’s at the heart of the service mesh value prop.

And all you have to do is add a lot of proxies! We promise that we were going to talk about the operational cost of adding all these proxies very soon. But first, we need a pit stop to examine this idea of decoupling from the perspective of *people*.

## Who does the service mesh help?

As inconvenient as it may be, it turns out that in order for technology to actually have an impact, it must be adopted by human beings. So who adopts the service mesh? Who benefits from it?

If you’re building what I’ve described above as modern server software above, you can roughly think of your team as divided into *service owners*, who are in the business of building the business logic, and *platform owners*, who are building the internal platform on which these services run. In small organizations, these may be the same people, but as the organization gets larger these roles typically get more defined and even further subdivided. (There’s a lot more to be said here about the changing nature of devops, the organizational impact of microservices, etc. But for now let’s take these descriptions as a given.)

Seen through this lens, the immediate beneficiary of the service mesh is the platform owners. The goal of the platform team, after all, is to build the internal platform on which the service owners can run their business logic, and to do so in a way that keeps the service owners as independent as possible from the gory details of operationalization. The service mesh not only provides features that are critical for accomplishing this, it does so in a way that doesn’t, in turn, incur a dependency on service owners.

The service owners also benefit, albeit in a more indirect way. The goal of the service owner is to be as productive in possible in building the logic of the business, and the fewer operational mechanics they have to worry about, the easier that is. Rather than being on the hook for implementing e.g. retry policies or TLS, they can focus purely on business logic concerns and trust that the platform will take care of the rest. That’s a big plus for them as well.

The organizational value of the decoupling between platform and service owners can’t be overstated. In fact, we think it might be *the* key reason why the service mesh is valuable.

We learned this lesson when one of our earliest Linkerd adopters told us just why they were adopting a service mesh: because it allowed them to “not have to talk to people”. This was a platform team at a large company that was migrating to Kubernetes. Because their app handled sensitive information, they wanted to encrypt all communication on the clusters. There were hundreds of services and hundreds of developers teams, and they were not looking forward to convincing each dev team to add TLS to their roadmap. By installing Linkerd, they shifted *ownership* of the feature out of the hands of developers, for whom it was an imposition, and into the hands of the platform team, for whom it was a top-level priority. Linkerd didn’t solve a technical problem for them so much as it solved an organizational problem.

In short, the service mesh is less a solution to a technical problem than it is a solution to a *socio-technical* problem.<sup>3</sup>

## Does the service mesh solve all my problems?

Yes. Er, no!

If you look at the three classes of features outlined above—reliability, security, and observability—it should be clear that the service mesh is not a complete solution for any of these domains. While Linkerd can retry requests when it knows that they are idempotent, it can’t make decisions about what to return to the user if a service is entirely down—the application must make these decisions. While Linkerd can report success rates, etc, it can’t look inside a service and report internal metrics—the application must have instrumentation. And while Linkerd can do things like mutual TLS “for free”, there’s a lot more to security solution than just that.

The subset of features in those domains that the service mesh provides are the ones that are *platform features*. By this we mean features that are:

1. **Independent of business logic.** The way that traffic latency histograms are computed for calls between Foo and Bar is totally independent of why Foo is calling the Bar in the first place.
2. **Difficult to implement correctly.** Linkerd’s retries are parameterized with sophisticated things like retry budgets because the naive approach to retries is a sure path to “retry storms” and other distributed system failure modes.
3. **Most effective when implemented uniformly.** The mechanics of mutual TLS only really make sense when everyone is doing them.

Because these features are implemented at the proxy layer, rather than at the application layer, the service mesh provides them at the *platform*, not application, level. It doesn’t matter what language the services are written in, or what framework they use, or who wrote them, or how they got there. The proxies function independent of all that, and the ownership of this functionality—including the operational ownership of configuration, updates, operation, maintenance, etc—lies purely at the platform level.

## Example features of the service mesh

**Service Mesh**

**Platform (non-service mesh)**

**Application**

**Service Mesh**

**Platform (non-service mesh)**

**App.**

**Service Mesh**

**Platform (non-service mesh)**

**App.**

**Service Mesh**

**Platform (non-service mesh)**

**App.**

To summarize: the service mesh is not a complete solution to reliability, or to observability, or to security. The broader ownership of those domains necessarily involves service owners, ops and SRE teams, and other parts of the organization. The service mesh can only provide a platform-layer “slice” of each domain.

## Why does the service mesh make sense *now*?

At this point you may be saying to yourself: ok, if this service mesh thing is so great, why weren’t we rolling millions of proxies in our stack ten years ago?

There’s a shallow answer to this, which is that ten years ago everyone was building monoliths, and so no one needed a service mesh. Which is true, but it misses the point. Even ten years ago, the concept of “microservices” as a feasible way of building high-scale systems was widely discussed, and was publicly being put into practice at companies like Twitter, Facebook, Google, and Netflix. The general sentiment, at least in the parts of the industry some people were exposed to, was that microservices were the “right way” to build high-scale systems, even if gosh they were really painful to do.

Of course, while there were companies operating microservices ten years ago, they were by and large not installing proxies everywhere to form a service mesh. If you looked closely, though, they were doing something related: many of these organizations mandated the use of a specific internal library for network communication (sometimes called a “fat client” library). Netflix had Hystrix, Google had the Stubby libraries, and Twitter had Finagle. Finagle, for example, was mandatory for every new service at Twitter, handled both client and server sides of the connection, and implemented retries, and request routing, and load balancing, and instrumentation. It provided a consistent layer of reliability and observability across the entire Twitter stack, independent of what the service itself actually did. Sure, it only worked for JVM languages, and it had a programming model that you had to build your whole app around, but the operational features it provided were almost exactly those of the service mesh.<sup>4</sup>

So ten years ago, not only did we have microservices, we had proto-service-mesh libraries that solved many of the same problems that the service mesh solves today. But we didn’t have the service mesh. Something else needed to change first.

And that’s where the deeper answer lies, buried in another difference that’s happened over the past ten years: there’s been a *dramatic* reduction of the cost of deploying microservices. The companies I’ve listed above who were publicly using microservices a decade ago—Twitter, Netflix, Facebook, Google—were companies of immense scale and immense resources. They had not just the need but the *talent* to build, deploy, and operate significant microservice applications. The sheer amount of engineering time and energy that went into Twitter’s migration from monolith to microservices boggles the imagination,[**<sup>5</sup>**](#) and this sort of infrastructural maneuver was essentially impossible for smaller companies.

Contrast that to today, where you might encounter startups with a 5:1 or even [**10:1 ratio of microservices to developers**](https://twitter.com/JackKleeman/status/1190407465659183104)—and what’s more, they are equipped to handle it. If running 50 microservices is a plausible approach for a 5-person startup, then clearly something has reduced the cost of adopting microservices.

The dramatic reduction in the cost of operating microservices is a result of one thing: *the rise in the adoption of containers and container orchestrators*. And this is where the deeper answer to the question of what change has enabled the service mesh lies. What’s made the service mesh operationally viable is the same thing that’s making microservices operationally viable: Kubernetes and Docker.

Why? Well, Docker solves one big thing: the packaging problem. By allowing you to package your app and its (non-network) runtime dependencies into a container, your app is now a fungible unit that can be thrown around and run anywhere. By the same token, Docker makes it exponentially easier to run a *polyglot* stack: because the container is an atomic unit of execution, for deploy and operational purposes it doesn’t really matter what’s inside the container, and whether it’s a JVM app or a Node app or Go or Python or Ruby. You just run it.

Kubernetes solves the next step: now that we have a bunch of “executable things”, and we also have a bunch of “things that can execute these executable things” (aka machines), I need a mapping between them. In a broad sense, you give Kubernetes a bunch of containers and a bunch of machines, and it figures out this mapping. (Which of course is a dynamic and ever-shifting thing, as new containers roll through the system, machines come in and out of operation, and so on. But Kubernetes figures it out.)

Once you have Kubernetes going, the deploy-time cost of running one service is not that much different from running ten services, and in fact not that different from 100 services. Combine that with the container as packaging mechanism that encourages polyglot implementations, and the result is a ton of new applications that are implemented as microservices written in a variety of languages—exactly the environment the service mesh is most suited for.

And so finally we come to why the service mesh is feasible *now*: the very same uniformity that Kubernetes provides for services is directly applicable to the operational challenges of the service mesh. You package the proxies into containers, you tell Kubernetes to stick ‘em everywhere, and voila! You got yourself a service mesh, with all the deploy-time mechanics handled for you by Kubernetes.<sup>6</sup>

To summarize: the reason why the service mesh makes sense now, as opposed to 10 years ago, is that the rise of Kubernetes and Docker have not only dramatically increased the *need* to run a service mesh, by making it easy to build your application as a polyglot microservices architecture, they’ve dramatically reduced the *cost* of running a service mesh, by providing mechanisms for deploying and maintaining fleets of sidecar proxies.

## Why do people talk SO MUCH about the service mesh?

**Content warning**: In this section, we resort to speculation, conjecture, inside baseball, and opinion.

One need only search for “service mesh” to encounter a Kafka-esque fever dream of a landscape, full of confusing projects, low-calorie recycled content, and general echo chamber distortion. All shiny new tech has a certain level of this, but the service mesh seems to have a particularly bad case. Why is that?

Well, partly it’s our fault. I’ve done our best to talk up Linkerd and the service mesh at every opportunity, over countless blog posts and podcasts and articles like this one. But I’m not *that* powerful. To really answer this question, I have to talk about the service mesh landscape. And it’s impossible to talk about the landscape without talking about one project in particular: *Istio*, an open source service mesh that’s billed as a collaboration between Google, IBM, and Lyft[.**<sup>7</sup>**](#)

What’s remarkable about Istio is two things. First, the sheer amount of marketing effort that Google, in particular, is placing behind it. In my estimation, the majority of people who know about the service mesh *today* were introduced to it through Istio. The second remarkable thing is just how poorly Istio has been received. Obviously, we have a horse in this race, but trying to be as objective as we can, it seems that Istio has [**developed**](https://twitter.com/quinnypig/status/1163959453810511872) a **pretty****public**[**backlash**](https://twitter.com/dave_strebel/status/1174116297468252160) in a way that’s uncommon (though not unheard of[**<sup>8</sup>**](#)) for an open source project.<sup>9</sup>

Leaving aside theories as to why that’s happening, we believe it’s Google’s involvement here that is really the reason that the service mesh space is *so* hype-y. Specifically, the combination of a) Istio being promoted so heavily by Google; b) its corresponding lackluster reception; and c) the recent meteoric rise of Kubernetes still fresh on everyone’s minds have all combined to form a kind of heady, oxygen-free environment where capacity for rational thought is extinguished and only a weird kind of cloud-native [**tulip mania**](https://en.wikipedia.org/wiki/Tulip_mania) remains.

From the Linkerd perspective, of course, this is… we would describe it as a mixed blessing. It’s great that the service mesh is a “thing” now—this was not the case in 2016 when Linkerd first got off the ground, and it was really hard to get anyone to pay attention. We don’t have that problem any more! But it sucks that the service mesh landscape is so confusing and it’s so hard to understand even *which* projects are service meshes, never mind which one fits your use case the best. That does everyone a disservice. (And there are certainly situations where Istio or another project would be the right choice over Linkerd—it’s far from a one-size-fits-all solution.)

On the Linkerd side, our strategy has been to ignore the noise, continue focusing on solving real problems for our community, and basically wait for the whole thing to blow over. The level of hype will eventually subside and we can all get on with our lives.

In the meantime, though, we’re all going to have to suffer through this together.

## So… should I, a humble software engineer, care about the service mesh?

If you’re a software engineer, here’s my basic rubric for whether you should care about the service mesh.

**If you are in a pure business-logic-implementing’ developer role:** No, you don’t really need to care about the service mesh. You’re certainly welcome to care, but ideally the service mesh won’t directly affect anything in your life. Keep building that sweet, sweet business logic that gets everyone around you paid.

**If you are in a platform role in an org that is using Kubernetes:** Yes, you 100% should care. Unless you are adopting K8s purely to run a monolith or to do batch processing (in which case, you should seriously ask the question of why K8s), you’re going to end up in a situation where you have lots of microservices, all written by other people, all talking to each other, all tied together into one unholy bundle of runtime dependencies, and you’re going to need a way to deal with that. Since you’re on Kubernetes, you will have several service mesh options, and you should have an informed opinion about which ones or even whether you want any of them at all. (Start with Linkerd.)

**If you are in a platform role in an org that is NOT using Kubernetes, but IS “doing microservices”:** Yes, you should care, but it’s going to be complicated. Sure, you could get the *value* of the service mesh by deploying lots of proxies everywhere, but the nice part of Kubernetes is the deployment model, and your ROI equation is going to look very different if you have to manage these proxies yourself.

**If you are in a platform role in an org that is “doing monoliths”:** No, you probably don’t need to care. If you are operating a monolith, or even a “collection of monoliths” that have well-defined and infrequently-changing communication patterns, then the service mesh will not add very much and you can probably just ignore it and hope it goes away.

## Conclusion

The service mesh probably doesn’t actually hold the title of “the World’s Most Over-Hyped Technology”–that dubious distinction probably goes to Bitcoin or AI. Maybe it’s merely in the top 5. But if you can cut through the layers of noise, there’s some real value to be had for anyone who’s building applications on Kubernetes.

Finally, I’d love for you to try Linkerd—it should [**take about 60 seconds to install**](https://linkerd.io/2/getting-started/?__hstc=9342122.9f37a03d298b30064ef59de46534bd68.1734033336652.1741043420325.1741105972302.35&__hssc=9342122.2.1741105972302&__hsfp=2113114665) on a Kubernetes cluster, even just a Minikube on your laptop—and you can see for yourself exactly what I’m talking about.

Want to give Linkerd a try? You can download and run the production-ready [Buoyant Enterprise for Linkerd](https://docs.buoyant.io/buoyant-enterprise-linkerd/latest/overview/) in minutes. Get started today!

## FAQs

If I just ignore this whole service mesh thing will it just go away?

Sadly, the service mesh is here to stay.

But I don’t WANT to use a service mesh

Then don’t. But see my guide above as to whether you need to understand it.

Isn’t this just ESB / middleware all over again?

Sadly, the service mesh is here to stay.Then don’t. But see my guide above as to whether you need to understand it.One big difference is that the service mesh focuses on operational logic, not business logic. [That was the downfall of the enterprise service bus](https://twitter.com/samnewman/status/1131116454118612997). Keeping that separation is critical for the service mesh avoiding the same fate.

How is this different from API gateways?

There are a million articles about this, but basically it comes down to: API gateways handle ingress concerns, not intra-cluster concerns, and often deal with a certain amount of business logic, e.g. “user X is only allowed to make 30 requests a day”.

Is Envoy a service mesh?

No, Envoy is a proxy. Envoy can be *used* to make a service mesh (and many other things; it’s a general-purpose proxy). But it’s not a service mesh.No, Envoy is a proxy. Envoy can be *used* to make a service mesh (and many other things; it’s a general-purpose proxy). But it’s not a service mesh.

I wrote a blog post about [why Linkerd doesn’t use Envoy](https://linkerd.io/2020/12/03/why-linkerd-doesnt-use-envoy/?__hstc=9342122.7b9a6ed1cc14f39b242dadcff4ff60f3.1742838825785.1743178613652.1743186075847.7&__hssc=9342122.1.1743186075847&__hsfp=416990115).

Is Network Service Mesh a service mesh?

No. Despite the name, and the talented engineers behind it, it’s not a service mesh. (Marketing is fun, right?)

Will the service mesh help my reactive, asynchronous message queue-based system?

Yes. At least, Linkerd’s ability to provide things like mTLS, policy, byte-level metrics, etc will be very useful. Other features, such as request balancing and latency monitoring, are specific to synchronous systems such as HTTP and won’t be useful, but typically your message broker will have other ways of achieving those goals.

Which service mesh should I use?

[Linkerd](https://linkerd.io/?__hstc=9342122.7b9a6ed1cc14f39b242dadcff4ff60f3.1742838825785.1743178613652.1743186075847.7&__hssc=9342122.1.1743186075847&__hsfp=416990115). Duh.

## Footnotes

1. From Linkerd’s perspective, gRPC is basically the same as HTTP/2, you just happen to be using protobuf in the payload. From the developer’s perspective, of course, it’s quite different. [<sup>\[return\]</sup>](#)
2. “Mutual” means that the client’s certificate is also validated. This is as opposed to “regular” TLS, e.g. between a web browser and a web server, which typically only validates the server’s certificate. [<sup>\[return\]</sup>](#)
3. Thanks to [Cindy Sridharan](https://twitter.com/copyconstruct) for introducing us to this term.[<sup>\[return\]</sup>](#)
4. In fact, the first version of Linkerd was simply Finagle wrapped up in proxy form. [<sup>\[return\]</sup>](#)
5. As does, frankly, the fact that it succeeded. [<sup>\[return\]</sup>](#)
6. At least, at the 10,000-ft level. There’s a lot more to it than this, of course. [<sup>\[return\]</sup>](#)
7. These three companies play very different roles: Lyft’s involvement seems to be in name only; they were the originator of Envoy but don’t appear to use Istio or even contribute to it. IBM contributes to Istio and also uses it. Google contributes heavily but as far as we can tell doesn’t actually use Istio. [<sup>\[return\]</sup>](#)
8. Systemd comes to mind. The comparison has been made, [several](https://twitter.com/pczarkowski/status/1118865428485431296) times.[<sup>\[return\]</sup>](#)
9. In practice, Istio appears to have issues not just with complexity and UX but with performance. During our [third-party Linkerd benchmark evaluation](https://kinvolk.io/blog/2019/05/performance-benchmark-analysis-of-istio-and-linkerd/) , for example, evaluators were able to find situations where Istio’s tail latency was 100x that of Linkerd, as well as low-resource environments where Linkerd happily chugged along but Istio completely stopped functioning.[<sup>\[return\]</sup>](#)
