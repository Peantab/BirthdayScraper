import time
import re

TITLE_FORMAT = '{} - Urodziny'

START = """BEGIN:VCALENDAR
PRODID:-//Paweł Taborowski//BirthdayScraper//PL
VERSION:2.0
CALSCALE:GREGORIAN
"""

END = '\nEND:VCALENDAR'

EVENT_TEMPLATE = """
BEGIN:VEVENT
DTSTAMP:{0}
DTSTART;VALUE=DATE:{1}
SUMMARY:{2}
DESCRIPTION:{2}
RRULE:FREQ=YEARLY
UID:PTBS-{0}-{3}
END:VEVENT
"""

DATETIME_FORMAT = '%Y%m%dT%H%M%S'


def main():
    """
    Script for scraping an HTML file of Facebook's birthdays: https://www.facebook.com/events/birthdays/

    To get a correct file you need to enter the website, scroll down (make it load the whole year) and copy the HTML
    from e.g Google Chrome's Inspector.

    You can modify events' name template by editing `TITLE_FORMAT` variable at the top of this script.

    It expects the input in a file `to_scrap.txt`

    It creates the file `birthday.ics` as an output.
    """

    now = time.strftime(DATETIME_FORMAT, time.localtime())
    year = str(time.localtime().tm_year)

    # data-tooltip-content="Name Surname (day.month)"
    regex = re.compile(r'data-tooltip-content="((?:\w+ ){1,2}[\w-]+) \((\d+)\.(\d+)\)"')
    with open('birthday.ics', 'w', encoding="utf8") as calendar, open('to_scrap.txt', 'r', encoding="utf8") as source:
        calendar.write(START)
        source_str = " ".join(source.readlines())
        matched = regex.findall(source_str)
        matched = list(set(matched))
        matched.sort(key=lambda p: int(p[2])*100+int(p[1]))
        for index, entry in enumerate(matched):
            print('name: ' + entry[0] + ' day: ' + str(int(entry[1])) + ' month: ' + str(int(entry[2])))

            title = TITLE_FORMAT.format(entry[0])
            # 19991231 (31-12-1999)
            formatted_birthday = year + '{:0=2}'.format(int(entry[2])) + '{:0=2}'.format(int(entry[1]))
            calendar.write(EVENT_TEMPLATE.format(now, formatted_birthday, title, index))
        calendar.write(END)


if __name__ == "__main__":
    main()
