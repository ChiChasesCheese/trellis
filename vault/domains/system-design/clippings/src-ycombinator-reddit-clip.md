---
title: How Hacker News ranking algorithm works
source: https://news.ycombinator.com/item?id=1781013
published: '2010-10-11'
site: news.ycombinator.com
clipped: '2026-09-20'
---

# How Hacker News ranking algorithm works

| [Guidelines](newsguidelines.html) \|[FAQ](newsfaq.html) \|[Lists](lists) \|[API](https://github.com/HackerNews/API) \|[Security](security.html) \|[Legal](https://www.ycombinator.com/legal/) \|[Apply to YC](https://www.ycombinator.com/apply/) \|[Contact](mailto:hn@ycombinator.com) | 

|  | **[Hacker News](news)**[new](newest) \|[past](front) \|[comments](newcomments) \|[ask](ask) \|[show](show) \|[jobs](jobs) \|[submit](submit) | [login](login?goto=item%3Fid%3D1781013) | 

|  |  | [How Hacker News ranking algorithm works](http://amix.dk/blog/post/19574) ([amix.dk](from?site=amix.dk) ) | 
|  |  | 311 points by [cristoperb](user?id=cristoperb)[on Oct 11, 2010](item?id=1781013) \|[hide](hide?id=1781013&goto=item%3Fid%3D1781013) \|[past](https://hn.algolia.com/?query=How%20Hacker%20News%20ranking%20algorithm%20works&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0) \|[favorite](fave?id=1781013&auth=ba1dc8f91037458783c3654aba97322dc0b1ace0) \|[74 comments](item?id=1781013) | 

|  |  | That's close to the current version, but a little out of date. Here's the code running now: | 

|  |  | For those who aren't well versed in Arc or Lisp, could someone go through the differences? | 

|  |  | Appears to be substantially identical to what's outlined in the post. The only changes are in the penalties dealt out by the type of story, inclusion of a url, buried status, gagged status, and the operation of penalties due to the contro(versial?)-factor function. If you're just submitting interesting URLs and worry about them being shunted off the main page by gravity then there are no practical differences. | 

|  |  | The gag tag doesn't mean "gagged."  It means the post is a gag, in the sense of a joke. Sorry I can't be more transparent about how contro-factor is calculated, incidentally. Its purpose is to recognize flamewars. | 

|  |  | I'm curious about how you evaluate prospective algorithm changes. Do you roll out a change you think should work and then monitor, or do you have a corpus of e.g. flame wars you test against? | 

|  |  | There's a repl on the server, and I test tweaks on the live site. | 

|  |  | Do you have a dashboard of some kind to visualize your tests effects? I am curious about the broad kind of insight one could have with such a programmatic access to this community. Perhaps I missed an essay about HN/REPL? | 

|  |  | Any genius willing to translate this to python? | 

|  |  | There's a python implementation in the original article: ```   def calculate_score(votes, item_hour_age, gravity=1.8):       return (votes - 1) / pow((item_hour_age+2), gravity) ```  | 

|  |  | I would prefer PHP but seconded | 

|  |  | This is pretty trivial but sure, something like: ```   function calculate_score($votes, $item_hour_age, $gravity=1.8) {     return ($votes - 1) / pow(($item_hour_age+2), $gravity);   } ```  | 

|  |  | it's interested to see such a direction comparison of PHP to Python. PHP is very similar to the Python except with more syntax noise. :) And probably worse docs. And worse namespacing, etc. ;) | 

|  |  | do you guys take logs of both sides, so you don't have to keep updating the scores of all the previously posted items? I mean, if all that matters is how big the scores are relative to one another, then A > B <=> log A > log B (since A and B are positive). You'll just have to add a G*log(T+2) to the log(P) for new items, which can go on for a very long time. ... T is the time since some arbitrary point. I think I may have just reinvented the way reddit does it :P | 

|  |  | in fact, as someone else said if you then make T = the number of submissions / votes since the beginning, people would be able to post at midnight and it would still have a "fair" chance of being ranked along with the other articles posted at busier times. | 

|  |  | Some weaknesses of this algorithm are: (1) Wall-clock hours penalize an article even if no one is reading (overnight, for example). A time denominated in ticks of actual activity (such as views of the 'new' page, or even upvotes-to-all-submissions) might address this. (2) An article that misses its audience first time through -- perhaps due to (1) or a bad headline -- may never recover, even with a later flurry of votes far beyond what new submissions are getting. Without checking the exact numbers, consider a contrived example: Article A is submitted at midnight and 3 votes trickle in until 8am. Then at 8am article B is submitted. Over the next hour, B gets 6 votes and A gets 9 votes. (Perhaps many of those are duplicate-submissions that get turned into upvotes.) A has double the total votes, and 50% more votes even in the shared hour, but still may never rank above B, because of the drag of its first 8 hours. (I think you'd need to timestamp each vote for an improved decay function.) | 

|  |  | *Wall-clock hours penalize an article even if no one is reading (overnight, for example)*I'd be interested to know what the hourly fluctuation for HN is actually like, on account of having readers all over the world. I'm in Australia, so your example "submitted at midnight" California time[1] means submitted at 6pm my time. Also 8am London time, 11am Moscow time. :). [1] I'm going to go ahead and assume you're in California. ;) | 

|  |  | I'm in California, usually, but have often observed HN through the California night -- either because of my own odd online hours, or trips to distant time-zones. It's true there's never total quiescence, but the pace of actions changes by a noticeable factor. (Without going to the data, I'd guess 5X from trough to peak over a day's cycle, and a somewhat smaller weekend-to-weekday difference. Holidays and nice bay area weather also play a factor.) | 

|  |  | I've found optimal submission time to generally be midday london time, you catch the european lunch-time traffic and the US wake-up/get-into-work traffic. I don't think traffic from anywhere else is heavy enough to matter. | 

|  |  | I'm in Iowa, so it's central time.  But it's not uncommon to see 2 or 3 hour old stories on the front page by 10:30 or so. | 

|  |  | I believe reddit has historically done something similar.  Rather than having a given article's ranking decay over time, they simply hand out better ranks to newer articles, leading to continual inflation.  A naive example of this sort of ranking would be (timestamp in hours + upvotes - downvotes). This would make your (excellent) idea easy to implement, because you could just use an autoincrement key as the timestamp, ignoring any sort of decay calculations. | 

|  |  | This inflation based approach also plays nicely with database indexes. | 

|  |  | (1) "overnight" not exist in the Internet era. (from Spain) | 

|  |  | You are right of course, but I suspect the vast majority of HN users are not only in the USA but specifically in California. So even though people are using the site around the clock, there is probably a lot more traffic during the "awake hours" of California. | 

|  |  | > I suspect the vast majority of HN users are not only in the USA but specifically in California I suspect that you have a nonstandard definition of "vast majority." I'd be surprised if even 1/4 of HN users are in California. There's a whole wide world out there! :) | 

|  |  | Although my Hacker Newsletter stats could be completely different than HN, it is a subset of HN users so it might be relevant - California averages around 20% of my opens and the USA about 70% of the total. Edit: Just to add to this - New York and Massachusetts are the next highest and combined make up about the same as California. | 

|  |  | 25% of a website's userbase being located in one state of one country is a "vast majority" on the Internet, it having a far higher HN'er/population ratio then any other state or country. | 

|  |  | To be pedantic, the definition of majority is half the group, and 'vast' implies upwards of 70%. You probably mean something like a "large plurality" | 

|  |  | Yes and when somebody in France makes a French equivalent of Le Hacker News, and a bunch of Americans start posting there, in second language French, then the "host country" readers can make the same geo assumption in reverse. ;) | 

