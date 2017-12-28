# FERC Document Trail
#### Grant Project funded by the Fund for Multimedia Documentation
#### of Engaged Learning, The New School.
#### Project supervisor: Stephen Metts

## General Information

The aim of this project is to assist with extraction of documents submitted to
the Federal Energy Regulatory Commission
([FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp)) and issued by
[FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp).

The purpose of this project is to provide tools for extracting all the meta data
and documents relating to the documents that can be found in
[FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp) online library
available for public access. The tools provided in this repository allow to pass
a string to the search query (search by some text such as "pipeline") and/or a
docket that has been assigned to a specific project (or a list of dockets).

The way [FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp) handles
HTML pages is not very friendly for the conventional means of web scraping.
Links are not links, file links don't actually point to the
existing files. Every link generates either a GET or POST HTTP request and such
request is processed by the
[FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp) server.
This scraper does all the HTTP request work by itself and yields traditionally
acceptable output.

## Installation

Clone the repository the regular way of cd'ing into a directory of choice and
issuing the regular git clone command

```
cd Users/username
git clone https://github.com/ilyaperepelitsa/FERC_DOC_TRAIL.git
cd FERC_DOC_TRAIL
```

This project relies on [Scrapy](https://scrapy.org) platform designed by
[Scrapinghub](https://scrapinghub.com). Scrapy is an advanced tool and it's open
source although credit is due for maintaining such a useful tool.

The only other external library that this project relies on is a library that
was created for [Scrapy](https://scrapy.org) and is called
[scrapy-fake-useragent](https://github.com/alecxe/scrapy-fake-useragent). This
library creates fake headers for requests so that requests look like they are
coming from random browsers.
[FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp) bans high
volume of requests coming in
frequently. The fake browser headers is just one step away from getting banned.
In order to install both libraries type:

```
pip3 install scrapy
pip3 install scrapy-fake-useragent
```

## Setup
Before starting the project - open the repository folder that you cloned and go
to the **FERC** folder that contains the **spiders** folder. Open the
**fercgov.py**
file with a text editor and go to line 30 for general info and description.
After reading the description navigate to lines **104** and **107** - your search
parameters are there. The docket parameter **HAS** to be a list even if it has one
or zero dockets (empty list). Respectively, variable **search** has to be a
string, current version of this project doesn't support a list of strings since
it mimics the basic functionality of
[FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp) search form.

Make sure that the search parameters are the ones that you need (for the
project(s) that you're inquiring about).

The **settings** file in the FERC directory has the setting:
``` python
DOWNLOAD_DELAY = 5
```
By default this project is ethical towards the
[FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp) servers - 5
seconds is a
good enough delay ([Scrapy](https://scrapy.org) processes this default delay
with some randomization so that delays look more realistic) that shouldn't cause
the servers to go down and consume much of processing power by overloading. You
can manually change it to higher or lower numbers (down to 0) depending on your
project. **This setting is your responsibility**, consider yourself warned.

## Launch
After installing the libraries, just cd into the directory of the repository
that you cloned and issue the following command in the terminal:

```
scrapy crawl fercgov
```
fercgov is the name of the spider that is used to send requests and record the
activity + download files. It is different from the regular sctructure of
[Scrapy](https://scrapy.org) project where the item is generated and passed
through a pipeline. This is due to the fact that an item is populated across
multiple nodes that are traversed via new requests (data from previous pages is
passed to such requests), in addition the regular
[Scrapy](https://scrapy.org) file download pipelines don't work - the file links
are internal links to be processed by the server, they don;t actually point to
files directly.

## Convert to CSV
The script writes its output to a **log.json** located in the
**FERC_DOC_TRAIL/FERC**
directory. JSON was intentionally used as one of the easiest wide-spread formats
to use (requires no database setup and is easily parsable with python when we
need to determine whether entries exist) however one may prefer to work with CSV
since it's readable by Excel and is preferable in the office environment. To
duplicate the log file run the following commands:
```
cd FERC
python3 process_to_csv.py
```
If you just ran the main spider script - you're already in **FERC_DOC_TRAIL** directory
therefore you **cd** only once again (as noted in the code above) to get to
**FERC_DOC_TRAIL/FERC**

## Random important details
* Do not launch the scraper on weekends. I think someone physically turns off
the server - no request returns any response
* [FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp) bans for some
noticeable time - the easiest way to check is to simulate a query in a browser
  * Think about your requests in advance - if you play with the scraper for too
long and get banned you will have to wait for the ban to go down. Use it only
for the requess that you are sure about (tested docket numbers, proper search
strings etc.)


P.S. I will be updating this section later - it takes time to remember all the
details
