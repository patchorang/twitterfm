import cgi
import json
import urllib2
import webapp2


from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
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
		query = 'http://search.twitter.com/search.json?q=' + self.request.get('content')
		twitterResponse = urllib2.urlopen(query)
		data = json.loads(twitterResponse.read())
		
		for result in data['results']:
			self.response.write('<p>')
			self.response.write(result['from_user'] + " - ")
			self.response.write(result['text'])
			self.response.write('</p>')

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
