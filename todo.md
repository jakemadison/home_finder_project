Okay, so, what actually is the plan with this thing?


The Problem:

- Trying to find a home on craigslist is annoying

- Mainly this is because you're essentially looking for a needle in a haystack

- The overwhelming majority of ads are useless.

- Let's make a more intelligent tool to parse through the listings.


1) Filters should not be binary but should represent trade-offs:
eg: There are certain areas of town where my price range is more flexible than others.
the same goes for en-suite laundry, amenities, etc

2) Multiple listings are a complete waste of everyone's time.  Let's filter those out completely.

3) A way of directly replying to the ad in question might be worthwhile.  Could include a template as well, which would
be editable before sending...

4) Any filtering based on the content of the post should probably be able to deal with typos... which are going to
be incredibly commonplace.  Levenschtein distance??

5) Being able to score each posting and then sort desc by score would probably be the best idea.  Then our filtering isn't necessarily
removing posts.  

Criteria for scoring: Price, Location, insuite/ensuite laundry, washing machine, availability, cat OK,
"furnished" that does not include "unfurnished/un furnished), size?

Right, so controls should assign filters, and then assign weights to filters.
An easy way of doing that might be just to order them in the list (top of list = most important)
=> this could be added to, expanded on by rating each of the postings 
(this one should have been higher, this one should have been lower, etc)

6) The current craigslist interface is ugly and fairly useless.  If I can determine I don't like a place in the first
few lines of the posting, let's just add that to the link.

7) Obviously, selecting that you are not interested in a place should nix that from the list: I don't want to have to
look at the same posting twice ever after making a decision on it's viability.

8) I should be able to keep a record all in one place of all the ads I have applied for, current message threads with the
owners, etc.


9) Is there a way to generalize this to all of craigslist??  Create filter type: post contains words, doesn't contain
=> standardized elements per posting category? 

10) Any time I am looking at craigslist it is with a specific goal in mind: new job, new apt, whatever.  When starting,
user should create a new "goal" page.  Then you can have the ability to switch between them.  Keep one for toronto, one for
vancouver, etc.


======
Here's an idea:

- there is a difference between looking for a job when you have a job, (or looking for a home when you have a home) vs
when you do not.

- If I have a home, I don't want to be actively looking as much, but I would love to be made aware of high-threshold
contenders. That is, total gem of places.

-> based on ordered-by-filter list, send me my top three picks per day? per week?

How can we make this self-learning? score by words in the page?
-> machine learn the fucker?  Location lat/lon information, price, details, etc.
-> word comparison (contains the words, blah or blah and blah).


=======
Location data is available, but we'll have to scrape it.
Model should be simple.  Let's ignore users and just have it on a per-instance level.
id, link (to the post), text of the post, location data, posting date, price, text of the post, images included in 
the post, positive_rating (1,0,null), insert time on the DB.


=======
ratings should be done using bootstrap carousel: http://getbootstrap.com/javascript/#carousel
something like a double click to "like" a post
refresh button for grabbing new posts
navigation: "new posts", "liked posts", "all posts"
basically, like tinder for navigation
post attributes could be iconified, map location, price, title, maybe the start of the post
carousel should be images from post.


-- we need a way of removing posts from the DB that are no longer active..
--> ugh, okay, maybe we should ditch the rss feed and parse out links from the main page.
except... we want to retain user choice to be able to continue to build the match algo..
still, users need a way of being shown that something has been delisted.. 
let's just add a field on the postings model for "delisted", and update that.
then current query just ignores delisted records.


===
so apparently there is an angular-js lib for doing exactly what tinder does: 
https://github.com/gajus/angular-swing/blob/master/examples/card-stack/index.html

I'm still not sure how that would work with mobile vs desktop platforms.
I don't think it would work for desktop... but it's really cool...



