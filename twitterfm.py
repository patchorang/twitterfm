import cgi
import json
import pickle
import urllib
import urllib2
import webapp2

from google.appengine.api import users

api_key = pickle.load(open('api_key.pic', 'rb'))

class MainPage(webapp2.RequestHandler):

	def getTopArtists(self, username):
		base_url = 'http://ws.audioscrobbler.com/2.0/'
		query = '?method=user.getweeklyartistchart&user=' + urllib.quote(username) + '&api_key=' + api_key + '&format=json'
		lastfmResponse = urllib2.urlopen(base_url + query)
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

	def displayTweet(self, tweet):
		self.response.write('<p>')
		self.response.write(tweet['from_user'] + " - ")
		self.response.write(tweet['text'])
		#self.response.write('<img src="' + tweet['profile_image_url'] + '">' )
		self.response.write('</p>')

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
		artists = self.getTopArtists(self.request.get('content'))

		for artist in artists['weeklyartistchart']['artist']:
			self.response.write(artist['name'])
			tweets = self.searchTwitter(artist['name'])
			if tweets != None:
				for tweet in tweets['results']:
					self.displayTweet(tweet)
	
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
