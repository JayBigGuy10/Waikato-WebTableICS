import ics

from html.parser import HTMLParser

lines = []


class MyHTMLParser(HTMLParser):
    write = False
    def handle_starttag(self, tag, attrs):
        
        if tag == "table":
            self.write = True
        
        if self.write:
            lines.append(tag)
            lines.append(attrs)
            print("Encountered a start tag:", tag, attrs)


    def handle_endtag(self, tag):
        
        if tag == "table":
            self.write = False
        if self.write:
            lines.append(tag)
            print("Encountered an end tag :", tag)

    def handle_data(self, data):
        
        if self.write:
            lines.append(data)
            print("Encountered some data  :", data)

parser = MyHTMLParser()

import urllib.request

fp = urllib.request.urlopen("https://timetable.waikato.ac.nz/perl-bin/timetable.pl?term=COMPX102-23B+%28TGA%29+COMPX310-23B+%28TGA%29+MATHS135-23B+%28TGA%29+ENGEN180-23B+%28TGA%29&submit=Create&action=Create&year=2023")
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

parser.feed(mystr)