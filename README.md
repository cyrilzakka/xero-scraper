# xero-scraper
A simple web-scraper for [Xero Image Viewer](https://global.agfahealthcare.com/main/enterprise-imaging/universal-viewer/) that automatically downloads standard-view mammograms (R CC, L CC, R MLO, L MLO) and their accompanying reports, given patient accession numbers. 

## Usage
### Installation
You will need:
* [Python 3](https://www.python.org/downloads/)
* Credentials to a licensed [Xero Image Viewer](https://global.agfahealthcare.com/main/enterprise-imaging/universal-viewer/) point of access.

```shell
$ git clone https://github.com/cyrilzakka/xero-scraper.git
$ cd xero-scraper

# Install requirements
$ pip install scrapy
$ pip install pandas
```

### How to Run
* Fill your credentials into [`xero_downloader.py`](https://github.com/cyrilzakka/xero-scraper/blob/master/xero/spiders/xero_downloader.py). The `SOURCE_CSV` should point to a `CSV` file containing a column with accession numbers, under a header labeled `accession_number`.
```
USER_NAME = 'username'
PASSWORD = 'password'
ROOT_URL = 'https://xero.yourorganization.org/'
SOURCE_CSV = '/Directory/To/Input_File.csv'
```
* Edit the required fields in [`settings.py`](https://github.com/cyrilzakka/xero-scraper/blob/master/xero/settings.py). The files will be downloaded to a directory specified by `FILES_STORE`. A record of all images and their labels is kept in a `CSV` file specified by `FEED_URI`.
```
# Configure Files Pipeline
FILES_STORE = '/Target/Directory/For/Downloaded/Files/'
FEED_URI = '/Directory/To/Target/ImagesAndLabels.csv'
```
* Run the script:
```
scrapy crawl xero
```

## Disclaimer
`xero-script` was developed first and foremost for personal use, to streamline and simplify research in medical machine learning. The project is offered “as-is”, without warranty, and disclaiming liability for damages resulting from use.

With that being said, all contributions to improve `xero-script` are welcome. 