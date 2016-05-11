Notifier script for mentions of the word "sock" on Elite: Dangerous subreddits

Originally, I had tried my hand at creating a bot which would parse a JSON API to check for blog posts from [the ArmA 3 Dev Blog](https://dev.arma3.com/) and then post the blog post along with its text to the respective subreddit on Reddit.

I completed this script and I knew it worked properly under test conditions, however at the time I did not wish to leave my computer running 24/7 and I was not aware of cheaply available VPS services. Eventually I lost interest in deploying the script as I stopped actively playing ArmA, moving on to Frontier Development's Elite: Dangerous instead.

Fast forwarding to EGX 2015, a reddit user /u/tfaddy claimed that he would "eat a sock" if a planetary landings expansion was announced for Elite: Dangerous at EGX, saying that it was too soon for them to have finished the technology required, however Frontier Developments CEO David Braben revealed planetary landings on stage at EGX that year. Eventually /u/tfaddy released an unlisted youtube video of him talking about the bet, then eating some sock shaped seaweed.

Sockbot arose from another redditor's comment where "typing the word sock in the subreddit is basically equivalent to paging /u/tfaddy". Remembering my ArmaBot project, I volunteered to create a bot which would message /u/tfaddy every time someone used the word sock in any Elite: Dangerous subreddit. I deployed sockbot to my personal Raspberry Pi 1, enabling me to leave it running 24/7.

By using a Python module called PRAW and interfacing with an sqlite database, the script searches through the latest reddit comment, responds to any involving the word sock (with a check to avoid false positives such as "socket"), then record the comment ID in a database to avoid responding move than once. After two months, the sockbot project was retired from the main subreddits due to popular demand and the comedic effect of sockbot having worn off.

I wrote a post-mortem about the project [here](https://www.reddit.com/r/EliteDangerous/comments/3zwxih/sockbot_a_postmortem/). Eventually, Frontier Developments released Elite: Dangerous socks on their store, with the tagline "Good enough to eat!" as a reference to /u/tfaddy's sock eating bet. You can find them [here](https://www.frontierstore.net/eur/merchandise/elite-dangerous-merchandise/elite-dangerous-logo-socks-black.html).

Turns out that Frontier Developments CEO David Braben is a co-founder of the Raspberry Pi foundation, so the project turned out to be a case of two worlds colliding, in his own words:

> Happy that sockbot (RIP) ran on a Raspberry Pi. Didn't realise. one of those 'two worlds colliding' moments...

You can find the source code for sockbot [here on GitHub](https://github.com/purrcat259/sockbot).
