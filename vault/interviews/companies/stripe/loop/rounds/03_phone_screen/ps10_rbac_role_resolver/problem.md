# ps10 · RBAC Role Resolver

**类型：** Phone Screen（Technical Screen）· **阶段：** Technical Screen（电面）· **最近一次报告：** PracHub 2026-05-12 · **频率：** PracHub 与 1point3acres 两个独立站点各收录一道"账户层级 + 角色/权限解析"题，标题不完全相同但主题一致（PracHub: "Resolve User Roles Across Account Hierarchy"；1point3acres: "RBAC Role Resolver"）· **置信度：** medium-low —— 1point3acres 原始来源（post/7100148）的镜像现在给出了完整的四段式目录（`Phase 1: Direct Role Lookup` / `Phase 2: Adding Inheritance` / `Phase 3: Finding Users with Access` / `Phase 4: Filtering Users by Role`，只有标题，没有正文），证实了本题**四个 part 的划分和递进方向**不是本仓库凭空编的——Part 1/2 沿用原有的高置信度重建（直接查角色 / 继承并集），Part 3/4 据此改成了与标题吻合的"反向查询"主题（给权限找用户 / 给角色找用户）。但目录之外没有任何一处正文——具体规则（"拥有角色"是否算继承、去重规则）、字段名、输入输出格式、以及全部 worked examples 的数值，**依然全部是本仓库自拟**，见下方警示块与 Sources。

> ⚠️ **重建题（part 划分有据，规则与格式仍自拟）**：本题面的四个 part——Part 1 直接角色、Part 2
> 继承（并集）、Part 3 反向查询"谁有这个权限"、Part 4 反向查询"谁有这个角色"——与
> 1point3acres「RBAC Role Resolver」
> （https://www.1point3acres.com/interview/problems/post/7100148）镜像页面公开的四段式目录
> （Phase 1: Direct Role Lookup / Phase 2: Adding Inheritance / Phase 3: Finding Users with Access /
> Phase 4: Filtering Users by Role）一一对应，**part 的数量、顺序、主题不是本仓库凭空编的**。
> 但该镜像只留下了章节标题，没有任何一处正文被抓取到——具体的字段名（`account_id`/`parent_id`）、
> "拥有角色"是否包含继承、输入输出协议、以及全部 worked examples 的具体数值，**依然全部是本仓库
> 自拟**，不要把这里的规则细节或输出格式当成真题背。本题练习 **S03、S18、S08、S19**。
> （本题面此前的 Part 3/4 是另一套自编内容——"通配符 + deny 全局优先"与"批量查询双层缓存"——与
> 上述真实的四段式标题完全对不上；本次改动已将它们替换为与标题吻合的反向查询设计，详见 REPORT.md
> "为什么改这次"一节。）

## Context
Stripe's platform accounts sit above a hierarchy of connected accounts (a platform's users manage
one or more connected accounts, and a connected account can itself have sub-accounts). A single
user can hold different roles at different levels of that hierarchy — a support engineer might be
a read-only `viewer` on the whole platform but a full `admin` on one specific connected account
they're actively investigating. Part 1/2 answer "what can this one user do here?" by walking the
account tree forward, from the user's own assignments down to the account in question. Part 3/4
flip that question around — "which users can do *this*?" / "which users hold *this role*?" — the
kind of audit query a security team runs when a permission or a role needs to be revoked or
reviewed, and a per-user forward scan of the whole system is the wrong tool for answering it at
scale.

## Input
`accounts`: a list of `{account_id, parent_id}` (a root account, e.g. a platform account, has
`parent_id = None`). `roles`: a list of `{role_id, permissions}` where `permissions` is a list of
plain, literal permission strings (e.g. `"charges:read"`) — no wildcards, no denies, exact string
equality throughout every part of this problem. `assignments`: a list of `{user_id, account_id,
role_id}` — a user may hold at most **one** role at any single account (holding different roles at
different accounts is normal and expected, and the same role at two different accounts is also
allowed).

## Rules

### Part 1 — direct role, no hierarchy
Return the sorted permissions of the role `user_id` is **directly** assigned at `account_id`
itself — `[]` if the user has no role there. Do not look at ancestors yet. Assume the input is
well-formed (no validation required in this part).

### Part 2 — hierarchy inheritance (union)
Accounts now form a tree via `parent_id`. A user's effective permissions at `account_id` are the
**union** of the permissions granted by every role the user holds anywhere along the chain from
the topmost ancestor down to `account_id` itself (a level where the user holds no role there
simply contributes nothing). Inheritance is additive only — a role at a closer level never removes
a permission granted by a role at a farther level. Return the sorted union.
**Validate** (raise `ValueError` — a clear message is enough, exact wording is not tested):
a duplicate `account_id` or `role_id` in the input; an assignment naming an unknown `account_id`
or `role_id`; two assignments for the same `(user_id, account_id)` pair; an `account_id` anywhere
in the ancestor chain that isn't in `accounts`; or a `parent_id` cycle (including an account that
is its own parent). A cycle must be **detected and rejected**, never walked forever.

