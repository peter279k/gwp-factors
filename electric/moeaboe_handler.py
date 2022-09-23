import os
import re
import sys
import requests
import pdftotext
from bs4 import BeautifulSoup


keyword = '年度電力排碳係數'
url = 'https://www.moeaboe.gov.tw/ECW/populace/news/Board.aspx?kind=3&menu_id=57'
response = requests.get(url)

if response.ok is False:
    print('Request the %s is failed!' % url)
    print('HTTP status code is not 200, ' + str(repsonse.status_code))
    sys.exit(1)

if keyword not in response.text:
    print('No electric CO2e message found!')
    sys.exit()


prefix_url = 'https://www.moeaboe.gov.tw/ECW/'

soup = BeautifulSoup(response.text, 'html.parser')
message_links = soup.select('ul.NewsMain > li > a')
co2e_link = ''

for message_link in message_links:
    if keyword in message_link.string:
        co2e_link = message_link['href']
        break

if co2e_link == '':
    print('The co2e_link is not found.')
    sys.exit(0)

co2e_link = prefix_url + co2e_link.replace('../', '')
print('The %s PDF file link is found.' % co2e_link)

pdf_file_id = 'ctl00_holderContent_wUctlNewsDetail_repFiles_ctl01_repFileTypes_ctl00_lnkFiles'

response = requests.get(co2e_link)

if response.ok is False:
    print('Request the %s is failed!' % url)
    print('HTTP status code is not 200, ' + str(repsonse.status_code))
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
pdf_file_link = soup.select_one('a#' + pdf_file_id)['href']

response = requests.get(pdf_file_link)
content_dis = response.headers['Content-Disposition']
regex = re.compile('\d+')
matched = regex.findall(content_dis)
co2e_year = matched[0]

local_filename = 'co2e_value.pdf'
f_handler = open(local_filename, 'wb')
for chunk in response.iter_content():
    if chunk:
        f_handler.write(chunk)
f_handler.close()

print('The %s PDF file has been saved.' % local_filename)

pdf = pdftotext.PDF(open(local_filename, 'rb'))
pdf_lines = pdf[0].split('\n')
co2e_value = pdf_lines[3].replace(' ', '').split('公斤')[0]
csv_line = co2e_year + ',' + co2e_value + '\n'

ele_csv_path = './datasets/electric_co2e.csv'
f_handler = open(ele_csv_path, 'r')
last_year = f_handler.readlines()[-1].split(',')[0]
if last_year == co2e_year:
    print('%s year is existed. Stopped.' % last_year)
    f_handler.close()
    if os.path.isfile(local_filename) is True:
        os.remove(local_filename)
    sys.exit()

f_handler = open(ele_csv_path, 'a')
f_handler.write(csv_line)
f_handler.close()

print('The electric_co2e.csv file is updated.')

if os.path.isfile(local_filename) is True:
   os.remove(local_filename)
