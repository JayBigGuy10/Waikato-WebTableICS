import requests
from bs4 import BeautifulSoup

URL = "https://timetable.waikato.ac.nz/perl-bin/timetable.pl?term=COMPX102-23B+%28TGA%29+COMPX310-23B+%28TGA%29+MATHS135-23B+%28TGA%29+ENGEN180-23B+%28TGA%29&submit=Create&action=Create&year=2023"
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

#print(dataTable)



from ics import Calendar, Event
import datetime

#first_day = '2023-09-04 00:00:00'
start_dt = datetime.datetime(2023, 8, 28)
weeks = 6

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
        e.name = data[0][0] +" "+ data[0][1].split('\xa0')[0]
        e.begin = event_dt#'2023-11-0'+str(data[2])+" "':00:00'
        e.duration = {"hours": 1}
        e.location = data[0][2]+" "+data[0][3]

        c.events.add(e)

    
    #print(e)
#print(c.events)

with open('s2p2.ics', 'w') as f:
    f.writelines(c.serialize_iter())

#[ss, dayTrack, rowTrack]
#[['COMPX102-23B (TGA)', 'Laboratory 01\xa0(2023)', 'Room', 'TCBD.3.04'], 1, 9]