### Part 3 — Finding Users with Access (reverse: permission -> users)
Given an `account_id` and a `permission` string, return the sorted, deduplicated list of every
`user_id` who **effectively has** that permission at `account_id` — i.e. every user for whom
`permission` would show up in Part 2's result if you called it with that user and that
`account_id` (a direct role at `account_id` itself, or a role inherited from any ancestor, exactly
Part 2's union rule; still no wildcards, still exact string equality). A user is only a candidate
because of **their own** assignment somewhere on `account_id`'s ancestor chain (root down to
`account_id` itself) — another user's role never makes anyone else a candidate, and a user's role
at some unrelated account elsewhere in the tree (not an ancestor of `account_id`) never does
either. Same structural validation and cycle detection as Part 2, applied to `account_id`'s chain.

A `permission` string that no role in the system ever grants is **not** an error, just `[]` —
`permission` is a free-form value with no declared catalog (like `user_id`), unlike `account_id`
and `role_id`, which do have one (`accounts` and `roles`) and raise on an unknown reference.

**Why the obvious approach doesn't scale**: reusing Part 2 by calling it once per user — "for
every user in the system, compute their effective permissions at `account_id` and check if
`permission` is in there" — costs `O(U × D)` where `U` is every user who has ever been assigned a
role *anywhere* and `D` is the chain depth, even though only a handful of those users could
possibly be relevant (the ones with an assignment on this one chain). Part 3 is answerable in
`O(D + M)`, where `M` is the number of assignments that actually sit on `account_id`'s own
ancestor chain, by indexing assignments **by account** instead of scanning every user: walk the
chain once (`O(D)`, and only the chain — never the accounts on some other branch of the tree), and
at each level look up only the assignments recorded *there* — see "Why later parts break earlier
assumptions" below and REPORT.md's complexity section for the measured gap between the two.

### Part 4 — Filtering Users by Role (reverse: role -> users)
Given a `role_id`, return the sorted, deduplicated list of every `user_id` **directly** assigned
that role, at any account.

**Decided rule — "having" a role is direct-only, and inheritance is provably the same set here**:
Part 2 already establishes that a user's effective *permissions* at a descendant account are the
**union** of every role they hold along their own chain — which means a single user can be
simultaneously "under the effect of" several different roles at once. There is no single role
that "is" a user's role at a descendant account once more than one ancestor level contributes, so
"does user X have role R" can only be answered as "is X directly assigned R at some account" —
there is no separate, well-defined notion of "R inherited" the way there is for a single
permission string in Part 2/3. This is not just a simplifying assumption: because inheritance in
this model only ever propagates a user's *own* roles down their *own* chain (Part 3's rule — never
across users), a user can only ever "inherit the effect of" role R at some descendant account if
they *already* directly hold R somewhere on their own chain above it. So "direct-only" and "count
inheritance too" produce the *exact same set of user ids* for this query — Part 4 picks the
simpler of two provably-equal definitions, not an arbitrary one. (Two different roles that happen
to grant an identical set of permissions are still two different roles for this purpose — Part 4
answers "who holds role R", not "who effectively has R's permissions"; see the worked example.)

A `role_id` unknown to the system (not in `roles`) -> `ValueError` (same asymmetry as
`account_id`: `roles` is a declared catalog, so referencing one that isn't in it is a caller
error). A `role_id` that is valid but that nobody happens to hold -> `[]`, not an error.

## Why later parts break earlier assumptions
This progression is deliberately not just "add more rules" — each part invalidates a structural
choice a straightforward Part-N implementation would make:
- **Part 1 -> Part 2**: a Part 1 solution can get away with a flat, one-shot scan over
  `assignments` (no indexing, no tree at all). Part 2 makes that insufficient — you now need an
  indexed graph walk with cycle protection, not a bigger scan.
- **Part 2 -> Part 3**: Part 2 answers "user + account -> permissions" with a *forward* walk up
  one user's own chain. Part 3 flips the query direction: "account + permission -> users." Calling
  Part 2's logic once per user to answer it is `O(U × D)` and wastes almost all of that work on
  users who were never assigned anywhere near the queried chain. Part 3 forces a **reverse index**
  instead — group assignments by `account_id` once, so a query only ever touches the assignments
  that live on `account_id`'s own ancestor chain, not every user in the system.
