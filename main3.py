import requests
from bs4 import BeautifulSoup

from icalendar import Calendar, Event
import datetime
import pytz
import uuid

#URL = "https://timetable.waikato.ac.nz/perl-bin/timetable.pl?term=COMPX102-23B+%28TGA%29+COMPX310-23B+%28TGA%29+MATHS135-23B+%28TGA%29+ENGEN180-23B+%28TGA%29&submit=Create&action=Create&year=2023"
URL = "http://localhost/2024%20Online%20Timetable_%20University%20of%20Waikato.html"

start_dt = datetime.datetime(2024, 2, 19, tzinfo=pytz.timezone("Pacific/Auckland"))
weeks = 1

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

dataTable = []

dayTrack = 0
rowTrack = 0

job_elements = soup.find_all("table", class_="customtt table")
for table in job_elements:
    trows = table.find_all("tr", class_="")
    for row in trows:
        ttd = row.find_all("td")
        for td in ttd:
            if td["class"][0] == 'valuecell':
                spans = td.find_all("span")
                for span in spans:
                    subject = span.find("strong")
                    ss = span.get_text(strip=True, separator='|').split("|")
                    event = [ss, dayTrack, rowTrack]
                    dataTable.append(event)

            dayTrack += 1
        rowTrack += 1
        dayTrack = 0



c = Calendar()
c.creator = "ics"
for week in range(0,weeks):
    start_dt = start_dt + datetime.timedelta(weeks=1)
    print(start_dt)
    for data in dataTable:
        hour = data[2] + 7
        day_of_week = data[1]

        event_dt = start_dt + datetime.timedelta(days=day_of_week,hours=hour)

        e = Event()
        e.add('dtstart', event_dt)
        e.add('summary', data[0][0] +" "+ data[0][1].split('\xa0')[0])

        e.add('location', data[0][2]+" "+data[0][3] )

        duration = datetime.timedelta(hours=1)
        end_time = event_dt + duration
        e.add('dtend', end_time)
        
        uid = str(uuid.uuid4())
        e.add('uid', uid)

        c.add_component(e)

f = open('example.ics', 'wb')
f.write(c.to_ical())
f.close()

#[ss, dayTrack, rowTrack]
#[['COMPX102-23B (TGA)', 'Laboratory 01\xa0(2023)', 'Room', 'TCBD.3.04'], 1, 9]