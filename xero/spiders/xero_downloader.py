import scrapy
import json
import pandas as pd

from xero.items import XeroItem

USER_NAME = 'username'
PASSWORD = 'password'
ROOT_URL = 'https://xero.yourorganization.org/'
SOURCE_CSV = '/Directory/To/Input_File.csv'

# Miscellaneous
IMG_SIZE = '1024' # Requests an image of this width from server before downloading. 
n_rows = None # Download the first n_rows from source CSV. Set to 'None' to download all. 
skip_rows = None # Skip n_rows in source CSV. Set to 'None' to begin from the start.

def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)
    return results

class XeroSpider(scrapy.Spider):
    name = 'xero'
    start_urls = [ROOT_URL]

    def parse(self, response):
        return scrapy.FormRequest.from_response(response, formname='loginForm', formdata={'user': USER_NAME, 'password': PASSWORD},
                                                callback=self.find_accession)

    def find_accession(self, response):
        self.logger.info('Loading accession numbers from file...')
        df = pd.read_csv(SOURCE_CSV, nrows=n_rows, skiprows=(1,skip_rows))
        accession_numbers = df['accession_number'].tolist()
        for i in accession_numbers:
            yield scrapy.FormRequest(url=f'{ROOT_URL}wado/?v=1.0.0.R812SP3HF_v20180718_1223&requestType=STUDY&contentType=text/javascript&maxResults=250&AccessionNumber={i}&ae=local&IssuerOfPatientID=&groupByIssuer=*&suppressReportFlags=PRELIMINARY&language=en_US&theme=theme,XeroCreator',
                                     callback=self.load_data)

    def load_data(self, response):
        STUDY_UID = find_values('studyUID', response.body_as_unicode())[0]
        yield scrapy.FormRequest(url=f'{ROOT_URL}wado/?v=1.0.0.R812SP3HF_v20180718_1223&requestType=IMAGE&contentType=text/javascript&regroup=*&studyUID={STUDY_UID}&Position=0&Count=256&fromHeader=true&suppressReportFlags=PRELIMINARY&ae=local&ver=9.9.MGSR.rt&language=en_US&theme=theme,XeroCreator',
                                 callback=self.scrape_data)

    def scrape_data(self, response):
        item = XeroItem()
        urls = []

        STUDY_UID = find_values('studyUID', response.body_as_unicode())[0]
        item['study_uid'] = STUDY_UID
        self.logger.info('Downloading resources for %s...', STUDY_UID)

        valid_mammos = list(filter(lambda x: x.count(' ') == 1 and x.split(':')[0] in ['R MLO' , 'R CC', 'L MLO' , 'L CC'], find_values('seriesUID', response.body_as_unicode())))
        valid_objects = find_values('objectUID', response.body_as_unicode())
        if len(valid_mammos) >= 1:
            for i, j in enumerate(valid_mammos):
                MAMMO_TYPE, SERIES_UID = j.split(':')
                OBJECT_UID = valid_objects[i]
                mammo = f'{ROOT_URL}wado/?v=1.0.0.R812SP3HF_v20180718_1223&requestType=XERO&studyUID={STUDY_UID}&seriesUID={SERIES_UID}&language=en_US&objectUID={OBJECT_UID}&columns={IMG_SIZE}&ae=local&v=1.0.0.R812SP3HF_v20180718_1223'
                urls.append(mammo)
                item[MAMMO_TYPE.lower().replace(" ", "_")] = SERIES_UID

        report = f'{ROOT_URL}wado/proxy/default/ris/web/reporting/report?studyUID={STUDY_UID}&agilityToken=&ae=local&validated=true&template=customLight&language=en_US&theme=theme,XeroCreator'
        urls.append(report)

        item['file_urls'] = urls

        yield item