|  |  | The thing I like about HN's ranking algorithm is how simple it is. Implementing something more sophisticated would require more work and probably much better servers. Recently, I have been implementing a ranking algorithm and I started in the wrong direction by taking all kinds of things into consideration. This is dangerous because you spend a lot of time on something that is mostly irrelevant. The bottom line is that HN's algorithm works pretty well for the majority of cases. There are some edges, but solving them would not be trivial and would require a lot more work. | 

|  |  | I'd agree simple is better. Of the two suggestions, replacing hours with artificial ticks adds very little complexity: it's the same formula, with one value replaced, and the accompanying factor adjusted. (The ticks might be submission-count, upvote-count, visit-count, or anything else trivially tallied -- it may not make much difference, except that over time greater activity could require adjusting the tick-deflator-factor.) | 

|  |  | visit count is not trivial. A db write for every page view is heavy. | 

|  |  | Persist it in memory, you only need periodical writes for something like that. We're not running on a $5 powweb account here. | 

|  |  | Right, but then it's not trivial which was my point. It can. Be trivial and not scale, or scale and not be trivial. I'm not sure why I get down voted for this. | 

|  |  | I do agree that that the *Wall-clock* hours argument is somewhat weak due to the international crowd behind HN, but it would be interesting to see how weekends or really more general traffic patterns such as what may happen on holidays attribute to scores. I know that in these cases, I generally diverge from my normal HN-checking patterns. | 

