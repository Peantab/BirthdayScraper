import time
import datetime
import re

TITLE_FORMAT = '{} - Urodziny'
MONDAY = 'poniedziałek'
TUESDAY = 'wtorek'
WEDNESDAY = 'środa'
THURSDAY = 'czwartek'
FRIDAY = 'piątek'
SATURDAY = 'sobota'
SUNDAY = 'niedziela'

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

    It expects the input in a file `to_scrap.txt`

    It creates the file `birthday.ics` as an output.

    To get a correct file you need to enter the website, scroll down (make it load the whole year) and copy the HTML
    from e.g Google Chrome's Inspector (the "show source" won't load the whole year). For script to work correctly,
    you need to have HTML from the same day you run the script!

    If you use Facebook in other language than Polish, fill weekday constants at the top of the script
    to match your locale.

    You can modify events' name template by editing `TITLE_FORMAT` variable at the top of this script.
    """

    now = time.localtime()
    now_str = time.strftime(DATETIME_FORMAT, now)
    year = str(now.tm_year)

    # data-tooltip-content="Name Surname (day.month)"
    regex_date = re.compile(r'data-tooltip-content="((?:\w+ ){1,2}[\w-]+) \((\d+)\.(\d+)\)"')
    # data-tooltip-content="Name Surname (weekday)"
    regex_weekday = re.compile(r'data-tooltip-content="((?:\w+ ){1,2}[\w-]+) \((\w+)\)"')

    with open('birthday.ics', 'w', encoding="utf8") as calendar, open('to_scrap.txt', 'r', encoding="utf8") as source:
        source_str = " ".join(source.readlines())

        matched_date = regex_date.findall(source_str)
        matched_date = list(set(matched_date))

        matched_weekday = regex_weekday.findall(source_str)
        matched_weekday = list(set(matched_weekday))
        weekdays = get_weekday_offsets()
        matched_date.extend(map(lambda m: convert_weekday_to_date_tuple(m, weekdays), matched_weekday))

        matched_date.sort(key=lambda p: int(p[2])*100+int(p[1]))

        calendar.write(START)

        print("Calendar entries to generate: {}".format(len(matched_date)))

        for index, entry in enumerate(matched_date):
            print('name: ' + entry[0] + ', day: ' + str(int(entry[1])) + ', month: ' + str(int(entry[2])))

            title = TITLE_FORMAT.format(entry[0])
            # 19991231 (31-12-1999)
            formatted_birthday = year + '{:0=2}'.format(int(entry[2])) + '{:0=2}'.format(int(entry[1]))
            calendar.write(EVENT_TEMPLATE.format(now_str, formatted_birthday, title, index))
        calendar.write(END)


def get_weekday_offsets():
    weekdays = [(MONDAY, 0), (TUESDAY, 1), (WEDNESDAY, 2), (THURSDAY, 3), (FRIDAY, 4), (SATURDAY, 5), (SUNDAY, 6)]
    weekday_today = time.localtime().tm_wday
    shifted_weekdays = map(lambda d: (d[0], (d[1] - weekday_today) % 7), weekdays)
    shifted_weekdays_1_7 = map(lambda d: (d[0], 7) if d[1] == 0 else d, shifted_weekdays)
    return dict((x, y) for (x, y) in shifted_weekdays_1_7)


def convert_weekday_to_date_tuple(birthday_pair, weekdays):
    birthday_time = datetime.datetime.now() + datetime.timedelta(days=weekdays[birthday_pair[1]])
    return birthday_pair[0], birthday_time.day, birthday_time.month


if __name__ == "__main__":
    main()
