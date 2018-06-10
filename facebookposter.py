import facebook
import secrets
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup


#facebook authentication
graph = facebook.GraphAPI(secrets.access_token)
print (graph)

# set variable for date and time for logs
currentdatetime = datetime.now()

# correct URL
page = urlopen("https://alerts.weather.gov/cap/wwaatmget.php?x=NJZ020&y=0")

#run xml through beautifulsoup
soup = BeautifulSoup(page, "lxml")
print (soup.prettify())

# creates a list of the alert titles from the xml page
alert_descripton_list = []
for tag in soup.findAll('title'):
    alert_descripton_list.append(str((tag.contents)))

# checks for active alerts and ends program if there are no active alerts
secondTitle = alert_descripton_list[1].strip("[]'")
print (secondTitle)

if secondTitle == "There are no active watches, warnings or advisories":
    f = open('E:\logs\staffordnwsweatherlogs.txt', 'a')
    f.write('\n%s - No active alerts' % (currentdatetime))
    f.close()
    print("No active alerts - exiting program")
    exit()

# checks log file for current id from XML. If ID is present the program exits
# if ID is not present, it is written to the file and the program continues
id_descripton_list = []
for tag in soup.findAll('id'):
    id_descripton_list.append(str((tag.contents)))


# creates id object for duplicate alerts, if duplicate is found in log file program exits
uniqueID = id_descripton_list[1]
# test print
print (uniqueID)

if uniqueID in open('E:\logs\staffordnwsweatherlogs.txt').read():
    f = open('E:\logs\staffordnwsweatherlogs.txt', 'a')
    f.write('\n%s - Duplicate alert found' % (currentdatetime))
    f.close()
    print("Duplicate alert found, exiting program.")
    exit()

# if the alert id is not found in the log file this adds the id to the
# log file and continues on

else:
    f = open('E:\logs\staffordnwsweatherlogs.txt', 'a')
    f.write('\n%s - New alert found: %s' % (currentdatetime, secondTitle))
    f.write ("\n%s" % (uniqueID))
    print ("New alert found - written to log")
    status_update = ("Stafford Weather Alert: %s. Visit https://goo.gl/pAkZqg for more information." % (secondTitle))


#post to facebook page wall
graph.put_object("me", "feed", message=status_update)
