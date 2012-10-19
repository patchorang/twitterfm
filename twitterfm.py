import cgi
import json
import os
import pickle
import urllib
import urllib2
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

api_key = pickle.load(open('api_key.pic', 'rb'))
lastfm_base_url = 'http://ws.audioscrobbler.com/2.0/'


class MainPage(webapp2.RequestHandler):

	def getTopArtists(self, username):
		query = '?method=user.getweeklyartistchart&user=' + urllib.quote(username) + '&api_key=' + api_key + '&format=json'
		lastfmResponse = urllib2.urlopen(lastfm_base_url + query)
		return json.loads(lastfmResponse.read())

	def searchTwitter(self, searchString):
		base_url = 'http://search.twitter.com/search.json?q='
		twitterResponse = None
		try:
			query = urllib.quote(searchString)
			twitterResponse = urllib2.urlopen(base_url + query)
		except KeyError:
			pass
		except urllib2.HTTPError:
			pass
		if twitterResponse != None:
			return json.loads(twitterResponse.read())

	def getTweetArray(self, tweets):
		tweetArray = []
		for tweet in tweets['results']:
			tweetArray.append(tweet)
		return tweetArray

	"""	def displayTweet(self, tweet):
		self.response.write('<p>')
		self.response.write(tweet['from_user'] + " - ")
		self.response.write(tweet['text'])
		#self.response.write('<img src="' + tweet['profile_image_url'] + '" width="48" height="48">' )
		self.response.write('</p>')

	def getArtistImage(self, mbid):
		query = '?method=artist.getinfo&mbid=' + mbid + '&api_key=' + api_key + '&format=json'
		lastfmResponse = urllib2.urlopen(lastfm_base_url + query)
		artistInfo = json.loads(lastfmResponse.read())
		return artistInfo['image']"""
		
	def get(self):
		self.response.out.write("""
			<html>
				<body>
					<form action="" method="post">
						<div><textarea name="content" rows="1" cols="60"></textarea></div>
						<div><input type="submit" value="Find Tweets"></div>
					</form>
				</body>
			</html>""")

	def post(self):
		weeklyInfo = self.getTopArtists(self.request.get('content'))

		artistsUnfiltered = weeklyInfo['weeklyartistchart']['artist']
		artistsAndTweets = {}
		for artist in artistsUnfiltered[0:5]:
		    artistDict = {}
		    name = artist['name']
		    tweetsJson = self.getTweetArray(self.searchTwitter(artist['name']))
		    tweets = []
		    for tweet in tweetsJson:
		    	tweets.append(tweet['text'])
			artistsAndTweets[name] = tweets
						
		template_values = {'artistsAndTweets': artistsAndTweets}
			
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
	
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
