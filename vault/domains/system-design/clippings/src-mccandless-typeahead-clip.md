---
title: Using Finite State Transducers in Lucene
source: https://blog.mikemccandless.com/2010/12/using-finite-state-transducers-in.html
author: Michael McCandless
published: '2010-12-03'
site: blog.mikemccandless.com
clipped: '2026-09-20'
---

# Using Finite State Transducers in Lucene

[FSTs](http://en.wikipedia.org/wiki/Finite_state_transducer)are finite-state machines that map a term (byte sequence) to an arbitrary output. They also look cool:

That FST maps the sorted words

*mop*,

*moth*,

*pop*,

*star*,

*stop*and

*top*to their ordinal number (0, 1, 2, ...). As you traverse the arcs, you sum up the outputs, so

*stop*hits 3 on the

**s**and 1 on the

**o**, so its output ordinal is 4. The outputs can be arbitrary numbers or byte sequences, or combinations, etc. -- it's pluggable.

Essentially, an FST is a SortedMap<ByteSequence,SomeOutput>, if the arcs are in sorted order. With the right representation, it requires far less RAM than other SortedMap implementations, but has a higher CPU cost during lookup. The low memory footprint is vital for Lucene since an index can easily have many millions (sometimes, billions!) of unique terms.

There's a

[great deal of theory](http://www.cs.nyu.edu/~mohri/pub/fla.pdf)behind FSTs. They generally support the same operations as

[FSMs](http://en.wikipedia.org/wiki/Finite-state_machine)(determinize, minimize, union, intersect, etc.). You can also compose them, where the outputs of one FST are intersected with the inputs of the next, resulting in a new FST.

There are some nice general-purpose FST toolkits (

[OpenFst](http://www.openfst.org/)looks great) that support all these operations, but for Lucene I decided to implement

[this neat algorithm](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698)which incrementally builds up the minimal unweighted FST from pre-sorted inputs. This is a perfect fit for Lucene since we already store all our terms in sorted (unicode) order.

The resulting implementation (currently a patch on

[LUCENE-2792](https://issues.apache.org/jira/browse/LUCENE-2792)) is fast and memory efficient: it builds the 9.8 million terms in a 10 million Wikipedia index in ~8 seconds (on a fast computer), requiring less than 256 MB heap. The resulting FST is 69 MB. It can also build a

[prefix trie](http://en.wikipedia.org/wiki/Trie), pruning by how many terms come through each node, with even less memory.

Note that because

[addition is commutative](http://en.wikipedia.org/wiki/Commutativity), an FST with numeric outputs is not guaranteed to be minimal in my implementation; perhaps if I could generalize the algorithm to a weighted FST instead, which also stores a weight on each arc, that would yield the minimal FST. But I don't expect this will be a problem in practice for Lucene.

In the patch I modified the

[SimpleText](http://chbits.blogspot.com/2010/10/lucenes-simpletext-codec.html)codec, which was loading all terms into a TreeMap mapping the BytesRef term to an int docFreq and long filePointer, to use an FST instead, and all tests pass!

There are lots of other potential places in Lucene where we could use FSTs, since we often need map the index terms to "something". For example, the terms index maps to a long file position; the field cache maps to ordinals; the terms dictionary maps to codec-specific metadata, etc. We also have multi-term queries (eg Prefix, Wildcard, Fuzzy, Regexp) that need to test a large number of terms, that could work directly via intersection with the FST instead (many apps could easily fit their entire terms dict in RAM as an FST since the format is so compact). The FST could be used for a key/value store. Lots of fun things to try!

Many thanks to

[Dawid Weiss](http://www.cs.put.poznan.pl/dweiss/)for helping me iterate on this.

Hello, what does the fst with 69 mb for wikipedia contains ? Only the titles of the entries or the whole text as well ?

ReplyDelete
Hi Michael,

ReplyDelete
That FST held all unique terms (tokens) from indexing all English Wikipedia content.

Hi Mike,

ReplyDelete
As the FST has a high CPU because of seeking, how bad are its performances affected by multiplying the number of existing terms?

Do you have an estimation of how is a typical query time distributed between the FST, seek in the term dictionary, calculating frequency or positions? How can I profile that in my own index?

Thanks!

Hi kbros,

Delete
The FST seek time is typically a tiny part of the overall query execution time; usually most of the time is spent iterating through the postings once the lookup is done in the terms dict. Only terms-dict heavy queries (e.g. FuzzyQuery, DirectSpellChecker, WildcardQuery) will really stress the terms dictionary.

That said, we have a Google Summer of Code project now working on using an FST to hold all terms in the terms dict, which then relies much more on the FST performance ... https://issues.apache.org/jira/browse/LUCENE-3069 has the details.

But if you are worried about it, run a profiler and report back the results! There are always things that need fixing :)

Hi Michael,

Delete
it seems that the result of the Google Summer of Code project has been committed.

Having a FST holding the complete Term Dictionary I think could be useful, for example in the SpellCheck scenario, to make a quick intersection between the Levenstein Automaton and the Index Terms Dictionary .

Am I right ?

Also in the Term component scenario, i think it can give us improvements ...

Can you briefly summarize me where do you think to use the FST Term Dictionary ? :)

Cheers

Hi Alessandro,

Delete
Unfortunately, I believe the FuzzyQuery performance was slower with the new FST-based terms dictionary, but yes, that is the idea: it ought to be faster.

DirectPostingsFormat, which stores all terms AND postings in RAM, does give a good speedup for fuzzy queries, so a DirectSpellChecker implemented on that would be faster. However, this format is VERY RAM consuming, i.e. it makes no effort to "compress" things (unlike FST).

I think there is room for a happy medium, e.g. pull out the terms dict from DirectPostingsFormat, maybe compress it a bit (but not as much as FST), and I think we'd see good speedups for terms-dict intensive operations.

We may even want to implement the Levenshtein intersection without the intermediate automaton, i.e. "on the fly", because constructing that automaton takes non-trivial time.

Thank you Michael for the quick answer,

ReplyDelete
For the intermediate automaton are you referring to the Levenstein Automaton, accepting all the strings with the expected distance from the query term ?

So directly building an automaton, accepting only Index terms with the expected distance from the the query term ?

Yes, that automaton.

Delete
But it turns out you don't have to fully build it up front, in order to do the "intersection". You can expand it as-you-go, which in theory saves time because then you only expand the parts that your terms dictionary would ever have encountered. It's sort of like a lazy automaton building ...

Yes , it makes sense and sounds reasonable :)

ReplyDelete
But is it feasible ?

I am starting learning about FSA and FST now, so I'm not yet into the implementation,

but one thing I remember is that Lucene FST implementation is so good and compact because it creates an immutable FST ( that becomes a sort of byte array under the hood) .

So creating an expandable FST is already possible or it will be a challenge ?

Can you suggest me other material to study ragarding this really interesting topic ? ( I followed your Solr revolution conference, some blog posts and videos so far :) )

Hi Alessandro,

Delete
Maybe read the original paper for the FST building algorithm we implemented in Lucene? http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698

But note that the Levenshtein automaton that we build/intersect for FuzzyQuery is not an FST; it's an Automaton (Lucene has two separate packages for these). I suspect by not pre-building the automaton, but rather expanding it on the fly, we could see some speedups in certain cases; not sure how much.

Hey Mike,

ReplyDelete
Are we using fst to make inverted index? If yes, where the output of traversing a string in fst pointing to?

FSTs are used only in certain places, e.g. the terms index (held in RAM, mapping term prefixes to blocks on disk), dictionaries (hunspell), suggesters, synonyms, etc. They are also used in an optional MemoryPostingsFormat, where each term and its postings are held in a big FST (good for primary key fields). We also more recently added a terms dict that holds just the terms + pointers to on-disk postings, in an FST.

Delete
What the output contains / where it points to varies drastically with each of these uses... really it's generic and can be whatever you need it to be.

I am curious what is the performance of FST. And its possible to map the words with id they occur in (a simple typeahead). and this will output the ids of document in which word occur can we somehow emulate the ranking formula (Similarity, or bmk21) and bake that in the FST, of course it would not be that simple but is it possilbe. Lets say we control the preprocess of words i.e know how many times the word appeared in the doc know how times word appeared in all docsids and then

Delete
bake that in some fst`s like wordFST scoringFST and so on. is this approach will benefit over traditional, and as i red there is no incremental way of updateing a fst i has to be rebuild from ground up.

Yes, you can encode that into an FST, and e.g. Lucene's MemoryPostingsFormat does exactly that. But this is not a good fit for fields where each term may occur in many docs, because the output byte[] in that case can get quite large.

Delete
i see thanks. I am almost sure you have seen the talk Michael Butch(sorry if i misspelled his name) gave about their implementation of memory postings in lucene and recent improvments that can lead them to be merged back in lucene, wondering is there initial talk about that.

Delete
I was wondering whether it is possible to associate ids with recognized strings in the automata. Say for instance I have a lexicon and each of its entry has a unique integer id. I'd like to compile the lexicon as an union string automata and whenever it recognizes an entry in a string, it outputs the unique id. It's like using the automata as a set of primary keys.

ReplyDelete
I could not find such an example of use online.

In a previous comment you mention MemoryPostingsFormat begin able to output ids (but document id), would it be possible to use that ? Thanks

Hi Anonymous,

Delete
Associating a String to an arbitrary (including Integer) output is precisely what FSTs are for, so that use case works easily. Try looking at TestFSTs.java for an example?

Thats astonishing...

ReplyDelete
Hi michael,

ReplyDelete
I have a question regarding prefix queries. How expensive it is to do prefix queries.

We are using solr in our organization. Majority of our queries are becoming prefix queries and i am worried that it will effect the performance. since it is not searching at that point but more of a matching.

what do you suggest if majority of the queries are prefix then should these be handled on index time using something like EdgeNgram instead doing all this at query time.

Just to give you an idea , our index might have 500 million terms.

This comment has been removed by the author.

ReplyDelete
Hi Michael,

ReplyDelete
I have three newbie questions about the (your) FST:

1) "As you traverse the arcs, you sum up the outputs, so stop hits 3 on the s and 1 on the o, so its output ordinal is 4."

For a given word (in your discussion, the word "stop"), are the output values assigned to arbitrary transition ("arcs")? Could you have instead assign: "stop hits 3 on the t and 1 on the o, so its output ordinal is 4."?

2) From the start state, why do transitions "p/2" and "t/5" going to the same state?

3) For simplicity, let's ignore stemming for a sec, and suppose we index a new word "popstar", do we simply introduce an arc going from end state back to the state which "s/3" points to?

After giving it more thoughts, 3)is not correct.

Delete
Perhaps I'll just ask, what would your FST would look like if we indexed popstar?

Hi Michael,

ReplyDelete
Is it possible that the FST takes regular expressions so that any sequence matching one regular expression can be transformed to an output. Could you please give me a few pointers please. Thank you!
