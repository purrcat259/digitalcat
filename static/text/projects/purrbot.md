A twitch.tv bot to automate visualisation of donations during charity livestreams.

Purrbot as an idea started from my participation in a 24 hour stream by [Dave Hughes](www.twitch.tv/selezen).

He played Elite: Dangerous for 24 hours straight in aid of the Marie Curie Cancer Foundation. As I watched I realised that he had his hands full trying to keep up with his agenda that he had for the day, especially since he had a number of guests joining him throughout the day.

At the time I did not have much leeway to help financially, so instead I used my time and skills, offering to write a script (or bot) that would post the amount donated every so often to the live chat beside the livestream.

Over the next few hours, I managed to cobble a web scrape to get the donation amount and a headless IRC connection to connect to the stream's chat.
Sticking to the mantra of "Always improving, never perfect", I continued to work on the bot as the stream went on. Posting the amount raised every X minutes or so meant that a number of donations were being collated as one donation. By decreasing the scrape delay to something close to 5 seconds and doing a simple string comparison, I set the bot to post whenever a donation occured.

Using the Python winsound module, a module which allowed playing audio files, the bot could then play a sound of a chewbacca roar with every donation that occurred. Eventually the 24 hour stream closed to over £1,000 raised.

Later on in 2015, another community centered around Elite: Dangerous, The Imperial Inqusition, were planning a 72 hour livestream in aid of the Princess Margaret Cancer Foundation. The scope of this charity stream was larger than the previous one, including a timetable of events where a different amount of streamers were streaming different games for varying, sometimes overlapping amounts of time.
I recorded the timetable (and adjusted it on the fly during the stream) in an SQLite database, storing the start and end times, title of the stream and streamers, then posting current events, donation amounts and links to the donation page and stream schedule.

Centralising this flow of information via my script helped take the load off the organisers and allowed visualisaiton of the donation data afterwords. The stream ended with over £2,200 raised for cancer research. To visualise the data, I used the python module matplotlib.

The Elite: Dangerous community is becoming well known for charity streams, which pushed me to keep working on Purrbot. The tool of choice for most streamers is Open Broadcaster Software or OBS. OBS also has plugin support, one of which is called the CLR browser plugin.

The CLR browser plugin runs a version of chromium as a source in the stream to allow addition of web assets. By wrapping the total amount donated in some HTML and making it available via a (currently disabled) [API](www.digitalcat.me/charity ), streamers could put the running total directly on their stream. It has been tested live to great effect in keeping both the streamer and the viewers informed during the course of the stream.