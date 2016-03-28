Pitchfork Scraping
==================
Pitchfork is a popular music website that publishes reviews, news, and exclusive content daily. It's a pretty good source if you're able to ignore the occasional snarkiness. 

I tend to use Pitchfork's "Best Of" features to find new music. I always use Spotify to listen to any songs that seem interesting.

I'm tired of having to manually search for artist and song names to add to a playlist on Spotify. This script will scrape artist and song titles from all the pages of the online feature provided, add a new playlist to the Spotify user provided, and populate that playlist with as many tracks as it can find.

Usage
-----
    $ python pitchforkScraping/ YOUR_SPOTIFY_URI_NUMBER http://pitchfork.com/LINK/TO/BEST/OF/FEATURE

Dependencies
------------------
###Beautiful Soup 4.x
    $ pip install beautifulsoup4

###Spotipy 2.0
    $ pip install spotipy

See [Spotipy's documentation](http://spotipy.readthedocs.org/en/latest/) for help setting up local Spotify API environment, including saving access keys to your local environment (which is necessary for this script to work).


"Best Of" Example URLs
----------------------------
### [Top 100 Tracks of 2010-2014](http://pitchfork.com/features/lists-and-guides/9466-the-top-200-tracks-of-2010-2014/)

### [200 Best Songs of the 1980s](http://pitchfork.com/features/lists-and-guides/9700-the-200-best-songs-of-the-1980s/)

### [100 Best Tracks of 2015](http://pitchfork.com/features/lists-and-guides/9765-the-100-best-tracks-of-2015/)

####More lists can be found [here](http://pitchfork.com/features/lists-and-guides/).
