# Waikato-WebTableICS

Quick python script to pull the table from [timetable.waikato.ac.nz](timetable.waikato.ac.nz) and convert / assemble into an ICS file that can be imported into any digital calendar software

Demo use case
-
- I create [my timetable](https://timetable.waikato.ac.nz/perl-bin/timetable.pl?term=COMPX102-23B+%28TGA%29+COMPX310-23B+%28TGA%29+MATHS135-23B+%28TGA%29+ENGEN180-23B+%28TGA%29&submit=Create&action=Create&year=2023) by adding my papers in the waikato university timetable site
- copy the timetable link into URL on line 4 of the script
- set the start_dt to the monday of the week before i want the events to start
- change weeks to the number of weeks to repeat the events for
- run the script
- open [outlook.live.com/calendar](outlook.live.com/calendar)
- add calendar, upload from file 
- Warning, add the events to a new empty calendar just in case something has gone wrong [painful to delete the events 1 by 1 because the cal has other events you want to keep]
