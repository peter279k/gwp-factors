import os
import re
import sys
import requests
import tempfile
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup


def recognize_captcha(captcha_img_path):
    image = Image.open(captcha_img_path)
    image = image.convert('L')
    threshold = 50
    table = []
    for i in [*range(256)]:
        if i < threshold:
            table.append(0)
        else:
            table.append(i)

    image = image.point(table, '1')
    grey_scale_img = tempfile.gettempdir() + '/greyscale.jpg'
    image.save(grey_scale_img)

    result = pytesseract.image_to_string(image)
    pattern = re.compile('\d+')

    os.remove(captcha_img_path)
    os.remove(grey_scale_img)

    matched = pattern.findall(result)

    if len(matched) == 0:
        return False

    return matched[0]


def cfp_login(user_name, user_password):
    request = requests.Session()
    cfp_cal_url = 'https://cfp-calculate.tw/cfpc/WebPage/LoginPage.aspx'
    cfp_captcha_url = 'https://cfp-calculate.tw/cfpc/'

    login_response = request.get(cfp_cal_url)
    soup = BeautifulSoup(login_response.text, 'html.parser')
    post_data = {
        '__VIEWSTATE': '',
        '__VIEWSTATEENCRYPTED': '',
        '__VIEWSTATEGENERATOR': 'C8B91BE1',
        '__EVENTVALIDATION': '',
        'ctl00$ContentPlaceHolder1$tbx_MemberAt': '',
        'ctl00$ContentPlaceHolder1$tbx_MemberMima': '',
        'ctl00$ContentPlaceHolder1$tbx_ValidateNumber': '',
        'ctl00$ContentPlaceHolder1$btn_Login': '登入',
        'ctl00$ContentPlaceHolder1$hf_cooperation_countset': '5',
    }
    view_state = soup.select_one('input#__VIEWSTATE')
    event_validation = soup.select_one('input#__EVENTVALIDATION')
    captcha_path = soup.select_one('img[name="imgCode"]').get('src')

    cfp_captcha_response = request.get(cfp_captcha_url + captcha_path[3:])
    captcha_img_path = tempfile.gettempdir() + '/captcha.jpg'
    with open(captcha_img_path, 'wb') as f:
        f.write(cfp_captcha_response.content)

    captcha_number = recognize_captcha(captcha_img_path)
    if captcha_number is False:
        return False

    post_data['__VIEWSTATE'] = view_state.get('value')
    post_data['__EVENTVALIDATION'] = event_validation.get('value')
    post_data['ctl00$ContentPlaceHolder1$tbx_MemberAt'] = user_name
    post_data['ctl00$ContentPlaceHolder1$tbx_MemberMima'] = user_password
    post_data['ctl00$ContentPlaceHolder1$tbx_ValidateNumber'] = captcha_number

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'https://cfp-calculate.tw',
        'Referer': 'https://cfp-calculate.tw/cfpc/WebPage/LoginPage.aspx',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    login_response = request.post(cfp_cal_url, data=post_data, headers=headers)

    return [login_response.text, request, headers]


cfp_auth_path = './cfp_auth.txt'
if os.path.isfile(cfp_auth_path) is False:
    print('Please create the %s firstly.' % cfp_auth_path)
    sys.exit(1)

with open(cfp_auth_path, 'r') as file_handler:
    auth_info = file_handler.read()
    auth_info_arr = auth_info.split('\n')
    user_name = auth_info_arr[0]
    user_password = auth_info_arr[1]


index = 0
retry_counter = 3
login_success = False
while index < retry_counter:
    login_responses = cfp_login(user_name, user_password)
    if login_responses is False or '登出' not in login_responses[0]:
        print('Login is failed')
        index += 1
    else:
        login_success = True
        break

if login_success is False:
    print('Login is failed and retrying count is three times!')
    sys.exit(1)


print('Fetch overviewed factors PDF file is started!')
co2e_url = 'https://cfp-calculate.tw/cfpc/WebPage/WebSites/CoefficientDB.aspx'

pdf_request = login_responses[1]
co2e_response = pdf_request.get(co2e_url) 

soup = BeautifulSoup(co2e_response.text, 'html.parser')
view_state = soup.select_one('input#__VIEWSTATE')
event_validation = soup.select_one('input#__EVENTVALIDATION')

headers = login_responses[2]
headers['Referer'] = co2e_url
headers['Accept-Language'] = 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'

post_data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE': '',
    '__VIEWSTATEGENERATOR': 'C294CB5F',
    '__VIEWSTATEENCRYPTED': '',
    '__EVENTVALIDATION': '',
    'ctl00$ContentPlaceHolder1$CoefficientData_Tab$ddlCat': '',
    'ctl00$ContentPlaceHolder1$CoefficientData_Tab$ddlSub': '',
    'ctl00$ContentPlaceHolder1$CoefficientData_Tab$txt_keyword': '',
    'ctl00$ContentPlaceHolder1$CoefficientData_Tab$btnDown1': '下載',
}

post_data['__VIEWSTATE'] = view_state.get('value')
post_data['__EVENTVALIDATION'] = event_validation.get('value')


pdf_file_path = './datasets/cfp_factors.pdf' 
pdf_response = pdf_request.post(co2e_url, data=post_data, headers=headers)
with open(pdf_file_path, 'wb') as f:
    f.write(pdf_response.content)

print('%s is saved in datasets folder!' % pdf_file_path)
