---
title: 'Peritext: A CRDT for Rich-Text Collaboration'
source: https://www.inkandswitch.com/peritext/
author: Preserving the authors’ intent
published: '2021-11-23'
site: inkandswitch.com
clipped: '2026-09-20'
---

# Peritext: A CRDT for Rich-Text Collaboration

In a real-time collaborative editor such as Google Docs, every keystroke typed into a document is immediately visible to the other collaborators. While this can be very convenient, such real-time (or *synchronous*) collaboration is not always what users want.

We interviewed eight people who regularly collaborate professionally on documents such as news articles, and several told us that they found real-time collaboration a stressful experience: they felt performative, self-conscious of others witnessing their messy work-in-progress, or irritated when a collaborator acted on suggestions before the editing pass was complete. When doing creative work, they preferred to have space to ideate and experiment in private, sharing their progress only when they are ready to do so.

With *asynchronous* collaboration, this is possible: a user may work in isolation on their own copy of a document for a while, without seeing other users’ real-time updates; sometime later, when they are ready to share their work, they can choose to merge it with their collaborators’ edits. Several such copies may exist side-by-side, and some might never be merged (e.g. if the user changed their mind about a set of edits).

Many software developers are familiar with asynchronous workflows in the form of Git branches and [pull](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) . However, the manual merge conflict resolution required by Git is not user-friendly, especially for a complex file format such as rich text (i.e. text with formatting).

