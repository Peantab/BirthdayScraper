# Birthday Scraper

by Paweł Taborowski

Script for scraping an HTML file of Facebook's birthdays: https://www.facebook.com/events/birthdays/

It expects the input in a file `to_scrap.txt`

It creates the file `birthday.ics` as an output, which you can import into your favourite calendar app
(e.g. *Google Calendar*, Windows' *Calendar* app, *Outlook*).

To get a correct file you need to enter the website, scroll down (make it load the whole year) and copy the HTML
from e.g Google Chrome's Inspector (the "show source" won't load the whole year). For script to work correctly,
you need to have HTML from the same day you run the script!

If you use Facebook in other language than Polish, fill weekday constants at the top of the script
to match your locale (e.g. `MONDAY = 'monday'`).

You can modify events' name template by editing `TITLE_FORMAT` variable at the top of this script.