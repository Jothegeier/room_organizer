# Room-Organizer

A Webserver with connection to WebUntis API, which can show all the lesson data. It is made to be shown on every floor of a building to let every student see which class is in which room.

## Installation

1. Make sure you installed Python correctly
2. Install pip packages
- pip install
--> webuntis
--> flask
3. Execute RaumStundenPlan.py

## Konfiguration

1. "credentials"
The user-credentials with access for requesting the Data from webuntis
2. "url"
URL for Webuntis-API.
3. "request_time"
The interval for the API requests.
4. "server_url"
The URL for the Webserver. If you want it to be open in LAN, choose 0.0.0.0.
5. "server_port"
The Port on which the webserver is running.
6. "website_refresh_time"
The interval of refreshing the Website.
7. "lesson_switch_difference"
Minutes before ending of the lesson before, where the website shows the lessons of the next lesson.
8. "lesson_length"
Minutes, how long a lesson is.
9. "lesson_times"
The start-times of every lesson.
10. "rooms"
The room ordered to each

## Website Options

URL arguments:

    - "hour"
    -> "auto"
    -> number of lesson (ex. "hour=4")
    - "floor"
    -> number of the floor (ex. "floor=3")
    - "teacher"
    -> nickname of teacher (ex. "teacher=GEM")
    - "subject"
    -> name of subject (ex. "subject=SWD")
    - "room"
    -> roomname (ex. "room=R324")
    - "class"
    -> classname (ex. "class=FS215")
    - "buttons"
    -> disable left button options with buttons=false
    - "searchbar"
    -> enable searchbar of the table with searchbar=true

Full Example:
http://localhost:8088/raumstundenplan?hour=auto&class=FS215&subject=SWD&teacher=GEM&room=R324&floor=3&buttons=false&searchbar=true

Other Options:
- Manual choose floor and lesson