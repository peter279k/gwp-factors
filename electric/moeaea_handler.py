import os
import re
import sys
import requests
import pdftotext
from bs4 import BeautifulSoup


keyword = '年度電力排碳係數'
url = 'https://www.moeaea.gov.tw/ecw/populace/content/ContentDesc.aspx?menu_id=26391'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
response = requests.get(url, headers=headers)

if response.ok is False:
    print('Request the %s is failed!' % url)
    print('HTTP status code is not 200, ' + str(repsonse.status_code))
    sys.exit(1)

if keyword not in response.text:
    print('No electric CO2e message found!')
    sys.exit()


prefix_url = 'https://www.moeaea.gov.tw/ecw/populace/'

soup = BeautifulSoup(response.text, 'html.parser')
message_links = soup.select('ul.menu_list > li > a')
co2e_links = []

for message_link in message_links:
    if keyword in message_link.string:
        co2e_links += message_link['href'],

if len(co2e_links) == 0:
    print('The co2e_link is not found.')
    sys.exit(0)


pdf_file_id = 'ctl00_holderContent_wUctlContentDesc_repFiles_ctl01_repFileTypes_ctl00_lnkFiles'
for co2e_link in co2e_links:
    co2e_link = prefix_url + co2e_link.replace('../', '')
    print('The %s PDF file link is found.' % co2e_link)

    response = requests.get(co2e_link, headers=headers)

    if response.ok is False:
        print('Request the %s is failed!' % url)
        print('HTTP status code is not 200, ' + str(repsonse.status_code))
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_file_link = soup.select_one('a#' + pdf_file_id)['href']
    pdf_file_link = pdf_file_link.replace('../', '')
    pdf_file_link = prefix_url + pdf_file_link

    response = requests.get(pdf_file_link, headers=headers)
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
    factor_pdf_line = pdf_lines[3]
    if factor_pdf_line == '':
        factor_pdf_line = pdf_lines[4]
    co2e_value = factor_pdf_line.replace(' ', '').split('公斤')[0]
    csv_line = co2e_year + ',' + co2e_value + '\n'

    ele_csv_path = './datasets/electric_co2e.csv'
    f_handler = open(ele_csv_path, 'r')
    last_years = []
    contents = f_handler.readlines()
    for content in contents:
        last_years += content.split(',')[0],
    if co2e_year in last_years:
        print('%s year is existed. Stopped.' % co2e_year)
        f_handler.close()
        if os.path.isfile(local_filename) is True:
            os.remove(local_filename)

        continue

    f_handler = open(ele_csv_path, 'a')
    f_handler.write(csv_line)
    f_handler.close()

    print('The electric_co2e.csv file is updated.')

    if os.path.isfile(local_filename) is True:
        os.remove(local_filename)
