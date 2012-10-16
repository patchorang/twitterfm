import cgi
import json
import urllib
import urllib2
import webapp2

from google.appengine.api import users

class MainPage(webapp2.RequestHandler):

	def searchTwitter(self, searchString):
		base_url = 'http://search.twitter.com/search.json?q='
		query = urllib.quote(searchString)
		twitterResponse = urllib2.urlopen(base_url + query)
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
		data = self.searchTwitter(self.request.get('content'))
		
		for result in data['results']:
			self.displayTweet(result)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
