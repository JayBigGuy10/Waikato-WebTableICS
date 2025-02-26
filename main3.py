from bs4 import BeautifulSoup

from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import uuid

lines = []
while True:
    line = input(": ")
    lines.append(line)
    if '</table>' in line:
        break

soup = BeautifulSoup("".join(lines),"html.parser")

events = []

job_elements = soup.find_all("table")
for table in job_elements:
    trows = table.find_all("tr", class_="")
    for row in trows:
        ttd = row.find_all("td")
        for td in ttd:
            if td.contents:
                eventObjs = td.find_all("div")
                for eventObj in eventObjs:
                    subject = eventObj.find("strong")
                    event = eventObj.get_text(strip=True, separator='|').split("|")
                    if event not in events:
                        events.append(event)

c = Calendar()
c.creator = "ics"

for event in events:

    print(event)

    # Step 1: Extract weekday and time
    parts = event[2].split(" ")
    weekday = parts[1]  # "Wednesday"

    start_time = datetime.strptime(parts[2], "%I:%M%p").time()
    end_time = datetime.strptime(parts[4], "%I:%M%p").time()

    dummy_date = datetime.today().date()
    start_datetime = datetime.combine(dummy_date, start_time)
    end_datetime = datetime.combine(dummy_date, end_time)

    event_length = end_datetime - start_datetime

    # Step 2: Extract weeks
    weeks = []
    for part in event[3].replace("Weeks: ", "").split(", "):
        if "-" in part:
            start_week, end_week = map(int, part.split("-"))
            weeks.extend(range(start_week, end_week + 1))
        else:
            weeks.append(int(part))

    # Step 3: Generate datetime objects for each week
    # Assume the academic calendar starts on week 1 at a given reference date (e.g., first Monday)
    reference_date = datetime(datetime.today().year, 1, 1)  # Example: Start of the year (adjust if needed)
    while reference_date.weekday() != 0:  # 0 = Monday
        reference_date += timedelta(days=1)

    # Find the first occurrence of the target weekday
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_index = days_of_week.index(weekday)

    # Create the list of datetimes
    datetimes = []
    for week in weeks:
        # Find the start of the given week
        week_start = reference_date + timedelta(weeks=week - 1)
        
        # Find the specific weekday in that week
        target_date = week_start + timedelta(days=(weekday_index - week_start.weekday()) % 7)
        
        # Create datetime object for the start time
        datetime_obj = datetime.combine(target_date, start_time)

        datetime_obj = pytz.timezone("Pacific/Auckland").localize(datetime_obj)

        datetimes.append(datetime_obj)

    for dt in datetimes:

        e = Event()

        e.add('dtstart', dt)

        e.add('dtend', dt+event_length)

        e.add('summary', event[0].split(' -')[0]+" "+ event[1])

        if len(event) == 6:
            e.add('description',event[0].split(' -')[1]+", "+event[4].replace("\n",""))
        else:
            e.add('description',event[0].split(' -')[1])

        e.add('location', event[-1] )

        uid = str(uuid.uuid4())
        e.add('uid', uid)

        c.add_component(e)

f = open(datetimes[0].strftime('%Y-%m-%d')+'.ics', 'wb')
f.write(c.to_ical())
f.close()

#[ss, dayTrack, rowTrack]
#[['COMPX102-23B (TGA)', 'Laboratory 01\xa0(2023)', 'Room', 'TCBD.3.04'], 1, 9]

# ['ENGEN370-25A (HAM) - Engineering and the Environment', 'TUT 01 *D', 'Time: Wednesday 9:00am - 10:00am', 'Weeks: 9-14, 17-21', 'I.1.05']
# ['COMPX523-25A (HAM) - Machine Learning for Data Streams', 'LEC 01', 'Time: Thursday 9:00am - 11:00am', 'Weeks: 8-14, 17-21', 'Lecturers: Bifet Figuerol Albert', 'G.1.15']
# ['ENGEN370-25A (HAM) - Engineering and the Environment', 'TUT 01 *B', 'Time: Monday 10:00am - 11:00am', 'Weeks: 9-14, 17-21', 'TC.2.68']
# ['ENGEN370-25A (HAM) - Engineering and the Environment', 'TUT 01 *E', 'Time: Wednesday 10:00am - 11:00am', 'Weeks: 9-14, 17-21', 'I.G.02']
# ['COMPX523-25A (HAM) - Machine Learning for Data Streams', 'LEC 01', 'Time: Thursday 9:00am - 11:00am', 'Weeks: 8-14, 17-21', 'Lecturers: Bifet Figuerol Albert', 'G.1.15']
# ['COMPX553-25A (HAM) - Extremely Parallel Programming', 'LAB 01', 'Time: Thursday 11:00am - 1:00pm', 'Weeks: 8-14, 17-21', 'Lecturers: Wu Shaoqun', 'R.G.06']
# ['COMPX553-25A (HAM) - Extremely Parallel Programming', 'LAB 01', 'Time: Thursday 11:00am - 1:00pm', 'Weeks: 8-14, 17-21', 'Lecturers: Wu Shaoqun', 'R.G.06']
# ['COMPX301-25A (HAM) - Design and Analysis of Algorithms', 'LEC 03', 'Time: Friday 12:00pm - 1:00pm', 'Weeks: 8-14, 17-19, 21', 'Lecturers: Smith Anthony', 'L.G.04']
# ['COMPX301-25A (HAM) - Design and Analysis of Algorithms', 'LEC 02', 'Time: Tuesday 1:00pm - 2:00pm', 'Weeks: 8-14, 17-21', 'Lecturers: Smith Anthony', 'TL.2.26']
# ['ENGEN370-25A (HAM) - Engineering and the Environment', 'LEC 02', 'Time: Thursday 1:00pm - 2:00pm', 'Weeks: 8-14, 17-21', 'Lecturers: Boston Megan, Lay Mark, Kovalsky\t\t\t\t\tPeter', 'L.G.01']