---
title: Why Authorization is Hard
source: https://www.osohq.com/post/why-authorization-is-hard
author: About the author
published: '2025-06-11'
site: Oso
clipped: '2026-08-15'
---

# Why Authorization is Hard

**Feb 2023 Update:** Since writing this post in 2021, we've built, released, and now run [Oso Cloud](https://www.osohq.com/docs): our fully managed Authorization as a Service platform. 

Two years ago, my cofounder and I started building security tools for infrastructure. We kept hearing that application developers were building their own homegrown authorization tools. At first we were a little skeptical. People have been building authorization for many years. Isn't this a solved problem? But it kept coming up.

As we met with more engineering teams, we heard a range of responses.

Some teams told us, "We just spent 18 months building an authorization service." Others said, "Authorization is part of our core business logic, we could never split it out." Some said, "Our requirements are so simple," while others said, "Our system is crazy custom."

Both sides were right.

There's a fundamental tension in authorization. Is it business logic or [authorization logic](https://www.osohq.com/docs/oso-in-depth/glossary#authorization-logic)? Should it be in the app, or separate?

At the time, authorization wasn't particularly fashionable in tech circles. Fast-forward to today, and [Airbnb](https://medium.com/airbnb-engineering/himeji-a-scalable-centralized-system-for-authorization-at-airbnb-341664924574), [Carta](https://medium.com/building-carta/authz-cartas-highly-scalable-permissions-system-782a7f2c840f), [Slack](https://slack.engineering/role-management-at-slack/), and [Intuit](https://medium.com/intuit-engineering/authz-intuits-unified-dynamic-authorization-system-bea554d18f91) are all writing blog posts about the internal authorization systems they built. Suddenly it seems like authorization is a topic as cool as moving to Kubernetes!

Now feels like a good time to talk about what makes authorization hard, some of the approaches for solving it, and the associated tradeoffs. That's what I'll cover in this post. TL;DR

