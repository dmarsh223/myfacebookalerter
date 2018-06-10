import facebook
import secrets

graph = facebook.GraphAPI(secrets.access_token)
print (graph)
#to post to your wall
graph.put_object("me", "feed", message="access token test")