- **Part 3 -> Part 4**: Part 4 flips the grouping key again ("role -> users"), but this time there
  is *no hierarchy to walk at all* — a role's identity is direct-only (see Part 4's rule above), so
  even the ancestor-chain walk that Part 3 still needed disappears entirely. What is left is a pure
  indexing problem: a role-keyed reverse index over `assignments`, built once, turns every query
  into an `O(1)` lookup instead of an `O(assignments)` scan — the "harder" reverse-index problem
  (Part 3, which still needs the chain) and the "easier" one (Part 4, which doesn't) are worth
  telling apart, not solved with the same amount of machinery.

## Worked examples
Shared setup:
```
accounts: platform (root) -> connected (parent: platform) -> submerchant (parent: connected)
roles:
  viewer:  [payouts:read, charges:read]
  admin:   [charges:read, charges:write, payouts:read, payouts:write]
assignments:
  alice @ platform  -> viewer
  alice @ connected -> admin
  bob   @ submerchant -> viewer
```
- `part1(..., "alice", "connected")` -> `["charges:read","charges:write","payouts:read","payouts:write"]`
  (alice's own role at connected, no inheritance needed)
- `part1(..., "alice", "submerchant")` -> `[]` (alice has no role AT submerchant itself; Part 1
  never looks at ancestors)
- `part2(..., "alice", "submerchant")` -> `["charges:read","charges:write","payouts:read","payouts:write"]`
  (nothing at submerchant itself, but union of viewer@platform + admin@connected reaches down to it)
- `part2(..., "bob", "submerchant")` -> `["charges:read","payouts:read"]` (bob has no assignment at
  connected or platform — only his own submerchant-level viewer role applies)

Add for Part 3:
```
roles += manager: [charges:read, charges:write]
assignments += carol @ platform -> manager
```
- `part3(..., "connected", "charges:read")` -> `["alice", "carol"]` — alice has it directly at
  connected (her own admin role there); carol has no assignment at connected or submerchant, but
  her platform-level manager role reaches connected by inheritance. bob is **not** in this answer:
  his only assignment is at submerchant, a *descendant* of connected, not an ancestor of it, so he
  is never a candidate for this particular `account_id`.
- `part3(..., "submerchant", "charges:read")` -> `["alice", "bob", "carol"]` — same permission,
  one level lower: now bob's own direct submerchant role counts too, and carol's platform-level
  role reaches two levels down instead of one.
- `part3(..., "submerchant", "payouts:write")` -> `["alice"]` (only admin grants it, and only
  alice's chain includes admin — bob's viewer and carol's manager both lack it)
- `part3(..., "submerchant", "invoices:void")` -> `[]` (no role in the system grants this
  permission at all — not an error, same as an unknown `user_id` in Part 1/2)

Add for Part 4 (same accounts/roles/assignments as just above):
- `part4(..., "viewer")` -> `["alice", "bob"]` — each is directly assigned `viewer` somewhere
  (alice at platform, bob at submerchant); the fact that alice *also* holds `admin` at a different
  account doesn't remove her from `viewer`'s list.
- `part4(..., "admin")` -> `["alice"]` (her connected assignment; nobody else is ever directly
  assigned `admin`, even though its permissions reach carol and bob nowhere — they hold different
  roles, not `admin` itself, so it's irrelevant here regardless)
- `part4(..., "manager")` -> `["carol"]`
- Add `roles += clone_of_manager: [charges:read, charges:write]` (identical permissions to
  `manager`, different `role_id`) and `assignments += dave @ platform -> clone_of_manager`:
  `part4(..., "manager")` is still just `["carol"]` — dave effectively has the exact same
  permissions as carol everywhere carol's reach, but he holds a *different* role, and Part 4
  answers "who holds this role", not "who has an equivalent permission set."

## Edge cases
- a user with no role anywhere in the chain: Part 1/2 return `[]` (never an error)
- `account_id` unknown to the system (not in `accounts`, referenced only by a query or by another
  account's `parent_id`) -> `ValueError`, from Part 2 onward, including Part 3's query `account_id`
- `role_id` unknown to the system -> `ValueError` when it appears in `assignments` (Part 2 onward)
  *and* when it is Part 4's query argument (same "declared catalog" reasoning as `account_id`)
- `user_id` unknown to the system (never appears in `assignments`) -> **not** an error, just no
  effective permissions anywhere; likewise a `permission` string no role ever grants (Part 3) is
  **not** an error, just `[]` — both are free-form values with no declared catalog, unlike
  `account_id`/`role_id`, which do have one and error when unknown. This asymmetry is deliberate
  and tested on both sides (declared-catalog id vs. free-form value) for both Part 3 and Part 4.
- a two-node cycle (`x`'s parent is `y`, `y`'s parent is `x`) and a one-node cycle (`x` is its own
  parent) both must raise `ValueError`, not recurse forever — still applies to Part 3, since it
  still walks `account_id`'s chain; Part 4 never walks a chain at all, so a cycle elsewhere in
  `accounts` that nothing queries is not an error for Part 4
- the same permission granted at two different levels in the chain is still listed once (Part 2's
  union, not concatenation); likewise Part 3 lists a matching user once even if more than one
  level of their own chain grants the queried permission
- Part 3: a user with an assignment on a **sibling** branch of the account tree (not an ancestor
  of the queried `account_id`) must never appear, even if their role grants the exact permission
  being queried — only their own chain up to `account_id` matters
- Part 4: a user holding the *same* `role_id` at two different accounts is listed once, not twice
- Part 4: two roles with byte-for-byte identical `permissions` lists are still different `role_id`s
  — a user assigned the "wrong" one of the two must never appear in the other's result (see the
  `clone_of_manager` worked example)
- Part 3 at scale: a system with many thousands of users scattered across unrelated branches of a
  deep tree, queried against one specific chain, must not cost proportional to the whole user
  population — only to that one chain's depth and the assignments actually on it (see REPORT.md)

## What this tests
skills: S03 record modeling (accounts/roles/assignments as small dicts, indexed by id — and here,
indexed a *second* way, by account and by role, once the query direction reverses) · S08
deterministic sorting (permission and user-id lists sorted, ties never left to insertion order) ·
S18 validation and error paths (unknown references, duplicate assignments, cycle detection, and
the deliberate declared-catalog-vs-free-form-value asymmetry, now exercised on both `account_id`
and `role_id` as the declared side) · S19 layered/incremental design (each part forces a genuine
representation change — Part 3/4 in particular force *reusing* Part 1/2's own helpers while
building a new, differently-keyed index on top of the same underlying data, rather than
re-deriving everything from scratch)

## Sources
- https://www.1point3acres.com/interview/problems/post/7100148（标题 "RBAC Role Resolver"，本次
  更新的镜像抓取日期 2026-09-04）——镜像页面这次给出了完整的**章节目录**（`Problem Definition` /
  `Phase 1: Direct Role Lookup` / `Phase 2: Adding Inheritance` / `Phase 3: Finding Users with
  Access` / `Phase 4: Filtering Users by Role` / `Solution Details` / `Full Code Solution` /
  `Optimization and Scaling`），本地留存于
  `catalog/raw/mirror_1p3a_stripe/coding/046__20260127__rbac_role_resolver__popular_7100148.txt`。
  **只有这些标题**——每个 Phase 标题下面的正文、字段名、规则文本、样例数据全部没有被抓到（镜像只
  保留了 `<h2>`/`<h3>` 级别的目录结构）。本题据此把 Part 3/4 的**主题**（反向查权限持有者 / 反向查
  角色持有者）改成与标题吻合，但**规则的具体定义、输入输出格式、以及全部 worked examples 的数值
  仍然是本仓库自拟**——不是从这份镜像转录的，镜像里根本没有这些内容可转录。
- https://prachub.com/coding-questions/resolve-user-roles-across-account-hierarchy（访问日期
  2026-09-03）——PracHub 自动生成的 Quick Overview 摘要："This question evaluates understanding of
  hierarchical data structures, role-based access control semantics, and set/map operations for
  computing effective permissions across account ancestors."正文因登录墙/异步加载多次重试均未获取
  到。发布信息：Software Engineer / Coding & Algorithms / Medium / **Technical Screen (Phone)** /
  2026-05-12。这份摘要没有提到反向查询，只覆盖 Part 1/2 的正向继承主题，与本题 Part 1/2 一致。
- https://www.interviewdb.io/question/stripe/user-roles（访问日期 2026-09-03）——页面 `<title>`
  确认"User Roles"这个标题独立存在，正文未加载（占位符）。
- `catalog/discovery/2026-09/C_batchA.md` `## C6` 一节（本仓库 2026-09-03 的二轮排查记录，含完整
  检索方法与失败检索式列表）。
- **本题面自拟的部分**：账户层级的具体字段名（`account_id`/`parent_id`）、角色权限的字符串格式、
  Part 3/4 各自的确切规则定义（尤其是 Part 4"拥有角色 = 直接持有，且可证明与算继承等价"这条推理）、
  4 个 part 内部的具体递进方式、输入输出的 stdin 协议、以及全部 worked examples 中的具体数值——
  两份原始来源（含这次更新后的 1point3acres 目录）都只给出了"账户层级 + 角色/权限解析"这个主题级
  描述和四个 Phase 的标题，没有任何一处规则文本、样例数据或函数签名，因此以上全部内容都是本仓库为
  覆盖 S03/S08/S18/S19 而设计，不是任何逐字转录。