1. **Enforcing** authorization is hard because it needs to happen in so many places. Controllers, database mappers, routers, and user interfaces all need to enforce authorization. As a result, there are limited off-the-shelf approaches that work in all cases.
2. **Decision architecture** is hard because you want to separate authorization from the application, but a lot of authorization data (which we call[Facts](#) ) is application data too. A monolith can check its own database when it needs to make a decision, but what happens if you want to consolidate authorization into a separate service? Many off-the-shelf solutions focus on the separation – coordinating it and keeping everything in sync is challenging too.
3. **Modeling** authorization is hard too. It's easy to whip up the first use case — adding a`roles` table to your database works for a while. But it's hard to start simple and grow into your complexity as you need it. And it's hard to make something powerful that's simple to get started with. The options available typically err on one end of the spectrum or the other.

Note: I'm cofounder and CTO of [Oso](https://www.osohq.com/), a company that builds a framework for application authorization.

## The Three Pieces of Authorization

We can break any authorization system down into three basic parts: enforcement, decision mechanisms, and modeling. This tiny snippet of Ruby contains all three:

```
unless user.admin?
  raise Forbidden, "you must be an admin to update this post"
end
```
**Enforcement**

Enforcement is what your application actually does with an authorization decision. Once your app has decided to deny access, how does it show that to the user? That's the line `raise Forbidden, "you must be an admin to update this post"`

The challenge with enforcement is that there's no single place or single way to do it. It shows up from the data access layer all the way to the client-side interface.

**Decisions**

Authorization decisions answer the question: is the user allowed to perform this action on this resource? Decisions are made up of logic (admins can update) and data (the `user` object).

The best practice is to separate the decision logic from the application code. But decision *data* is typically made up of both authorization data (e.g. what role a user has), and application data (e.g. who wrote the post). How does the decision logic access the application data? Anything beyond a simple monolithic architecture makes this a hard question to answer.

**Modeling**

Modeling is how we group individual pieces of authorization logic into higher-level concepts. For instance, take `user.admin?` in the snippet above. That implies that `User`s can have a *role* called `admin` and that having that role grants the user some number of permissions. That's a model!

Most applications start with a simple authorization model but get complex over time. It's natural to start with simple rules and to evolve into more fine-grained permissions involving relationships and attributes.

The upshot is a tension between simple systems — easy to start with, get you going fast — and systems that can handle more complexity but have an overwhelming number of options and sometimes a steeper learning curve.

## Why Enforcement is Hard

Enforcement is a wide-reaching problem that touches everything from the data access layer all the way to the client-facing user interface.

### Why make enforcement its own concept?

The goal of enforcement is that age-old engineering principle: separation of concerns. It's common to see enforcement and decision intermingled. Take the snippet of Ruby code from above:

```
unless user.admin?
  raise Forbidden, "you must be an admin to update this post"
end
```
Here we have the decision inline: "the user can update the post if they are an admin." And then the enforcement: "raise `Forbidden` if the decision is to deny."

The usual rationale for separation of concerns applies. If we add a new user role, "editor," we don't want to hunt through the code-base for all the places where we'll need to update the logic. It's too easy to miss a place to update!

Many existing authorization libraries offer a better approach. For example, the Ruby library `pundit` puts all authorization decisions behind an `authorize` interface:

```
def update
  @post = Post.find(params[:id])
  authorize @post
  ...
end
```
This way, you can implement the decision mechanism separately.

As we'll see in the following sections, existing authorization solutions will help you solve enforcement problems to varying degrees. Library solutions typically use a tighter integration with specific frameworks to offer more functionality. Authorization services and policy engines generally have a smaller footprint in the application, but can only offer limited support based on whatever generic API they expose.

### Separating concerns is particularly hard for enforcement

Getting the right abstraction for enforcement is hard. In general, the higher up the stack you perform authorization, the coarser it becomes. Push it lower down the stack, and it gets more fine-grained but takes more effort to implement.

The previous example using `pundit` is one of the most common enforcement scenarios — can the current user perform some action (`:update`) on a resource (`@post`)? That's called **resource-level** enforcement, and it works well: it's explicit and very flexible.

On the other hand, you'll need to add resource-level enforcement statements all over an application. It's tedious and error-prone. Usually, you'd solve that by putting this logic higher up the stack, closer to the middleware or request handlers.

But if we try to push this logic into a generic request middleware, we'll probably find ourselves re-implementing the logic of `Post.find(params[:id])` ("find post matching the ID supplied in the request parameters"). Now we've gone too far and pushed application logic into the authorization code.

This is what makes enforcement hard — if we want to keep to a clean abstraction, with good separation of concerns, we end up needing to add enforcement to many places in the code.

**Data Filtering**

Another challenge is: how do you perform enforcement in bulk? That is, what if I want to get all posts that a user can read? Do I have to fetch all records and authorize them individually? Can I recreate my rules as database filters? The former would be prohibitively slow, and the latter would break separation of concerns.

Framework-specific solutions have solved these problems to varying degrees. Continuing on our Ruby theme, Pundit has [scopes](https://github.com/varvet/pundit#scopes) and CanCanCan has [`accessible_by`](https://github.com/CanCanCommunity/cancancan#fetching-records) . Both of these use ActiveRecord integrations to support attribute-based filtering for database queries.

Similarly, [CASL](https://github.com/stalniy/casl), a library for JavaScript, takes the concepts in CanCanCan and extends them further to translate them to different database adapters.

Unfortunately, these frameworks tend to only support specific authorization models. We'll cover this topic in more depth in Modeling, but for example: [CanCanCan](https://github.com/CanCanCommunity/cancancan/blob/develop/docs/role_based_authorization.md) has example documentation for implementing roles, but this does not handle roles on a per-resource level. This prevents you from implementing cross-organization roles, or fine-grained permissions.

Alternatively, [Google Zanzibar](https://research.google/pubs/pub48190/) and systems built on the same principles generally implement something called "reverse-indexing." Reverse indexing is an API that returns all resources a user can access or all users who can access a given resource.

But, Zanzibar relies on a centralized data model, so:

1. You need to migrate or sync all your data – not just authorization data like roles and permissions, but any data that you would use to make an authorization decision – into the service. And it turns out that this can mean most of the data in your application. We will come to this in more detail in the section on Decision Architecture.
2. You need to figure out how to integrate results from the service with any subsequent application actions. For example, Zanzibar can give me all the resources I can see, but I might still need to join this list with my own database and implement pagination.

At the end of the day, you will almost certainly need some form of data filtering for list endpoints. When the authorization logic is reasonably simple, taking a manual approach can work. But as logic gets more complex, you want to implement data filtering in a way that maintains the separation of concerns. Making data filtering work well needs a framework-level integration, which is not something typically offered by authorization service implementations.

**Showing Permissions in the UI is Hard**

To give your end-users any hope of navigating through your system of permissions, you also need to expose some amount of the authorization to the user interface.

GitHub UI showing a few repository actions with certain buttons unavailable based on permissions.

Now your authorization decisions need to be available in the frontend too. Again, we want to avoid breaking the separation. We really don't want to recreate the same logic from the backend in the frontend.

One approach would be to somehow share logic between the frontend and backend.

For example, the CASL library runs both on a Node.js backend as well as in the browser — the same JavaScript code can be used across both. Similarly, the policy engine OPA makes it possible to compile policies to WASM, so these could be shared with [frontend code](https://github.com/open-policy-agent/npm-opa-wasm/). But evaluating a policy requires access to data, not all of which might be available to the frontend. Additionally, it makes frontend and backend intrinsically coupled.

The alternative is to make it possible for the backend to return just permissions data to the frontend. The idea is to expand the enforcement API to not just answer *if* the user can perform this action, but *what* actions the user can perform too.

This might end up being a large amount of data. Instead, the backend can expose an API to ask whether a user has a specific permission. Doing this might result in clobbering the backend and slow performance. Slack recently discovered that they had this problem, and added in a cache of permissions data.

Client-side authorization architecture at Slack

Once you have permissions data, you can start building a UI that is "permissions-aware." For example, it can hide UI elements, or provide helpful information based on permissions data.

For more inspiration in this area, go read [this fantastic post](https://www.johnnunemaker.com/rails-authorization/) from John Nunemaker diving into returning the "why" back to users.

```
unless record.enabled?
  deny! :disabled, "Disabled tokens cannot access the API."
end
```
**Summary**

Overall, enforcement is a problem area that needs more attention. Most frameworks tend to do the basics, and in some cases also address data filtering, but often leave a lot to the application developer to figure out. Authorization services tend to stay away from this domain entirely since their approach is all about decoupling authorization from the application.

Enforcement needs to be a first-class citizen in application systems, which means supporting who can do what in my application and why. We've been working on this at Oso.

### How Oso does enforcement

A big part of the challenge we were looking to address was first the availability of information around this problem. As I said before, a lot of people don't even think about this area at all. So we wrote the [Enforcement chapter of Authorization Academy](https://www.osohq.com/academy/authorization-enforcement) to cover the different approaches and when to use them. These are not specific to Oso at all, and instead can be used by anyone to implement authorization.

One of the problems we've had to solve was how to provide a consistent interface to enforcement across multiple languages and frameworks. Here's what that looks like in Oso:

```
# can the user update the post
oso.authorize(user, "update", post)
# what posts can the user read?
posts = oso.authorized_resources(user, "read", Post)
# what can the user do on the post?
actions = oso.authorized_actions(user, post)
```
[List filtering](https://www.osohq.com/docs/app-integration/integrate-authorization/filter-lists) in Oso works by using [Polar](https://www.osohq.com/docs/reference/polar/foundations) to evaluate policies and return a set of filters. The same approach works for fetching all the permissions a user has on a resource, or all the users that can read a resource.

We have more work to do here to make this as easy as possible to integrate from the database down to the UI. But we believe this integration is essential for any authorization framework.

## Why Decision Architecture is Hard

Whereas decision enforcement is fundamentally tied to the application, the decision-making mechanism can live virtually anywhere.

What makes it hard to choose how to architect authorization, is that there is a matrix of possible options for how your app is structured, where your data lives, and where the authorization decision is made.

- Is your application a monolith, or made up of multiple services?
- Is your decision logic in the app or is it in a separate service?
- Is all the data you need for authorization in the app or somewhere else?

And there are unique considerations for each of the *eight* (2^3 🙂) combinations. Below we will look at the six most common combinations; the others don't make sense to cover separately.

I'll speed through the six combinations, with an eye towards when they come up and how you might deal with the associated tradeoffs. Each case merits its own post, so please bear with me. Come find me on Twitter/in our Slack/buy me a coffee if you want the full version.

### What makes up a decision

Authorization decisions answer whether an **actor** (e.g. the user) can perform an **action** on a **resource**. In our previous example, where admins can update posts, this might look like:

```
class PostPolicy < ApplicationPolicy
  def update?
    user.admin?
  end
end
```
The two pieces that make up a decision are logic and data.

1. Logic: rules and conditions that govern access (e.g., admins can update posts).
2. Data: record-level information about application objects (e.g., whether this user is an admin).

Data is made up of:

- Application data: fields of your data model (this post is marked as public), as well as the relationships between data models (this post belongs to this project, which belongs to this organization).
- Authorization data/Facts: permissions and roles (this post was shared with this user, this user is an admin of Acme org).

Despite giving them those nice clean labels, the separation isn't that clean.

You often need application data when evaluating authorization logic. For example, you can view a post if it belongs to a project you were assigned to. In this case, information about *if you were assigned to the project* and *if the post belongs to the project*  are part of your data model. You will use them as inputs to an authorization decision, but they're also fundamental to your app itself. In this way, it is hard to cleanly separate application data and authorization data (Facts).

So, the challenge is figuring out how to let the decision mechanism access the data it needs, while also keeping the data available to the application.

### What are the architecture options?

Okay, let's do this. 6 architectures in 6 minutes or your money back.

I. **Beginner's Delight – the Monolith**

Also known as the "status quo." This is what you have by default.

The application is a monolith, so both logic and data live in the monolith.

Authorization logic — presumably kept separate by the enforcement interface — has direct access to the application. You probably don't even give it a second thought.

For example, in CASL (JavaScript framework which supports data filtering), you can express permissions like:

`can('read', 'Post', { authorId: 1 });`
This example expresses the permission: "[user] can read posts with `authorId` equal to 1". `authorId` is a field on the model, i.e. application data. If the application developer decided to refactor this so that posts could have multiple authors, then the permissions logic would no longer be valid.

II. **Monolith with some external data (e.g. roles)**

This is a slight variation on the standard monolith. It's common to have some data *outside* the monolith that you need to use for authorization. For example, if using an identity provider like Auth0 or Amazon Cognito to manage users and their roles, you might end up with authorization data outside of the application.

This brings with it the challenge of how to get the data. You now need to either query that external identity service or put authorization information into secure tokens and make it available to the monolith.

III. **Monolith calling out to an authorization service**

The primary scenario in which this combination comes up is when you have not one, but multiple monoliths. Maybe you're moving towards microservices, or maybe you just like the idea of outsourcing your authorization to someone else.

So, you move the decision logic completely out of the monolith into a separate service. The main benefit of this approach is that you can amortize the functionality that the service provides across all monoliths calling into it. If that functionality is particularly complex, then there can be value in having a specific team or another company manage this on your behalf.

But in order to do its job, this service will also need to get the relevant data – the question is how. You might store *zero* data in the service, and ensure that application developers include it on every request. Or you could store all roles and permissions data in the service, plus any application data needed for decisions. In the latter case, you will need to work out some sort of mechanism to keep this data in sync with your monoliths.

You will still have to reimplement enforcement across all the monoliths.

**Introducing... Microservices**

Unsurprisingly, everything gets harder once you move from a monolith to an application made up of microservices. Note: here I use the term *microservices* broadly. This could mean an app with a small number of *services*, too.

Take [Airbnb](https://medium.com/airbnb-engineering/himeji-a-scalable-centralized-system-for-authorization-at-airbnb-341664924574) and [Carta](https://medium.com/building-carta/authz-cartas-highly-scalable-permissions-system-782a7f2c840f). Both write that they didn't have trouble with their authorization systems until they started breaking up their monoliths into service-oriented architectures.

The problem: for any decision that needs data from more than one service, you need to figure out how to make that data available.

IV. **Microservices — keep logic and data local to the individual microservices**

In this scenario, you break up your application into microservices. Each microservice owns and manages its own data. Each microservice is responsible for enforcing access to the data it manages, so the authorization logic lives in each microservice too.

The benefit of this approach: by keeping the logic, and in particular, the data local to each microservice, you maintain the service boundaries that (in all likelihood) you sought to create when you moved to microservices. If you update your application data model in an individual microservice, the relevant authorization data model is automatically updated because the two are one and the same.

The downside is that you may end up repeating similar logic across microservices. In practice, most microservices handle separate authorization logic since they are enforcing different parts of the application. The parts that might be shared would be logic around how users are assigned roles within an organization.

This comes up when multiple microservices share a single concept of a user. This is effectively the same situation as the monolith with external data. You can apply the same solutions as before — either having a single 'users' microservice and querying it for data as needed, or putting user information into secure tokens.

Again, you will still have to reimplement enforcement across all the microservices.

V. **Microservices — keep logic in the individual services, manage data in a data service**

At larger scale, you can end up with many data interdependencies between services. You might have deeply nested, hierarchical data, like what might occur at Google or Facebook. At that point, the company may decide to invest in a central data access layer.

For example, Twitter has [Strato](https://about.sourcegraph.com/graphql/graphql-at-twitter/) as a "virtual database" to federate access to data, and is the idea behind [GraphQL federation](https://www.apollographql.com/docs/federation/), and [Prisma's vision](https://www.prisma.io/blog/prisma-raises-series-a-saks1zr7kip6#inspired-by-the-data-layers-of-big-companies-twitter-facebook-) for a unified data access layer.

If all microservices have a consistent way to access the data they need, then in a sense it's like being back in the monolith world! The authorization system can fetch the data to make a decision. Not bad, but also not terribly common in the real world.

Again, you will still have to reimplement enforcement across all the microservices.

VI. **Microservices — with an authorization service**

In this scenario, you introduce an authorization service. The benefit of this approach is you get to fully decouple logic from the application. This makes it possible to share authorization logic between different microservices.

But now you have a service boundary problem. If one microservice's data structures change, you have to update how your policy handles them. And, if you'd like to make a change to the way the policy consumes data, you'll have to update your microservices' data. Microservices decoupling undone!

There are actually two flavors of this scenario: one where the authorization service manages no data, and one where it does manage data. Both are subject to the tradeoffs described above, but for the sake of brevity, let's focus on the latter. This is the approach that Google implemented in Zanzibar. The benefit is that you often have everything you need to make an authorization decision in one place – logic and data. The challenges are now:

1. You need to remodel all data from all microservices into the authorization service's single data model
2. You need to find a way to sync data from your microservices to the authorization service on an ongoing basis (and manage conflicts, etc.)
3. This service is on the critical path of nearly every request, so you need to find a way to ensure you can meet your latency service-level objectives despite having just added an extra dependency – either through caching or some other mechanism
4. Related, you need to ensure you can meet uptime SLAs. If the authorization service is down, either your app goes down or you have to fail open

Again, you will still have to reimplement enforcement across all the microservices.

### Options for Decision Architecture

Phew! That was a lot. Now onto the options available today for implementing the scenarios above:

Most authorization libraries work for a specific framework, making them an easy choice for monoliths (1 and 2). For implementing authorization where you keep logic and data local to microservices (3), you might want to look for a cross-language solution for consistency. You could use an authorization library like Oso to build an authorization service (4), but it isn't a service itself.

Policy engines like OPA, and authorization services built on them, can also be used for any of the scenarios where you want a separate authorization service. They give you a centralized way to manage policies, but require you to figure out how to manage the data and make it available for authorization decisions; and how to meet latency and uptime SLAs (considerations 2-4 above).

Authorization services like Zanzibar, or those built on Zanzibar, can also be used for any of the scenarios where you want a separate authorization service, but take a more opinionated approach. They give you everything you need to make an authorization decision in one go, but come with all the data structure and operational tradeoffs that you need to sort through (considerations 1-4 above).

### How Oso does decision architecture

My golden rule for authorization is: *Build authorization around your application, not the other way around.*

For a monolithic application, Oso offers a simple approach. It's a library, which lends itself well to handling decisions that require access to application data.

For microservices, a common pattern we see is a take on scenario IV: keep domain-specific logic and data in the individual microservices, and build a microservice to manage shared logic + data for things like users, roles and permissions.

If you want a central authorization service, you can use Oso to build one. But it will come with all the same operational considerations on centralizing data, latency and uptime (considerations 2-4 above). There is no way around those. Or for a preview of [what we're building](https://www.osohq.com/docs) to solve this problem, you can [set up a 1x1 with an Oso engineer](https://calendly.com/osohq/oso-cloud-1-on-1).

## Modeling

What we've covered so far aren't even areas that people typically consider as part of the challenge of authorization! The heart of any authorization system is how you model your authorization logic. This often means controlling access based on roles, relationships, or attributes ([RBAC,](https://www.osohq.com/academy/role-based-access-control-rbac) [ReBAC](https://www.osohq.com/academy/relationship-based-access-control-rebac), and [ABAC](https://www.osohq.com/learn/what-is-attribute-based-access-control-abac) respectively).

The difficulty in modeling authorization is achieving a model that's easy to get started with and simple to understand, but that can also extend to the kinds of complex scenarios that every authorization system inevitably ends up facing.

### What is modeling?

Continuing on our earlier example:

```
class PostPolicy < ApplicationPolicy
  def update?
    user.admin?
  end
end
```
The logical piece is "admins can update posts."

The abstract model underlying this is role-based access control (RBAC). If you're interested in reading more about this model, which you're likely to encounter in any authorization system, I like [this post](https://heap.io/blog/structure-permissions-saas-app) for a succinct, pragmatic introduction to roles, or our own [Authorization Academy](https://www.osohq.com/academy/role-based-access-control-rbac) chapter for a detailed explanation.

The general idea is that you assign permissions to *roles* rather than to users, and make authorization decisions based on the role that someone has.

Other typical models include: relationship-based access control (ReBAC), which uses the relationships between data to decide access (e.g., users can close issues that they submitted); and attribute-based access control (ABAC), which more or less means using any piece of data (attribute) to make an authorization decision.

### What's hard about modeling?

Starting out, almost every application will want to implement some form of basic roles, e.g., admins can "read, update and delete," and members can only "read." You can implement this yourself, or find a library to do it.

But inevitably, models change over time. In our experience, it's pretty common for teams to refactor their authorization models four or five different times. Sometimes those continue to exist at the same time:

But we had a problem. Instead of maintaining one legacy system, we were maintaining five. The permissions could conflict — and they were impossible to extend. Our business needs were growing, and we had several new products in the funnel.

*— Aaron Tainter at* *Carta*

The reason this happens is because — correctly — no engineering team wants to spend cycles early-on building a bulletproof authorization system to meet all their future requirements.

So you start with a simple `is_admin` field on the user. After all, that's all that differentiates access. Later you start tracking what `role` the user has — still a fairly simple change.

As the company grows, you start attracting larger clients. They need to start assigning granular access based on sub-resources like projects. Maybe users can have multiple roles, resource-specific roles, or belong to groups. There might be resources that users can conditionally access based on attributes.

All of this was mostly written from the perspective of teams building authorization themselves. But there are existing solutions that address some of this.

**Libraries for role-based access control**

There are a lot of libraries for simple role-based access control. They vary a fair bit, so it's hard to summarize them all at once. Many focus on simple global roles without any further granularity. Others go further, such as Casbin, which also manages your roles data, and supports basic attribute-based access control.

The main pro of these libraries is that you get them in whatever language you're using for your app, and in some cases they may give you what you need.

The challenge is that while everything works okay while you're on the paved road, things start to break down once *go off the trail.* As such, these libraries are often sufficient in the beginning but start showing limitations before too long.

Here is an example. (I don't mean to pick on any specific library, so I went to [Django packages](https://djangopackages.org/grids/g/perms/) for permissions, and picked the [first that mentions roles](https://django-role-permissions.readthedocs.io/en/stable/quickstart.html)). It seems like it does what you need:

```
>>> from rolepermissions.roles import assign_role
>>> user = User.objects.get(id=1)
>>> assign_role(user, 'doctor')
```
Indeed, you can assign roles and permissions to users. It manages the data model for you.

But this simple roles implementation cannot handle [role inheritance](https://github.com/vintasoftware/django-role-permissions/issues/125) — a fairly common requirement — e.g., a super admin can do everything an admin can do, and then some.

**Zanzibar**

We've already covered what you get from Zanzibar from an architectural standpoint. But one of the other core contributions from Zanzibar was the proposed authorization model.

Relationship-based access control (ReBAC) is an extension of role-based access control and cleanly encompasses both direct permissions (access control lists, or ACLs) as well as relationships between resources (like in hierarchical data structures). In the [Google Zanzibar paper](https://research.google/pubs/pub48190/), the authors also present a version of a configuration language for expressing logical rules over that data format.

What's great about the Zanzibar model is that it is highly opinionated. "Think about your authorization data as relationships," it says. As a developer, there's comfort in knowing someone has done the thinking for you and chosen a model.

The challenges are:

1. You need to orient yourself and all of your authorization logic to this model (the data too, of course, but we covered that earlier). It can be a little mind-bending at first to understand how roles are represented as a relationships, and how "userset rewrites" accomplish concepts like role hierarchies.
2. If you have an authorization scenario that doesn't fit the model, you need to go outside Zanzibar to implement it. For instance, if you need attribute-based access control – e.g., anyone can read this repo if it's public – you would implement that somewhere else. Existing Zanzibar implementations suggest [pairing with policy engines](https://web.archive.org/web/20230301072401/https://github.com/ory/keto/issues/319) to support attributes.

**Policy engines**

This leaves us with policy engines. Two of the most well known policy engines are [XACML](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=xacml) — a bit of a dated implementation with an XML-like syntax — and [OPA](https://github.com/open-policy-agent/opa).

From a flexibility standpoint, policy engines offer you pretty much anything you need! And if it doesn't have what you need, you can typically build it. So, lots of runway.

Conversely, by focusing on making it possible to do anything, there is less in the engine itself that guides you towards implementing specific use cases like roles or relationships, for instance. This means implementing common authorization patterns like basic roles is *possible*, but you as the developer will do most of the thinking to get where you need to go.

The learning curve is another downside to the power of many policy languages, and one of the common challenges that new users cite. For example, in the Kubernetes landscape, [Kyverno](https://github.com/kyverno/kyverno) emerged as a simpler alternative to OPA's Gatekeeper. Less flexible, but simpler and more familiar to existing Kubernetes users. This shows where that tension comes in.

### How Oso does modeling

Oso is at its core a policy engine, but with abstractions for common authorization patterns like RBAC, ReBAC, and ABAC layered on top. It is based on [Polar](https://www.osohq.com/docs/reference/polar/foundations), a purpose-built declarative policy language. We include these abstractions as primitives built into the language – for roles, relationships and other common patterns. For instance, using a [resource block](https://www.osohq.com/docs/reference/polar/resource-blocks), you can write `"update" if "admin" on "parent_org"` to say: a user can update [a post] if they are an admin on the parent organization [of the post]. This is similar to how relationships work in Zanzibar, and it expresses a lot. In this line, we have granular access on a post, traversing relationships between data.

The pro of this approach, like with other policy-based approaches, is you are unlikely to run out of runway. Providing primitives for common authorization patterns helps early users get off the ground the way many libraries do. Layering these primitives on top of the language itself provides a glide path from simple to complex.

The tradeoff is that, like policy engines and Zanzibar-based systems, you need to learn a new way to express authorization logic.

## Conclusion

I come back to my original claim that the three hardest problems in authorization are:

1. Enforcement, which comes down to separation of concerns
2. Decision architecture, which comes down to how you bring together authorization logic and the data it depends on
3. Modeling, which comes down to a tension between abstract patterns and the details of your application

While these are hard problems, it's great to see that we've gone from "Isn't this a solved problem?" to "What's the best way to solve them?"

And if you're interested in *our* view on the best way to solve authorization, check out our [documentation](https://www.osohq.com/docs).
