import os
import sys
import requests
from bs4 import BeautifulSoup


print('Download latest GWP factor file from EPA is started')
file_url = 'https://ghgregistry.epa.gov.tw/ghg_rwd/Main/Tool/Tool_1?Type=1'
download_file_url = 'https://ghgregistry.epa.gov.tw/upload/Tools/'

response = requests.get(file_url)
soup = BeautifulSoup(response.text, 'html.parser')
spans = soup.select('span')
keyword = '溫室氣體排放係數管理表'
ods_keyword = 'ODS檔'
download_files = []
for span in spans:
    if span.string is None:
        continue
    if keyword in span.string and ods_keyword in span.string:
        ods_filename = span.string.replace('（ODS檔）', '')
        ods_filename += '.ods'
        if os.path.isfile('./datasets/' + ods_filename) is False:
            print(ods_filename + ' file is not found.')
            download_files.append(ods_filename)


for download_file in download_files:
    response = requests.get(download_file_url + download_file)
    f_handler = open('./datasets/' + download_file, 'wb')
    for chunk in response.iter_content():
        if chunk:
            f_handler.write(chunk)
    f_handler.close()
    print('The ' + download_file + ' file has been saved.')

print('Download latest GWP factor file from EPA is done')