|  |  | *(I think you'd need to timestamp each vote for an improved decay function.)*Well, somewhat. You'd need a timestamped sufficient statistic, but not necessarily each vote. Consider ACO. Given +1: ```   t0=last_change_timestamp   s0=score_after_last_change   s1=1+s0/exp(t1-t0) ```  | 

|  |  | HN does't really experience a night, since people from all over the planet or on the site. But maybe it would be better to divide by a number of impressions wighted with something. | 

|  |  | Well, you can fix (1) by simply incrementing T not by actual time but just be the total # of votes/submissions since the beginning. | 

|  |  | When I built oknotizie.virgilio.it many years ago, more or less at the same time reddit was created, I used the same base algorithm, that is: RANK = SCORE / AGE^ALPHA, where ALPHA is the obsolescence factor. This is a pretty obvious algorithm, but the evil is in the details. First, since oknotizie is based in italy AGE is calculated in a special way so that nightly hours are calculated in a different way (every hour should be take into account proportionally to the traffic that there is in this hour). Second, there is to do a lot of filtering. Oknotizie is completely built out of anti-spamming: statistical analysis on users voting patterns, cycles detection, an algorithm penalizing similarities in general in the home page, and so forth. To run a simple HN style site is simple as long as the community is not trying hard to game it. Otherwise it starts to get a much more complex (and sad) affair. | 

|  |  | A problem (IMHO) with the HN ranking algorithm is that once a post fails to get traction (perhaps because things were busy at the time it was submitted), it won't really be able to get traction later, even if it's re-discovered 6 hours or 2 days later. Seems to me like velocity ought to be taken into account a little more for items that have otherwise languished. | 

|  |  | This has been the case with my bootstrapping post.  It has been revived a few times thanks to tweets and other references since its initial publication to HN, but it has never risen back to where it was, even though it has twice as many points as it did 11 days ago. | 

|  |  | Here's an explanation of other ranking algorithms, including Bayesian average, Wilson score and the ones used on HN, Reddit, StumbleUpon and Del.icio.us: [http://blog.linkibol.com/2010/05/07/how-to-build-a-popularit...](http://blog.linkibol.com/2010/05/07/how-to-build-a-popularity-algorithm-you-can-be-proud-of/) | 

|  |  | This is not the 'hacker news' ranking algorithm, this is the ranking algorithm distributed with 'ARC', which is the basis for the HN algorithm, but definitely not equal to it. The biggest missing ingredients are flagged posts dropping off quicker and posts that contain no URL dropping off quicker but there are quite a few other subtle tweaks. The (very good) reason why the ARC sources do not give out the real ranking algorithm is to make it a bit harder to game the system. | 

|  |  | He glossed over it, but this code does include URL-free posts dropping off faster. See the stuff dealing with "nourl-factor*". I don't know arc at all, but it appears that having no URL multiplies your final score by a factor of .4, meaning that it's ranked almost 3x lower than it otherwise would be. That surprises me; I've noticed that Ask HN get rated lower, but it doesn't seem that extreme. So is Hacker News is a fork of news.arc, rather than straight news.arc? I figured it was, but never heard that officially (since people refer to news.arc as the HN "source code"). Edit: Also, the "lightweight" thing is interesting. There's something in place that sees if the post is a "rallying cry" or is mostly made of images. Additionally, if you link directly to an image file, or to some list of domains that have been deemed lightweight, that'll get marked as lightweight as well. Lightweight posts have a .3 factor, meaning that they're even more deflated than URL-free posts. | 

|  |  | Ah yes, you're right, the 'nourl' is there, it's in the arc bit, but I couldn't find that in the graphs or in the python code. | 

|  |  | The current HN algorithm probably follows the same basic idea, but the implementation is more complex because of spammers. I did a fast test of how placements would look like with the vanilla HN algorithm using the current frontpage: [http://paste.plurk.com/show/316811/](http://paste.plurk.com/show/316811/) The code to generate the new sorting: [http://paste.plurk.com/show/316812/](http://paste.plurk.com/show/316812/) As you can see the rankings are not the same, but very similar... | 

|  |  | Flags are the main factor that you've missed I'm not quite sure how to measure them reliably but from what I've seen in terms of 'jumps' downward on a heavily flagged post it looked like 6 flags will take you off the homepage on to page two when you have about 20 upvotes. Maybe that will allow you to model it. | 

|  |  | I have two will take you off when you are under 9 upvotes. | 

|  |  | How did you know how many flags it had? | 

|  |  | Counting the jumps down the home page. Would be nice if PG could confirm this either way (right or wrong), but I'm fairly sure that's what it is. It wouldn't make sense any other way (it was this post: [http://news.ycombinator.com/item?id=1759548](http://news.ycombinator.com/item?id=1759548) ) it got to the first spot on the homepage very quickly and then dropped in six steps off the homepage. 19 points, six steps, that's averaging 3 points per step, so it's like a single flag counts for 3 'downvotes' on an article or something close to that. That's all guesswork of course. | 

|  |  | I built a reasonably similar ranking system a few years ago, but also taking social media interaction (blog links, delicious bookmarks, etc) with the content items being ranked into account: [http://bergie.iki.fi/blog/calculating_news_item_relevance/](http://bergie.iki.fi/blog/calculating_news_item_relevance/) You can see it in action on maemo.org: [http://maemo.org/news/](http://maemo.org/news/) PHP sources: [http://trac.midgard-project.org/browser/branches/ragnaroek/m...](http://trac.midgard-project.org/browser/branches/ragnaroek/midcom/org.maemo.socialnews) | 

|  |  | I made an HN filter for myself, that's basically: points / comments It works shockingly well. Its here if anyone would like to check it out: [http://www.upthread.com/](http://www.upthread.com/) | 

|  |  | Yep, you basically have a controversy filter. | 

|  |  | Does anybody care to explain the strange indentation I see in the Arc code? I know Lisp a little (mostly Clojure), but I don't get the indentation of the code at the bottom of the algorithm where it looks like it's branching in two parts. Is this peculiar to Arc? Or to other Lisps as well? | 

|  |  | That's because of the way Arc does if-expressions. In Scheme and Common Lisp, you have two conditional forms: 'if and 'cond. 'if takes three arguments (or two, with an implied nil, in CL), and is analogous to an if-then-else in other languages: 'cond, in contrast, takes as many branches as you like, but they're parenthesized like so:```     > (if #t 'then 'else)     then     > (if #f 'then 'else)     else  ``` In arc, there's just 'if, which is like 'cond with a lot of implicit parenthesization and else-branches:```     > (cond (#f 'a)              (#t (display "I can have a body here!\n")                 'b)             (#t 'c))     I can have a body here!     b  ``` ```     arc> (if t 'then 'else)     then     arc> (if nil 'then)         ; if no else-branch is given, nil is implied     nil     arc> (if nil 'a              t   (do (prn "'do is like Scheme's 'begin or CL's 'progn.")                      'b)              'else)     'do is like Scheme's 'begin or CL's 'progn.     b ```  | 

|  |  | I've barely looked at Arc[1] but as far as I remember, the *if* macro/special form allows an arbitrary number of argument forms, a bit like a combination of Clojure/CL's*if* and*cond* :*cond* ). With an even number of arguments, there is no else-expr (the same as CL/Clojure```   (if     cond1  expr1     cond2  expr2     ..     ..     condN  exprN            else-expr)  ``` The indentation is probably to distinguish between condition and conditional expression - the second column is what could be evaluated and returned from the whole expression. [1] I too use Clojure | 

|  |  | Doesn't stray that much from clojure, so I think it's a lisp thing. To keep bindings in clojure with different length names more readable, people tend to indent like this: Sort of the same effect in the arc snippet in OP.```     (let [really-long-name l           score            (get-score x)           position         (get-pos) x)           test             test]          (...                 ....)))))  ```  | 

|  |  | For more details on the algorithm, see my article "Inside the news.yc ranking formula" from last year: [http://www.arcfn.com/2009/06/how-does-newsyc-ranking-work.ht...](http://www.arcfn.com/2009/06/how-does-newsyc-ranking-work.html) | 

|  |  | Nice post. Do you know what is the algorithm for the ranking of comments? I think this would be interesting to write about that too. | 

|  |  | The home page algorithm seems to have changed recently, but the RSS feed hasn't and is much noisier. It would be nice to see the RSS feed updated to reflect the home page changes (or confirmation that I'm just perceiving a difference that doesn't actually exist). | 

|  |  | So, if you're implementing this in a framework like Django or Rails, can you get a result set in this order directly from a query? Or do you have to query then sort? | 

|  |  | In Django, you could make the ranking score a property of the model and then do query.order_by('-score'). | 

|  |  | A basic question: If this was performed on page load, and in-memory, how would the first db fetch occur? Unless this is pushed 'somehow' to the database. | 

|  |  | so this means you'd be best served to submit something at or nearest peak hours? what are the peak use hours on HN? since everyone is a hacker, i'd assume it was evening hours on east and west coast US as heaviest load? not 9-5 ET? | 

|  |  | Don't forget employed people with ADD, or people who are bored at work, who stroll over here when they need a break from their job. | 

|  |  | Looks like there is a built in max lifetime of about 5-10 hrs. | 

|  |  | I feel like lots of big stories have managed to last overnight, so at least 12 hours, so I don't think this can be true. I've no idea how I would prove that though. | 

|  |  | This is also anecdotal but I think TechCrunch's "AngelGate" article was on the front page for almost 3 days. | 

|  |  | Maybe 'half life' is a better way to put it. Looking at the graphs, the score drops to ~1 in 5-10 hrs, unless the points are very high. | 

|  |  | I've wondered if there aren't some hands-on efforts (as in, non-automated) to keep particular stories on the front page. | 

|  |  | I thought the "secret sauce" was hidden from Arc sources..? | 

|  |  | My understanding is that the actual HN implementation is heavily customized and not public. | 

|  |  | Maybe what's hidden is the code for determining what counts as a vote.  e.g., multiple votes from the same IP may be discounted or simply counted as a single vote.  Or a bunch of votes coming from fresh accounts created at or after submission time. | 

|  |  | That algorithm has been in the source for a while. What is unknown is the current constants and if he changed it at all since first publishing it. | 

|  |  | Thanks for the info!  now I need to get my son to explain to me. :) |