The collaboration algorithm used by Google Docs ([Operational](https://drive.googleblog.com/2010/09/whats-different-about-new-google-docs.html) ) assumes that a document has a single, linear timeline of edits, which is managed by a cloud service. In order to support asynchronous collaboration with a Git-like branching and merging workflow, one key problem we need to solve is: how can we take any two versions of a document, which have been edited independently, and merge them in a way that preserves the intentions behind the different users’ edits as much as possible?

Peritext is a novel algorithm for merging versions of a rich-text document. It is a Conflict-free Replicated Data Type (

Peritext is not a complete system for asynchronous collaboration: for example, it does not yet visualize differences between document versions. Moreover, in this article we focus only on *inline formatting* such as bold, italic, font, text color, links, and comments, which can occur within a single paragraph of text. In a future article we will extend our algorithm to support *block elements* such as headings, bullet points, block quotes, and tables. Despite these limitations, Peritext is an important step towards asynchronous collaboration for rich text.

Besides explaining our algorithm and demonstrating our prototype implementation, this article also analyzes several examples of rich-text editor behavior in practice, which inform a model for preserving user intent in rich-text editing. To our knowledge there is no existing algorithm that is able to handle all of these examples correctly; existing CRDTs for plain text are difficult to adapt for rich text. As there is surprisingly little existing research on enabling collaboration in rich-text documents, we hope that this analysis will also be valuable for anybody who is interested in rich-text collaboration.

## [Preserving the authors’ intent](#preserving-the-authors-intent)

When writers are collaborating asynchronously, it is impossible for an algorithm to always merge edits perfectly. As one example, if two writers are editing the script for a TV show, changes to one episode may require plot changes in future episodes. Since an algorithm cannot do this automatically, human intervention is often necessary to produce the desired final result.

However, writing tools can still help enormously with the collaboration process. When two users have independently edited a document, manually merging those versions is tedious and error-prone. We want a writing system that helps authors perform these merges easily and consistently. Even if an automatic merge is imperfect, it allows authors to quickly get back in sync with each other, and minimize the time they have to spend struggling with their writing tools.

Before we can implement an algorithm to perform this automatic merge, we first need to define a clear model for user intent, and define the expected results when concurrent edits are merged. In this section we develop such a model through a series of examples.

### [Plaintext insertions](#plaintext-insertions)

**Example 1.** Let’s begin with a preliminary example: concurrent insertions on plain text. Imagine that Alice and Bob are editing a document concurrently, without knowledge of each others’ changes. Perhaps Alice is editing offline on the train, or Bob is trying out some changes in a private branch.

Before either user applies their changes, we start with the sentence:

The fox jumped.

Each user, unbeknownst to the other, inserts some text somewhere in the sentence:

Alice:

The quick fox jumped.

Bob:

The fox jumped over the dog.

Later on, the two users sync back up, and we need to merge both of their changes. Intuitively, the correct merge result is to keep both of their insertions in the same location, relative to the surrounding text at the time the text was inserted:

The quick fox jumped over the dog.

For example, Bob inserted “␣over the dog” after the word “jumped”, so it makes sense that the word ends up in that position in the merged sentence. Inserted characters should stay in the same place relative to the context in which they were inserted; text shouldn’t move around just because some words were added or removed elsewhere in the document. Existing algorithms for plain text collaboration already implement this behavior.

### [Concurrent formatting and insertion](#concurrent-formatting-and-insertion)

Now let’s consider some new intent preservation properties that emerge when formatting is involved. Starting with the same sentence as before:

The fox jumped.

**Example 2.** Alice bolds the text, while Bob inserts some new text:

Alice:

**The fox jumped.**

Bob:

The brown fox jumped.

What should the merge result be in this case? One answer might be:

**The** brown **fox jumped.**

This seems like an odd result. It’s true that Alice didn’t apply bold to the word “brown,” but that’s just because she didn’t know the word would be there when she applied the formatting. Similarly, Bob did not insert “brown” with bold formatting, but that’s only because he didn’t know Alice had bolded the surrounding area.

A different way to interpret the users’ intent would be to assume that Alice’s intent is to bold the whole sentence, and Bob’s intent is to add a word in the middle of the sentence. Both of these intents can be preserved by a different merge result:

**The brown fox jumped.**

The latter result seems more likely to be correct. This merge result suggests a general rule: when formatting is added to the document, it applies to any text inside a range between two characters, even if that text wasn’t present when the formatting was applied.

### [Overlapping formatting](#overlapping-formatting)

What should happen when both users apply formatting at the same time to overlapping regions?

**Example 3.** Let’s say Alice bolds the first two words while Bob bolds the last two words:

Alice:

**The fox** jumped.

Bob:

The **fox jumped.**

When we merge these two edits into a single document, we observe that the word “fox” was set to bold by both users. A given character is either bold or non-bold, so in this case there is only one reasonable outcome — the whole text should be bold:

**The fox jumped.**

**Example 4.** What should happen if Alice bolds some text while Bob makes an overlapping span italic?

Alice:

**The fox** jumped.

Bob:

The *fox jumped.*

It seems clear that “**The**” should be bolded, and “*jumped*” should be italicized. But what formatting should apply to “fox”, where both users changed the formatting?

One option would be to exclusively pick either the bold or italic formatting, eliminating the effects of one user’s actions. However, because bold and italic can coexist on the same word, we think it is most logical to apply both stylings to the word, making “fox” both bold and italic:

**The *fox*** *jumped.*

#### [Conflicting overlaps](#conflicting-overlaps)

So far, we have seen merge results that seem to faithfully preserve both users’ intent. However, not all kinds of formatting merge so cleanly.

**Example 5.** Consider assigning colored highlighting to some text. Alice applies red coloring to “The fox”, and Bob applies blue coloring to “fox jumped”:

Alice:

The fox jumped.

Bob:

The fox jumped.

What should happen when we merge these two edits? Unlike the previous examples, there is no way to preserve the intent of both users — the word “fox” must be either red or blue, it can’t be both. As a result, this is a *conflict* that may require some manual intervention to resolve.

One strategy might be to entirely eliminate one user’s edit because the two can’t coexist. For example, we could just apply Alice’s red highlighting and ignore Bob’s blue highlighting. However, to us this seems unreasonably restrictive. Only *part* of the two highlighted ranges overlapped; Bob’s coloring on the word “jumped” could have been preserved without issue. Another option might be to blend the two colors together on the word “fox”, but then we would be creating a new color that was used by neither Alice nor Bob, and that doesn’t seem right either.

In our opinion, the most reasonable behavior is: in the region where the two formatting ranges overlap, we arbitrarily choose either Alice’s color or Bob’s color.

The fox jumped.

The important thing is that the same color is chosen for everyone who views the document, so the choice needs to be deterministic. And if somebody subsequently changes the color again, then the latest color-change operation determines the final color.

It’s also worth noting that when faced with a conflict, we aren’t just limited to making an arbitrary automated choice. We could also [expose the conflicting value to the user](https://www.inkandswitch.com/pixelpusher/#but-what-about-conflict-resolution)  — for example, the editor could show an annotation noting that a conflict had occurred, asking a human to review the merged result. This approach of surfacing granular conflicts represents a middle ground between an automatic and manual merge process.

**Example 6.** Conflicts don’t only occur with colors; even simple bold formatting operations can produce conflicts. For example, Alice first makes the entire text bold, and then updates “fox jumped” to be non-bold, while Bob marks only the word “jumped” as bold:

Alice:

**The fox jumped.**

**The** fox jumped.

Bob:

The fox **jumped.**

The word “The” was set to bold by Alice and not changed by Bob, so it should be bold. The word “fox” was set to non-bold by Alice and not changed by Bob, so it should be non-bold. But the word “jumped” was set to non-bold by Alice, and to bold by Bob. In this case we have a conflict on the word “jumped”, because the word cannot be both bold and non-bold at the same time. We therefore have to choose arbitrarily between either:

**The** fox jumped.

or

**The** fox **jumped.**

Crucially, even though the choice is arbitrary, it must be consistent across both Alice and Bob’s devices, to ensure they continue seeing the same document state.

#### [Multiple instances of the same mark](#multiple-instances-of-the-same-mark)

**Example 7.** There is one more case to consider for handling overlapping marks of the same type. Consider the case where Alice and Bob both leave comments on overlapping parts of the text:

Alice:

Alice's commentThe fox jumped.

Bob:

The Bob's commentfox jumped.

This might seem somewhat similar to [Example 5](#example-5). The two users have assigned overlapping formatting, and unlike adding bold, we can’t just merge the two users’ marks into a single mark.

However, comments behave very differently from colored text — although a single character can’t be both red and blue, multiple comments *can* be associated with a single character in the text. We can render this in the editor by showing the two highlight regions overlapping:

Alice's commentThe Bob's commentfox jumped.

### [Text insertion at span boundaries](#text-insertion-at-span-boundaries)

Another case we need to consider is: when a user types new text somewhere in the document, what formatting should those new characters have? We argued in [Example 2](#example-2) that if text is inserted into the middle of a bold span, then that new text should also be bold. But it’s less clear what should happen when text is inserted at the boundary between differently formatted portions of text.

**Example 8.** Let’s say we start with a document where the span “fox jumped” is bold, and the rest is non-bold:

The **fox jumped**.

Now Alice inserts “quick␣” before the bold span, and “␣over the dog” before the final period. In all major rich-text editors we tested (Microsoft Word, Google Docs, Apple Pages), the result is:

The quick **fox jumped over the dog**.

That is, the text inserted before the bold span becomes non-bold, and the text inserted after the bold span becomes bold. The general rule here is that an inserted character inherits the bold/non-bold status of the preceding character. The same applies to most types of character formatting, including italic, underline, font, font size, and text color. However, if text is inserted at the start of a paragraph, where there is no preceding character in the same paragraph, then it inherits the formatting of the following character.

**Example 9.** There are some exceptions to the rule in [Example 8](#example-8): if we insert text at the start or end of a link, or the start or end of a comment, then the major rich-text editors place the new text outside of the link/comment span. For example, if “fox jumped” is a link:

The [fox](https://www.google.com/search?q=jumping+fox) .

jumped 

After Alice inserts text like in [Example 8](#example-8), the result is:

The quick [fox](https://www.google.com/search?q=jumping+fox)  over the dog.

jumped 

That is, while a bold or italic span grows to include text inserted at the end of the span, a link or comment span does not grow in the same way. Whether this behavior is desirable is perhaps up for debate, but we note that popular rich-text editors are remarkably consistent in this regard, suggesting that this behavior is a deliberate design choice.

We do not have an exhaustive set of correctness criteria for merging edits of a rich-text document, but we believe these examples can serve as a test suite characterizing desirable merging behaviors that preserve user intent.

## [Limitations of existing CRDTs](#limitations-of-existing-crdts)

[Conflict-free Replicated Data](https://crdt.tech/)  (CRDTs) are algorithms that allow each user to edit their local copy of a document, and which ensure that different users’ copies can be cleanly merged into a consistent result. For plain text documents there are plenty of CRDT algorithms, such as [Causal](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.994.4371&rep=rep1&type=pdf) , 

Before building a new CRDT for managing rich text, we might ask if we can simply use an existing one. It turns out that, while there are ideas from existing CRDTs that are very useful for modeling formatted text, applying existing algorithms in a naive way does not yield the desired behaviors listed above. In this section we briefly describe three approaches to representing rich text using existing CRDTs, and highlight their problems.

### [Markdown in a plain text CRDT](#markdown-in-a-plain-text-crdt)

The most straightforward way of representing rich text would be to encode it in a plain text format such as 

```
This is **bolded text**
```
This approach is convenient for some users who may already know the format (although many people who are not software developers find Markdown unfamiliar and hard to use). It also handles some intent preservation scenarios well, including the concurrent formatting and insertion scenario.

However, it doesn’t handle concurrent formatting well. Take [Example 3](#example-3) above, where Alice marks “The fox” as bold, and Bob concurrently makes “fox jumped” bold. (We show each user’s asterisks in a different color to clarify the merge result later on.)

Alice:

**The fox** jumped.

`**The fox** jumped.`
Bob:

The **fox jumped.**

`The **fox jumped.**`
The correct merge result here is for the entire sentence to become bolded. However, when we merge the plain text insertions, we arrive at the following Markdown sequence, which interleaves the two users’ control characters:

`**The **fox** jumped.**`
This sequence renders as:

**The** fox **jumped**

The users’ intent hasn’t been preserved — both users bolded the word “fox”, but in the merged result it has ended up non-bold. Bob’s first insertion before “fox” was intended to mean “start bolding here”, but in the merged result it was interpreted as ending the bolded sequence started earlier in the sentence by Alice.

This is just one example of a more general problem, due to the fact that the language was not designed to preserve intent under concurrent edits. As another example, if two people created a top-level heading by inserting `#` at the beginning of a line, that would become `##` denoting a second level heading.

### [Adding control characters to plain text](#adding-control-characters-to-plain-text)

To get around these limitations of Markdown, another approach might be to use HTML, or to insert special hidden control characters into the plain text sequence to denote the beginning and end of formatting spans. These characters wouldn’t be directly visible to the user; rather they would simply serve as an underlying storage format backing a WYSIWYG editor UI. For example, one option would be to store separate characters for “start bold” and “end bold”, rather than using a single character sequence for “toggle bold” as in Markdown. This is the approach used by the CRDT library 

While this approach seems promising at first, it has subtle problems. Once again consider [Example 3](#example-3), but this time with start/end control characters, represented as `<bold>` and `</bold>`.

Alice:

**The fox** jumped.

```
<bold>The fox</bold> jumped.
```
Bob:

The **fox jumped.**

```
The <bold>fox jumped.</bold>
```
After merging we get:

```
<bold>The <bold>fox</bold> jumped.</bold>
```
We could render this document by iterating left to right through the text, remembering the current combined formatting at every given point. For example, when we encounter a `<bold>` character, we make the following text bold, and when we encounter a `</bold>` character, we make the following text non-bold.

This strategy seems reasonable at first, but it does not achieve the desired outcome for [Example 3](#example-3). When we reach the end of the word “fox”, we know there is a bold range active, but the `</bold>` character after “fox” ends that bolded range. As a result, “jumped” is not bold even though it should have been:

**The fox** jumped.

The reason for this anomaly is that our accumulated state did not contain enough information to accurately reflect the effects of overlapping spans. We tried several variations of the algorithm, such as counting the number of span beginnings and span ends we have seen, or linking each span-end character with its associated span-beginning, but found them difficult to reason about and prone to strange edge cases.

In particular, with control characters it is difficult to represent changes of formatting over time. Consider partially overlapping spans of text that are toggled between bold and non-bold several times, or partially overlapping spans whose text color is changed several times. Control characters tell us where a span begins or ends, but they do not tell us which formatting is older and which is newer. When several users concurrently modify control characters, it is difficult to determine whether the merged result reflects the users’ intentions.

It might be possible to make the control character approach work reliably and to handle all of these edge cases correctly, at the cost of significant complexity. We believe the approach we have taken with Peritext is simpler, and easier to verify that it behaves as expected in all of the examples. Moreover, Peritext also makes it easier to determine how a document changed from one version to another, which is important for asynchronous collaboration workflows.

### [Format spans in a JSON document](#format-spans-in-a-json-document)

Another approach would be to use a tree-structured representation of formatted text, akin to HTML, XML, and the Document Object Model (DOM). For example, **fox** jumped.” with this JSON document:

```
[
	{ text: "The ", format: [] },
	{ text: "fox", format: ["bold"] },
	{ text: " jumped.", format: [] }
]
```
Unfortunately, when we use the Automerge semantics for merging JSON documents, this representation does a poor job at preserving user intent. To see why, imagine we start with a single unformatted span:

```
[{ text: "The fox jumped.", format: []}]
```
Now, imagine two users both make changes to this text without communicating updates to one another. Alice bolds the word “jumped” to get “The fox **jumped.**” This requires splitting up the single span; in JSON terms, we could model this as deleting “jumped” from the first span, and then adding a new span for the newly bolded word:

```
spans[0].text.delete(8, 7) // delete "jumped." from first span
spans.push({ text: "jumped.", format: ["bold"] }) // add new span
```
Meanwhile, Bob also formats the word “jumped”, applying italics to get “The fox *jumped.*” We similarly model this with two actions: modifying the first span and inserting a new second span.

```
spans[0].text.delete(8, 7) // delete "jumped." from first span
spans.push({ text: "jumped.", format: ["italic"] }) // add new span
```
So far, User A and User B both see a reasonable result locally. But what happens when we merge their changes? In Automerge’s algorithm, when two users insert into a list at the same position, both users’ insertions are preserved and it’s not considered a conflict, so we converge to this result:

```
[
	{ text: "The fox ", format: [] },
	{ text: "jumped.", format: ["bold"] },
	{ text: "jumped.", format: ["italic"] }
]
```
This data structure renders as “The fox **jumped.***jumped.*”, rather than the expected result “The fox ***jumped.***”. The last word has become duplicated!

The problem here is that users intended to only change the formatting, but their actions were represented in the JSON document in a way that suggested they were also modifying the text content. While one could design other JSON representations of a document which would have different merge characteristics than this, we have not found one that is suitable.

## [Peritext: A rich-text CRDT](#peritext-a-rich-text-crdt)

We now introduce the approach we have taken for rich-text collaboration in Peritext. We describe our algorithm in four parts:

- Representing the textual content of a rich-text document using an existing plain text CRDT
- Generating CRDT operations representing formatting changes
- Applying these operations to produce an internal document state
- Deriving a document suitable for a text editor, based on the internal state

Our approach in designing the algorithm was to capture the user input, and hence the user intent, as closely as possible:

- `insert` operations are generated when the user types or pastes new characters somewhere in the text;
- `remove` operations are generated when the user hits the backspace or delete key somewhere in the text, or overwrites selected text;
- an `addMark` or`removeMark` operation is generated when the user selects some text and chooses a formatting option from the menu or by keyboard shortcut.

### [The underlying plain text CRDT](#the-underlying-plain-text-crdt)

Every operation that modifies the state of the document is given a unique, immutable identifier called `opId` (operation ID). An opId is a string of the form `counter@nodeId` where `counter` is an integer and `nodeId` is a unique ID (e.g. UUID) of the client that generated the operation. Whenever we make a new operation, we give it a `counter` that is one greater than the greatest counter value of any existing operation in the document, from any client. Since a given client never uses the same `counter` value twice, the combination of `counter` and `nodeId` is globally unique.

We also define an ordering of opIds as follows: `counter1@node1 < counter2@node2` if `counter1 < counter2` (using a numeric comparison); if `counter1 == counter2` we break ties using a string comparison of `node1` and `node2`.

#### [Inserting and deleting plain text](#inserting-and-deleting-plain-text)

The key idea of most text CRDTs is to represent the text as a sequence of characters, and to give each character a unique identifier. In our case, the ID of a character is the opId of the operation that inserted that character. To insert a character into a document, we generate an insert operation of the following form:

```
{
  action: "insert",
  opId: "2@alice",
  afterId: "1@alice",
  character: "x"
}
```
This insert operation has an opId of `2@alice`, and its effect is to insert the character “x” after the existing character whose ID is `1@alice`. To determine the position where a character is inserted, we always reference the ID of the existing character after which we want to insert. We do not use an index to identify the insertion position because an index would change every time text is inserted or deleted earlier in the document, whereas an opId remains stable.

To insert at the beginning of the document we use `afterId: null`. If two users concurrently insert at the same position (i.e. with the same `afterId`), we order the insertions by their `opId` to ensure both users converge towards the same sequence of characters.

To delete a character from a document, we generate a `remove` operation of the following form:

```
{
  action: "remove",
  opId: "5@alice",
  removedId: "2@alice"
}
```
This operation has an opId of `5@alice`, and its effect is to remove the existing character whose ID is `2@alice` (i.e. the “x” we inserted above). As before, it is easier to identify the deleted character by its ID than by its index. When we process a remove operation, we don’t actually delete it from the document entirely, but we just mark it as deleted. That way, if another insert operation references the deleted character’s ID in its `afterId`, we still know where to put the inserted character.

The state of the plain text document then consists of three things for each character: the opId of the operation that inserted it, the actual character, and a flag to tell us whether it has been deleted.

In the diagram, Alice (nodeId `A`) first typed the text “the fox”, generating opIds `1@A` to `7@A`. Then Bob (nodeId `B`) deleted the initial lowercase “t” (the deletion has opId `8@B`) and replaced it with an uppercase “T” (opId `9@B`), and finally Bob typed the remaining text “␣jumped.” (opIds `10@B` to `17@B`). The final text therefore reads “The fox jumped.” but the lowercase “t” is still in the sequence, marked as deleted.

That’s all we need to implement collaborative editing of plain text: inserting a single character, and removing a single character. Larger operations, such as cutting or pasting an entire paragraph, turn into lots of single-character operations. This can all be [optimized to be more efficient](#performance-and-efficiency), but for now, single-character insertions and deletions are sufficient.

### [Generating inline formatting operations](#generating-inline-formatting-operations)

The next step is to allow the formatting of the text to be changed. Every time the user modifies the formatting of the document, we generate either an `addMark` or a `removeMark` operation. For example, if Alice selects the text “fox jumped” and hits ⌘+B or Ctrl+B to make it bold, the generated operation might look like this:

```
{
  action: "addMark",
  opId: "18@A",
  start: { type: "before", opId: "5@A" },
  end:   { type: "before", opId: "17@B" },
  markType: "bold"
}
```
This operation has an opId of `18@A`. It takes the span of text starting with the character whose ID is `5@A` (i.e. the “f” of “fox”), and ending with the character whose ID is `17@B` (the final period). All characters in this span (including the start character, but excluding the end character) become bold. As with earlier operations, we use opIds, not indexes, as stable identifiers of the `start` and `end` of the span.

We can imagine each character in the text as having two anchor points where the start or end of a formatting operation may attach — either before or after the character:

A formatting change always occurs in the “gap” between two characters. The `type: "before"` properties in the example operation indicate that the bold span starts in the gap immediately before the “f” (i.e. the “f” is bold, but the preceding space is not), and the bold span ends in the gap immediately before the “.” (i.e. the “d” of “jumped” is bold, but the period is not). We could also choose `type: "after"` if we wanted a span to start or end on the gap immediately after a particular character. Moreover, the `start` property could be `"startOfText"` if we want the span to always start right at the beginning of the document, and the `end` property could be `"endOfText"` if we want it to end after the last character.

If another user inserts text within that span, like in [Example 2](#example-2) above, those new characters still fall within the range defined by the `addMark` operation, and so they are also formatted bold. And when text is inserted at the boundaries of the bold span, it behaves like in [Example 8](#example-8): text inserted before the “f” is non-bold, whereas text inserted between the “d” and the period is bold, because it still falls within the span before the period.

For marks that should not grow when text is inserted at the boundary, like the link in [Example 9](#example-9), we let the mark end in the gap after the the last character of the mark:

```
{
  action: "addMark",
  opId: "19@A",
  start: { type: "before", opId: "5@A" },
  end:   { type: "after",  opId: "16@B" },
  markType: "link",
  url: "https://www.google.com/search?q=jumping+fox"
}
```
With this operation, the “d” of “jumped” is still part of the link, but any text that is inserted after that character will not be part of the link. Note also that an operation with `markType: "link"` has an additional `url` attribute. To change the URL that a link points to, we simply generate another `addMark` operation with a new URL and the same `start` and `end`.

If the user changes their mind and decides they don’t want the text to be bold/linked after all, we don’t remove the `addMark` operation. In fact, we never remove an operation, we only ever generate new operations (we discuss [later](#performance-and-efficiency) why it’s fine to store operations forever). Instead, we generate a `removeMark` operation that undoes the effect of the earlier `addMark` and sets a sequence of characters back to be non-bold. For example, the following operation makes “␣jumped” non-bold:

```
{
  action: "removeMark",
  opId: "20@A",
  start: { type: "before", opId: "10@A" },
  end:   { type: "before", opId: "17@B" },
  markType: "bold"
}
```
To remove a prior mark entirely, the `start` and `end` of the `removeMark` operation should be the same as for the `addMark` that should be overwritten. In general, a `removeMark` can start and end on any character, regardless of its current formatting, and the effect is to set that span to be non-bold/non-linked/non-italic/etc.

#### [Inserting text at span boundaries](#inserting-text-at-span-boundaries)

A transition from bold to not-bold could happen not only because of the end of an `addMark`, but also because of the start of a `removeMark` (and vice versa for transition from not-bold to bold). To maintain the rule that an inserted character is formatted the same as the preceding character, `removeMark` operations use `type: "before"` on both `start` and `end` for bold and similar types of marks. For example, if we apply the `removeMark` operation above and then insert “␣suddenly” immediately after the “x”, it will be bold, because it falls within the `addMark` span but not within the `removeMark` span.

Inserting a character at the start of a paragraph requires a special case: we have to first insert the character, and then (if necessary) generate additional formatting operations so that the inserted character is given the same formatting as its successor.

For marks that should not grow at the end, such as links, `addMark` uses `type: "before"` for `start` and `type: "after"` for `end`. For `removeMark` it’s the other way round: these operations use `type: "after"` for `start` and `type: "before"` for `end`. This ensures that when text is inserted at the end of a link, that text is not part of the link, regardless of whether the link is ending because it’s the end of the `addMark` that created it, or the beginning of a `removeMark` that removed the link property from the subsequent characters.

One more detail is required to ensure that insertions at the end of a link behave correctly: it could happen that the character to which the link end is anchored is deleted (a tombstone). In the following example, “fox jumped” was linked, and then the word “jumped” was deleted.

Now assume the user wants to replace “jumped” with “frolicked”, so they insert that word after the space `10@B`. This position is at the end of the link (the next visible character, the period, is not part of the link), so we expect the new character to be non-linked because links don’t grow. However, when there are tombstones at the position where a new character is inserted, our plain text CRDT by default places the inserted character before the tombstones. This would place “frolicked” before “jumped”, making it part of the link, which is undesirable.

To fix this issue, if we need to insert a character at a position where there are tombstones, we scan the list of tombstones at this position. If there are any tombstones whose “after” anchor is the start or end of any formatting operation, we insert the character after the last such tombstone. Otherwise we insert before the tombstones, as usual. In the example above, the after-anchor of character “d” (`16@B`) is the end of `addMark` operation `19@A`, and so we place the new word after that character. This ensures that insertions at the end of a link are placed outside of the link.

If the list of tombstones contains anchors for the start or end of several formatting operations, it’s possible that no ideal insertion position exists. In this situation, the inserted text can be placed arbitrarily relative to the tombstones, and the worst-case outcome is that the text is formatted differently from what was desired. We believe that this situation is rare enough that it is acceptable for the user to manually fix the formatting in this case.

### [Applying operations](#applying-operations)

We now show how our algorithm applies `insert`, `remove`, `addMark` and `removeMark` operations to update a rich-text document state.  In a CRDT, we must ensure that when two operations were generated concurrently, we can apply those operations in any order, and the resulting document must always be the same. This is what allows us to merge two documents edited by different users: we can take all operations that have been applied to one document but not the other, and apply them to the other document in order to obtain the merged document.

In the diagrams above, we visualized each character as having two associated anchor points for formatting operations, one before and one after the character. Our implementation closely follows this idea. For each character, the internal data structure stores the opId, whether it has been deleted, and the set of operations anchored to the gaps before and after the character (which we sometimes refer to as *op-sets*).

```
type CharacterMetadata = {
    /** One character of the text */
    char: string
    /** opId of operation that created the list item. */
    opId: OperationId
    /** Has the list item been deleted? */
    deleted: boolean
    /** Mark operations in the gap before this list item */
    markOpsBefore?: Set<AddMarkOperation | RemoveMarkOperation>
    /** Mark operations in the gap after this list item */
    markOpsAfter?: Set<AddMarkOperation | RemoveMarkOperation>
}
type TextMetadata = Array<CharacterMetadata>
```
In a text without formatting operations, the `markOpsBefore` and `markOpsAfter` properties are absent (`undefined`). Inserting and deleting characters in the sequence uses the normal RGA plain text CRDT logic described previously.

When applying an `addMark` or `removeMark` operation, we update either the `markOpsBefore` or the `markOpsAfter` property (depending on whether the operation specifies `type: "before"` or `type: "after"`) on both the `start` and the `end` character of the operation.

First, we update the start character for the operation. If there is an existing set of formatting operations on the start character, we add the new formatting operation to that set. If no such set exists, we create a new set containing one element: the new formatting operation. This indicates that the new formatting operation applies to the characters from this position onward.

Next, we update the end character. If there is an existing set of formatting operations, we don’t modify it; if there is no set of formatting operations, we create an empty set at that position. This indicates that the new formatting operation no longer applies to the characters from this position onward.

We never remove operations from these sets, and so each of these sets contains all the `addMark` or `removeMark` operations in the history of the document that started at a particular position. We show in the next section how to compute the current formatting for the text based on these sets of operations.

Continuing with the example, let’s say the current text is “The fox jumped.” with no formatting, and Alice wants to bold the first two words. She generates an `addMark` operation that starts before the “T” (`9@B`) and ends before the space following “x” (`10@B`):

```
{
  action: "addMark",
  opId: "19@A",
  start: { type: "before", opId: "9@B" },
  end:   { type: "before", opId: "10@B" },
  markType: "bold"
}
```
Alice applies the operation to her own document data structure. She does this by setting `markOpsBefore` on the first character (`9@B`) to be a set containing that `addMark` operation, and setting `markOpsBefore` on the second space character (`10@B`) to be the empty set:

```
[
  { char: "T", opId: "9@B", deleted: false, markOpsBefore: [
    {
      action: "addMark",
      opId: "19@A",
      start: { type: "before", opId: "9@B" },
      end:   { type: "before", opId: "10@B" },
      markType: "bold"
    }
  ] },
  { char: "t", opId: "1@A", deleted: true },
  { char: "h", opId: "2@A", deleted: false },
  { char: "e", opId: "3@A", deleted: false },
  { char: " ", opId: "4@A", deleted: false },
  { char: "f", opId: "5@A", deleted: false },
  { char: "o", opId: "6@A", deleted: false },
  { char: "x", opId: "7@A", deleted: false },
  { char: " ", opId: "10@B", deleted: false, markOpsBefore: [] },
  …
]
```
#### [Handling overlapping formatting spans](#handling-overlapping-formatting-spans)

Let’s say Bob concurrently wants to italicize the last two words and the period, as in [Example 4](#example-4) above. He generates an `addMark` operation for this span, which starts before the “f” and runs until the end of the text (i.e. after the last character):

```
{
  action: "addMark",
  opId: "19@B",
  start: { type: "before", opId: "5@A" },
  end: { type: "endOfText" },
  markType: "italic"
}
```
When Alice receives Bob’s operation, and when Bob receives Alice’s operation, we have to determine all the formatting operations that apply to a given character, and we need to deal with the fact that their spans partially overlap. One way of doing this would be to scan from the beginning of the document, keeping track of all operations whose span has started and not yet ended. However, for performance reasons we want to avoid scanning the entire document on every keystroke.

As an optimization, we say that the sets of operations `markOpsBefore` and `markOpsAfter` contain not only the operations that start at that particular position, but also the operations whose span contains that position. It is still the case that the `markOpsBefore` and `markOpsAfter` properties are absent whenever the formatting is not changing. But if we have a formatted span whose start or end falls within another operation’s span, we repeat the containing operation.

We illustrate this algorithm in the following figures, by considering the case of Alice, who has already applied her own bold operation, and is now applying Bob’s italic operation.

To apply an `addMark` or `removeMark` operation, we first find the markOps set where the start of the operation is anchored (either `markOpsBefore` or `markOpsAfter` on the character with ID `operation.start.opId`, depending on `operation.start.type`). If that set is already present, we add the new operation to it. If that set is absent, we search backwards in the character metadata sequence until we find the nearest markOps set that is present; we copy that set and add the new operation to it. In the example, `markOpsBefore` on the “f” character is absent, so we copy `markOpsBefore` from the “T” character and add the italic operation to it.

Next, we iterate forwards over the character sequence from the new operation’s start. Whenever we encounter a `markOpsBefore` or `markOpsAfter` property that is present, we add the new operation to it, in order to indicate that this position falls within the span of the new operation. In the example, this happens at `markOpsBefore` on the second space character: this was previously the empty set, and we add the italic operation to it.

This iteration finishes when we reach the markOps set at which the end position of the new operation is anchored. If this set is absent, we initialize it to be a copy of the closest preceding markOps set, except that we do not add the new operation to this set. In the example, the italic operation ends at `endOfText`, and we initialize it to be the empty set.

The result is that whenever a `markOpsBefore` or `markOpsAfter` property is present, it contains all of the formatting operations that pertain to the following run of characters, until we reach the next `markOpsBefore` or `markOpsAfter` property that is present. In the example, it is clear that “fox” falls both within the bold and within the italic span.

This algorithm is commutative: no matter in which order the formatting operations are applied, we end up in the same final state (the same sets of operations in `markOpsBefore` and `markOpsAfter` on each character). Moreover, it is efficient: we only need to scan over the part of the document that is affected by the formatting operation, not the whole document.

When the first formatting operation is added to a document, the initial backwards scan that looks for the closest preceding markOps set will have to go all the way to the beginning of the document, which might be slow on a large document. To speed this up, we can use the following trick: when inserting characters, on some characters (say one in a thousand, chosen randomly) we initialize their `markOpsBefore` to be a copy of the closest preceding markOps set (or an empty set if there is none). This has no effect on the correctness of the algorithm, but it ensures that when searching for the closest preceding markOps set, we will find one that is present after scanning backwards for only about 1,000 characters (on average). This avoids having to scan the entire document.

### [Producing a final document](#producing-a-final-document)

So far, the algorithm in the previous section has subdivided the document into a sequence of spans, with a set of mark operations that is active for each span. Next, we need to turn this into a document state that can be displayed by a text-editing UI; in particular, we need to derive the current formatting state for each span of characters.

Our goal is to produce a data structure that contains only the current text of the document (no deleted text), annotated with its current formatting. This is in line with how rich-text editing user interface components, such as 

```
[
  { text: "The ",     format: { bold: true } },
  { text: "fox",      format: { bold: true, italic: true } },
  { text: " jumped.", format: { italic: true } }
]
```
To produce this data structure, we can iterate over the list of characters, converting each set of mark operations into a current formatting state for the corresponding span.

Every `addMark` or `removeMark` operation has a `markType` property indicating which aspect of the formatting is being modified: boldness, italicization, text color, presence of a comment, or various other properties. We assume that each operation affects only the aspect indicated by its `markType`, and leaves all other formatting marks unchanged. This means we can consider the operations for each `markType` separately. In the example from the previous section, we can easily see that the word “fox” should be both bold and italic, because the bold and italic operations overlap with that word:

However, in other cases, the conversion process might be more complicated. There may be multiple operations with the same `markType` for the same span: for example, some text may be bolded and unbolded again several times. With most mark types, the values indicated by different operations are mutually exclusive: a character must be either bold or non-bold; a character cannot have more than one text color. For these mark types, we use a simple last-write-wins conflict resolution policy, as discussed previously in [Example 5](#example-5), based on the opIds of the formatting operations. For example, imagine a span to which the following two operations apply:

```
{
  action: "addMark",
  opId: "19@A",
  start: { type: "before", opId: "9@B" },
  end:   { type: "before", opId: "10@B" },
  markType: "bold"
}
{
  action: "removeMark",
  opId: "23@B",
  start: { type: "before", opId: "9@B" },
  end:   { type: "before", opId: "10@B" },
  markType: "bold"
}
```
Because the mark operations are in an unordered set, we need to ensure that the span always ends up with the same formatting — either bold or non-bold — regardless of the order in which those two operations are processed. We do this by comparing the opIds of the operations using the ordering defined earlier: if the opIds are `counter1@node1`  and `counter2@node2` , the winning operation is the one with the greater counter, or the one with the greater node ID if the counters are the same. In this example, the `removeMark` operation takes precedence because `23@B > 19@A`, and therefore this span is non-bold. The same principle applies to marks that have additional attributes, such as text color: the winning color is the one indicated by the operation with the greatest opId.

Recall that whenever we make a new operation, we give it an opId with a `counter` that is one greater than the greatest counter value of any existing operation in the document. This ensures that if the user changes their mind about formatting several times — for example, if they toggle the same word between bold and non-bold several times — then the final formatting operation will have the greatest counter and therefore take precedence over all the earlier operations.

In fact, for the purposes of determining the current formatting of a document, it’s not strictly necessary to store the sets of all historical formatting operations, but it would be sufficient to store the latest value for each mark type and each span, along with the opId that set that value. However, storing the set of formatting operations is useful if we want to compute what a document looked like sometime in the past, for the purpose of visualizing the differences between versions of a document. Although the current version of Peritext does not support this feature, we believe it is important for asynchronous collaboration, and we plan to add it in the future.

As further optimizations, we can avoid computing the current formatting for any spans that only contain deleted characters (tombstones), since they do not show up in a WYSIWYG editor, and we can concatenate any adjacent spans whose current formatting is identical.

#### [Incremental patches](#incremental-patches)

The section above describes a way of iterating over an internal document state and producing a representation that is suitable for display in a text editor. This is a reasonable approach when a document is first loaded in an editor, but it is not very suitable for handling character-by-character editing. Iterating through the whole document on every keystroke can become slow in large documents, so we would prefer to have a process that can reason more locally about the effects of an operation. Moreover, a text editor is typically implemented as a stateful object; each edit needs to describe what *changed* in the document, not just produce a new document state.

When we apply an operation in Peritext, in addition to updating the internal document state, we also compute a *patch*, which describes how this operation affects the document state in the text editor. Different editor libraries have slightly different patch formats, but the editors we considered have sufficiently similar patch formats that our approach applies to all of them.

To process an `insert` operation, we first use the existing RGA algorithm to determine the insertion position for the new character, and compute its index. To compute the index of the character, we can count the number of non-deleted characters that precede the insertion position. (There are [data](https://pages.lip6.fr/Marc.Shapiro/papers/rgasplit-group2016-11.pdf)  that can perform this index computation efficiently, without having to scan the whole document, but they go beyond the scope of this article.)

In addition, we need to determine what formatting to apply to the inserted character. We do this by searching backwards in the array of characters, starting from the insertion position, until we find a markOps set that is present. From this set of operations we then compute the marks for the inserted character using the usual last-write-wins logic, and then we construct a patch that inserts a character with that formatting at the index we computed.

For example, a patch to insert the letter “x” at index 6 with bold formatting might look like this:

```
{
  type: "insert",
  char: "x",
  index: 6,
  format: { bold: true }
}
```
A `remove` operation is the simplest to process: we find the character with the appropriate opId; if it is already deleted, we do nothing; if it is not yet deleted, we mark it as deleted and compute the index of the deleted character. We then construct a patch that asks the editor to delete the character at that index.

When processing an `addMark` or `removeMark` operation, we don’t need to change any text in the editor, but we may need to update the formatting of several spans of text. For example, say the current state of the document is “The **fox** jumped.” (where “fox” is bold), and we receive an operation that formats the entire text as italic.

We add the `addMark` or `removeMark` operation to the markOps sets as described above, and for each span that the operation applies to, we calculate the updated marks using the last-write-wins rule. For each span where the new formatting differs from the previous formatting for that span, we construct a patch that instructs the text editor to change the formatting accordingly. In this case, we produce three patches, corresponding to each individual span in the text: to mark “The” as italic, to mark “fox” as bold and italic, and to mark “jumped.” as italic:

```
[
  {
    type: "addMark", format: { italic: true },
    startIndex: 0, endIndex: 3
  },
  {
    type: "addMark", format: { bold: true, italic: true },
    startIndex: 3, endIndex: 7
  },
  {
    type: "addMark", format: { italic: true },
    startIndex: 7, endIndex: 14
  }
]
```
With this approach, the patches we send to the text editor are the minimum required in order to make the text editor state consistent with the CRDT state.

### [Prototype implementation](#prototype-implementation)

We have implemented a working prototype of the Peritext CRDT, which is shown running at the top of this essay. It is implemented in TypeScript, and the code is [open](https://github.com/inkandswitch/peritext) . Our code is a self-contained implementation that extends a simplified version of the 

For the editor UI, we chose to build on 

Currently, our implementation is somewhat specialized to the small set of marks shown in this article: bold, italic, links, and comments. However, we intend these to be a representative set of formatting marks, and expect that their behavior would extend to other kinds of user-configurable marks as well.

### [Performance and efficiency](#performance-and-efficiency)

Our algorithm is designed with performance in mind: in particular, updates only operate locally on the text they touch, and do not require scanning or recomputing the entire document. However, we have prioritized simplicity over performance in some areas: we store each character as a separate object (which uses a lot of memory); we remember all tombstones and the history of all formatting operations; and the process of finding the character with a particular opId, and computing its index, is not optimized.

These areas in which we have prioritized simplicity are not fundamental to the algorithm, and can be addressed with some implementation effort. For example, [compressed](https://hal.inria.fr/hal-00903813/document)  of the character sequence, in which characters with consecutive opIds are represented as a simple string rather than an object per character. They also feature data structures that make it efficient to convert an opId into a character index and vice versa, which is needed for integration with editors such as ProseMirror.

Storing all of the operations forever is not as expensive as you might think: Automerge’s compression algorithm can store every single keystroke in the editing history of a text document at a cost of about one byte per operation. All of these optimizations can be applied directly to Peritext, which gives us confidence that with some further engineering effort, Peritext can be very fast and efficient.

## [Conclusion](#conclusion)

We believe that CRDTs for rich text could enable new writing workflows, with powerful version control and support for both synchronous and asynchronous collaboration. In this work, we have shown that traditional plain-text CRDTs are not capable of preserving authors’ intent when merging edits to rich-text documents. We have developed a rich-text CRDT that supports overlapping inline formatting, and shown how to implement it efficiently.

Peritext is only the first step towards a system for asynchronous collaboration: it simply allows two versions of a rich-text document to be merged automatically. To realize asynchronous collaboration will require further work on visualizing editing history and changes, highlighting conflicts for manual resolution, and other features. Since Peritext works by capturing a document’s edit history as a log of operations, it provides a good basis for implementing those further features in the future.

There are many types of marks found in text that can be modeled as spans, and their semantics vary. Some marks can coexist, and others cannot. Further, user expectations about how marks behave can vary by type. We believe Peritext can capture these intents, but careful editor integration is vital to delivering on user expectations.

Inline formatting is sufficient for short blocks of text like a Trello card description, but longer documents often rely on more sophisticated block elements or hierarchical formats, such as nested bullet points, which Peritext does not currently model. Further work is required to ensure edits to block structures like bulleted lists can be merged while preserving author intent. Hierarchical formatting constructs raise new questions around intent preservation — for example, what should happen when users concurrently split, join, and move block elements?

Another area for future exploration is moving and duplicating text within a document. If two people concurrently cut-paste the same text to different places in a document, and then further modify the pasted text, what is the most sensible outcome?

The writers we spoke with love the convenience of live collaborative writing tools, but also described a wide variety of workarounds for asynchronous editing. For example, one interviewee worked from personal copies of documents to preserve their privacy during an edit. Others, lacking version control tools, relied on manually bolded text to identify changes made by an editor. These workarounds stem from an underlying technical paucity caused by a lack of systematic change tracking. We hope that Peritext and other CRDTs for rich text will enable new workflows for these users, which are not possible to build on top of existing data structures for storing text documents. Users could try out their own divergent long-running branches and easily merge them back together with powerful comparison views. People could choose to work in private, or to block out distracting changes being made by others. Rather than seeing document history as a linear sequence of versions, we could see it as a multitude of projected views on top of a database of granular changes.

*Thanks to Notion for sponsoring Slim Lim’s contributions to this project; to Blaine Cook and Tim Evans at Conde Nast for their input throughout the project; to Marijn Haverbeke for ProseMirror and for other guidance; to Kevin Jahns and Seph Gentle for valuable feedback on our algorithm; to Sam Broner, Daniel Jackson, Rae McKelvey, Ivy Reese, and Adam Wiggins for feedback on the essay, and to the many editors, journalists, and writers who showed us how they work and shared their insight and experience with us.*

We welcome your feedback: [hello@inkandswitch.com](mailto:hello@inkandswitch.com).
