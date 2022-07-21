import os
import sys
import pdftotext


factor_pdf_file = './datasets/cfp_factors.pdf'
print('Parsing the %s is started!' % factor_pdf_file)

if os.path.isfile(factor_pdf_file) is False:
    print('The %s PDF file is not found.' % factor_pdf_file)
    sys.exit(1)

with open(factor_pdf_file, 'rb') as f:
    pdf_contents = pdftotext.PDF(f)


keywords = ['揭露項目', '內容']

csv_tw_head = '中文名稱,碳足跡數值,碳足跡數值單位,數量,宣告單位,生命週期範疇(系統邊界),盤查起迄日'
csv_head = 'ch_name,co2e_value,co2e_unit,amount,declared_unit,lifecycle_boundary,checked_date_range'

head_arr = csv_tw_head.split(',')
csv_contents = csv_head + '\n'
csv_file_path = './datasets/cfp_factors.csv'

for pdf_content in pdf_contents:
    page_arr = pdf_content.split('\n')
    if len(page_arr) < 1:
        continue
    check_item_row = page_arr[0]
    if check_item_row.count(keywords[0]) != 1 and check_item_row.count(keywords[1]) != 1:
        continue
    item_ch_name = page_arr[1].replace(' ', '').replace(head_arr[0], '')
    index = 4
    while head_arr[1] not in page_arr[index]:
        index += 1

    co2e_val_info = page_arr[index].replace(head_arr[1], '').split(' ')
    co2e_value = co2e_val_info[-2]
    co2e_unit = co2e_val_info[-1]

    index = 5
    while head_arr[3] not in page_arr[index]:
        index += 1

    amount = page_arr[index].replace(' ', '').replace(head_arr[3], '')

    while head_arr[4] not in page_arr[index]:
        index += 1

    declared_unit = page_arr[index].replace(head_arr[4], '').replace(' ', '')

    index = 5
    life_cycle_keyword = '生命週期範疇'
    while life_cycle_keyword not in page_arr[index]:
        index += 1

    life_cycle_boundary = page_arr[index].replace(' ', '').replace(life_cycle_keyword, '')

    index = 8
    while head_arr[6] not in page_arr[index]:
        index += 1

    checked_date = page_arr[index].replace(' ', '').replace(head_arr[6], '')

    csv_row = '"%s",%s,%s,%s,%s,%s,%s\n' % (
        item_ch_name,
        co2e_value,
        co2e_unit,
        amount,
        declared_unit,
        life_cycle_boundary[0:5],
        checked_date,
    )

    csv_contents += csv_row

with open(csv_file_path, 'w') as f:
    f.write(csv_contents)

print('Parsing the %s PDF file is done.\nThe %s CSV file is saved in dataserts folder.' % (
    factor_pdf_file,
    csv_file_path,
))
