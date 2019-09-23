READ ME
##########################################################################

Drafting during the cycling portion of triathlons is illegal according the USA
Triathlon rules as drafting benefits the drafter and gives them an unfair
advantage over the rest of the competitors.  Drafting rules are outlined
in the USAT guidelines and should be enforced by referees and officials,
but officials are usually focused on the leaders of the race and many
competitors ride unchecked.

We developed this program as a proof of concept that drafting can be detected
by examining GPX data that racers upload to Strava after an event.
This program analyzes these GPX files to determine whether drafting occurred,
by which rider, and for how long.  This method of policing can check any
athlete who records and uploads their race.  

Run main.py in Python3 to get the drafting results from two gpx files.

Running this program will give drafting information represented as the amounts
of time that drafting rules were violated and by which rider.
Additionally, the program outputs assesses the quality of the GPX files and
informs the user how accurate this drafting assessment is.
Finally, the program creates and saves a map "map.html" to user's computer.
The user can open map.html in a browser to see a flyby of the two cycling files.
