# Birthday Scrapper

by Paweł Taborowski

Script for scraping an HTML file of Facebook's birthdays: https://www.facebook.com/events/birthdays/

To get a correct file you need to enter the website, scroll down (make it load the whole year) and copy the HTML
from e.g Google Chrome's Inspector.

You can modify events' name template by editing `TITLE_FORMAT` variable at the top of the script.

It expects the input in a file `to_scrap.txt`

It creates the file `birthday.ics` as an output.